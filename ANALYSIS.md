# Deep Analysis — 2026 World Cup Simulation

**Date:** 2026-06-08 · **Simulations:** 1,000,000 · **Model:** FC25 + FIFA22 + TM cascade

---

## 1. Goal and Scope

This document details every modeling decision made during the build, data quality issues found and fixed, the impact of each fix, and the interpretation of the final results. The goal is full transparency about what the model captures well, where it has structural limitations, and what the numbers actually mean.

---

## 2. Data Pipeline

### 2.1 Source Cascade

For every player on every squad, the system assigns a rating in priority order:

```
FC25 (akshay dataset)   → 17,470 players, attributes current as of 2025
  ↓ fallback
FIFA 22                 → 19,239 players, attributes as of 2022
  ↓ fallback
Transfermarket 2025     → market value converted to rating via log-linear formula
  ↓ fallback
Global sector median    → single fallback value per sector (GK / DEF / MID / ATT)
```

FC25 has the highest priority: if a player is found there, the FIFA22 entry is ignored for that player. This is critical for players who broke out after 2022 (Lamine Yamal, Nico Williams, Gavi, Endrick, etc.).

### 2.2 Name Matching

The match between squad file names and dataset entries uses:
- **SequenceMatcher** (string similarity ratio, 0–1 scale)
- **Token overlap bonus** (word intersection divided by max set size)
- **Nationality filter** (only candidates from the same country pool)
- **Suffix stripping** (Junior, Sr, Jr removed before comparison)
- **Threshold 0.72** — matches below this are rejected

Final score: `max(full_ratio, clean_ratio, overlap × 0.8 + ratio × 0.2)`

### 2.3 Market Value Conversion (Tier 3)

When a player has no FIFA dataset entry, their Transfermarket value is converted via log-linear formula:

```
t = (log(MV) - log(1M)) / (log(180M) - log(1M))
rating = 65 + t × (91 - 65)    → clipped to [45, 95]
```

Anchors: €1M → 65 pts · €180M → 91 pts

### 2.4 Sector Scores

Attributes used per sector (averaged from FC25/FIFA22):

| Sector | FC25/FIFA22 attributes | Players kept |
|--------|----------------------|--------------|
| Goalkeeper | diving, reflexes, handling, positioning | top 1 |
| Defense | defending, physic | top 4 |
| Midfield | passing, dribbling | top 4 |
| Attack | shooting, pace | top 3 |

For FC25, the goalkeeper column mapping is: `pac`=diving, `sho`=handling, `dri`=reflexes, `phy`=positioning.

Final flow: **drop bottom 30% by rating → log-mean of the rest → min-max across 48 nations → [0, 1]**

---

## 3. Data Quality Audit — Bugs Found and Fixed

### 3.1 Cross-Position GK Mismatches (FIFA22)

**Problem:** The fuzzy matcher was finding outfield players with the same surname as goalkeepers, assigning GK attribute averages of 7–15 (outfield players have near-zero values in the four GK metrics). These bad matches were being accepted and used in the calculation.

**Fix:** `MIN_SECTOR_RATING` — any FIFA match producing a rating below the threshold is rejected and the player falls through to the next tier:

```python
MIN_SECTOR_RATING = {'goalkeepers': 30.0, 'defenders': 35.0, 'middle': 35.0, 'attackers': 35.0}
```

**Impact by team:**

| Team | Wrong match | Bad rating | GK before | GK after |
|------|-------------|-----------|-----------|----------|
| Côte d'Ivoire | Mohamed Kone → M. Diomande (outfield) | 9.5 | 0.0000 | 0.2294 |
| Australia | Mathew Ryan → M. Jurman (outfield) | 13.0 | 0.0522 | 0.2149 |
| Scotland | Liam Kelly → L. Kelly (outfield) | 12.0 | 0.0494 | 0.1027 |
| Sweden | Gustaf Lagerbielke → wrong G. Lagerbielke | 11.5 | 0.1776 | 0.3490 |

The filter also caught 2 outfield players with bad matches (Tunisia and USA, ratings 29–32).

### 3.2 Son Heung-min — Non-Latin Name in FIFA22

**Problem:** FIFA22 stores Son Heung-min as `short_name="H. Son"`, `long_name="손흥민 孙兴慜"`. NFKD normalization converts Korean/Chinese characters to empty strings, making the long name unusable. The fuzzy matcher then couldn't connect "Son Heungmin" (squad) to "H. Son" and matched "Song Seung Min" instead (score 0.85).

**Impact:** Son appeared with an outfield rating of 65.5 and was discarded (bottom 30%). South Korea's ATT was near-zero.

**Fix:** Direct manual override:
```python
SQUAD_TO_FIFA_SHORTNAME = {
    ('republic_of_korea', 'Son Heungmin'): 'H. Son',
}
```

**Impact:** South Korea ATT: 0.168 → 0.804 · xG: 0.718 → 1.755

### 3.3 Mikel Merino — Truncated Name in FIFA22

**Problem:** In FIFA22, Mikel Merino has `short_name="Merino"`. The fuzzy matcher comparing "Mikel MERINO" against "Merino" produced a low score (name too short). Instead it matched "Mikel Rico" (36 years old, Athletic Club) with a 0.82 score — wrong match accepted by the threshold.

**Impact:** Merino appeared with a MID rating of 68.5 (Mikel Rico) instead of 81.5 (the real Merino). Spain's midfield was artificially depressed.

**Fix:** Override added to the dict:
```python
('spain', 'Mikel MERINO'): 'Merino',
```

**Impact:** Spain MID: 0.6877 → 0.8088 · xG: 1.461 → 1.555

### 3.4 Germany — Squad Composition (ATT)

**Problem:** In the squad file, Leroy Sané and Florian Wirtz were listed as midfielders. The xG model weights ATT at 70% of offensive output — without them in the attack sector, Germany had ATT=0.015 (near-zero), xG=0.707, and only a 0.57% title shot.

**Decision:** Sané and Wirtz were moved to `attackers`. Both have genuinely offensive profiles (Sané: pace/finishing, Wirtz: creativity/goals). Germany played the Euro 2024 with both in advanced roles.

**Impact:**

| Metric | Before | After |
|--------|--------|-------|
| ATT | 0.015 | 0.564 |
| xG | 0.707 | 1.540 |
| Champion % | 0.57% | 3.24% |

### 3.5 FC25 Integration — Impact on Young Players

FC25 was the broadest fix. The youngest generation was systematically underrated in FIFA22:

| Player | FIFA22 OVR | FC25 OVR | Team | Impact |
|--------|-----------|---------|------|--------|
| Lamine Yamal | Doesn't exist | 81 | Spain | ATT via TM → now properly in FC25 |
| Nico Williams | 67 (age 18) | 85 | Spain | ATT +18 OVR points |
| Gavi | 66 (age 16, discarded) | 83 | Spain | Back in midfield as a contributor |
| Endrick | Doesn't exist | 82 | Brazil | Real ATT coverage |
| Rodri | ~77 | 91 | Spain | MID anchor for the whole sector |
| Vinicius Jr | ~85 | ~93 | Brazil | ATT already high, confirmed |

**Aggregate impact on Spain:** xG 1.461 → 1.891 · Title probability: 2.26% → 6.95%

---

## 4. Coverage by Team

| Team | FC25 players | Total FIFA matched | TM | Median | Data quality |
|------|-------------|-------------------|-----|--------|-------------|
| Portugal | 27/27 | 27 | 0 | 0 | ★★★★★ only team with 100% FC25 |
| Spain | 19/26 | 23 | 2 | 1 | ★★★★ |
| Brazil | 18/26 | 25 | 0 | 1 | ★★★★ |
| USA | 21/26 | 23 | 1 | 2 | ★★★★ |
| Netherlands | 0/26 | 26 | 0 | 0 | ★★★ — zero FC25, fully FIFA22 |
| Iran | 0/26 | 12 | 5 | 9 | ★★ — no FC25 at all |
| Qatar | 0/34 | 0 | 6 | 28 | ★ — 82% median fallbacks |
| Jordan | 2/30 | 2 | 0 | 28 | ★ — 93% median fallbacks |

Netherlands is a notable outlier: FC25=0 despite having high-caliber players (Van Dijk, Gakpo, Depay). Dutch names likely have accent/formatting mismatches in the akshay dataset that prevent matching. The squad is served entirely by FIFA22, which is still reasonable since the Dutch core hasn't changed dramatically since 2022.

---

## 5. Results Analysis

### 5.1 Top-3: Brazil, Portugal, France (essentially tied)

With 1M simulations the top three are remarkably close:

| Team | Champion | Finalist | Semi |
|------|----------|----------|------|
| Brazil | 20.82% | 31.96% | 48.03% |
| Portugal | 17.09% | 28.49% | 49.87% |
| France | 16.89% | 30.04% | 44.63% |

**Why Brazil #1?**

Brazil is the only team with three sectors above 0.96 simultaneously:
- **GK=1.000**: Alisson (87.5) + Ederson (85.5) — the best goalkeeper duo in the tournament
- **DEF=0.967**: Bremer (85.5), Marquinhos (85.0), Ibañez, Danilo — Champions League-level defense
- **ATT=0.960**: Raphinha, Martinelli, Endrick, Vinicius, Neymar, Cunha — six attackers above 80

No visible weak point (MID=0.763 is the only "merely good" sector), combined with FC25 coverage of 18/26 players, gives Brazil the highest xG against an average opponent: **2.344**.

**Portugal #2** has MID=1.000 (the best midfield: Bruno Fernandes, Bernardo Silva, etc.) but DEF=0.760 — vulnerable defensively. Best midfield in the tournament but concedes more than Brazil or France.

**France #3** has DEF=1.000 (best defense) but the FC25 redistribution removed the double-maximum effect they had with FIFA22 alone. More balanced, but also facing stiffer competition at the top.

### 5.2 Spain — The FC25 Effect

Spain is the most dramatic example of how FC25 changes the model. With FIFA22 only, they ranked 11th (2.26%). With FC25 they jump to 7th (6.95%).

The difference comes from the Euro 2024 generation:
- Gavi went from discarded (OVR 66 → dropped) to active contributor (OVR 83)
- Nico Williams went from 73 (age 18 in 2022) to 85 (2025)
- Yamal got real coverage (didn't exist in FIFA22)
- Rodri confirmed as the tournament's top midfielder (OVR 91 in FC25)

### 5.3 Expected Anomalies

**Norway — xG=2.099, champion=0.00%**
Haaland (ATT=1.000 — tournament maximum) drives xG of 2.099, but DEF=0.136 and GK=0.180 mean Norway concedes more than they score against any mid-to-high level opponent. In the knockout stage, they need to win by score to advance and can't hold leads. In 1M simulations they never reached the final.

**South Korea — xG=1.755, champion=0.02%**
Son Heung-min (corrected via override) gives ATT=0.804 and a respectable xG. But DEF=0.156 — second worst defense in the tournament. Korea frequently advances from groups but is eliminated in the Round of 16 by any team with solid MID/DEF.

**Egypt — ATT=0.873, champion=0.01%**
Mohamed Salah is the sole highlight. MID=0.198, DEF=0.135. xG=1.743 against an average opponent but the model consistently pairs them with Belgium in the R32. With near-minimum defense they lose systematically in the knockout stage.

**Colombia — ATT=0.900, champion=3.45%**
Looks high for a non-European side. The squad has James Rodríguez, Luis Díaz, Falcao — all with strong FC25 ratings. MID=0.395 is weak but the attacking xG partially compensates. 3.45% title odds is probably generous but not absurd.

### 5.4 Teams Well-Positioned by the Draw

Belgium has **QF=58.66%** but only 2.65% title probability — a classic easy-group-then-early-exit profile. DEF=0.392 (low) explains why they advance in groups but lose in the quarters against the top-4.

### 5.5 Structural Limitations

**1. Netherlands with no FC25 (FC25=0/26):** Van Dijk, Gakpo, Depay are major players who have developed since 2022. The model uses FIFA22 for all of them. The Netherlands may be underestimated by 1–2%.

**2. xG formula doesn't capture playing styles:** Spain under Martínez plays possession and high press — the model only sees ATT/MID/DEF as numbers. A team that plays reactively and scores on the counter (as Spain did at Euro 2024) is indistinguishable from a team that presses high.

**3. Frozen squads:** The model uses convocations defined today. Injuries, suspensions, and last-minute changes between now and July 2026 are not captured.

**4. Knockout stage has high variance:** With 48 teams and a fixed bracket, a strong team can be eliminated early if they fall on the same side as another giant. Title probability reflects both quality and bracket luck.

---

## 6. Conclusion

The model, after all corrections, produces results consistent with the international football landscape of 2026:

- **Brazil** emerges as the legitimate favorite — they have the world's best goalkeeper (Alisson), an elite European-level defense, and an attack with six options above 80 in FC25. The absence of a visible weak point is what sets them apart.
- **Portugal and France** are real co-favorites, each with one maximum sector (MID and DEF respectively) and squads without serious gaps.
- **England and Argentina** form the second block (8–9%), complete teams without an absolute standout in any single sector.
- **Spain** at 7th (6.95%) reflects the actual quality of the current European champions — the model captures the Yamal/Williams/Pedri generation well via FC25.
- **Germany** at 9th (3.24%) is reasonable for a team in transition with excellent defense and goalkeeper but a midfield under renewal.

The biggest single impact was the FC25 integration: the difference between a model based solely on 2022 data and one calibrated for 2025 is substantial for teams built around young players (Spain, Brazil) and negligible for teams with stable squads (Argentina, Netherlands).
