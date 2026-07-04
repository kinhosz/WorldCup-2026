#!/usr/bin/env python3
"""
Monte Carlo simulation of the 2026 FIFA World Cup.

Uses Poisson-distributed goals derived from sector-weighted xG scores
(output/team_scores.json) to simulate the full 48-team tournament:
  - Group stage (round-robin, 12 groups)
  - Best-8 third-place selection
  - Round of 32 → R16 → QF → SF → Final (official 2026 bracket)

Usage:
    python scripts/simulate.py [N_SIMULATIONS]
    python scripts/simulate.py 50000

Default: 10,000 simulations.
Results are printed to stdout and saved to output/simulation_results.json.
"""

import json
import os
import random
import sys
import time
from collections import defaultdict
from itertools import combinations

import numpy as np


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Tournament structure — official 2026 FIFA World Cup draw
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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

# Round of 32 matchups — official FIFA bracket (matches 73–88).
# spec tuple: ('1'/'2', group_letter) or ('3rd', eligible_groups_string)
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

# Each entry: (match_id, source_match_1, source_match_2)
# Pareamento sequencial oficial (ver output/r32_bracket.json → r16_pairs):
# 73&74, 75&76, 77&78, 79&80, 81&82, 83&84, 85&86, 87&88.
# Mantido para compatibilidade (megazord.py) — simulate_tournament() usa
# REAL_R16_BRACKET abaixo, que trava os times reais em vez de resolver
# pelos specs de grupo do ROUND32 (dessincronizados dos resultados reais).
ROUND16 = [
    (89,  73, 74),
    (90,  75, 76),
    (91,  77, 78),
    (92,  79, 80),
    (93,  81, 82),
    (94,  83, 84),
    (95,  85, 86),
    (96,  87, 88),
]

# Oitavas (R16) — bracket real fixo, confirmado com os 16 resultados do R32.
REAL_R16_BRACKET = {
    89: ('canada',      'morocco'),
    90: ('paraguay',    'france'),
    91: ('belgium',     'united_states_of_america'),
    92: ('spain',       'portugal'),
    93: ('brazil',      'norway'),
    94: ('mexico',      'england'),
    95: ('switzerland', 'colombia'),
    96: ('egypt',       'argentina'),
}

QUARTERFINALS = [
    (97,   89, 90),
    (98,   93, 94),
    (99,   91, 92),
    (100,  95, 96),
]

SEMIFINALS = [
    (101,  97,  99),
    (102,  98, 100),
]

FINAL_ID   = 104
THIRD_PLACE_ID = 103

# match_id → set of eligible group letters for 3rd-place slot
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

FALLBACK_SCORE = 0.5
ET_FACTOR     = 0.35   # extra time: 30 min ≈ 35% of 90-min xG
RES_FLOOR = 0.10
MAX_XG    = 8.0

# ── Pesos e biases calibrados (SA+biases, R1 com outliers) ───────────
_SA_FILE = os.path.join(os.path.dirname(__file__), '..', 'output', 'calibrated_weights_sa.json')
with open(_SA_FILE) as _f:
    _SA = json.load(_f)

# ── Resultados reais já jogados ───────────────────────────────────────
_STATE_FILE = os.path.join(os.path.dirname(__file__), '..', 'output', 'copa_real_state.json')
_REAL_GROUP_RESULTS = {}
_REAL_KNOCKOUT_RESULTS = {}
if os.path.exists(_STATE_FILE):
    with open(_STATE_FILE) as _f:
        _real_state = json.load(_f)
        _REAL_GROUP_RESULTS = _real_state.get('group_results', {})
        _REAL_KNOCKOUT_RESULTS = _real_state.get('knockout_results', {})

_W = _SA['weights']
BASE_XG    = _W['BASE_XG']
OFF_ATT_W  = _W['OFF_ATT_W']
OFF_MID_W  = _W['OFF_MID_W']
RES_DEF_W  = _W['RES_DEF_W']
RES_GK_W   = _W['RES_GK_W']
RES_MID_W  = _W['RES_MID_W']
TEAM_BIASES = _SA.get('biases', {})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  xG formula  (mirrors build_team_scores.py)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _get(scores, key):
    v = scores.get(key)
    return v if v is not None else FALLBACK_SCORE


def compute_xg(s_a, s_b, ta=None, tb=None):
    """Return (xG_A, xG_B) applying team biases when team keys are provided."""
    ab = TEAM_BIASES.get(ta, {}).get('att_bias', 1.0) if ta else 1.0
    bb = TEAM_BIASES.get(tb, {}).get('att_bias', 1.0) if tb else 1.0
    db = TEAM_BIASES.get(ta, {}).get('def_bias', 1.0) if ta else 1.0
    eb = TEAM_BIASES.get(tb, {}).get('def_bias', 1.0) if tb else 1.0
    off_a = ab * (OFF_ATT_W * _get(s_a, 'attack') + OFF_MID_W * _get(s_a, 'midfield'))
    off_b = bb * (OFF_ATT_W * _get(s_b, 'attack') + OFF_MID_W * _get(s_b, 'midfield'))
    res_a = max(db * (RES_DEF_W * _get(s_a, 'defense') + RES_GK_W * _get(s_a, 'goalkeeper') + RES_MID_W * _get(s_a, 'midfield')), RES_FLOOR)
    res_b = max(eb * (RES_DEF_W * _get(s_b, 'defense') + RES_GK_W * _get(s_b, 'goalkeeper') + RES_MID_W * _get(s_b, 'midfield')), RES_FLOOR)
    return min(BASE_XG * off_a / res_b, MAX_XG), min(BASE_XG * off_b / res_a, MAX_XG)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Match simulation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def sim_group_match(ta, tb, scores):
    """Group stage — draw allowed. Returns (goals_a, goals_b)."""
    xg_a, xg_b = compute_xg(scores[ta], scores[tb], ta, tb)
    return int(np.random.poisson(xg_a)), int(np.random.poisson(xg_b))


def sim_knockout_match(ta, tb, scores):
    """
    Knockout — must have a winner.
    Regulation → extra time (if draw) → penalties (if still level).
    Returns winner team key.
    """
    xg_a, xg_b = compute_xg(scores[ta], scores[tb], ta, tb)
    ga = int(np.random.poisson(xg_a))
    gb = int(np.random.poisson(xg_b))

    if ga != gb:
        return ta if ga > gb else tb

    # Extra time + penalties — times play defensively, most go to shootout (50/50)
    return ta if random.random() < 0.5 else tb


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Group stage
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _h2h_key(team, tied_teams, match_results):
    """Head-to-head sub-table for `team` among `tied_teams`."""
    pts = gd = gf = 0
    for opp in tied_teams:
        if opp == team:
            continue
        key = f"{team}|{opp}"
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


def simulate_group(teams, scores, letter=None):
    """
    Simulate one group (round-robin). Returns list of (team, pts, gd, gf, wins)
    sorted 1st → 4th.
    Tiebreaker (FIFA 2026): pts → H2H pts → H2H GD → H2H GF → overall GD → GF → wins → random.
    Already-played matches (in copa_real_state.json) use real scores.
    """
    stats = {t: {'pts': 0, 'gd': 0, 'gf': 0, 'wins': 0} for t in teams}
    real_group = _REAL_GROUP_RESULTS.get(letter, {}) if letter else {}
    match_results = {}   # "ta|tb" → (ga, gb) — all matches this group

    for ta, tb in combinations(teams, 2):
        key_ab, key_ba = f"{ta}|{tb}", f"{tb}|{ta}"
        if key_ab in real_group:
            ga, gb = real_group[key_ab]
        elif key_ba in real_group:
            gb, ga = real_group[key_ba]
        else:
            ga, gb = sim_group_match(ta, tb, scores)
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

    # Group teams by point total for head-to-head computation
    pts_groups = {}
    for t in teams:
        p = stats[t]['pts']
        pts_groups.setdefault(p, []).append(t)

    def sort_key(t):
        tied = pts_groups[stats[t]['pts']]
        h2h = _h2h_key(t, tied, match_results) if len(tied) > 1 else (0, 0, 0)
        return (
            -stats[t]['pts'],
            h2h[0], h2h[1], h2h[2],          # H2H pts, GD, GF (negated inside _h2h_key)
            -stats[t]['gd'],
            -stats[t]['gf'],
            -stats[t]['wins'],
            random.random(),
        )

    ranked = sorted(teams, key=sort_key)
    return [(t, stats[t]['pts'], stats[t]['gd'], stats[t]['gf'], stats[t]['wins'])
            for t in ranked]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Third-place selection and bracket assignment
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _rank_thirds(thirds):
    """
    thirds: list of (group_letter, team, pts, gd, gf, wins).
    Returns same list sorted best → worst.
    """
    return sorted(
        thirds,
        key=lambda x: (-x[2], -x[3], -x[4], -x[5], random.random()),
    )


def _assign_thirds(qualifying):
    """
    Assign 8 qualifying 3rd-place teams to Round-of-32 3rd-place slots.

    qualifying: list of (group_letter, team) in rank order (best first).
    Returns dict {match_id: team} using backtracking.
    Falls back to random assignment if no valid matching found (shouldn't happen).
    """
    slots  = list(THIRD_PLACE_SLOTS.keys())   # 8 match IDs
    assign = {}
    used   = [False] * len(qualifying)

    def bt(slot_idx):
        if slot_idx == len(slots):
            return True
        slot     = slots[slot_idx]
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

    # Fallback: random (should never trigger with valid FIFA groups)
    shuffled = list(qualifying)
    random.shuffle(shuffled)
    return {slot: shuffled[i][1] for i, slot in enumerate(slots)}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Full tournament simulation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def simulate_tournament(scores):
    """
    Simulate one complete tournament from the Round of 16 onward.

    Fase de grupos + R32 são fato consumado (72 jogos de grupo + 16 do R32
    já decididos de verdade) — usa o bracket real fixo das oitavas
    (REAL_R16_BRACKET) em vez de resolver pelos specs de grupo do ROUND32,
    que ficaram dessincronizados dos resultados reais entrados em
    copa_real_state.json (ver TASKS.md/CLAUDE.md).

    Returns a dict with sets of teams that *participated* in each round:
      champion          : team key
      r32_participants  : 32 teams that reached R32 (fato real, fixo)
      r16_participants  : 16 teams in R16  (= R32 winners, fato real, fixo)
      qf_participants   :  8 teams in QFs  (= R16 winners)
      sf_participants   :  4 teams in SFs  (= QF winners)
      finalists         :  2 teams in Final (= SF winners)
    """
    match_teams = {}   # match_id → (team_a, team_b)
    winners = {}       # match_id → winning team

    def play(mid):
        ta, tb = match_teams[mid]
        real = _REAL_KNOCKOUT_RESULTS.get(str(mid))
        if real and real['winner'] in (ta, tb):
            w = real['winner']
        else:
            w = sim_knockout_match(ta, tb, scores)
        winners[mid] = w
        return w

    # Round of 16 — bracket real fixo (R32 já decidido)
    r16_participants = set()   # os 16 times reais que chegaram ao R16 (fato, 100%)
    for mid, (ta, tb) in REAL_R16_BRACKET.items():
        match_teams[mid] = (ta, tb)
        r16_participants.add(ta)
        r16_participants.add(tb)
        play(mid)

    # 32 times reais que jogaram o R32 (fato, 100%) — vencedores + perdedores
    r32_participants = set()
    for game in _REAL_KNOCKOUT_RESULTS.values():
        r32_participants.add(game['home'])
        r32_participants.add(game['away'])

    # Quarterfinals
    for mid, src1, src2 in QUARTERFINALS:
        match_teams[mid] = (winners[src1], winners[src2])
        play(mid)

    qf_participants = set(winners[mid] for mid in REAL_R16_BRACKET)  # R16 winners

    # Semifinals
    sf_losers = []
    for mid, src1, src2 in SEMIFINALS:
        ta, tb = winners[src1], winners[src2]
        match_teams[mid] = (ta, tb)
        w = play(mid)
        sf_losers.append(tb if w == ta else ta)

    sf_participants = set(winners[mid] for mid, *_ in QUARTERFINALS)  # QF winners

    # Final
    sf1_id, sf2_id = SEMIFINALS[0][0], SEMIFINALS[1][0]
    match_teams[FINAL_ID] = (winners[sf1_id], winners[sf2_id])
    champion = play(FINAL_ID)
    finalists = {winners[sf1_id], winners[sf2_id]}

    return {
        'champion':          champion,
        'r32_participants':  r32_participants,   # 32 teams
        'r16_participants':  r16_participants,   # 16 teams
        'qf_participants':   qf_participants,    #  8 teams
        'sf_participants':   sf_participants,    #  4 teams
        'finalists':         finalists,          #  2 teams
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Monte Carlo
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def run_monte_carlo(scores, n_sims):
    counts = {stage: defaultdict(int)
              for stage in ('champion', 'finalist', 'semifinalist',
                            'quarterfinalist', 'r16', 'r32')}

    t0 = time.time()
    for i in range(n_sims):
        if i % 1000 == 0 and i > 0:
            elapsed = time.time() - t0
            eta = elapsed / i * (n_sims - i)
            print(f"  {i:>6,} / {n_sims:,}  ({elapsed:.1f}s elapsed, ~{eta:.0f}s remaining)",
                  end='\r', flush=True)

        result = simulate_tournament(scores)

        counts['champion'][result['champion']] += 1
        for t in result['finalists']:
            counts['finalist'][t] += 1
        for t in result['sf_participants']:        # QF winners = SF participants
            counts['semifinalist'][t] += 1
        for t in result['qf_participants']:        # R16 winners = QF participants
            counts['quarterfinalist'][t] += 1
        for t in result['r16_participants']:       # R32 winners = R16 participants
            counts['r16'][t] += 1
        for t in result['r32_participants']:       # group stage advancers
            counts['r32'][t] += 1

    elapsed = time.time() - t0
    print(f"  {n_sims:>6,} / {n_sims:,}  done in {elapsed:.1f}s ({n_sims / elapsed:.0f} sim/s)   ")

    all_teams = sorted(t for teams in GROUPS.values() for t in teams)
    results = {}
    for team in all_teams:
        results[team] = {
            'champion_pct':       round(counts['champion'][team]       / n_sims * 100, 2),
            'finalist_pct':       round(counts['finalist'][team]       / n_sims * 100, 2),
            'semifinalist_pct':   round(counts['semifinalist'][team]   / n_sims * 100, 2),
            'quarterfinalist_pct':round(counts['quarterfinalist'][team] / n_sims * 100, 2),
            'r16_pct':            round(counts['r16'][team]            / n_sims * 100, 2),
            'r32_pct':            round(counts['r32'][team]            / n_sims * 100, 2),
        }
    return results


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Output helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_GROUP_OF = {team: g for g, teams in GROUPS.items() for team in teams}

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


def _name(team):
    return DISPLAY_NAMES.get(team, team.replace('_', ' ').title())


def print_results(results, n_sims, top_n=20):
    print(f"\n{'═'*85}")
    print(f"  2026 FIFA WORLD CUP — Monte Carlo results  ({n_sims:,} simulations)")
    print(f"{'═'*85}")
    print(f"  {'#':>2}  {'Team':<28} {'Grp'}  {'Champion':>9}  {'Finalist':>9}  {'Semi':>9}  {'QF':>9}  {'R16':>9}")
    print(f"  {'─'*80}")

    ranked = sorted(results.items(), key=lambda x: -x[1]['champion_pct'])
    for i, (team, s) in enumerate(ranked[:top_n], 1):
        g = _GROUP_OF[team]
        print(
            f"  {i:>2}. {_name(team):<28} [{g}]"
            f"  {s['champion_pct']:>8.1f}%"
            f"  {s['finalist_pct']:>8.1f}%"
            f"  {s['semifinalist_pct']:>8.1f}%"
            f"  {s['quarterfinalist_pct']:>8.1f}%"
            f"  {s['r16_pct']:>8.1f}%"
        )
    print(f"{'─'*85}")

    print("\n  Group advancement rates (R32):")
    for letter in sorted(GROUPS):
        teams = GROUPS[letter]
        line = f"  Group {letter}: "
        parts = [f"{_name(t)} {results[t]['r32_pct']:.0f}%" for t in teams]
        print(line + "  |  ".join(parts))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Entry point
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    n_sims = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000

    scores_path = "output/team_scores.json"
    if not os.path.exists(scores_path):
        sys.exit(f"Error: {scores_path} not found — run scripts/build_team_scores.py first.")

    with open(scores_path, encoding='utf-8') as f:
        scores = json.load(f)

    # Validate all group teams are present in scores
    missing = [
        f"Group {g}: {t}"
        for g, teams in GROUPS.items()
        for t in teams
        if t not in scores
    ]
    if missing:
        print("WARNING — teams missing from team_scores.json:")
        for m in missing:
            print(f"  {m}")

    print(f"Running {n_sims:,} Monte Carlo simulations...")
    results = run_monte_carlo(scores, n_sims)
    print_results(results, n_sims)

    os.makedirs("output", exist_ok=True)
    out_path = sys.argv[2] if len(sys.argv) > 2 else "output/simulation_results.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(
            {'n_simulations': n_sims, 'groups': GROUPS, 'results': results},
            f, ensure_ascii=False, indent=2,
        )
    print(f"\n  Full results saved to {out_path}\n")


if __name__ == '__main__':
    main()
