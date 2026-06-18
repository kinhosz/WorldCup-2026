#!/usr/bin/env python3
"""
calibrate_sa.py — calibrar constantes xG via Simulated Annealing.

Modo padrão (4 parâmetros livres):
  θ = [BASE_XG, w_att, w_def, w_gk]
  OFF_MID_W = 1 − w_att
  RES_MID_W = max(1 − w_def − w_gk, 0.05)

Modo biases (--biases, útil a partir da R3 com ~48+ jogos):
  θ = [BASE_XG, w_att, w_def, w_gk, att_bias_t1..tN, def_bias_t1..tN]
  xG_A = BASE_XG × (off_A × att_bias_A) / (res_B × def_bias_B)
  loss  = NLL + λ × Σ (bias − 1)²

SA schedule:
  T(k) = T0 × alpha^k
  Aceita solução pior com P = exp(−Δloss / T)
  Perturbação: 50% parâmetros globais, 50% biases (quando --biases ativo)

Uso:
  python3 scripts/calibrate_sa.py
  python3 scripts/calibrate_sa.py --exclude-outliers
  python3 scripts/calibrate_sa.py --biases --lambda 0.5
  python3 scripts/calibrate_sa.py --restarts 10 --iters 500000
  python3 scripts/calibrate_sa.py --seed 42
"""

import argparse
import json
import math
import os
import random
import time

import numpy as np
from scipy.stats import poisson as sp_poisson

# ── Arquivos ──────────────────────────────────────────────────────────────────

STATE_FILE  = "output/copa_real_state.json"
SCORES_FILE = "output/team_scores.json"
LBFGS_FILE  = "output/calibrated_weights.json"
OUT_FILE    = "output/calibrated_weights_sa.json"

# ── Constantes do modelo ──────────────────────────────────────────────────────

FALLBACK              = 0.5
RES_FLOOR             = 0.10
MAX_XG                = 8.0
MAX_GOALS             = 12
OUTLIER_MIN_GOAL_DIFF = 4

# ── Parâmetros globais ────────────────────────────────────────────────────────

N_GLOBAL     = 4
PARAM_NAMES  = ["BASE_XG", "w_att",  "w_def", "w_gk"]
DEFAULTS     = [1.30,       0.70,     0.60,    0.20]
BOUNDS       = [(0.50, 4.00), (0.10, 0.90), (0.10, 0.80), (0.05, 0.50)]
STEP_GLOBAL  = [0.04,       0.03,     0.03,    0.02]

# ── Biases ────────────────────────────────────────────────────────────────────

BIAS_BOUNDS  = (0.20, 5.00)   # cada bias multiplicativo
BIAS_STEP    = 0.05
BIAS_DEFAULT = 1.0

# ── SA defaults ───────────────────────────────────────────────────────────────

DEFAULT_T0       = 3.0
DEFAULT_ALPHA    = 0.99996    # T_final ≈ T0 × alpha^300k ≈ 0.005
DEFAULT_ITERS    = 300_000
DEFAULT_RESTARTS = 5
DEFAULT_LAMBDA   = 1.0        # força da regularização L2 nos biases
LOG_EVERY        = 10_000


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Fórmula xG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _get(s, key):
    v = s.get(key)
    return v if v is not None else FALLBACK


def compute_xg(s_a, s_b, theta):
    """Sem biases — modo padrão."""
    base_xg, w_att, w_def, w_gk = theta[:N_GLOBAL]
    w_mid_off = 1.0 - w_att
    w_mid_res = max(1.0 - w_def - w_gk, 0.05)

    off_a = w_att * _get(s_a, 'attack')  + w_mid_off * _get(s_a, 'midfield')
    off_b = w_att * _get(s_b, 'attack')  + w_mid_off * _get(s_b, 'midfield')
    res_a = max(w_def * _get(s_a, 'defense') + w_gk * _get(s_a, 'goalkeeper') + w_mid_res * _get(s_a, 'midfield'), RES_FLOOR)
    res_b = max(w_def * _get(s_b, 'defense') + w_gk * _get(s_b, 'goalkeeper') + w_mid_res * _get(s_b, 'midfield'), RES_FLOOR)
    return min(base_xg * off_a / res_b, MAX_XG), min(base_xg * off_b / res_a, MAX_XG)


def compute_xg_biased(s_a, s_b, theta, idx_a, idx_b, n_teams):
    """Com biases por seleção.
    θ = [BASE_XG, w_att, w_def, w_gk, att_bias_0..N-1, def_bias_0..N-1]
    """
    base_xg, w_att, w_def, w_gk = theta[:N_GLOBAL]
    w_mid_off = 1.0 - w_att
    w_mid_res = max(1.0 - w_def - w_gk, 0.05)

    att_bias_a = theta[N_GLOBAL + idx_a]
    att_bias_b = theta[N_GLOBAL + idx_b]
    def_bias_a = theta[N_GLOBAL + n_teams + idx_a]
    def_bias_b = theta[N_GLOBAL + n_teams + idx_b]

    off_a = (w_att * _get(s_a, 'attack') + w_mid_off * _get(s_a, 'midfield')) * att_bias_a
    off_b = (w_att * _get(s_b, 'attack') + w_mid_off * _get(s_b, 'midfield')) * att_bias_b
    res_a = max((w_def * _get(s_a, 'defense') + w_gk * _get(s_a, 'goalkeeper') + w_mid_res * _get(s_a, 'midfield')) * def_bias_a, RES_FLOOR)
    res_b = max((w_def * _get(s_b, 'defense') + w_gk * _get(s_b, 'goalkeeper') + w_mid_res * _get(s_b, 'midfield')) * def_bias_b, RES_FLOOR)
    return min(base_xg * off_a / res_b, MAX_XG), min(base_xg * off_b / res_a, MAX_XG)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Loss functions
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def poisson_nll(theta, matches, scores, teams_idx=None, lam=0.0):
    """
    NLL = Σ [ xg − k × log(xg) ].
    Se teams_idx fornecido, usa compute_xg_biased + regularização L2.
    """
    total = 0.0
    if teams_idx is not None:
        n_teams = len(teams_idx)
        for m in matches:
            xg_a, xg_b = compute_xg_biased(
                scores[m['team_a']], scores[m['team_b']], theta,
                teams_idx[m['team_a']], teams_idx[m['team_b']], n_teams,
            )
            total += xg_a - m['goals_a'] * math.log(max(xg_a, 1e-9))
            total += xg_b - m['goals_b'] * math.log(max(xg_b, 1e-9))
        # regularização L2: penaliza desvio de 1.0
        biases = theta[N_GLOBAL:]
        total += lam * sum((b - 1.0) ** 2 for b in biases)
    else:
        for m in matches:
            xg_a, xg_b = compute_xg(scores[m['team_a']], scores[m['team_b']], theta)
            total += xg_a - m['goals_a'] * math.log(max(xg_a, 1e-9))
            total += xg_b - m['goals_b'] * math.log(max(xg_b, 1e-9))
    return total


def match_probs(xg_a, xg_b):
    pa = np.array([sp_poisson.pmf(k, xg_a) for k in range(MAX_GOALS + 1)])
    pb = np.array([sp_poisson.pmf(k, xg_b) for k in range(MAX_GOALS + 1)])
    m  = np.outer(pa, pb)
    win_a = float(np.tril(m, -1).sum())
    draw  = float(np.trace(m))
    win_b = float(np.triu(m, 1).sum())
    s = win_a + draw + win_b
    return win_a / s, draw / s, win_b / s


def brier_score(probs, outcome):
    actual = {'a': (1, 0, 0), 'draw': (0, 1, 0), 'b': (0, 0, 1)}[outcome]
    return sum((p - o) ** 2 for p, o in zip(probs, actual))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SA — vizinhança e perturbação
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_initial_theta(rng, use_biases, n_teams, is_first_restart):
    if is_first_restart:
        global_part = DEFAULTS[:]
    else:
        global_part = [rng.uniform(lo, hi) for lo, hi in BOUNDS]

    if not use_biases:
        return global_part

    # biases começam todos em 1.0 (neutro) — SA vai explorar desvios
    bias_part = [BIAS_DEFAULT] * (2 * n_teams)
    return global_part + bias_part


def neighbor(theta, rng, use_biases, n_teams):
    """
    Seleciona um parâmetro para perturbar.
    Com biases: 50% chance de mexer num global, 50% num bias.
    """
    new_theta = theta[:]

    if use_biases and rng.random() >= 0.50:
        # perturba um bias
        i = N_GLOBAL + rng.randint(0, 2 * n_teams - 1)
        delta = rng.gauss(0, BIAS_STEP)
        lo, hi = BIAS_BOUNDS
    else:
        # perturba um parâmetro global
        i = rng.randint(0, N_GLOBAL - 1)
        delta = rng.gauss(0, STEP_GLOBAL[i])
        lo, hi = BOUNDS[i]

    new_theta[i] = min(max(new_theta[i] + delta, lo), hi)
    return new_theta


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Logging
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def format_globals(theta):
    return "  ".join(f"{n}={theta[i]:.4f}" for i, n in enumerate(PARAM_NAMES))


def format_top_biases(theta, teams_list, n_top=5):
    """Mostra os biases com maior desvio de 1.0."""
    n_teams = len(teams_list)
    entries = []
    for i, team in enumerate(teams_list):
        att = theta[N_GLOBAL + i]
        dfb = theta[N_GLOBAL + n_teams + i]
        entries.append((abs(att - 1.0) + abs(dfb - 1.0), team, att, dfb))
    entries.sort(reverse=True)
    parts = [f"{t}(att={a:.2f},def={d:.2f})" for _, t, a, d in entries[:n_top]]
    return "  ".join(parts)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SA — loop principal
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def simulated_annealing(matches, scores, n_iter, T0, alpha, rng,
                        restart_idx, n_restarts, use_biases,
                        teams_idx, teams_list, lam):
    n_teams   = len(teams_list)
    theta     = build_initial_theta(rng, use_biases, n_teams, restart_idx == 0)
    curr_loss = poisson_nll(theta, matches, scores, teams_idx if use_biases else None, lam)
    best_theta = theta[:]
    best_loss  = curr_loss

    T = T0
    accepts_window = 0
    total_window   = 0
    t_start = time.time()

    mode_str = f"biases λ={lam}" if use_biases else "sem biases"
    n_params = len(theta)
    print(f"\n{'━'*72}")
    print(f"  Restart {restart_idx+1}/{n_restarts}  |  {n_iter:,} iters  |  T0={T0}  |  {mode_str}  |  θ={n_params}")
    print(f"  globals: {format_globals(theta)}")
    print(f"  loss inicial: {curr_loss:.4f}")
    print(f"{'━'*72}")

    for k in range(1, n_iter + 1):
        new_theta = neighbor(theta, rng, use_biases, n_teams)
        new_loss  = poisson_nll(new_theta, matches, scores, teams_idx if use_biases else None, lam)

        delta       = new_loss - curr_loss
        total_window += 1

        if delta < 0 or rng.random() < math.exp(-delta / max(T, 1e-10)):
            theta    = new_theta
            curr_loss = new_loss
            accepts_window += 1
            if new_loss < best_loss:
                best_loss  = new_loss
                best_theta = new_theta[:]

        T *= alpha

        if k % LOG_EVERY == 0:
            elapsed  = time.time() - t_start
            acc_rate = accepts_window / total_window * 100
            progress = k / n_iter * 100

            print(
                f"  [{k:>7,}/{n_iter:,}  {progress:4.1f}%  {elapsed:5.1f}s]"
                f"  T={T:.5f}  acc={acc_rate:5.1f}%"
                f"  curr={curr_loss:.4f}  best={best_loss:.4f}"
            )
            print(f"    globals: {format_globals(best_theta)}")
            if use_biases:
                print(f"    top bias: {format_top_biases(best_theta, teams_list)}")

            accepts_window = 0
            total_window   = 0

    elapsed = time.time() - t_start
    print(f"\n  Restart {restart_idx+1} concluído em {elapsed:.1f}s  |  best loss={best_loss:.4f}")

    return best_theta, best_loss


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Avaliação final (NLL puro sem regularização, para comparar com L-BFGS-B)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def evaluate(theta, matches, scores, teams_idx=None):
    """Retorna (nll_puro, brier_medio) — sem regularização para comparação justa."""
    nll = poisson_nll(theta, matches, scores, teams_idx, lam=0.0)
    brier_sum = 0.0
    for m in matches:
        if teams_idx is not None:
            n_teams = len(teams_idx)
            xg_a, xg_b = compute_xg_biased(
                scores[m['team_a']], scores[m['team_b']], theta,
                teams_idx[m['team_a']], teams_idx[m['team_b']], n_teams,
            )
        else:
            xg_a, xg_b = compute_xg(scores[m['team_a']], scores[m['team_b']], theta)
        probs = match_probs(xg_a, xg_b)
        brier_sum += brier_score(probs, m['outcome'])
    return nll, brier_sum / len(matches)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Dados
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def load_data(exclude_outliers):
    with open(STATE_FILE)  as f: state  = json.load(f)
    with open(SCORES_FILE) as f: scores = json.load(f)

    matches = []
    for grp, games in state['group_results'].items():
        for key, (ga, gb) in games.items():
            ta, tb = key.split('|')
            if ta not in scores or tb not in scores:
                continue
            out = 'a' if ga > gb else ('b' if ga < gb else 'draw')
            matches.append({'team_a': ta, 'team_b': tb,
                            'goals_a': ga, 'goals_b': gb,
                            'outcome': out})

    if exclude_outliers:
        before  = len(matches)
        matches = [m for m in matches if abs(m['goals_a'] - m['goals_b']) < OUTLIER_MIN_GOAL_DIFF]
        print(f"  --exclude-outliers: {before - len(matches)} jogo(s) removido(s)")

    # índice de times presentes no treino
    teams = sorted({m['team_a'] for m in matches} | {m['team_b'] for m in matches})
    teams_idx = {t: i for i, t in enumerate(teams)}

    return matches, scores, teams, teams_idx


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exclude-outliers', action='store_true')
    parser.add_argument('--biases',  action='store_true',
                        help='Ativa biases por seleção (útil com 48+ jogos)')
    parser.add_argument('--lambda',  dest='lam', type=float, default=DEFAULT_LAMBDA,
                        help=f'Força L2 nos biases (default: {DEFAULT_LAMBDA})')
    parser.add_argument('--iters',    type=int,   default=DEFAULT_ITERS)
    parser.add_argument('--restarts', type=int,   default=DEFAULT_RESTARTS)
    parser.add_argument('--T0',       type=float, default=DEFAULT_T0)
    parser.add_argument('--alpha',    type=float, default=DEFAULT_ALPHA)
    parser.add_argument('--seed',     type=int,   default=2026)
    args = parser.parse_args()

    T_final  = args.T0 * (args.alpha ** args.iters)

    print("=" * 72)
    print("  Simulated Annealing — Calibração xG  |  Copa do Mundo 2026")
    print("=" * 72)
    print(f"  Iters/restart : {args.iters:,}")
    print(f"  Restarts      : {args.restarts}")
    print(f"  T0 → T_final  : {args.T0} → {T_final:.5f}")
    print(f"  alpha         : {args.alpha}")
    print(f"  Seed          : {args.seed}")
    print(f"  Outliers      : {'excluídos' if args.exclude_outliers else 'incluídos'}")
    print(f"  Modo biases   : {'SIM  (λ=' + str(args.lam) + ')' if args.biases else 'NÃO'}")
    print("=" * 72)

    print("\nCarregando dados...")
    matches, scores, teams_list, teams_idx = load_data(args.exclude_outliers)
    print(f"  {len(matches)} jogos  |  {len(teams_list)} seleções")
    if args.biases:
        n_params = N_GLOBAL + 2 * len(teams_list)
        print(f"  Parâmetros totais: {n_params}  ({N_GLOBAL} globais + {2*len(teams_list)} biases)")

    # ── Baselines ─────────────────────────────────────────────────────────────

    nll_default, brier_default = evaluate(DEFAULTS, matches, scores)
    print(f"\n  NLL baseline (originais): {nll_default:.4f}  Brier: {brier_default:.4f}")

    lbfgs_theta = lbfgs_nll = lbfgs_brier = None
    if os.path.exists(LBFGS_FILE):
        with open(LBFGS_FILE) as f:
            lb = json.load(f)
        lbfgs_theta = [lb['weights']['BASE_XG'], lb['weights']['OFF_ATT_W'],
                       lb['weights']['RES_DEF_W'], lb['weights']['RES_GK_W']]
        lbfgs_nll, lbfgs_brier = evaluate(lbfgs_theta, matches, scores)
        print(f"  NLL L-BFGS-B:             {lbfgs_nll:.4f}  Brier: {lbfgs_brier:.4f}")
        print(f"  θ L-BFGS-B: {format_globals(lbfgs_theta)}")

    # ── SA ────────────────────────────────────────────────────────────────────

    rng = random.Random(args.seed)
    global_best_theta = None
    global_best_loss  = float('inf')
    t_total = time.time()

    for r in range(args.restarts):
        theta, loss = simulated_annealing(
            matches, scores,
            n_iter      = args.iters,
            T0          = args.T0,
            alpha       = args.alpha,
            rng         = rng,
            restart_idx = r,
            n_restarts  = args.restarts,
            use_biases  = args.biases,
            teams_idx   = teams_idx,
            teams_list  = teams_list,
            lam         = args.lam,
        )
        if loss < global_best_loss:
            global_best_loss  = loss
            global_best_theta = theta[:]
            print(f"  *** Novo melhor global: loss={loss:.4f} ***")

    elapsed = time.time() - t_total

    # ── Resultado final ───────────────────────────────────────────────────────

    eval_idx = teams_idx if args.biases else None
    nll_sa, brier_sa = evaluate(global_best_theta, matches, scores, eval_idx)

    print(f"\n{'=' * 72}")
    print(f"  RESULTADO FINAL  ({elapsed:.1f}s total)")
    print(f"{'=' * 72}\n")

    print(f"  {'Método':<22} {'NLL':>8}  {'Δ default':>10}  {'Brier':>8}")
    print(f"  {'-'*22} {'-'*8}  {'-'*10}  {'-'*8}")
    print(f"  {'Padrão (original)':<22} {nll_default:>8.4f}  {'—':>10}  {brier_default:>8.4f}")
    if lbfgs_nll is not None:
        print(f"  {'L-BFGS-B':<22} {lbfgs_nll:>8.4f}  {lbfgs_nll-nll_default:>+10.4f}  {lbfgs_brier:>8.4f}")
    print(f"  {'SA':<22} {nll_sa:>8.4f}  {nll_sa-nll_default:>+10.4f}  {brier_sa:>8.4f}")

    # globais
    print(f"\n  Parâmetros globais SA:")
    orig = dict(zip(PARAM_NAMES, DEFAULTS))
    for i, name in enumerate(PARAM_NAMES):
        print(f"    {name:<12} = {global_best_theta[i]:.4f}  (era {orig[name]})")

    # biases
    if args.biases:
        n_teams = len(teams_list)
        print(f"\n  Biases por seleção (λ={args.lam}):")
        bias_rows = []
        for i, team in enumerate(teams_list):
            att = global_best_theta[N_GLOBAL + i]
            dfb = global_best_theta[N_GLOBAL + n_teams + i]
            bias_rows.append((team, att, dfb))
        bias_rows.sort(key=lambda x: -(abs(x[1]-1) + abs(x[2]-1)))
        print(f"  {'Seleção':<28} {'att_bias':>10}  {'def_bias':>10}")
        print(f"  {'-'*28} {'-'*10}  {'-'*10}")
        for team, att, dfb in bias_rows:
            flag = " ←" if abs(att-1) > 0.15 or abs(dfb-1) > 0.15 else ""
            print(f"  {team:<28} {att:>10.4f}  {dfb:>10.4f}{flag}")

    # veredicto vs L-BFGS-B
    if lbfgs_nll is not None:
        if nll_sa < lbfgs_nll - 0.01:
            verdict = "SA encontrou mínimo MELHOR que L-BFGS-B"
        elif nll_sa > lbfgs_nll + 0.01:
            verdict = "L-BFGS-B mantém resultado melhor"
        else:
            verdict = "SA e L-BFGS-B convergiram para mínimo equivalente"
        print(f"\n  Veredicto: {verdict}")

    # ── Salva ─────────────────────────────────────────────────────────────────

    w_global = {
        'BASE_XG':   round(global_best_theta[0], 4),
        'OFF_ATT_W': round(global_best_theta[1], 4),
        'OFF_MID_W': round(1.0 - global_best_theta[1], 4),
        'RES_DEF_W': round(global_best_theta[2], 4),
        'RES_GK_W':  round(global_best_theta[3], 4),
        'RES_MID_W': round(max(1.0 - global_best_theta[2] - global_best_theta[3], 0.05), 4),
    }

    out = {
        'method':           'simulated_annealing',
        'n_matches':        len(matches),
        'exclude_outliers': args.exclude_outliers,
        'use_biases':       args.biases,
        'sa_params': {
            'n_iter':     args.iters,
            'n_restarts': args.restarts,
            'T0':         args.T0,
            'alpha':      args.alpha,
            'T_final':    round(T_final, 6),
            'seed':       args.seed,
            'lambda':     args.lam if args.biases else None,
        },
        'nll_default': round(nll_default, 4),
        'nll_sa':      round(nll_sa,      4),
        'nll_lbfgs':   round(lbfgs_nll,   4) if lbfgs_nll else None,
        'brier_default': round(brier_default, 4),
        'brier_sa':      round(brier_sa,      4),
        'brier_lbfgs':   round(lbfgs_brier,   4) if lbfgs_brier else None,
        'weights': w_global,
    }

    if args.biases:
        n_teams = len(teams_list)
        out['biases'] = {
            team: {
                'att_bias': round(global_best_theta[N_GLOBAL + i], 4),
                'def_bias': round(global_best_theta[N_GLOBAL + n_teams + i], 4),
            }
            for i, team in enumerate(teams_list)
        }

    with open(OUT_FILE, 'w') as f:
        json.dump(out, f, indent=2)

    print(f"\n  Salvo em {OUT_FILE}")
    print("=" * 72)


if __name__ == '__main__':
    main()
