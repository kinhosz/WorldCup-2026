# Instagram Post — Semifinais (estilo "Troféu Chegando")

Mesmo estilo visual das quartas (aprovado 08 jul 2026), agora na Semifinal. Texto sempre em inglês. Formato 4:5, 1080×1350. Dados de `output/odds_france_vs_spain.json`, `output/odds_england_vs_argentina.json` (Model6, `--knockout`) e `output/simulation_results_model6.json` (10M simulações, 4 semifinalistas). Model6 **não foi recalibrado** com os resultados das quartas — decisão consciente do usuário pra manter o teste out-of-sample real das quartas em diante (ver CLAUDE.md).

**Bracket confirmado:** SF1 = França x Espanha (W97 x W99), SF2 = Inglaterra x Argentina (W98 x W100).

**Bug encontrado e corrigido (14 jul 2026):** o `KNOCKOUT_SCHEDULE` em `resultado.py` tinha os pares da semifinal errados (`101: W97×W98`, `102: W99×W100` — França x Inglaterra e Espanha x Argentina), inconsistente com o `SEMIFINALS` de `simulate.py` (`(101, 97, 99)`, `(102, 98, 100)` — o array que a simulação de verdade usa). Mesma classe de bug que já tinha acontecido no R16. Corrigido em `resultado.py`; o `simulate.py` já estava certo, então a simulação de 10M não precisou ser refeita.

**Ordem do carrossel:** Hook (0) · Report Card das quartas (1) · Title Odds (2, 4 times) · O que o modelo aprendeu (2b, 4 times num slide só) · França x Espanha (3) · Inglaterra x Argentina (4).

**Paleta e identidade:** idêntica às quartas — preto quente `#14110C`, cards bronze `#201A12`, accent dourado `#E3B341`, tag de rodada oxblood `#7A2E2E`, "PATH TO THE FINAL" agora com QF completo (dourado sólido) e SF ativo (dourado com glow), FINAL ainda oco/cinza.

---

## SLIDE 0 — Hook

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the title and team names (evoking an engraved trophy plaque), clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light and gold confetti/pyro haze in the crowd. Apply a warm near-black overlay at 80% opacity on top of the whole scene (color #14110C) so it reads as rich and prestigious behind the UI, not distracting.

Large bold serif display title, centered near the top, metallic gold color #E3B341 with a soft warm glow, two lines, huge and bold: "SEMIFINALS" on the first line, "FIFA WORLD CUP 2026" smaller on the second line.

Below the title, a thin horizontal progress line representing the path to the final, with 3 small circular nodes evenly spaced left to right, each with a label below: "QF" (filled solid gold, completed stage, no glow), "SF" (filled solid gold WITH a soft glow, this is the active stage), "FINAL" (hollow outline, muted grey) — connect the nodes with a thin line, solid gold from QF through SF and muted grey afterward. Small caps micro-label above the line, wide letter-spacing, color #A99B7D, reading exactly: "PATH TO THE FINAL"

Below that, two rows stacked vertically and evenly spaced, each row has a shield-shaped crest (rounded-bottom heraldic shield outline, dark bronze-brown #201A12 fill, thin gold border, drop shadow) filled edge-to-edge with the left team's flag design, bold gold "VS" centered between the two shields, then a matching shield filled with the right team's flag design, team names in serif bold white caps below each shield.

ROW 1: LEFT SHIELD — France flag (vertical blue-white-red bands). Name below: FRANCE. RIGHT SHIELD — Spain flag (horizontal red-yellow-red bands, wider yellow band with a coat of arms on the left side). Name below: SPAIN.

ROW 2: LEFT SHIELD — England flag (white field with a red St George's cross — a simple red plus-sign cross on white, NOT the Union Jack, NOT a black flag). Name below: ENGLAND. RIGHT SHIELD — Argentina flag (horizontal light-blue-white-light-blue bands with a golden sun face centered in the white band). Name below: ARGENTINA.

Caption below the rows, small caps, wide letter-spacing, color #E3B341, centered, reading exactly: "ROUND OF 4 · FIFA WORLD CUP 2026"
```

---

## SLIDE 1 — Como o modelo se saiu nas quartas (Model6, primeiro teste out-of-sample)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline, clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light. Apply a warm near-black overlay at 82% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the top, rotated slightly, deep oxblood-red background #7A2E2E, white bold text reading exactly: "MODEL REPORT CARD"

Serif display headline below, white, bold, reading exactly: "How the model did in the Quarterfinals"

Small caps label, wide letter-spacing, color #A99B7D, reading exactly: "MODEL6 · 4 GAMES · FIRST TRUE OUT-OF-SAMPLE TEST"

Four stat cards in a 2x2 grid (background #201A12, thin gold border #4A3A22), each with a large bold gold number and a small muted caption below:
CARD 1: "3/4" big number, caption below: "Who advances — correct (75%)"
CARD 2: "1/1" big number, caption below: "Accuracy above 70% confidence (100%)"
CARD 3: "2/4" big number, caption below: "Exact scoreline in the model's top 3"
CARD 4: "2/4" big number, caption below: "Derived bet (over/under, both teams score) correct"

Insight card below the grid (color #C9BBA0 text, dark warm card background #201A12, thin gold left border), reading exactly: "The only miss: Argentina vs Switzerland was a near coin flip, 51.0% Switzerland to 49.0% Argentina — and the underdog side won, even though the model's top-scoring guess, 1-1, was exactly right after 90 minutes."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches, frozen since the Round of 16 — no recalibration after the Quarterfinals"
```

---

## SLIDE 2 — Probabilidade de ser campeão (Model6, 4 semifinalistas)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names, clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light, a single trophy silhouette faintly visible and out of focus in the deep background. Apply a warm near-black overlay at 84% opacity on top of the whole scene (color #14110C) so it reads as moody and prestigious behind the UI.

Small ribbon/tag near the top, rotated slightly, metallic gold background #E3B341, dark bold text reading exactly: "TITLE ODDS"

Serif display headline below, white, bold, reading exactly: "Who's most likely to lift the trophy"

Small caps label, wide letter-spacing, color #A99B7D, reading exactly: "MODEL6 · 10,000,000 SIMULATIONS · 4 TEAMS REMAINING"

A ranked list of 4 rows, each row: rank number in a small gold circle, a small rectangular national flag icon, team name in serif font (white bold) right next to the flag, a horizontal bar filling proportionally to the team's percentage (gold #E3B341 with soft glow for rank 1, muted graphite #6B7280 for the rest), and the percentage in bold gold tabular numbers at the right edge of each row.

ROW 1: "1" — small flag icon: Spain flag (horizontal red-yellow-red bands, wider yellow band with a coat of arms on the left side) — Spain — bar 41.44% (longest bar, gold, glowing) — "41.4%"
ROW 2: "2" — small flag icon: England flag (white field with a red St George's cross — a simple red plus-sign cross on white, NOT the Union Jack, NOT a black flag) — England — bar 27.36% — "27.4%"
ROW 3: "3" — small flag icon: France flag (vertical blue-white-red bands) — France — bar 22.67% — "22.7%"
ROW 4: "4" — small flag icon: Argentina flag (horizontal light-blue-white-light-blue bands with a golden sun face centered in the white band) — Argentina — bar 8.54% — "8.5%"

Insight card below the list (color #C9BBA0 text, dark warm card background #201A12, thin gold left border), reading exactly: "Spain's title odds climbed from 35.3% to 41.4% now that the field is down to four — largely on the back of a 60.5% chance of getting past France in the semifinal."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches · 10,000,000 simulations"
```

---

## SLIDE 2b — O que o modelo aprendeu (os 4 semifinalistas)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names, clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light. Apply a warm near-black overlay at 86% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the top, rotated slightly, metallic gold background #E3B341, dark bold text reading exactly: "MODEL INSIGHT"

Serif display headline below, white, bold, reading exactly: "What the model actually learned"

Small caps label, wide letter-spacing, color #A99B7D, reading exactly: "THE FOUR SEMIFINALISTS"

Four compact stacked rows (background #201A12, thin gold border #4A3A22), each row: a small national flag icon + team name in serif bold white on the left, two small bold stat chips "ATT" and "DEF" with their numbers, and a single line of real-data commentary in color #C9BBA0 below the name.

ROW 1: flag icon (France flag: vertical blue-white-red bands) + "FRANCE" — chips "ATT 0.87" (neutral grey chip, below-average discount) / "DEF 1.00" (neutral grey chip) — commentary: "16 goals scored across 6 games, but only 2 conceded — the tightest defense of the four, including back-to-back 1-0 and 2-0 knockout wins over Paraguay and Morocco."

ROW 2: flag icon (Spain flag: horizontal red-yellow-red bands, wider yellow band with a coat of arms on the left side) + "SPAIN" — chips "ATT 1.14" (gold-tinted chip, background #E3B341 dark text) / "DEF 1.16" (gold-tinted chip, background #E3B341 dark text — the best pair of ratings of the four) — commentary: "Conceded only once in 6 games, while scoring more goals than any other team left — 11 in total."

ROW 3: flag icon (England flag: white field with a red St George's cross — a simple red plus-sign cross on white, NOT the Union Jack, NOT a black flag) + "ENGLAND" — chips "ATT 0.94" (neutral grey chip) / "DEF 1.00" (neutral grey chip) — commentary: "12 goals scored, but conceded in every knockout game so far — needed extra time to beat Norway 2-1 after a 1-1 draw in regulation."

ROW 4: flag icon (Argentina flag: horizontal light-blue-white-light-blue bands with a golden sun face centered in the white band) + "ARGENTINA" — chips "ATT 1.01" (neutral grey chip) / "DEF 0.55" (red-tinted chip, background #7A2E2E white text — the lowest defense rating of the four) — commentary: "Needed extra time in two of its three knockout wins so far — 3-2 over Cape Verde in the Round of 32 and 3-1 over Switzerland in the Quarterfinal, both after 1-1 draws in regulation."

Footer card at the bottom (color #C9BBA0 text, dark warm card background, thin gold left border), reading exactly: "These bias numbers are frozen since the Round of 16 — the model has not updated them with any Quarterfinal result yet."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches"
```

---

## SLIDE 3 — França x Espanha

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names (evoking an engraved trophy plaque), clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light spilling across the pitch (not cool blue/white light). On the left third of the image, an illustrated football player in a France kit (blue shirt, white shorts), mid-action celebration pose, face generic/stylized (not a specific real athlete's likeness). On the right third, an illustrated football player in a Spain kit (red shirt, blue shorts), mid-action pose facing toward the center, also generic/no specific likeness. Both figures partially faded into the dark stadium background. Apply a warm near-black overlay at 80% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the very top, rotated slightly, deep oxblood-red background #7A2E2E, white bold text reading exactly: "SEMIFINALS"

Text label below the ribbon, small caps, wide letter-spacing, color #E3B341, reading exactly: "FIFA WORLD CUP 2026"

Below that, a thin horizontal progress line with 3 small circular nodes evenly spaced, labeled below: "QF" (filled solid gold, completed), "SF" (filled solid gold with a soft glow, active), "FINAL" (hollow grey), connected by a thin line, solid gold through the SF node and muted grey afterward. Small caps micro-label above, color #A99B7D, reading exactly: "PATH TO THE FINAL"

Below that, two generic shield-shaped crests (rounded-bottom heraldic shield outline, dark bronze-brown #201A12 fill, thin gold border, strong drop shadow) side by side, each shield filled edge-to-edge with the team's actual flag design. A warm gold radial spotlight glow directly behind the pair of shields, centered on the "VS". Between the two shields, large bold serif text reading exactly "VS" with a subtle gold glow. Below each shield, the team name in an elegant serif display font, white bold caps.
LEFT SHIELD: France flag (vertical blue-white-red bands). Name below: FRANCE
RIGHT SHIELD: Spain flag (horizontal red-yellow-red bands, wider yellow band with a coat of arms on the left side). Name below: SPAIN

Cards below (background #201A12, border #4A3A22, semi-opaque so the stadium photo behind is still faintly visible) contain the following, stacked vertically:

A line of centered white medium text reading exactly: "xG 1.01 · · · 1.45 xG"

Small caps label above the bar, muted #A99B7D, wide letter-spacing, reading exactly: "WHO ADVANCES"
Probability bar — single rounded pill, TWO segments only, with the percentage written in bold text directly inside each colored segment:
LEFT segment: muted graphite #6B7280, no glow, with "39.5%" in bold white text centered inside the segment.
RIGHT segment: metallic gold #E3B341 with a soft glow, with "60.5%" in bold dark text centered inside the segment.
Team name labels below the bar (names only, percentages already shown inside the bar): "France      Spain"

(no confidence pill for this game — 60.5% falls short of the 70% threshold)

Model's pick badge (dark pill background #201A12, gold border #E3B341) reading exactly: "MODEL'S PICK · Under 2.5 goals · 55.7%"

Small caps label "TOP SCORES" followed by 3 chips inline (dark #201A12 background, thin gold border, white bold text): "1–1  12.6%   0–1  12.5%   1–2  9.0%"

Insight card (color #C9BBA0 text, dark warm card background) reading exactly: "Spain's defense drags France's expected goals down to 1.01 — the lowest of any team in either semifinal — while carrying a 36.6% chance of a clean sheet, extending a run of conceding just once in its last 6 games."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches · 1,000,000 simulations"
```

---

## SLIDE 4 — Inglaterra x Argentina

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names (evoking an engraved trophy plaque), clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light spilling across the pitch. On the left third of the image, an illustrated football player in an England kit (white shirt, navy shorts), mid-action celebration pose, face generic/stylized (not a specific real athlete's likeness). On the right third, an illustrated football player in an Argentina kit (light-blue and white striped shirt, black shorts), mid-action pose facing toward the center, also generic/no specific likeness. Both figures partially faded into the dark stadium background. Apply a warm near-black overlay at 80% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the very top, rotated slightly, deep oxblood-red background #7A2E2E, white bold text reading exactly: "SEMIFINALS"

Text label below the ribbon, small caps, wide letter-spacing, color #E3B341, reading exactly: "FIFA WORLD CUP 2026"

Below that, a thin horizontal progress line with 3 small circular nodes evenly spaced, labeled below: "QF" (filled solid gold, completed), "SF" (filled solid gold with a soft glow, active), "FINAL" (hollow grey), connected by a thin line, solid gold through the SF node and muted grey afterward. Small caps micro-label above, color #A99B7D, reading exactly: "PATH TO THE FINAL"

Below that, two generic shield-shaped crests (rounded-bottom heraldic shield outline, dark bronze-brown #201A12 fill, thin gold border, strong drop shadow) side by side, each shield filled edge-to-edge with the team's actual flag design. A warm gold radial spotlight glow directly behind the pair of shields, centered on the "VS". Between the two shields, large bold serif text reading exactly "VS" with a subtle gold glow. Below each shield, the team name in an elegant serif display font, white bold caps.
LEFT SHIELD: England flag (white field with a red St George's cross — a simple red plus-sign cross on white, NOT the Union Jack, NOT a black flag). Name below: ENGLAND
RIGHT SHIELD: Argentina flag (horizontal light-blue-white-light-blue bands with a golden sun face centered in the white band). Name below: ARGENTINA

Cards below (background #201A12, border #4A3A22, semi-opaque so the stadium photo behind is still faintly visible) contain the following, stacked vertically:

A line of centered white medium text reading exactly: "xG 2.20 · · · 1.38 xG"

Small caps label above the bar, muted #A99B7D, wide letter-spacing, reading exactly: "WHO ADVANCES"
Probability bar — single rounded pill, TWO segments only, with the percentage written in bold text directly inside each colored segment:
LEFT segment: metallic gold #E3B341 with a soft glow, with "66.3%" in bold dark text centered inside the segment.
RIGHT segment: muted graphite #6B7280, no glow, with "33.7%" in bold white text centered inside the segment.
Team name labels below the bar (names only, percentages already shown inside the bar): "England      Argentina"

(no confidence pill for this game — 66.3% falls just short of the 70% threshold)

Model's pick badge (dark pill background #201A12, gold border #E3B341) reading exactly: "MODEL'S PICK · Over 2.5 goals · 69.2%"

Small caps label "TOP SCORES" followed by 3 chips inline (dark #201A12 background, thin gold border, white bold text): "2–1  9.3%   1–1  8.5%   3–1  6.8%"

Insight card (color #C9BBA0 text, dark warm card background) reading exactly: "England is favored at 66.3% — just short of the model's high-confidence threshold — against an Argentina defense carrying the weakest rating of the four semifinalists, after needing extra time in two of its three knockout wins so far."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches · 1,000,000 simulations"
```
