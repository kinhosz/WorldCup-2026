# Copa do Mundo 2026 — Simulação Monte Carlo

**Data:** 06/06/2026
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
| France | 2.497 | 1.000 | 0.867 | 0.830 | 0.796 |
| Portugal | 2.108 | 0.765 | 0.916 | 0.934 | 0.699 |
| Argentina | 2.057 | 0.788 | 0.799 | 0.785 | 0.817 |
| Brazil | 1.928 | 0.761 | 0.696 | 0.848 | 0.979 |
| Senegal | 1.886 | 0.817 | 0.512 | 0.690 | 0.753 |
| Netherlands | 1.885 | 0.680 | 0.829 | 1.000 | 0.376 |
| Spain | 1.860 | 0.730 | 0.680 | 0.773 | 0.731 |
| Belgium | 1.821 | 0.606 | 0.922 | 0.604 | 0.935 |
| England | 1.821 | 0.669 | 0.774 | 0.890 | 0.720 |
| Colombia | 1.748 | 0.625 | 0.782 | 0.605 | 0.591 |
| Morocco | 1.742 | 0.598 | 0.838 | 0.520 | 0.710 |
| Algeria | 1.556 | 0.600 | 0.595 | 0.638 | 0.150 |
| Croatia | 1.510 | 0.404 | 0.993 | 0.465 | 0.688 |

---

## 6. Resultados — 1,000,000 simulações

| # | Seleção | Grupo | Campeão | Finalista | Semi | QF | R16 |
|---|---------|-------|---------|-----------|------|----|-----|
| 1 | France | I | 20.5% | 32.3% | 48.8% | 71.4% | 91.5% |
| 2 | Portugal | K | 15.1% | 26.1% | 43.2% | 66.4% | 84.2% |
| 3 | Argentina | J | 10.7% | 20.0% | 35.7% | 60.3% | 70.8% |
| 4 | Brazil | C | 8.7% | 16.5% | 29.2% | 48.6% | 72.5% |
| 5 | Netherlands | F | 7.9% | 15.2% | 26.6% | 49.9% | 60.3% |
| 6 | England | L | 7.8% | 15.5% | 29.4% | 53.2% | 71.2% |
| 7 | Belgium | G | 7.2% | 15.5% | 33.9% | 64.7% | 92.0% |
| 8 | Spain | H | 4.9% | 10.3% | 21.6% | 38.5% | 62.5% |
| 9 | Senegal | I | 4.7% | 11.2% | 23.4% | 42.9% | 74.7% |
| 10 | Colombia | K | 2.9% | 7.5% | 17.8% | 36.3% | 59.4% |
| 11 | Morocco | C | 2.6% | 6.6% | 15.1% | 34.1% | 54.7% |
| 12 | Turkey | D | 1.4% | 4.2% | 12.4% | 31.6% | 80.0% |
| 13 | Croatia | L | 1.4% | 4.0% | 11.1% | 26.9% | 49.4% |
| 14 | Germany | E | 0.9% | 2.6% | 7.2% | 17.6% | 50.8% |
| 15 | Algeria | J | 0.8% | 2.8% | 8.7% | 22.7% | 43.1% |
| 16 | Switzerland | B | 0.7% | 2.7% | 8.6% | 23.8% | 78.3% |
| 17 | Côte d'Ivoire | E | 0.6% | 2.0% | 6.2% | 16.8% | 61.1% |
| 18 | Uruguay | H | 0.5% | 1.8% | 6.2% | 19.2% | 31.3% |
| 19 | Czech Republic | A | 0.3% | 1.4% | 5.1% | 19.2% | 65.3% |
| 20 | Congo | K | 0.1% | 0.7% | 2.9% | 11.1% | 23.8% |

### Classificação por grupo (R32)

| Grupo | 1° aprox. | 2° aprox. | 3° aprox. | 4° aprox. |
|-------|-----------|-----------|-----------|-----------|
| A | Czech Republic 99% | Mexico 95% | South Korea 46% | South Africa 24% |
| B | Switzerland 100% | Canada 98% | Qatar 27% | Bosnia-Herzegovina 17% |
| C | Brazil 100% | Morocco 99% | Scotland 64% | Haiti 3% |
| D | Turkey 99% | Paraguay 86% | USA 74% | Australia 15% |
| E | Côte d'Ivoire 100% | Germany 99% | Ecuador 68% | Curacao 5% |
| F | Netherlands 100% | Japan 87% | Sweden 63% | Tunisia 17% |
| G | Belgium 100% | Egypt 76% | Iran 54% | New Zealand 16% |
| H | Spain 100% | Uruguay 100% | Cape Verde 70% | Saudi Arabia 0% |
| I | France 100% | Senegal 100% | Norway 83% | Iraq 0% |
| J | Argentina 100% | Algeria 99% | Austria 75% | Jordan 1% |
| K | Portugal 99% | Colombia 96% | Congo 76% | Uzbekistan 7% |
| L | England 100% | Croatia 99% | Ghana 62% | Panama 4% |

---

## 7. Simulações individuais

Quatro exemplos de torneios completos rodados individualmente.
O vencedor de cada partida está em **negrito**. Placar sempre mandante–visitante.

---

### 7.1 Simulação aleatória

**Campeão: France**

### FASE DE GRUPOS

**Grupo A**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Mexico | 7 | +3 | 6 | → R32
| 2 | Czech Republic | 5 | +1 | 3 | → R32
| 3 | South Africa | 2 | -2 | 3 | → R32 (3°)
| 4 | South Korea | 1 | -2 | 2 | ✗

Jogos:
- Mexico 3–1 South Africa
- Mexico 2–1 South Korea
- Mexico 1–1 Czech Republic
- South Africa 1–1 South Korea
- South Africa 1–1 Czech Republic
- South Korea 0–1 Czech Republic

**Grupo B**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Canada | 9 | +8 | 9 | → R32
| 2 | Switzerland | 6 | +6 | 9 | → R32
| 3 | Qatar | 3 | -5 | 2 | → R32 (3°)
| 4 | Bosnia-Herzegovina | 0 | -9 | 2 | ✗

Jogos:
- Canada 4–0 Bosnia-Herzegovina
- Canada 3–0 Qatar
- Canada 2–1 Switzerland
- Bosnia-Herzegovina 1–2 Qatar
- Bosnia-Herzegovina 1–5 Switzerland
- Qatar 0–3 Switzerland

**Grupo C**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Brazil | 7 | +6 | 6 | → R32
| 2 | Morocco | 7 | +4 | 5 | → R32
| 3 | Scotland | 3 | -5 | 2 | → R32 (3°)
| 4 | Haiti | 0 | -5 | 2 | ✗

Jogos:
- Brazil 0–0 Morocco
- Brazil 2–0 Haiti
- Brazil 4–0 Scotland
- Morocco 3–1 Haiti
- Morocco 2–0 Scotland
- Haiti 1–2 Scotland

**Grupo D**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Paraguay | 7 | +3 | 6 | → R32
| 2 | Turkey | 5 | +3 | 6 | → R32
| 3 | USA | 4 | +0 | 6 | → R32 (3°)
| 4 | Australia | 0 | -6 | 2 | ✗

Jogos:
- USA 1–3 Paraguay
- USA 3–1 Australia
- USA 2–2 Turkey
- Paraguay 2–1 Australia
- Paraguay 1–1 Turkey
- Australia 0–3 Turkey

**Grupo E**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Germany | 9 | +6 | 8 | → R32
| 2 | Côte d'Ivoire | 6 | +11 | 14 | → R32
| 3 | Curacao | 3 | -12 | 4 | → R32 (3°)
| 4 | Ecuador | 0 | -5 | 3 | ✗

Jogos:
- Germany 4–1 Curacao
- Germany 1–0 Côte d'Ivoire
- Germany 3–1 Ecuador
- Curacao 1–11 Côte d'Ivoire
- Curacao 2–1 Ecuador
- Côte d'Ivoire 3–1 Ecuador

**Grupo F**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Netherlands | 9 | +11 | 13 | → R32
| 2 | Japan | 6 | -1 | 4 | → R32
| 3 | Sweden | 3 | +3 | 7 | → R32 (3°)
| 4 | Tunisia | 0 | -13 | 0 | ✗

Jogos:
- Netherlands 4–1 Japan
- Netherlands 2–1 Sweden
- Netherlands 7–0 Tunisia
- Japan 2–1 Sweden
- Japan 1–0 Tunisia
- Sweden 5–0 Tunisia

**Grupo G**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Belgium | 7 | +18 | 21 | → R32
| 2 | Iran | 4 | -9 | 5 | → R32
| 3 | New Zealand | 3 | -8 | 2 | → R32 (3°)
| 4 | Egypt | 2 | -1 | 5 | ✗

Jogos:
- Belgium 3–3 Egypt
- Belgium 11–0 Iran
- Belgium 7–0 New Zealand
- Egypt 2–2 Iran
- Egypt 0–1 New Zealand
- Iran 3–1 New Zealand

**Grupo H**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Uruguay | 9 | +17 | 17 | → R32
| 2 | Spain | 6 | +8 | 10 | → R32
| 3 | Cape Verde | 3 | -3 | 6 | → R32 (3°)
| 4 | Saudi Arabia | 0 | -22 | 0 | ✗

Jogos:
- Spain 3–0 Cape Verde
- Spain 7–0 Saudi Arabia
- Spain 0–2 Uruguay
- Cape Verde 6–0 Saudi Arabia
- Cape Verde 0–6 Uruguay
- Saudi Arabia 0–9 Uruguay

**Grupo I**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Senegal | 9 | +10 | 15 | → R32
| 2 | France | 6 | +12 | 14 | → R32
| 3 | Norway | 3 | -4 | 7 | → R32 (3°)
| 4 | Iraq | 0 | -18 | 1 | ✗

Jogos:
- France 1–2 Senegal
- France 7–0 Iraq
- France 6–0 Norway
- Senegal 8–1 Iraq
- Senegal 5–3 Norway
- Iraq 0–4 Norway

**Grupo J**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Argentina | 9 | +13 | 13 | → R32
| 2 | Austria | 6 | +1 | 4 | → R32
| 3 | Algeria | 3 | +0 | 5 | → R32 (3°)
| 4 | Jordan | 0 | -14 | 0 | ✗

Jogos:
- Argentina 3–0 Algeria
- Argentina 2–0 Austria
- Argentina 8–0 Jordan
- Algeria 1–2 Austria
- Algeria 4–0 Jordan
- Austria 2–0 Jordan

**Grupo K**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Portugal | 9 | +6 | 9 | → R32
| 2 | Colombia | 6 | +1 | 4 | → R32
| 3 | Congo | 3 | -1 | 5 | → R32 (3°)
| 4 | Uzbekistan | 0 | -6 | 0 | ✗

Jogos:
- Portugal 4–2 Congo
- Portugal 3–0 Uzbekistan
- Portugal 2–1 Colombia
- Congo 2–0 Uzbekistan
- Congo 1–2 Colombia
- Uzbekistan 0–1 Colombia

**Grupo L**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | England | 9 | +9 | 9 | → R32
| 2 | Croatia | 6 | +5 | 7 | → R32
| 3 | Ghana | 3 | -5 | 6 | → R32 (3°)
| 4 | Panama | 0 | -9 | 3 | ✗

Jogos:
- England 1–0 Croatia
- England 6–0 Ghana
- England 2–0 Panama
- Croatia 2–1 Ghana
- Croatia 5–0 Panama
- Ghana 5–3 Panama

**8 melhores 3ºs lugares classificados:**
- USA (Grupo D)
- Sweden (Grupo F)
- Algeria (Grupo J)
- Congo (Grupo K)
- Cape Verde (Grupo H)
- Norway (Grupo I)
- Ghana (Grupo L)
- Scotland (Grupo C)

### OITAVAS DE FINAL (Round of 32)

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M73 | Czech Republic | 2–4 | **Switzerland** | 90' |
| M74 | **Germany** | 1–0 | USA | 90' |
| M75 | **Netherlands** | 0–0 pen. | Morocco | PEN |
| M76 | Brazil | 0–1 (0–0 AET) | **Japan** | AET |
| M77 | Senegal | 3–4 (3–3 AET) | **Sweden** | AET |
| M78 | Côte d'Ivoire | 0–1 | **France** | 90' |
| M79 | Mexico | 0–0 pen. | **Scotland** | PEN |
| M80 | **England** | 3–2 (2–2 AET) | Congo | AET |
| M81 | Paraguay | 2–3 | **Algeria** | 90' |
| M82 | **Belgium** | 3–0 | Cape Verde | 90' |
| M83 | **Colombia** | 2–1 | Croatia | 90' |
| M84 | Uruguay | 0–1 | **Austria** | 90' |
| M85 | **Canada** | 5–2 | Norway | 90' |
| M86 | **Argentina** | 3–1 | Spain | 90' |
| M87 | **Portugal** | 6–1 | Ghana | 90' |
| M88 | **Turkey** | 3–0 | Iran | 90' |

### ROUND OF 16

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M89 | **Germany** | 1–0 (0–0 AET) | Sweden | AET |
| M90 | Switzerland | 0–3 | **Netherlands** | 90' |
| M91 | Japan | 0–4 | **France** | 90' |
| M92 | Scotland | 2–4 | **England** | 90' |
| M93 | Colombia | 0–1 | **Austria** | 90' |
| M94 | Algeria | 0–1 | **Belgium** | 90' |
| M95 | Argentina | 0–1 | **Turkey** | 90' |
| M96 | Canada | 1–4 | **Portugal** | 90' |

### QUARTAS DE FINAL

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M97 | Germany | 0–1 | **Netherlands** | 90' |
| M98 | Austria | 0–3 | **Belgium** | 90' |
| M99 | **France** | 5–2 | England | 90' |
| M100 | Turkey | 0–5 | **Portugal** | 90' |

### SEMIFINAIS

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M101 | Netherlands | 1–2 | **Belgium** | 90' |
| M102 | **France** | 1–0 | Portugal | 90' |

### FINAL

**Belgium** 1–2 **France**

🏆 **CAMPEÃO: FRANCE**

---

### 7.2 Brasil campeão 🇧🇷

**Campeão: Brazil**

### FASE DE GRUPOS

**Grupo A**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Mexico | 7 | +7 | 8 | → R32
| 2 | Czech Republic | 7 | +5 | 6 | → R32
| 3 | South Korea | 3 | -3 | 2 | → R32 (3°)
| 4 | South Africa | 0 | -9 | 0 | ✗

Jogos:
- Mexico 4–0 South Africa
- Mexico 3–0 South Korea
- Mexico 1–1 Czech Republic
- South Africa 0–2 South Korea
- South Africa 0–3 Czech Republic
- South Korea 0–2 Czech Republic

**Grupo B**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Switzerland | 9 | +13 | 14 | → R32
| 2 | Canada | 6 | +5 | 10 | → R32
| 3 | Bosnia-Herzegovina | 1 | -6 | 2 | → R32 (3°)
| 4 | Qatar | 1 | -12 | 1 | ✗

Jogos:
- Canada 4–1 Bosnia-Herzegovina
- Canada 5–0 Qatar
- Canada 1–4 Switzerland
- Bosnia-Herzegovina 1–1 Qatar
- Bosnia-Herzegovina 0–3 Switzerland
- Qatar 0–7 Switzerland

**Grupo C**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Morocco | 7 | +4 | 4 | → R32
| 2 | Scotland | 6 | +1 | 3 | → R32
| 3 | Brazil | 4 | +10 | 11 | → R32 (3°)
| 4 | Haiti | 0 | -15 | 1 | ✗

Jogos:
- Brazil 0–0 Morocco
- Brazil 11–0 Haiti
- Brazil 0–1 Scotland
- Morocco 3–0 Haiti
- Morocco 1–0 Scotland
- Haiti 1–2 Scotland

**Grupo D**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Turkey | 7 | +7 | 10 | → R32
| 2 | Paraguay | 6 | +2 | 8 | → R32
| 3 | USA | 3 | -3 | 4 | → R32 (3°)
| 4 | Australia | 1 | -6 | 4 | ✗

Jogos:
- USA 1–4 Paraguay
- USA 3–1 Australia
- USA 0–2 Turkey
- Paraguay 4–0 Australia
- Paraguay 0–5 Turkey
- Australia 3–3 Turkey

**Grupo E**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Côte d'Ivoire | 9 | +8 | 8 | → R32
| 2 | Germany | 6 | +5 | 6 | → R32
| 3 | Ecuador | 3 | -2 | 2 | → R32 (3°)
| 4 | Curacao | 0 | -11 | 0 | ✗

Jogos:
- Germany 5–0 Curacao
- Germany 0–1 Côte d'Ivoire
- Germany 1–0 Ecuador
- Curacao 0–4 Côte d'Ivoire
- Curacao 0–2 Ecuador
- Côte d'Ivoire 3–0 Ecuador

**Grupo F**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Netherlands | 9 | +8 | 9 | → R32
| 2 | Japan | 4 | -1 | 2 | → R32
| 3 | Sweden | 3 | -3 | 3 | → R32 (3°)
| 4 | Tunisia | 1 | -4 | 0 | ✗

Jogos:
- Netherlands 2–0 Japan
- Netherlands 4–1 Sweden
- Netherlands 3–0 Tunisia
- Japan 2–1 Sweden
- Japan 0–0 Tunisia
- Sweden 1–0 Tunisia

**Grupo G**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Belgium | 9 | +15 | 16 | → R32
| 2 | Egypt | 6 | +5 | 11 | → R32
| 3 | New Zealand | 3 | -11 | 4 | → R32 (3°)
| 4 | Iran | 0 | -9 | 3 | ✗

Jogos:
- Belgium 2–1 Egypt
- Belgium 5–0 Iran
- Belgium 9–0 New Zealand
- Egypt 4–3 Iran
- Egypt 6–1 New Zealand
- Iran 0–3 New Zealand

**Grupo H**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Spain | 7 | +14 | 14 | → R32
| 2 | Uruguay | 7 | +5 | 5 | → R32
| 3 | Cape Verde | 3 | -2 | 2 | → R32 (3°)
| 4 | Saudi Arabia | 0 | -17 | 0 | ✗

Jogos:
- Spain 2–0 Cape Verde
- Spain 12–0 Saudi Arabia
- Spain 0–0 Uruguay
- Cape Verde 2–0 Saudi Arabia
- Cape Verde 0–2 Uruguay
- Saudi Arabia 0–3 Uruguay

**Grupo I**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | France | 9 | +16 | 17 | → R32
| 2 | Senegal | 6 | +0 | 4 | → R32
| 3 | Norway | 3 | -2 | 4 | → R32 (3°)
| 4 | Iraq | 0 | -14 | 1 | ✗

Jogos:
- France 3–0 Senegal
- France 11–0 Iraq
- France 3–1 Norway
- Senegal 2–0 Iraq
- Senegal 2–1 Norway
- Iraq 1–2 Norway

**Grupo J**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Argentina | 9 | +10 | 12 | → R32
| 2 | Austria | 4 | -2 | 3 | → R32
| 3 | Algeria | 3 | +2 | 7 | → R32 (3°)
| 4 | Jordan | 1 | -10 | 2 | ✗

Jogos:
- Argentina 4–2 Algeria
- Argentina 3–0 Austria
- Argentina 5–0 Jordan
- Algeria 0–1 Austria
- Algeria 5–0 Jordan
- Austria 2–2 Jordan

**Grupo K**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Portugal | 7 | +7 | 9 | → R32
| 2 | Congo | 6 | +1 | 7 | → R32
| 3 | Colombia | 4 | +0 | 5 | → R32 (3°)
| 4 | Uzbekistan | 0 | -8 | 2 | ✗

Jogos:
- Portugal 4–0 Congo
- Portugal 4–1 Uzbekistan
- Portugal 1–1 Colombia
- Congo 4–0 Uzbekistan
- Congo 3–2 Colombia
- Uzbekistan 1–2 Colombia

**Grupo L**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | England | 9 | +10 | 10 | → R32
| 2 | Ghana | 6 | +1 | 5 | → R32
| 3 | Croatia | 3 | -1 | 3 | → R32 (3°)
| 4 | Panama | 0 | -10 | 0 | ✗

Jogos:
- England 3–0 Croatia
- England 4–0 Ghana
- England 3–0 Panama
- Croatia 0–1 Ghana
- Croatia 3–0 Panama
- Ghana 4–0 Panama

**8 melhores 3ºs lugares classificados:**
- Brazil (Grupo C)
- Colombia (Grupo K)
- Algeria (Grupo J)
- Croatia (Grupo L)
- Norway (Grupo I)
- Cape Verde (Grupo H)
- Ecuador (Grupo E)
- USA (Grupo D)

### OITAVAS DE FINAL (Round of 32)

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M73 | **Czech Republic** | 3–0 | Canada | 90' |
| M74 | Côte d'Ivoire | 1–1 pen. | **Brazil** | PEN |
| M75 | **Netherlands** | 6–1 | Scotland | 90' |
| M76 | Morocco | 1–2 (1–1 AET) | **Japan** | AET |
| M77 | **France** | 4–2 | USA | 90' |
| M78 | Germany | 1–1 pen. | **Senegal** | PEN |
| M79 | Mexico | 0–2 | **Norway** | 90' |
| M80 | **England** | 1–0 | Colombia | 90' |
| M81 | **Turkey** | 1–0 | Algeria | 90' |
| M82 | **Belgium** | 6–0 | Cape Verde | 90' |
| M83 | **Congo** | 6–1 | Ghana | 90' |
| M84 | Spain | 2–2 pen. | **Austria** | PEN |
| M85 | **Switzerland** | 2–0 | Ecuador | 90' |
| M86 | **Argentina** | 3–0 | Uruguay | 90' |
| M87 | **Portugal** | 1–0 (0–0 AET) | Croatia | AET |
| M88 | Paraguay | 2–3 | **Egypt** | 90' |

### ROUND OF 16

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M89 | **Brazil** | 1–0 (0–0 AET) | France | AET |
| M90 | Czech Republic | 0–1 | **Netherlands** | 90' |
| M91 | Japan | 0–4 | **Senegal** | 90' |
| M92 | **Norway** | 2–1 | England | 90' |
| M93 | **Congo** | 1–0 | Austria | 90' |
| M94 | Turkey | 0–2 | **Belgium** | 90' |
| M95 | **Argentina** | 8–1 | Egypt | 90' |
| M96 | Switzerland | 2–3 (2–2 AET) | **Portugal** | AET |

### QUARTAS DE FINAL

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M97 | **Brazil** | 3–2 | Netherlands | 90' |
| M98 | Congo | 0–3 | **Belgium** | 90' |
| M99 | **Senegal** | 5–1 | Norway | 90' |
| M100 | Argentina | 1–2 | **Portugal** | 90' |

### SEMIFINAIS

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M101 | **Brazil** | 2–1 (0–0 AET) | Belgium | AET |
| M102 | Senegal | 0–2 | **Portugal** | 90' |

### FINAL

**Brazil** 2–1 **Portugal**

🏆 **CAMPEÃO: BRAZIL**

---

### 7.3 França campeã 🇫🇷

**Campeão: France**

### FASE DE GRUPOS

**Grupo A**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Czech Republic | 9 | +12 | 12 | → R32
| 2 | Mexico | 6 | +5 | 8 | → R32
| 3 | South Africa | 3 | -8 | 4 | → R32 (3°)
| 4 | South Korea | 0 | -9 | 0 | ✗

Jogos:
- Mexico 6–1 South Africa
- Mexico 2–0 South Korea
- Mexico 0–2 Czech Republic
- South Africa 3–0 South Korea
- South Africa 0–6 Czech Republic
- South Korea 0–4 Czech Republic

**Grupo B**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Switzerland | 9 | +9 | 9 | → R32
| 2 | Canada | 6 | +10 | 11 | → R32
| 3 | Qatar | 3 | -4 | 4 | → R32 (3°)
| 4 | Bosnia-Herzegovina | 0 | -15 | 1 | ✗

Jogos:
- Canada 7–0 Bosnia-Herzegovina
- Canada 4–0 Qatar
- Canada 0–1 Switzerland
- Bosnia-Herzegovina 1–4 Qatar
- Bosnia-Herzegovina 0–5 Switzerland
- Qatar 0–3 Switzerland

**Grupo C**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Brazil | 9 | +7 | 9 | → R32
| 2 | Morocco | 6 | +6 | 8 | → R32
| 3 | Scotland | 1 | -4 | 3 | → R32 (3°)
| 4 | Haiti | 1 | -9 | 2 | ✗

Jogos:
- Brazil 1–0 Morocco
- Brazil 4–0 Haiti
- Brazil 4–2 Scotland
- Morocco 6–1 Haiti
- Morocco 2–0 Scotland
- Haiti 1–1 Scotland

**Grupo D**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Paraguay | 9 | +6 | 9 | → R32
| 2 | Turkey | 4 | +2 | 4 | → R32
| 3 | USA | 4 | -1 | 3 | → R32 (3°)
| 4 | Australia | 0 | -7 | 2 | ✗

Jogos:
- USA 1–3 Paraguay
- USA 1–0 Australia
- USA 1–1 Turkey
- Paraguay 5–2 Australia
- Paraguay 1–0 Turkey
- Australia 0–3 Turkey

**Grupo E**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Côte d'Ivoire | 9 | +11 | 12 | → R32
| 2 | Ecuador | 4 | -3 | 1 | → R32
| 3 | Germany | 3 | -1 | 3 | → R32 (3°)
| 4 | Curacao | 1 | -7 | 1 | ✗

Jogos:
- Germany 2–1 Curacao
- Germany 1–2 Côte d'Ivoire
- Germany 0–1 Ecuador
- Curacao 0–6 Côte d'Ivoire
- Curacao 0–0 Ecuador
- Côte d'Ivoire 4–0 Ecuador

**Grupo F**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Japan | 9 | +3 | 6 | → R32
| 2 | Netherlands | 6 | +1 | 4 | → R32
| 3 | Tunisia | 1 | -2 | 3 | → R32 (3°)
| 4 | Sweden | 1 | -2 | 2 | ✗

Jogos:
- Netherlands 1–2 Japan
- Netherlands 1–0 Sweden
- Netherlands 2–1 Tunisia
- Japan 2–1 Sweden
- Japan 2–1 Tunisia
- Sweden 1–1 Tunisia

**Grupo G**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Belgium | 9 | +17 | 17 | → R32
| 2 | Iran | 3 | -3 | 4 | → R32
| 3 | Egypt | 3 | -7 | 5 | → R32 (3°)
| 4 | New Zealand | 3 | -7 | 4 | ✗

Jogos:
- Belgium 6–0 Egypt
- Belgium 4–0 Iran
- Belgium 7–0 New Zealand
- Egypt 1–4 Iran
- Egypt 4–2 New Zealand
- Iran 0–2 New Zealand

**Grupo H**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Spain | 9 | +16 | 16 | → R32
| 2 | Uruguay | 4 | +2 | 5 | → R32
| 3 | Cape Verde | 2 | -9 | 1 | → R32 (3°)
| 4 | Saudi Arabia | 1 | -9 | 1 | ✗

Jogos:
- Spain 9–0 Cape Verde
- Spain 6–0 Saudi Arabia
- Spain 1–0 Uruguay
- Cape Verde 0–0 Saudi Arabia
- Cape Verde 1–1 Uruguay
- Saudi Arabia 1–4 Uruguay

**Grupo I**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | France | 9 | +13 | 14 | → R32
| 2 | Senegal | 6 | +7 | 11 | → R32
| 3 | Norway | 3 | -3 | 6 | → R32 (3°)
| 4 | Iraq | 0 | -17 | 0 | ✗

Jogos:
- France 4–1 Senegal
- France 6–0 Iraq
- France 4–0 Norway
- Senegal 5–0 Iraq
- Senegal 5–0 Norway
- Iraq 0–6 Norway

**Grupo J**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Argentina | 9 | +10 | 11 | → R32
| 2 | Algeria | 6 | +7 | 9 | → R32
| 3 | Austria | 3 | -1 | 1 | → R32 (3°)
| 4 | Jordan | 0 | -16 | 0 | ✗

Jogos:
- Argentina 2–1 Algeria
- Argentina 1–0 Austria
- Argentina 8–0 Jordan
- Algeria 1–0 Austria
- Algeria 7–0 Jordan
- Austria 1–0 Jordan

**Grupo K**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Portugal | 9 | +9 | 11 | → R32
| 2 | Colombia | 6 | +0 | 4 | → R32
| 3 | Congo | 3 | +1 | 6 | → R32 (3°)
| 4 | Uzbekistan | 0 | -10 | 2 | ✗

Jogos:
- Portugal 3–1 Congo
- Portugal 5–0 Uzbekistan
- Portugal 3–1 Colombia
- Congo 5–1 Uzbekistan
- Congo 0–1 Colombia
- Uzbekistan 1–2 Colombia

**Grupo L**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | England | 7 | +10 | 12 | → R32
| 2 | Ghana | 6 | -1 | 6 | → R32
| 3 | Croatia | 4 | +5 | 9 | → R32 (3°)
| 4 | Panama | 0 | -14 | 1 | ✗

Jogos:
- England 1–1 Croatia
- England 4–1 Ghana
- England 7–0 Panama
- Croatia 2–3 Ghana
- Croatia 6–0 Panama
- Ghana 2–1 Panama

**8 melhores 3ºs lugares classificados:**
- Croatia (Grupo L)
- USA (Grupo D)
- Congo (Grupo K)
- Germany (Grupo E)
- Austria (Grupo J)
- Norway (Grupo I)
- Qatar (Grupo B)
- Egypt (Grupo G)

### OITAVAS DE FINAL (Round of 32)

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M73 | **Mexico** | 2–0 | Canada | 90' |
| M74 | Côte d'Ivoire | 2–3 | **USA** | 90' |
| M75 | **Japan** | 2–0 | Morocco | 90' |
| M76 | Brazil | 1–3 (1–1 AET) | **Netherlands** | AET |
| M77 | **France** | 12–0 | Egypt | 90' |
| M78 | Ecuador | 0–2 | **Senegal** | 90' |
| M79 | Czech Republic | 0–1 | **Germany** | 90' |
| M80 | **England** | 2–0 | Congo | 90' |
| M81 | **Paraguay** | 5–1 | Qatar | 90' |
| M82 | **Belgium** | 2–0 | Austria | 90' |
| M83 | **Colombia** | 5–0 | Ghana | 90' |
| M84 | Spain | 1–2 | **Algeria** | 90' |
| M85 | **Switzerland** | 2–1 | Norway | 90' |
| M86 | **Argentina** | 2–1 (1–1 AET) | Uruguay | AET |
| M87 | **Portugal** | 2–1 | Croatia | 90' |
| M88 | **Turkey** | 5–0 | Iran | 90' |

### ROUND OF 16

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M89 | USA | 0–6 | **France** | 90' |
| M90 | **Mexico** | 2–1 (1–1 AET) | Japan | AET |
| M91 | **Netherlands** | 3–1 | Senegal | 90' |
| M92 | **Germany** | 0–0 pen. | England | PEN |
| M93 | **Colombia** | 7–3 | Algeria | 90' |
| M94 | Paraguay | 1–7 | **Belgium** | 90' |
| M95 | **Argentina** | 3–2 (1–1 AET) | Turkey | AET |
| M96 | **Switzerland** | 2–0 | Portugal | 90' |

### QUARTAS DE FINAL

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M97 | **France** | 2–1 | Mexico | 90' |
| M98 | **Colombia** | 2–1 | Belgium | 90' |
| M99 | **Netherlands** | 3–0 | Germany | 90' |
| M100 | Argentina | 1–2 | **Switzerland** | 90' |

### SEMIFINAIS

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M101 | **France** | 3–1 | Colombia | 90' |
| M102 | Netherlands | 0–0 pen. | **Switzerland** | PEN |

### FINAL

**France** 3–2 **Switzerland**

🏆 **CAMPEÃO: FRANCE**

---

### 7.4 Azarão campeão

**Campeão: Senegal**

### FASE DE GRUPOS

**Grupo A**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Czech Republic | 9 | +5 | 6 | → R32
| 2 | Mexico | 6 | +4 | 5 | → R32
| 3 | South Korea | 3 | -2 | 1 | → R32 (3°)
| 4 | South Africa | 0 | -7 | 1 | ✗

Jogos:
- Mexico 3–0 South Africa
- Mexico 2–0 South Korea
- Mexico 0–1 Czech Republic
- South Africa 0–1 South Korea
- South Africa 1–4 Czech Republic
- South Korea 0–1 Czech Republic

**Grupo B**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Switzerland | 9 | +11 | 14 | → R32
| 2 | Canada | 6 | +6 | 10 | → R32
| 3 | Qatar | 3 | -6 | 4 | → R32 (3°)
| 4 | Bosnia-Herzegovina | 0 | -11 | 2 | ✗

Jogos:
- Canada 3–0 Bosnia-Herzegovina
- Canada 6–0 Qatar
- Canada 1–4 Switzerland
- Bosnia-Herzegovina 1–3 Qatar
- Bosnia-Herzegovina 1–7 Switzerland
- Qatar 1–3 Switzerland

**Grupo C**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Brazil | 9 | +14 | 15 | → R32
| 2 | Morocco | 6 | +3 | 7 | → R32
| 3 | Scotland | 1 | -4 | 0 | → R32 (3°)
| 4 | Haiti | 1 | -13 | 0 | ✗

Jogos:
- Brazil 4–1 Morocco
- Brazil 8–0 Haiti
- Brazil 3–0 Scotland
- Morocco 5–0 Haiti
- Morocco 1–0 Scotland
- Haiti 0–0 Scotland

**Grupo D**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Turkey | 9 | +12 | 13 | → R32
| 2 | USA | 4 | -4 | 3 | → R32
| 3 | Paraguay | 3 | +0 | 4 | → R32 (3°)
| 4 | Australia | 1 | -8 | 1 | ✗

Jogos:
- USA 2–1 Paraguay
- USA 1–1 Australia
- USA 0–5 Turkey
- Paraguay 2–0 Australia
- Paraguay 1–2 Turkey
- Australia 0–6 Turkey

**Grupo E**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Germany | 7 | +5 | 5 | → R32
| 2 | Côte d'Ivoire | 6 | +9 | 10 | → R32
| 3 | Ecuador | 4 | +0 | 3 | → R32 (3°)
| 4 | Curacao | 0 | -14 | 0 | ✗

Jogos:
- Germany 4–0 Curacao
- Germany 1–0 Côte d'Ivoire
- Germany 0–0 Ecuador
- Curacao 0–7 Côte d'Ivoire
- Curacao 0–3 Ecuador
- Côte d'Ivoire 3–0 Ecuador

**Grupo F**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Netherlands | 9 | +8 | 11 | → R32
| 2 | Sweden | 4 | +0 | 2 | → R32
| 3 | Tunisia | 2 | -3 | 4 | → R32 (3°)
| 4 | Japan | 1 | -5 | 4 | ✗

Jogos:
- Netherlands 5–1 Japan
- Netherlands 1–0 Sweden
- Netherlands 5–2 Tunisia
- Japan 1–2 Sweden
- Japan 2–2 Tunisia
- Sweden 0–0 Tunisia

**Grupo G**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Belgium | 9 | +15 | 16 | → R32
| 2 | Egypt | 6 | -1 | 7 | → R32
| 3 | New Zealand | 1 | -4 | 2 | → R32 (3°)
| 4 | Iran | 1 | -10 | 2 | ✗

Jogos:
- Belgium 8–1 Egypt
- Belgium 5–0 Iran
- Belgium 3–0 New Zealand
- Egypt 5–0 Iran
- Egypt 1–0 New Zealand
- Iran 2–2 New Zealand

**Grupo H**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Uruguay | 9 | +7 | 10 | → R32
| 2 | Spain | 6 | +14 | 15 | → R32
| 3 | Cape Verde | 3 | -1 | 7 | → R32 (3°)
| 4 | Saudi Arabia | 0 | -20 | 1 | ✗

Jogos:
- Spain 5–0 Cape Verde
- Spain 10–0 Saudi Arabia
- Spain 0–1 Uruguay
- Cape Verde 5–0 Saudi Arabia
- Cape Verde 2–3 Uruguay
- Saudi Arabia 1–6 Uruguay

**Grupo I**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Senegal | 9 | +7 | 8 | → R32
| 2 | France | 6 | +9 | 12 | → R32
| 3 | Norway | 3 | -4 | 4 | → R32 (3°)
| 4 | Iraq | 0 | -12 | 2 | ✗

Jogos:
- France 1–2 Senegal
- France 6–0 Iraq
- France 5–1 Norway
- Senegal 5–0 Iraq
- Senegal 1–0 Norway
- Iraq 2–3 Norway

**Grupo J**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Argentina | 9 | +7 | 8 | → R32
| 2 | Austria | 4 | -1 | 1 | → R32
| 3 | Algeria | 3 | +3 | 5 | → R32 (3°)
| 4 | Jordan | 1 | -9 | 1 | ✗

Jogos:
- Argentina 1–0 Algeria
- Argentina 2–0 Austria
- Argentina 5–1 Jordan
- Algeria 0–1 Austria
- Algeria 5–0 Jordan
- Austria 0–0 Jordan

**Grupo K**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Colombia | 7 | +7 | 11 | → R32
| 2 | Portugal | 7 | +7 | 10 | → R32
| 3 | Uzbekistan | 1 | -7 | 1 | → R32 (3°)
| 4 | Congo | 1 | -7 | 0 | ✗

Jogos:
- Portugal 5–0 Congo
- Portugal 2–0 Uzbekistan
- Portugal 3–3 Colombia
- Congo 0–0 Uzbekistan
- Congo 0–2 Colombia
- Uzbekistan 1–6 Colombia

**Grupo L**

| # | Seleção | Pts | GD | GP |
|---|---------|-----|----|----|
| 1 | Croatia | 9 | +7 | 9 | → R32
| 2 | England | 6 | +7 | 9 | → R32
| 3 | Ghana | 3 | -3 | 5 | → R32 (3°)
| 4 | Panama | 0 | -11 | 1 | ✗

Jogos:
- England 1–2 Croatia
- England 6–0 Ghana
- England 2–0 Panama
- Croatia 2–0 Ghana
- Croatia 5–1 Panama
- Ghana 5–0 Panama

**8 melhores 3ºs lugares classificados:**
- Ecuador (Grupo E)
- Algeria (Grupo J)
- Paraguay (Grupo D)
- Cape Verde (Grupo H)
- South Korea (Grupo A)
- Ghana (Grupo L)
- Norway (Grupo I)
- Qatar (Grupo B)

### OITAVAS DE FINAL (Round of 32)

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M73 | Mexico | 2–3 | **Canada** | 90' |
| M74 | **Germany** | 3–0 | Paraguay | 90' |
| M75 | Netherlands | 0–2 | **Morocco** | 90' |
| M76 | **Brazil** | 3–1 | Sweden | 90' |
| M77 | **Senegal** | 4–0 | Cape Verde | 90' |
| M78 | Côte d'Ivoire | 3–6 | **France** | 90' |
| M79 | **Czech Republic** | 3–1 (1–1 AET) | Ecuador | AET |
| M80 | **Croatia** | 1–0 | Algeria | 90' |
| M81 | **Turkey** | 5–0 | Qatar | 90' |
| M82 | **Belgium** | 4–0 | South Korea | 90' |
| M83 | **Portugal** | 1–0 | England | 90' |
| M84 | Uruguay | 0–1 | **Austria** | 90' |
| M85 | **Switzerland** | 1–0 | Norway | 90' |
| M86 | Argentina | 1–2 | **Spain** | 90' |
| M87 | **Colombia** | 5–0 | Ghana | 90' |
| M88 | **USA** | 5–0 | Egypt | 90' |

### ROUND OF 16

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M89 | Germany | 0–1 | **Senegal** | 90' |
| M90 | **Canada** | 1–1 pen. | Morocco | PEN |
| M91 | Brazil | 1–3 | **France** | 90' |
| M92 | Czech Republic | 1–4 | **Croatia** | 90' |
| M93 | **Portugal** | 1–0 | Austria | 90' |
| M94 | Turkey | 2–3 | **Belgium** | 90' |
| M95 | **Spain** | 3–2 | USA | 90' |
| M96 | **Switzerland** | 2–1 (0–0 AET) | Colombia | AET |

### QUARTAS DE FINAL

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M97 | **Senegal** | 2–0 | Canada | 90' |
| M98 | Portugal | 0–1 | **Belgium** | 90' |
| M99 | France | 0–2 | **Croatia** | 90' |
| M100 | **Spain** | 3–1 | Switzerland | 90' |

### SEMIFINAIS

| Jogo | Mandante | Placar | Visitante | Obs |
|------|----------|--------|-----------|-----|
| M101 | **Senegal** | 3–0 | Belgium | 90' |
| M102 | Croatia | 0–3 | **Spain** | 90' |

### FINAL

**Senegal** 3–1 **Spain**

🏆 **CAMPEÃO: SENEGAL**


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
