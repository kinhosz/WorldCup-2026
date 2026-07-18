# Instagram Post — Final + 3º Lugar (estilo "Troféu Chegando", último post da Copa)

Mesmo estilo visual das quartas/semis, agora no fechamento do torneio. Texto sempre em inglês. Formato 4:5, 1080×1350. Dados de `output/odds_france_vs_england.json` (Model7, sem prorrogação — regra FIFA do 3º lugar) e `output/odds_spain_vs_argentina.json` (Model7, com prorrogação). Report Card revisa a Semifinal com os pesos do **Model6** (antes da recalibração), que é o teste out-of-sample de verdade.

**Correção importante (18 jul 2026):** o Model6 **NÃO** acertou as duas semis — só a Espanha (60.5%). Favoreceu a Inglaterra (66.3%) contra a Argentina e errou; foi a segunda zebra consecutiva da Argentina (a primeira foi a virada quase-50/50 contra a Suíça nas quartas). Nenhum dos dois placares da semi bateu o top-3 do modelo. Essa é a mensagem real do slide 1 — nada de "acertou tudo".

**Destaque pedido pelo usuário:** troféu em evidência no Hook e no slide da Final, já que é a última rodada. Último slide é um agradecimento à comunidade do Instagram (40k+ views, bastante interação) convidando pro repositório GitHub.

**Ordem do carrossel:** Hook com troféu (0) · Report Card da semifinal — Model6, a zebra da Argentina (1) · O que o modelo aprendeu — Espanha x Argentina, biases do Model7 (2) · 3º Lugar: França x Inglaterra (3) · A FINAL: Espanha x Argentina, troféu em destaque (4) · Agradecimento + convite pro GitHub (5).

**Paleta e identidade:** idêntica às quartas/semis — preto quente `#14110C`, cards bronze `#201A12`, accent dourado `#E3B341`, tag de rodada oxblood `#7A2E2E`. Elemento "PATH TO THE FINAL" (QF→SF→FINAL) **removido** (pedido do usuário, 18 jul 2026) — não faz mais sentido mostrar progresso de rodada no post de fechamento.

---

## SLIDE 0 — Hook (com destaque pro troféu)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the title and team names (evoking an engraved trophy plaque), clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light and heavy gold confetti/pyro haze filling the air. Apply a warm near-black overlay at 76% opacity on top of the whole scene (color #14110C) so it reads as rich and prestigious behind the UI.

CENTERPIECE: a large, detailed, brightly lit gold World Cup trophy illustration, centered near the top of the frame, with a strong warm golden glow/halo radiating behind it and light rays fanning outward — this is the visual hero of the slide, bigger and more prominent than any other element.

Below the trophy, large bold serif display title, centered, metallic gold color #E3B341 with a soft warm glow, two lines, huge and bold: "THE FINAL" on the first line, "FIFA WORLD CUP 2026" smaller on the second line.

Below the title, one row with a shield-shaped crest pair (rounded-bottom heraldic shield outline, dark bronze-brown #201A12 fill, thin gold border, strong drop shadow, slightly larger than usual to mark the main event) filled edge-to-edge with each team's flag design, large bold gold "VS" centered between them with a soft glow, team names in serif bold white caps below each shield.

LEFT SHIELD: Spain flag (horizontal red-yellow-red bands, wider yellow band with a coat of arms on the left side). Name below: SPAIN. RIGHT SHIELD: Argentina flag (horizontal light-blue-white-light-blue bands with a golden sun face centered in the white band). Name below: ARGENTINA.

Below that row, a smaller secondary row, visually subordinate (smaller shields, muted grey-bronze tone instead of gold accents), reading a small caps label above it, wide letter-spacing, color #A99B7D: "THIRD PLACE PLAY-OFF" — then two small shields: LEFT — France flag (vertical blue-white-red bands), name below FRANCE. RIGHT — England flag (white field with a red St George's cross — a simple red plus-sign cross on white, NOT the Union Jack, NOT a black flag), name below ENGLAND.

Caption at the very bottom, small caps, wide letter-spacing, color #E3B341, centered, reading exactly: "FIFA WORLD CUP 2026 · THE LAST WEEKEND"
```

---

## SLIDE 1 — Report Card da Semifinal (Model6, a zebra da Argentina)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline, clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light. Apply a warm near-black overlay at 82% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the top, rotated slightly, deep oxblood-red background #7A2E2E, white bold text reading exactly: "MODEL REPORT CARD"

Serif display headline below, white, bold, reading exactly: "The model's second reality check"

Small caps label, wide letter-spacing, color #A99B7D, reading exactly: "MODEL6 · SEMIFINALS · WHO ADVANCES METHOD"

Four stat cards in a 2x2 grid (background #201A12, thin gold border #4A3A22), each with a large bold gold number and a small muted caption below:
CARD 1: "1/2" big number, caption below: "Who advances — correct (Spain only)"
CARD 2: "0/2" big number, caption below: "Games above 70% confidence"
CARD 3: "66.3%" big number, caption below: "Confidence England was favored to beat Argentina"
CARD 4: "0/2" big number, caption below: "Exact scorelines in the model's top 3"

Insight card below the grid (color #C9BBA0 text, dark warm card background #201A12, thin gold left border), reading exactly: "Argentina's second upset in a row: a near-coin-flip win over Switzerland in the quarterfinals, then a come-from-behind 2-1 win over an England side favored at 66.3%. The model never saw either coming."

Footer, muted #7A6E56, very small, reading exactly: "Model6 · SA by points, 96 training matches · frozen before the semifinals"
```

---

## SLIDE 2 — O que o modelo aprendeu (Espanha x Argentina, biases do Model7)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names, clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light. Apply a warm near-black overlay at 86% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the top, rotated slightly, metallic gold background #E3B341, dark bold text reading exactly: "MODEL INSIGHT"

Serif display headline below, white, bold, reading exactly: "What the model learned about the finalists"

Small caps label, wide letter-spacing, color #A99B7D, reading exactly: "MODEL7 · RECALIBRATED AFTER 102 MATCHES"

Two compact stacked rows (background #201A12, thin gold border #4A3A22), each row: a small national flag icon + team name in serif bold white on the left, two small bold stat chips "ATT BIAS" and "DEF BIAS" with their numbers, and a single line of real-data commentary in color #C9BBA0 below the name.

ROW 1: flag icon (Spain flag: horizontal red-yellow-red bands, wider yellow band with a coat of arms on the left side) + "SPAIN" — chips "ATT BIAS 1.13" (gold-tinted chip, background #E3B341 dark text) / "DEF BIAS 1.30" (gold-tinted chip, background #E3B341 dark text — the best defensive rating left in the tournament) — commentary: "Conceded just 1 goal in 7 games so far — the model has never had to correct its trust in this defense."

ROW 2: flag icon (Argentina flag: horizontal light-blue-white-light-blue bands with a golden sun face centered in the white band) — "ARGENTINA" — chips "ATT BIAS 1.04" (neutral grey chip) / "DEF BIAS 0.51" (red-tinted chip, background #7A2E2E white text — one of the lowest defensive ratings left in the tournament) — commentary: "Conceded 7 goals in 7 games — a defense the model has flagged as fragile all tournament, even as the team kept winning anyway."

Insight card below the rows (color #C9BBA0 text, dark warm card background #201A12, thin gold left border), reading exactly: "The model sees a historic mismatch on paper — Spain's best defense in the field against Argentina's shakiest. Argentina has spent the whole knockout stage proving the model wrong about results while it keeps being right about the underlying numbers."

Footer, muted #7A6E56, very small, reading exactly: "Model7 · SA by points, 102 training matches, SF/Final weighted higher"
```

---

## SLIDE 3 — 3º Lugar: França x Inglaterra

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names (evoking an engraved trophy plaque), clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light spilling across the pitch. On the left third of the image, an illustrated football player in a France kit (blue shirt, white shorts), mid-action pose, face generic/stylized (not a specific real athlete's likeness). On the right third, an illustrated football player in an England kit (white shirt, navy shorts), mid-action pose facing toward the center, also generic/no specific likeness. Both figures partially faded into the dark stadium background. Apply a warm near-black overlay at 80% opacity on top of the whole scene (color #14110C).

Small ribbon/tag near the very top, rotated slightly, deep oxblood-red background #7A2E2E, white bold text reading exactly: "THIRD PLACE PLAY-OFF"

Text label below the ribbon, small caps, wide letter-spacing, color #E3B341, reading exactly: "FIFA WORLD CUP 2026"

Below that, two generic shield-shaped crests (rounded-bottom heraldic shield outline, dark bronze-brown #201A12 fill, thin gold border, strong drop shadow) side by side, each shield filled edge-to-edge with the team's actual flag design. Between the two shields, large bold serif text reading exactly "VS". Below each shield, the team name in an elegant serif display font, white bold caps.
LEFT SHIELD: France flag (vertical blue-white-red bands). Name below: FRANCE
RIGHT SHIELD: England flag (white field with a red St George's cross — a simple red plus-sign cross on white, NOT the Union Jack, NOT a black flag). Name below: ENGLAND

Cards below (background #201A12, border #4A3A22, semi-opaque so the stadium photo behind is still faintly visible) contain the following, stacked vertically:

A line of centered white medium text reading exactly: "xG 1.89 · · · 0.93 xG"

Small caps note directly below the xG line, muted #A99B7D, small, reading exactly: "No extra time in this match — FIFA rules send a 90-minute draw straight to penalties"

Small caps label above the bar, muted #A99B7D, wide letter-spacing, reading exactly: "WHO FINISHES THIRD"
Probability bar — single rounded pill, TWO segments only, with the percentage written in bold text directly inside each colored segment:
LEFT segment: metallic gold #E3B341 with a soft glow, with "70.9%" in bold dark text centered inside the segment.
RIGHT segment: muted graphite #6B7280, no glow, with "29.1%" in bold white text centered inside the segment.
Team name labels below the bar (names only, percentages already shown inside the bar): "France      England"

Confidence pill (background #E3B341, dark bold text, small trophy or star icon to the left), reading exactly: "★ MODEL CONFIDENCE 70.9%"

Model's pick badge (dark pill background #201A12, gold border #E3B341) reading exactly: "MODEL'S PICK · Over 2.5 goals · 53.5%"

Small caps label "TOP SCORES" followed by 3 chips inline (dark #201A12 background, thin gold border, white bold text): "1–0  11.3%   2–0  10.7%   1–1  10.5%"

Insight card (color #C9BBA0 text, dark warm card background) reading exactly: "France carries a 39.5% chance of a clean sheet here — more than double England's 15.1% — while England has conceded 8 goals in 7 games, tied for the leakiest defense of any team still playing."

Footer, muted #7A6E56, very small, reading exactly: "Model7 · SA by points, 102 training matches · 1,000,000 simulations"
```

---

## SLIDE 4 — A FINAL: Espanha x Argentina (troféu em destaque + narrativa do bicampeonato 2010→2026)

Versão especial pedida pelo usuário (18 jul 2026) depois de ver a primeira geração do slide: já que é a pick mais confiante do mata-mata inteiro (86.5%), o card ganha um tratamento mais grandioso e um elemento novo dedicado à história — Espanha só tem 1 título (2010); vencer aqui seria a 2ª estrela, 16 anos depois.

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline and team names (evoking an engraved trophy plaque), clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, warm golden light, dense gold confetti falling, bursts of gold pyro/fireworks in the upper corners — the single most spectacular and celebratory background of the entire series, this is the championship moment. On the left third of the image, an illustrated football player in a Spain kit (red shirt, blue shorts) — a young Black man with short curly dark hair, generic/stylized facial features (not a specific real athlete's likeness) — triumphantly lifting the World Cup trophy overhead with both arms. On the right third, an illustrated football player in an Argentina kit (light-blue-and-white striped shirt, black shorts), mid-action pose facing toward the center, also generic/no specific likeness. Apply a warm near-black overlay at 74% opacity on top of the whole scene (color #14110C).

A strong golden halo glow and light rays fan outward from the trophy the Spain player is holding, making it the clear visual hero of this card and reinforcing that this is the title match — no separate floating trophy icon elsewhere in the frame.

Small ribbon/tag near the very top, rotated slightly, deep oxblood-red background #7A2E2E, white bold text reading exactly: "THE FINAL"

Text label below the ribbon, small caps, wide letter-spacing, color #E3B341, reading exactly: "FIFA WORLD CUP 2026"

Below that, a compact horizontal history strip, centered, evoking two stars on a crest connected by a thin dotted gold line: a small solid gold star icon above the text "2010" (both in gold #E3B341), then a dotted gold connector line spanning "16 YEARS" written tiny in muted #A99B7D beneath the dots, then a second star icon — outlined/hollow, not yet filled, with a soft pulsing gold glow around just the outline — above the text "2026?" in gold #E3B341. Small caps label above this whole strip, wide letter-spacing, color #A99B7D, reading exactly: "CHASING A SECOND STAR"

Below that, two generic shield-shaped crests (rounded-bottom heraldic shield outline, dark bronze-brown #201A12 fill, thin gold border, strong drop shadow, a warm gold radial spotlight glow directly behind the pair) side by side, each shield filled edge-to-edge with the team's actual flag design. Between the two shields, large bold serif text reading exactly "VS" with a gold glow. Below each shield, the team name in an elegant serif display font, white bold caps.
LEFT SHIELD: Spain flag (horizontal red-yellow-red bands, wider yellow band with a coat of arms on the left side). Name below: SPAIN
RIGHT SHIELD: Argentina flag (horizontal light-blue-white-light-blue bands with a golden sun face centered in the white band). Name below: ARGENTINA

Cards below (background #201A12, border #4A3A22, semi-opaque so the stadium photo behind is still faintly visible) contain the following, stacked vertically:

A line of centered white medium text reading exactly: "xG 3.09 · · · 1.06 xG"

Small caps label above the bar, muted #A99B7D, wide letter-spacing, reading exactly: "WHO LIFTS THE TROPHY"
Probability bar — single rounded pill, TWO segments only, with the percentage written in bold text directly inside each colored segment:
LEFT segment: metallic gold #E3B341 with a strong glow, with "86.5%" in bold dark text centered inside the segment.
RIGHT segment: muted graphite #6B7280, no glow, with "13.5%" in bold white text centered inside the segment.
Team name labels below the bar (names only, percentages already shown inside the bar): "Spain      Argentina"

Confidence pill (background #E3B341, dark bold text, small trophy icon to the left, a soft pulsing glow around the whole pill making it the most eye-catching badge on the card), reading exactly: "★ MODEL CONFIDENCE 86.5% — HIGHEST OF THE KNOCKOUT STAGE"

Small caps note below the confidence pill, muted #A99B7D, small, reading exactly: "If level after 90 minutes: extra time modeled, then penalties as a coin flip"

Model's pick badge (dark pill background #201A12, gold border #E3B341) reading exactly: "MODEL'S PICK · Over 2.5 goals · 78.2%"

Small caps label "TOP SCORES" followed by 3 chips inline (dark #201A12 background, thin gold border, white bold text): "3–1  8.2%   2–1  7.9%   3–0  7.7%"

Insight card (color #C9BBA0 text, dark warm card background, thin gold left border, slightly larger and more prominent than in previous slides) reading exactly: "Spain's only World Cup title came in 2010. Sixteen years later, the model gives them their best shot yet at a second — the most lopsided pick of the entire knockout stage. But Argentina has already beaten longer odds twice this tournament. Nobody's coasting into this one."

Footer, muted #7A6E56, very small, reading exactly: "Model7 · SA by points, 102 training matches · 1,000,000 simulations"
```

---

## SLIDE 5 — Agradecimento + convite pro GitHub (fecha o carrossel)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Elegant serif display typeface for the headline, clean geometric sans-serif for labels and data, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night from the pitch level looking up into the stands, floodlights blazing, thousands of phone camera flashes and warm gold confetti falling like rain, a celebratory, grateful atmosphere. Apply a warm near-black overlay at 78% opacity on top of the whole scene (color #14110C).

CENTERPIECE: a medium-sized gold World Cup trophy illustration near the top, softly glowing, slightly smaller and calmer than the previous slide — a closing note, not a competing headline.

Large bold serif display title below the trophy, centered, white with a soft gold edge glow, two lines: "THANK YOU" on the first line, smaller gold subtitle below: "FOR FOLLOWING THE WHOLE RUN"

Below the title, a short paragraph, centered, warm off-white color #C9BBA0, medium serif-adjacent body text, reading exactly: "From the group stage to this final weekend, every prediction, every graph, every model update — all because you kept showing up."

Two stat cards side by side (background #201A12, thin gold border #4A3A22, each with a large bold gold number and a small muted caption below):
CARD 1: "40,000+" big number, caption below: "Views across the series"
CARD 2: "7" big number, caption below: "Model versions, calibrated live as results came in"

Below the cards, a distinct call-to-action card (background #201A12, gold border #E3B341, slightly larger padding, centered content) containing: a small caps label, wide letter-spacing, color #A99B7D, reading exactly: "WANT TO SEE HOW IT ALL WORKS" — below it, large bold monospace-style text on its own line, color #E3B341, reading exactly: "github.com/kinhosz/WorldCup-2026" — below that, smaller muted text color #A99B7D reading exactly: "Every model, every dataset, every line of code — open for anyone to dig into."

Footer, muted #7A6E56, very small, centered, reading exactly: "Model7 · Monte Carlo World Cup Simulator · See you in 2030"
```
