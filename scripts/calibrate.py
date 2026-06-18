#!/usr/bin/env python3
"""
calibrate.py — calibrar as constantes da fórmula xG usando resultados reais.

Loss function: Poisson NLL (gols são contagens — distribuição correta).
  NLL = Σ [ xG_pred - k × log(xG_pred) ]   para cada placar real k

Parâmetros livres (4):
  θ = [BASE_XG, w_att, w_def, w_gk]

  Derivados (restrição soma=1):
    OFF_MID_W = 1 - w_att
    RES_MID_W = 1 - w_def - w_gk

Bounds:
  BASE_XG ∈ (0.5, 4.0)
  w_att   ∈ (0.1, 0.9)
  w_def   ∈ (0.1, 0.8)
  w_gk    ∈ (0.05, 0.5)

Validação: LOO-CV (leave-one-out) — calibra nos N-1 jogos, prediz o deixado de fora.
Métrica secundária: Brier Score por outcome (mais interpretável para comparação).

Uso:
    python3 scripts/calibrate.py

O script NÃO altera nenhum arquivo — só imprime os valores sugeridos.
"""

import json
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy.optimize import minimize
from scipy.stats import poisson as sp_poisson

STATE_FILE   = "output/copa_real_state.json"
SCORES_FILE  = "output/team_scores.json"
OUT_FILE     = "output/calibrated_weights.json"
REPORT_FILE  = "output/calibration_report.png"

FALLBACK  = 0.5
RES_FLOOR = 0.10
MAX_XG    = 8.0
MAX_GOALS = 12

# θ₀ = valores atuais como ponto de partida
DEFAULTS = [1.30, 0.70, 0.60, 0.20]   # [BASE_XG, w_att, w_def, w_gk]
BOUNDS   = [(0.50, 4.00), (0.10, 0.90), (0.10, 0.80), (0.05, 0.50)]

_DISPLAY = {
    'united_states_of_america': 'USA',
    'republic_of_korea':        'South Korea',
    'bosnia_and_herzegovina':   'Bosnia',
    'cape_verte':               'Cape Verde',
    'ivory_coast':              "Côte d'Ivoire",
    'ira':                      'Iran',
    'new_zealand':              'New Zealand',
    'saudi_arabia':             'Saudi Arabia',
    'south_africa':             'South Africa',
    'czech_republic':           'Czech Rep.',
}


def dn(t):
    return _DISPLAY.get(t, t.replace('_', ' ').title())


def _get(s, key):
    v = s.get(key)
    return v if v is not None else FALLBACK


def compute_xg(s_a, s_b, theta):
    base_xg, w_att, w_def, w_gk = theta
    w_mid_off = 1.0 - w_att
    w_mid_res = max(1.0 - w_def - w_gk, 0.05)

    off_a = w_att * _get(s_a, 'attack')  + w_mid_off * _get(s_a, 'midfield')
    off_b = w_att * _get(s_b, 'attack')  + w_mid_off * _get(s_b, 'midfield')
    res_a = max(w_def * _get(s_a, 'defense') + w_gk * _get(s_a, 'goalkeeper') + w_mid_res * _get(s_a, 'midfield'), RES_FLOOR)
    res_b = max(w_def * _get(s_b, 'defense') + w_gk * _get(s_b, 'goalkeeper') + w_mid_res * _get(s_b, 'midfield'), RES_FLOOR)
    return min(base_xg * off_a / res_b, MAX_XG), min(base_xg * off_b / res_a, MAX_XG)


def poisson_nll(theta, matches, scores):
    """NLL = Σ [ xg - k*log(xg) ] para cada placar (xg, k)."""
    total = 0.0
    for m in matches:
        xg_a, xg_b = compute_xg(scores[m['team_a']], scores[m['team_b']], theta)
        total += xg_a - m['goals_a'] * np.log(max(xg_a, 1e-9))
        total += xg_b - m['goals_b'] * np.log(max(xg_b, 1e-9))
    return total


def calibrate(matches, scores, x0=None):
    x0 = x0 or DEFAULTS[:]
    res = minimize(
        lambda t: poisson_nll(t, matches, scores),
        x0=x0,
        bounds=BOUNDS,
        method='L-BFGS-B',
        options={'maxiter': 2000, 'ftol': 1e-12},
    )
    return res.x.tolist(), res.fun


# ── Brier Score como métrica secundária de interpretação ─────────────────────

def match_probs(xg_a, xg_b):
    pa = np.array([sp_poisson.pmf(k, xg_a) for k in range(MAX_GOALS + 1)])
    pb = np.array([sp_poisson.pmf(k, xg_b) for k in range(MAX_GOALS + 1)])
    m  = np.outer(pa, pb)
    win_a = float(np.tril(m, -1).sum())
    draw  = float(np.trace(m))
    win_b = float(np.triu(m, 1).sum())
    total = win_a + draw + win_b
    return win_a / total, draw / total, win_b / total


def brier(probs, outcome):
    actual = {'a': (1, 0, 0), 'draw': (0, 1, 0), 'b': (0, 0, 1)}[outcome]
    return sum((p - o) ** 2 for p, o in zip(probs, actual))


# ── LOO-CV ────────────────────────────────────────────────────────────────────

def loo_cv(matches, scores):
    n = len(matches)
    nll_def, nll_cal   = [], []
    brier_def, brier_cal = [], []

    for i in range(n):
        train = [m for j, m in enumerate(matches) if j != i]
        test  = matches[i]
        cal_theta, _ = calibrate(train, scores)

        sa, sb = scores[test['team_a']], scores[test['team_b']]

        for theta, nll_list, brier_list in [
            (DEFAULTS, nll_def, brier_def),
            (cal_theta, nll_cal, brier_cal),
        ]:
            xg_a, xg_b = compute_xg(sa, sb, theta)
            nll = (xg_a - test['goals_a'] * np.log(max(xg_a, 1e-9)) +
                   xg_b - test['goals_b'] * np.log(max(xg_b, 1e-9)))
            nll_list.append(nll)
            brier_list.append(brier(match_probs(xg_a, xg_b), test['outcome']))

        print(f"    fold {i+1:2}/{n}  NLL def={nll_def[-1]:.3f}  cal={nll_cal[-1]:.3f}  "
              f"Brier def={brier_def[-1]:.3f}  cal={brier_cal[-1]:.3f}", flush=True)

    return nll_def, nll_cal, brier_def, brier_cal


# ── Dados ─────────────────────────────────────────────────────────────────────

def load_data():
    with open(STATE_FILE) as f:
        state = json.load(f)
    with open(SCORES_FILE) as f:
        scores = json.load(f)
    matches = []
    for grp, results in state['group_results'].items():
        for key, (ga, gb) in results.items():
            ta, tb = key.split('|')
            if ta not in scores or tb not in scores:
                print(f"  Aviso: {ta} ou {tb} não encontrado, pulando.")
                continue
            outcome = 'a' if ga > gb else ('b' if gb > ga else 'draw')
            matches.append({'team_a': ta, 'team_b': tb,
                            'goals_a': ga, 'goals_b': gb, 'outcome': outcome})
    return matches, scores


# ── Report visual ─────────────────────────────────────────────────────────────

COLORS = {'default': '#4C72B0', 'calibrated': '#DD8452', 'better': '#2CA02C', 'worse': '#D62728', 'neutral': '#888888'}

def _short(ta, tb):
    def abbr(t):
        d = {'united_states_of_america': 'USA', 'republic_of_korea': 'KOR',
             'bosnia_and_herzegovina': 'BIH', 'cape_verte': 'CPV',
             'ivory_coast': 'CIV', 'ira': 'IRN', 'new_zealand': 'NZL',
             'saudi_arabia': 'KSA', 'south_africa': 'RSA', 'czech_republic': 'CZE'}
        return d.get(t, t[:3].upper())
    return f"{abbr(ta)}-{abbr(tb)}"


def generate_report(matches, cal_theta, nll_d, nll_c, brier_d, brier_c,
                    nll_before, nll_after, mean_nll_d, mean_nll_c,
                    mean_brier_d, mean_brier_c, scores):
    labels = [_short(m['team_a'], m['team_b']) for m in matches]
    results = [f"{m['goals_a']}–{m['goals_b']}" for m in matches]
    n = len(matches)
    x = np.arange(n)
    w = 0.38

    fig = plt.figure(figsize=(20, 14))
    fig.patch.set_facecolor('#1a1a2e')
    title_color, label_color, grid_color = '#e0e0e0', '#bbbbbb', '#333355'

    fig.suptitle('Calibração xG — Rodada 1 · LOO-CV', fontsize=16,
                 color=title_color, fontweight='bold', y=0.98)

    # ── Brier Score por jogo ──────────────────────────────────────────────────
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_facecolor('#0f0f23')
    bars_d = ax1.bar(x - w/2, brier_d, w, label='Atual', color=COLORS['default'], alpha=0.85)
    bars_c = ax1.bar(x + w/2, brier_c, w, label='Calibrado', color=COLORS['calibrated'], alpha=0.85)
    ax1.axhline(mean_brier_d, color=COLORS['default'],   ls='--', lw=1.2, alpha=0.7)
    ax1.axhline(mean_brier_c, color=COLORS['calibrated'], ls='--', lw=1.2, alpha=0.7)
    ax1.set_title('Brier Score por jogo (LOO-CV)', color=title_color, fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"{l}\n{r}" for l, r in zip(labels, results)],
                        fontsize=6.5, color=label_color, rotation=45, ha='right')
    ax1.tick_params(colors=label_color)
    ax1.set_ylabel('Brier Score', color=label_color)
    ax1.legend(facecolor='#1a1a2e', labelcolor=label_color, fontsize=9)
    ax1.spines[:].set_color(grid_color)
    ax1.yaxis.grid(True, color=grid_color, alpha=0.5)
    ax1.set_axisbelow(True)

    # ── NLL por jogo ──────────────────────────────────────────────────────────
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_facecolor('#0f0f23')
    ax2.bar(x - w/2, nll_d, w, label='Atual',     color=COLORS['default'],    alpha=0.85)
    ax2.bar(x + w/2, nll_c, w, label='Calibrado', color=COLORS['calibrated'], alpha=0.85)
    ax2.axhline(mean_nll_d, color=COLORS['default'],   ls='--', lw=1.2, alpha=0.7)
    ax2.axhline(mean_nll_c, color=COLORS['calibrated'], ls='--', lw=1.2, alpha=0.7)
    ax2.axhline(0, color='white', lw=0.6, alpha=0.3)
    ax2.set_title('Poisson NLL por jogo (LOO-CV)', color=title_color, fontsize=11)
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"{l}\n{r}" for l, r in zip(labels, results)],
                        fontsize=6.5, color=label_color, rotation=45, ha='right')
    ax2.tick_params(colors=label_color)
    ax2.set_ylabel('NLL (menor = melhor)', color=label_color)
    ax2.legend(facecolor='#1a1a2e', labelcolor=label_color, fontsize=9)
    ax2.spines[:].set_color(grid_color)
    ax2.yaxis.grid(True, color=grid_color, alpha=0.5)
    ax2.set_axisbelow(True)

    # ── Comparação de pesos ───────────────────────────────────────────────────
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_facecolor('#0f0f23')
    base_xg_d, w_att_d, w_def_d, w_gk_d = DEFAULTS
    base_xg_c, w_att_c, w_def_c, w_gk_c = cal_theta
    weight_names  = ['BASE_XG', 'w_att\n(OFF)', 'w_mid\n(OFF)', 'w_def\n(RES)', 'w_gk\n(RES)', 'w_mid\n(RES)']
    weights_before = [base_xg_d, w_att_d, 1-w_att_d, w_def_d, w_gk_d, max(1-w_def_d-w_gk_d, 0.05)]
    weights_after  = [base_xg_c, w_att_c, 1-w_att_c, w_def_c, w_gk_c, max(1-w_def_c-w_gk_c, 0.05)]
    xw = np.arange(len(weight_names))
    ax3.bar(xw - w/2, weights_before, w, label='Atual',     color=COLORS['default'],    alpha=0.85)
    ax3.bar(xw + w/2, weights_after,  w, label='Calibrado', color=COLORS['calibrated'], alpha=0.85)
    for i, (b, a) in enumerate(zip(weights_before, weights_after)):
        delta = a - b
        color = COLORS['better'] if delta < -0.02 else (COLORS['worse'] if delta > 0.02 else COLORS['neutral'])
        ax3.annotate(f'{delta:+.3f}', xy=(xw[i] + w/2, a), xytext=(0, 4),
                     textcoords='offset points', ha='center', fontsize=8, color=color, fontweight='bold')
    ax3.set_title('Mudança nos pesos', color=title_color, fontsize=11)
    ax3.set_xticks(xw)
    ax3.set_xticklabels(weight_names, color=label_color, fontsize=9)
    ax3.tick_params(colors=label_color)
    ax3.set_ylabel('Valor', color=label_color)
    ax3.legend(facecolor='#1a1a2e', labelcolor=label_color, fontsize=9)
    ax3.spines[:].set_color(grid_color)
    ax3.yaxis.grid(True, color=grid_color, alpha=0.5)
    ax3.set_axisbelow(True)

    # ── xG antes vs depois por jogo ────────────────────────────────────────────
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_facecolor('#0f0f23')
    xg_def, xg_cal = [], []
    for m in matches:
        sa, sb = scores[m['team_a']], scores[m['team_b']]
        a_d, b_d = compute_xg(sa, sb, DEFAULTS)
        a_c, b_c = compute_xg(sa, sb, cal_theta)
        xg_def.extend([a_d, b_d])
        xg_cal.extend([a_c, b_c])
    ax4.scatter(xg_def, xg_cal, color=COLORS['calibrated'], alpha=0.75, s=45, zorder=3)
    max_val = max(max(xg_def), max(xg_cal)) * 1.05
    ax4.plot([0, max_val], [0, max_val], '--', color='white', lw=0.8, alpha=0.4, label='sem mudança')
    ax4.set_xlim(0, max_val); ax4.set_ylim(0, max_val)
    ax4.set_title('xG: atual vs calibrado (todos os placares)', color=title_color, fontsize=11)
    ax4.set_xlabel('xG atual', color=label_color)
    ax4.set_ylabel('xG calibrado', color=label_color)
    ax4.tick_params(colors=label_color)
    ax4.legend(facecolor='#1a1a2e', labelcolor=label_color, fontsize=9)
    ax4.spines[:].set_color(grid_color)
    ax4.yaxis.grid(True, color=grid_color, alpha=0.5)
    ax4.xaxis.grid(True, color=grid_color, alpha=0.5)
    ax4.set_axisbelow(True)

    # ── Rodapé com métricas resumidas ──────────────────────────────────────────
    delta_nll   = mean_nll_c   - mean_nll_d
    delta_brier = mean_brier_c - mean_brier_d
    nll_color   = COLORS['better'] if delta_nll   < -0.02 else (COLORS['worse'] if delta_nll   > 0.02 else COLORS['neutral'])
    brier_color = COLORS['better'] if delta_brier < -0.005 else (COLORS['worse'] if delta_brier > 0.005 else COLORS['neutral'])

    summary = (
        f"LOO-CV NLL:  atual={mean_nll_d:.4f}  calibrado={mean_nll_c:.4f}  Δ={delta_nll:+.4f}     "
        f"LOO-CV Brier:  atual={mean_brier_d:.4f}  calibrado={mean_brier_c:.4f}  Δ={delta_brier:+.4f}     "
        f"In-sample NLL: {nll_before:.4f} → {nll_after:.4f}  ({nll_after-nll_before:+.4f})"
    )
    fig.text(0.5, 0.01, summary, ha='center', fontsize=9, color=label_color,
             bbox=dict(facecolor='#0f0f23', edgecolor=grid_color, boxstyle='round,pad=0.4'))

    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig(REPORT_FILE, dpi=140, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"  Gráfico salvo em {REPORT_FILE}")


# Jogos removidos do treino com --exclude-outliers (diff >= este valor).
OUTLIER_MIN_GOAL_DIFF = 4


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    exclude_outliers = '--exclude-outliers' in sys.argv

    # --out <arquivo> permite salvar em path específico (usado pelo outlier_comparison)
    out_file = OUT_FILE
    if '--out' in sys.argv:
        out_file = sys.argv[sys.argv.index('--out') + 1]

    matches, scores = load_data()

    if exclude_outliers:
        outliers = [m for m in matches if abs(m['goals_a'] - m['goals_b']) >= OUTLIER_MIN_GOAL_DIFF]
        matches  = [m for m in matches if abs(m['goals_a'] - m['goals_b']) <  OUTLIER_MIN_GOAL_DIFF]
        print(f"\n  --exclude-outliers: removendo {len(outliers)} jogo(s) com diff ≥ {OUTLIER_MIN_GOAL_DIFF} gols:")
        for o in outliers:
            print(f"    {dn(o['team_a'])} {o['goals_a']}–{o['goals_b']} {dn(o['team_b'])}")

    n = len(matches)

    print(f"\n{'═'*70}")
    print(f"  CALIBRAÇÃO DE CONSTANTES xG — {n} partidas  ({n*2} observações de gols)")
    print(f"{'═'*70}")
    print(f"  Loss: Poisson NLL = Σ [ xG - k·log(xG) ]  (por placar)")

    # ── Calibração full ───────────────────────────────────────────────────────
    nll_before = poisson_nll(DEFAULTS, matches, scores)
    print(f"\n  Otimizando... ", end='', flush=True)
    cal_theta, nll_after = calibrate(matches, scores)
    print("pronto.")

    base_xg, w_att, w_def, w_gk = cal_theta
    w_mid_off = 1.0 - w_att
    w_mid_res = max(1.0 - w_def - w_gk, 0.05)

    print(f"\n  {'':16} {'BASE_XG':>8}  {'w_att':>6}  {'w_def':>6}  {'w_gk':>6}  │  {'w_mid_off':>9}  {'w_mid_res':>9}")
    print(f"  {'Atuais:':16} {DEFAULTS[0]:>8.3f}  {DEFAULTS[1]:>6.3f}  {DEFAULTS[2]:>6.3f}  {DEFAULTS[3]:>6.3f}  │  {1-DEFAULTS[1]:>9.3f}  {max(1-DEFAULTS[2]-DEFAULTS[3],0.05):>9.3f}")
    print(f"  {'Calibrados:':16} {base_xg:>8.3f}  {w_att:>6.3f}  {w_def:>6.3f}  {w_gk:>6.3f}  │  {w_mid_off:>9.3f}  {w_mid_res:>9.3f}")
    print(f"\n  NLL in-sample:   {nll_before:.4f} → {nll_after:.4f}  (Δ={nll_after - nll_before:+.4f})")

    # ── LOO-CV ────────────────────────────────────────────────────────────────
    print(f"\n  Rodando LOO-CV ({n} folds)...")
    nll_d, nll_c, brier_d, brier_c = loo_cv(matches, scores)

    mean_nll_d  = sum(nll_d)    / n
    mean_nll_c  = sum(nll_c)    / n
    mean_brier_d = sum(brier_d) / n
    mean_brier_c = sum(brier_c) / n
    delta_nll   = mean_nll_c   - mean_nll_d
    delta_brier = mean_brier_c - mean_brier_d

    nll_verdict   = "✓ MELHORA" if delta_nll   < -0.02 else ("≈ NEUTRO" if abs(delta_nll)   < 0.02 else "✗ PIORA")
    brier_verdict = "✓ MELHORA" if delta_brier < -0.005 else ("≈ NEUTRO" if abs(delta_brier) < 0.005 else "✗ PIORA")

    print(f"\n  LOO-CV NLL:    padrão={mean_nll_d:.4f}  calibrado={mean_nll_c:.4f}  (Δ={delta_nll:+.4f})  {nll_verdict}")
    print(f"  LOO-CV Brier:  padrão={mean_brier_d:.4f}  calibrado={mean_brier_c:.4f}  (Δ={delta_brier:+.4f})  {brier_verdict}")

    # ── Tabela por jogo ───────────────────────────────────────────────────────
    print(f"\n  {'─'*70}")
    print(f"  {'Partida':<32} {'Real':>5}  {'NLL def':>7}  {'NLL cal':>7}  {'Brier def':>9}  {'Brier cal':>9}")
    print(f"  {'─'*70}")
    for m, nd, nc, bd, bc in zip(matches, nll_d, nll_c, brier_d, brier_c):
        name = f"{dn(m['team_a'])} vs {dn(m['team_b'])}"
        real = f"{m['goals_a']}–{m['goals_b']}"
        nll_icon   = "↑" if nc < nd - 0.05 else ("↓" if nc > nd + 0.05 else "≈")
        brier_icon = "↑" if bc < bd - 0.02 else ("↓" if bc > bd + 0.02 else "≈")
        print(f"  {name:<32} {real:>5}  {nd:>7.3f}  {nc:>7.3f} {nll_icon}  {bd:>9.4f}  {bc:>9.4f} {brier_icon}")

    print(f"\n{'═'*70}\n")

    # ── Gráfico ───────────────────────────────────────────────────────────────
    generate_report(matches, cal_theta, nll_d, nll_c, brier_d, brier_c,
                    nll_before, nll_after, mean_nll_d, mean_nll_c,
                    mean_brier_d, mean_brier_c, scores)

    # ── Salvar ────────────────────────────────────────────────────────────────
    out = {
        "n_matches": n,
        "nll_baseline":            round(nll_before, 4),
        "nll_calibrated_insample": round(nll_after, 4),
        "loo_cv_nll_default":      round(mean_nll_d, 4),
        "loo_cv_nll_calibrated":   round(mean_nll_c, 4),
        "loo_cv_nll_delta":        round(delta_nll, 4),
        "loo_cv_brier_default":    round(mean_brier_d, 4),
        "loo_cv_brier_calibrated": round(mean_brier_c, 4),
        "loo_cv_brier_delta":      round(delta_brier, 4),
        "nll_verdict":             nll_verdict,
        "brier_verdict":           brier_verdict,
        "weights": {
            "BASE_XG":   round(base_xg, 4),
            "OFF_ATT_W": round(w_att, 4),
            "OFF_MID_W": round(w_mid_off, 4),
            "RES_DEF_W": round(w_def, 4),
            "RES_GK_W":  round(w_gk, 4),
            "RES_MID_W": round(w_mid_res, 4),
        },
        "per_game": [
            {
                "match":      f"{dn(m['team_a'])} vs {dn(m['team_b'])}",
                "result":     f"{m['goals_a']}-{m['goals_b']}",
                "outcome":    m['outcome'],
                "nll_default":    round(nd, 4),
                "nll_calibrated": round(nc, 4),
                "brier_default":  round(bd, 4),
                "brier_calibrated": round(bc, 4),
            }
            for m, nd, nc, bd, bc in zip(matches, nll_d, nll_c, brier_d, brier_c)
        ],
    }
    os.makedirs("output", exist_ok=True)
    with open(out_file, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"  Resultado salvo em {out_file}")
    print(f"\n  Para aplicar os pesos sugeridos em simulate.py e build_team_scores.py,")
    print(f"  edite manualmente as constantes acima.\n")


if __name__ == '__main__':
    main()
