# WorldCup 2026 — Monte Carlo Simulation

A complete 2026 FIFA World Cup simulator using FC25 and FIFA22 player attributes as strength proxies, Poisson-distributed xG to model matches, and Monte Carlo to estimate title probabilities across all 48 nations.

**Results (1,000,000 simulations):** Brazil 20.8% · Portugal 17.1% · France 16.9% · England 9.3% · Argentina 8.2%

---

## Documents

| Document | Language | Contents |
|----------|----------|----------|
| [SIMULATION.md](SIMULATION.md) | English | Methodology, scores, full results table, group-stage odds |
| [ANALYSIS.md](ANALYSIS.md) | English | Deep analysis: data quality bugs fixed, FC25 impact, team-by-team interpretation |
| [SIMULACAO.md](SIMULACAO.md) | Portuguese | Full methodology + individual simulation traces |
| [ANALISE.md](ANALISE.md) | Portuguese | Deep analysis (Portuguese version) |
| [output/score_audit.md](output/score_audit.md) | — | Per-player breakdown: data source and rating for all 48 squads |
| [output/megazord_report_en.md](output/megazord_report_en.md) | English | Megazord — consensus bracket: argmax predictions + advance probabilities |

---

## Megazord — Consensus Bracket

The Megazord is a single deterministic tournament built from the **most likely outcome at every stage**, derived from thousands of simulations rather than a single random draw.

**How it works:**

1. **Group stage — 50,000 simulations.** Each team's probability of finishing 1st, 2nd, 3rd, or 4th is computed across all runs, along with their probability of advancing to R32 (including the best-3rd-place rule across all 12 groups). Bracket positions are assigned by **greedy argmax**: the team most likely to finish 1st gets the 1st-place slot, the team most likely to finish 2nd among the remaining three gets 2nd, and so on.
2. **Knockout rounds — 10,000 sub-simulations per match.** Each knockout match is resolved independently: 10k head-to-head simulations determine the modal winner, who advances with their modal scoreline.
3. The result is a single, fully-determined bracket — not a single random seed, but the **statistically most likely path** through the entire tournament.

**Result:** Brazil beats France 1–0 in the final (54% win probability in that specific matchup).

```bash
python3 scripts/megazord.py          # runs 50k group sims (default)
python3 scripts/megazord.py 100000   # more sims, more stable modes
```

### Visual Bracket

| Stage | Image |
|-------|-------|
| Group Stage (A–F) | ![Group Stage 1](images/group_1.png) |
| Group Stage (G–L) | ![Group Stage 2](images/group_2.png) |
| Best Third-Place Qualifiers | ![Best 3rd](images/best_3.png) |
| Round of 32 | ![Round of 32](images/round_of_32.png) |
| Round of 16 | ![Round of 16](images/round_of_16.png) |
| Quarterfinals → Final | ![Quarters to Final](images/quarters_to_final.png) |

---

## How to Run

```bash
python3 scripts/build_team_scores.py   # generates output/team_scores.json
python3 scripts/simulate.py 100000     # runs 100k simulations
python3 scripts/generate_report.py     # regenerates SIMULACAO.md
```

---

## Data Pipeline

```
squads/*.json
    │
    ▼
build_team_scores.py
    │  Tier 1: FC25    (datasets/extracted/fc25_akshay/players_info.csv)
    │  Tier 2: FIFA22  (datasets/extracted/players_22.csv)
    │  Tier 3: Transfermarket market value → log-linear rating
    │  Tier 4: global sector median
    ▼
output/team_scores.json  →  simulate.py  →  output/simulation_results.json
```

---

## Results — 1,000,000 Simulations

| # | Team | Champion | Finalist | Semi | QF |
|---|------|----------|----------|------|----|
| 1 | Brazil | 20.82% | 31.96% | 48.03% | 68.09% |
| 2 | Portugal | 17.09% | 28.49% | 49.87% | 71.28% |
| 3 | France | 16.89% | 30.04% | 44.63% | 65.29% |
| 4 | England | 9.32% | 17.88% | 33.11% | 63.48% |
| 5 | Argentina | 8.18% | 15.79% | 31.93% | 55.64% |
| 6 | Netherlands | 7.00% | 15.56% | 26.80% | 51.82% |
| 7 | Spain | 6.95% | 15.45% | 32.05% | 47.38% |
| 8 | Colombia | 3.45% | 9.45% | 23.71% | 41.85% |
| 9 | Germany | 3.24% | 8.23% | 16.60% | 31.81% |
| 10 | Belgium | 2.65% | 8.63% | 24.26% | 58.66% |

Full 48-team table and group-stage odds: [SIMULATION.md](SIMULATION.md)

---

## Example Seeds

Each seed produces a fully deterministic tournament — run it again and you get the exact same bracket.

| Seed | Champion | Final | Output |
|------|----------|-------|--------|
| `2026` | Netherlands | Netherlands 3–1 England | [output/JOGO_2026.md](output/JOGO_2026.md) |
| `303` | Brazil | Brazil 2–1 France | [output/JOGO_303.md](output/JOGO_303.md) |

```bash
python3 scripts/play_simulation.py 2026   # Netherlands lifts the trophy
python3 scripts/play_simulation.py 303    # Brazil campeão
```
