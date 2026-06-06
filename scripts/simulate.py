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

BASE_XG       = 1.3
FALLBACK_SCORE = 0.5
ET_FACTOR     = 0.35   # extra time: 30 min ≈ 35% of 90-min xG

# Resistance floor prevents division-by-zero for teams with 0.0 normalized scores
# (min-max normalization gives the weakest team in each sector exactly 0.0).
# At RES_FLOOR = 0.1, max xG ≈ 1.3 × 1.0 / 0.1 = 13; capped further by MAX_XG.
RES_FLOOR = 0.10
MAX_XG    = 8.0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  xG formula  (mirrors build_team_scores.py)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _get(scores, key):
    v = scores.get(key)
    return v if v is not None else FALLBACK_SCORE


def compute_xg(s_a, s_b):
    """
    Return (xG_A, xG_B) for a match between teams with score dicts s_a and s_b.

    RES_FLOOR prevents division-by-zero when a team has 0.0 normalized scores
    (min-max normalization assigns 0.0 to the weakest team in each sector).
    MAX_XG caps extreme values that would cause numpy Poisson overflow.
    """
    off_a = 0.7 * _get(s_a, 'attack')  + 0.3 * _get(s_a, 'midfield')
    off_b = 0.7 * _get(s_b, 'attack')  + 0.3 * _get(s_b, 'midfield')
    res_a = max(0.6 * _get(s_a, 'defense') + 0.2 * _get(s_a, 'goalkeeper') + 0.2 * _get(s_a, 'midfield'), RES_FLOOR)
    res_b = max(0.6 * _get(s_b, 'defense') + 0.2 * _get(s_b, 'goalkeeper') + 0.2 * _get(s_b, 'midfield'), RES_FLOOR)
    return min(BASE_XG * off_a / res_b, MAX_XG), min(BASE_XG * off_b / res_a, MAX_XG)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Match simulation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def sim_group_match(ta, tb, scores):
    """Group stage — draw allowed. Returns (goals_a, goals_b)."""
    xg_a, xg_b = compute_xg(scores[ta], scores[tb])
    return int(np.random.poisson(xg_a)), int(np.random.poisson(xg_b))


def sim_knockout_match(ta, tb, scores):
    """
    Knockout — must have a winner.
    Regulation → extra time (if draw) → penalties (if still level).
    Returns winner team key.
    """
    xg_a, xg_b = compute_xg(scores[ta], scores[tb])
    ga = int(np.random.poisson(xg_a))
    gb = int(np.random.poisson(xg_b))

    if ga != gb:
        return ta if ga > gb else tb

    # Extra time
    et_a = int(np.random.poisson(xg_a * ET_FACTOR))
    et_b = int(np.random.poisson(xg_b * ET_FACTOR))
    if et_a != et_b:
        return ta if et_a > et_b else tb

    # Penalties — 50 / 50
    return ta if random.random() < 0.5 else tb


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Group stage
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def simulate_group(teams, scores):
    """
    Simulate one group (round-robin). Returns list of (team, pts, gd, gf, wins)
    sorted 1st → 4th. Tiebreaker: pts → GD → GF → wins → random.
    """
    stats = {t: {'pts': 0, 'gd': 0, 'gf': 0, 'wins': 0} for t in teams}

    for ta, tb in combinations(teams, 2):
        ga, gb = sim_group_match(ta, tb, scores)
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
    Simulate one complete tournament.

    Returns a dict with sets of teams that *participated* in each round:
      champion          : team key
      group_rankings    : {letter: [1st, 2nd, 3rd, 4th]}
      r32_participants  : 32 teams in R32 bracket (advanced from groups)
      r16_participants  : 16 teams in R16  (= R32 winners)
      qf_participants   :  8 teams in QFs  (= R16 winners)
      sf_participants   :  4 teams in SFs  (= QF winners)
      finalists         :  2 teams in Final (= SF winners)
    """
    # ── Group stage ──────────────────────────────────────────────────
    group_rankings = {}   # letter → [(team, pts, gd, gf, wins), ...]
    thirds         = []   # (group_letter, team, pts, gd, gf, wins)

    for letter, teams in GROUPS.items():
        ranked = simulate_group(teams, scores)
        group_rankings[letter] = ranked
        _, *third = ranked[2]
        thirds.append((letter, ranked[2][0], *third))

    # ── Best-8 third-place ────────────────────────────────────────────
    ranked_thirds    = _rank_thirds(thirds)
    qualifying_thirds = [(g, t) for g, t, *_ in ranked_thirds[:8]]
    third_slot_map   = _assign_thirds(qualifying_thirds)  # {match_id: team}

    # ── Build Round-of-32 matchups ────────────────────────────────────
    match_teams = {}   # match_id → (team_a, team_b)

    for mid, spec1, spec2 in ROUND32:
        def resolve(spec, mid=mid):
            kind, val = spec
            if kind == '1':
                return group_rankings[val][0][0]
            if kind == '2':
                return group_rankings[val][1][0]
            # '3rd'
            return third_slot_map.get(mid)

        team_a = resolve(spec1)
        team_b = resolve(spec2)
        match_teams[mid] = (team_a, team_b)

    # ── Simulate knockout rounds ──────────────────────────────────────
    winners = {}   # match_id → winning team

    def play(mid):
        ta, tb = match_teams[mid]
        w = sim_knockout_match(ta, tb, scores)
        winners[mid] = w
        return w

    # Round of 32 — collect participants before simulating
    r32_participants = set()
    for mid, _, _ in ROUND32:
        ta, tb = match_teams[mid]
        r32_participants.add(ta)
        if tb is not None:
            r32_participants.add(tb)
        play(mid)

    # Round of 16
    for mid, src1, src2 in ROUND16:
        match_teams[mid] = (winners[src1], winners[src2])
        play(mid)

    r16_participants = set(winners[mid] for mid, *_ in ROUND32)   # R32 winners

    # Quarterfinals
    for mid, src1, src2 in QUARTERFINALS:
        match_teams[mid] = (winners[src1], winners[src2])
        play(mid)

    qf_participants = set(winners[mid] for mid, *_ in ROUND16)    # R16 winners

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
        'group_rankings':    {l: [t for t, *_ in ranked] for l, ranked in group_rankings.items()},
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
    out_path = "output/simulation_results.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(
            {'n_simulations': n_sims, 'groups': GROUPS, 'results': results},
            f, ensure_ascii=False, indent=2,
        )
    print(f"\n  Full results saved to {out_path}\n")


if __name__ == '__main__':
    main()
