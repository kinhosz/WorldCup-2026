#!/usr/bin/env python3
"""
calibrate.py — calibrar as constantes da fórmula xG usando resultados reais.

Loss function: Poisson NLL (gols são contagens — distribuição correta).
  NLL = Σ [ xG_pred - k × log(xG_pred) ]   para cada placar real k

Modo padrão (4 parâmetros):
  θ = [BASE_XG, w_att, w_def, w_gk]

Modo att-only (--att-only, recomendado para ~44 jogos):
  θ = [BASE_XG, w_att, w_def, w_gk, att_bias_t1..tN]
  xG_A = BASE_XG × (off_A × att_bias_A) / res_B
  loss  = NLL + λ × Σ (att_bias − 1)²

Validação: LOO-CV — calibra nos N-1 jogos, prediz o deixado de fora.
  No modo att-only, LOO-CV é desabilitado (muitos parâmetros / folds).

Uso:
    python3 scripts/calibrate.py
    python3 scripts/calibrate.py --att-only --lambda 1.5
    python3 scripts/calibrate.py --exclude-outliers
"""

import argparse
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
OUTLIER_MIN_GOAL_DIFF = 4

DEFAULTS = [1.30, 0.70, 0.60, 0.20]
BOUNDS   = [(0.50, 4.00), (0.10, 0.90), (0.10, 0.80), (0.05, 0.50)]
BIAS_BOUNDS = (0.20, 5.00)

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
    base_xg, w_att, w_def, w_gk = theta[:4]
    w_mid_off = 1.0 - w_att
    w_mid_res = max(1.0 - w_def - w_gk, 0.05)

    off_a = w_att * _get(s_a, 'attack')  + w_mid_off * _get(s_a, 'midfield')
    off_b = w_att * _get(s_b, 'attack')  + w_mid_off * _get(s_b, 'midfield')
    res_a = max(w_def * _get(s_a, 'defense') + w_gk * _get(s_a, 'goalkeeper') + w_mid_res * _get(s_a, 'midfield'), RES_FLOOR)
    res_b = max(w_def * _get(s_b, 'defense') + w_gk * _get(s_b, 'goalkeeper') + w_mid_res * _get(s_b, 'midfield'), RES_FLOOR)
    return min(base_xg * off_a / res_b, MAX_XG), min(base_xg * off_b / res_a, MAX_XG)


def compute_xg_biased(s_a, s_b, theta, teams_idx, ta, tb):
    """att_bias por seleção; def_bias fixo em 1.0."""
    base_xg, w_att, w_def, w_gk = theta[:4]
    w_mid_off = 1.0 - w_att
    w_mid_res = max(1.0 - w_def - w_gk, 0.05)

    n_global = 4
    att_bias_a = theta[n_global + teams_idx.get(ta, -1)] if ta in teams_idx else 1.0
    att_bias_b = theta[n_global + teams_idx.get(tb, -1)] if tb in teams_idx else 1.0

    off_a = (w_att * _get(s_a, 'attack') + w_mid_off * _get(s_a, 'midfield')) * att_bias_a
    off_b = (w_att * _get(s_b, 'attack') + w_mid_off * _get(s_b, 'midfield')) * att_bias_b
    res_a = max(w_def * _get(s_a, 'defense') + w_gk * _get(s_a, 'goalkeeper') + w_mid_res * _get(s_a, 'midfield'), RES_FLOOR)
    res_b = max(w_def * _get(s_b, 'defense') + w_gk * _get(s_b, 'goalkeeper') + w_mid_res * _get(s_b, 'midfield'), RES_FLOOR)
    return min(base_xg * off_a / res_b, MAX_XG), min(base_xg * off_b / res_a, MAX_XG)


def poisson_nll(theta, matches, scores, teams_idx=None, lam=0.0):
    total = 0.0
    for m in matches:
        if teams_idx is not None:
            xg_a, xg_b = compute_xg_biased(scores[m['team_a']], scores[m['team_b']], theta, teams_idx, m['team_a'], m['team_b'])
        else:
            xg_a, xg_b = compute_xg(scores[m['team_a']], scores[m['team_b']], theta)
        total += xg_a - m['goals_a'] * np.log(max(xg_a, 1e-9))
        total += xg_b - m['goals_b'] * np.log(max(xg_b, 1e-9))
    if teams_idx is not None and lam > 0:
        biases = theta[4:]
        total += lam * np.sum((biases - 1.0) ** 2)
    return total


def calibrate(matches, scores, teams_idx=None, lam=0.0):
    if teams_idx is not None:
        n_biases = len(teams_idx)
        x0 = DEFAULTS[:] + [1.0] * n_biases
        bounds = BOUNDS + [BIAS_BOUNDS] * n_biases
    else:
        x0 = DEFAULTS[:]
        bounds = BOUNDS

    res = minimize(
        lambda t: poisson_nll(t, matches, scores, teams_idx, lam),
        x0=x0,
        bounds=bounds,
        method='L-BFGS-B',
        options={'maxiter': 5000, 'ftol': 1e-12},
    )
    return res.x.tolist(), res.fun


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


def loo_cv(matches, scores):
    """LOO-CV sem biases — apenas parâmetros globais."""
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


def load_data(exclude_outliers):
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

    if exclude_outliers:
        outliers = [m for m in matches if abs(m['goals_a'] - m['goals_b']) >= OUTLIER_MIN_GOAL_DIFF]
        matches  = [m for m in matches if abs(m['goals_a'] - m['goals_b']) <  OUTLIER_MIN_GOAL_DIFF]
        print(f"  --exclude-outliers: removendo {len(outliers)} jogo(s):")
        for o in outliers:
            print(f"    {dn(o['team_a'])} {o['goals_a']}–{o['goals_b']} {dn(o['team_b'])}")

    teams = sorted({m['team_a'] for m in matches} | {m['team_b'] for m in matches})
    teams_idx = {t: i for i, t in enumerate(teams)}
    return matches, scores, teams_idx


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

    fig.suptitle('Calibração xG — LOO-CV', fontsize=16,
                 color=title_color, fontweight='bold', y=0.98)

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_facecolor('#0f0f23')
    ax1.bar(x - w/2, brier_d, w, label='Atual',     color=COLORS['default'],    alpha=0.85)
    ax1.bar(x + w/2, brier_c, w, label='Calibrado', color=COLORS['calibrated'], alpha=0.85)
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

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_facecolor('#0f0f23')
    ax2.bar(x - w/2, nll_d, w, label='Atual',     color=COLORS['default'],    alpha=0.85)
    ax2.bar(x + w/2, nll_c, w, label='Calibrado', color=COLORS['calibrated'], alpha=0.85)
    ax2.axhline(mean_nll_d, color=COLORS['default'],   ls='--', lw=1.2, alpha=0.7)
    ax2.axhline(mean_nll_c, color=COLORS['calibrated'], ls='--', lw=1.2, alpha=0.7)
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

    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_facecolor('#0f0f23')
    base_xg_d, w_att_d, w_def_d, w_gk_d = DEFAULTS
    base_xg_c, w_att_c, w_def_c, w_gk_c = cal_theta[:4]
    weight_names   = ['BASE_XG', 'w_att\n(OFF)', 'w_mid\n(OFF)', 'w_def\n(RES)', 'w_gk\n(RES)', 'w_mid\n(RES)']
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

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_facecolor('#0f0f23')
    xg_def, xg_cal = [], []
    for m in matches:
        sa, sb = scores[m['team_a']], scores[m['team_b']]
        a_d, b_d = compute_xg(sa, sb, DEFAULTS)
        a_c, b_c = compute_xg(sa, sb, cal_theta[:4])
        xg_def.extend([a_d, b_d])
        xg_cal.extend([a_c, b_c])
    ax4.scatter(xg_def, xg_cal, color=COLORS['calibrated'], alpha=0.75, s=45, zorder=3)
    max_val = max(max(xg_def), max(xg_cal)) * 1.05
    ax4.plot([0, max_val], [0, max_val], '--', color='white', lw=0.8, alpha=0.4, label='sem mudança')
    ax4.set_xlim(0, max_val); ax4.set_ylim(0, max_val)
    ax4.set_title('xG: atual vs calibrado', color=title_color, fontsize=11)
    ax4.set_xlabel('xG atual', color=label_color)
    ax4.set_ylabel('xG calibrado', color=label_color)
    ax4.tick_params(colors=label_color)
    ax4.legend(facecolor='#1a1a2e', labelcolor=label_color, fontsize=9)
    ax4.spines[:].set_color(grid_color)
    ax4.yaxis.grid(True, color=grid_color, alpha=0.5)
    ax4.xaxis.grid(True, color=grid_color, alpha=0.5)
    ax4.set_axisbelow(True)

    delta_nll   = mean_nll_c   - mean_nll_d
    delta_brier = mean_brier_c - mean_brier_d
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exclude-outliers', action='store_true')
    parser.add_argument('--att-only', action='store_true',
                        help='Habilita att_bias por seleção via L-BFGS-B (desabilita LOO-CV)')
    parser.add_argument('--lambda', dest='lam', type=float, default=1.0,
                        help='Força L2 nos biases (default: 1.0)')
    # compatibilidade: --out <arquivo>
    parser.add_argument('--out', default=OUT_FILE)
    args = parser.parse_args()

    print(f"\n{'═'*70}")
    print(f"  CALIBRAÇÃO DE CONSTANTES xG — L-BFGS-B  |  Copa do Mundo 2026")
    print(f"{'═'*70}")
    print(f"  Modo       : {'att-only biases (λ=' + str(args.lam) + ')' if args.att_only else 'parâmetros globais'}")
    print(f"  LOO-CV     : {'desabilitado (biases ativos)' if args.att_only else 'habilitado'}")
    print(f"  Loss       : Poisson NLL = Σ [ xG - k·log(xG) ]  (por placar)")

    matches, scores, teams_idx = load_data(args.exclude_outliers)
    n = len(matches)
    print(f"  Partidas   : {n}  ({n*2} observações de gols)")

    if args.att_only:
        n_params = 4 + len(teams_idx)
        print(f"  Parâmetros : {n_params}  (4 globais + {len(teams_idx)} att_bias)")
        print(f"  Ratio      : {n_params}/{n*2} = {n_params/(n*2):.2f}")

    # ── Baseline ──────────────────────────────────────────────────────────────
    nll_before = poisson_nll(DEFAULTS, matches, scores)
    print(f"\n  NLL baseline (originais): {nll_before:.4f}")

    # ── Calibração full ───────────────────────────────────────────────────────
    t_idx = teams_idx if args.att_only else None
    lam   = args.lam  if args.att_only else 0.0

    print(f"  Otimizando... ", end='', flush=True)
    cal_theta, nll_after = calibrate(matches, scores, t_idx, lam)
    print("pronto.")

    base_xg, w_att, w_def, w_gk = cal_theta[:4]
    w_mid_off = 1.0 - w_att
    w_mid_res = max(1.0 - w_def - w_gk, 0.05)

    print(f"\n  {'':16} {'BASE_XG':>8}  {'w_att':>6}  {'w_def':>6}  {'w_gk':>6}  │  {'w_mid_off':>9}  {'w_mid_res':>9}")
    print(f"  {'Atuais:':16} {DEFAULTS[0]:>8.3f}  {DEFAULTS[1]:>6.3f}  {DEFAULTS[2]:>6.3f}  {DEFAULTS[3]:>6.3f}  │  {1-DEFAULTS[1]:>9.3f}  {max(1-DEFAULTS[2]-DEFAULTS[3],0.05):>9.3f}")
    print(f"  {'Calibrados:':16} {base_xg:>8.3f}  {w_att:>6.3f}  {w_def:>6.3f}  {w_gk:>6.3f}  │  {w_mid_off:>9.3f}  {w_mid_res:>9.3f}")
    nll_pure = poisson_nll(cal_theta, matches, scores, t_idx, lam=0.0)
    print(f"\n  NLL in-sample:   {nll_before:.4f} → {nll_pure:.4f}  (Δ={nll_pure - nll_before:+.4f})")

    if args.att_only:
        teams_list = sorted(teams_idx, key=teams_idx.get)
        print(f"\n  Biases att por seleção (λ={args.lam}):")
        bias_rows = [(teams_list[i], cal_theta[4 + i]) for i in range(len(teams_list))]
        bias_rows.sort(key=lambda x: -abs(x[1] - 1.0))
        print(f"  {'Seleção':<28} {'att_bias':>10}")
        print(f"  {'-'*28} {'-'*10}")
        for team, att in bias_rows:
            flag = " ←" if abs(att - 1.0) > 0.15 else ""
            print(f"  {team:<28} {att:>10.4f}{flag}")

    # ── LOO-CV (só sem biases) ─────────────────────────────────────────────────
    if not args.att_only:
        print(f"\n  Rodando LOO-CV ({n} folds)...")
        nll_d, nll_c, brier_d, brier_c = loo_cv(matches, scores)

        mean_nll_d   = sum(nll_d)   / n
        mean_nll_c   = sum(nll_c)   / n
        mean_brier_d = sum(brier_d) / n
        mean_brier_c = sum(brier_c) / n
        delta_nll    = mean_nll_c - mean_nll_d
        delta_brier  = mean_brier_c - mean_brier_d

        nll_verdict   = "✓ MELHORA" if delta_nll   < -0.02 else ("≈ NEUTRO" if abs(delta_nll)   < 0.02 else "✗ PIORA")
        brier_verdict = "✓ MELHORA" if delta_brier < -0.005 else ("≈ NEUTRO" if abs(delta_brier) < 0.005 else "✗ PIORA")

        print(f"\n  LOO-CV NLL:    padrão={mean_nll_d:.4f}  calibrado={mean_nll_c:.4f}  (Δ={delta_nll:+.4f})  {nll_verdict}")
        print(f"  LOO-CV Brier:  padrão={mean_brier_d:.4f}  calibrado={mean_brier_c:.4f}  (Δ={delta_brier:+.4f})  {brier_verdict}")

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

        generate_report(matches, cal_theta, nll_d, nll_c, brier_d, brier_c,
                        nll_before, nll_after, mean_nll_d, mean_nll_c,
                        mean_brier_d, mean_brier_c, scores)
    else:
        mean_nll_d = mean_nll_c = mean_brier_d = mean_brier_c = None
        delta_nll = delta_brier = None
        nll_verdict = brier_verdict = "N/A (biases ativos)"

    print(f"\n{'═'*70}\n")

    # ── Salvar ─────────────────────────────────────────────────────────────────
    out = {
        "n_matches":               n,
        "att_only":                args.att_only,
        "lambda":                  args.lam if args.att_only else None,
        "nll_baseline":            round(nll_before, 4),
        "nll_calibrated_insample": round(nll_pure, 4),
        "loo_cv_nll_default":      round(mean_nll_d, 4) if mean_nll_d else None,
        "loo_cv_nll_calibrated":   round(mean_nll_c, 4) if mean_nll_c else None,
        "loo_cv_nll_delta":        round(delta_nll, 4)  if delta_nll  else None,
        "loo_cv_brier_default":    round(mean_brier_d, 4) if mean_brier_d else None,
        "loo_cv_brier_calibrated": round(mean_brier_c, 4) if mean_brier_c else None,
        "loo_cv_brier_delta":      round(delta_brier, 4)  if delta_brier  else None,
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
    }

    if args.att_only:
        teams_list = sorted(teams_idx, key=teams_idx.get)
        out["biases"] = {
            team: {"att_bias": round(cal_theta[4 + i], 4), "def_bias": 1.0}
            for i, team in enumerate(teams_list)
        }

    if not args.att_only:
        out["per_game"] = [
            {
                "match":              f"{dn(m['team_a'])} vs {dn(m['team_b'])}",
                "result":             f"{m['goals_a']}-{m['goals_b']}",
                "outcome":            m['outcome'],
                "nll_default":        round(nd, 4),
                "nll_calibrated":     round(nc, 4),
                "brier_default":      round(bd, 4),
                "brier_calibrated":   round(bc, 4),
            }
            for m, nd, nc, bd, bc in zip(matches, nll_d, nll_c, brier_d, brier_c)
        ]

    os.makedirs("output", exist_ok=True)
    with open(args.out, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"  Resultado salvo em {args.out}")
    print(f"\n{'═'*70}\n")


if __name__ == '__main__':
    main()
