#!/usr/bin/env python3
"""
megazord.py — MEGAZORD Consensus Bracket · FIFA World Cup 2026

Group stage: position probabilities from N Monte Carlo simulations.
Bracket positions assigned by greedy argmax (team most likely to finish
at each position gets that slot). Advance probability tracks R32 qualification
including best-3rd-place rule across all 12 groups.

Knockout rounds: modal winner from K sub-simulations per match.

Usage:
    python scripts/megazord.py [N_SIMS]
    python scripts/megazord.py 50000   (default)

Output: output/megazord_report_en.md
"""

import json
import os
import random
import sys
import time
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from simulate import (
    GROUPS, ROUND32, ROUND16, QUARTERFINALS, SEMIFINALS, FINAL_ID,
    ET_FACTOR,
    compute_xg, sim_group_match, _assign_thirds, DISPLAY_NAMES,
)

SCORES_PATH = "output/team_scores.json"
OUT_PATH    = "output/megazord_report_en.md"
K_KO        = 10_000


def _name(team):
    return DISPLAY_NAMES.get(team, team.replace('_', ' ').title())


def load_scores():
    with open(SCORES_PATH, encoding='utf-8') as f:
        return json.load(f)


# ─── Phase 1: Collect group-stage distributions ──────────────────────────────

def collect_groups(scores, n, seed=2026):
    """
    Run N group-stage simulations. Returns:
      rank_ctr[g]         : Counter of (1st,2nd,3rd,4th) ranking tuples
      match_ctr[g][(a,b)] : Counter of (ga,gb) scorelines
      third_stat[g][team] : list of (pts,gd,gf,wins) when team finishes 3rd
      advance_ctr[g][team]: # simulations where team advanced to R32
                            (1st + 2nd always advance; 3rd only if best 8 of 12)
    """
    random.seed(seed)
    np.random.seed(seed % (2**32))

    rank_ctr    = {g: Counter() for g in GROUPS}
    match_ctr   = {g: {} for g in GROUPS}
    third_stat  = {g: defaultdict(list) for g in GROUPS}
    advance_ctr = {g: {t: 0 for t in teams} for g, teams in GROUPS.items()}

    for g, teams in GROUPS.items():
        for a, b in combinations(sorted(teams), 2):
            match_ctr[g][(a, b)] = Counter()

    t0 = time.time()
    for i in range(n):
        if i % 5000 == 0 and i:
            print(f"  groups: {i:,}/{n:,}  ({time.time()-t0:.1f}s)", end='\r', flush=True)

        sim_rankings = {}
        sim_stats    = {}

        for g, teams in GROUPS.items():
            st = {t: {'pts': 0, 'gd': 0, 'gf': 0, 'wins': 0} for t in teams}
            for a, b in combinations(sorted(teams), 2):
                ga, gb = sim_group_match(a, b, scores)
                match_ctr[g][(a, b)][(ga, gb)] += 1
                st[a]['gf'] += ga;  st[b]['gf'] += gb
                st[a]['gd'] += ga - gb;  st[b]['gd'] += gb - ga
                if ga > gb:
                    st[a]['pts'] += 3;  st[a]['wins'] += 1
                elif gb > ga:
                    st[b]['pts'] += 3;  st[b]['wins'] += 1
                else:
                    st[a]['pts'] += 1;  st[b]['pts'] += 1

            ranked = sorted(
                teams,
                key=lambda t: (-st[t]['pts'], -st[t]['gd'],
                               -st[t]['gf'], -st[t]['wins'], random.random()),
            )
            rank_ctr[g][tuple(ranked)] += 1
            s3 = st[ranked[2]]
            third_stat[g][ranked[2]].append((s3['pts'], s3['gd'], s3['gf'], s3['wins']))
            sim_rankings[g] = ranked
            sim_stats[g]    = st

        # Determine which 3rd-place teams advance (best 8 of 12 groups)
        all_thirds = []
        for g, ranked in sim_rankings.items():
            t3 = ranked[2]
            s3 = sim_stats[g][t3]
            all_thirds.append((g, t3, s3['pts'], s3['gd'], s3['gf'], s3['wins']))

        best_8_set = {
            (g, t)
            for g, t, *_ in sorted(
                all_thirds,
                key=lambda x: (-x[2], -x[3], -x[4], -x[5], random.random()),
            )[:8]
        }

        for g, ranked in sim_rankings.items():
            advance_ctr[g][ranked[0]] += 1
            advance_ctr[g][ranked[1]] += 1
            if (g, ranked[2]) in best_8_set:
                advance_ctr[g][ranked[2]] += 1

    elapsed = time.time() - t0
    print(f"  groups: {n:,}/{n:,}  done in {elapsed:.1f}s          ")
    return rank_ctr, match_ctr, third_stat, advance_ctr


# ─── Phase 2: Derive predictions ─────────────────────────────────────────────

def derive_groups(rank_ctr, match_ctr, third_stat, advance_ctr, n):
    """
    Returns:
      order[g]      : [1st,2nd,3rd,4th] — greedy argmax of position probabilities
      pos_probs[g]  : {team: [p1%,p2%,p3%,p4%]}
      advance_pct[g]: {team: R32 advance %}
      mscores[g]    : {(a,b): (ga,gb)} — modal scoreline (used for 3rd-place ranking)
      stats[g]      : {team: {pts,gd,gf,wins}} — derived from modal scorelines
    """
    order       = {}
    pos_probs   = {}
    advance_pct = {}
    mscores     = {}
    stats       = {}

    for g, teams in GROUPS.items():
        total = sum(rank_ctr[g].values())

        # Per-position probabilities
        pos_cnt = {t: [0, 0, 0, 0] for t in teams}
        for ranking, cnt in rank_ctr[g].items():
            for i, t in enumerate(ranking):
                pos_cnt[t][i] += cnt
        pos_probs[g]   = {t: [c / total * 100 for c in pos_cnt[t]] for t in teams}
        advance_pct[g] = {t: advance_ctr[g][t] / n * 100 for t in teams}

        # Greedy argmax: assign each position to the team most likely to finish there
        remaining = list(teams)
        ranked = []
        for pos in range(4):
            pick = max(remaining, key=lambda t: pos_probs[g][t][pos])
            ranked.append(pick)
            remaining.remove(pick)
        order[g] = ranked

        # Modal scorelines (for 3rd-place team ranking in bracket)
        mscores[g] = {}
        st = {t: {'pts': 0, 'gd': 0, 'gf': 0, 'wins': 0} for t in teams}
        for (a, b), ctr in match_ctr[g].items():
            ga, gb = ctr.most_common(1)[0][0]
            mscores[g][(a, b)] = (ga, gb)
            st[a]['gf'] += ga;  st[b]['gf'] += gb
            st[a]['gd'] += ga - gb;  st[b]['gd'] += gb - ga
            if ga > gb:
                st[a]['pts'] += 3;  st[a]['wins'] += 1
            elif gb > ga:
                st[b]['pts'] += 3;  st[b]['wins'] += 1
            else:
                st[a]['pts'] += 1;  st[b]['pts'] += 1
        stats[g] = st

    return order, pos_probs, advance_pct, mscores, stats


def best_thirds(order, third_stat):
    """
    Predicted 3rd-place team per group = order[g][2].
    Rank them by their average stats across all simulations where they finished 3rd.
    """
    thirds = []
    for g, ranking in order.items():
        team = ranking[2]
        runs = third_stat[g].get(team, [])
        if runs:
            avg = lambda i: sum(r[i] for r in runs) / len(runs)
            thirds.append((g, team, avg(0), avg(1), avg(2), avg(3)))
        else:
            thirds.append((g, team, 0.0, 0.0, 0.0, 0.0))

    return sorted(thirds, key=lambda x: (-x[2], -x[3], -x[4], -x[5]))


# ─── Phase 3: Simulate knockout rounds ───────────────────────────────────────

def modal_ko(ta, tb, scores, k=K_KO, seed_off=0):
    """
    Run K knockout simulations. Returns (winner, ga, gb, method, win_pct)
    where ga/gb is the modal scoreline conditioned on the modal winner winning.
    """
    random.seed(2026 + seed_off)
    np.random.seed((2026 + seed_off) % (2**32))

    xg_a, xg_b = compute_xg(scores[ta], scores[tb])
    outcomes    = Counter()

    for _ in range(k):
        ga = int(np.random.poisson(xg_a))
        gb = int(np.random.poisson(xg_b))
        if ga != gb:
            outcomes[(ta if ga > gb else tb, ga, gb, "90'")] += 1
        else:
            ea = int(np.random.poisson(xg_a * ET_FACTOR))
            eb = int(np.random.poisson(xg_b * ET_FACTOR))
            if ea != eb:
                w = ta if ea > eb else tb
                outcomes[(w, ga + ea, gb + eb, "AET")] += 1
            else:
                w = ta if random.random() < 0.5 else tb
                outcomes[(w, ga, gb, "PEN")] += 1

    win_cnt = Counter()
    for (w, *_), cnt in outcomes.items():
        win_cnt[w] += cnt

    winner  = win_cnt.most_common(1)[0][0]
    win_pct = win_cnt[winner] / k * 100

    winner_oc = Counter({key: v for key, v in outcomes.items() if key[0] == winner})
    (_, ga_m, gb_m, meth), _ = winner_oc.most_common(1)[0]

    return winner, ga_m, gb_m, meth, win_pct


def build_bracket(order, thirds_ranked, scores):
    qualifying     = [(g, t) for g, t, *_ in thirds_ranked[:8]]
    third_slot_map = _assign_thirds(qualifying)

    match_teams = {}
    for mid, spec1, spec2 in ROUND32:
        def resolve(spec, mid=mid):
            kind, val = spec
            if kind == '1': return order[val][0]
            if kind == '2': return order[val][1]
            return third_slot_map.get(mid)
        match_teams[mid] = (resolve(spec1), resolve(spec2))

    match_results = {}
    winners       = {}

    def play(mid, seed_off):
        ta, tb = match_teams[mid]
        w, ga, gb, meth, pct = modal_ko(ta, tb, scores, seed_off=seed_off)
        winners[mid] = w
        match_results[mid] = {
            'home': ta, 'away': tb, 'winner': w,
            'loser': tb if w == ta else ta,
            'ga': ga, 'gb': gb, 'method': meth, 'win_pct': pct,
        }

    total_ko = len(ROUND32) + len(ROUND16) + len(QUARTERFINALS) + len(SEMIFINALS) + 1
    done = 0

    for mid, _, _ in ROUND32:
        play(mid, seed_off=mid);  done += 1
        print(f"  knockout: {done}/{total_ko}", end='\r', flush=True)

    for mid, s1, s2 in ROUND16:
        match_teams[mid] = (winners[s1], winners[s2])
        play(mid, seed_off=mid);  done += 1
        print(f"  knockout: {done}/{total_ko}", end='\r', flush=True)

    for mid, s1, s2 in QUARTERFINALS:
        match_teams[mid] = (winners[s1], winners[s2])
        play(mid, seed_off=mid);  done += 1
        print(f"  knockout: {done}/{total_ko}", end='\r', flush=True)

    for mid, s1, s2 in SEMIFINALS:
        match_teams[mid] = (winners[s1], winners[s2])
        play(mid, seed_off=mid);  done += 1
        print(f"  knockout: {done}/{total_ko}", end='\r', flush=True)

    match_teams[FINAL_ID] = (winners[SEMIFINALS[0][0]], winners[SEMIFINALS[1][0]])
    play(FINAL_ID, seed_off=FINAL_ID);  done += 1
    print(f"  knockout: {done}/{total_ko}  ✓          ")

    return match_results, winners, qualifying


# ─── Phase 4: Generate report ────────────────────────────────────────────────

def format_score(r):
    ga, gb = r['ga'], r['gb']
    if r['method'] == 'PEN':  return f"{ga}–{gb} pen."
    if r['method'] == 'AET':  return f"{ga}–{gb} (AET)"
    return f"{ga}–{gb}"


def generate_report(order, pos_probs, advance_pct, mscores,
                    thirds_ranked, qualifying, match_results, winners, n_sims):
    lines = []
    nl = lines.append
    qual_groups = {g for g, _ in qualifying}

    nl("# MEGAZORD — Consensus Bracket · FIFA World Cup 2026")
    nl("")
    nl(f"*Based on {n_sims:,} Monte Carlo simulations.*  ")
    nl("*Group stage: bracket positions assigned by argmax of finishing-position probabilities.*  ")
    nl(f"*Knockout: modal winner from {K_KO:,} sub-simulations per match.*")
    nl("")
    nl("---")
    nl("")
    nl("## GROUP STAGE")
    nl("")

    for g in sorted(GROUPS):
        ranked = order[g]
        probs  = pos_probs[g]
        adv    = advance_pct[g]

        nl(f"### Group {g}")
        nl("")
        nl("| # | Team | 1st% | 2nd% | 3rd% | 4th% | Advance% | |")
        nl("|---|------|------|------|------|------|----------|---|")
        for pos, team in enumerate(ranked, 1):
            p = probs[team]
            if pos == 1:
                clf = "→ R32 (1st)"
            elif pos == 2:
                clf = "→ R32 (2nd)"
            elif pos == 3:
                clf = "→ R32 (3rd?)" if g in qual_groups else "✗"
            else:
                clf = "✗"
            nl(f"| {pos} | **{_name(team)}** | {p[0]:.1f}% | {p[1]:.1f}% | {p[2]:.1f}% | {p[3]:.1f}% | **{adv[team]:.1f}%** | {clf} |")
        nl("")
        nl("**Modal scorelines** *(used for 3rd-place bracket seeding only)*")
        nl("")
        for (a, b), (ga, gb) in sorted(mscores[g].items()):
            if ga > gb:
                line = f"- **{_name(a)}** {ga}–{gb} {_name(b)}"
            elif gb > ga:
                line = f"- {_name(a)} {ga}–{gb} **{_name(b)}**"
            else:
                line = f"- {_name(a)} {ga}–{gb} {_name(b)}  *(draw)*"
            nl(line)
        nl("")

    nl("---")
    nl("")
    nl("## 8 BEST THIRD-PLACE QUALIFIERS")
    nl("")
    nl("*Predicted 3rd-place team per group (argmax), ranked by average stats when finishing 3rd.*")
    nl("")
    nl("| # | Team | Group | Avg Pts | Avg GD | Advance% |")
    nl("|---|------|-------|---------|--------|----------|")
    for rank, (g, team, pts, gd, gf, _) in enumerate(thirds_ranked[:8], 1):
        adv = advance_pct[g][team]
        nl(f"| {rank} | **{_name(team)}** | {g} | {pts:.1f} | {gd:+.1f} | {adv:.1f}% |")
    nl("")

    def fmt_round(round_ids, title):
        nl("---")
        nl("")
        nl(f"## {title}")
        nl("")
        nl("| Match | Home | Score | Away | Phase | Win Prob. |")
        nl("|-------|------|-------|------|-------|-----------|")
        for mid in round_ids:
            r = match_results[mid]
            h, a, w = r['home'], r['away'], r['winner']
            bh = "**" if w == h else ""
            ba = "**" if w == a else ""
            sc = format_score(r)
            nl(f"| M{mid} | {bh}{_name(h)}{bh} | {sc} | {ba}{_name(a)}{ba} | {r['method']} | {_name(w)} ({r['win_pct']:.0f}%) |")
        nl("")

    fmt_round([m for m, *_ in ROUND32],       "ROUND OF 32")
    fmt_round([m for m, *_ in ROUND16],       "ROUND OF 16")
    fmt_round([m for m, *_ in QUARTERFINALS], "QUARTERFINALS")
    fmt_round([m for m, *_ in SEMIFINALS],    "SEMIFINALS")

    nl("---")
    nl("")
    nl("## FINAL")
    nl("")
    r  = match_results[FINAL_ID]
    sc = format_score(r)
    nl(f"| {_name(r['home'])} | **{sc}** | {_name(r['away'])} | {r['method']} |")
    nl("|---|---|---|---|")
    nl("")
    champion  = winners[FINAL_ID]
    runner_up = r['loser']
    nl(f"## CHAMPION: **{_name(champion).upper()}**")
    nl("")
    nl(f"Score: **{_name(r['home'])} {sc} {_name(r['away'])}**  ")
    nl(f"Method: {r['method']} | Champion's win probability in the final: **{r['win_pct']:.0f}%**")
    nl("")
    nl("---")
    nl("")
    nl("## BRACKET SUMMARY")
    nl("")
    nl("| Round | Winner |")
    nl("|-------|--------|")
    for mid, *_ in SEMIFINALS:
        nl(f"| Semifinal M{mid} | **{_name(winners[mid])}** |")
    nl(f"| Runner-up | {_name(runner_up)} |")
    nl(f"| **CHAMPION** | **{_name(champion)}** |")
    nl("")

    return "\n".join(lines)


# ─── Entry point ─────────────────────────────────────────────────────────────

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000
    scores = load_scores()

    print(f"Megazord — collecting group data ({n:,} simulations)...")
    rank_ctr, match_ctr, third_stat, advance_ctr = collect_groups(scores, n)

    print("Deriving group predictions (argmax)...")
    order, pos_probs, advance_pct, mscores, stats = derive_groups(
        rank_ctr, match_ctr, third_stat, advance_ctr, n
    )

    print("Ranking third-place qualifiers...")
    thirds_ranked = best_thirds(order, third_stat)

    print(f"Simulating knockout bracket ({K_KO:,} sub-sims per match)...")
    match_results, winners, qualifying = build_bracket(order, thirds_ranked, scores)

    print("Generating report...")
    report = generate_report(
        order, pos_probs, advance_pct, mscores,
        thirds_ranked, qualifying, match_results, winners, n,
    )

    os.makedirs("output", exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)

    champion  = winners[FINAL_ID]
    runner_up = match_results[FINAL_ID]['loser']
    print(f"\nReport saved to {OUT_PATH}")
    print(f"\n{'═'*50}")
    print(f"  CHAMPION : {_name(champion).upper()}")
    print(f"  Runner-up: {_name(runner_up).upper()}")
    print(f"{'═'*50}\n")


if __name__ == '__main__':
    main()
