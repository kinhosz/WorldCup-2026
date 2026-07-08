# Model6 — Reavaliação Retroativa das 96 Partidas

Todas as partidas já disputadas da Copa 2026, reavaliadas com os pesos **ativos** do Model6 (objetivo por pontos, treinado nesses mesmos 96 jogos). Avaliação **in-sample** — mede ajuste do modelo, não generalização. Quartas em diante são o primeiro teste real fora da amostra.

## Resumo

- **Acerto geral:** 75/96 (78.1%)
- **Pontos (Model6):** 67.00/78 (85.9%)
- **Grupo (W/D/L):** 52/72 (72.2%)
- **Mata-mata (quem avança):** 23/24 (95.8%)
- **Placar exato top-1 (mata-mata):** 20/24
- **Placar exato top-3 (mata-mata):** 23/24

## Rodada 1 (15/24 acertos)

| Confronto | Placar | Pick | Confiança | xG | Top-3 placares | Resultado |
|---|---|---|---|---|---|---|
| Mexico x South Africa | 2–0 | Mexico | 60.9% | 1.54–0.57 | 1-0 18.6%  2-0 14.3%  0-0 12.1% | ✅ |
| South Korea x Czech Republic | 2–1 | South Korea | 37.8% | 1.48–1.48 | 1-1 11.3%  2-1 8.4%  1-2 8.4% | ✅ |
| Canada x Bosnia-Herzegovina | 1–1 | Canada | 43.0% | 1.39–1.13 | 1-1 12.6%  1-0 11.2%  0-1 9.1% | ❌ |
| Qatar x Switzerland | 1–1 | Switzerland | 77.8% | 0.56–2.36 | 0-2 15.1%  0-1 12.8%  0-3 11.9% | ❌ |
| Brazil x Morocco | 1–1 | Morocco | 42.0% | 1.30–1.50 | 1-1 11.8%  0-1 9.1%  1-2 8.9% | ❌ |
| Haiti x Scotland | 0–1 | Scotland | 60.3% | 0.72–1.68 | 0-1 15.2%  0-2 12.7%  1-1 11.0% | ✅ |
| Australia x Turkey | 2–0 | Australia | 35.3% | 1.00–0.97 | 1-0 13.9%  0-0 13.9%  1-1 13.5% | ✅ |
| USA x Paraguay | 4–1 | USA | 44.8% | 1.46–1.13 | 1-1 12.4%  1-0 11.0%  2-1 9.0% | ✅ |
| Germany x Curacao | 7–1 | Germany | 78.7% | 2.50–0.60 | 2-0 14.1%  3-0 11.7%  1-0 11.3% | ✅ |
| Côte d'Ivoire x Ecuador | 1–0 | Côte d'Ivoire | 80.3% | 2.76–0.69 | 2-0 12.1%  3-0 11.1%  1-0 8.8% | ✅ |
| Netherlands x Japan | 2–2 | Netherlands | 64.2% | 2.53–1.30 | 2-1 9.0%  3-1 7.6%  1-1 7.1% | ❌ |
| Sweden x Tunisia | 5–1 | Sweden | 50.2% | 1.94–1.39 | 1-1 9.7%  2-1 9.3%  1-0 6.9% | ✅ |
| Belgium x Egypt | 1–1 | Belgium | 69.6% | 3.95–2.18 | 3-2 5.3%  4-2 5.2%  3-1 4.9% | ❌ |
| Iran x New Zealand | 2–2 | Iran | 88.1% | 4.17–1.07 | 4-1 7.1%  3-1 6.9%  4-0 6.7% | ❌ |
| Saudi Arabia x Uruguay | 1–1 | Uruguay | 75.0% | 0.60–2.26 | 0-2 14.5%  0-1 12.9%  0-3 11.0% | ❌ |
| Spain x Cape Verde | 0–0 | Spain | 79.2% | 2.36–0.49 | 2-0 16.0%  1-0 13.6%  3-0 12.6% | ❌ |
| France x Senegal | 3–1 | France | 54.3% | 1.71–0.99 | 1-0 11.5%  1-1 11.4%  2-0 9.8% | ✅ |
| Iraq x Norway | 1–4 | Norway | 84.7% | 0.91–3.50 | 0-3 8.7%  1-3 7.9%  0-4 7.6% | ✅ |
| Argentina x Algeria | 3–0 | Argentina | 66.6% | 2.91–1.49 | 2-1 7.8%  3-1 7.5%  2-2 5.8% | ✅ |
| Austria x Jordan | 3–1 | Austria | 49.8% | 1.73–1.20 | 1-1 11.1%  2-1 9.6%  1-0 9.2% | ✅ |
| Portugal x Congo | 1–1 | Portugal | 75.8% | 2.85–0.98 | 2-0 8.8%  2-1 8.6%  3-0 8.4% | ❌ |
| Uzbekistan x Colombia | 1–3 | Colombia | 70.9% | 0.57–1.98 | 0-1 15.4%  0-2 15.3%  0-3 10.1% | ✅ |
| England x Croatia | 4–2 | England | 61.8% | 2.10–1.04 | 2-1 9.9%  2-0 9.5%  1-1 9.4% | ✅ |
| Ghana x Panama | 1–0 | Ghana | 54.7% | 1.99–1.24 | 1-1 9.8%  2-1 9.7%  1-0 7.9% | ✅ |

## Rodada 2 (21/24 acertos)

| Confronto | Placar | Pick | Confiança | xG | Top-3 placares | Resultado |
|---|---|---|---|---|---|---|
| Mexico x South Korea | 1–0 | Mexico | 37.7% | 1.46–1.46 | 1-1 11.5%  2-1 8.4%  1-2 8.4% | ✅ |
| South Africa x Czech Republic | 1–1 | Czech Republic | 61.3% | 0.58–1.56 | 0-1 18.3%  0-2 14.3%  0-0 11.7% | ❌ |
| Bosnia-Herzegovina x Switzerland | 1–4 | Switzerland | 75.4% | 0.50–2.13 | 0-2 16.3%  0-1 15.3%  0-3 11.6% | ✅ |
| Canada x Qatar | 6–0 | Canada | 44.1% | 1.54–1.25 | 1-1 11.8%  1-0 9.5%  2-1 9.1% | ✅ |
| Brazil x Haiti | 3–0 | Brazil | 78.8% | 2.38–0.53 | 2-0 15.4%  1-0 13.0%  3-0 12.3% | ✅ |
| Morocco x Scotland | 1–0 | Morocco | 63.9% | 2.06–0.92 | 2-0 10.8%  1-0 10.5%  2-1 9.9% | ✅ |
| Paraguay x Turkey | 1–0 | Paraguay | 33.8% | 0.93–0.93 | 0-0 15.7%  1-0 14.5%  0-1 14.5% | ✅ |
| USA x Australia | 2–0 | USA | 44.5% | 1.53–1.22 | 1-1 11.9%  1-0 9.8%  2-1 9.1% | ✅ |
| Ecuador x Curacao | 0–0 | Empate | 34.0% | 0.87–0.83 | 0-0 18.2%  1-0 15.8%  0-1 15.2% | ✅ |
| Germany x Côte d'Ivoire | 2–1 | Germany | 39.6% | 1.99–1.99 | 1-1 7.4%  2-1 7.4%  1-2 7.4% | ✅ |
| Netherlands x Sweden | 5–1 | Netherlands | 74.1% | 3.08–1.23 | 3-1 8.0%  2-1 7.8%  3-0 6.5% | ✅ |
| Tunisia x Japan | 0–4 | Japan | 58.0% | 1.15–2.04 | 1-2 9.9%  1-1 9.7%  0-2 8.6% | ✅ |
| Belgium x Iran | 0–0 | Belgium | 87.9% | 4.33–1.17 | 4-1 7.0%  3-1 6.5%  5-1 6.1% | ❌ |
| New Zealand x Egypt | 1–3 | Egypt | 99.0% | 0.97–7.73 | 0-7 5.4%  1-7 5.3%  0-8 5.2% | ✅ |
| Spain x Saudi Arabia | 4–0 | Spain | 99.1% | 6.20–0.38 | 6-0 11.0%  5-0 10.7%  7-0 9.7% | ✅ |
| Uruguay x Cape Verde | 2–2 | Empate | 34.6% | 0.86–0.80 | 0-0 19.1%  1-0 16.4%  0-1 15.2% | ✅ |
| France x Iraq | 3–0 | France | 86.0% | 2.77–0.42 | 2-0 15.8%  3-0 14.6%  1-0 11.4% | ✅ |
| Norway x Senegal | 3–2 | Norway | 40.1% | 2.16–2.16 | 2-2 7.2%  2-1 6.7%  1-2 6.7% | ✅ |
| Algeria x Jordan | 2–1 | Algeria | 49.4% | 1.88–1.38 | 1-1 10.0%  2-1 9.4%  1-0 7.2% | ✅ |
| Argentina x Austria | 2–0 | Argentina | 62.7% | 2.54–1.38 | 2-1 8.8%  3-1 7.5%  1-1 7.0% | ✅ |
| Congo x Colombia | 0–1 | Colombia | 59.5% | 1.08–2.04 | 1-2 9.9%  1-1 9.8%  0-2 9.2% | ✅ |
| Portugal x Uzbekistan | 5–0 | Portugal | 84.0% | 2.77–0.52 | 2-0 14.2%  3-0 13.2%  1-0 10.3% | ✅ |
| Croatia x Panama | 1–0 | Croatia | 67.3% | 2.30–0.97 | 2-0 10.1%  2-1 9.8%  1-0 8.8% | ✅ |
| England x Ghana | 0–0 | England | 75.4% | 2.70–0.90 | 2-0 10.0%  3-0 9.0%  2-1 9.0% | ❌ |

## Rodada 3 (16/24 acertos)

| Confronto | Placar | Pick | Confiança | xG | Top-3 placares | Resultado |
|---|---|---|---|---|---|---|
| Mexico x Czech Republic | 3–0 | Mexico | 35.2% | 1.07–1.07 | 1-1 13.5%  1-0 12.6%  0-1 12.6% | ✅ |
| South Africa x South Korea | 1–0 | South Korea | 68.2% | 0.80–2.13 | 0-2 12.2%  0-1 11.4%  1-2 9.7% | ❌ |
| Bosnia-Herzegovina x Qatar | 3–1 | Bosnia-Herzegovina | 35.7% | 1.13–1.13 | 1-1 13.3%  1-0 11.8%  0-1 11.8% | ✅ |
| Canada x Switzerland | 1–2 | Switzerland | 74.8% | 0.69–2.36 | 0-2 13.3%  0-1 11.3%  0-3 10.4% | ✅ |
| Brazil x Scotland | 3–0 | Brazil | 57.6% | 1.76–0.90 | 1-0 12.3%  1-1 11.1%  2-0 10.8% | ✅ |
| Morocco x Haiti | 4–2 | Morocco | 84.0% | 2.79–0.54 | 2-0 14.0%  3-0 13.0%  1-0 10.0% | ✅ |
| Paraguay x Australia | 0–0 | Empate | 33.9% | 0.84–0.87 | 0-0 18.0%  0-1 15.7%  1-0 15.2% | ✅ |
| USA x Turkey | 2–3 | USA | 46.4% | 1.68–1.30 | 1-1 11.1%  2-1 9.3%  1-0 8.6% | ❌ |
| Curacao x Côte d'Ivoire | 0–2 | Côte d'Ivoire | 74.7% | 0.51–2.09 | 0-2 16.3%  0-1 15.6%  0-3 11.4% | ✅ |
| Germany x Ecuador | 1–2 | Germany | 83.9% | 3.28–0.83 | 3-0 9.7%  2-0 8.8%  3-1 8.0% | ❌ |
| Japan x Sweden | 1–1 | Japan | 49.2% | 2.23–1.74 | 2-1 8.2%  1-1 7.3%  2-2 7.1% | ❌ |
| Netherlands x Tunisia | 3–1 | Netherlands | 78.8% | 2.82–0.81 | 2-0 10.5%  3-0 9.9%  2-1 8.6% | ✅ |
| Belgium x New Zealand | 5–1 | Belgium | 99.4% | 8.00–0.80 | 8-0 6.2%  7-0 6.2%  9-0 5.6% | ✅ |
| Egypt x Iran | 1–1 | Egypt | 67.7% | 2.89–1.42 | 2-1 8.0%  3-1 7.7%  2-2 5.7% | ❌ |
| Cape Verde x Saudi Arabia | 0–0 | Cape Verde | 75.0% | 2.38–0.69 | 2-0 13.2%  1-0 11.1%  3-0 10.4% | ❌ |
| Spain x Uruguay | 1–0 | Spain | 75.2% | 2.07–0.47 | 2-0 16.9%  1-0 16.3%  3-0 11.7% | ✅ |
| France x Norway | 4–1 | France | 60.3% | 2.47–1.43 | 2-1 8.8%  3-1 7.3%  1-1 7.2% | ✅ |
| Senegal x Iraq | 5–0 | Senegal | 77.1% | 2.43–0.63 | 2-0 13.9%  1-0 11.4%  3-0 11.2% | ✅ |
| Algeria x Austria | 3–3 | Austria | 40.6% | 1.67–1.76 | 1-1 9.6%  1-2 8.4%  2-1 8.0% | ❌ |
| Argentina x Jordan | 3–1 | Argentina | 74.2% | 2.87–1.08 | 2-1 8.6%  3-1 8.2%  2-0 7.9% | ✅ |
| Congo x Uzbekistan | 3–1 | Congo | 60.3% | 2.24–1.23 | 2-1 9.6%  1-1 8.6%  2-0 7.8% | ✅ |
| Portugal x Colombia | 0–0 | Portugal | 47.5% | 1.33–0.87 | 1-0 14.8%  1-1 12.8%  0-0 11.1% | ❌ |
| Croatia x Ghana | 2–1 | Croatia | 53.4% | 2.12–1.42 | 2-1 9.2%  1-1 8.7%  2-2 6.6% | ✅ |
| England x Panama | 2–0 | England | 84.2% | 2.94–0.61 | 2-0 12.4%  3-0 12.2%  4-0 8.9% | ✅ |

## Round of 32 (15/16 acertos — quem avança)

| Confronto | Placar (90') | Vencedor real | Pick | Confiança | xG | Top-3 placares | Rank placar real | Resultado |
|---|---|---|---|---|---|---|---|---|
| South Africa x Canada | 0–1 | Canada | Canada | 57.1% | 1.00–1.29 | 0-1 13.1%  1-1 13.1%  0-0 10.1% | top-1 (+1.00pt) | ✅ |
| Netherlands x Morocco | 1–1 (PEN) | Morocco | Morocco | 50.3% | 1.65–1.66 | 1-1 10.0%  1-2 8.3%  2-1 8.2% | top-1 (+1.00pt) | ✅ |
| Germany x Paraguay | 1–1 (PEN) | Paraguay | Germany | 69.6% | 1.91–1.00 | 1-1 10.4%  1-0 10.4%  2-1 9.9% | top-1 (+1.00pt) | ❌ |
| France x Sweden | 3–0 | France | France | 87.3% | 3.00–0.80 | 3-0 10.1%  2-0 10.1%  3-1 8.1% | top-1 (+1.00pt) | ✅ |
| Belgium x Senegal | 2–2 (AET) | Belgium | Belgium | 58.0% | 2.44–2.00 | 2-2 7.0%  2-1 7.0%  1-2 5.8% | top-1 (+1.00pt) | ✅ |
| USA x Bosnia-Herzegovina | 2–0 | USA | USA | 72.5% | 2.08–1.00 | 2-0 10.0%  2-1 9.9%  1-0 9.6% | top-1 (+1.00pt) | ✅ |
| Spain x Austria | 3–0 | Spain | Spain | 89.3% | 3.00–0.66 | 3-0 11.6%  2-0 11.6%  4-0 8.7% | top-1 (+1.00pt) | ✅ |
| Portugal x Croatia | 2–1 | Portugal | Portugal | 71.2% | 2.00–1.00 | 2-1 10.0%  2-0 10.0%  1-1 10.0% | top-1 (+1.00pt) | ✅ |
| Brazil x Japan | 2–1 (90+4') | Brazil | Brazil | 67.3% | 2.00–1.17 | 2-1 9.8%  1-1 9.8%  2-0 8.4% | top-1 (+1.00pt) | ✅ |
| Côte d'Ivoire x Norway | 1–2 | Norway | Norway | 61.8% | 1.98–2.64 | 1-2 6.8%  2-2 6.7%  1-3 6.0% | top-1 (+1.00pt) | ✅ |
| Mexico x Ecuador | 2–0 | Mexico | Mexico | 80.2% | 2.00–0.60 | 1-0 14.8%  2-0 14.8%  3-0 9.9% | top-2 (+0.67pt) | ✅ |
| England x Congo | 2–1 | England | England | 83.7% | 3.00–1.02 | 2-1 8.2%  3-1 8.2%  2-0 8.1% | top-1 (+1.00pt) | ✅ |
| Switzerland x Algeria | 2–0 | Switzerland | Switzerland | 71.2% | 2.00–1.00 | 2-0 10.0%  1-0 10.0%  2-1 10.0% | top-1 (+1.00pt) | ✅ |
| Colombia x Ghana | 1–0 | Colombia | Colombia | 69.5% | 1.83–0.95 | 1-0 11.3%  1-1 10.8%  2-0 10.4% | top-1 (+1.00pt) | ✅ |
| Australia x Egypt | 1–1 (PEN) | Egypt | Egypt | 66.5% | 1.21–2.00 | 1-1 9.8%  1-2 9.8%  0-1 8.1% | top-1 (+1.00pt) | ✅ |
| Argentina x Cape Verde | 1–1 (AET) | Argentina | Argentina | 70.4% | 2.00–1.03 | 1-1 10.0%  2-1 10.0%  1-0 9.6% | top-1 (+1.00pt) | ✅ |

## Oitavas de Final (8/8 acertos — quem avança)

| Confronto | Placar (90') | Vencedor real | Pick | Confiança | xG | Top-3 placares | Rank placar real | Resultado |
|---|---|---|---|---|---|---|---|---|
| Canada x Morocco | 0–3 | Morocco | Morocco | 87.5% | 0.78–3.00 | 0-3 10.2%  0-2 10.2%  1-3 8.0% | top-1 (+1.00pt) | ✅ |
| Paraguay x France | 0–1 | France | France | 83.5% | 0.45–2.00 | 0-1 17.2%  0-2 17.2%  0-3 11.5% | top-1 (+1.00pt) | ✅ |
| Belgium x USA | 4–1 | Belgium | Belgium | 83.6% | 4.00–1.67 | 3-1 6.2%  4-1 6.2%  3-2 5.1% | top-2 (+0.67pt) | ✅ |
| Spain x Portugal | 1–0 | Spain | Spain | 63.1% | 1.56–1.00 | 1-0 12.0%  1-1 12.0%  2-0 9.4% | top-1 (+1.00pt) | ✅ |
| Brazil x Norway | 1–2 | Norway | Norway | 50.0% | 2.00–2.00 | 2-2 7.3%  1-2 7.3%  2-1 7.3% | top-2 (+0.67pt) | ✅ |
| Mexico x England | 2–3 | England | England | 75.4% | 0.74–1.89 | 0-1 13.7%  0-2 12.9%  1-1 10.1% | fora do top-3 | ✅ |
| Switzerland x Colombia | 0–0 (PEN) | Switzerland | Switzerland | 50.0% | 1.00–1.00 | 0-0 13.6%  1-0 13.6%  0-1 13.5% | top-1 (+1.00pt) | ✅ |
| Egypt x Argentina | 2–3 | Argentina | Argentina | 66.9% | 2.00–3.00 | 2-3 6.1%  1-3 6.1%  2-2 6.1% | top-1 (+1.00pt) | ✅ |

## Times ainda vivos — todas as combinações possíveis (bônus)

Chaveamento oficial das quartas ainda não confirmado — tabela abaixo é o Model6 aplicado a **todas as combinações possíveis** entre os 8 times restantes (Marrocos, França, Bélgica, Espanha, Noruega, Inglaterra, Suíça, Argentina), ordenada pela diferença de força entre os lados.

| Confronto | xG | Favorito | Confiança | Top-3 placares |
|---|---|---|---|---|
| Spain x Norway | 3.16–1.27 | Spain | 81.3% | 3-1 8.0%  2-1 7.6%  4-1 6.3% |
| Spain x Argentina | 2.69–1.09 | Spain | 79.1% | 2-1 9.0%  2-0 8.3%  3-1 8.1% |
| Belgium x Spain | 1.44–2.92 | Spain | 75.8% | 1-2 7.8%  1-3 7.6%  2-2 5.6% |
| Spain x Switzerland | 1.80–0.75 | Spain | 73.7% | 1-0 14.1%  2-0 12.7%  1-1 10.5% |
| Morocco x Spain | 0.96–2.06 | Spain | 73.1% | 0-2 10.4%  0-1 10.1%  1-2 9.9% |
| France x Norway | 2.47–1.43 | France | 69.6% | 2-1 8.8%  3-1 7.3%  1-1 7.2% |
| Norway x England | 1.60–2.58 | England | 67.9% | 1-2 8.1%  1-3 7.0%  2-2 6.5% |
| France x Argentina | 2.10–1.22 | France | 67.9% | 2-1 9.7%  1-1 9.2%  2-0 7.9% |
| England x Argentina | 2.20–1.38 | England | 66.3% | 2-1 9.3%  1-1 8.5%  3-1 6.8% |
| France x Switzerland | 1.41–0.84 | France | 63.8% | 1-0 14.8%  1-1 12.5%  0-0 10.6% |
| Spain x England | 1.62–1.05 | Spain | 63.1% | 1-1 11.8%  1-0 11.2%  2-1 9.6% |
| France x Belgium | 2.29–1.61 | France | 62.9% | 2-1 8.5%  1-1 7.5%  2-2 6.9% |
| England x Switzerland | 1.47–0.95 | England | 62.5% | 1-0 13.1%  1-1 12.4%  2-0 9.6% |
| Morocco x France | 1.07–1.61 | France | 62.2% | 1-1 11.8%  0-1 11.0%  1-2 9.5% |
| Belgium x England | 1.81–2.39 | England | 60.8% | 1-2 7.7%  2-2 7.0%  1-1 6.5% |
| Morocco x England | 1.21–1.68 | England | 60.5% | 1-1 11.3%  1-2 9.5%  0-1 9.4% |
| France x Spain | 1.00–1.45 | Spain | 60.5% | 1-1 12.5%  0-1 12.5%  1-2 9.0% |
| Belgium x Norway | 3.52–2.89 | Belgium | 59.7% | 3-2 5.0%  3-3 4.8%  4-2 4.4% |
| Belgium x Argentina | 3.00–2.48 | Belgium | 58.6% | 2-2 5.8%  3-2 5.8%  2-3 4.8% |
| Belgium x Switzerland | 2.01–1.71 | Belgium | 56.0% | 2-1 8.4%  1-1 8.4%  2-2 7.1% |
| Morocco x Norway | 2.35–2.03 | Morocco | 55.8% | 2-2 7.1%  2-1 7.0%  1-2 6.1% |
| Morocco x Argentina | 2.00–1.74 | Morocco | 55.1% | 1-1 8.3%  2-1 8.3%  1-2 7.2% |
| Morocco x Switzerland | 1.34–1.20 | Morocco | 53.2% | 1-1 12.7%  1-0 10.6%  0-1 9.5% |
| Morocco x Belgium | 2.17–2.29 | Belgium | 52.2% | 2-2 7.1%  1-2 6.6%  2-1 6.2% |
| France x England | 1.27–1.18 | France | 52.1% | 1-1 12.9%  1-0 10.9%  0-1 10.2% |
| Norway x Switzerland | 1.78–1.84 | Switzerland | 51.3% | 1-1 8.8%  1-2 8.1%  2-1 7.8% |
| Switzerland x Argentina | 1.57–1.52 | Switzerland | 50.9% | 1-1 10.9%  2-1 8.5%  1-2 8.3% |
| Norway x Argentina | 2.65–2.67 | Argentina | 50.3% | 2-2 6.1%  2-3 5.5%  3-2 5.4% |
