# WorldCup 2026 — Monte Carlo Simulation

A Monte Carlo simulator for the 2026 FIFA World Cup: player attributes from FC25/FIFA22/Transfermarket become per-nation sector scores (GK/DEF/MID/ATT), which feed a Poisson xG model to simulate every match. Real results are tracked round by round and the model is recalibrated (Simulated Annealing) against them as the tournament progresses.

Followed the whole thing on Instagram? Welcome — this is where all the numbers behind the posts actually live.

---

## Where things stand

🏆 **Final: Spain vs Argentina** · 🥉 **3rd place: France vs England**

Model7 (the current, final calibration) gives Spain **86.5%** to lift the trophy against Argentina's **13.5%**, and France **70.9%** to take 3rd over England's **29.1%**. Full breakdown — xG, score probabilities, extra-time modeling — in `output/odds_spain_vs_argentina.json` and `output/odds_france_vs_england.json`.

**Interactive report** — every match played so far re-evaluated with Model7 (pick, confidence, top score, right/wrong), the two pending predictions, and all 48 nations ranked by score and calibrated bias:
👉 **https://kinhosz.github.io/WorldCup-2026/**

For the full story of how the model evolved (Model1 → Model7, every calibration decision and why) see [CLAUDE.md](CLAUDE.md) and [TASKS.md](TASKS.md) — this repo's real running log.

---

## How the model works

```
squads/*.json + player datasets
        │
        ▼
build_team_scores.py   →  output/team_scores.json      (GK/DEF/MID/ATT per nation, 0.1–1.0)
        │
        ▼
simulate.py             →  output/simulation_results.json   (Monte Carlo, N simulations)
match_odds.py            →  output/odds_{a}_vs_{b}.json      (odds for one specific match)
        │
        ▼
resultado.py             →  output/copa_real_state.json      (real results, entered as they happen)
        │
        ▼
calibrate_sa.py           →  output/calibrated_weights_sa.json  (Simulated Annealing recalibration)
```

**xG formula:**

```
offense_A    = OFF_ATT_W × attack_A  + OFF_MID_W × midfield_A
resistance_B = RES_DEF_W × defense_B + RES_GK_W  × goalkeeper_B + RES_MID_W × midfield_B

xG_A = min(BASE_XG × (offense_A × att_bias_A) / max(resistance_B × def_bias_B, 0.10), 8.0)
```

`att_bias`/`def_bias` are per-nation multipliers learned by Simulated Annealing from real results — they're how the model corrects itself when a squad's actual performance diverges from what raw player ratings predicted (see Argentina, Brazil, Spain in the interactive report above for the most dramatic examples).

Knockout matches: draws after 90' go to a modeled extra time (30min at 1/3 the 90'-xG rate), then penalties as a 50/50 coin flip if still level — except the 3rd-place match, which skips extra time entirely per FIFA rules.

---

## Tracking real results

```bash
python3 scripts/resultado.py --list          # all games and their IDs
python3 scripts/resultado.py --list r1       # filter: r1 r2 r3 r32 r16 qf sf final
python3 scripts/resultado.py                 # enter a result interactively by game ID
```

State persists in `output/copa_real_state.json` across runs — `Ctrl+C` any time to pause and resume later.

---

## Branch structure

Each branch snapshots the project at a specific tournament phase:

| Branch | Phase |
|--------|-------|
| `main` | Pre-tournament predictions (frozen) |
| `fase-grupos/rodada-2` | After Rodada 1 |
| `fase-grupos/rodada-3` | After Rodada 2 |
| `rodada-de-32` | After group stage closes |
| `oitavas-de-final` | After Round of 32 |
| `quartas-de-final` | After Round of 16 |
| `semifinal` | After Quarterfinals |
| `final` | After Semifinals — current |

---

## Running it yourself

```bash
python3 scripts/build_team_scores.py            # generates output/team_scores.json
python3 scripts/simulate.py 1000000              # runs 1M Monte Carlo simulations
python3 scripts/match_odds.py spain argentina 1000000 --knockout   # odds for one match
python3 scripts/full_evaluation.py               # regenerates the interactive report above
```
