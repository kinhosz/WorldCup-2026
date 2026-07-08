# Instagram Post — Quartas de Final (Novo estilo "Troféu Chegando")

Formato validado com Argentina x Suíça (aprovado pelo usuário em 08 jul 2026). Texto sempre em inglês. Formato 4:5, 1080×1350. Dados de `output/odds_*.json` (Model6, `--knockout`) e `output/simulation_results_model6.json` (10M simulações, campeão). Model5 é citado só no slide técnico (performance das oitavas, avaliado com o modelo daquela época).

**Ordem final do carrossel:** Hook (0) · Report Card oitavas (1) · Title Odds (2) · O que o modelo aprendeu 1/2 (2b, lado França-Marrocos/Espanha-Bélgica) · O que o modelo aprendeu 2/2 (2c, lado Noruega-Inglaterra/Argentina-Suíça) · França-Marrocos (3) · Espanha-Bélgica (4) · Noruega-Inglaterra (5) · Argentina-Suíça (6). Os slides 2b/2c nasceram de uma dúvida real do usuário sobre os bias de Argentina e França, e depois do pedido de cobrir os 8 times, não só 2 — cada linha cita um resultado real de `copa_real_state.json`, sem inventar nenhum dado.

**Nova identidade visual — Quartas em diante:** paleta esquenta de azul/verde neon (oitavas) pra **preto quente + dourado metálico** (tema "troféu chegando"), tipografia dos nomes/títulos vira serifada (efeito "placa gravada"), e entra o elemento "PATH TO THE FINAL" (QF → SF → Final) — só faz sentido a partir daqui porque o bracket completo até a final já é conhecido.

### Paleta e identidade — Quartas

- Fundo: preto quente `#14110C` (overlay 80% sobre foto de estádio com luz dourada, não azul/branca fria)
- Cards: bronze escuro `#201A12`, borda fina dourada `#4A3A22`
- Accent principal: dourado metálico `#E3B341`
- Accent secundário (tag de rodada): vermelho oxblood `#7A2E2E`
- Texto muted dentro dos cards: `#A99B7D` / `#C9BBA0`
- Segmento "não favorito" da barra: grafite `#6B7280`
- Tipografia: serifada de exibição pros nomes/título (efeito placa gravada), sans-serif geométrica limpa pros dados/labels, números tabulares

---

## SLIDE 0 — Hook (título do carrossel)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the title and team names (evoking an engraved trophy plaque), clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light and gold confetti/pyro haze in the crowd. Apply a warm near-black overlay at 80% opacity on top of the whole scene (color #14110C) so it reads as rich and prestigious behind the UI, not distracting.

Large bold serif display title, centered near the top, metallic gold color #E3B341 with a soft warm glow, two lines, huge and bold: "QUARTERFINALS" on the first line, "FIFA WORLD CUP 2026" smaller on the second line.

Below the title, a thin horizontal progress line representing the path to the final, with 3 small circular nodes evenly spaced left to right, each with a label below: "QF" (filled solid gold, this is the active stage), "SF" (hollow outline, muted grey), "FINAL" (hollow outline, muted grey) — connect the nodes with a thin line, gold up to the QF node and muted grey afterward. Small caps micro-label above the line, wide letter-spacing, color #A99B7D, reading exactly: "PATH TO THE FINAL"

Below that, four rows stacked vertically and evenly spaced, each row has a shield-shaped crest (rounded-bottom heraldic shield outline, dark bronze-brown #201A12 fill, thin gold border, drop shadow) filled edge-to-edge with the left team's flag design, bold gold "VS" centered between the two shields, then a matching shield filled with the right team's flag design, team names not needed below the shields.

ROW 1: LEFT SHIELD — France flag (vertical blue-white-red bands). RIGHT SHIELD — Morocco flag (red field, green five-pointed star outlined in the center).

ROW 2: LEFT SHIELD — Spain flag (horizontal red-yellow-red bands, wider yellow band with a coat of arms on the left side). RIGHT SHIELD — Belgium flag (vertical black-yellow-red bands).

ROW 3: LEFT SHIELD — Norway flag (red field with a blue-and-white Nordic cross). RIGHT SHIELD — England flag (white field with a red St George's cross — a simple red plus-sign cross on white, NOT the Union Jack, NOT a black flag).

ROW 4: LEFT SHIELD — Argentina flag (horizontal light-blue-white-light-blue bands with a golden sun face centered in the white band). RIGHT SHIELD — Switzerland flag (red square field with a bold white cross in the center).

Caption below the rows, small caps, wide letter-spacing, color #E3B341, centered, reading exactly: "ROUND OF 8 · FIFA WORLD CUP 2026"
```

---

## SLIDE 1 — Como o modelo se saiu nas oitavas (Model5)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline, clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light. Apply a warm near-black overlay at 82% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the top, rotated slightly, deep oxblood-red background #7A2E2E, white bold text reading exactly: "MODEL REPORT CARD"

Serif display headline below, white, bold, reading exactly: "How the model did in the Round of 16"

Small caps label, wide letter-spacing, color #A99B7D, reading exactly: "MODEL5 · 8 GAMES · WHO ADVANCES METHOD"

Four stat cards in a 2x2 grid (background #201A12, thin gold border #4A3A22), each with a large bold gold number and a small muted caption below:
CARD 1: "6/8" big number, caption below: "Who advances — correct"
CARD 2: "75%" big number, caption below: "Accuracy above 70% confidence (down from 97% historically)"
CARD 3: "4/6" big number, caption below: "Derived bet (over/under, BTTS, clean sheet) correct"
CARD 4: "3/8" big number, caption below: "Exact scoreline in the model's top 3"

Insight card below the grid (color #C9BBA0 text, dark warm card background #201A12, thin gold left border), reading exactly: "The one miss above 70% confidence: Brazil was favored at 84.3% to beat Norway and lost 1-2 — the first real crack in a streak that had been correct 97% of the time above that confidence level all tournament."

Footer, muted #7A6E56, very small, reading exactly: "Model5 · SA+biases att+def, 88 training matches"
```

---

## SLIDE 2 — Probabilidade de ser campeão (Model6, 8 times vivos)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names, clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light, a single trophy silhouette faintly visible and out of focus in the deep background. Apply a warm near-black overlay at 84% opacity on top of the whole scene (color #14110C) so it reads as moody and prestigious behind the UI.

Small ribbon/tag near the top, rotated slightly, metallic gold background #E3B341, dark bold text reading exactly: "TITLE ODDS"

Serif display headline below, white, bold, reading exactly: "Who's most likely to lift the trophy"

Small caps label, wide letter-spacing, color #A99B7D, reading exactly: "MODEL6 · 10,000,000 SIMULATIONS · 8 TEAMS REMAINING"

A ranked list of 8 rows, each row: rank number in a small gold circle, a small rectangular national flag icon, team name in serif font (white bold) right next to the flag, a horizontal bar filling proportionally to the team's percentage (gold #E3B341 with soft glow for rank 1, muted graphite #6B7280 for the rest), and the percentage in bold gold tabular numbers at the right edge of each row.

ROW 1: "1" — small flag icon: Spain flag (horizontal red-yellow-red bands, wider yellow band with a coat of arms on the left side) — Spain — bar 35.3% (longest bar, gold, glowing) — "35.3%"
ROW 2: "2" — small flag icon: England flag (white field with a red St George's cross — a simple red plus-sign cross on white, NOT the Union Jack, NOT a black flag) — England — bar 19.8% — "19.8%"
ROW 3: "3" — small flag icon: France flag (vertical blue-white-red bands) — France — bar 17.0% — "17.0%"
ROW 4: "4" — small flag icon: Switzerland flag (red square field with a bold white cross in the center) — Switzerland — bar 7.2% — "7.2%"
ROW 5: "5" — small flag icon: Morocco flag (red field, green five-pointed star outlined in the center) — Morocco — bar 5.8% — "5.8%"
ROW 6: "6" — small flag icon: Argentina flag (horizontal light-blue-white-light-blue bands with a golden sun face centered in the white band) — Argentina — bar 5.6% — "5.6%"
ROW 7: "7" — small flag icon: Belgium flag (vertical black-yellow-red bands) — Belgium — bar 5.2% — "5.2%"
ROW 8: "8" — small flag icon: Norway flag (red field with a blue-and-white Nordic cross) — Norway — bar 4.3% — "4.3%"

Insight card below the list (color #C9BBA0 text, dark warm card background #201A12, thin gold left border), reading exactly: "Spain is the clear favorite at 35.3% — more than the bottom five teams combined — largely on the back of a 75.8% chance of getting past Belgium in the quarterfinal."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches · 10,000,000 simulations"
```

---

## SLIDE 2b — O que o modelo aprendeu (França, Marrocos, Espanha, Bélgica — lado QF1/QF2)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names, clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light. Apply a warm near-black overlay at 86% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the top, rotated slightly, metallic gold background #E3B341, dark bold text reading exactly: "MODEL INSIGHT · 1 OF 2"

Serif display headline below, white, bold, reading exactly: "What the model actually learned"

Small caps label, wide letter-spacing, color #A99B7D, reading exactly: "THE FRANCE–MOROCCO / SPAIN–BELGIUM SIDE OF THE BRACKET"

Four compact stacked rows (background #201A12, thin gold border #4A3A22), each row: a small national flag icon + team name in serif bold white on the left, two small bold stat chips "ATT" and "DEF" with their numbers, and a single line of real-data commentary in color #C9BBA0 below the name.

ROW 1: flag icon (France flag: vertical blue-white-red bands) + "FRANCE" — chips "ATT 0.87" / "DEF 1.00" (both neutral grey chips) — commentary: "14 goals in 5 games, but against Senegal, Iraq, Sweden and Paraguay — no serious test yet, and the Round of 16 win over underdog Paraguay finished a narrow 1-0."

ROW 2: flag icon (Morocco flag: red field, green five-pointed star outlined in the center) + "MOROCCO" — chips "ATT 1.03" / "DEF 1.00" (both neutral grey chips) — commentary: "Held the Netherlands scoreless before winning on penalties in the Round of 32, then routed Canada 3-0 in the Round of 16 — balanced, no glaring weak side."

ROW 3: flag icon (Spain flag: horizontal red-yellow-red bands, wider yellow band with a coat of arms on the left side) + "SPAIN" — chips "ATT 1.14" / "DEF 1.16" (both gold-tinted chips, background #E3B341 with dark text — the best pair of ratings in the tournament) — commentary: "Zero goals conceded in 5 games — the only unbeaten defense left in the tournament."

ROW 4: flag icon (Belgium flag: vertical black-yellow-red bands) + "BELGIUM" — chips "ATT 1.31" (gold-tinted chip, background #E3B341 dark text) / "DEF 0.66" (red-tinted chip, background #7A2E2E white text — one of the lowest defense ratings left) — commentary: "Scored 5 against New Zealand and 4 against the USA, but also drew 1-1 with Egypt and 2-2 with Senegal after 90 minutes — explosive and leaky in the same breath."

Footer card at the bottom (color #C9BBA0 text, dark warm card background, thin gold left border), reading exactly: "The model only sees these 96 real matches and player attribute ratings — no sense of pedigree, history, or market reputation."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches · 1 of 2"
```

---

## SLIDE 2c — O que o modelo aprendeu (Noruega, Inglaterra, Argentina, Suíça — lado QF3/QF4)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names, clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light. Apply a warm near-black overlay at 86% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the top, rotated slightly, metallic gold background #E3B341, dark bold text reading exactly: "MODEL INSIGHT · 2 OF 2"

Serif display headline below, white, bold, reading exactly: "What the model actually learned"

Small caps label, wide letter-spacing, color #A99B7D, reading exactly: "THE NORWAY–ENGLAND / ARGENTINA–SWITZERLAND SIDE OF THE BRACKET"

Four compact stacked rows (background #201A12, thin gold border #4A3A22), each row: a small national flag icon + team name in serif bold white on the left, two small bold stat chips "ATT" and "DEF" with their numbers, and a single line of real-data commentary in color #C9BBA0 below the name.

ROW 1: flag icon (Norway flag: red field with a blue-and-white Nordic cross) + "NORWAY" — chips "ATT 1.23" / "DEF 1.29" (both gold-tinted chips, background #E3B341 dark text) — commentary: "Lost 1-4 to France in the group stage, but conceded just 1 goal while upsetting Brazil 2-1 in the Round of 16."

ROW 2: flag icon (England flag: white field with a red St George's cross — a simple red plus-sign cross on white, NOT the Union Jack, NOT a black flag) + "ENGLAND" — chips "ATT 0.94" / "DEF 1.00" (both neutral grey chips) — commentary: "Conceded in 4 of its 5 games, including 2 goals to non-favorite Mexico in the Round of 16."

ROW 3: flag icon (Argentina flag: horizontal light-blue-white-light-blue bands with a golden sun face centered in the white band) + "ARGENTINA" — chips "ATT 1.01" (neutral grey chip) / "DEF 0.55" (red-tinted chip, background #7A2E2E white text — the lowest defense rating of the 8 remaining teams) — commentary: "Drew 1-1 with a 5.7%-underdog Cape Verde through 90 minutes in the Round of 32, needing extra time to win 3-2, then conceded 2 goals to non-favorite Egypt in the Round of 16."

ROW 4: flag icon (Switzerland flag: red square field with a bold white cross in the center) + "SWITZERLAND" — chips "ATT 1.03" / "DEF 1.13" (both neutral-to-gold chips) — commentary: "Clean sheets against Algeria and Colombia, but needed penalties to get past Colombia in the Round of 16 — resilient more than dominant."

Small caps micro-label above the rows, color #A99B7D, reading exactly: "GLOBAL CONTEXT"
One-line note, color #A99B7D, italic, reading exactly: "The model's baseline expected-goals rate jumped from 1.01 to 1.38 between versions — the Round of 16 was far more high-scoring than expected, which pulls every team's raw number up or down with it."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches · 2 of 2"
```

---

## SLIDE 3 — França x Marrocos

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names (evoking an engraved trophy plaque), clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light spilling across the pitch (not cool blue/white light). On the left third of the image, an illustrated football player in a France kit (blue shirt, white shorts), mid-action celebration pose, face generic/stylized (not a specific real athlete's likeness). On the right third, an illustrated football player in a Morocco kit (red shirt, green trim), mid-action pose facing toward the center, also generic/no specific likeness. Both figures partially faded into the dark stadium background. Apply a warm near-black overlay at 80% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the very top, rotated slightly, deep oxblood-red background #7A2E2E, white bold text reading exactly: "QUARTERFINALS"

Text label below the ribbon, small caps, wide letter-spacing, color #E3B341, reading exactly: "FIFA WORLD CUP 2026"

Below that, a thin horizontal progress line with 3 small circular nodes evenly spaced, labeled below: "QF" (filled solid gold, active), "SF" (hollow grey), "FINAL" (hollow grey), connected by a thin line, gold up to the QF node. Small caps micro-label above, color #A99B7D, reading exactly: "PATH TO THE FINAL"

Below that, two generic shield-shaped crests (rounded-bottom heraldic shield outline, dark bronze-brown #201A12 fill, thin gold border, strong drop shadow) side by side, each shield filled edge-to-edge with the team's actual flag design. A warm gold radial spotlight glow directly behind the pair of shields, centered on the "VS". Between the two shields, large bold serif text reading exactly "VS" with a subtle gold glow. Below each shield, the team name in an elegant serif display font, white bold caps.
LEFT SHIELD: France flag (vertical blue-white-red bands). Name below: FRANCE
RIGHT SHIELD: Morocco flag (red field, green five-pointed star outlined in the center). Name below: MOROCCO

Cards below (background #201A12, border #4A3A22, semi-opaque so the stadium photo behind is still faintly visible) contain the following, stacked vertically:

A line of centered white medium text reading exactly: "xG 1.61 · · · 1.07 xG"

Small caps label above the bar, muted #A99B7D, wide letter-spacing, reading exactly: "WHO ADVANCES"
Probability bar — single rounded pill, TWO segments only, with the percentage written in bold text directly inside each colored segment:
LEFT segment: metallic gold #E3B341 with a soft glow, with "62.2%" in bold dark text centered inside the segment.
RIGHT segment: muted graphite #6B7280, no glow, with "37.8%" in bold white text centered inside the segment.
Team name labels below the bar (names only, percentages already shown inside the bar): "France      Morocco"

(no confidence pill for this game — favorite is below 70%)

Model's pick badge (dark pill background #201A12, gold border #E3B341) reading exactly: "MODEL'S PICK · Both teams score · 52.6%"

Small caps label "TOP SCORES" followed by 3 chips inline (dark #201A12 background, thin gold border, white bold text): "1–1  11.8%   1–0  11.0%   2–1  9.5%"

Insight card (color #C9BBA0 text, dark warm card background) reading exactly: "Morocco has the lowest attacking xG of the round on either side of the ball, but France's own defense has conceded goals all tournament — this is the only quarterfinal where the model doesn't back a clean sheet for anyone."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches · 1,000,000 simulations"
```

---

## SLIDE 4 — Espanha x Bélgica

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names (evoking an engraved trophy plaque), clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light spilling across the pitch. On the left third of the image, an illustrated football player in a Spain kit (red shirt, blue shorts), mid-action celebration pose, face generic/stylized (not a specific real athlete's likeness). On the right third, an illustrated football player in a Belgium kit (red shirt, black shorts), mid-action pose facing toward the center, also generic/no specific likeness. Both figures partially faded into the dark stadium background. Apply a warm near-black overlay at 80% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the very top, rotated slightly, deep oxblood-red background #7A2E2E, white bold text reading exactly: "QUARTERFINALS"

Text label below the ribbon, small caps, wide letter-spacing, color #E3B341, reading exactly: "FIFA WORLD CUP 2026"

Below that, a thin horizontal progress line with 3 small circular nodes evenly spaced, labeled below: "QF" (filled solid gold, active), "SF" (hollow grey), "FINAL" (hollow grey), connected by a thin line, gold up to the QF node. Small caps micro-label above, color #A99B7D, reading exactly: "PATH TO THE FINAL"

Below that, two generic shield-shaped crests (rounded-bottom heraldic shield outline, dark bronze-brown #201A12 fill, thin gold border, strong drop shadow) side by side, each shield filled edge-to-edge with the team's actual flag design. A warm gold radial spotlight glow directly behind the pair of shields, centered on the "VS". Between the two shields, large bold serif text reading exactly "VS" with a subtle gold glow. Below each shield, the team name in an elegant serif display font, white bold caps.
LEFT SHIELD: Spain flag (horizontal red-yellow-red bands, wider yellow band with a coat of arms on the left side). Name below: SPAIN
RIGHT SHIELD: Belgium flag (vertical black-yellow-red bands). Name below: BELGIUM

Cards below (background #201A12, border #4A3A22, semi-opaque so the stadium photo behind is still faintly visible) contain the following, stacked vertically:

A line of centered white medium text reading exactly: "xG 2.93 · · · 1.44 xG"

Small caps label above the bar, muted #A99B7D, wide letter-spacing, reading exactly: "WHO ADVANCES"
Probability bar — single rounded pill, TWO segments only, with the percentage written in bold text directly inside each colored segment:
LEFT segment: metallic gold #E3B341 with a soft glow, with "75.8%" in bold dark text centered inside the segment.
RIGHT segment: muted graphite #6B7280, no glow, with "24.2%" in bold white text centered inside the segment.
Team name labels below the bar (names only, percentages already shown inside the bar): "Spain      Belgium"

Gold confidence pill (rounded, background #E3B341, dark bold text) reading exactly: "★ SPAIN ADVANCES · 75.8%"

Model's pick badge (dark pill background #201A12, gold border #E3B341) reading exactly: "MODEL'S PICK · Over 2.5 goals · 81.0%"

Small caps label "TOP SCORES" followed by 3 chips inline (dark #201A12 background, thin gold border, white bold text): "2–1  7.9%   3–1  7.7%   2–2  5.6%"

Insight card (color #C9BBA0 text, dark warm card background) reading exactly: "The most one-sided quarterfinal by far — Spain's 2.93 expected goals is the highest of any team left in the tournament, and a 48.6% chance of winning by two goals or more."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches · 1,000,000 simulations"
```

---

## SLIDE 5 — Noruega x Inglaterra

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names (evoking an engraved trophy plaque), clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light spilling across the pitch. On the left third of the image, an illustrated football player in a Norway kit (red shirt, white shorts), mid-action celebration pose, face generic/stylized (not a specific real athlete's likeness). On the right third, an illustrated football player in an England kit (white shirt, navy shorts), mid-action pose facing toward the center, also generic/no specific likeness. Both figures partially faded into the dark stadium background. Apply a warm near-black overlay at 80% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the very top, rotated slightly, deep oxblood-red background #7A2E2E, white bold text reading exactly: "QUARTERFINALS"

Text label below the ribbon, small caps, wide letter-spacing, color #E3B341, reading exactly: "FIFA WORLD CUP 2026"

Below that, a thin horizontal progress line with 3 small circular nodes evenly spaced, labeled below: "QF" (filled solid gold, active), "SF" (hollow grey), "FINAL" (hollow grey), connected by a thin line, gold up to the QF node. Small caps micro-label above, color #A99B7D, reading exactly: "PATH TO THE FINAL"

Below that, two generic shield-shaped crests (rounded-bottom heraldic shield outline, dark bronze-brown #201A12 fill, thin gold border, strong drop shadow) side by side, each shield filled edge-to-edge with the team's actual flag design. A warm gold radial spotlight glow directly behind the pair of shields, centered on the "VS". Between the two shields, large bold serif text reading exactly "VS" with a subtle gold glow. Below each shield, the team name in an elegant serif display font, white bold caps.
LEFT SHIELD: Norway flag (red field with a blue-and-white Nordic cross). Name below: NORWAY
RIGHT SHIELD: England flag (white field with a red St George's cross — a simple red plus-sign cross on white, NOT the Union Jack, NOT a black flag). Name below: ENGLAND

Cards below (background #201A12, border #4A3A22, semi-opaque so the stadium photo behind is still faintly visible) contain the following, stacked vertically:

A line of centered white medium text reading exactly: "xG 1.60 · · · 2.58 xG"

Small caps label above the bar, muted #A99B7D, wide letter-spacing, reading exactly: "WHO ADVANCES"
Probability bar — single rounded pill, TWO segments only, with the percentage written in bold text directly inside each colored segment:
LEFT segment: muted graphite #6B7280, no glow, with "32.0%" in bold white text centered inside the segment.
RIGHT segment: metallic gold #E3B341 with a soft glow, with "68.0%" in bold dark text centered inside the segment.
Team name labels below the bar (names only, percentages already shown inside the bar): "Norway      England"

(no confidence pill for this game — 68.0% falls just short of the 70% threshold)

Model's pick badge (dark pill background #201A12, gold border #E3B341) reading exactly: "MODEL'S PICK · Over 2.5 goals · 78.8%"

Small caps label "TOP SCORES" followed by 3 chips inline (dark #201A12 background, thin gold border, white bold text): "1–2  8.1%   1–3  7.0%   2–2  6.5%"

Insight card (color #C9BBA0 text, dark warm card background) reading exactly: "England is favored at 68.0% — just short of the model's high-confidence threshold — but Norway is the tournament's biggest giant-killer so far, having already eliminated Brazil in the Round of 16."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches · 1,000,000 simulations"
```

---

## SLIDE 6 — Argentina x Suíça

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names (evoking an engraved trophy plaque), clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light spilling across the pitch (not cool blue/white light). On the left third of the image, an illustrated football player in an Argentina kit (light-blue and white striped shirt, black shorts), mid-action celebration pose, face generic/stylized (not a specific real athlete's likeness). On the right third, an illustrated football player in a Switzerland kit (red shirt, white shorts), mid-action pose facing toward the center, also generic/no specific likeness. Both figures partially faded into the dark stadium background. Apply a warm near-black overlay at 80% opacity on top of the whole scene (color #14110C) so it reads as rich and prestigious behind the UI, not distracting.

Small ribbon/tag near the very top, rotated slightly, deep oxblood-red background #7A2E2E, white bold text reading exactly: "QUARTERFINALS"

Text label below the ribbon, small caps, wide letter-spacing, color #E3B341 (metallic gold), reading exactly: "FIFA WORLD CUP 2026"

Below that, a thin horizontal progress line representing the path to the final, with 3 small circular nodes evenly spaced left to right, each with a label below: "QF" (filled solid gold, this is the active stage), "SF" (hollow outline, muted grey), "FINAL" (hollow outline, muted grey) — connect the nodes with a thin line, gold up to the QF node and muted grey afterward. Small caps micro-label above the line reading exactly: "PATH TO THE FINAL"

Below that, two generic shield-shaped crests (rounded-bottom heraldic shield outline, dark bronze-brown #201A12 fill, thin gold border, strong drop shadow) side by side, each shield filled edge-to-edge with the team's actual flag design (not the real federation crest). A warm gold radial spotlight glow directly behind the pair of shields, centered on the "VS". Between the two shields, large bold serif text reading exactly "VS" with a subtle gold glow. Below each shield, the team name in an elegant serif display font, white bold caps.
LEFT SHIELD: Argentina flag (horizontal light-blue-white-light-blue bands with a golden sun face centered in the white band). Name below: ARGENTINA
RIGHT SHIELD: Switzerland flag (red square field with a bold white cross in the center). Name below: SWITZERLAND

Cards below (background #201A12 dark warm bronze-brown, border #4A3A22 thin gold-brown, semi-opaque so the stadium photo behind is still faintly visible through the dark tone) contain the following, stacked vertically:

A line of centered white medium text reading exactly: "xG 1.52 · · · 1.57 xG"

Small caps label above the bar, muted #A99B7D, wide letter-spacing, reading exactly: "WHO ADVANCES"
Probability bar — single rounded pill, TWO segments only (not three), with the percentage written in bold text directly inside each colored segment (not just below):
LEFT segment: muted graphite #6B7280, no glow, with "49.0%" in bold white text centered inside the segment.
RIGHT segment: metallic gold #E3B341 with a soft glow, with "51.0%" in bold dark text centered inside the segment.
Team name labels below the bar (names only, percentages already shown inside the bar): "Argentina      Switzerland"

(no confidence pill for this game — it's a near coin-flip, no side reaches 70%)

Model's pick badge (dark pill background #201A12, gold border #E3B341) reading exactly: "MODEL'S PICK · Both teams score · 62.0%"

Small caps label "TOP SCORES" followed by 3 chips inline (dark #201A12 background, thin gold border, white bold text): "1–1  10.9%   1–2  8.5%   2–1  8.3%"

Insight card (color #C9BBA0 text, dark warm card background) reading exactly: "The tightest matchup of the Quarterfinals — Switzerland's 51.0% edge over Argentina's 49.0% is the closest 'who advances' split of the round. Switzerland reached this stage via a penalty shootout against Colombia in the Round of 16."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches · 1,000,000 simulations"
```
