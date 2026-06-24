#!/usr/bin/env python3
"""
group_projection.py — simula os jogos restantes de cada grupo (R2 + R3)
partindo dos resultados reais da R1 como ponto de partida fixo.

Saída: output/group_projection.json com P(1º/2º/3º/4º) por time
e ranking de 3ºs colocados por pts/GD médios simulados.

Uso: python3 scripts/group_projection.py [N]
     N: número de simulações (default 50000)
"""

import json
import os
import random
import sys
from collections import defaultdict

import numpy as np

ROOT     = os.path.join(os.path.dirname(__file__), '..')
SCORES_F = os.path.join(ROOT, 'output', 'team_scores.json')
STATE_F  = os.path.join(ROOT, 'output', 'copa_real_state.json')
SA_F     = os.path.join(ROOT, 'output', 'calibrated_weights_sa.json')
OUT_F    = os.path.join(ROOT, 'output', 'group_projection.json')

with open(SCORES_F) as f: SCORES = json.load(f)
with open(STATE_F)  as f: STATE  = json.load(f)
with open(SA_F)     as f: SA     = json.load(f)

W          = SA['weights']
BASE_XG    = W['BASE_XG']
OFF_ATT_W  = W['OFF_ATT_W']
OFF_MID_W  = W['OFF_MID_W']
RES_DEF_W  = W['RES_DEF_W']
RES_GK_W   = W['RES_GK_W']
RES_MID_W  = W['RES_MID_W']
BIASES     = SA.get('biases', {})
FALLBACK   = 0.5
RES_FLOOR  = 0.10
MAX_XG     = 8.0

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

# R1=(0,1)(2,3)  R2=(0,2)(1,3)  R3=(0,3)(1,2)  — índices na lista do grupo
R2_PAIRS = [(0, 2), (1, 3)]
R3_PAIRS = [(0, 3), (1, 2)]


def _get(s, key):
    v = s.get(key)
    return v if v is not None else FALLBACK


def compute_xg(ta, tb):
    s_a, s_b = SCORES.get(ta, {}), SCORES.get(tb, {})
    ab = BIASES.get(ta, {}).get('att_bias', 1.0)
    bb = BIASES.get(tb, {}).get('att_bias', 1.0)
    db = BIASES.get(ta, {}).get('def_bias', 1.0)
    eb = BIASES.get(tb, {}).get('def_bias', 1.0)
    off_a = ab * (OFF_ATT_W * _get(s_a, 'attack') + OFF_MID_W * _get(s_a, 'midfield'))
    off_b = bb * (OFF_ATT_W * _get(s_b, 'attack') + OFF_MID_W * _get(s_b, 'midfield'))
    res_a = max(db * (RES_DEF_W*_get(s_a,'defense') + RES_GK_W*_get(s_a,'goalkeeper') + RES_MID_W*_get(s_a,'midfield')), RES_FLOOR)
    res_b = max(eb * (RES_DEF_W*_get(s_b,'defense') + RES_GK_W*_get(s_b,'goalkeeper') + RES_MID_W*_get(s_b,'midfield')), RES_FLOOR)
    return min(BASE_XG * off_a / res_b, MAX_XG), min(BASE_XG * off_b / res_a, MAX_XG)


def sim_game(ta, tb):
    xg_a, xg_b = compute_xg(ta, tb)
    return int(np.random.poisson(xg_a)), int(np.random.poisson(xg_b))


def _h2h_key(team, tied_teams, match_results):
    """Head-to-head sub-table for `team` among `tied_teams`."""
    pts = gd = gf = 0
    for opp in tied_teams:
        if opp == team:
            continue
        key  = f"{team}|{opp}"
        rkey = f"{opp}|{team}"
        if key in match_results:
            ga, gb = match_results[key]
        elif rkey in match_results:
            gb, ga = match_results[rkey]
        else:
            continue
        gf += ga
        gd += ga - gb
        if ga > gb:
            pts += 3
        elif ga == gb:
            pts += 1
    return (-pts, -gd, -gf)


def rank_group(teams, stats, match_results=None):
    """Tiebreaker FIFA 2026: pts → H2H pts → H2H GD → H2H GF → GD → GF → wins → random."""
    pts_groups = {}
    for t in teams:
        pts_groups.setdefault(stats[t]['pts'], []).append(t)

    def sort_key(t):
        tied = pts_groups[stats[t]['pts']]
        if len(tied) > 1 and match_results:
            h2h = _h2h_key(t, tied, match_results)
        else:
            h2h = (0, 0, 0)
        return (
            -stats[t]['pts'],
            h2h[0], h2h[1], h2h[2],
            -stats[t]['gd'],
            -stats[t]['gf'],
            -stats[t]['wins'],
            random.random(),
        )

    return sorted(teams, key=sort_key)


def simulate_group_once(group_letter, teams):
    """Simula jogos pendentes do grupo usando resultados reais quando disponíveis.
    Respeita R1 e R2 reais; simula apenas os jogos ainda não disputados."""
    real_group = STATE.get('group_results', {}).get(group_letter, {})
    stats = {t: {'pts': 0, 'gd': 0, 'gf': 0, 'wins': 0} for t in teams}
    match_results = {}

    all_pairs = [(teams[0], teams[1]), (teams[2], teams[3]),   # R1
                 (teams[0], teams[2]), (teams[1], teams[3]),   # R2
                 (teams[0], teams[3]), (teams[1], teams[2])]   # R3

    for ta, tb in all_pairs:
        key_ab = f"{ta}|{tb}"
        key_ba = f"{tb}|{ta}"
        if key_ab in real_group:
            ga, gb = real_group[key_ab]
        elif key_ba in real_group:
            gb, ga = real_group[key_ba]
        else:
            ga, gb = sim_game(ta, tb)

        match_results[f"{ta}|{tb}"] = (ga, gb)
        stats[ta]['gf'] += ga
        stats[tb]['gf'] += gb
        stats[ta]['gd'] += ga - gb
        stats[tb]['gd'] += gb - ga
        if ga > gb:
            stats[ta]['pts'] += 3
            stats[ta]['wins'] += 1
        elif gb > ga:
            stats[tb]['pts'] += 3
            stats[tb]['wins'] += 1
        else:
            stats[ta]['pts'] += 1
            stats[tb]['pts'] += 1

    ranked = rank_group(teams, stats, match_results)
    return [(ranked[pos], pos + 1, stats[ranked[pos]]['pts'],
             stats[ranked[pos]]['gd'], stats[ranked[pos]]['gf'])
            for pos in range(4)]


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000
    print(f"Rodando {N:,} simulações de grupo...")

    # pos_count[group][team][pos] = contagem (pos 1-4)
    pos_count  = {g: {t: [0]*4 for t in teams} for g, teams in GROUPS.items()}
    # Para 3ºs: acumular pts e gd por (group, team) quando terminam em 3º
    third_pts  = defaultdict(list)  # (group, team) → [pts_totais, ...]
    third_gd   = defaultdict(list)
    third_gf   = defaultdict(list)

    for sim_i in range(N):
        if sim_i % 10_000 == 0 and sim_i > 0:
            print(f"  {sim_i:,}/{N:,}...")

        for g, teams in GROUPS.items():
            result = simulate_group_once(g, teams)
            for team, pos, pts, gd, gf in result:
                pos_count[g][team][pos - 1] += 1
                if pos == 3:
                    third_pts[(g, team)].append(pts)
                    third_gd[(g, team)].append(gd)
                    third_gf[(g, team)].append(gf)

    # Monta output por grupo
    output = {}
    for g, teams in GROUPS.items():
        group_data = []
        for t in teams:
            counts = pos_count[g][t]
            group_data.append({
                'team': t,
                'p1': round(counts[0] / N * 100, 1),
                'p2': round(counts[1] / N * 100, 1),
                'p3': round(counts[2] / N * 100, 1),
                'p4': round(counts[3] / N * 100, 1),
                'p_advance': round((counts[0] + counts[1]) / N * 100, 1),
            })
        # Ordena por p1 desc
        group_data.sort(key=lambda x: -x['p1'])
        output[g] = group_data

    # 3ºs colocados: para cada (group, team) que já apareceu em 3º,
    # calcula média de pts/gd/gf quando termina em 3º
    thirds_summary = []
    for g, teams in GROUPS.items():
        for t in teams:
            key = (g, t)
            if third_pts[key]:
                n3 = len(third_pts[key])
                avg_pts = sum(third_pts[key]) / n3
                avg_gd  = sum(third_gd[key])  / n3
                avg_gf  = sum(third_gf[key])  / n3
                p3      = n3 / N * 100
                thirds_summary.append({
                    'group': g,
                    'team': t,
                    'p3': round(p3, 1),
                    'avg_pts': round(avg_pts, 2),
                    'avg_gd':  round(avg_gd,  2),
                    'avg_gf':  round(avg_gf,  2),
                })

    # Ordena 3ºs por avg_pts desc, depois avg_gd
    thirds_summary.sort(key=lambda x: (-x['avg_pts'], -x['avg_gd'], -x['avg_gf']))

    output['thirds_ranking'] = thirds_summary

    with open(OUT_F, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSalvo em {OUT_F}")
    print("\n=== TOP 12 TERCEIROS COLOCADOS (por avg_pts) ===")
    print(f"{'Grupo':>6} {'Time':30} {'P(3º)':>6} {'avg_pts':>8} {'avg_GD':>7} {'avg_GF':>7}")
    for row in thirds_summary[:12]:
        print(f"  {row['group']:>4}  {row['team']:30} {row['p3']:>5.1f}%  {row['avg_pts']:>7.2f}  {row['avg_gd']:>6.2f}  {row['avg_gf']:>6.2f}")

    print("\n=== POSIÇÕES FINAIS POR GRUPO ===")
    for g in sorted(GROUPS.keys()):
        print(f"\nGrupo {g}:")
        print(f"  {'Time':30} {'P1':>6} {'P2':>6} {'P3':>6} {'P4':>6} {'P_adv':>6}")
        for row in output[g]:
            print(f"  {row['team']:30} {row['p1']:>5.1f}% {row['p2']:>5.1f}% {row['p3']:>5.1f}% {row['p4']:>5.1f}%  {row['p_advance']:>5.1f}%")


if __name__ == '__main__':
    main()
