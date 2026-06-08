# 2026 World Cup — Monte Carlo Simulation

**Date:** 2026-06-08 · **Simulations:** 1,000,000 · **Model:** FC25 + FIFA22 + Transfermarket cascade

---

## 1. What We Built

A complete 2026 World Cup simulator capable of playing a full tournament — group stage, Round of 32, Round of 16, quarterfinals, semifinals, and final — using real player data as the basis for each team's strength. The goal: estimate title probabilities for all 48 nations, accounting for the official FIFA bracket, the best-8 third-place rule, and the full knockout structure.

---

## 2. Data Pipeline

### 2.1 Score Sources

For each team we compute a score in four sectors: **goalkeeper**, **defense**, **midfield**, and **attack**. The source cascade:

| Tier | Source | Coverage |
|------|--------|----------|
| 1st | **FC25** — per-sector attributes (EA Sports FC 25) | ~17k players, highest priority |
| 2nd | **FIFA 22** — per-sector attributes | fallback for players absent from FC25 |
| 3rd | **Transfermarket** — market value converted to rating | supplementary |
| 4th | **Global sector median** — single fallback value | players with no data anywhere |

Market value to rating conversion (log-linear, anchored at €1M → 65 pts and €180M → 91 pts):
```
rating = 65 + (91 - 65) × (log(MV) - log(1M)) / (log(180M) - log(1M))   clipped to [45, 95]
```

### 2.2 Attributes per Sector

| Sector | FC25 / FIFA22 attributes used | Players kept |
|--------|------------------------------|--------------|
| Goalkeeper | diving, reflexes, handling, positioning | top 1 |
| Defense | defending, physic | top 4 |
| Midfield | passing, dribbling | top 4 |
| Attack | shooting, pace | top 3 |

For FC25 goalkeepers the column mapping is: `pac`=diving · `sho`=handling · `dri`=reflexes · `phy`=positioning.

### 2.3 Score Calculation

1. Collect all player ratings in a sector
2. Drop the bottom 30% (weakest players)
3. Compute the **log-mean** (geometric mean) of the remaining players
4. **Min-max normalize** across all 48 nations → final score in [0, 1]

A score of `1.0` means best in the tournament for that sector. All scores are relative — they have no absolute meaning on their own.

### 2.4 Name Matching

Names in squad files are matched to dataset entries using:
- `SequenceMatcher` string similarity ratio
- Token overlap bonus (word intersection / max set size)
- Nationality pool filter (only candidates from the same national pool)
- Suffix stripping (Junior, Sr, Jr)
- Minimum threshold of 0.72 — anything below is rejected

---

## 3. xG Formula

For a match **A vs B**, expected goals for each side:

```
offense_A    = 0.7 × attack_A    + 0.3 × midfield_A
resistance_B = 0.6 × defense_B  + 0.2 × goalkeeper_B + 0.2 × midfield_B

xG_A = 1.3 × (offense_A / resistance_B)
```

Safety constants:
- `BASE_XG = 1.3` — historical average goals per team per World Cup game
- `RES_FLOOR = 0.10` — resistance floor (avoids division by near-zero)
- `MAX_XG = 8.0` — expected goals ceiling

---

## 4. Tournament Structure

### Group Stage
- 12 groups of 4 teams (A–L), round-robin
- Points: win=3, draw=1, loss=0
- Advance: 1st and 2nd from each group (24 teams) + 8 best third-place finishers
- Goals simulated via Poisson distribution with the computed xG
- Tiebreakers: points → goal difference → goals scored → wins → random

### Knockout Stage
- **Round of 32** → Round of 16 → Quarterfinals → Semifinals → Final
- Official FIFA bracket (matches 73–104)
- Draw after 90 min → extra time (30 min, xG × 0.35) → penalty shootout (50/50)
- Third-place slot assignment via backtracking with official group eligibility constraints

---

## 5. Team Scores (top 20 by xG)

Scores are relative (min-max). `1.000` = best in the tournament for that sector.

| Team | xG vs avg | Attack | Midfield | Defense | Goalkeeper |
|------|-----------|--------|----------|---------|------------|
| Brazil | 2.344 | 0.960 | 0.763 | 0.967 | 1.000 |
| Portugal | 2.296 | 0.833 | 1.000 | 0.760 | 0.752 |
| Norway | 2.099 | 1.000 | 0.358 | 0.136 | 0.180 |
| France | 2.074 | 0.823 | 0.738 | 1.000 | 0.838 |
| England | 2.042 | 0.835 | 0.670 | 0.772 | 0.754 |
| Colombia | 1.945 | 0.900 | 0.395 | 0.597 | 0.597 |
| Netherlands | 1.893 | 0.795 | 0.572 | 0.949 | 0.278 |
| Spain | 1.891 | 0.675 | 0.851 | 0.626 | 0.848 |
| Argentina | 1.821 | 0.663 | 0.787 | 0.838 | 0.821 |
| Belgium | 1.798 | 0.625 | 0.846 | 0.392 | 0.541 |
| South Korea | 1.755 | 0.804 | 0.375 | 0.156 | 0.450 |
| Egypt | 1.743 | 0.873 | 0.198 | 0.135 | 0.524 |
| Congo | 1.653 | 0.833 | 0.176 | 0.470 | 0.190 |
| Morocco | 1.612 | 0.646 | 0.559 | 0.475 | 0.583 |
| Senegal | 1.554 | 0.735 | 0.278 | 0.475 | 0.681 |
| Germany | 1.540 | 0.564 | 0.658 | 0.733 | 0.817 |
| Ivory Coast | 1.474 | 0.625 | 0.431 | 0.516 | 0.362 |
| Sweden | 1.427 | 0.732 | 0.121 | 0.400 | 0.349 |
| Ghana | 1.272 | 0.573 | 0.295 | 0.214 | 0.344 |
| Switzerland | 1.205 | 0.483 | 0.418 | 0.588 | 0.639 |

---

## 6. Results — 1,000,000 Simulations

| # | Team | Group | Champion | Finalist | Semi | QF | R16 |
|---|------|-------|----------|----------|------|----|-----|
| 1 | Brazil | C | 20.8% | 32.0% | 48.0% | 68.1% | 84.0% |
| 2 | Portugal | K | 17.1% | 28.5% | 49.9% | 71.3% | 88.8% |
| 3 | France | I | 16.9% | 30.0% | 44.6% | 65.3% | 91.0% |
| 4 | England | L | 9.3% | 17.9% | 33.1% | 63.5% | 76.2% |
| 5 | Argentina | J | 8.2% | 15.8% | 31.9% | 55.6% | 66.7% |
| 6 | Netherlands | F | 7.0% | 15.6% | 26.8% | 51.8% | 61.8% |
| 7 | Spain | H | 7.0% | 15.4% | 32.0% | 47.4% | 73.7% |
| 8 | Colombia | K | 3.5% | 9.4% | 23.7% | 41.9% | 68.3% |
| 9 | Germany | E | 3.2% | 8.2% | 16.6% | 31.8% | 75.8% |
| 10 | Belgium | G | 2.6% | 8.6% | 24.3% | 58.7% | 82.6% |
| 11 | Morocco | C | 1.1% | 3.9% | 10.0% | 28.8% | 44.0% |
| 12 | Uruguay | H | 0.9% | 3.0% | 9.8% | 24.6% | 43.5% |
| 13 | Switzerland | B | 0.6% | 2.0% | 7.8% | 21.1% | 74.4% |
| 14 | Senegal | I | 0.6% | 2.2% | 6.8% | 18.2% | 55.4% |
| 15 | Ivory Coast | E | 0.4% | 1.6% | 5.4% | 15.5% | 57.0% |
| 16 | Croatia | L | 0.2% | 1.1% | 4.3% | 11.9% | 28.6% |
| 17 | Turkey | D | 0.2% | 1.1% | 4.8% | 18.5% | 55.1% |
| 18 | Czech Republic | A | 0.1% | 0.8% | 3.4% | 15.4% | 57.6% |
| 19 | Congo | K | 0.1% | 0.7% | 3.4% | 12.2% | 26.1% |
| 20 | Japan | F | 0.1% | 0.6% | 2.2% | 8.5% | 23.2% |
| 21 | USA | D | 0.0% | 0.3% | 2.3% | 13.0% | 50.3% |
| 22 | Austria | J | 0.0% | 0.2% | 1.4% | 5.7% | 19.0% |
| 23 | Sweden | F | 0.0% | 0.2% | 1.2% | 5.7% | 19.5% |
| 24 | Algeria | J | 0.0% | 0.2% | 1.2% | 5.4% | 18.6% |
| 25 | South Korea | A | 0.0% | 0.2% | 1.4% | 10.5% | 58.4% |
| 26 | Egypt | G | 0.0% | 0.1% | 1.3% | 10.2% | 52.2% |
| 27 | Mexico | A | 0.0% | 0.1% | 0.6% | 4.9% | 27.6% |
| 28 | Australia | D | 0.0% | 0.0% | 0.1% | 1.2% | 11.8% |
| 29 | Bosnia-Herzegovina | B | 0.0% | 0.0% | 0.0% | 0.1% | 5.2% |
| 30 | Canada | B | 0.0% | 0.0% | 0.0% | 0.0% | 1.4% |
| 31 | Cape Verde | H | 0.0% | 0.0% | 0.0% | 0.6% | 4.9% |
| 32 | Curaçao | E | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 33 | Ecuador | E | 0.0% | 0.1% | 0.5% | 3.9% | 24.2% |
| 34 | Ghana | L | 0.0% | 0.0% | 0.2% | 1.1% | 4.8% |
| 35 | Haiti | C | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| 36 | Iran | G | 0.0% | 0.0% | 0.0% | 0.2% | 5.6% |
| 37 | Iraq | I | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% |
| 38 | Jordan | J | 0.0% | 0.0% | 0.0% | 0.2% | 2.0% |
| 39 | New Zealand | G | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 40 | Norway | I | 0.0% | 0.0% | 0.4% | 3.1% | 19.3% |
| 41 | Panama | L | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% |
| 42 | Paraguay | D | 0.0% | 0.0% | 0.0% | 0.1% | 1.4% |
| 43 | Qatar | B | 0.0% | 0.0% | 0.0% | 0.9% | 17.6% |
| 44 | Saudi Arabia | H | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 45 | Scotland | C | 0.0% | 0.0% | 0.3% | 2.7% | 14.6% |
| 46 | South Africa | A | 0.0% | 0.0% | 0.0% | 0.4% | 6.5% |
| 47 | Tunisia | F | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% |
| 48 | Uzbekistan | K | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |

---

## 7. Group Stage Advancement Odds (R32)

| Group | 1st | 2nd | 3rd (best) | 4th |
|-------|-----|-----|-----------|-----|
| A | South Korea 92% | Czech Republic 90% | Mexico 65% | South Africa 26% |
| B | Switzerland 100% | Qatar 81% | Bosnia-Herzegovina 49% | Canada 26% |
| C | Brazil 100% | Morocco 98% | Scotland 59% | Haiti 2% |
| D | Turkey 93% | USA 93% | Australia 63% | Paraguay 22% |
| E | Germany 100% | Ivory Coast 100% | Ecuador 85% | Curaçao 0% |
| F | Netherlands 100% | Japan 87% | Sweden 85% | Tunisia 6% |
| G | Belgium 100% | Egypt 99% | Iran 51% | New Zealand 1% |
| H | Spain 100% | Uruguay 100% | Cape Verde 58% | Saudi Arabia 1% |
| I | France 100% | Senegal 96% | Norway 65% | Iraq 2% |
| J | Argentina 100% | Algeria 76% | Austria 72% | Jordan 20% |
| K | Portugal 100% | Colombia 98% | Congo 79% | Uzbekistan 2% |
| L | England 100% | Croatia 90% | Ghana 58% | Panama 14% |

---

For the full methodology, data quality audit, and team-by-team analysis: [ANALYSIS.md](ANALYSIS.md)
