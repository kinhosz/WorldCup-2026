#!/usr/bin/env python3
"""
Simulação única e determinística da Copa do Mundo 2026.

Define uma seed para reprodutibilidade total, roda um torneio completo com
bracket detalhado e salva o relatório em output/JOGO_<seed>.md.
O campeão é revelado apenas no final do documento — sem spoilers.

Uso:
    python scripts/play_simulation.py <seed>
    python scripts/play_simulation.py 42
    python scripts/play_simulation.py 1000000
"""

import json
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trace_simulation import simulate_tournament_traced, format_trace


def build_report(seed, result, scores):
    lines = []

    lines.append(f"# 🌍 Copa do Mundo 2026 — Simulação #{seed}")
    lines.append("")
    lines.append(f"**Seed:** `{seed}`  ")
    lines.append("**Metodologia:** xG via atributos FIFA/FC25 · Distribuição de Poisson · Tempo extra (×0.35) · Pênaltis 50/50  ")
    lines.append("**Universo:** uma única linha do tempo determinística — toda vez que usar essa seed o resultado é idêntico.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(format_trace(result, scores))

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        sys.exit(
            "Uso: python scripts/play_simulation.py <seed>\n"
            "Exemplo: python scripts/play_simulation.py 42"
        )

    try:
        seed = int(sys.argv[1])
    except ValueError:
        sys.exit(f"Erro: seed deve ser um inteiro. Recebido: {sys.argv[1]!r}")

    scores_path = "output/team_scores.json"
    if not os.path.exists(scores_path):
        sys.exit(
            f"Erro: {scores_path} não encontrado — "
            "rode scripts/build_team_scores.py primeiro."
        )

    with open(scores_path, encoding="utf-8") as f:
        scores = json.load(f)

    random.seed(seed)
    np.random.seed(seed % (2**32))  # np.random.seed aceita apenas uint32

    print(f"Simulando Copa 2026 com seed={seed}...")
    result = simulate_tournament_traced(scores)

    report = build_report(seed, result, scores)

    os.makedirs("output", exist_ok=True)
    out_path = f"output/JOGO_{seed}.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nRelatório gerado: {out_path}")
    print("Abra o arquivo — o campeão está revelado apenas no final. Boa emoção!")


if __name__ == "__main__":
    main()
