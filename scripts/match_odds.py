#!/usr/bin/env python3
"""
Probabilidades de resultado para uma partida específica.

Uso:
    python scripts/match_odds.py <time_casa> <time_fora> [N_simulacoes]

Exemplos:
    python scripts/match_odds.py brazil morocco
    python scripts/match_odds.py qatar switzerland 200000
    python scripts/match_odds.py australia turkey

Saída:
    - % vitória time da casa / empate / vitória time de fora
    - Top 5 placares mais prováveis com suas probabilidades
"""

import json
import os
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate import compute_xg, DISPLAY_NAMES

DEFAULT_SIMS = 100_000

TEAM_ALIASES = {
    "usa":          "united_states_of_america",
    "eua":          "united_states_of_america",
    "estados_unidos": "united_states_of_america",
    "south_korea":  "republic_of_korea",
    "coreia":       "republic_of_korea",
    "bosnia":       "bosnia_and_herzegovina",
    "bosnia_herz":  "bosnia_and_herzegovina",
    "cape_verde":   "cape_verte",
    "ivory_coast":  "ivory_coast",
    "iran":         "ira",
    "new_zealand":  "new_zealand",
    "saudi_arabia": "saudi_arabia",
    "south_africa": "south_africa",
    "czech":        "czech_republic",
    "czechia":      "czech_republic",
    "tchequia":     "czech_republic",
}


def resolve(name):
    key = name.lower().replace("-", "_").replace(" ", "_")
    return TEAM_ALIASES.get(key, key)


def dn(team):
    return DISPLAY_NAMES.get(team, team.replace("_", " ").title())


def run_match(team_a, team_b, scores, n_sims):
    sa = scores[team_a]
    sb = scores[team_b]
    xg_a, xg_b = compute_xg(sa, sb, team_a, team_b)

    wins_a = 0
    draws  = 0
    wins_b = 0
    score_counts = defaultdict(int)

    goals_a = np.random.poisson(xg_a, n_sims)
    goals_b = np.random.poisson(xg_b, n_sims)

    for ga, gb in zip(goals_a, goals_b):
        score_counts[(ga, gb)] += 1
        if ga > gb:
            wins_a += 1
        elif gb > ga:
            wins_b += 1
        else:
            draws += 1

    return wins_a, draws, wins_b, score_counts, xg_a, xg_b


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit("Uso: python scripts/match_odds.py <time_casa> <time_fora> [N]")

    team_a_raw = args[0]
    team_b_raw = args[1]
    n_sims = int(args[2]) if len(args) > 2 else DEFAULT_SIMS

    team_a = resolve(team_a_raw)
    team_b = resolve(team_b_raw)

    scores_path = "output/team_scores.json"
    if not os.path.exists(scores_path):
        sys.exit(f"Erro: {scores_path} não encontrado — rode scripts/build_team_scores.py primeiro.")

    with open(scores_path, encoding="utf-8") as f:
        scores = json.load(f)

    for t, raw in [(team_a, team_a_raw), (team_b, team_b_raw)]:
        if t not in scores:
            sys.exit(f"Time '{raw}' (→ '{t}') não encontrado em team_scores.json.\n"
                     f"Times disponíveis: {', '.join(sorted(scores))}")

    wins_a, draws, wins_b, score_counts, xg_a, xg_b = run_match(team_a, team_b, scores, n_sims)

    pct_a  = wins_a / n_sims * 100
    pct_d  = draws  / n_sims * 100
    pct_b  = wins_b / n_sims * 100

    top_scores = sorted(score_counts.items(), key=lambda x: -x[1])[:5]

    name_a = dn(team_a)
    name_b = dn(team_b)

    print()
    print(f"{'═'*55}")
    print(f"  {name_a}  vs  {name_b}")
    print(f"  {n_sims:,} simulações  |  xG: {xg_a:.2f} – {xg_b:.2f}")
    print(f"{'═'*55}")
    print(f"  {name_a:<28} {pct_a:>6.1f}%")
    print(f"  {'Empate':<28} {pct_d:>6.1f}%")
    print(f"  {name_b:<28} {pct_b:>6.1f}%")
    print(f"{'─'*55}")
    print(f"  Placares mais prováveis:")
    for (ga, gb), count in top_scores:
        pct = count / n_sims * 100
        bar = "█" * int(pct / 2)
        print(f"    {ga}–{gb}   {pct:>5.1f}%  {bar}")
    print(f"{'═'*55}")
    print()

    result = {
        "team_a":     team_a,
        "team_b":     team_b,
        "n_sims":     n_sims,
        "xg": {team_a: round(xg_a, 3), team_b: round(xg_b, 3)},
        "odds": {
            team_a:  round(pct_a, 1),
            "draw":  round(pct_d, 1),
            team_b:  round(pct_b, 1),
        },
        "top_scores": [
            {"score": f"{ga}-{gb}", "pct": round(count / n_sims * 100, 1)}
            for (ga, gb), count in top_scores
        ],
    }

    os.makedirs("output", exist_ok=True)
    out_path = f"output/odds_{team_a}_vs_{team_b}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  Resultados salvos em {out_path}")


if __name__ == "__main__":
    main()
