#!/usr/bin/env python3
"""
model_compare.py — avalia e compara múltiplas configurações de modelo.

Sistema de pontuação RankScore:
  Rank 1: +10  Rank 2: +6  Rank 3: +3  Rank 4-5: +1
  Rank 6+ e P<2%: -5  |  Rank 6+ e P<5%: -2  |  Rank 6+ e P≥5%: 0

Uso:
  python scripts/model_compare.py              # avalia modelos disponíveis (S01–S07)
  python scripts/model_compare.py --calibrate  # roda calibrações pendentes, depois avalia
  python scripts/model_compare.py --save       # salva resultado em output/model_comparison.md
  python scripts/model_compare.py --verbose S01  # breakdown por jogo do modelo S01
"""

import argparse
import json
import math
import os
import subprocess
import sys

import numpy as np
from scipy.stats import poisson as sp_poisson

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT        = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SCORES_FILE = os.path.join(ROOT, 'output', 'team_scores.json')
STATE_FILE  = os.path.join(ROOT, 'output', 'copa_real_state.json')

MAX_GOALS  = 8
FALLBACK   = 0.5
RES_FLOOR  = 0.10
MAX_XG_VAL = 8.0

DEFAULT_WEIGHTS = {
    'BASE_XG':   1.30, 'OFF_ATT_W': 0.70, 'OFF_MID_W': 0.30,
    'RES_DEF_W': 0.60, 'RES_GK_W':  0.20, 'RES_MID_W': 0.20,
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Estratégias
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Campos:
#   file            → JSON de pesos (relativo ao ROOT)
#   weights + biases → inline (sem arquivo)
#   base_xg_factor  → multiplica BASE_XG após carregar arquivo
#   no_biases       → True: zera todos os biases (att=def=1.0)
#   calibrate_cmd   → comando para gerar o arquivo (quando ausente)

STRATEGIES = [
    # ── S01–S07: disponíveis agora ────────────────────────────────────────────
    {
        'id': 'S01',
        'name': 'SA+att_only 48g λ=1.5',
        'desc': 'Modelo atual em produção (calibrado R1+R2, 48 jogos)',
        'file': 'output/calibrated_weights_sa.json',
    },
    {
        'id': 'S02',
        'name': 'L-BFGS-B 48g',
        'desc': 'Calibração L-BFGS-B sem biases (referência, 48 jogos)',
        'file': 'output/calibrated_weights.json',
    },
    {
        'id': 'S03',
        'name': 'S01 + xG×1.20',
        'desc': 'Biases de S01, BASE_XG × 1.2 → mais gols esperados',
        'file': 'output/calibrated_weights_sa.json',
        'base_xg_factor': 1.20,
    },
    {
        'id': 'S04',
        'name': 'S01 + xG×1.40',
        'desc': 'Biases de S01, BASE_XG × 1.4',
        'file': 'output/calibrated_weights_sa.json',
        'base_xg_factor': 1.40,
    },
    {
        'id': 'S05',
        'name': 'S01 + xG×1.60',
        'desc': 'Biases de S01, BASE_XG × 1.6',
        'file': 'output/calibrated_weights_sa.json',
        'base_xg_factor': 1.60,
    },
    {
        'id': 'S06',
        'name': 'S01 sem biases',
        'desc': 'Pesos globais de S01, todos os biases removidos',
        'file': 'output/calibrated_weights_sa.json',
        'no_biases': True,
    },
    {
        'id': 'S07',
        'name': 'Default (sem calibração)',
        'desc': 'Pesos originais hardcoded, sem calibração nem biases',
        'weights': DEFAULT_WEIGHTS,
        'biases': {},
    },
    # ── S08–S18: precisam calibração com 72 jogos ─────────────────────────────
    {
        'id': 'S08',
        'name': 'SA global 72g',
        'desc': 'SA global sem biases, 72 jogos (R1+R2+R3)',
        'file': 'output/weights_s08.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--iters 500000 --restarts 5 '
            '--output output/weights_s08.json'
        ),
    },
    {
        'id': 'S09',
        'name': 'SA+att_only λ=0.5 72g',
        'desc': 'SA att_only λ baixo (biases agressivos), 72 jogos',
        'file': 'output/weights_s09.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--att-only --lambda 0.5 --iters 500000 --restarts 5 '
            '--output output/weights_s09.json'
        ),
    },
    {
        'id': 'S10',
        'name': 'SA+att_only λ=1.0 72g',
        'desc': 'SA att_only λ=1.0, 72 jogos',
        'file': 'output/weights_s10.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--att-only --lambda 1.0 --iters 500000 --restarts 5 '
            '--output output/weights_s10.json'
        ),
    },
    {
        'id': 'S11',
        'name': 'SA+att_only λ=1.5 72g',
        'desc': 'Mesmo setup de S01 mas com 72 jogos (R1+R2+R3)',
        'file': 'output/weights_s11.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--att-only --lambda 1.5 --iters 500000 --restarts 5 '
            '--output output/weights_s11.json'
        ),
    },
    {
        'id': 'S12',
        'name': 'SA+att_only λ=2.5 72g',
        'desc': 'SA att_only λ=2.5 (biases conservadores), 72 jogos',
        'file': 'output/weights_s12.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--att-only --lambda 2.5 --iters 500000 --restarts 5 '
            '--output output/weights_s12.json'
        ),
    },
    {
        'id': 'S13',
        'name': 'SA+biases att+def λ=1.0 72g',
        'desc': 'Biases att+def completos λ=1.0, 72 jogos',
        'file': 'output/weights_s13.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--biases --lambda 1.0 --iters 500000 --restarts 5 '
            '--output output/weights_s13.json'
        ),
    },
    {
        'id': 'S14',
        'name': 'SA+biases att+def λ=2.0 72g',
        'desc': 'Biases att+def λ=2.0, 72 jogos',
        'file': 'output/weights_s14.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--biases --lambda 2.0 --iters 500000 --restarts 5 '
            '--output output/weights_s14.json'
        ),
    },
    {
        'id': 'S15',
        'name': 'SA+biases att+def λ=3.0 72g',
        'desc': 'Biases att+def λ=3.0 (alta regularização), 72 jogos',
        'file': 'output/weights_s15.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--biases --lambda 3.0 --iters 500000 --restarts 5 '
            '--output output/weights_s15.json'
        ),
    },
    {
        'id': 'S16',
        'name': 'SA+att_only λ=1.5 72g −outliers',
        'desc': 'SA att_only λ=1.5, sem jogos com Δgols≥4',
        'file': 'output/weights_s16.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--att-only --lambda 1.5 --exclude-outliers --iters 500000 --restarts 5 '
            '--output output/weights_s16.json'
        ),
    },
    {
        'id': 'S17',
        'name': 'SA+biases λ=2.0 72g −outliers',
        'desc': 'Biases att+def λ=2.0, sem outliers, 72 jogos',
        'file': 'output/weights_s17.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--biases --lambda 2.0 --exclude-outliers --iters 500000 --restarts 5 '
            '--output output/weights_s17.json'
        ),
    },
    {
        'id': 'S18',
        'name': 'SA+att_only λ=1.0 72g −outliers',
        'desc': 'SA att_only λ=1.0, sem outliers, 72 jogos',
        'file': 'output/weights_s18.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--att-only --lambda 1.0 --exclude-outliers --iters 500000 --restarts 5 '
            '--output output/weights_s18.json'
        ),
    },
    # ── S19–S21: unconstrained (BASE_XG=1.0 fixo, 5 pesos livres) ────────────
    {
        'id': 'S19',
        'name': 'SA+biases att+def λ=2.0 unc',
        'desc': 'Pesos livres (BASE_XG=1.0), biases att+def λ=2.0, 72 jogos',
        'file': 'output/weights_s19.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--biases --lambda 2.0 --unconstrained --iters 500000 --restarts 5 '
            '--output output/weights_s19.json'
        ),
    },
    {
        'id': 'S20',
        'name': 'SA+biases att+def λ=1.0 unc',
        'desc': 'Pesos livres (BASE_XG=1.0), biases att+def λ=1.0, 72 jogos',
        'file': 'output/weights_s20.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--biases --lambda 1.0 --unconstrained --iters 500000 --restarts 5 '
            '--output output/weights_s20.json'
        ),
    },
    {
        'id': 'S21',
        'name': 'SA+att_only λ=2.0 unc',
        'desc': 'Pesos livres (BASE_XG=1.0), att_only λ=2.0, 72 jogos',
        'file': 'output/weights_s21.json',
        'calibrate_cmd': (
            'python scripts/calibrate_sa.py '
            '--att-only --lambda 2.0 --unconstrained --iters 500000 --restarts 5 '
            '--output output/weights_s21.json'
        ),
    },
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Funções xG + scoring
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _get(s, k):
    v = s.get(k)
    return v if v is not None else FALLBACK


def compute_xg(weights, biases, ta, tb, team_scores):
    w  = weights
    sa = team_scores[ta]
    sb = team_scores[tb]
    ab = biases.get(ta, {}).get('att_bias', 1.0)
    bb = biases.get(tb, {}).get('att_bias', 1.0)
    db = biases.get(ta, {}).get('def_bias', 1.0)
    eb = biases.get(tb, {}).get('def_bias', 1.0)
    off_a = ab * (w['OFF_ATT_W'] * _get(sa, 'attack')  + w['OFF_MID_W'] * _get(sa, 'midfield'))
    off_b = bb * (w['OFF_ATT_W'] * _get(sb, 'attack')  + w['OFF_MID_W'] * _get(sb, 'midfield'))
    res_a = max(db * (w['RES_DEF_W'] * _get(sa, 'defense') + w['RES_GK_W'] * _get(sa, 'goalkeeper') + w['RES_MID_W'] * _get(sa, 'midfield')), RES_FLOOR)
    res_b = max(eb * (w['RES_DEF_W'] * _get(sb, 'defense') + w['RES_GK_W'] * _get(sb, 'goalkeeper') + w['RES_MID_W'] * _get(sb, 'midfield')), RES_FLOOR)
    return (
        min(w['BASE_XG'] * off_a / res_b, MAX_XG_VAL),
        min(w['BASE_XG'] * off_b / res_a, MAX_XG_VAL),
    )


def score_dist(xg_a, xg_b):
    entries = []
    for ga in range(MAX_GOALS + 1):
        for gb in range(MAX_GOALS + 1):
            p = sp_poisson.pmf(ga, xg_a) * sp_poisson.pmf(gb, xg_b)
            entries.append((p, ga, gb))
    entries.sort(reverse=True)
    return entries


def find_rank(entries, ga_real, gb_real):
    for rank, (p, ga, gb) in enumerate(entries, 1):
        if ga == ga_real and gb == gb_real:
            return rank, p
    return len(entries) + 1, 0.0


def rank_score(rank, prob):
    if rank == 1:    return 10
    if rank == 2:    return 6
    if rank == 3:    return 3
    if rank <= 5:    return 1
    if prob >= 0.05: return 0
    if prob >= 0.02: return -2
    return -5


def result_probs(xg_a, xg_b):
    pa = np.array([sp_poisson.pmf(k, xg_a) for k in range(MAX_GOALS + 1)])
    pb = np.array([sp_poisson.pmf(k, xg_b) for k in range(MAX_GOALS + 1)])
    m   = np.outer(pa, pb)
    w_a  = float(np.tril(m, -1).sum())
    draw = float(np.trace(m))
    w_b  = float(np.triu(m, 1).sum())
    s    = w_a + draw + w_b
    return w_a / s, draw / s, w_b / s


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Carregamento de estratégia e dados
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def load_strategy(s):
    if 'weights' in s:
        return dict(s['weights']), dict(s.get('biases', {}))

    fpath = os.path.join(ROOT, s['file'])
    if not os.path.exists(fpath):
        raise FileNotFoundError(fpath)

    with open(fpath) as f:
        data = json.load(f)

    weights = dict(data['weights'])
    biases  = data.get('biases', {})

    if s.get('no_biases'):
        biases = {}

    if s.get('base_xg_factor'):
        weights['BASE_XG'] = round(weights['BASE_XG'] * s['base_xg_factor'], 4)

    return weights, biases


def load_matches():
    with open(STATE_FILE) as f:
        state = json.load(f)

    matches = []
    for grp, games in state.get('group_results', {}).items():
        for key, score in games.items():
            ta, tb = key.split('|')
            ga, gb = score
            matches.append({'phase': f'Grupo {grp}', 'team_a': ta, 'team_b': tb,
                            'goals_a': ga, 'goals_b': gb})

    for key, score in state.get('knockout_results', {}).items():
        ta, tb = key.split('|')
        ga, gb = score
        matches.append({'phase': 'Mata-mata', 'team_a': ta, 'team_b': tb,
                        'goals_a': ga, 'goals_b': gb})
    return matches


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Avaliação
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def evaluate(weights, biases, matches, team_scores):
    n            = len(matches)
    total_rs     = 0
    ranks        = []
    score_probs  = []
    result_ok    = 0
    result_p     = []
    nll          = 0.0
    xg_sum       = 0.0

    for m in matches:
        ta, tb        = m['team_a'], m['team_b']
        ga_real, gb_real = m['goals_a'], m['goals_b']

        xg_a, xg_b = compute_xg(weights, biases, ta, tb, team_scores)
        xg_sum += xg_a + xg_b

        entries      = score_dist(xg_a, xg_b)
        rank, prob   = find_rank(entries, ga_real, gb_real)
        total_rs    += rank_score(rank, prob)
        ranks.append(rank)
        score_probs.append(prob)

        pw_a, pd, pw_b = result_probs(xg_a, xg_b)
        if ga_real > gb_real:
            result_ok += 1 if (pw_a > pd and pw_a > pw_b) else 0
            result_p.append(pw_a)
        elif gb_real > ga_real:
            result_ok += 1 if (pw_b > pd and pw_b > pw_a) else 0
            result_p.append(pw_b)
        else:
            result_ok += 1 if (pd > pw_a and pd > pw_b) else 0
            result_p.append(pd)

        nll += xg_a - ga_real * math.log(max(xg_a, 1e-9))
        nll += xg_b - gb_real * math.log(max(xg_b, 1e-9))

    return {
        'rank_score':  total_rs,
        'top1':        sum(1 for r in ranks if r == 1),
        'top3':        sum(1 for r in ranks if r <= 3),
        'top5':        sum(1 for r in ranks if r <= 5),
        'penalties':   sum(1 for i, r in enumerate(ranks) if r > 5 and score_probs[i] < 0.05),
        'result_ok':   result_ok,
        'result_pct':  result_ok / n * 100,
        'avg_p_result': sum(result_p) / n * 100,
        'avg_p_score': sum(score_probs) / n * 100,
        'avg_rank':    sum(ranks) / n,
        'avg_xg':      xg_sum / (2 * n),
        'nll':         nll,
        'n':           n,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Saída
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_table(results):
    if not results:
        return "  Nenhum modelo disponível."

    results_sorted = sorted(results, key=lambda x: -x['metrics']['rank_score'])
    n = results_sorted[0]['metrics']['n']

    hdr = (
        f"  {'ID':<5} {'Modelo':<30} {'RankScore':>10} {'Top1':>5} {'Top3':>5} "
        f"{'Top5':>5} {'Pnlt':>5} {'Res%':>6} {'AvgP%':>6} {'AvgRank':>8} "
        f"{'AvgXG':>7} {'NLL':>8}"
    )
    sep = "  " + "─" * (len(hdr) - 2)

    lines = [
        f"\n  Comparação de Modelos — {n} jogos",
        sep, hdr, sep,
    ]

    for i, r in enumerate(results_sorted):
        m    = r['metrics']
        star = " ★" if i == 0 else ""
        lines.append(
            f"  {r['id']:<5} {r['name']:<30} "
            f"{m['rank_score']:>+10d} "
            f"{m['top1']:>5} {m['top3']:>5} {m['top5']:>5} "
            f"{m['penalties']:>5} "
            f"{m['result_pct']:>5.1f}% "
            f"{m['avg_p_result']:>5.1f}% "
            f"{m['avg_rank']:>8.1f} "
            f"{m['avg_xg']:>7.3f} "
            f"{m['nll']:>8.2f}"
            f"{star}"
        )

    lines.append(sep)
    lines.append(
        "\n  Legenda:\n"
        "    RankScore  = pontos totais (rank do placar real na distribuição Poisson)\n"
        "    Top1/3/5   = nº de jogos onde o placar real estava no rank 1/top3/top5\n"
        "    Pnlt       = nº de jogos com penalidade (rank>5 e P<5%)\n"
        "    Res%       = acerto W/D/L  |  AvgP% = prob média do resultado correto\n"
        "    AvgRank    = rank médio do placar real  |  AvgXG = xG médio por time\n"
        "    NLL        = Poisson NLL (menor = melhor fit)"
    )

    return "\n".join(lines)


def print_verbose(sid, weights, biases, matches, team_scores):
    print(f"\n  Breakdown por jogo — {sid}\n")
    hdr = f"  {'Jogo':<34} {'GA':>3}{'GB':>3}  {'xGA':>5} {'xGB':>5}  {'Rank':>5} {'P%':>6}  {'Score':>6}  Top-3 prováveis"
    print(hdr)
    print("  " + "─" * (len(hdr) - 2))
    for m in matches:
        ta, tb   = m['team_a'], m['team_b']
        ga, gb   = m['goals_a'], m['goals_b']
        xg_a, xg_b = compute_xg(weights, biases, ta, tb, team_scores)
        entries  = score_dist(xg_a, xg_b)
        rank, prob = find_rank(entries, ga, gb)
        rs       = rank_score(rank, prob)
        top3     = "  ".join(f"{g}–{h}({p*100:.1f}%)" for p, g, h in entries[:3])
        label    = f"{ta[:15]} vs {tb[:15]}"
        flag     = " ◄" if rs < 0 else (" ★" if rank == 1 else "")
        print(f"  {label:<34} {ga:>3}{gb:>3}  {xg_a:>5.2f} {xg_b:>5.2f}  "
              f"{rank:>5} {prob*100:>5.1f}%  {rs:>+6}  {top3}{flag}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--calibrate', action='store_true',
                        help='Roda calibrações pendentes (S08–S18) antes de avaliar')
    parser.add_argument('--save', action='store_true',
                        help='Salva resultado em output/model_comparison.md')
    parser.add_argument('--verbose', metavar='ID',
                        help='Mostra breakdown jogo a jogo para o ID especificado (ex: S01)')
    args = parser.parse_args()

    if not os.path.exists(SCORES_FILE):
        sys.exit(f"Erro: {SCORES_FILE} não encontrado — rode scripts/build_team_scores.py primeiro.")
    if not os.path.exists(STATE_FILE):
        sys.exit(f"Erro: {STATE_FILE} não encontrado.")

    with open(SCORES_FILE) as f:
        team_scores = json.load(f)

    matches = load_matches()
    matches = [m for m in matches if m['team_a'] in team_scores and m['team_b'] in team_scores]
    print(f"\n  {len(matches)} jogos carregados de copa_real_state.json\n")

    results = []
    pending = []

    for s in STRATEGIES:
        try:
            weights, biases = load_strategy(s)
        except FileNotFoundError:
            if 'calibrate_cmd' in s and args.calibrate:
                cmd = s['calibrate_cmd'].replace('python scripts/', f'{sys.executable} scripts/', 1)
                print(f"  [{s['id']}] Calibrando: {cmd}")
                ret = subprocess.run(cmd, shell=True, cwd=ROOT)
                if ret.returncode != 0:
                    print(f"  [{s['id']}] ERRO na calibração — pulando\n")
                    pending.append(s)
                    continue
                try:
                    weights, biases = load_strategy(s)
                except FileNotFoundError:
                    pending.append(s)
                    continue
            else:
                pending.append(s)
                continue

        metrics = evaluate(weights, biases, matches, team_scores)
        results.append({'id': s['id'], 'name': s['name'], 'desc': s['desc'], 'metrics': metrics})
        print(
            f"  [{s['id']}] {s['name']:<33}  "
            f"RankScore={metrics['rank_score']:+4d}  "
            f"Top1={metrics['top1']:2d}  Top3={metrics['top3']:2d}  "
            f"Res={metrics['result_pct']:.0f}%  "
            f"AvgXG={metrics['avg_xg']:.3f}"
        )

    table = build_table(results)
    print(table)

    if args.save:
        out_path = os.path.join(ROOT, 'output', 'model_comparison.md')
        with open(out_path, 'w') as f:
            f.write("# Comparação de Modelos — Copa do Mundo 2026\n\n")
            f.write(f"Avaliação sobre {len(matches)} jogos reais\n\n")
            f.write("```\n")
            f.write(table)
            f.write("\n```\n")
        print(f"\n  Salvo em {out_path}")

    if pending:
        print(f"\n  {'─'*60}")
        print(f"  Pendentes (arquivo não encontrado):\n")
        for s in pending:
            print(f"  [{s['id']}] {s['name']}")
            if 'calibrate_cmd' in s:
                print(f"         {s['calibrate_cmd']}")
        print(f"\n  Use --calibrate para rodar automaticamente.")

    if args.verbose:
        vid = args.verbose.upper()
        target = next((s for s in STRATEGIES if s['id'] == vid), None)
        if target is None:
            print(f"\n  ID '{vid}' não encontrado. IDs disponíveis: {[s['id'] for s in STRATEGIES]}")
        else:
            try:
                weights, biases = load_strategy(target)
                print_verbose(vid, weights, biases, matches, team_scores)
            except FileNotFoundError as e:
                print(f"\n  Arquivo não encontrado para {vid}: {e}")


if __name__ == '__main__':
    main()
