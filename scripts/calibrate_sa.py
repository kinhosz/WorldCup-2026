#!/usr/bin/env python3
"""
calibrate_sa.py — calibrar constantes xG via Simulated Annealing.

Modo padrão (4 parâmetros livres):
  θ = [BASE_XG, w_att, w_def, w_gk]

Modo att-only (--att-only, recomendado para ~44 jogos / R2-R3):
  θ = [BASE_XG, w_att, w_def, w_gk, att_bias_t1..tN]
  xG_A = BASE_XG × (off_A × att_bias_A) / res_B      (def_bias fixo em 1.0)
  loss  = NLL + λ × Σ (att_bias − 1)²
  52 parâmetros para 88 observações — ratio aceitável com regularização.

Modo biases completo (--biases, recomendado a partir da R3 com ~72+ jogos):
  θ = [BASE_XG, w_att, w_def, w_gk, att_bias_t1..tN, def_bias_t1..tN]
  xG_A = BASE_XG × (off_A × att_bias_A) / (res_B × def_bias_B)
  loss  = NLL + λ × Σ (bias − 1)²

SA schedule:
  T(k) = T0 × alpha^k
  Aceita solução pior com P = exp(−Δloss / T)
  Perturbação: 50% parâmetros globais, 50% biases (quando ativo)

Uso:
  python3 scripts/calibrate_sa.py
  python3 scripts/calibrate_sa.py --exclude-outliers
  python3 scripts/calibrate_sa.py --att-only --lambda 1.5
  python3 scripts/calibrate_sa.py --att-only --iters 500000 --restarts 5
  python3 scripts/calibrate_sa.py --biases --lambda 2.0
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

# ── Parâmetros unconstrained (BASE_XG=1.0 fixo, 5 pesos livres) ──────────────

N_GLOBAL_UC    = 5
PARAM_NAMES_UC = ["w_att", "w_mid_off", "w_def", "w_gk", "w_mid_res"]
DEFAULTS_UC    = [0.82,     0.33,        0.45,    0.05,   0.50]
BOUNDS_UC      = [(0.05, 5.0), (0.05, 5.0), (0.05, 4.0), (0.02, 2.0), (0.05, 4.0)]
STEP_GLOBAL_UC = [0.05,     0.04,        0.04,    0.02,   0.04]
FIXED_BASE_XG  = 1.0

# ── Biases ────────────────────────────────────────────────────────────────────

BIAS_BOUNDS  = (0.20, 5.00)
BIAS_STEP    = 0.05
BIAS_DEFAULT = 1.0

# ── SA defaults ───────────────────────────────────────────────────────────────

DEFAULT_T0       = 3.0
DEFAULT_ALPHA    = 0.99996
DEFAULT_ITERS    = 300_000
DEFAULT_RESTARTS = 5
DEFAULT_LAMBDA   = 1.0
LOG_EVERY        = 10_000

# ── Grupos e pesos por rodada ─────────────────────────────────────────────────

GROUPS = {
    "A": ["mexico", "south_africa", "republic_of_korea", "czech_republic"],
    "B": ["canada", "bosnia_and_herzegovina", "qatar", "switzerland"],
    "C": ["brazil", "morocco", "haiti", "scotland"],
    "D": ["united_states_of_america", "paraguay", "australia", "turkey"],
    "E": ["germany", "curacao", "ivory_coast", "ecuador"],
    "F": ["netherlands", "japan", "sweden", "tunisia"],
    "G": ["belgium", "egypt", "ira", "new_zealand"],
    "H": ["spain", "cape_verte", "saudi_arabia", "uruguay"],
    "I": ["france", "senegal", "iraq", "norway"],
    "J": ["argentina", "algeria", "austria", "jordan"],
    "K": ["portugal", "congo", "uzbekistan", "colombia"],
    "L": ["england", "croatia", "ghana", "panama"],
}

ROUND_WEIGHTS = {
    'r1':    0.5,
    'r2':    0.5,
    'r3':    0.25,
    'r32':   1.0,
    'r16':   1.0,
    'qf':    1.0,
    'sf':    1.0,    # ainda não jogado — assumido igual ao resto do mata-mata
    'final': 1.0,    # idem
}

# Objetivo Model6: maximizar pontos, não minimizar NLL. Pontos = acerto do
# resultado (peso da rodada acima) + bônus de placar exato só no mata-mata
# (fase de grupos não ganha bônus de placar, só o ponto de W/D/L).
KNOCKOUT_ROUNDS  = {'r32', 'r16', 'qf', 'sf', 'final'}
TOP_SCORE_BONUS  = [1.0, 2 / 3, 4 / 9]   # queda constante (razão 2/3) — top1/top2/top3
SCORE_BONUS_GRID = 10                     # 0..9 gols cobre a massa de probabilidade relevante


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Fórmula xG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _get(s, key):
    v = s.get(key)
    return v if v is not None else FALLBACK


def _group_round(ta, tb):
    """Determina rodada (1/2/3) de um jogo da fase de grupos pelo padrão round-robin."""
    for members in GROUPS.values():
        if ta in members and tb in members:
            ia, ib = members.index(ta), members.index(tb)
            pair = frozenset([ia, ib])
            if pair in (frozenset([0, 1]), frozenset([2, 3])):
                return 1
            elif pair in (frozenset([0, 2]), frozenset([1, 3])):
                return 2
            else:
                return 3
    return 1


def _knockout_round(match_id):
    """Mapeia ID de jogo do mata-mata para fase (r32/r16/qf/sf/final)."""
    mid = int(match_id)
    if mid <= 88:  return 'r32'
    if mid <= 96:  return 'r16'
    if mid <= 100: return 'qf'
    if mid <= 102: return 'sf'
    return 'final'


def _parse_score(score_str, note=None):
    """Extrai o placar de 90' de score_str, ignorando prorrogação/pênaltis.

    Formatos suportados: '1–1', '2-0', '1–1 pen.', '3–2 (1–1 AET)'.
    Em jogos AET, o placar de 90' vem entre parênteses — a prorrogação não
    entra no treino (decisão de projeto: modelar só os 90').
    """
    s = score_str.replace('–', '-').replace('—', '-')
    if note == 'AET':
        s = s[s.index('(') + 1:s.index(')')]
    else:
        s = s.split('(')[0]
    s = s.replace('pen.', '').replace('PEN', '').replace('AET', '').strip()
    a, b = s.split('-')
    return int(a.strip()), int(b.strip())


def compute_xg(s_a, s_b, theta, uc=False):
    """Sem biases — modo padrão.
    uc=True: BASE_XG=1.0 fixo, 5 pesos livres (sem restrição de soma).
    """
    if uc:
        w_att, w_mid_off, w_def, w_gk, w_mid_res = theta[:N_GLOBAL_UC]
        base_xg = FIXED_BASE_XG
    else:
        base_xg, w_att, w_def, w_gk = theta[:N_GLOBAL]
        w_mid_off = 1.0 - w_att
        w_mid_res = max(1.0 - w_def - w_gk, 0.05)

    off_a = w_att * _get(s_a, 'attack')  + w_mid_off * _get(s_a, 'midfield')
    off_b = w_att * _get(s_b, 'attack')  + w_mid_off * _get(s_b, 'midfield')
    res_a = max(w_def * _get(s_a, 'defense') + w_gk * _get(s_a, 'goalkeeper') + w_mid_res * _get(s_a, 'midfield'), RES_FLOOR)
    res_b = max(w_def * _get(s_b, 'defense') + w_gk * _get(s_b, 'goalkeeper') + w_mid_res * _get(s_b, 'midfield'), RES_FLOOR)
    return min(base_xg * off_a / res_b, MAX_XG), min(base_xg * off_b / res_a, MAX_XG)


def compute_xg_biased(s_a, s_b, theta, idx_a, idx_b, n_teams, att_only=False, uc=False):
    """Com biases por seleção.
    att_only=True: só att_bias (def_bias fixo em 1.0).
    uc=True: BASE_XG=1.0 fixo, 5 pesos livres (biases indexados a partir de N_GLOBAL_UC).
    """
    ng = N_GLOBAL_UC if uc else N_GLOBAL
    if uc:
        w_att, w_mid_off, w_def, w_gk, w_mid_res = theta[:ng]
        base_xg = FIXED_BASE_XG
    else:
        base_xg, w_att, w_def, w_gk = theta[:ng]
        w_mid_off = 1.0 - w_att
        w_mid_res = max(1.0 - w_def - w_gk, 0.05)

    att_bias_a = theta[ng + idx_a]
    att_bias_b = theta[ng + idx_b]

    if att_only:
        def_bias_a = def_bias_b = 1.0
    else:
        def_bias_a = theta[ng + n_teams + idx_a]
        def_bias_b = theta[ng + n_teams + idx_b]

    off_a = (w_att * _get(s_a, 'attack') + w_mid_off * _get(s_a, 'midfield')) * att_bias_a
    off_b = (w_att * _get(s_b, 'attack') + w_mid_off * _get(s_b, 'midfield')) * att_bias_b
    res_a = max((w_def * _get(s_a, 'defense') + w_gk * _get(s_a, 'goalkeeper') + w_mid_res * _get(s_a, 'midfield')) * def_bias_a, RES_FLOOR)
    res_b = max((w_def * _get(s_b, 'defense') + w_gk * _get(s_b, 'goalkeeper') + w_mid_res * _get(s_b, 'midfield')) * def_bias_b, RES_FLOOR)
    return min(base_xg * off_a / res_b, MAX_XG), min(base_xg * off_b / res_a, MAX_XG)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Loss functions
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def poisson_nll(theta, matches, scores, teams_idx=None, lam=0.0, att_only=False, uc=False):
    """
    NLL = Σ [ xg − k × log(xg) ].
    Se teams_idx fornecido, usa compute_xg_biased + regularização L2.
    att_only=True: só att_bias (def fixo em 1.0), regulariza apenas N biases.
    uc=True: modo unconstrained (BASE_XG=1.0, 5 pesos livres).
    """
    ng = N_GLOBAL_UC if uc else N_GLOBAL
    total = 0.0
    if teams_idx is not None:
        n_teams = len(teams_idx)
        for m in matches:
            xg_a, xg_b = compute_xg_biased(
                scores[m['team_a']], scores[m['team_b']], theta,
                teams_idx[m['team_a']], teams_idx[m['team_b']], n_teams,
                att_only=att_only, uc=uc,
            )
            w = m.get('weight', 1.0)
            total += w * (xg_a - m['goals_a'] * math.log(max(xg_a, 1e-9)))
            total += w * (xg_b - m['goals_b'] * math.log(max(xg_b, 1e-9)))
        n_biases = n_teams if att_only else 2 * n_teams
        biases = theta[ng:ng + n_biases]
        total += lam * sum((b - 1.0) ** 2 for b in biases)
    else:
        for m in matches:
            xg_a, xg_b = compute_xg(scores[m['team_a']], scores[m['team_b']], theta, uc=uc)
            w = m.get('weight', 1.0)
            total += w * (xg_a - m['goals_a'] * math.log(max(xg_a, 1e-9)))
            total += w * (xg_b - m['goals_b'] * math.log(max(xg_b, 1e-9)))
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
#  Objetivo por pontos (Model6) — usado no loop quente do SA, sem scipy
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _pmf(lam, max_k):
    """Poisson pmf k=0..max_k via recorrência — evita overhead do scipy no loop quente do SA."""
    p = math.exp(-lam)
    out = [p]
    for k in range(1, max_k + 1):
        p *= lam / k
        out.append(p)
    return out


def _outcome_probs(pa, pb):
    """win_a, draw, win_b via somas cumulativas — O(n), sem outer product."""
    n = len(pa)
    cum_b = [0.0] * (n + 1)
    for j in range(n):
        cum_b[j + 1] = cum_b[j] + pb[j]
    total_b = cum_b[n]
    win_a = sum(pa[i] * cum_b[i] for i in range(n))
    draw  = sum(pa[i] * pb[i] for i in range(n))
    win_b = sum(pa[i] * (total_b - cum_b[i + 1]) for i in range(n))
    s = win_a + draw + win_b
    if s <= 0:
        return 1 / 3, 1 / 3, 1 / 3
    return win_a / s, draw / s, win_b / s


def _score_bonus(pa, pb, ga, gb, grid=SCORE_BONUS_GRID):
    """Bônus de placar exato — só chamado para jogos de mata-mata.

    Conta quantos placares da grade têm probabilidade estritamente maior que o
    placar real; rank 0 = placar mais provável do modelo (top-1).
    """
    if ga >= len(pa) or gb >= len(pb):
        return 0.0
    p_actual = pa[ga] * pb[gb]
    rank = 0
    for i in range(grid):
        pai = pa[i] if i < len(pa) else 0.0
        for j in range(grid):
            pbj = pb[j] if j < len(pb) else 0.0
            if pai * pbj > p_actual:
                rank += 1
                if rank >= 3:
                    return 0.0
    return TOP_SCORE_BONUS[rank]


def points_score(theta, matches, scores, teams_idx=None, att_only=False, uc=False, max_goals=MAX_GOALS):
    """Pontos totais: acerto do resultado (peso da rodada) + bônus de placar exato (só mata-mata)."""
    n_teams = len(teams_idx) if teams_idx is not None else 0
    total = 0.0
    for m in matches:
        if teams_idx is not None:
            xg_a, xg_b = compute_xg_biased(
                scores[m['team_a']], scores[m['team_b']], theta,
                teams_idx[m['team_a']], teams_idx[m['team_b']], n_teams,
                att_only=att_only, uc=uc,
            )
        else:
            xg_a, xg_b = compute_xg(scores[m['team_a']], scores[m['team_b']], theta, uc=uc)

        pa = _pmf(xg_a, max_goals)
        pb = _pmf(xg_b, max_goals)
        win_a, draw, win_b = _outcome_probs(pa, pb)

        if m['round'] in KNOCKOUT_ROUNDS:
            pred = 'a' if (win_a + 0.5 * draw) >= 0.5 else 'b'
            if pred == m['winner_side']:
                total += m['weight']
            total += _score_bonus(pa, pb, m['goals_a'], m['goals_b'])
        else:
            if win_a >= draw and win_a >= win_b:
                pred = 'a'
            elif draw >= win_b:
                pred = 'draw'
            else:
                pred = 'b'
            if pred == m['outcome']:
                total += m['weight']

    return total


def max_possible_points(matches):
    return sum(m['weight'] for m in matches) + sum(
        TOP_SCORE_BONUS[0] for m in matches if m['round'] in KNOCKOUT_ROUNDS
    )


def neg_points_loss(theta, matches, scores, teams_idx=None, lam=0.0, att_only=False, uc=False):
    """Objetivo do SA: minimizar -pontos + regularização L2 dos biases (desempate suave)."""
    loss = -points_score(theta, matches, scores, teams_idx, att_only, uc)
    if teams_idx is not None:
        ng = N_GLOBAL_UC if uc else N_GLOBAL
        n_teams = len(teams_idx)
        n_biases = n_teams if att_only else 2 * n_teams
        biases = theta[ng:ng + n_biases]
        loss += lam * sum((b - 1.0) ** 2 for b in biases)
    return loss


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SA — vizinhança e perturbação
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_initial_theta(rng, use_biases, n_teams, is_first_restart, att_only=False, uc=False):
    bounds_g   = BOUNDS_UC   if uc else BOUNDS
    defaults_g = DEFAULTS_UC if uc else DEFAULTS
    if is_first_restart:
        global_part = defaults_g[:]
    else:
        global_part = [rng.uniform(lo, hi) for lo, hi in bounds_g]

    if not use_biases:
        return global_part

    n_biases = n_teams if att_only else 2 * n_teams
    return global_part + [BIAS_DEFAULT] * n_biases


def neighbor(theta, rng, use_biases, n_teams, att_only=False, uc=False):
    """
    Seleciona um parâmetro para perturbar.
    Com biases: 50% chance de mexer num global, 50% num bias.
    """
    new_theta = theta[:]
    ng       = N_GLOBAL_UC if uc else N_GLOBAL
    bounds_g = BOUNDS_UC   if uc else BOUNDS
    steps_g  = STEP_GLOBAL_UC if uc else STEP_GLOBAL

    if use_biases and rng.random() >= 0.50:
        n_biases = n_teams if att_only else 2 * n_teams
        i = ng + rng.randint(0, n_biases - 1)
        delta = rng.gauss(0, BIAS_STEP)
        lo, hi = BIAS_BOUNDS
    else:
        i = rng.randint(0, ng - 1)
        delta = rng.gauss(0, steps_g[i])
        lo, hi = bounds_g[i]

    new_theta[i] = min(max(new_theta[i] + delta, lo), hi)
    return new_theta


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Logging
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def format_globals(theta, uc=False):
    names = PARAM_NAMES_UC if uc else PARAM_NAMES
    return "  ".join(f"{n}={theta[i]:.4f}" for i, n in enumerate(names))


def format_top_biases(theta, teams_list, n_top=5, att_only=False, uc=False):
    """Mostra os biases com maior desvio de 1.0."""
    ng = N_GLOBAL_UC if uc else N_GLOBAL
    n_teams = len(teams_list)
    entries = []
    for i, team in enumerate(teams_list):
        att = theta[ng + i]
        dfb = 1.0 if att_only else theta[ng + n_teams + i]
        entries.append((abs(att - 1.0) + abs(dfb - 1.0), team, att, dfb))
    entries.sort(reverse=True)
    if att_only:
        parts = [f"{t}(att={a:.2f})" for _, t, a, _ in entries[:n_top]]
    else:
        parts = [f"{t}(att={a:.2f},def={d:.2f})" for _, t, a, d in entries[:n_top]]
    return "  ".join(parts)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SA — loop principal
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def simulated_annealing(matches, scores, n_iter, T0, alpha, rng,
                        restart_idx, n_restarts, use_biases,
                        teams_idx, teams_list, lam, att_only=False, uc=False):
    n_teams   = len(teams_list)
    theta     = build_initial_theta(rng, use_biases, n_teams, restart_idx == 0, att_only, uc)
    curr_loss = neg_points_loss(theta, matches, scores, teams_idx if use_biases else None, lam, att_only, uc)
    best_theta = theta[:]
    best_loss  = curr_loss

    T = T0
    accepts_window = 0
    total_window   = 0
    t_start = time.time()

    if att_only:
        mode_str = f"att-only λ={lam}"
    elif use_biases:
        mode_str = f"biases λ={lam}"
    else:
        mode_str = "sem biases"
    if uc:
        mode_str += " [unc]"

    n_params = len(theta)
    print(f"\n{'━'*72}")
    print(f"  Restart {restart_idx+1}/{n_restarts}  |  {n_iter:,} iters  |  T0={T0}  |  {mode_str}  |  θ={n_params}")
    print(f"  globals: {format_globals(theta, uc)}")
    print(f"  pontos iniciais: {-curr_loss:.3f}")
    print(f"{'━'*72}")

    for k in range(1, n_iter + 1):
        new_theta = neighbor(theta, rng, use_biases, n_teams, att_only, uc)
        new_loss  = neg_points_loss(new_theta, matches, scores, teams_idx if use_biases else None, lam, att_only, uc)

        delta        = new_loss - curr_loss
        total_window += 1

        if delta < 0 or rng.random() < math.exp(-delta / max(T, 1e-10)):
            theta     = new_theta
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
                f"  curr={-curr_loss:.3f}pts  best={-best_loss:.3f}pts"
            )
            print(f"    globals: {format_globals(best_theta, uc)}")
            if use_biases:
                print(f"    top bias: {format_top_biases(best_theta, teams_list, att_only=att_only, uc=uc)}")

            accepts_window = 0
            total_window   = 0

    elapsed = time.time() - t_start
    print(f"\n  Restart {restart_idx+1} concluído em {elapsed:.1f}s  |  best pontos={-best_loss:.3f}")

    return best_theta, best_loss


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Avaliação final
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def evaluate(theta, matches, scores, teams_idx=None, att_only=False, uc=False):
    """Retorna (nll_puro, brier_medio) — sem regularização para comparação justa."""
    nll = poisson_nll(theta, matches, scores, teams_idx, lam=0.0, att_only=att_only, uc=uc)
    brier_sum = 0.0
    for m in matches:
        if teams_idx is not None:
            n_teams = len(teams_idx)
            xg_a, xg_b = compute_xg_biased(
                scores[m['team_a']], scores[m['team_b']], theta,
                teams_idx[m['team_a']], teams_idx[m['team_b']], n_teams,
                att_only=att_only, uc=uc,
            )
        else:
            xg_a, xg_b = compute_xg(scores[m['team_a']], scores[m['team_b']], theta, uc=uc)
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
            rnd = _group_round(ta, tb)
            w   = ROUND_WEIGHTS[f'r{rnd}']
            out = 'a' if ga > gb else ('b' if ga < gb else 'draw')
            matches.append({'team_a': ta, 'team_b': tb,
                            'goals_a': ga, 'goals_b': gb,
                            'outcome': out, 'weight': w, 'round': f'r{rnd}'})

    for mid, game in state.get('knockout_results', {}).items():
        ta, tb = game['home'], game['away']
        if ta not in scores or tb not in scores:
            continue
        ga, gb = _parse_score(game['score_str'], game.get('note'))
        out = 'a' if ga > gb else ('b' if ga < gb else 'draw')
        rnd = _knockout_round(mid)
        w   = ROUND_WEIGHTS[rnd]
        winner_side = 'a' if game['winner'] == ta else 'b'
        matches.append({'team_a': ta, 'team_b': tb,
                        'goals_a': ga, 'goals_b': gb,
                        'outcome': out, 'weight': w, 'round': rnd,
                        'winner_side': winner_side})

    if exclude_outliers:
        before  = len(matches)
        matches = [m for m in matches if abs(m['goals_a'] - m['goals_b']) < OUTLIER_MIN_GOAL_DIFF]
        print(f"  --exclude-outliers: {before - len(matches)} jogo(s) removido(s)")

    teams = sorted({m['team_a'] for m in matches} | {m['team_b'] for m in matches})
    teams_idx = {t: i for i, t in enumerate(teams)}

    return matches, scores, teams, teams_idx


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exclude-outliers', action='store_true')

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--att-only', action='store_true',
                            help='Biases somente de ataque por seleção (recomendado para ~44 jogos)')
    mode_group.add_argument('--biases', action='store_true',
                            help='Biases att+def por seleção (recomendado para 72+ jogos)')

    parser.add_argument('--unconstrained', action='store_true',
                        help='BASE_XG=1.0 fixo, 5 pesos livres (sem restrição de soma)')
    parser.add_argument('--lambda',  dest='lam', type=float, default=DEFAULT_LAMBDA)
    parser.add_argument('--iters',    type=int,   default=DEFAULT_ITERS)
    parser.add_argument('--restarts', type=int,   default=DEFAULT_RESTARTS)
    parser.add_argument('--T0',       type=float, default=DEFAULT_T0)
    parser.add_argument('--alpha',    type=float, default=DEFAULT_ALPHA)
    parser.add_argument('--seed',     type=int,   default=2026)
    parser.add_argument('--output',   type=str,   default=OUT_FILE,
                        help='Arquivo de saída JSON (default: output/calibrated_weights_sa.json)')
    args = parser.parse_args()

    use_biases = args.biases or args.att_only
    att_only   = args.att_only
    uc         = args.unconstrained

    T_final = args.T0 * (args.alpha ** args.iters)

    if att_only:
        mode_label = f"att-only  (λ={args.lam})"
    elif use_biases:
        mode_label = f"biases att+def  (λ={args.lam})"
    else:
        mode_label = "sem biases"
    if uc:
        mode_label += "  [unconstrained, BASE_XG=1.0]"

    print("=" * 72)
    print("  Simulated Annealing — Calibração xG  |  Copa do Mundo 2026")
    print("=" * 72)
    print(f"  Iters/restart : {args.iters:,}")
    print(f"  Restarts      : {args.restarts}")
    print(f"  T0 → T_final  : {args.T0} → {T_final:.5f}")
    print(f"  alpha         : {args.alpha}")
    print(f"  Seed          : {args.seed}")
    print(f"  Outliers      : {'excluídos' if args.exclude_outliers else 'incluídos'}")
    print(f"  Modo          : {mode_label}")
    print("=" * 72)

    print("\nCarregando dados...")
    matches, scores, teams_list, teams_idx = load_data(args.exclude_outliers)
    ng = N_GLOBAL_UC if uc else N_GLOBAL
    from collections import Counter
    round_counts = Counter(m['round'] for m in matches)
    print(f"  {len(matches)} jogos  |  {len(teams_list)} seleções")
    print(f"  Jogos por rodada: { {r: round_counts[r] for r in ['r1','r2','r3','r32','r16','qf','sf','final'] if round_counts[r]} }")
    rw = ROUND_WEIGHTS
    print(f"  Pesos por rodada: r1={rw['r1']}  r2={rw['r2']}  r3={rw['r3']}  r32={rw['r32']}  "
          f"r16={rw['r16']}  qf={rw['qf']}  sf={rw['sf']}  final={rw['final']}")
    print(f"  Bônus placar exato (só mata-mata): top1={TOP_SCORE_BONUS[0]:.3f}  "
          f"top2={TOP_SCORE_BONUS[1]:.3f}  top3={TOP_SCORE_BONUS[2]:.3f}")
    max_pts = max_possible_points(matches)
    print(f"  Pontos máximos possíveis: {max_pts:.3f}")
    if uc:
        print(f"  Modo unconstrained: {ng} pesos livres, BASE_XG={FIXED_BASE_XG}")
    if use_biases:
        n_biases = len(teams_list) if att_only else 2 * len(teams_list)
        n_params = ng + n_biases
        print(f"  Parâmetros totais: {n_params}  ({ng} globais + {n_biases} biases)")
        print(f"  Ratio params/dados: {n_params}/{len(matches)*2} = {n_params/(len(matches)*2):.2f}")

    # ── Baselines ─────────────────────────────────────────────────────────────

    defaults_g = DEFAULTS_UC if uc else DEFAULTS
    nll_default, brier_default = evaluate(defaults_g, matches, scores, uc=uc)
    points_default = points_score(defaults_g, matches, scores, uc=uc)
    print(f"\n  NLL baseline (defaults): {nll_default:.4f}  Brier: {brier_default:.4f}  "
          f"Pontos: {points_default:.3f}/{max_pts:.3f}")

    lbfgs_theta = lbfgs_nll = lbfgs_brier = lbfgs_points = None
    if not uc and os.path.exists(LBFGS_FILE):
        with open(LBFGS_FILE) as f:
            lb = json.load(f)
        lbfgs_theta = [lb['weights']['BASE_XG'], lb['weights']['OFF_ATT_W'],
                       lb['weights']['RES_DEF_W'], lb['weights']['RES_GK_W']]
        lbfgs_nll, lbfgs_brier = evaluate(lbfgs_theta, matches, scores)
        lbfgs_points = points_score(lbfgs_theta, matches, scores)
        print(f"  NLL L-BFGS-B:            {lbfgs_nll:.4f}  Brier: {lbfgs_brier:.4f}  "
              f"Pontos: {lbfgs_points:.3f}/{max_pts:.3f}")
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
            use_biases  = use_biases,
            teams_idx   = teams_idx,
            teams_list  = teams_list,
            lam         = args.lam,
            att_only    = att_only,
            uc          = uc,
        )
        if loss < global_best_loss:
            global_best_loss  = loss
            global_best_theta = theta[:]
            print(f"  *** Novo melhor global: pontos={-loss:.3f} ***")

    elapsed = time.time() - t_total

    # ── Resultado final ───────────────────────────────────────────────────────

    eval_idx = teams_idx if use_biases else None
    nll_sa, brier_sa = evaluate(global_best_theta, matches, scores, eval_idx, att_only, uc)
    points_sa = points_score(global_best_theta, matches, scores, eval_idx, att_only, uc)

    print(f"\n{'=' * 72}")
    print(f"  RESULTADO FINAL  ({elapsed:.1f}s total)")
    print(f"{'=' * 72}\n")

    print(f"  {'Método':<22} {'Pontos':>14}  {'NLL':>8}  {'Δ default':>10}  {'Brier':>8}")
    print(f"  {'-'*22} {'-'*14}  {'-'*8}  {'-'*10}  {'-'*8}")
    print(f"  {'Padrão (original)':<22} {points_default:>7.3f}/{max_pts:<6.3f}  {nll_default:>8.4f}  {'—':>10}  {brier_default:>8.4f}")
    if lbfgs_nll is not None:
        print(f"  {'L-BFGS-B':<22} {lbfgs_points:>7.3f}/{max_pts:<6.3f}  {lbfgs_nll:>8.4f}  {lbfgs_nll-nll_default:>+10.4f}  {lbfgs_brier:>8.4f}")
    print(f"  {'SA (Model6)':<22} {points_sa:>7.3f}/{max_pts:<6.3f}  {nll_sa:>8.4f}  {nll_sa-nll_default:>+10.4f}  {brier_sa:>8.4f}")
    print(f"\n  SA capturou {points_sa/max_pts*100:.1f}% dos pontos possíveis "
          f"({points_default/max_pts*100:.1f}% no baseline padrão)")

    param_names_g = PARAM_NAMES_UC if uc else PARAM_NAMES
    defaults_g    = DEFAULTS_UC   if uc else DEFAULTS
    print(f"\n  Parâmetros globais SA:")
    orig = dict(zip(param_names_g, defaults_g))
    for i, name in enumerate(param_names_g):
        print(f"    {name:<12} = {global_best_theta[i]:.4f}  (default {orig[name]})")
    if uc:
        print(f"    {'BASE_XG':<12} = {FIXED_BASE_XG}  (fixo)")

    if use_biases:
        n_teams = len(teams_list)
        print(f"\n  Biases por seleção ({mode_label}):")
        bias_rows = []
        for i, team in enumerate(teams_list):
            att = global_best_theta[ng + i]
            dfb = 1.0 if att_only else global_best_theta[ng + n_teams + i]
            bias_rows.append((team, att, dfb))
        bias_rows.sort(key=lambda x: -(abs(x[1]-1) + abs(x[2]-1)))
        header = f"  {'Seleção':<28} {'att_bias':>10}" + ("" if att_only else f"  {'def_bias':>10}")
        print(header)
        print(f"  {'-'*28} {'-'*10}" + ("" if att_only else f"  {'-'*10}"))
        for team, att, dfb in bias_rows:
            flag = " ←" if abs(att-1) > 0.15 or (not att_only and abs(dfb-1) > 0.15) else ""
            if att_only:
                print(f"  {team:<28} {att:>10.4f}{flag}")
            else:
                print(f"  {team:<28} {att:>10.4f}  {dfb:>10.4f}{flag}")

    if lbfgs_points is not None:
        if points_sa > lbfgs_points + 0.01:
            verdict = "SA encontrou MAIS pontos que L-BFGS-B"
        elif points_sa < lbfgs_points - 0.01:
            verdict = "L-BFGS-B mantém resultado melhor em pontos"
        else:
            verdict = "SA e L-BFGS-B empatam em pontos"
        print(f"\n  Veredicto: {verdict}")

    # ── Salva ─────────────────────────────────────────────────────────────────

    if uc:
        w_global = {
            'BASE_XG':   FIXED_BASE_XG,
            'OFF_ATT_W': round(global_best_theta[0], 4),
            'OFF_MID_W': round(global_best_theta[1], 4),
            'RES_DEF_W': round(global_best_theta[2], 4),
            'RES_GK_W':  round(global_best_theta[3], 4),
            'RES_MID_W': round(global_best_theta[4], 4),
        }
    else:
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
        'objective':        'points',
        'n_matches':        len(matches),
        'round_weights':    ROUND_WEIGHTS,
        'top_score_bonus':  {'top1': TOP_SCORE_BONUS[0], 'top2': TOP_SCORE_BONUS[1], 'top3': TOP_SCORE_BONUS[2]},
        'exclude_outliers': args.exclude_outliers,
        'use_biases':       use_biases,
        'att_only':         att_only,
        'unconstrained':    uc,
        'sa_params': {
            'n_iter':     args.iters,
            'n_restarts': args.restarts,
            'T0':         args.T0,
            'alpha':      args.alpha,
            'T_final':    round(T_final, 6),
            'seed':       args.seed,
            'lambda':     args.lam if use_biases else None,
        },
        'max_points':      round(max_pts, 4),
        'points_default':  round(points_default, 4),
        'points_sa':       round(points_sa, 4),
        'points_lbfgs':    round(lbfgs_points, 4) if lbfgs_points is not None else None,
        'nll_default': round(nll_default, 4),
        'nll_sa':      round(nll_sa,      4),
        'nll_lbfgs':   round(lbfgs_nll,   4) if lbfgs_nll else None,
        'brier_default': round(brier_default, 4),
        'brier_sa':      round(brier_sa,      4),
        'brier_lbfgs':   round(lbfgs_brier,   4) if lbfgs_brier else None,
        'weights': w_global,
    }

    if use_biases:
        n_teams = len(teams_list)
        out['biases'] = {
            team: {
                'att_bias': round(global_best_theta[ng + i], 4),
                'def_bias': 1.0 if att_only else round(global_best_theta[ng + n_teams + i], 4),
            }
            for i, team in enumerate(teams_list)
        }

    with open(args.output, 'w') as f:
        json.dump(out, f, indent=2)

    print(f"\n  Salvo em {args.output}")
    print("=" * 72)


if __name__ == '__main__':
    main()
