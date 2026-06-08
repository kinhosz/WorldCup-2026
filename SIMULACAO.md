# Copa do Mundo 2026 — Simulação Monte Carlo

**Data:** 08/06/2026
**Simulações realizadas:** 1,000,000
**Seed:** aleatória (resultados variam a cada execução)

---

## 1. O que fizemos

Construímos um simulador da Copa do Mundo 2026 capaz de jogar um torneio completo — fase de grupos, oitavas, round of 16, quartas, semis e final — usando dados reais dos jogadores convocados como base para calcular a força de cada seleção.

O objetivo foi estimar probabilidades de título para cada um dos 48 países, levando em conta o chaveamento oficial da FIFA, a regra dos melhores 8 terceiros colocados e os detalhes do bracket de mata-mata.

---

## 2. Pipeline de dados

### 2.1 Fonte dos scores

Para cada seleção, calculamos um score em quatro setores: **goleiro**, **defesa**, **meio-campo** e **ataque**. A estratégia em cascata foi:

| Tier | Fonte | Cobertura |
|------|-------|-----------|
| 1° | **FIFA 22** — atributos por setor | ~80% dos jogadores |
| 2° | **Transfermarket** — valor de mercado convertido para rating | complemento |
| 3° | **Mediana global do setor** | jogadores sem dados em nenhuma fonte |

A conversão de valor de mercado para rating usa uma fórmula log-linear calibrada nos extremos:
- €1M → 65 pontos
- €180M → 91 pontos

### 2.2 Atributos FIFA 22 por setor

| Setor | Atributos usados |
|-------|-----------------|
| Goleiro | `goalkeeping_diving`, `goalkeeping_reflexes`, `goalkeeping_handling`, `goalkeeping_positioning` |
| Defesa | `defending`, `physic` |
| Meio | `passing`, `dribbling` |
| Ataque | `shooting`, `pace` |

### 2.3 Top-K por setor

Para cada setor, pegamos os **K melhores jogadores** (por rating) e calculamos a média geométrica (log-mean):

| Setor | K |
|-------|---|
| Goleiro | 1 |
| Defesa | 4 |
| Meio | 4 |
| Ataque | 3 |

Os scores brutos são então normalizados com **min-max** entre as 48 seleções → intervalo [0, 1].

### 2.4 Matching de nomes

O matching entre nomes dos arquivos de convocação e os datasets (FIFA 22 / TM) usa:
- `SequenceMatcher` (ratio de similaridade de strings)
- Token overlap (interseção de palavras)
- Filtro por nacionalidade (pool da seleção nacional + cidadania)
- Strip de sufixos como *Junior*, *Sr*, *Jr*
- Threshold mínimo de 0.72

---

## 3. Fórmula xG

Para um confronto **A × B**, o xG (gols esperados) de cada time é:

```
offense_A    = 0.7 × attack_A    + 0.3 × midfield_A
resistance_B = 0.6 × defense_B  + 0.2 × goalkeeper_B + 0.2 × midfield_B

xG_A = 1.3 × (offense_A / resistance_B)
```

Constantes de segurança:
- `BASE_XG = 1.3` — média histórica de gols por time por jogo em Copas
- `RES_FLOOR = 0.10` — piso da resistência (evita divisão por zero)
- `MAX_XG = 8.0` — teto dos gols esperados

---

## 4. Estrutura da simulação

### Fase de grupos
- 12 grupos de 4 times (A–L), round-robin
- Pontuação: vitória=3, empate=1, derrota=0
- Classificam: 1º e 2º de cada grupo (24 times) + 8 melhores terceiros
- Gols simulados via distribuição de Poisson com o xG calculado
- Critérios de desempate: pontos → saldo de gols → gols pró → vitórias → aleatório

### Mata-mata
- **Round of 32** → Round of 16 → Quartas → Semis → Final
- Bracket oficial da FIFA (partidas 73–104)
- Empate no tempo normal → prorrogação (30 min, xG × 0.35) → pênaltis (50/50)
- Atribuição dos slots de 3°s colocados via backtracking com as restrições oficiais de grupos elegíveis

### Execução
```bash
python3 scripts/build_team_scores.py   # gera output/team_scores.json
python3 scripts/simulate.py 10000      # roda 10k simulações
python3 scripts/generate_report.py     # gera este documento
```

---

---

## 5. Scores atuais das seleções

| Seleção | xG vs médio | Ataque | Meio | Defesa | Goleiro |
|---------|------------|--------|------|--------|---------|
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

---

## 6. Resultados — 1,000,000 simulações

| # | Seleção | Grupo | Campeão | Finalista | Semi | QF | R16 |
|---|---------|-------|---------|-----------|------|----|-----|
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
| 15 | Côte d'Ivoire | E | 0.4% | 1.6% | 5.4% | 15.5% | 57.0% |
| 16 | Croatia | L | 0.2% | 1.1% | 4.3% | 11.9% | 28.6% |
| 17 | Turkey | D | 0.2% | 1.1% | 4.8% | 18.5% | 55.1% |
| 18 | Czech Republic | A | 0.1% | 0.8% | 3.4% | 15.4% | 57.6% |
| 19 | Congo | K | 0.1% | 0.7% | 3.4% | 12.2% | 26.1% |
| 20 | Japan | F | 0.1% | 0.6% | 2.2% | 8.5% | 23.2% |

### Classificação por grupo (R32)

| Grupo | 1° aprox. | 2° aprox. | 3° aprox. | 4° aprox. |
|-------|-----------|-----------|-----------|-----------|
| A | South Korea 92% | Czech Republic 90% | Mexico 65% | South Africa 26% |
| B | Switzerland 100% | Qatar 81% | Bosnia-Herzegovina 49% | Canada 26% |
| C | Brazil 100% | Morocco 98% | Scotland 59% | Haiti 2% |
| D | Turkey 93% | USA 93% | Australia 63% | Paraguay 22% |
| E | Germany 100% | Côte d'Ivoire 100% | Ecuador 85% | Curacao 0% |
| F | Netherlands 100% | Japan 87% | Sweden 85% | Tunisia 6% |
| G | Belgium 100% | Egypt 99% | Iran 51% | New Zealand 1% |
| H | Spain 100% | Uruguay 100% | Cape Verde 58% | Saudi Arabia 1% |
| I | France 100% | Senegal 96% | Norway 65% | Iraq 2% |
| J | Argentina 100% | Algeria 76% | Austria 72% | Jordan 20% |
| K | Portugal 100% | Colombia 98% | Congo 79% | Uzbekistan 2% |
| L | England 100% | Croatia 90% | Ghana 58% | Panama 14% |

---

## 7. Simulações individuais

Quatro exemplos de torneios completos rodados individualmente.
O vencedor de cada partida está em **negrito**. Placar sempre mandante–visitante.

---

### 7.1 Simulação aleatória

**Campeão: Belgium**

### FASE DE GRUPOS

**Grupo A**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Czech Republic | 7 | +4 | 5 | → R32
| 2 | South Korea | 4 | +2 | 5 | → R32
| 3 | Mexico | 4 | -1 | 2 | → R32 (3°)
| 4 | South Africa | 1 | -5 | 2 | ✗

Jogos:
- Mexico 1–1 South Africa
- Mexico 1–0 South Korea
- Mexico 0–2 Czech Republic
- South Africa 1–4 South Korea
- South Africa 0–2 Czech Republic
- South Korea 1–1 Czech Republic

**Grupo B**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Switzerland | 9 | +6 | 11 | → R32
| 2 | Bosnia-Herzegovina | 6 | +2 | 9 | → R32
| 3 | Qatar | 3 | +0 | 6 | → R32 (3°)
| 4 | Canada | 0 | -8 | 5 | ✗

Jogos:
- Canada 2–4 Bosnia-Herzegovina
- Canada 2–4 Qatar
- Canada 1–5 Switzerland
- Bosnia-Herzegovina 2–1 Qatar
- Bosnia-Herzegovina 3–4 Switzerland
- Qatar 1–2 Switzerland

**Grupo C**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Brazil | 9 | +5 | 5 | → R32
| 2 | Morocco | 6 | +5 | 8 | → R32
| 3 | Scotland | 3 | -1 | 4 | → R32 (3°)
| 4 | Haiti | 0 | -9 | 1 | ✗

Jogos:
- Brazil 3–0 Morocco
- Brazil 1–0 Haiti
- Brazil 1–0 Scotland
- Morocco 5–0 Haiti
- Morocco 3–0 Scotland
- Haiti 1–4 Scotland

**Grupo D**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Australia | 9 | +4 | 5 | → R32
| 2 | USA | 4 | +3 | 4 | → R32
| 3 | Turkey | 4 | +1 | 3 | → R32 (3°)
| 4 | Paraguay | 0 | -8 | 0 | ✗

Jogos:
- USA 4–0 Paraguay
- USA 0–1 Australia
- USA 0–0 Turkey
- Paraguay 0–2 Australia
- Paraguay 0–2 Turkey
- Australia 2–1 Turkey

**Grupo E**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Germany | 9 | +11 | 11 | → R32
| 2 | Ecuador | 4 | +1 | 4 | → R32
| 3 | Côte d'Ivoire | 4 | -2 | 2 | → R32 (3°)
| 4 | Curacao | 0 | -10 | 0 | ✗

Jogos:
- Germany 4–0 Curacao
- Germany 4–0 Côte d'Ivoire
- Germany 3–0 Ecuador
- Curacao 0–2 Côte d'Ivoire
- Curacao 0–4 Ecuador
- Côte d'Ivoire 0–0 Ecuador

**Grupo F**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Netherlands | 7 | +9 | 10 | → R32
| 2 | Japan | 5 | +1 | 4 | → R32
| 3 | Sweden | 4 | +2 | 8 | → R32 (3°)
| 4 | Tunisia | 0 | -12 | 2 | ✗

Jogos:
- Netherlands 0–0 Japan
- Netherlands 3–1 Sweden
- Netherlands 7–0 Tunisia
- Japan 2–2 Sweden
- Japan 2–1 Tunisia
- Sweden 5–1 Tunisia

**Grupo G**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Belgium | 9 | +19 | 23 | → R32
| 2 | Egypt | 6 | +10 | 18 | → R32
| 3 | Iran | 3 | -9 | 6 | → R32 (3°)
| 4 | New Zealand | 0 | -20 | 3 | ✗

Jogos:
- Belgium 8–4 Egypt
- Belgium 7–0 Iran
- Belgium 8–0 New Zealand
- Egypt 5–0 Iran
- Egypt 9–0 New Zealand
- Iran 6–3 New Zealand

**Grupo H**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Spain | 9 | +20 | 20 | → R32
| 2 | Uruguay | 6 | +6 | 12 | → R32
| 3 | Cape Verde | 3 | -3 | 3 | → R32 (3°)
| 4 | Saudi Arabia | 0 | -23 | 1 | ✗

Jogos:
- Spain 3–0 Cape Verde
- Spain 14–0 Saudi Arabia
- Spain 3–0 Uruguay
- Cape Verde 1–0 Saudi Arabia
- Cape Verde 2–3 Uruguay
- Saudi Arabia 1–9 Uruguay

**Grupo I**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | France | 9 | +12 | 13 | → R32
| 2 | Norway | 4 | -2 | 5 | → R32
| 3 | Senegal | 3 | +0 | 8 | → R32 (3°)
| 4 | Iraq | 1 | -10 | 3 | ✗

Jogos:
- France 4–1 Senegal
- France 6–0 Iraq
- France 3–0 Norway
- Senegal 5–1 Iraq
- Senegal 2–3 Norway
- Iraq 2–2 Norway

**Grupo J**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Argentina | 6 | +6 | 8 | → R32
| 2 | Algeria | 5 | +1 | 3 | → R32
| 3 | Austria | 2 | -2 | 2 | → R32 (3°)
| 4 | Jordan | 2 | -5 | 3 | ✗

Jogos:
- Argentina 0–1 Algeria
- Argentina 3–1 Austria
- Argentina 5–0 Jordan
- Algeria 0–0 Austria
- Algeria 2–2 Jordan
- Austria 1–1 Jordan

**Grupo K**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Portugal | 9 | +19 | 20 | → R32
| 2 | Colombia | 6 | +0 | 6 | → R32
| 3 | Uzbekistan | 3 | -11 | 3 | → R32 (3°)
| 4 | Congo | 0 | -8 | 1 | ✗

Jogos:
- Portugal 6–0 Congo
- Portugal 10–1 Uzbekistan
- Portugal 4–0 Colombia
- Congo 0–1 Uzbekistan
- Congo 1–2 Colombia
- Uzbekistan 1–4 Colombia

**Grupo L**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | England | 9 | +7 | 7 | → R32
| 2 | Croatia | 4 | +2 | 7 | → R32
| 3 | Ghana | 4 | -1 | 3 | → R32 (3°)
| 4 | Panama | 0 | -8 | 2 | ✗

Jogos:
- England 3–0 Croatia
- England 2–0 Ghana
- England 2–0 Panama
- Croatia 1–1 Ghana
- Croatia 6–1 Panama
- Ghana 2–1 Panama

**8 melhores 3ºs lugares classificados:**
- Sweden (Grupo F)
- Turkey (Grupo D)
- Ghana (Grupo L)
- Mexico (Grupo A)
- Côte d'Ivoire (Grupo E)
- Senegal (Grupo I)
- Qatar (Grupo B)
- Scotland (Grupo C)

### OITAVAS DE FINAL (Round of 32)

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M73 | **South Korea** | 8–0 | Bosnia-Herzegovina | 90' |
| M74 | Germany | 1–2 | **Sweden** | 90' |
| M75 | Netherlands | 1–2 | **Morocco** | 90' |
| M76 | **Brazil** | 3–0 | Japan | 90' |
| M77 | France | 1–1 pen. | **Turkey** | PEN |
| M78 | Ecuador | 0–3 | **Norway** | 90' |
| M79 | **Czech Republic** | 0–0 pen. | Scotland | PEN |
| M80 | **England** | 2–0 | Côte d'Ivoire | 90' |
| M81 | Australia | 0–2 | **Qatar** | 90' |
| M82 | **Belgium** | 3–0 | Mexico | 90' |
| M83 | **Colombia** | 2–1 (1–1 AET) | Croatia | AET |
| M84 | Spain | 3–4 | **Algeria** | 90' |
| M85 | Switzerland | 1–2 | **Senegal** | 90' |
| M86 | Argentina | 0–2 | **Uruguay** | 90' |
| M87 | **Portugal** | 6–1 | Ghana | 90' |
| M88 | USA | 2–3 (1–1 AET) | **Egypt** | AET |

### ROUND OF 16

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M89 | **Sweden** | 2–1 | Turkey | 90' |
| M90 | South Korea | 1–2 | **Morocco** | 90' |
| M91 | **Brazil** | 6–2 | Norway | 90' |
| M92 | Czech Republic | 1–2 (1–1 AET) | **England** | AET |
| M93 | **Colombia** | 3–2 (2–2 AET) | Algeria | AET |
| M94 | Qatar | 0–3 | **Belgium** | 90' |
| M95 | **Uruguay** | 3–2 | Egypt | 90' |
| M96 | Senegal | 1–3 | **Portugal** | 90' |

### QUARTAS DE FINAL

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M97 | Sweden | 0–1 | **Morocco** | 90' |
| M98 | Colombia | 1–2 | **Belgium** | 90' |
| M99 | Brazil | 0–2 | **England** | 90' |
| M100 | Uruguay | 0–2 | **Portugal** | 90' |

### SEMIFINAIS

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M101 | Morocco | 2–2 pen. | **Belgium** | PEN |
| M102 | England | 0–1 | **Portugal** | 90' |

### FINAL

**Belgium** 3–2 (1–1 AET) **Portugal**

🏆 **CAMPEÃO: BELGIUM**

---

### 7.2 Brasil campeão 🇧🇷

**Campeão: Brazil**

### FASE DE GRUPOS

**Grupo A**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | South Korea | 9 | +8 | 13 | → R32
| 2 | Mexico | 4 | -2 | 3 | → R32
| 3 | Czech Republic | 2 | -2 | 3 | → R32 (3°)
| 4 | South Africa | 1 | -4 | 2 | ✗

Jogos:
- Mexico 1–0 South Africa
- Mexico 2–5 South Korea
- Mexico 0–0 Czech Republic
- South Africa 1–4 South Korea
- South Africa 1–1 Czech Republic
- South Korea 4–2 Czech Republic

**Grupo B**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Switzerland | 9 | +13 | 15 | → R32
| 2 | Qatar | 3 | +0 | 6 | → R32
| 3 | Canada | 3 | -5 | 8 | → R32 (3°)
| 4 | Bosnia-Herzegovina | 3 | -8 | 6 | ✗

Jogos:
- Canada 3–5 Bosnia-Herzegovina
- Canada 3–2 Qatar
- Canada 2–6 Switzerland
- Bosnia-Herzegovina 1–4 Qatar
- Bosnia-Herzegovina 0–7 Switzerland
- Qatar 0–2 Switzerland

**Grupo C**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Brazil | 9 | +8 | 9 | → R32
| 2 | Morocco | 4 | +3 | 8 | → R32
| 3 | Scotland | 4 | +1 | 5 | → R32 (3°)
| 4 | Haiti | 0 | -12 | 0 | ✗

Jogos:
- Brazil 3–1 Morocco
- Brazil 4–0 Haiti
- Brazil 2–0 Scotland
- Morocco 5–0 Haiti
- Morocco 2–2 Scotland
- Haiti 0–3 Scotland

**Grupo D**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | USA | 9 | +9 | 9 | → R32
| 2 | Turkey | 6 | +1 | 4 | → R32
| 3 | Australia | 3 | -2 | 4 | → R32 (3°)
| 4 | Paraguay | 0 | -8 | 0 | ✗

Jogos:
- USA 3–0 Paraguay
- USA 4–0 Australia
- USA 2–0 Turkey
- Paraguay 0–3 Australia
- Paraguay 0–2 Turkey
- Australia 1–2 Turkey

**Grupo E**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Germany | 7 | +7 | 10 | → R32
| 2 | Côte d'Ivoire | 6 | +7 | 10 | → R32
| 3 | Ecuador | 4 | +1 | 5 | → R32 (3°)
| 4 | Curacao | 0 | -15 | 0 | ✗

Jogos:
- Germany 6–0 Curacao
- Germany 2–1 Côte d'Ivoire
- Germany 2–2 Ecuador
- Curacao 0–7 Côte d'Ivoire
- Curacao 0–2 Ecuador
- Côte d'Ivoire 2–1 Ecuador

**Grupo F**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Netherlands | 5 | +4 | 8 | → R32
| 2 | Tunisia | 4 | -1 | 4 | → R32
| 3 | Japan | 3 | +0 | 4 | → R32 (3°)
| 4 | Sweden | 2 | -3 | 3 | ✗

Jogos:
- Netherlands 2–2 Japan
- Netherlands 2–2 Sweden
- Netherlands 4–0 Tunisia
- Japan 1–1 Sweden
- Japan 1–1 Tunisia
- Sweden 0–3 Tunisia

**Grupo G**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Egypt | 7 | +13 | 19 | → R32
| 2 | Belgium | 7 | +12 | 15 | → R32
| 3 | New Zealand | 3 | -13 | 5 | → R32 (3°)
| 4 | Iran | 0 | -12 | 5 | ✗

Jogos:
- Belgium 3–3 Egypt
- Belgium 3–0 Iran
- Belgium 9–0 New Zealand
- Egypt 10–2 Iran
- Egypt 6–1 New Zealand
- Iran 3–4 New Zealand

**Grupo H**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Spain | 7 | +15 | 18 | → R32
| 2 | Uruguay | 7 | +11 | 14 | → R32
| 3 | Cape Verde | 1 | -9 | 4 | → R32 (3°)
| 4 | Saudi Arabia | 1 | -17 | 4 | ✗

Jogos:
- Spain 7–0 Cape Verde
- Spain 9–1 Saudi Arabia
- Spain 2–2 Uruguay
- Cape Verde 3–3 Saudi Arabia
- Cape Verde 1–3 Uruguay
- Saudi Arabia 0–9 Uruguay

**Grupo I**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | France | 7 | +6 | 11 | → R32
| 2 | Senegal | 7 | +5 | 11 | → R32
| 3 | Norway | 3 | -2 | 7 | → R32 (3°)
| 4 | Iraq | 0 | -9 | 0 | ✗

Jogos:
- France 3–3 Senegal
- France 3–0 Iraq
- France 5–2 Norway
- Senegal 4–0 Iraq
- Senegal 4–3 Norway
- Iraq 0–2 Norway

**Grupo J**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Austria | 6 | +5 | 7 | → R32
| 2 | Argentina | 6 | +2 | 5 | → R32
| 3 | Jordan | 3 | -3 | 3 | → R32 (3°)
| 4 | Algeria | 3 | -4 | 3 | ✗

Jogos:
- Argentina 3–1 Algeria
- Argentina 1–0 Austria
- Argentina 1–2 Jordan
- Algeria 0–4 Austria
- Algeria 2–0 Jordan
- Austria 3–1 Jordan

**Grupo K**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Colombia | 7 | +5 | 8 | → R32
| 2 | Portugal | 7 | +3 | 5 | → R32
| 3 | Uzbekistan | 3 | -2 | 8 | → R32 (3°)
| 4 | Congo | 0 | -6 | 4 | ✗

Jogos:
- Portugal 2–1 Congo
- Portugal 3–1 Uzbekistan
- Portugal 0–0 Colombia
- Congo 2–5 Uzbekistan
- Congo 1–3 Colombia
- Uzbekistan 2–5 Colombia

**Grupo L**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | England | 7 | +4 | 7 | → R32
| 2 | Croatia | 5 | +4 | 6 | → R32
| 3 | Ghana | 2 | -1 | 6 | → R32 (3°)
| 4 | Panama | 1 | -7 | 1 | ✗

Jogos:
- England 0–0 Croatia
- England 4–3 Ghana
- England 3–0 Panama
- Croatia 2–2 Ghana
- Croatia 4–0 Panama
- Ghana 1–1 Panama

**8 melhores 3ºs lugares classificados:**
- Ecuador (Grupo E)
- Scotland (Grupo C)
- Japan (Grupo F)
- Uzbekistan (Grupo K)
- Norway (Grupo I)
- Australia (Grupo D)
- Jordan (Grupo J)
- Canada (Grupo B)

### OITAVAS DE FINAL (Round of 32)

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M73 | Mexico | 0–2 | **Qatar** | 90' |
| M74 | **Germany** | 3–1 | Scotland | 90' |
| M75 | **Netherlands** | 2–1 | Morocco | 90' |
| M76 | **Brazil** | 6–0 | Tunisia | 90' |
| M77 | **France** | 3–1 | Japan | 90' |
| M78 | Côte d'Ivoire | 1–2 (1–1 AET) | **Senegal** | AET |
| M79 | South Korea | 2–2 pen. | **Ecuador** | PEN |
| M80 | **England** | 2–0 | Uzbekistan | 90' |
| M81 | **USA** | 12–3 | Canada | 90' |
| M82 | **Egypt** | 7–5 | Norway | 90' |
| M83 | **Portugal** | 4–1 | Croatia | 90' |
| M84 | Spain | 0–2 | **Argentina** | 90' |
| M85 | **Switzerland** | 2–1 | Jordan | 90' |
| M86 | Austria | 0–3 | **Uruguay** | 90' |
| M87 | **Colombia** | 6–2 | Australia | 90' |
| M88 | **Turkey** | 1–0 | Belgium | 90' |

### ROUND OF 16

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M89 | Germany | 0–1 | **France** | 90' |
| M90 | Qatar | 0–10 | **Netherlands** | 90' |
| M91 | **Brazil** | 4–0 | Senegal | 90' |
| M92 | Ecuador | 0–7 | **England** | 90' |
| M93 | **Portugal** | 2–0 | Argentina | 90' |
| M94 | **USA** | 3–2 | Egypt | 90' |
| M95 | Uruguay | 0–1 | **Turkey** | 90' |
| M96 | **Switzerland** | 3–2 | Colombia | 90' |

### QUARTAS DE FINAL

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M97 | **France** | 1–1 pen. | Netherlands | PEN |
| M98 | **Portugal** | 3–1 (1–1 AET) | USA | AET |
| M99 | **Brazil** | 3–1 | England | 90' |
| M100 | Turkey | 0–3 | **Switzerland** | 90' |

### SEMIFINAIS

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M101 | France | 1–4 | **Portugal** | 90' |
| M102 | **Brazil** | 2–1 | Switzerland | 90' |

### FINAL

**Portugal** 1–2 **Brazil**

🏆 **CAMPEÃO: BRAZIL**

---

### 7.3 França campeã 🇫🇷

**Campeão: France**

### FASE DE GRUPOS

**Grupo A**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Mexico | 7 | +4 | 5 | → R32
| 2 | Czech Republic | 5 | +2 | 6 | → R32
| 3 | South Korea | 2 | -1 | 5 | → R32 (3°)
| 4 | South Africa | 1 | -5 | 4 | ✗

Jogos:
- Mexico 3–0 South Africa
- Mexico 2–1 South Korea
- Mexico 0–0 Czech Republic
- South Africa 2–2 South Korea
- South Africa 2–4 Czech Republic
- South Korea 2–2 Czech Republic

**Grupo B**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Qatar | 9 | +5 | 9 | → R32
| 2 | Switzerland | 6 | +5 | 9 | → R32
| 3 | Bosnia-Herzegovina | 1 | -4 | 5 | → R32 (3°)
| 4 | Canada | 1 | -6 | 6 | ✗

Jogos:
- Canada 2–2 Bosnia-Herzegovina
- Canada 3–5 Qatar
- Canada 1–5 Switzerland
- Bosnia-Herzegovina 1–3 Qatar
- Bosnia-Herzegovina 2–4 Switzerland
- Qatar 1–0 Switzerland

**Grupo C**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Brazil | 9 | +11 | 11 | → R32
| 2 | Morocco | 6 | +5 | 6 | → R32
| 3 | Scotland | 3 | -4 | 1 | → R32 (3°)
| 4 | Haiti | 0 | -12 | 0 | ✗

Jogos:
- Brazil 1–0 Morocco
- Brazil 7–0 Haiti
- Brazil 3–0 Scotland
- Morocco 4–0 Haiti
- Morocco 2–0 Scotland
- Haiti 0–1 Scotland

**Grupo D**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Turkey | 7 | +2 | 3 | → R32
| 2 | Australia | 6 | +2 | 5 | → R32
| 3 | USA | 4 | +3 | 6 | → R32 (3°)
| 4 | Paraguay | 0 | -7 | 1 | ✗

Jogos:
- USA 4–0 Paraguay
- USA 1–2 Australia
- USA 1–1 Turkey
- Paraguay 1–3 Australia
- Paraguay 0–1 Turkey
- Australia 0–1 Turkey

**Grupo E**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Côte d'Ivoire | 7 | +6 | 7 | → R32
| 2 | Germany | 6 | +4 | 6 | → R32
| 3 | Ecuador | 4 | +5 | 8 | → R32 (3°)
| 4 | Curacao | 0 | -15 | 0 | ✗

Jogos:
- Germany 4–0 Curacao
- Germany 0–2 Côte d'Ivoire
- Germany 2–0 Ecuador
- Curacao 0–4 Côte d'Ivoire
- Curacao 0–7 Ecuador
- Côte d'Ivoire 1–1 Ecuador

**Grupo F**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Netherlands | 9 | +6 | 7 | → R32
| 2 | Japan | 4 | +3 | 6 | → R32
| 3 | Sweden | 4 | -1 | 4 | → R32 (3°)
| 4 | Tunisia | 0 | -8 | 3 | ✗

Jogos:
- Netherlands 2–0 Japan
- Netherlands 2–0 Sweden
- Netherlands 3–1 Tunisia
- Japan 1–1 Sweden
- Japan 5–0 Tunisia
- Sweden 3–2 Tunisia

**Grupo G**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Belgium | 9 | +12 | 14 | → R32
| 2 | Egypt | 6 | +8 | 12 | → R32
| 3 | Iran | 3 | -7 | 3 | → R32 (3°)
| 4 | New Zealand | 0 | -13 | 1 | ✗

Jogos:
- Belgium 3–1 Egypt
- Belgium 6–0 Iran
- Belgium 5–1 New Zealand
- Egypt 4–1 Iran
- Egypt 7–0 New Zealand
- Iran 2–0 New Zealand

**Grupo H**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Uruguay | 9 | +6 | 8 | → R32
| 2 | Spain | 6 | +10 | 14 | → R32
| 3 | Cape Verde | 3 | -1 | 7 | → R32 (3°)
| 4 | Saudi Arabia | 0 | -15 | 4 | ✗

Jogos:
- Spain 5–1 Cape Verde
- Spain 8–1 Saudi Arabia
- Spain 1–2 Uruguay
- Cape Verde 6–2 Saudi Arabia
- Cape Verde 0–1 Uruguay
- Saudi Arabia 1–5 Uruguay

**Grupo I**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | France | 9 | +8 | 9 | → R32
| 2 | Senegal | 6 | +6 | 9 | → R32
| 3 | Norway | 3 | -4 | 9 | → R32 (3°)
| 4 | Iraq | 0 | -10 | 2 | ✗

Jogos:
- France 3–0 Senegal
- France 1–0 Iraq
- France 5–1 Norway
- Senegal 3–0 Iraq
- Senegal 6–0 Norway
- Iraq 2–8 Norway

**Grupo J**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Argentina | 7 | +6 | 7 | → R32
| 2 | Algeria | 6 | -3 | 3 | → R32
| 3 | Jordan | 3 | -1 | 3 | → R32 (3°)
| 4 | Austria | 1 | -2 | 0 | ✗

Jogos:
- Argentina 5–0 Algeria
- Argentina 0–0 Austria
- Argentina 2–1 Jordan
- Algeria 1–0 Austria
- Algeria 2–1 Jordan
- Austria 0–1 Jordan

**Grupo K**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Portugal | 7 | +7 | 12 | → R32
| 2 | Colombia | 6 | +6 | 13 | → R32
| 3 | Congo | 4 | +2 | 13 | → R32 (3°)
| 4 | Uzbekistan | 0 | -15 | 1 | ✗

Jogos:
- Portugal 4–4 Congo
- Portugal 6–0 Uzbekistan
- Portugal 2–1 Colombia
- Congo 5–0 Uzbekistan
- Congo 4–7 Colombia
- Uzbekistan 1–5 Colombia

**Grupo L**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | England | 9 | +13 | 14 | → R32
| 2 | Croatia | 6 | +1 | 5 | → R32
| 3 | Ghana | 3 | -3 | 4 | → R32 (3°)
| 4 | Panama | 0 | -11 | 1 | ✗

Jogos:
- England 3–0 Croatia
- England 4–1 Ghana
- England 7–0 Panama
- Croatia 2–1 Ghana
- Croatia 3–0 Panama
- Ghana 2–1 Panama

**8 melhores 3ºs lugares classificados:**
- Ecuador (Grupo E)
- USA (Grupo D)
- Congo (Grupo K)
- Sweden (Grupo F)
- Cape Verde (Grupo H)
- Jordan (Grupo J)
- Ghana (Grupo L)
- Norway (Grupo I)

### OITAVAS DE FINAL (Round of 32)

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M73 | Czech Republic | 0–2 | **Switzerland** | 90' |
| M74 | **Côte d'Ivoire** | 3–2 (2–2 AET) | USA | AET |
| M75 | **Netherlands** | 5–1 | Morocco | 90' |
| M76 | **Brazil** | 2–0 | Japan | 90' |
| M77 | **France** | 6–2 | Sweden | 90' |
| M78 | **Germany** | 3–2 (2–2 AET) | Senegal | AET |
| M79 | **Mexico** | 1–0 | Ecuador | 90' |
| M80 | **England** | 6–1 | Congo | 90' |
| M81 | **Turkey** | 3–1 | Jordan | 90' |
| M82 | **Belgium** | 1–0 (0–0 AET) | Cape Verde | AET |
| M83 | **Colombia** | 1–0 | Croatia | 90' |
| M84 | **Uruguay** | 2–1 (1–1 AET) | Algeria | AET |
| M85 | Qatar | 2–5 | **Norway** | 90' |
| M86 | **Argentina** | 1–0 | Spain | 90' |
| M87 | **Portugal** | 5–3 | Ghana | 90' |
| M88 | Australia | 3–5 | **Egypt** | 90' |

### ROUND OF 16

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M89 | Côte d'Ivoire | 1–2 | **France** | 90' |
| M90 | Switzerland | 1–2 (1–1 AET) | **Netherlands** | AET |
| M91 | Brazil | 2–2 pen. | **Germany** | PEN |
| M92 | Mexico | 0–4 | **England** | 90' |
| M93 | **Colombia** | 3–0 | Uruguay | 90' |
| M94 | **Turkey** | 1–1 pen. | Belgium | PEN |
| M95 | **Argentina** | 2–1 | Egypt | 90' |
| M96 | Norway | 1–6 | **Portugal** | 90' |

### QUARTAS DE FINAL

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M97 | **France** | 2–0 | Netherlands | 90' |
| M98 | **Colombia** | 3–2 | Turkey | 90' |
| M99 | **Germany** | 1–0 | England | 90' |
| M100 | Argentina | 0–2 | **Portugal** | 90' |

### SEMIFINAIS

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M101 | **France** | 1–0 | Colombia | 90' |
| M102 | Germany | 2–3 (2–2 AET) | **Portugal** | AET |

### FINAL

**France** 2–1 (1–1 AET) **Portugal**

🏆 **CAMPEÃO: FRANCE**

---

### 7.4 Azarão campeão

**Campeão: Morocco**

### FASE DE GRUPOS

**Grupo A**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Czech Republic | 9 | +3 | 3 | → R32
| 2 | South Korea | 4 | +3 | 5 | → R32
| 3 | Mexico | 4 | +0 | 2 | → R32 (3°)
| 4 | South Africa | 0 | -6 | 0 | ✗

Jogos:
- Mexico 1–0 South Africa
- Mexico 1–1 South Korea
- Mexico 0–1 Czech Republic
- South Africa 0–4 South Korea
- South Africa 0–1 Czech Republic
- South Korea 0–1 Czech Republic

**Grupo B**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Switzerland | 7 | +3 | 5 | → R32
| 2 | Canada | 4 | +2 | 9 | → R32
| 3 | Qatar | 4 | -1 | 4 | → R32 (3°)
| 4 | Bosnia-Herzegovina | 1 | -4 | 3 | ✗

Jogos:
- Canada 5–2 Bosnia-Herzegovina
- Canada 2–3 Qatar
- Canada 2–2 Switzerland
- Bosnia-Herzegovina 1–1 Qatar
- Bosnia-Herzegovina 0–1 Switzerland
- Qatar 0–2 Switzerland

**Grupo C**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Brazil | 9 | +12 | 13 | → R32
| 2 | Scotland | 4 | -7 | 5 | → R32
| 3 | Morocco | 3 | +5 | 11 | → R32 (3°)
| 4 | Haiti | 1 | -10 | 1 | ✗

Jogos:
- Brazil 2–1 Morocco
- Brazil 3–0 Haiti
- Brazil 8–0 Scotland
- Morocco 7–0 Haiti
- Morocco 3–4 Scotland
- Haiti 1–1 Scotland

**Grupo D**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Turkey | 7 | +6 | 7 | → R32
| 2 | USA | 4 | -1 | 3 | → R32
| 3 | Paraguay | 4 | -3 | 3 | → R32 (3°)
| 4 | Australia | 1 | -2 | 3 | ✗

Jogos:
- USA 1–1 Paraguay
- USA 2–1 Australia
- USA 0–2 Turkey
- Paraguay 2–1 Australia
- Paraguay 0–4 Turkey
- Australia 1–1 Turkey

**Grupo E**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Germany | 9 | +10 | 12 | → R32
| 2 | Côte d'Ivoire | 6 | +6 | 9 | → R32
| 3 | Ecuador | 3 | +0 | 2 | → R32 (3°)
| 4 | Curacao | 0 | -16 | 0 | ✗

Jogos:
- Germany 8–0 Curacao
- Germany 3–2 Côte d'Ivoire
- Germany 1–0 Ecuador
- Curacao 0–6 Côte d'Ivoire
- Curacao 0–2 Ecuador
- Côte d'Ivoire 1–0 Ecuador

**Grupo F**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Netherlands | 6 | +5 | 9 | → R32
| 2 | Japan | 6 | +4 | 6 | → R32
| 3 | Sweden | 6 | -1 | 4 | → R32 (3°)
| 4 | Tunisia | 0 | -8 | 2 | ✗

Jogos:
- Netherlands 0–2 Japan
- Netherlands 5–0 Sweden
- Netherlands 4–2 Tunisia
- Japan 0–2 Sweden
- Japan 4–0 Tunisia
- Sweden 2–0 Tunisia

**Grupo G**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Belgium | 9 | +13 | 16 | → R32
| 2 | Egypt | 6 | +5 | 14 | → R32
| 3 | Iran | 3 | +2 | 10 | → R32 (3°)
| 4 | New Zealand | 0 | -20 | 2 | ✗

Jogos:
- Belgium 6–2 Egypt
- Belgium 2–1 Iran
- Belgium 8–0 New Zealand
- Egypt 4–3 Iran
- Egypt 8–0 New Zealand
- Iran 6–2 New Zealand

**Grupo H**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Uruguay | 9 | +10 | 10 | → R32
| 2 | Spain | 6 | +9 | 10 | → R32
| 3 | Cape Verde | 3 | -3 | 5 | → R32 (3°)
| 4 | Saudi Arabia | 0 | -16 | 3 | ✗

Jogos:
- Spain 3–0 Cape Verde
- Spain 7–0 Saudi Arabia
- Spain 0–1 Uruguay
- Cape Verde 5–3 Saudi Arabia
- Cape Verde 0–2 Uruguay
- Saudi Arabia 0–7 Uruguay

**Grupo I**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Senegal | 7 | +5 | 9 | → R32
| 2 | Norway | 4 | +2 | 9 | → R32
| 3 | France | 4 | +2 | 6 | → R32 (3°)
| 4 | Iraq | 1 | -9 | 2 | ✗

Jogos:
- France 1–2 Senegal
- France 3–0 Iraq
- France 2–2 Norway
- Senegal 2–2 Iraq
- Senegal 5–1 Norway
- Iraq 0–6 Norway

**Grupo J**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Argentina | 9 | +6 | 7 | → R32
| 2 | Austria | 6 | +1 | 2 | → R32
| 3 | Algeria | 1 | -3 | 2 | → R32 (3°)
| 4 | Jordan | 1 | -4 | 1 | ✗

Jogos:
- Argentina 3–1 Algeria
- Argentina 1–0 Austria
- Argentina 3–0 Jordan
- Algeria 0–1 Austria
- Algeria 1–1 Jordan
- Austria 1–0 Jordan

**Grupo K**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Portugal | 9 | +10 | 14 | → R32
| 2 | Colombia | 4 | +0 | 3 | → R32
| 3 | Congo | 4 | -2 | 3 | → R32 (3°)
| 4 | Uzbekistan | 0 | -8 | 4 | ✗

Jogos:
- Portugal 4–1 Congo
- Portugal 8–2 Uzbekistan
- Portugal 2–1 Colombia
- Congo 2–1 Uzbekistan
- Congo 0–0 Colombia
- Uzbekistan 1–2 Colombia

**Grupo L**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | England | 9 | +13 | 13 | → R32
| 2 | Ghana | 6 | -1 | 6 | → R32
| 3 | Croatia | 3 | -2 | 5 | → R32 (3°)
| 4 | Panama | 0 | -10 | 2 | ✗

Jogos:
- England 2–0 Croatia
- England 4–0 Ghana
- England 7–0 Panama
- Croatia 2–4 Ghana
- Croatia 3–1 Panama
- Ghana 2–1 Panama

**8 melhores 3ºs lugares classificados:**
- Sweden (Grupo F)
- France (Grupo I)
- Mexico (Grupo A)
- Qatar (Grupo B)
- Congo (Grupo K)
- Paraguay (Grupo D)
- Morocco (Grupo C)
- Iran (Grupo G)

### OITAVAS DE FINAL (Round of 32)

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M73 | **South Korea** | 7–1 | Canada | 90' |
| M74 | **Germany** | 3–2 | Sweden | 90' |
| M75 | Netherlands | 0–1 | **Scotland** | 90' |
| M76 | **Brazil** | 2–1 | Japan | 90' |
| M77 | **Senegal** | 7–0 | Paraguay | 90' |
| M78 | **Côte d'Ivoire** | 3–2 | Norway | 90' |
| M79 | Czech Republic | 1–2 (1–1 AET) | **Morocco** | AET |
| M80 | **England** | 3–2 | Congo | 90' |
| M81 | **Turkey** | 3–2 (1–1 AET) | Qatar | AET |
| M82 | **Belgium** | 3–2 (1–1 AET) | Mexico | AET |
| M83 | Colombia | 1–3 | **Ghana** | 90' |
| M84 | Uruguay | 1–2 | **Austria** | 90' |
| M85 | **Switzerland** | 3–1 | Iran | 90' |
| M86 | Argentina | 0–1 (0–0 AET) | **Spain** | AET |
| M87 | **Portugal** | 3–2 (1–1 AET) | France | AET |
| M88 | USA | 2–6 | **Egypt** | 90' |

### ROUND OF 16

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M89 | **Germany** | 2–0 | Senegal | 90' |
| M90 | **South Korea** | 2–1 | Scotland | 90' |
| M91 | Brazil | 0–2 | **Côte d'Ivoire** | 90' |
| M92 | **Morocco** | 2–0 | England | 90' |
| M93 | Ghana | 1–2 (1–1 AET) | **Austria** | AET |
| M94 | Turkey | 0–2 | **Belgium** | 90' |
| M95 | **Spain** | 8–0 | Egypt | 90' |
| M96 | Switzerland | 1–3 | **Portugal** | 90' |

### QUARTAS DE FINAL

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M97 | **Germany** | 2–1 | South Korea | 90' |
| M98 | Austria | 1–2 (0–0 AET) | **Belgium** | AET |
| M99 | Côte d'Ivoire | 0–1 | **Morocco** | 90' |
| M100 | Spain | 1–2 | **Portugal** | 90' |

### SEMIFINAIS

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M101 | **Germany** | 1–0 | Belgium | 90' |
| M102 | **Morocco** | 3–1 | Portugal | 90' |

### FINAL

**Germany** 1–2 **Morocco**

🏆 **CAMPEÃO: MOROCCO**


---

## 8. Limitações e próximos passos

### Limitações atuais

| Limitação | Impacto |
|-----------|---------|
| Cobertura irregular no FIFA 22 (Jordan 1 jogador, Qatar 0) | Times com muita mediana fallback têm scores menos confiáveis |
| Pênaltis como 50/50 puro | Não reflete histórico de pênaltis por seleção |
| `BASE_XG = 1.3` fixo para todos | Não captura estilos de jogo (defensivo vs ofensivo) |
| Lesões/suspensões não modeladas | Todos os convocados sempre disponíveis |
| Forma recente não considerada | Scores baseados apenas em atributos estáticos |

### Próximos passos potenciais

1. **FC25 como Tier 1** — dataset do EA FC 25 (~18k jogadores, cobertura global) já disponível em `datasets/extracted/`, basta plugar no pipeline e substituir FIFA 22. Resolveria a cobertura deficiente de Jordan, Qatar, etc.
2. **Pênaltis ponderados** — incorporar histórico de pênaltis por seleção em Copas anteriores
3. **Forma recente** — multiplicador baseado no ranking FIFA atual
4. **Variância de home advantage** — pequeno boost para times anfitriões (EUA, Canadá, México)
