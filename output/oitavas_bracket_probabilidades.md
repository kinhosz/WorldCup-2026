# Oitavas em diante — Probabilidades do Chaveamento (Model5)

> Cálculo exato via recursão pelo chaveamento (não Monte Carlo) — para cada nó da chave (R16→QF→SF→Final), computa a distribuição de probabilidade de qual time chega ali, propagando: P(time T vence o nó) = P(T chegar de um lado) × Σ P(oponente O chegar do outro lado) × P(T vence O). P(T vence O) usa a metodologia "quem avança" (`P(vence 90') + 0.5×P(empate)`, pênaltis/prorrogação tratados como 50/50).
>
> Fonte dos pesos: `output/weights_model5.json` (Model5, ativo).

## Bug corrigido no chaveamento (`scripts/simulate.py`)

Duas correções feitas antes deste cálculo — o chaveamento anterior estava errado:

1. **`ROUND16`** tinha os pares 1, 2, 3, 7 e 8 embaralhados (não seguia a ordem sequencial oficial dos jogos 73–88).
2. **`SEMIFINALS`** cruzava as duas metades da chave uma fase cedo demais — fazia o Brasil (metade B: jogos 81–88) encontrar o lado da França (metade A: jogos 73–80) já na semifinal, quando na verdade só deveriam se encontrar na final.
3. **`ROUND32`** (specs de grupo tipo "1º E vs 3º ABCDF" usados por `simulate_tournament()`) estava dessincronizado dos resultados reais em 15 dos 16 jogos — a simulação às vezes não reconhecia o resultado real de um jogo e resimulava do zero, deixando times já eliminados (Holanda, Alemanha, Japão) reaparecerem nas odds. Corrigido trocando a resolução por specs por um bracket fixo (`REAL_R16_BRACKET`) com os 16 times reais das oitavas — a fase de grupos e o R32 não são mais simulados (já são fato consumado).

Estrutura correta confirmada:
- **Oitavas (sequencial, jogos 73–88):** Canadá×Marrocos, Paraguai×França, EUA×Bélgica, Espanha×Portugal, Brasil×Noruega, México×Inglaterra, Suíça×Colômbia, Egito×Argentina
- **Quartas:** QF1 = (Canadá/Marrocos) x (Paraguai/França) · QF2 = (EUA/Bélgica) x (Espanha/Portugal) · QF3 = (Brasil/Noruega) x (México/Inglaterra) · QF4 = (Suíça/Colômbia) x (Egito/Argentina)
- **Semifinal:** SF1 = QF1 x QF2 (metade A) · SF2 = QF3 x QF4 (metade B, onde está o Brasil)
- **Final:** SF1 x SF2 — só aqui as duas metades se cruzam

## Top 10 Campeões

| # | Seleção | Prob. Campeão |
|---|---------|----------------|
| 1 | França | 26.72% |
| 2 | Brasil | 20.16% |
| 3 | Espanha | 13.66% |
| 4 | Argentina | 6.75% |
| 5 | Portugal | 6.62% |
| 6 | Marrocos | 6.31% |
| 7 | Inglaterra | 6.03% |
| 8 | Colômbia | 4.86% |
| 9 | Suíça | 2.71% |
| 10 | EUA | 2.21% |

## Caminho do Brasil — decomposição completa

**R16 x Noruega:** 84.18%

**QF x (México ou Inglaterra):**
```
México passa 38.72%   × Brasil vence México 71.43%      = 27.66pp
Inglaterra passa 61.28% × Brasil vence Inglaterra 63.51% = 38.92pp
                                                          ────────
P(Brasil vence QF | chegou) = 66.58%
```
→ P(Brasil chega à semi) = 84.18% × 66.58% = **56.04%**

**SF x (Argentina, Colômbia, Suíça ou Egito)** — metade B da chave:
```
Argentina:  chega 39.30% × Brasil vence 64.45% = 25.33pp
Colômbia:   chega 29.49% × Brasil vence 64.83% = 19.11pp
Suíça:      chega 22.35% × Brasil vence 71.05% = 15.88pp
Egito:      chega  8.87% × Brasil vence 85.89% =  7.62pp
                                                 ────────
P(Brasil vence SF | chegou) = 67.94%
```
→ P(Brasil chega à final) = 56.04% × 67.94% = **38.07%**

**Final x (Canadá, Marrocos, Paraguai, França, Bélgica, EUA, Espanha ou Portugal)** — metade A da chave:
```
França:     chega 41.24% × Brasil vence 44.34% = 18.29pp   ← só aqui a França aparece
Espanha:    chega 22.68% × Brasil vence 48.82% = 11.07pp
Marrocos:   chega 13.45% × Brasil vence 64.04% =  8.61pp
Portugal:   chega 12.67% × Brasil vence 57.97% =  7.35pp
EUA:        chega  5.77% × Brasil vence 73.64% =  4.25pp
Bélgica:    chega  3.06% × Brasil vence 78.17% =  2.40pp
Canadá:     chega  0.67% × Brasil vence 89.02% =  0.60pp
Paraguai:   chega  0.45% × Brasil vence 89.36% =  0.40pp
                                                 ────────
P(Brasil vence a final | chegou) = 52.96%
```
→ **P(Brasil campeão) = 38.07% × 52.96% = 20.16%** ✓ (bate com a tabela do Top 10)

França é o único adversário contra quem o Brasil fica abaixo de 50% — e é também o que tem mais chance de chegar na final (41.24%), por isso é a "ameaça" mais citada.

## "Chalk bracket" — cada time testado, resto do chaveamento 100% favorito

Cenário: em toda a chave, sempre vence o time com maior probabilidade — **exceto** nas partidas do time sendo avaliado, onde usamos a chance real. Isola a incerteza do próprio caminho do time, sem depender de zebra alheia.

| Time | R16 | QF | SF | Final | Chalk campeão% | Prob. real% |
|------|-----|-----|-----|-------|:---:|:---:|
| França | Paraguai (90%) | Marrocos (68%) | Espanha (54%) | Brasil (56%) | 18.18% | 26.72% |
| Brasil | Noruega (84%) | Inglaterra (64%) | Argentina (64%) | França (44%) | 15.28% | 20.16% |
| Espanha | Portugal (58%) | EUA (72%) | França (46%) | Brasil (51%) | 9.82% | 13.66% |
| Argentina | Egito (73%) | Colômbia (52%) | Brasil (36%) | França (32%) | 4.28% | 6.75% |
| Portugal | Espanha (42%) | EUA (64%) | França (38%) | Brasil (42%) | 4.28% | 6.62% |
| Marrocos | Canadá (78%) | França (32%) | Espanha (37%) | Brasil (36%) | 3.33% | 6.31% |
| Inglaterra | México (61%) | Brasil (36%) | Argentina (53%) | França (32%) | 3.79% | 6.03% |
| Colômbia | Suíça (55%) | Argentina (48%) | Brasil (35%) | França (32%) | 2.99% | 4.86% |
| Suíça | Colômbia (45%) | Argentina (43%) | Brasil (29%) | França (26%) | 1.49% | 2.71% |
| EUA | Bélgica (58%) | Espanha (28%) | França (23%) | Brasil (26%) | 1.01% | 2.21% |

Cada célula = adversário "chalk" daquela fase + chance real do time testado vencer esse confronto específico.

**Leitura:** França e Brasil aparecem como o adversário "chalk" da final pra quase todos os outros 8 times — são os dois super-favoritos do chaveamento. A diferença entre chalk% e prob. real% é maior pra eles (quase metade do valor real) do que pros times menores, porque times grandes se beneficiam proporcionalmente mais de zebras nos ramos alheios — times pequenos já dependem de zebra pra chegar longe de qualquer jeito, então a incerteza "ajuda" menos em termos relativos.

## Confirmação — Monte Carlo 10.000.000 (10 shards paralelos de 1M, `simulate.py` corrigido)

| # | Seleção | Exato | Monte Carlo 10M |
|---|---------|:---:|:---:|
| 1 | França | 26.72% | 26.70% |
| 2 | Brasil | 20.16% | 20.19% |
| 3 | Espanha | 13.66% | 13.67% |
| 4 | Argentina | 6.75% | 6.74% |
| 5 | Portugal | 6.62% | 6.62% |
| 6 | Marrocos | 6.31% | 6.30% |
| 7 | Inglaterra | 6.03% | 6.04% |
| 8 | Colômbia | 4.86% | 4.86% |
| 9 | Suíça | 2.71% | 2.71% |
| 10 | EUA | 2.21% | 2.21% |

Caminho do Brasil (Monte Carlo): vence R16 (chega à QF) 84.25% · chega à semi 56.11% · chega à final 38.12% · Campeão 20.19% — bate com a decomposição exata (84.18% / 56.04% / 38.07% / 20.16%) dentro do ruído esperado de amostragem. Holanda, Alemanha e Japão confirmados em 0% de chance de título (times já eliminados de verdade).
