# Model7 — Reavaliação Retroativa das 102 Partidas

Todas as partidas já disputadas da Copa 2026, reavaliadas com os pesos **ativos** do Model7 (objetivo por pontos, treinado nesses mesmos 102 jogos). Avaliação **in-sample** — mede ajuste do modelo, não generalização. 3º lugar e Final aparecem como previsão (ainda não disputados).

## Resumo

- **Acerto geral:** 77/102 (75.5%)
- **Pontos (Model7):** 77.14/91 (84.8%)
- **Grupo (W/D/L):** 48/72 (66.7%)
- **Mata-mata (quem avança):** 29/30 (96.7%)
- **Placar exato top-1 (mata-mata):** 23/30
- **Placar exato top-3 (mata-mata):** 28/30

## Rodada 1 (14/24 acertos)

| Confronto | Placar | Pick | Confiança | xG | Top-3 placares | Resultado |
|---|---|---|---|---|---|---|
| Mexico x South Africa | 2–0 | Mexico | 59.4% | 1.51–0.60 | 1-0 18.3%  2-0 13.8%  0-0 12.1% | ✅ |
| South Korea x Czech Republic | 2–1 | South Korea | 37.4% | 1.41–1.41 | 1-1 11.8%  1-0 8.4%  0-1 8.4% | ✅ |
| Canada x Bosnia-Herzegovina | 1–1 | Canada | 39.0% | 1.21–1.08 | 1-1 13.2%  1-0 12.2%  0-1 10.9% | ❌ |
| Qatar x Switzerland | 1–1 | Switzerland | 75.2% | 0.54–2.18 | 0-2 15.7%  0-1 14.4%  0-3 11.4% | ❌ |
| USA x Paraguay | 4–1 | USA | 50.2% | 1.67–1.12 | 1-1 11.5%  1-0 10.3%  2-1 9.6% | ✅ |
| Australia x Turkey | 2–0 | Turkey | 63.8% | 0.60–1.68 | 0-1 17.2%  0-2 14.5%  1-1 10.3% | ❌ |
| Brazil x Morocco | 1–1 | Morocco | 41.5% | 1.55–1.70 | 1-1 10.2%  1-2 8.7%  2-1 7.9% | ❌ |
| Haiti x Scotland | 0–1 | Scotland | 58.9% | 0.89–1.80 | 0-1 12.2%  0-2 11.0%  1-1 10.9% | ✅ |
| Germany x Curacao | 7–1 | Germany | 85.2% | 2.57–0.35 | 2-0 17.8%  3-0 15.3%  1-0 13.8% | ✅ |
| Côte d'Ivoire x Ecuador | 1–0 | Côte d'Ivoire | 77.5% | 2.89–0.92 | 2-0 9.2%  3-0 8.9%  2-1 8.5% | ✅ |
| Netherlands x Japan | 2–2 | Netherlands | 54.5% | 2.29–1.54 | 2-1 8.8%  1-1 7.7%  2-2 6.7% | ❌ |
| Sweden x Tunisia | 5–1 | Sweden | 46.8% | 1.67–1.27 | 1-1 11.2%  2-1 9.4%  1-0 8.8% | ✅ |
| Belgium x Egypt | 1–1 | Belgium | 69.9% | 3.41–1.72 | 3-1 6.7%  2-1 5.9%  3-2 5.8% | ❌ |
| Iran x New Zealand | 2–2 | Iran | 91.7% | 4.47–0.91 | 4-0 7.6%  4-1 7.0%  5-0 6.8% | ❌ |
| Spain x Cape Verde | 0–0 | Spain | 85.1% | 2.81–0.48 | 2-0 14.7%  3-0 13.7%  1-0 10.5% | ❌ |
| Saudi Arabia x Uruguay | 1–1 | Uruguay | 92.5% | 0.49–3.76 | 0-3 12.6%  0-4 11.9%  0-2 10.1% | ❌ |
| France x Senegal | 3–1 | France | 63.7% | 2.03–0.90 | 2-0 11.0%  1-0 10.9%  2-1 9.9% | ✅ |
| Iraq x Norway | 1–4 | Norway | 81.3% | 0.86–3.09 | 0-3 9.5%  0-2 9.2%  1-3 8.1% | ✅ |
| Argentina x Algeria | 3–0 | Argentina | 71.8% | 3.40–1.60 | 3-1 7.1%  2-1 6.2%  4-1 6.0% | ✅ |
| Austria x Jordan | 3–1 | Austria | 58.5% | 2.01–1.10 | 2-1 9.9%  1-1 9.8%  2-0 9.0% | ✅ |
| Portugal x Congo | 1–1 | Portugal | 86.3% | 3.54–0.83 | 3-0 9.4%  4-0 8.3%  2-0 7.9% | ❌ |
| Uzbekistan x Colombia | 1–3 | Colombia | 70.9% | 0.58–2.00 | 0-1 15.1%  0-2 15.1%  0-3 10.1% | ✅ |
| England x Croatia | 4–2 | England | 40.5% | 1.55–1.43 | 1-1 11.2%  2-1 8.7%  1-2 8.1% | ✅ |
| Ghana x Panama | 1–0 | Ghana | 55.6% | 1.93–1.15 | 1-1 10.2%  2-1 9.8%  1-0 8.8% | ✅ |

## Rodada 2 (17/24 acertos)

| Confronto | Placar | Pick | Confiança | xG | Top-3 placares | Resultado |
|---|---|---|---|---|---|---|
| Mexico x South Korea | 1–0 | South Korea | 37.2% | 1.37–1.37 | 1-1 12.1%  0-1 8.8%  1-0 8.8% | ❌ |
| South Africa x Czech Republic | 1–1 | Czech Republic | 60.0% | 0.62–1.55 | 0-1 17.7%  0-2 13.7%  0-0 11.4% | ❌ |
| Canada x Qatar | 6–0 | Canada | 40.2% | 1.37–1.22 | 1-1 12.6%  1-0 10.3%  0-1 9.2% | ✅ |
| Bosnia-Herzegovina x Switzerland | 1–4 | Switzerland | 72.3% | 0.48–1.93 | 0-1 17.4%  0-2 16.8%  0-3 10.8% | ✅ |
| USA x Australia | 2–0 | USA | 50.2% | 1.73–1.19 | 1-1 11.1%  2-1 9.6%  1-0 9.4% | ✅ |
| Paraguay x Turkey | 1–0 | Turkey | 63.3% | 0.56–1.62 | 0-1 18.2%  0-2 14.8%  0-0 11.2% | ❌ |
| Brazil x Haiti | 3–0 | Brazil | 76.3% | 2.53–0.74 | 2-0 12.2%  3-0 10.3%  1-0 9.6% | ✅ |
| Morocco x Scotland | 1–0 | Morocco | 59.1% | 2.05–1.10 | 2-1 9.9%  1-1 9.7%  2-0 9.0% | ✅ |
| Germany x Côte d'Ivoire | 2–1 | Germany | 49.5% | 1.73–1.21 | 1-1 11.1%  2-1 9.6%  1-0 9.1% | ✅ |
| Ecuador x Curacao | 0–0 | Ecuador | 49.5% | 1.37–0.83 | 1-0 15.1%  1-1 12.6%  0-0 11.0% | ❌ |
| Netherlands x Sweden | 5–1 | Netherlands | 70.6% | 2.74–1.15 | 2-1 8.8%  3-1 8.1%  2-0 7.6% | ✅ |
| Tunisia x Japan | 0–4 | Japan | 63.7% | 1.06–2.23 | 1-2 9.8%  0-2 9.2%  1-1 8.8% | ✅ |
| Belgium x Iran | 0–0 | Belgium | 87.7% | 4.06–1.03 | 4-1 7.2%  3-1 7.1%  4-0 7.0% | ❌ |
| New Zealand x Egypt | 1–3 | Egypt | 99.2% | 0.77–7.47 | 0-7 6.8%  0-6 6.4%  0-8 6.4% | ✅ |
| Spain x Saudi Arabia | 4–0 | Spain | 99.6% | 6.75–0.29 | 6-0 11.5%  7-0 11.1%  5-0 10.2% | ✅ |
| Uruguay x Cape Verde | 2–2 | Uruguay | 54.9% | 1.56–0.82 | 1-0 14.4%  1-1 11.8%  2-0 11.3% | ❌ |
| France x Iraq | 3–0 | France | 89.7% | 3.14–0.40 | 3-0 15.0%  2-0 14.3%  4-0 11.8% | ✅ |
| Norway x Senegal | 3–2 | Norway | 40.9% | 2.00–1.93 | 2-1 7.6%  1-1 7.6%  2-2 7.3% | ✅ |
| Argentina x Austria | 2–0 | Argentina | 57.3% | 2.62–1.71 | 2-1 7.7%  3-1 6.7%  2-2 6.6% | ✅ |
| Algeria x Jordan | 2–1 | Algeria | 48.2% | 1.88–1.43 | 1-1 9.8%  2-1 9.2%  1-2 7.0% | ✅ |
| Portugal x Uzbekistan | 5–0 | Portugal | 88.7% | 3.18–0.48 | 3-0 13.8%  2-0 13.0%  4-0 11.0% | ✅ |
| Congo x Colombia | 0–1 | Colombia | 65.0% | 1.01–2.23 | 1-2 9.8%  0-2 9.8%  1-1 8.8% | ✅ |
| England x Ghana | 0–0 | England | 62.1% | 2.24–1.15 | 2-1 9.7%  1-1 8.7%  2-0 8.5% | ❌ |
| Croatia x Panama | 1–0 | Croatia | 73.2% | 2.42–0.80 | 2-0 11.7%  1-0 9.7%  3-0 9.5% | ✅ |

## Rodada 3 (17/24 acertos)

| Confronto | Placar | Pick | Confiança | xG | Top-3 placares | Resultado |
|---|---|---|---|---|---|---|
| Mexico x Czech Republic | 3–0 | Mexico | 35.7% | 1.13–1.13 | 1-1 13.3%  1-0 11.9%  0-1 11.8% | ✅ |
| South Africa x South Korea | 1–0 | South Korea | 64.3% | 0.75–1.89 | 0-1 13.4%  0-2 12.7%  1-1 10.1% | ❌ |
| Canada x Switzerland | 1–2 | Switzerland | 74.4% | 0.62–2.25 | 0-2 14.3%  0-1 12.7%  0-3 10.7% | ✅ |
| Bosnia-Herzegovina x Qatar | 3–1 | Bosnia-Herzegovina | 35.0% | 1.05–1.05 | 1-1 13.5%  1-0 12.9%  0-1 12.9% | ✅ |
| USA x Turkey | 2–3 | Turkey | 61.5% | 1.14–2.20 | 1-2 9.8%  1-1 8.9%  0-2 8.6% | ✅ |
| Paraguay x Australia | 0–0 | Empate | 33.7% | 0.86–0.87 | 0-0 17.7%  0-1 15.5%  1-0 15.2% | ✅ |
| Brazil x Scotland | 3–0 | Brazil | 55.6% | 1.90–1.12 | 1-1 10.4%  2-1 9.9%  1-0 9.3% | ✅ |
| Morocco x Haiti | 4–2 | Morocco | 79.3% | 2.73–0.73 | 2-0 11.8%  3-0 10.7%  1-0 8.6% | ✅ |
| Germany x Ecuador | 1–2 | Germany | 83.4% | 2.96–0.66 | 2-0 11.7%  3-0 11.5%  4-0 8.5% | ❌ |
| Curacao x Côte d'Ivoire | 0–2 | Côte d'Ivoire | 81.5% | 0.49–2.51 | 0-2 15.7%  0-3 13.1%  0-1 12.5% | ✅ |
| Netherlands x Tunisia | 3–1 | Netherlands | 76.2% | 2.72–0.87 | 2-0 10.2%  3-0 9.2%  2-1 8.9% | ✅ |
| Japan x Sweden | 1–1 | Japan | 56.4% | 2.24–1.41 | 2-1 9.2%  1-1 8.2%  3-1 6.9% | ❌ |
| Belgium x New Zealand | 5–1 | Belgium | 99.6% | 8.00–0.59 | 7-0 7.7%  8-0 7.7%  9-0 6.9% | ✅ |
| Egypt x Iran | 1–1 | Egypt | 65.6% | 2.66–1.34 | 2-1 8.7%  3-1 7.7%  1-1 6.6% | ❌ |
| Spain x Uruguay | 1–0 | Spain | 69.9% | 2.07–0.68 | 2-0 13.7%  1-0 13.3%  3-0 9.5% | ✅ |
| Cape Verde x Saudi Arabia | 0–0 | Cape Verde | 79.9% | 2.68–0.66 | 2-0 12.7%  3-0 11.3%  1-0 9.5% | ❌ |
| France x Norway | 4–1 | France | 67.5% | 2.58–1.18 | 2-1 9.1%  3-1 7.9%  2-0 7.8% | ✅ |
| Senegal x Iraq | 5–0 | Senegal | 74.9% | 2.35–0.68 | 2-0 13.4%  1-0 11.4%  3-0 10.5% | ✅ |
| Argentina x Jordan | 3–1 | Argentina | 77.1% | 3.16–1.13 | 3-1 8.1%  2-1 7.7%  3-0 7.2% | ✅ |
| Algeria x Austria | 3–3 | Austria | 51.6% | 1.55–2.16 | 1-2 8.8%  1-1 8.2%  2-2 6.9% | ❌ |
| Portugal x Colombia | 0–0 | Portugal | 55.6% | 1.60–0.83 | 1-0 14.1%  1-1 11.7%  2-0 11.3% | ❌ |
| Congo x Uzbekistan | 3–1 | Congo | 53.9% | 2.00–1.29 | 1-1 9.6%  2-1 9.6%  1-0 7.5% | ✅ |
| England x Panama | 2–0 | England | 75.0% | 2.47–0.75 | 2-0 12.2%  3-0 10.0%  1-0 9.9% | ✅ |
| Croatia x Ghana | 2–1 | Croatia | 59.6% | 2.19–1.22 | 2-1 9.7%  1-1 8.8%  2-0 8.0% | ✅ |

## Round of 32 (15/16 acertos)

| Confronto | Placar (90') | Vencedor real | Pick | Confiança | xG | Top-3 placares | Rank placar real | Resultado |
|---|---|---|---|---|---|---|---|---|
| South Africa x Canada | 0–1 | Canada | Canada | 54.2% | 1.00–1.17 | 0-1 13.4%  1-1 13.4%  0-0 11.4% | top-1 (+1.00pt) | ✅ |
| Netherlands x Morocco | 1–1 (PEN) | Morocco | Morocco | 50.0% | 1.77–1.77 | 1-1 9.1%  1-2 8.0%  2-1 8.0% | top-1 (+1.00pt) | ✅ |
| Germany x Paraguay | 1–1 (PEN) | Paraguay | Germany | 78.8% | 1.83–0.56 | 1-0 16.8%  2-0 15.4%  3-0 9.4% | fora do top-3 | ❌ |
| France x Sweden | 3–0 | France | France | 90.1% | 3.09–0.65 | 3-0 11.7%  2-0 11.3%  4-0 9.0% | top-1 (+1.00pt) | ✅ |
| Brazil x Japan | 2–1 | Brazil | Brazil | 60.8% | 2.00–1.47 | 2-1 9.1%  1-1 9.1%  2-2 6.7% | top-1 (+1.00pt) | ✅ |
| Côte d'Ivoire x Norway | 1–2 | Norway | Norway | 57.4% | 1.88–2.28 | 1-2 7.6%  2-2 7.2%  1-1 6.7% | top-1 (+1.00pt) | ✅ |
| Mexico x Ecuador | 2–0 | Mexico | Mexico | 74.3% | 2.00–0.86 | 2-0 11.4%  1-0 11.4%  2-1 9.9% | top-1 (+1.00pt) | ✅ |
| England x Congo | 2–1 | England | England | 78.0% | 2.74–1.19 | 2-1 8.8%  3-1 8.0%  2-0 7.4% | top-1 (+1.00pt) | ✅ |
| Belgium x Senegal | 2–2 (AET) | Belgium | Belgium | 65.2% | 2.45–1.64 | 2-1 8.3%  2-2 6.8%  1-1 6.8% | top-2 (+0.67pt) | ✅ |
| USA x Bosnia-Herzegovina | 2–0 | USA | USA | 72.8% | 2.10–1.00 | 2-0 9.9%  2-1 9.9%  1-0 9.4% | top-1 (+1.00pt) | ✅ |
| Spain x Austria | 3–0 | Spain | Spain | 89.1% | 3.00–0.67 | 3-0 11.4%  2-0 11.4%  4-0 8.6% | top-1 (+1.00pt) | ✅ |
| Portugal x Croatia | 2–1 | Portugal | Portugal | 71.2% | 2.00–1.00 | 2-1 10.0%  1-1 10.0%  2-0 10.0% | top-1 (+1.00pt) | ✅ |
| Switzerland x Algeria | 2–0 | Switzerland | Switzerland | 71.2% | 2.00–1.00 | 2-0 10.0%  2-1 10.0%  1-0 9.9% | top-1 (+1.00pt) | ✅ |
| Colombia x Ghana | 1–0 | Colombia | Colombia | 68.7% | 1.82–0.97 | 1-0 11.2%  1-1 10.8%  2-0 10.2% | top-1 (+1.00pt) | ✅ |
| Australia x Egypt | 1–1 (PEN) | Egypt | Egypt | 70.9% | 1.01–2.00 | 1-1 10.0%  1-2 10.0%  0-1 9.8% | top-1 (+1.00pt) | ✅ |
| Argentina x Cape Verde | 1–1 (AET) | Argentina | Argentina | 73.3% | 2.45–1.22 | 2-1 9.3%  2-0 7.6%  1-1 7.6% | top-3 (+0.44pt) | ✅ |

## Oitavas de Final (8/8 acertos)

| Confronto | Placar (90') | Vencedor real | Pick | Confiança | xG | Top-3 placares | Rank placar real | Resultado |
|---|---|---|---|---|---|---|---|---|
| Belgium x USA | 4–1 | Belgium | Belgium | 85.9% | 4.00–1.49 | 4-1 6.6%  3-1 6.6%  5-1 5.3% | top-1 (+1.00pt) | ✅ |
| Spain x Portugal | 1–0 | Spain | Spain | 63.9% | 1.60–1.00 | 1-0 11.9%  1-1 11.9%  2-0 9.5% | top-1 (+1.00pt) | ✅ |
| Brazil x Norway | 1–2 | Norway | Norway | 50.0% | 2.00–2.00 | 1-2 7.3%  2-2 7.3%  1-1 7.3% | top-1 (+1.00pt) | ✅ |
| Canada x Morocco | 0–3 | Morocco | Morocco | 87.5% | 0.78–3.00 | 0-3 10.2%  0-2 10.2%  1-3 8.0% | top-1 (+1.00pt) | ✅ |
| Paraguay x France | 0–1 | France | France | 89.1% | 0.40–2.45 | 0-2 17.3%  0-3 14.1%  0-1 14.1% | top-3 (+0.44pt) | ✅ |
| Mexico x England | 2–3 | England | England | 66.4% | 0.96–1.68 | 0-1 12.1%  1-1 11.5%  0-2 10.1% | fora do top-3 | ✅ |
| Switzerland x Colombia | 0–0 (PEN) | Switzerland | Switzerland | 50.0% | 1.00–1.00 | 0-0 13.5%  1-0 13.5%  0-1 13.5% | top-1 (+1.00pt) | ✅ |
| Egypt x Argentina | 2–3 | Argentina | Argentina | 66.9% | 2.00–3.00 | 1-3 6.1%  2-3 6.1%  1-2 6.1% | top-2 (+0.67pt) | ✅ |

## Quartas de Final (4/4 acertos)

| Confronto | Placar (90') | Vencedor real | Pick | Confiança | xG | Top-3 placares | Rank placar real | Resultado |
|---|---|---|---|---|---|---|---|---|
| Morocco x France | 0–2 | France | France | 71.2% | 1.00–2.00 | 0-2 10.0%  1-2 10.0%  0-1 10.0% | top-1 (+1.00pt) | ✅ |
| Norway x England | 1–1 (AET) | England | England | 52.7% | 1.86–2.00 | 1-1 7.8%  1-2 7.8%  2-1 7.3% | top-1 (+1.00pt) | ✅ |
| Belgium x Spain | 1–2 | Spain | Spain | 76.5% | 1.20–2.65 | 1-2 9.0%  1-3 7.9%  0-2 7.4% | top-1 (+1.00pt) | ✅ |
| Switzerland x Argentina | 1–1 (AET) | Argentina | Argentina | 52.0% | 1.59–1.68 | 1-1 10.2%  1-2 8.5%  2-1 8.1% | top-1 (+1.00pt) | ✅ |

## Semifinal (2/2 acertos)

| Confronto | Placar (90') | Vencedor real | Pick | Confiança | xG | Top-3 placares | Rank placar real | Resultado |
|---|---|---|---|---|---|---|---|---|
| France x Spain | 0–2 | Spain | Spain | 60.8% | 1.00–1.45 | 0-1 12.5%  1-1 12.5%  0-2 9.1% | top-3 (+0.44pt) | ✅ |
| England x Argentina | 1–2 | Argentina | Argentina | 50.6% | 1.97–2.00 | 1-2 7.4%  1-1 7.4%  2-2 7.3% | top-1 (+1.00pt) | ✅ |

## Final + 3º Lugar (previsões — ainda não disputados)

### 3º Lugar: France x England

- **xG:** 1.89 – 0.93
- **90':** France 59.9% · Empate 22.0% · England 18.1%
- **Sem prorrogação** (regra FIFA do 3º lugar) — empate nos 90' vai direto pra pênaltis 50/50
- **Quem avança:** France 70.9% x England 29.1%
- **Aposta assertiva:** Mais de 2.5 gols — 53.5%
- **Top-3 placares:** 1-0 11.3%  2-0 10.7%  1-1 10.5%

### Final: Spain x Argentina

- **xG:** 3.09 – 1.06
- **90':** Spain 77.5% · Empate 12.9% · Argentina 9.6%
- **Prorrogação (dado empate nos 90'):** Spain 6.7% · ainda empatado 4.5% · Argentina 1.6% (pênaltis 50/50 resolvem o resto)
- **Quem avança:** Spain 86.5% x Argentina 13.5%
- **Aposta assertiva:** Mais de 2.5 gols — 78.2%
- **Top-3 placares:** 3-1 8.2%  2-1 7.9%  3-0 7.7%

## Seleções — Scores e Biases (Model7)

Ranking das 48 seleções só com dados do Model7: scores de setor (GK/DEF/MID/ATT, 0.1–1.0, de `team_scores.json`) + biases por seleção calibrados pelo Model7 + xG contra um adversário médio (recomputado com os pesos e biases ativos — não usa o `xg_vs_average_opponent` salvo em `team_scores.json`, que é de uma calibração antiga sem biases).

| # | Seleção | Grupo | GK | DEF | MID | ATT | Att Bias | Def Bias | xG vs média | Nota |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Spain | H | 0.863 | 0.663 | 0.866 | 0.707 | 1.13 | 1.30 | 2.73 | defesa bem acima do esperado |
| 2 | Belgium | G | 0.587 | 0.453 | 0.861 | 0.663 | 1.15 | 0.75 | 2.71 | defesa bem abaixo do esperado |
| 3 | Argentina | J | 0.839 | 0.854 | 0.808 | 0.697 | 1.04 | 0.51 | 2.38 | defesa bem abaixo do esperado |
| 4 | France | I | 0.854 | 1.000 | 0.764 | 0.841 | 0.95 | 1.07 | 2.25 |  |
| 5 | Portugal | K | 0.777 | 0.784 | 1.000 | 0.856 | 0.79 | 0.96 | 2.25 | ataque bem abaixo do esperado |
| 6 | Norway | I | 0.262 | 0.222 | 0.422 | 1.000 | 1.17 | 1.35 | 2.21 | ataque bem acima do esperado · defesa bem acima do esperado |
| 7 | Netherlands | F | 0.350 | 0.954 | 0.615 | 0.815 | 0.97 | 0.96 | 1.99 |  |
| 8 | Morocco | C | 0.625 | 0.527 | 0.604 | 0.681 | 0.99 | 0.90 | 1.88 |  |
| 9 | Egypt | G | 0.571 | 0.222 | 0.278 | 0.885 | 1.18 | 0.92 | 1.77 | ataque bem acima do esperado |
| 10 | Brazil | C | 1.000 | 0.970 | 0.787 | 0.964 | 0.68 | 0.58 | 1.74 | ataque bem abaixo do esperado · defesa bem abaixo do esperado |
| 11 | England | L | 0.779 | 0.794 | 0.703 | 0.852 | 0.77 | 0.76 | 1.74 | ataque bem abaixo do esperado · defesa bem abaixo do esperado |
| 12 | Croatia | L | 0.688 | 0.494 | 0.627 | 0.448 | 1.01 | 0.85 | 1.71 |  |
| 13 | Senegal | I | 0.713 | 0.528 | 0.350 | 0.761 | 1.13 | 0.95 | 1.68 |  |
| 14 | Germany | E | 0.835 | 0.759 | 0.692 | 0.608 | 0.85 | 0.84 | 1.68 | ataque bem abaixo do esperado · defesa bem abaixo do esperado |
| 15 | Côte d'Ivoire | E | 0.426 | 0.565 | 0.488 | 0.663 | 0.99 | 1.00 | 1.64 |  |
| 16 | Japan | F | 0.423 | 0.537 | 0.604 | 0.438 | 1.00 | 0.84 | 1.63 | defesa bem abaixo do esperado |
| 17 | USA | D | 0.415 | 0.387 | 0.521 | 0.499 | 1.00 | 0.73 | 1.53 | defesa bem abaixo do esperado |
| 18 | Uruguay | H | 0.712 | 0.698 | 0.503 | 0.520 | 1.00 | 1.00 | 1.52 |  |
| 19 | Austria | J | 0.480 | 0.502 | 0.629 | 0.293 | 1.00 | 0.82 | 1.52 | defesa bem abaixo do esperado |
| 20 | Turkey | D | 0.689 | 0.596 | 0.610 | 0.304 | 1.00 | 1.00 | 1.49 |  |
| 21 | South Korea | A | 0.505 | 0.240 | 0.438 | 0.823 | 0.82 | 0.91 | 1.43 | ataque bem abaixo do esperado |
| 22 | Algeria | J | 0.449 | 0.364 | 0.540 | 0.503 | 0.90 | 0.72 | 1.42 | defesa bem abaixo do esperado |
| 23 | Congo | K | 0.271 | 0.523 | 0.258 | 0.849 | 1.00 | 1.00 | 1.41 |  |
| 24 | Colombia | K | 0.637 | 0.637 | 0.455 | 0.910 | 0.76 | 1.18 | 1.41 | ataque bem abaixo do esperado · defesa bem acima do esperado |
| 25 | Switzerland | B | 0.675 | 0.629 | 0.476 | 0.535 | 0.94 | 1.14 | 1.40 |  |
| 26 | Ghana | L | 0.409 | 0.293 | 0.365 | 0.615 | 1.00 | 1.00 | 1.37 |  |
| 27 | Scotland | C | 0.444 | 0.429 | 0.451 | 0.351 | 1.00 | 1.00 | 1.24 |  |
| 28 | Sweden | F | 0.414 | 0.460 | 0.209 | 0.759 | 1.00 | 1.00 | 1.22 |  |
| 29 | Czech Republic | A | 0.572 | 0.632 | 0.395 | 0.436 | 0.95 | 0.94 | 1.17 |  |
| 30 | Mexico | A | 0.526 | 0.568 | 0.292 | 0.319 | 1.26 | 1.11 | 1.14 | ataque bem acima do esperado |
| 31 | Cape Verde | H | 0.449 | 0.315 | 0.343 | 0.296 | 1.11 | 1.20 | 1.08 | defesa bem acima do esperado |
| 32 | Iran | G | 0.332 | 0.238 | 0.346 | 0.369 | 1.00 | 1.00 | 1.06 |  |
| 33 | Jordan | J | 0.449 | 0.280 | 0.278 | 0.435 | 1.00 | 1.00 | 1.00 |  |
| 34 | Tunisia | F | 0.449 | 0.232 | 0.270 | 0.377 | 1.00 | 1.00 | 0.93 |  |
| 35 | Ecuador | E | 0.515 | 0.487 | 0.231 | 0.423 | 0.99 | 0.66 | 0.90 | defesa bem abaixo do esperado |
| 36 | Panama | L | 0.449 | 0.276 | 0.212 | 0.452 | 1.00 | 1.00 | 0.89 |  |
| 37 | Canada | B | 0.378 | 0.100 | 0.179 | 0.495 | 1.00 | 1.13 | 0.88 |  |
| 38 | Uzbekistan | K | 0.449 | 0.280 | 0.212 | 0.380 | 1.00 | 1.00 | 0.82 |  |
| 39 | Haiti | C | 0.317 | 0.286 | 0.372 | 0.100 | 1.00 | 1.00 | 0.82 |  |
| 40 | Australia | D | 0.497 | 0.321 | 0.235 | 0.435 | 0.87 | 1.13 | 0.80 |  |
| 41 | Qatar | B | 0.449 | 0.280 | 0.278 | 0.349 | 0.84 | 0.86 | 0.76 | ataque bem abaixo do esperado |
| 42 | Paraguay | D | 0.449 | 0.337 | 0.200 | 0.251 | 1.16 | 1.28 | 0.76 | ataque bem acima do esperado · defesa bem acima do esperado |
| 43 | Iraq | I | 0.449 | 0.280 | 0.226 | 0.289 | 1.00 | 1.00 | 0.75 |  |
| 44 | Bosnia-Herzegovina | B | 0.449 | 0.217 | 0.170 | 0.357 | 0.95 | 1.11 | 0.68 |  |
| 45 | Saudi Arabia | H | 0.261 | 0.187 | 0.104 | 0.412 | 1.00 | 1.00 | 0.65 |  |
| 46 | South Africa | A | 0.449 | 0.280 | 0.278 | 0.366 | 0.67 | 1.00 | 0.63 | ataque bem abaixo do esperado |
| 47 | New Zealand | G | 0.100 | 0.194 | 0.100 | 0.382 | 1.00 | 1.00 | 0.61 |  |
| 48 | Curacao | E | 0.470 | 0.164 | 0.159 | 0.157 | 1.00 | 1.00 | 0.47 |  |
