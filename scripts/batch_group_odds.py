#!/usr/bin/env python3
"""
Calcula odds para todos os 72 jogos da fase de grupos com Model4
e consolida em output/model4_group_odds.json.

Uso:
    python scripts/batch_group_odds.py [N_simulacoes]

Pula jogos que já têm arquivo individual salvo.
"""

import json
import os
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate import compute_xg

DEFAULT_SIMS = 1_000_000

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


def all_group_matches():
    matches = []
    for group, teams in GROUPS.items():
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                matches.append((group, teams[i], teams[j]))
    return matches


def run_match(team_a, team_b, scores, n_sims):
    sa = scores[team_a]
    sb = scores[team_b]
    xg_a, xg_b = compute_xg(sa, sb, team_a, team_b)

    goals_a = np.random.poisson(xg_a, n_sims)
    goals_b = np.random.poisson(xg_b, n_sims)

    wins_a = int(np.sum(goals_a > goals_b))
    draws  = int(np.sum(goals_a == goals_b))
    wins_b = int(np.sum(goals_b > goals_a))

    score_counts = defaultdict(int)
    for ga, gb in zip(goals_a, goals_b):
        score_counts[(ga, gb)] += 1

    top_scores = sorted(score_counts.items(), key=lambda x: -x[1])[:5]

    return wins_a, draws, wins_b, top_scores, xg_a, xg_b


def main():
    n_sims = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SIMS

    scores_path = "output/team_scores.json"
    if not os.path.exists(scores_path):
        sys.exit(f"Erro: {scores_path} não encontrado.")
    with open(scores_path, encoding="utf-8") as f:
        scores = json.load(f)

    matches = all_group_matches()
    print(f"Total de jogos da fase de grupos: {len(matches)}")
    print(f"Simulações por jogo: {n_sims:,}\n")

    consolidated = {}
    skipped = 0
    computed = 0

    for idx, (group, team_a, team_b) in enumerate(matches, 1):
        out_path = f"output/odds_{team_a}_vs_{team_b}.json"

        if os.path.exists(out_path):
            with open(out_path, encoding="utf-8") as f:
                result = json.load(f)
            consolidated[f"{team_a}|{team_b}"] = {**result, "group": group}
            skipped += 1
            continue

        print(f"[{idx:02}/{len(matches)}] {team_a} vs {team_b}...", end=" ", flush=True)
        wins_a, draws, wins_b, top_scores, xg_a, xg_b = run_match(team_a, team_b, scores, n_sims)

        pct_a = round(wins_a / n_sims * 100, 1)
        pct_d = round(draws  / n_sims * 100, 1)
        pct_b = round(wins_b / n_sims * 100, 1)

        result = {
            "team_a": team_a,
            "team_b": team_b,
            "n_sims": n_sims,
            "xg": {team_a: round(xg_a, 3), team_b: round(xg_b, 3)},
            "odds": {
                team_a: pct_a,
                "draw":  pct_d,
                team_b:  pct_b,
            },
            "top_scores": [
                {"score": f"{ga}-{gb}", "pct": round(cnt / n_sims * 100, 1)}
                for (ga, gb), cnt in top_scores
            ],
        }

        os.makedirs("output", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        consolidated[f"{team_a}|{team_b}"] = {**result, "group": group}
        computed += 1
        print(f"W={pct_a}% D={pct_d}% L={pct_b}%")

    # Save consolidated file
    out_consolidated = "output/model4_group_odds.json"
    with open(out_consolidated, "w", encoding="utf-8") as f:
        json.dump(consolidated, f, ensure_ascii=False, indent=2)

    print(f"\nProntos: {computed} calculados + {skipped} já existiam = {len(consolidated)} total")
    print(f"Consolidado salvo em {out_consolidated}")


if __name__ == "__main__":
    main()
