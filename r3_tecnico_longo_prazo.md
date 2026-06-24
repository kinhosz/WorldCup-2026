# Image Prompts — Post Técnico R3: Calibração + Odds de Campeão

Gerador: **Gemini**. Formato: **4:5 retrato, 1080×1350 px**.
Estilo: **Dark navy (#080C18) · Linhas de ranking escuras (#1E293B) · Accent azul (#38BDF8) · Sofascore-inspired.**

**REGRA OBRIGATÓRIA:** Cada prompt abaixo é autossuficiente. Todo texto, número e nome que deve aparecer na imagem está listado explicitamente dentro do prompt. Não inventar. Não alterar números. Renderizar exatamente o que está escrito.

Estrutura: 4 slides.

---

## LEGENDA ÚNICA

```
Modelo retreinado com 48 jogos (R1+R2). Argentina assume a liderança com 18.9%. Holanda deu o maior salto: do #8 para o #2 (+10.7pp). França caiu de 19.6% para 12.3%. Quem leva a taça?

1.000.000 de simulações · resultados R1+R2 já considerados.

#Copa2026 #WorldCup2026 #DataScience #MonteCarlo #IA #Futebol #Previsão
```

---

## SLIDE 1 — Hook

> Portrait image, 4:5, 1080x1350px. Background: very dark navy (#080C18). No borders, no glow. Typography: modern bold sans-serif (Inter or equivalent).
>
> Render this text, in this exact order, vertically centered on the image:
>
> TOP — small uppercase muted (#64748B): "COPA DO MUNDO 2026 · ANÁLISE TÉCNICA"
>
> A thin horizontal line in (#1E293B), full width.
>
> CENTER (stacked, generous vertical spacing):
> Large bold white (#F8FAFC): "Modelo Retreinado"
> Very large bold sky blue (#38BDF8): "Quem vai levantar a taça?"
>
> A thin horizontal line in (#1E293B), ~40% width, centered.
>
> Below, stacked in medium white (#F8FAFC):
> "48 jogos · Rodadas 1 e 2 · 1.000.000 simulações"
>
> A thin horizontal line in (#1E293B), ~40% width, centered.
>
> Below, a small index list in muted (#64748B), left-aligned inside a ~70% width block, centered on the page:
> "2 · O que mudou na calibração"
> "3 · Favoritos ao Título · Top 10"
> "4 · Surpresas e Decepções"
>
> BOTTOM — small uppercase muted (#64748B): "COPA 2026 · SIMULAÇÃO MONTE CARLO"

---

## SLIDE 2 — O que mudou na calibração

> Professional sports data analysis infographic. Portrait, 4:5, 1080x1350px. Background: very dark navy (#080C18). Typography: modern bold sans-serif (Inter or equivalent).
>
> At the very top, centered: small uppercase muted (#64748B): "O QUE MUDOU · ANTES vs DEPOIS DA CALIBRAÇÃO"
> Below: thin full-width line (#1E293B).
>
> A dark elevated card (#1E293B) with subtle shadow, centered, ~88% width, rounded corners.
>
> Inside the card, three sections separated by thin divider lines (#334155):
>
> --- SECTION 1: DADOS DE TREINO ---
> Small bold sky blue (#38BDF8) uppercase: "DADOS DE TREINO"
> Two rows:
> Small muted (#64748B): "Antes (pós-R1)" · white (#F8FAFC): "24 jogos"
> Small muted (#64748B): "Depois (pós-R2)" · bold white (#F8FAFC): "48 jogos"
>
> --- THIN DIVIDER (#334155) ---
>
> --- SECTION 2: PESOS GLOBAIS ---
> Small bold sky blue (#38BDF8) uppercase: "PESOS GLOBAIS — O QUE MUDOU"
> Five rows. Each row: parameter name (muted #64748B) · antes value (muted #94A3B8) · arrow → · depois value (bold white #F8FAFC):
> "BASE_XG         1.172  →  1.144"
> "Ataque (ATT)    0.853  →  0.715"
> "Meio (MID off)  0.147  →  0.285"
> "Meio (MID def)  0.170  →  0.503"
> "Goleiro (GK)    0.280  →  0.050"
>
> --- THIN DIVIDER (#334155) ---
>
> --- SECTION 3: PERFORMANCE ---
> Small bold sky blue (#38BDF8) uppercase: "PERFORMANCE DO MODELO"
> Four rows:
> Small muted (#64748B): "Prob score R1" · white (#F8FAFC): "47.1%"
> Small muted (#64748B): "Prob score R2" · bold white (#F8FAFC): "52.5%"
> Small muted (#64748B): "Resultado correto R1+R2" · bold white (#F8FAFC): "29/48  (60%)"
> Small muted (#64748B): "Baseline aleatório" · muted (#94A3B8): "33.3%"
>
> BOTTOM outside card: small muted (#64748B): "1.000.000 simulações · Modelo Monte Carlo"

---

## SLIDE 3 — Favoritos ao Título (Top 10)

> Professional sports ranking infographic. Portrait, 4:5, 1080x1350px. Background: very dark navy (#080C18). Typography: modern bold sans-serif (Inter or equivalent). The entire image is a vertical ranking table — no outer card, just the dark background with rows.
>
> At the very top, centered:
> Bold white (#F8FAFC), large: "COPA DO MUNDO 2026 · ODDS DE CAMPEÃO"
> Below in smaller muted (#94A3B8): "Antes vs depois da calibração · pós-Rodada 2"
>
> Below that, a header row in very small uppercase muted (#64748B), aligned to match the columns below:
> "#   SELEÇÃO          ANTES    AGORA     Δ"
>
> Then 10 rows, each a rounded-rectangle dark card (#1E293B) with ~90% width, small vertical gap between rows. Each row contains:
>
> — A small rounded rank badge on the far left with the rank number in muted text
> — Flag emoji + team name in white (#F8FAFC), medium bold
> — ANTES value aligned to the ANTES column, in muted gray (#94A3B8)
> — AGORA value aligned to the AGORA column, in bold white (#F8FAFC), slightly larger than ANTES
> — Δ value aligned to the Δ column: green (#22C55E) with ↑ arrow if positive, red (#EF4444) with ↓ arrow if negative, gray (#94A3B8) with → if near zero
> — When position change ≥ 2, show a small pill badge after Δ: green background for gains, red background for losses, white text inside (e.g. "↑6 pos")
>
> Row 1 has a green (#22C55E) left border accent (biggest absolute gain).
> Row 4 has a red (#EF4444) left border accent (biggest absolute drop).
>
> Do not invent any values. Render exactly:
>
> Row 1:  "#1"  "🇦🇷 Argentina"    "14.2%"  "18.9%"  "↑ +4.7%"  [green badge "↑1 pos"]
> Row 2:  "#2"  "🇳🇱 Netherlands"  " 4.0%"  "14.6%"  "↑ +10.7%" [green badge "↑6 pos"]
> Row 3:  "#3"  "🇵🇹 Portugal"     " 9.2%"  "14.1%"  "↑ +4.9%"  [green badge "↑2 pos"]
> Row 4:  "#4"  "🇫🇷 France"       "19.6%"  "12.3%"  "↓ −7.3%"  [red badge "↓3 pos"]
> Row 5:  "#5"  "🇧🇷 Brazil"       "13.8%"  " 9.5%"  "↓ −4.2%"  [red badge "↓2 pos"]
> Row 6:  "#6"  "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England"       " 9.5%"  " 8.8%"  "↓ −0.7%"  [red badge "↓2 pos"]
> Row 7:  "#7"  "🇩🇪 Germany"      " 4.5%"  " 7.9%"  "↑ +3.4%"  [no badge — same position]
> Row 8:  "#8"  "🇨🇴 Colombia"     " 6.1%"  " 2.1%"  "↓ −4.0%"  [red badge "↓2 pos"]
> Row 9:  "#9"  "🇪🇸 Spain"        " 2.7%"  " 1.8%"  "↓ −0.9%"  [green badge "↑1 pos"]
> Row 10: "#10" "🇯🇵 Japan"        " 0.4%"  " 1.7%"  "↑ +1.3%"  [green badge "↑11 pos"]
>
> Below the 10 rows, centered small muted (#64748B): "Demais 38 seleções somam 8.3%"
>
> At the very bottom, centered small muted (#64748B):
> "Modelo pós-R1 → SA+att_only calibrado com 48 jogos (R1+R2)"
> "1.000.000 simulações · atualizado após cada rodada"

---

## SLIDE 4 — Surpresas e Decepções

> Professional sports editorial infographic. Portrait, 4:5, 1080x1350px. Background: very dark navy (#080C18). One dark elevated card (#1E293B) with subtle shadow, centered, ~90% width, rounded corners. Typography: modern bold sans-serif (Inter or equivalent).
>
> At the very top, centered: small uppercase muted (#64748B): "QUEM SUPEROU AS EXPECTATIVAS · R1+R2"
> Below: thin full-width line (#1E293B).
>
> Inside the card:
>
> Small muted (#94A3B8) centered: "att_bias: razão entre gols marcados e esperados pelo modelo. >1.0 = marcou mais que o previsto."
>
> Thin divider (#334155).
>
> Small bold sky blue (#38BDF8) uppercase left-aligned: "ACIMA DO ESPERADO"
>
> Five rows. Each row: flag emoji + team name (white #F8FAFC) · short horizontal bar in green (#22C55E), width proportional to value (max = Japan 1.44) · value bold green (#22C55E):
> "🇯🇵 Japan         ████████  1.44"
> "🇨🇦 Canada        ███████   1.39"
> "🇩🇪 Germany       ██████    1.37"
> "🇳🇱 Netherlands   ██████    1.35"
> "🇸🇪 Sweden        █████     1.33"
>
> Thin divider (#334155).
>
> Small bold (#94A3B8) uppercase left-aligned: "ABAIXO DO ESPERADO"
>
> Five rows. Each row: flag emoji + team name (white #F8FAFC) · short horizontal bar in red (#EF4444) · value bold red (#EF4444):
> "🇹🇷 Turkey        ████████  0.20"
> "🇪🇨 Ecuador       ████████  0.20"
> "🇧🇪 Belgium       ███████   0.27"
> "🇵🇦 Panama        ██████    0.31"
> "🇬🇭 Ghana         ████      0.53"
>
> Thin divider (#334155).
>
> Small italic muted (#64748B) centered: "Calibrado com 48 jogos via Simulated Annealing · λ=1.5"
>
> BOTTOM outside card: small muted (#64748B): "1.000.000 simulações · Modelo Monte Carlo"
