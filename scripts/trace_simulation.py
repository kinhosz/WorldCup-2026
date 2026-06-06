#!/usr/bin/env python3
"""
Run single-tournament traces with full bracket output.
Used to generate example simulations for documentation.

Usage:
    python scripts/trace_simulation.py [--champion TEAM] [--dark-horse]
    python scripts/trace_simulation.py                     # random
    python scripts/trace_simulation.py --champion brazil
    python scripts/trace_simulation.py --champion france
    python scripts/trace_simulation.py --dark-horse
"""

import json
import os
import random
import sys
from collections import defaultdict
from itertools import combinations

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

# ── paste constants/helpers from simulate.py ─────────────────────────────────

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

ROUND32 = [
    (73,  ('2', 'A'),   ('2', 'B')),
    (74,  ('1', 'E'),   ('3rd', 'ABCDF')),
    (75,  ('1', 'F'),   ('2', 'C')),
    (76,  ('1', 'C'),   ('2', 'F')),
    (77,  ('1', 'I'),   ('3rd', 'CDFGH')),
    (78,  ('2', 'E'),   ('2', 'I')),
    (79,  ('1', 'A'),   ('3rd', 'CEFHI')),
    (80,  ('1', 'L'),   ('3rd', 'EHIJK')),
    (81,  ('1', 'D'),   ('3rd', 'BEFIJ')),
    (82,  ('1', 'G'),   ('3rd', 'AEHIJ')),
    (83,  ('2', 'K'),   ('2', 'L')),
    (84,  ('1', 'H'),   ('2', 'J')),
    (85,  ('1', 'B'),   ('3rd', 'EFGIJ')),
    (86,  ('1', 'J'),   ('2', 'H')),
    (87,  ('1', 'K'),   ('3rd', 'DEIJL')),
    (88,  ('2', 'D'),   ('2', 'G')),
]

ROUND16 = [
    (89,  74, 77),
    (90,  73, 75),
    (91,  76, 78),
    (92,  79, 80),
    (93,  83, 84),
    (94,  81, 82),
    (95,  86, 88),
    (96,  85, 87),
]

QUARTERFINALS = [
    (97,   89, 90),
    (98,   93, 94),
    (99,   91, 92),
    (100,  95, 96),
]

SEMIFINALS = [
    (101,  97,  98),
    (102,  99, 100),
]

FINAL_ID = 104

THIRD_PLACE_SLOTS = {
    74: set('ABCDF'),
    77: set('CDFGH'),
    79: set('CEFHI'),
    80: set('EHIJK'),
    81: set('BEFIJ'),
    82: set('AEHIJ'),
    85: set('EFGIJ'),
    87: set('DEIJL'),
}

BASE_XG = 1.3
FALLBACK_SCORE = 0.5
ET_FACTOR = 0.35
RES_FLOOR = 0.10
MAX_XG = 8.0

# Top-8 "famous" teams — used to detect dark-horse wins
FAMOUS = {'france', 'portugal', 'argentina', 'brazil',
          'netherlands', 'england', 'belgium', 'spain', 'germany'}

DISPLAY_NAMES = {
    'united_states_of_america': 'USA',
    'republic_of_korea':        'South Korea',
    'bosnia_and_herzegovina':   'Bosnia-Herzegovina',
    'cape_verte':               'Cape Verde',
    'ivory_coast':              "Côte d'Ivoire",
    'ira':                      'Iran',
    'new_zealand':              'New Zealand',
    'saudi_arabia':             'Saudi Arabia',
    'south_africa':             'South Africa',
    'czech_republic':           'Czech Republic',
}

_GROUP_OF = {team: g for g, teams in GROUPS.items() for team in teams}


def _name(team):
    return DISPLAY_NAMES.get(team, team.replace('_', ' ').title())


def _get(scores, key):
    v = scores.get(key)
    return v if v is not None else FALLBACK_SCORE


def compute_xg(s_a, s_b):
    off_a = 0.7 * _get(s_a, 'attack')  + 0.3 * _get(s_a, 'midfield')
    off_b = 0.7 * _get(s_b, 'attack')  + 0.3 * _get(s_b, 'midfield')
    res_a = max(0.6 * _get(s_a, 'defense') + 0.2 * _get(s_a, 'goalkeeper') + 0.2 * _get(s_a, 'midfield'), RES_FLOOR)
    res_b = max(0.6 * _get(s_b, 'defense') + 0.2 * _get(s_b, 'goalkeeper') + 0.2 * _get(s_b, 'midfield'), RES_FLOOR)
    return min(BASE_XG * off_a / res_b, MAX_XG), min(BASE_XG * off_b / res_a, MAX_XG)


def sim_group_match(ta, tb, scores):
    xg_a, xg_b = compute_xg(scores[ta], scores[tb])
    return int(np.random.poisson(xg_a)), int(np.random.poisson(xg_b))


def sim_knockout_match_traced(ta, tb, scores):
    """Returns (winner, loser, score_str, note). Score is always home–away."""
    xg_a, xg_b = compute_xg(scores[ta], scores[tb])
    ga = int(np.random.poisson(xg_a))
    gb = int(np.random.poisson(xg_b))

    if ga != gb:
        w, l = (ta, tb) if ga > gb else (tb, ta)
        return w, l, f"{ga}–{gb}", "90'"

    et_a = int(np.random.poisson(xg_a * ET_FACTOR))
    et_b = int(np.random.poisson(xg_b * ET_FACTOR))
    if et_a != et_b:
        w, l = (ta, tb) if et_a > et_b else (tb, ta)
        return w, l, f"{ga+et_a}–{gb+et_b} ({ga}–{gb} AET)", "AET"

    winner = ta if random.random() < 0.5 else tb
    loser = tb if winner == ta else ta
    return winner, loser, f"{ga}–{gb} pen.", "PEN"


def simulate_group(teams, scores):
    stats = {t: {'pts': 0, 'gd': 0, 'gf': 0, 'wins': 0} for t in teams}
    matches = []

    for ta, tb in combinations(teams, 2):
        ga, gb = sim_group_match(ta, tb, scores)
        matches.append((ta, tb, ga, gb))
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

    ranked = sorted(
        teams,
        key=lambda t: (-stats[t]['pts'], -stats[t]['gd'], -stats[t]['gf'],
                       -stats[t]['wins'], random.random()),
    )
    return [(t, stats[t]['pts'], stats[t]['gd'], stats[t]['gf'], stats[t]['wins'])
            for t in ranked], matches, stats


def _rank_thirds(thirds):
    return sorted(thirds, key=lambda x: (-x[2], -x[3], -x[4], -x[5], random.random()))


def _assign_thirds(qualifying):
    slots = list(THIRD_PLACE_SLOTS.keys())
    assign = {}
    used = [False] * len(qualifying)

    def bt(slot_idx):
        if slot_idx == len(slots):
            return True
        slot = slots[slot_idx]
        eligible = THIRD_PLACE_SLOTS[slot]
        for i, (group, team) in enumerate(qualifying):
            if not used[i] and group in eligible:
                assign[slot] = team
                used[i] = True
                if bt(slot_idx + 1):
                    return True
                del assign[slot]
                used[i] = False
        return False

    if bt(0):
        return assign
    shuffled = list(qualifying)
    random.shuffle(shuffled)
    return {slot: shuffled[i][1] for i, slot in enumerate(slots)}


def simulate_tournament_traced(scores):
    group_data = {}
    thirds = []

    for letter, teams in GROUPS.items():
        ranked, matches, stats = simulate_group(teams, scores)
        group_data[letter] = {'ranked': ranked, 'matches': matches, 'stats': stats}
        _, *third = ranked[2]
        thirds.append((letter, ranked[2][0], *third))

    ranked_thirds = _rank_thirds(thirds)
    qualifying_thirds = [(g, t) for g, t, *_ in ranked_thirds[:8]]
    third_slot_map = _assign_thirds(qualifying_thirds)

    match_teams = {}
    group_rankings = {l: d['ranked'] for l, d in group_data.items()}

    for mid, spec1, spec2 in ROUND32:
        def resolve(spec, mid=mid):
            kind, val = spec
            if kind == '1':
                return group_rankings[val][0][0]
            if kind == '2':
                return group_rankings[val][1][0]
            return third_slot_map.get(mid)
        match_teams[mid] = (resolve(spec1), resolve(spec2))

    winners = {}
    match_details = {}

    def play(mid):
        ta, tb = match_teams[mid]
        w, l, score_str, note = sim_knockout_match_traced(ta, tb, scores)
        winners[mid] = w
        match_details[mid] = {'home': ta, 'away': tb, 'score': score_str,
                               'winner': w, 'loser': l, 'note': note}
        return w

    for mid, _, _ in ROUND32:
        play(mid)
    for mid, src1, src2 in ROUND16:
        match_teams[mid] = (winners[src1], winners[src2])
        play(mid)
    for mid, src1, src2 in QUARTERFINALS:
        match_teams[mid] = (winners[src1], winners[src2])
        play(mid)
    for mid, src1, src2 in SEMIFINALS:
        match_teams[mid] = (winners[src1], winners[src2])
        play(mid)
    match_teams[FINAL_ID] = (winners[SEMIFINALS[0][0]], winners[SEMIFINALS[1][0]])
    champion = play(FINAL_ID)

    return {
        'champion': champion,
        'group_data': group_data,
        'group_rankings': {l: [t for t, *_ in r['ranked']] for l, r in group_data.items()},
        'qualifying_thirds': qualifying_thirds,
        'match_details': match_details,
        'match_teams': match_teams,
        'winners': winners,
    }


def format_trace(result, scores):
    lines = []
    nl = lines.append

    nl("### FASE DE GRUPOS")
    nl("")
    for letter in sorted(result['group_data'].keys()):
        gd = result['group_data'][letter]
        nl(f"**Grupo {letter}**")
        nl("")
        nl("| # | Seleção | Pts | GD | GP |")
        nl("|---|---------|-----|----|----|")
        for pos, (team, pts, gd_v, gf, wins) in enumerate(gd['ranked'], 1):
            adv = "→ R32" if pos <= 2 else ("→ R32 (3°)" if pos == 3 else "✗")
            nl(f"| {pos} | {_name(team)} | {pts} | {gd_v:+d} | {gf} | {adv}")
        nl("")
        nl("Jogos:")
        for ta, tb, ga, gb in gd['matches']:
            nl(f"- {_name(ta)} {ga}–{gb} {_name(tb)}")
        nl("")

    thirds_shown = result['qualifying_thirds']
    nl("**8 melhores 3ºs lugares classificados:**")
    for g, t in thirds_shown:
        nl(f"- {_name(t)} (Grupo {g})")
    nl("")

    def fmt_ko_round(ids, title):
        nl(f"### {title}")
        nl("")
        nl("| Jogo | Mandante | Placar | Visitante | Obs |")
        nl("|------|----------|--------|-----------|-----|")
        for mid in ids:
            d = result['match_details'][mid]
            w_marker_h = "**" if d['winner'] == d['home'] else ""
            w_marker_a = "**" if d['winner'] == d['away'] else ""
            nl(f"| M{mid} | {w_marker_h}{_name(d['home'])}{w_marker_h} | {d['score']} | {w_marker_a}{_name(d['away'])}{w_marker_a} | {d['note']} |")
        nl("")

    fmt_ko_round([m for m, *_ in ROUND32], "OITAVAS DE FINAL (Round of 32)")
    fmt_ko_round([m for m, *_ in ROUND16], "ROUND OF 16")
    fmt_ko_round([m for m, *_ in QUARTERFINALS], "QUARTAS DE FINAL")
    fmt_ko_round([m for m, *_ in SEMIFINALS], "SEMIFINAIS")

    fin = result['match_details'][FINAL_ID]
    nl("### FINAL")
    nl("")
    nl(f"**{_name(fin['home'])}** {fin['score']} **{_name(fin['away'])}**")
    nl("")
    champion = result['champion']
    nl(f"🏆 **CAMPEÃO: {_name(champion).upper()}**")
    nl("")

    return "\n".join(lines)


def run_until(scores, condition, max_tries=50000):
    for i in range(max_tries):
        result = simulate_tournament_traced(scores)
        if condition(result['champion']):
            print(f"  (found after {i+1} tries)", file=sys.stderr)
            return result
    print(f"  WARNING: condition not met after {max_tries} tries", file=sys.stderr)
    return simulate_tournament_traced(scores)


def main():
    scores_path = "output/team_scores.json"
    with open(scores_path, encoding='utf-8') as f:
        scores = json.load(f)

    mode = 'random'
    target = None
    if '--champion' in sys.argv:
        idx = sys.argv.index('--champion')
        target = sys.argv[idx + 1]
        mode = 'champion'
    elif '--dark-horse' in sys.argv:
        mode = 'dark-horse'

    if mode == 'random':
        print("Simulação aleatória...", file=sys.stderr)
        result = simulate_tournament_traced(scores)
    elif mode == 'champion':
        print(f"Procurando simulação onde {target} ganha...", file=sys.stderr)
        result = run_until(scores, lambda c: c == target)
    elif mode == 'dark-horse':
        print("Procurando simulação com azarão campeão...", file=sys.stderr)
        result = run_until(scores, lambda c: c not in FAMOUS)

    print(format_trace(result, scores))


if __name__ == '__main__':
    main()
