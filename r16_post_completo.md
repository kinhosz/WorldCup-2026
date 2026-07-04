# Instagram Post — R32 Encerrado + Model5 + Caminho do Brasil (Carrossel)

Cada prompt é autossuficiente. Copiar e colar diretamente no Gemini. Todos os dados vêm de `output/r32_analise_completa.md`, `output/model5_vs_model4_r32.md`, `output/top10_mudancas_model4_vs_model5.md` e `output/oitavas_bracket_probabilidades.md` — nenhum valor foi inventado. Texto do post em português. No Slide 1 (Top 10), os nomes de país ficam em inglês (igual ao post de referência já publicado); nos demais slides, nomes de país em português normalmente. Sem slide de hook — abre direto no conteúdo.

---

## SLIDE 1 — Top 10 Campeões: Antes x Agora

Professional sports editorial infographic. Format 4:5 portrait 1080×1350px. Background color #080C18 (dark navy). Cards #1E293B with border #334155. Inter or equivalent sans-serif font, tabular numbers. Do not invent any values. Do not add any text, flag, number or name not listed below. All text in Portuguese except team names, which are in English with their flag emoji (matching the previously published post's style exactly).

Layout: full-bleed dark navy background. Top section without card: title, subtitle, column headers. Below: 10 rows each as a plain rounded dark card (uniform #1E293B, no colored left-border accent). Each row shows a simple dark rank chip on the left (same neutral dark style for every rank, no gold/silver/bronze distinction), flag emoji, team name in English, ANTES value in muted grey, AGORA value bold and large in white, delta badge on the right.

Delta badge colors: positive delta uses upward arrow and green #4ADE80. Negative delta uses downward arrow and red #EF4444. Row with no prior individual rank uses a green "NOVO" pill instead of a delta.

TITLE: COPA DO MUNDO 2026 · ODDS DE CAMPEÃO
SUBTITLE: Antes do R32 (Model4) vs depois do sorteio das oitavas (Model5)
COLUMN HEADERS (small caps, wide letter-spacing): #   SELEÇÃO   ANTES   AGORA   Δ

ROW 1:  #1  🇫🇷 France       ANTES 12.0%  AGORA 26.7%  ↑ +14.7%   pill: "↑3pos" green
ROW 2:  #2  🇧🇷 Brazil       ANTES 10.0%  AGORA 20.2%  ↑ +10.2%   pill: "↑3pos" green
ROW 3:  #3  🇪🇸 Spain        ANTES "outros 22*"  AGORA 13.7%  pill: "NOVO" green
ROW 4:  #4  🇦🇷 Argentina    ANTES 22.4%  AGORA  6.7%  ↓ −15.7%   pill: "↓3pos" red
ROW 5:  #5  🇵🇹 Portugal     ANTES 12.3%  AGORA  6.6%  ↓ −5.7%    pill: "↓2pos" red
ROW 6:  #6  🇲🇦 Morocco      ANTES "outros 22*"  AGORA  6.3%  pill: "NOVO" green
ROW 7:  #7  🏴󠁧󠁢󠁥󠁮󠁧󠁿 England      ANTES  9.5%  AGORA  6.0%  ↓ −3.5%    pill: "↓1pos" red
ROW 8:  #8  🇨🇴 Colombia     ANTES  1.8%  AGORA  4.9%  ↑ +3.1%
ROW 9:  #9  🇨🇭 Switzerland  ANTES "outros 22*"  AGORA  2.7%  pill: "NOVO" green
ROW 10: #10 🇺🇸 United States ANTES 1.5%  AGORA  2.2%  ↑ +0.7%

FOOTER LINE 1 (muted italic #64748B, small): *as outras 22 seleções somavam 7.0% juntas antes do R32 — não existia número individual pra elas
FOOTER LINE 2 (red #EF4444, small): 3 favoritos saíram de verdade: 🇳🇱 Netherlands (era #2, 15.7%), 🇩🇪 Germany (era #7, 6.3%) e 🇯🇵 Japan (era #9, 1.6%) — pênaltis e zebra
FOOTER LINE 3 (muted #64748B, very small): Model5 (SA+biases att+def · 88 jogos) · 10.000.000 simulações

---

## SLIDE 2 — Como o Model4 se saiu no R32

Professional sports editorial infographic. Format 4:5 portrait 1080×1350px. Background color #080C18 (dark navy). Cards #1E293B with border #334155. Inter or equivalent sans-serif font. Vivid color coding throughout — use distinct accent colors per stat, not a monochrome layout. Do not invent any values or numbers not listed below. All text in Portuguese.

Layout: centered vertical stack. Eyebrow label, title, subtitle. One large prominent circular stat card (donut/gauge ring style filled proportionally, green #4ADE80 arc) with the number in the center. Then three colored stat chips in a row, each a different accent color. Then one insight card. Footer.

EYEBROW LABEL (small caps, muted #94A3B8, wide letter-spacing): MODEL4 · PERFORMANCE NO R32

TITLE (white bold): Acertou 10 de 16

SUBTITLE (muted #94A3B8): Olhando só o placar dos 90 minutos

LARGE CIRCULAR STAT (donut ring green #4ADE80, 62.5% filled, number in center white bold): 62.5%
Label below: W/D/L correto nos 90' (10/16 jogos)

THREE STAT CHIPS IN A ROW, each a distinctly colored rounded card:
Chip 1 (blue #60A5FA accent): 75%  |  label: acerto em "quem avança"
Chip 2 (orange #FB923C accent): 60%  |  label: confiança ≥70% (nos 90')
Chip 3 (purple #C084FC accent): 87.5% |  label: confiança ≥70% (quem avança)

INSIGHT CARD (color #93C5FD text, dark card background with a small yellow ⚠ icon): 5 dos 16 jogos empataram nos 90' (31%) — e, como sempre, o modelo nunca apontou empate como resultado mais provável em nenhum deles. Mesma limitação estrutural vista na fase de grupos.

Footer (muted #64748B, very small): Fonte: output/r32_analise_completa.md

---

## SLIDE 3 — Acertos e zebras da rodada

Professional sports editorial infographic. Format 4:5 portrait 1080×1350px. Background color #080C18 (dark navy). Cards #1E293B with border #334155. Inter or equivalent sans-serif font. Do not invent any values or add judgment labels not listed below. Rich, high-contrast color coding throughout — vivid and colorful at a glance, not monochrome text on dark cards. Country names in Portuguese, with flag emoji next to each one.

Draw every flag accurately using the exact design described below wherever that country appears — do not rely on the emoji alone, small flag icons are easy to get wrong.

FLAG DESIGNS (use these exact descriptions for every flag icon in this slide):
- França: vertical tricolor, blue-white-red.
- EUA: red and white horizontal stripes with a blue rectangle of white stars in the upper-left corner.
- Colômbia: horizontal tricolor, yellow band on top (double height), blue in the middle, red on the bottom.
- Alemanha: horizontal tricolor, black-red-gold (gold on the bottom).
- Paraguai: horizontal tricolor, red-white-blue, with a circular national emblem centered in the white band.
- Holanda: horizontal tricolor, red-white-blue (Netherlands, NOT the vertical French flag).
- Marrocos: red field with a green five-pointed pentagram (star) outlined in the center.
- Costa do Marfim: vertical tricolor, orange-white-green, in that exact left-to-right order (this is the mirror image of Ireland's flag, which is green-white-orange — do not swap the order).
- Noruega: red field with a blue-and-white Nordic cross (off-center toward the hoist).
- Bélgica: vertical tricolor, black-yellow-red.
- Senegal: vertical tricolor, green-yellow-red, with one small green five-pointed star centered in the yellow band.
- Suécia: blue field with a yellow Nordic cross (off-center toward the hoist).
- Gana: horizontal tricolor, red-yellow-green, with one black five-pointed star centered in the yellow band.

CHIP DEFINITION (applies to every "chip" mentioned anywhere in this slide, including the confidence chips in the CONFIRMADO/ZEBRA rows AND the score chips in the footer): a chip is always a small solid rounded-rectangle badge with padding — a filled background color, a thin border, and bold text on top — the same physical shape and treatment for every single chip on the slide. A chip is NEVER just colored text sitting inline in a sentence with no background shape. Confidence chips: green #4ADE80 background with dark text for high-confidence values, red #EF4444 background with white text for the favorite's confidence in the upset row, grey #64748B background with white text for underdog values.

Layout: eyebrow label, title. Two labeled sections stacked vertically, each with a colored icon/badge next to the section label: "CONFIRMADO" section has a green checkmark badge (circle background #4ADE80, dark checkmark) and green #4ADE80 left-border accent on its 3 rows. "ZEBRA" section has a red alert badge (circle background #EF4444, white icon) and red #EF4444 left-border accent on its large row. Footer callout card for exact scores with a gold/trophy accent.

EYEBROW LABEL (small caps, muted #94A3B8): ACERTOS E ZEBRAS

TITLE (white bold): Quem confirmou, quem surpreendeu

SECTION LABEL (green #4ADE80 badge + text, small caps): ✓ CONFIRMADO
ROW 1 (green left-border accent, card #1E293B): 🇫🇷 França — venceu 3–0 — confidence chip (green pill, dark bold text) reading "83.9%" placed at the right edge of the row
ROW 2 (green left-border accent): 🇺🇸 EUA — venceu 2–0 — confidence chip (green pill) reading "78.0%" at the right edge
ROW 3 (green left-border accent): 🇨🇴 Colômbia — venceu 1–0 — confidence chip (green pill) reading "53.5%" at the right edge

SECTION LABEL (red #EF4444 badge + text, small caps): ⚠ ZEBRA
LARGE ROW (red #EF4444 accent border, card background subtle dark red-tinted #2A1518): 🇩🇪 Alemanha era favorita, com um chip (red pill, white bold text) reading "76.7%" right next to the team name — sobre 🇵🇾 Paraguai, com a chip cinza (grey pill, white text) reading "8.9%" right next to that team name. Empate 1–1 nos 90', Paraguai venceu nos pênaltis. Label below in red bold: ÚNICA ZEBRA DE ALTA CONFIANÇA DO ROUND
Small line below (muted #94A3B8): mais 3 zebras leves, todas com favoritismo fraco (<42%): 🇳🇱 Holanda x 🇲🇦 Marrocos, 🇨🇮 Costa do Marfim x 🇳🇴 Noruega, 🇧🇪 Bélgica x 🇸🇳 Senegal

FOOTER CALLOUT CARD (gold/yellow #FBBF24 accent border and glow, dark background #1E293B, white bold text, small trophy icon on the left): PLACAR EXATO batido em 3 jogos, each match on its own line pairing one score chip with one flag+matchup, in this exact order — do not mix chips across lines:
Linha 1: chip "1–1"  🇳🇱 Holanda x 🇲🇦 Marrocos
Linha 2: chip "3–0"  🇫🇷 França x 🇸🇪 Suécia
Linha 3: chip "1–0"  🇨🇴 Colômbia x 🇬🇭 Gana

---

## SLIDE 4 — Por que o Top 10 mudou tanto

Professional sports editorial infographic. Format 4:5 portrait 1080×1350px. Background color #080C18 (dark navy). Cards #1E293B with border #334155. Inter or equivalent sans-serif font. Vivid color coding — each numbered card gets a distinct accent color, not identical white cards. Do not invent any values not listed below. Country names in Portuguese, with flag emoji next to each one.

Layout: eyebrow label, title. Three numbered cards stacked vertically, each with its own accent color, a bold headline and one line of explanation. Footer.

EYEBROW LABEL (small caps, muted #94A3B8): 3 FORÇAS, NÃO UMA SÓ

TITLE (white bold): O que moveu o ranking

CARD 1 (blue #60A5FA accent border and number badge "1"): 3 favoritos eliminados de verdade
Text below (muted): 🇳🇱 Holanda, 🇩🇪 Alemanha e 🇯🇵 Japão somavam 23.6 pontos percentuais — redistribuídos entre quem sobreviveu.

CARD 2 (orange #FB923C accent border and number badge "2"): O R32 real recalibrou os times
Text below (muted): 🇦🇷 Argentina só empatou com 🇨🇻 Cabo Verde (5.7% de chance) — bias de ataque caiu de 0.992 para 0.818. Times com goleada ou clean sheet (🇫🇷 França, 🇪🇸 Espanha, 🇨🇭 Suíça) subiram de bias.

CARD 3 (purple #C084FC accent border and number badge "3"): A posição na chave importa
Text below (muted): 🇫🇷 França caiu do lado mais fraco do chaveamento — só encontra o 🇧🇷 Brasil na final. 🇦🇷 Argentina está do MESMO lado do Brasil, e provavelmente precisa passar por ele antes da decisão.

Footer (muted #64748B, very small): Fonte: output/top10_mudancas_model4_vs_model5.md

---

## SLIDE 5 — Quem o modelo via errado

Professional sports editorial infographic. Format 4:5 portrait 1080×1350px. Background color #080C18 (dark navy). Cards #1E293B with border #334155. Inter or equivalent sans-serif font, tabular numbers. Vivid color coding, green and red columns clearly distinct. Do not invent any values or numbers not listed below. Country names in Portuguese, with flag emoji next to each one.

Layout: eyebrow label, title, subtitle. Two labeled sections stacked vertically: "SUBESTIMADO" (green #4ADE80 accent, badge with an upward icon, teams whose bias went up) and "SUPERESTIMADO" (red #EF4444 accent, badge with a downward icon, teams whose bias went down). Each row is a card with a colored left-border accent showing team name and the bias value moving from Model4 to Model5 with an arrow.

EYEBROW LABEL (small caps, muted #94A3B8, wide letter-spacing): BIAS RECALIBRADO

TITLE (white bold): Quem o modelo via errado

SUBTITLE (muted #94A3B8): Bias = desvio real de desempenho em relação ao que o elenco sugere. Subiu = o modelo via demais em baixo antes; caiu = via demais em cima.

SECTION LABEL (green #4ADE80 badge ↑, small caps): SUBESTIMADO ANTES
ROW 1 (green left-border): 🇪🇸 Espanha — ataque 0.745 → 0.922
ROW 2 (green left-border): 🇨🇭 Suíça — defesa 0.774 → 1.019
ROW 3 (green left-border): 🇺🇸 EUA — defesa 0.732 → 1.104
ROW 4 (green left-border): 🇫🇷 França — defesa 1.022 → 1.260

SECTION LABEL (red #EF4444 badge ↓, small caps): SUPERESTIMADO ANTES
ROW 1 (red left-border): 🇦🇷 Argentina — ataque 0.992 → 0.818
ROW 2 (red left-border): 🇦🇷 Argentina — defesa 1.156 → 0.843
ROW 3 (red left-border): 🇵🇹 Portugal — defesa 1.136 → 0.999
ROW 4 (red left-border): 🇧🇷 Brasil — defesa 1.081 → 0.878

Footer (muted #64748B, very small): Fonte: output/top10_mudancas_model4_vs_model5.md

---

## SLIDE 6 — O caminho do Brasil: bracket circular

Professional sports editorial infographic. Format 4:5 portrait 1080×1350px. Background color #080C18 (dark navy), subtle radial glow of warm gold light coming from the exact center. Inter or equivalent sans-serif font. Do not invent any values or names not listed below. Country names in Portuguese, with flag emoji next to each one.

LAYOUT: a circular knockout bracket diagram, matching the classic "World Cup circular bracket" format — 16 team flag icons arranged evenly around the outer edge of a circle, connecting lines running inward through each round (oitavas → quartas → semifinal → final) converging on a World Cup trophy icon glowing gold at the exact center.

TEAM PLACEMENT (clockwise starting at top-left, matching the two bracket halves so paired teams sit next to each other):
Top-left arc: 🇨🇦 Canadá, 🇲🇦 Marrocos, 🇵🇾 Paraguai, 🇫🇷 França
Left arc continuing down: 🇧🇪 Bélgica, 🇺🇸 EUA, 🇪🇸 Espanha, 🇵🇹 Portugal
Bottom-right arc: 🇧🇷 Brasil, 🇳🇴 Noruega, 🇲🇽 México, 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra
Right arc continuing up: 🇨🇭 Suíça, 🇨🇴 Colômbia, 🇪🇬 Egito, 🇦🇷 Argentina

LINE COLORS: every connecting line defaults to thin muted grey #334155 (representing the model's favorite advancing automatically). Brazil's own path is drawn as a thick glowing gold/green line (#4ADE80 with gold #FBBF24 glow) from the Brazil icon all the way to the trophy at the center, passing through every round Brazil plays.

OITAVAS (grey lines, connecting each pair to a winner icon one ring further in):
🇨🇦 Canadá vs 🇲🇦 Marrocos → 🇲🇦 Marrocos avança
🇵🇾 Paraguai vs 🇫🇷 França → 🇫🇷 França avança
🇧🇪 Bélgica vs 🇺🇸 EUA → 🇺🇸 EUA avança
🇪🇸 Espanha vs 🇵🇹 Portugal → 🇪🇸 Espanha avança
🇧🇷 Brasil vs 🇳🇴 Noruega → 🇧🇷 Brasil avança (LINHA DOURADA) — small label near this line: "84.2%"
🇲🇽 México vs 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra → 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra avança
🇨🇭 Suíça vs 🇨🇴 Colômbia → 🇨🇴 Colômbia avança
🇪🇬 Egito vs 🇦🇷 Argentina → 🇦🇷 Argentina avança

QUARTAS:
🇲🇦 Marrocos vs 🇫🇷 França → 🇫🇷 França avança
🇺🇸 EUA vs 🇪🇸 Espanha → 🇪🇸 Espanha avança
🇧🇷 Brasil vs 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra → 🇧🇷 Brasil avança (LINHA DOURADA) — small label: "63.5%"
🇨🇴 Colômbia vs 🇦🇷 Argentina → 🇦🇷 Argentina avança

SEMIFINAL:
🇫🇷 França vs 🇪🇸 Espanha → 🇫🇷 França avança
🇧🇷 Brasil vs 🇦🇷 Argentina → 🇧🇷 Brasil avança (LINHA DOURADA) — small label: "64.5%"

FINAL, no centro ao lado do troféu: 🇫🇷 França vs 🇧🇷 Brasil. Desenhar a linha dourada ligando o Brasil ao troféu (esse é o caminho do Brasil até o título). Ao lado do troféu, uma caixa de destaque honesta (card escuro, borda branca, NÃO dourada — pra não sugerir um resultado garantido): "🇫🇷 França 55.7% (favorita) · 🇧🇷 Brasil 44.3% (zebra)"

LEGENDA NO RODAPÉ (small, muted #64748B, horizontal row): linha cinza = favorito do modelo em cada jogo · linha dourada = caminho real do Brasil · o Brasil é zebra na final, não favorito

TOP LABEL (small caps, wide letter-spacing, color #93C5FD, above the circle): COPA DO MUNDO 2026 · O CAMINHO DO BRASIL ATÉ A FINAL

Footer (muted #64748B, very small, below the circle): Model5 · 10.000.000 simulações · pênaltis/prorrogação tratados como 50/50 · chance geral de título do Brasil: 20.2%

---

## Nota sobre o Slide 6

Bracket circular com 16 escudos conectados por linhas é um dos formatos mais difíceis pra IA de geração de imagem acertar de primeira (times trocados de lugar, linha ligada errado, contagem de conexões quebrada). Recomendo gerar e conferir com atenção antes de postar — se sair torto, posso montar a mesma informação como um diagrama HTML/SVG exato (sem risco de erro de posicionamento) pra você usar de referência ou print direto.
