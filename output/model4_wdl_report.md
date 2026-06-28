# Model4 — Report W/D/L

> Modelo S14 | 72 jogos | acurácia geral: 46/72 (63.9%)

## Matriz de Confusão

Leitura: linha = resultado real, coluna = o que o modelo previu como mais provável.

| Real \ Previsto | W (vitória A) | D (empate) | L (vitória B) | Total |
|-----------------|---------------|------------|---------------|-------|
| **W** (vitória A) | 37 | 0 | 4 | 41 |
| **D** (empate) | 16 | 0 | 4 | 20 |
| **L** (vitória B) | 2 | 0 | 9 | 11 |
| **Total previsto** | 55 | 0 | 17 | 72 |

## Acurácia por Tipo de Resultado

| Resultado | Ocorrências reais | Acertos | Taxa | Modelo nunca previu? |
|-----------|-------------------|---------|------|----------------------|
| W (vitória time A) | 41 | 37 | 90% | |
| D (empate) | 20 | 0 | 0% | **Sim — 0 previsões de empate** |
| L (vitória time B) | 11 | 9 | 82% | |
| **Total** | **72** | **46** | **64%** | |

## Probabilidade Média do Resultado Correto

| Resultado | Prob média que o modelo dava ao resultado real |
|-----------|------------------------------------------------|
| Vitórias (A) | 68.5% |
| Empates | 24.8% |
| Vitórias (B) | 63.0% |
| Geral | 55.5% |

> Prob média de empate dada pelo modelo nos 20 empates reais: **24.8%** (baseline aleatório = 33.3%)

## Jogos com Resultado Errado (26/72)

| Categoria | Qtd |
|-----------|-----|
| Empate real, modelo previu W | 16 |
| Empate real, modelo previu L | 4 |
| Vitória A real, modelo previu L (zebra) | 4 |
| Vitória B real, modelo previu W (zebra) | 2 |
| Vitória A real, modelo previu D | 0 |
| Vitória B real, modelo previu D | 0 |

### Zebras — modelo errou a direção do resultado

| Jogo | Real | Previsto | P(W) | P(D) | P(L) |
|------|------|----------|------|------|------|
| United States Of America × Turkey | ✓ L (2–3) | ✗ W | 58% | 19% | 22% |
| Germany × Ecuador | ✓ L (1–2) | ✗ W | 58% | 23% | 19% |
| Norway × Senegal | ✓ W (3–2) | ✗ L | 32% | 18% | 50% |
| Paraguay × Turkey | ✓ W (1–0) | ✗ L | 24% | 31% | 46% |
| South Africa × Republic Of Korea | ✓ W (1–0) | ✗ L | 30% | 34% | 37% |
| Australia × Turkey | ✓ W (2–0) | ✗ L | 33% | 33% | 34% |

### Empates reais — como o modelo distribuiu as probabilidades

| Jogo | xG | P(W) | P(D) | P(L) | Previsto | Tier |
|------|-----|------|------|------|----------|------|
| Paraguay × Australia | 0.53–0.80 | 22% | 39% | 39% | L | ✗ errou |
| Portugal × Colombia | 1.01–0.61 | 44% | 34% | 22% | W | ✗ errou |
| Uruguay × Cape Verte | 1.07–0.78 | 42% | 32% | 26% | W | ✗ errou |
| Cape Verte × Saudi Arabia | 1.29–0.56 | 55% | 29% | 16% | W | ✗ errou |
| Ecuador × Curacao | 1.32–0.31 | 63% | 28% | 8% | W | ✗ errou |
| Egypt × Ira | 1.39–0.83 | 50% | 27% | 22% | W | ✗ errou |
| Belgium × Egypt | 1.42–0.86 | 50% | 27% | 23% | W | ✗ errou |
| South Africa × Czech Republic | 1.39–1.04 | 45% | 27% | 28% | W | ✗ errou |
| Spain × Cape Verte | 1.45–0.34 | 66% | 26% | 8% | W | ✗ errou |
| Belgium × Ira | 1.56–0.56 | 62% | 25% | 13% | W | ✗ errou |
| Netherlands × Japan | 1.67–1.27 | 47% | 24% | 29% | W | ✗ errou |
| Brazil × Morocco | 1.72–0.78 | 60% | 23% | 17% | W | ✗ errou |
| Portugal × Congo | 1.70–0.62 | 64% | 23% | 13% | W | ✗ errou |
| England × Ghana | 1.79–0.56 | 67% | 22% | 11% | W | ✗ errou |
| Canada × Bosnia And Herzegovina | 2.08–1.28 | 56% | 21% | 23% | W | ✗ errou |
| Algeria × Austria | 1.75–2.07 | 33% | 21% | 46% | L | ✗ errou |
| Japan × Sweden | 2.11–1.22 | 58% | 21% | 21% | W | ✗ errou |
| Saudi Arabia × Uruguay | 0.63–1.97 | 11% | 20% | 69% | L | ✗ errou |
| Ira × New Zealand | 2.30–1.02 | 66% | 19% | 15% | W | ✗ errou |
| Qatar × Switzerland | 0.56–3.39 | 3% | 8% | 89% | L | ✗ errou |

## Acurácia por Rodada

| Rodada | Jogos | Acertos | Taxa |
|--------|-------|---------|------|
| R1 | 24 | 14 | 58% |
| R2 | 24 | 17 | 71% |
| R3 | 24 | 15 | 62% |

## Acurácia por Grupo

| Grupo | Jogos | Acertos | Taxa | Empates reais | Empates acertados |
|-------|-------|---------|------|---------------|-------------------|
| A | 6 | 4 | 67% | 1 | 0 |
| B | 6 | 4 | 67% | 2 | 0 |
| C | 6 | 5 | 83% | 1 | 0 |
| D | 6 | 2 | 33% | 1 | 0 |
| E | 6 | 4 | 67% | 1 | 0 |
| F | 6 | 4 | 67% | 2 | 0 |
| G | 6 | 2 | 33% | 4 | 0 |
| H | 6 | 2 | 33% | 4 | 0 |
| I | 6 | 5 | 83% | 0 | 0 |
| J | 6 | 5 | 83% | 1 | 0 |
| K | 6 | 4 | 67% | 2 | 0 |
| L | 6 | 5 | 83% | 1 | 0 |
