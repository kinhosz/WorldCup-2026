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


def extra_time_breakdown(xg_a, xg_b, n_draws):
    """Simula os 30min de prorrogação pra quem empatou nos 90'.

    xG escalado por 1/3 (proporcional ao tempo) — validado contra os 8
    empates reais do mata-mata até as semifinais: 8.72 gols esperados vs
    7 observados (4 jogos foram a pênaltis sem gol na prorrogação, 4 tiveram
    gols, com a Argentina marcando nas 2 vezes em que foi a prorrogação).
    Pênaltis, se ainda empatado após a prorrogação, seguem 50/50.
    """
    if n_draws == 0:
        return {"et_wins_a": 0, "et_wins_b": 0, "et_draws": 0,
                "pens_a": 0, "pens_b": 0}

    et_a = np.random.poisson(xg_a / 3, n_draws)
    et_b = np.random.poisson(xg_b / 3, n_draws)
    et_wins_a = int((et_a > et_b).sum())
    et_wins_b = int((et_b > et_a).sum())
    et_draws  = n_draws - et_wins_a - et_wins_b

    pens_a = int((np.random.random(et_draws) < 0.5).sum())
    pens_b = et_draws - pens_a

    return {"et_wins_a": et_wins_a, "et_wins_b": et_wins_b, "et_draws": et_draws,
            "pens_a": pens_a, "pens_b": pens_b}


def derived_metrics(score_counts, n_sims):
    """Métricas assertivas derivadas do placar — indiferentes a quem vence,
    então funcionam mesmo em jogos de mata-mata (ver metodologia em CLAUDE.md).
    """
    def pct(cond):
        return sum(c for (ga, gb), c in score_counts.items() if cond(ga, gb)) / n_sims * 100

    return {
        "over_2_5":        pct(lambda ga, gb: ga + gb >= 3),
        "under_2_5":       pct(lambda ga, gb: ga + gb <= 2),
        "btts_yes":        pct(lambda ga, gb: ga >= 1 and gb >= 1),
        "btts_no":         pct(lambda ga, gb: ga == 0 or gb == 0),
        "clean_sheet_a":   pct(lambda ga, gb: gb == 0),
        "clean_sheet_b":   pct(lambda ga, gb: ga == 0),
        "margin_a_2plus":  pct(lambda ga, gb: ga - gb >= 2),
        "margin_b_2plus":  pct(lambda ga, gb: gb - ga >= 2),
    }


def best_assertive_claim(dm, name_a, name_b):
    """Escolhe a claim de maior probabilidade entre as métricas derivadas
    (não inclui quem-avança — essa já é a chamada principal do card)."""
    candidates = [
        (f"Menos de 2.5 gols",              dm["under_2_5"]),
        (f"Mais de 2.5 gols",               dm["over_2_5"]),
        (f"Ambas marcam",                   dm["btts_yes"]),
        (f"Nem todas marcam",               dm["btts_no"]),
        (f"{name_a} não sofre gol",         dm["clean_sheet_a"]),
        (f"{name_b} não sofre gol",         dm["clean_sheet_b"]),
        (f"{name_a} vence por 2+ gols",     dm["margin_a_2plus"]),
        (f"{name_b} vence por 2+ gols",     dm["margin_b_2plus"]),
    ]
    label, pct = max(candidates, key=lambda x: x[1])
    return label, pct


def main():
    args = sys.argv[1:]
    knockout = "--mata-mata" in args or "--knockout" in args
    no_et = "--no-extra-time" in args or "--terceiro-lugar" in args
    args = [a for a in args if a not in
            ("--mata-mata", "--knockout", "--no-extra-time", "--terceiro-lugar")]

    if len(args) < 2:
        sys.exit("Uso: python scripts/match_odds.py <time_casa> <time_fora> [N] [--mata-mata]")

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

    dm = derived_metrics(score_counts, n_sims)
    assertive_label, assertive_pct = best_assertive_claim(dm, name_a, name_b)

    et = None
    if knockout and not no_et:
        et = extra_time_breakdown(xg_a, xg_b, draws)
        advance_a = (wins_a + et["et_wins_a"] + et["pens_a"]) / n_sims * 100
        advance_b = (wins_b + et["et_wins_b"] + et["pens_b"]) / n_sims * 100
        pct_et_a  = et["et_wins_a"] / n_sims * 100
        pct_et_b  = et["et_wins_b"] / n_sims * 100
        pct_et_d  = et["et_draws"]  / n_sims * 100
    else:
        # Sem prorrogação (3º lugar, regra FIFA) — empate nos 90' vai direto pra pênaltis 50/50
        advance_a = pct_a + 0.5 * pct_d
        advance_b = pct_b + 0.5 * pct_d

    print()
    print(f"{'═'*55}")
    print(f"  {name_a}  vs  {name_b}")
    print(f"  {n_sims:,} simulações  |  xG: {xg_a:.2f} – {xg_b:.2f}")
    print(f"{'═'*55}")
    if knockout and not no_et:
        print(f"  Quem avança (prorrogação modelada + pênaltis 50/50):")
        print(f"  {name_a:<28} {advance_a:>6.1f}%")
        print(f"  {name_b:<28} {advance_b:>6.1f}%")
        print(f"  (90': {name_a} {pct_a:.1f}% · Empate {pct_d:.1f}% · {name_b} {pct_b:.1f}%)")
        print(f"  (prorrogação, dado empate nos 90': {name_a} {pct_et_a:.1f}% · "
              f"ainda empatado {pct_et_d:.1f}% · {name_b} {pct_et_b:.1f}%)")
    elif knockout:
        print(f"  Quem avança (sem prorrogação — regra FIFA do 3º lugar — pênaltis 50/50):")
        print(f"  {name_a:<28} {advance_a:>6.1f}%")
        print(f"  {name_b:<28} {advance_b:>6.1f}%")
        print(f"  (90': {name_a} {pct_a:.1f}% · Empate {pct_d:.1f}% · {name_b} {pct_b:.1f}%)")
    else:
        print(f"  {name_a:<28} {pct_a:>6.1f}%")
        print(f"  {'Empate':<28} {pct_d:>6.1f}%")
        print(f"  {name_b:<28} {pct_b:>6.1f}%")
    print(f"{'─'*55}")
    print(f"  Aposta assertiva: {assertive_label} — {assertive_pct:.1f}%")
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
        "knockout":   knockout,
        "xg": {team_a: round(xg_a, 3), team_b: round(xg_b, 3)},
        "odds": {
            team_a:  round(pct_a, 1),
            "draw":  round(pct_d, 1),
            team_b:  round(pct_b, 1),
        },
        "advance": {
            team_a: round(advance_a, 1),
            team_b: round(advance_b, 1),
        } if knockout else None,
        "extra_time": {
            team_a:  round(pct_et_a, 1),
            "draw":  round(pct_et_d, 1),
            team_b:  round(pct_et_b, 1),
            "note":  "% dado empate nos 90'; pênaltis (50/50) resolvem o que sobra empatado",
        } if (knockout and not no_et) else None,
        "derived_metrics": {k: round(v, 1) for k, v in dm.items()},
        "assertive_bet": {"label": assertive_label, "pct": round(assertive_pct, 1)},
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
