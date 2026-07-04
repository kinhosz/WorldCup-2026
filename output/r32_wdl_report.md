# R32 — Report W/D/L (Model4)

> Modelo S14 | 16 jogos (mata-mata #73–88) | acurácia 90': 10/16 (62.5%) | acurácia "quem avança": 12/16 (75%)

## Tabela completa

| # | Jogo | Favorito do modelo | Real (90') | Decisão | Quem avançou | 90' | Avanço |
|---|------|--------------------|-----------|---------|--------------|:---:|:---:|
| 73 | África do Sul x Canadá | Canadá 43.7% | 0–1 | 90' | Canadá | ✓ | ✓ |
| 74 | Holanda x Marrocos | Holanda 41.0% (fraco) | 1–1 | PEN | Marrocos | ✗ | ✗ |
| 75 | Alemanha x Paraguai | Alemanha 76.7% | 1–1 | PEN | Paraguai | ✗ | ✗ |
| 76 | França x Suécia | França 83.9% | 3–0 | 90' | França | ✓ | ✓ |
| 81 | Brasil x Japão | Brasil 63.2% | 2–1 | 90+4' | Brasil | ✓ | ✓ |
| 82 | Costa do Marfim x Noruega | Costa do Marfim 41.1% (fraco) | 1–2 | 90' | Noruega | ✗ | ✗ |
| 83 | México x Equador | México 41.6% (fraco) | 2–0 | 90' | México | ✓ | ✓ |
| 84 | Inglaterra x Congo | Inglaterra 61.6% | 2–1 | 90' | Inglaterra | ✓ | ✓ |
| 77 | Bélgica x Senegal | Senegal 38.3% ("no call") | 2–2 | AET | Bélgica | ✗ | ✗ |
| 78 | EUA x Bósnia | EUA 78.0% | 2–0 | 90' | EUA | ✓ | ✓ |
| 79 | Espanha x Áustria | Espanha 64.9% | 3–0 | 90' | Espanha | ✓ | ✓ |
| 80 | Portugal x Croácia | Portugal 71.5% | 2–1 | 90' | Portugal | ✓ | ✓ |
| 85 | Suíça x Argélia | Suíça 46.1% (fraco) | 2–0 | 90' | Suíça | ✓ | ✓ |
| 86 | Colômbia x Gana | Colômbia 53.5% | 1–0 | 90' | Colômbia | ✓ | ✓ |
| 87 | Austrália x Egito | Egito 40.9% (fraco) | 1–1 | PEN | Egito | ✗ | ✓ |
| 88 | Argentina x Cabo Verde | Argentina 75.0% | 1–1 | AET | Argentina | ✗ | ✓ |

## Números gerais

| Métrica | Resultado |
|---------|-----------|
| W/D/L nos 90' correto | 10/16 (62.5%) |
| Quem avança correto | 12/16 (75%) |
| Empates reais (90') | 5/16 (31%) |
| Empates previstos como mais prováveis | 0/16 (0%) |
| Placar exato (Top-1 do modelo) | 3/16 (18.75%) |
| Placar real dentro do Top-3 | 6/16 (37.5%) |

## Empates — como o modelo distribuiu as probabilidades

| Jogo | xG | P(fav) | P(empate) | P(zebra) | Decisão real |
|------|-----|--------|-----------|----------|--------------|
| Holanda x Marrocos | 1.71–1.59 | 41.0% | 23.0% | 36.0% | PEN → Marrocos |
| Alemanha x Paraguai | 2.66–0.80 | 76.7% | 14.4% | 8.9% | PEN → Paraguai |
| Bélgica x Senegal | 1.32–1.37 | 38.3% | 25.9% | 35.8% | AET → Bélgica |
| Austrália x Egito | 0.78–1.04 | 40.9% | 32.3% | 26.8% | PEN → Egito |
| Argentina x Cabo Verde | 1.85–0.33 | 75.0% | 19.2% | 5.7% | AET → Argentina |

Probabilidade média de empate dada pelo modelo nos 5 jogos que realmente empataram nos 90': **22.96%** (baseline aleatório de 3 vias = 33.3%).

## Calibração de confiança (≥70%)

| Jogo | Confiança | Acerto 90'? | Acerto avanço? |
|------|-----------|:---:|:---:|
| França x Suécia | 83.9% | ✓ | ✓ |
| EUA x Bósnia | 78.0% | ✓ | ✓ |
| Alemanha x Paraguai | 76.7% | ✗ | ✗ |
| Argentina x Cabo Verde | 75.0% | ✗ | ✓ |
| Portugal x Croácia | 71.5% | ✓ | ✓ |

Taxa de acerto no bucket ≥70%: **60% (90')** / **80% (avanço)** — bem abaixo dos 97% observados na fase de grupos.

## Dark horse do round

**Paraguai** sobre Alemanha (76.7% de favoritismo) — maior confiança invertida da rodada. Paraguai tinha apenas 8.9% de chance de vitória direta no modelo.

## Arquivo fonte

Previsões: `r32_post1.md` (jogos 73–84) + `r32_post2.md` (jogos 74/77–88). Resultados reais: `output/copa_real_state.json` (`knockout_results`, IDs 73–88).
