#!/usr/bin/env python3
"""
Avaliação técnica do modelo preditivo.

Métricas calculadas:
  - Result Accuracy: % de partidas com resultado correto (vencedor ou empate)
  - Brier Score: mede calibração das probabilidades (0 = perfeito, 1 = péssimo)
  - Goal MAE: erro médio absoluto nos gols previstos vs reais

Uso:
    python3 scripts/model_eval.py
"""

import json
import os
import sys
import numpy as np
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate import compute_xg, DISPLAY_NAMES, GROUPS

N_SIMS = 100_000
STATE_FILE = "output/copa_real_state.json"
SCORES_FILE = "output/team_scores.json"

def dn(t):
    return DISPLAY_NAMES.get(t, t.replace("_", " ").title())

def get_match_probs(team_a, team_b, scores, n_sims=N_SIMS):
    """Retorna (p_win_a, p_draw, p_win_b) e (xg_a, xg_b)."""
    sa, sb = scores[team_a], scores[team_b]
    xg_a, xg_b = compute_xg(sa, sb)
    goals_a = np.random.poisson(xg_a, n_sims)
    goals_b = np.random.poisson(xg_b, n_sims)
    win_a = np.sum(goals_a > goals_b) / n_sims
    draw  = np.sum(goals_a == goals_b) / n_sims
    win_b = np.sum(goals_b > goals_a) / n_sims
    return (win_a, draw, win_b), (xg_a, xg_b)

def brier_score(probs, outcome):
    """
    Brier Score para um único jogo.
    probs: (p_win_a, p_draw, p_win_b)
    outcome: 'a' | 'draw' | 'b'
    """
    actuals = {
        'a':    [1, 0, 0],
        'draw': [0, 1, 0],
        'b':    [0, 0, 1],
    }[outcome]
    return sum((p - o) ** 2 for p, o in zip(probs, actuals))

def load_odds(team_a, team_b):
    """Carrega odds salvo pelo match_odds.py, se existir."""
    path = f"output/odds_{team_a}_vs_{team_b}.json"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None

def top_score_outcome(odds_data):
    """Deriva o resultado previsto pelo placar mais comum."""
    if not odds_data:
        return None
    top = odds_data["top_scores"][0]["score"]  # ex: "2-0"
    ga, gb = map(int, top.split("-"))
    return "a" if ga > gb else ("b" if gb > ga else "draw")


def main():
    for path in [STATE_FILE, SCORES_FILE]:
        if not os.path.exists(path):
            sys.exit(f"Erro: {path} não encontrado.")

    with open(STATE_FILE, encoding="utf-8") as f:
        state = json.load(f)
    with open(SCORES_FILE, encoding="utf-8") as f:
        scores = json.load(f)

    group_results = state.get("group_results", {})

    played = []
    for grp, matches in group_results.items():
        for key, score in matches.items():
            team_a, team_b = key.split("|")
            ga, gb = score
            played.append({
                "group":   grp,
                "team_a":  team_a,
                "team_b":  team_b,
                "goals_a": ga,
                "goals_b": gb,
                "outcome": "a" if ga > gb else ("b" if gb > ga else "draw"),
            })

    if not played:
        sys.exit("Nenhum resultado registrado em copa_real_state.json.")

    print(f"\nAnalisando {len(played)} partidas disputadas...\n")

    brier_scores = []
    correct_prob   = 0  # método 2: maior probabilidade
    correct_score  = 0  # método 1: placar mais comum
    goal_errors_a, goal_errors_b = [], []
    rows = []

    for m in played:
        ta, tb = m["team_a"], m["team_b"]
        if ta not in scores or tb not in scores:
            print(f"  Aviso: {dn(ta)} ou {dn(tb)} não encontrado. Pulando.")
            continue

        probs, (xg_a, xg_b) = get_match_probs(ta, tb, scores)
        bs = brier_score(probs, m["outcome"])
        brier_scores.append(bs)

        # Método 2 — maior probabilidade
        pred_prob = "a" if probs[0] >= probs[1] and probs[0] >= probs[2] else \
                    ("draw" if probs[1] >= probs[0] and probs[1] >= probs[2] else "b")
        ok_prob = pred_prob == m["outcome"]
        if ok_prob:
            correct_prob += 1

        # Método 1 — placar mais comum (carrega do JSON salvo)
        odds = load_odds(ta, tb)
        pred_score = top_score_outcome(odds)
        ok_score = (pred_score == m["outcome"]) if pred_score else None
        if ok_score:
            correct_score += 1

        # Probability Score — quanto o modelo apostou no resultado real
        prob_score = {"a": probs[0], "draw": probs[1], "b": probs[2]}[m["outcome"]]

        goal_errors_a.append(abs(xg_a - m["goals_a"]))
        goal_errors_b.append(abs(xg_b - m["goals_b"]))

        rows.append({
            "match":       f"{dn(ta)} vs {dn(tb)}",
            "real":        f"{m['goals_a']}–{m['goals_b']}",
            "outcome":     m["outcome"],
            "p_a":         probs[0],
            "p_draw":      probs[1],
            "p_b":         probs[2],
            "prob_score":  prob_score,
            "top_score":   odds["top_scores"][0]["score"] if odds else "?",
            "brier":       bs,
            "ok_prob":     ok_prob,
            "ok_score":    ok_score,
            "xg_a":        xg_a,
            "xg_b":        xg_b,
        })

    n = len(rows)
    mean_brier    = sum(brier_scores) / n
    mean_ps       = sum(r["prob_score"] for r in rows) / n
    acc_prob      = correct_prob  / n * 100
    acc_score     = correct_score / n * 100
    goal_mae      = (sum(goal_errors_a) + sum(goal_errors_b)) / (2 * n)
    baseline_brier = 2/3
    baseline_ps    = 1/3

    print(f"{'═'*75}")
    print(f"  AVALIAÇÃO DO MODELO — Copa do Mundo 2026  ({n} partidas)")
    print(f"{'═'*75}")
    print(f"  {'Partida':<32} {'Real':>5}  {'p(real)':>7}  {'Top':>5}  {'Brier':>5}  M1  M2")
    print(f"  {'─'*73}")
    for r in rows:
        m1 = "✓" if r["ok_score"] else "✗"
        m2 = "✓" if r["ok_prob"]  else "✗"
        print(f"  {r['match']:<32} {r['real']:>5}  {r['prob_score']:>7.3f}  "
              f"{r['top_score']:>5}  {r['brier']:>5.3f}   {m1}   {m2}")

    print(f"\n{'─'*75}")
    print(f"  MÉTRICAS GERAIS")
    print(f"{'─'*75}")
    print(f"  Probability Score   {mean_ps:.3f}  (baseline aleatório: {baseline_ps:.3f} | perfeito: 1.000)")
    print(f"  Brier Score         {mean_brier:.3f}  (baseline aleatório: {baseline_brier:.3f} | perfeito: 0.000)")
    print(f"  M1 — placar top     {acc_score:.0f}%  ({correct_score}/{n})")
    print(f"  M2 — maior prob     {acc_prob:.0f}%  ({correct_prob}/{n})")
    print(f"  Goal MAE            {goal_mae:.2f} gols/time/jogo")
    print(f"{'═'*75}\n")

    out = {
        "n_matches":         n,
        "probability_score": {"mean": round(mean_ps, 3), "baseline": round(baseline_ps, 3)},
        "brier_score":       {"mean": round(mean_brier, 3), "baseline": round(baseline_brier, 3)},
        "method1_score":     {"correct": correct_score, "total": n, "pct": round(acc_score, 1)},
        "method2_prob":      {"correct": correct_prob,  "total": n, "pct": round(acc_prob, 1)},
        "goal_mae":          round(goal_mae, 2),
        "matches":           rows,
    }

    os.makedirs("output", exist_ok=True)
    with open("output/model_eval.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, default=str)
    print(f"  Resultados salvos em output/model_eval.json")

if __name__ == "__main__":
    main()
