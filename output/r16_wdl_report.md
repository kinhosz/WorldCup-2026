# Model5 — Análise "Quem Avança" das Oitavas (R16)

8 jogos, mata-mata puro. Metodologia: `P(avança) = P(vence) + 0.5 × P(empate)`. Pênaltis tratados como 50/50 (ver seção "Metodologia de Mata-Mata" no `CLAUDE.md`).

Fonte das previsões: `r16_post1.md` (Canadá-Marrocos, Paraguai-França, Brasil-Noruega, México-Inglaterra) + `r16_post2.md` (Bélgica-EUA, Espanha-Portugal, Suíça-Colômbia, Egito-Argentina). Resultados reais: `output/copa_real_state.json` (`knockout_results`, IDs 89–96 — 95 e 96 ainda não registrados no state, ver TODO no fim).

## Tabela completa

| Jogo | xG previsto | Quem avança (previsão) | Real | Acerto? | Aposta do modelo | Resultado da aposta | Top-3 placar | Placar real |
|---|---|---|---|---|---|---|---|---|
| Canadá x Marrocos | 0.73 · 2.06 | Marrocos 78.1% | Marrocos 3–0 | ✅ | (sem sinal claro) | — | 0–2 13.1% · 0–1 12.6% · 1–2 9.5% | 0–3 (fora do top-3) |
| Paraguai x França | 0.23 · 2.13 | França 89.6% | França 1–0 | ✅ | Clean sheet França 79.4% | ✅ | 0–2 21.4% · 0–1 20.0% · 0–3 15.2% | 0–1 (2º mais provável) |
| Brasil x Noruega | 3.17 · 1.09 | **Brasil 84.3%** | Noruega 2–1 | ❌ **zebra** | Over 2.5 gols 79.8% | ✅ | 3–1 8.2% · 2–1 7.7% · 3–0 7.5% | 1–2 (fora do top-3) |
| México x Inglaterra | 0.77 · 1.21 | Inglaterra 61.3% | Inglaterra 3–2 | ✅ | Under 2.5 gols 68.2% | ❌ | 0–1 16.7% · 0–0 13.8% · 1–1 12.8% | 2–3 (fora do top-3) |
| Bélgica x EUA | 1.14 · 1.48 | Bélgica 58.0% | Bélgica 4–1 | ✅ | (sem sinal claro) | — | 1–1 12.3% · 0–1 10.8% · 1–2 9.1% | 4–1 (fora do top-3) |
| Espanha x Portugal | 0.87 · 0.61 | Espanha 57.9% | Espanha 1–0 | ✅ | Under 2.5 gols 81.5% | ✅ | 0–0 22.9% · 1–0 20.0% · 0–1 13.8% | 1–0 (2º mais provável) |
| Suíça x Colômbia | 0.64 · 0.80 | Colômbia 54.6% | Suíça (pênaltis, 0–0 nos 90') | ❌ | Under 2.5 gols 82.4% | ✅ | 0–0 23.7% · 0–1 18.8% · 1–0 15.3% | **0–0 (era o Nº1)** |
| Egito x Argentina | 0.65 · 1.61 | Argentina 72.8% | Argentina 3–2 | ✅ | Not BTTS 61.7% | ❌ | 0–1 16.8% · 0–2 13.5% · 1–1 11.0% | 2–3 (fora do top-3) |

## Números consolidados

- **Quem avança: 6/8 (75%)** — errou Brasil x Noruega (zebra grande, 84.3% de confiança) e Suíça x Colômbia (54.6%, decidido nos pênaltis)
- **Faixa de confiança ≥70%: 3/4 (75%)** — Canadá-Marrocos ✅, Paraguai-França ✅, Brasil-Noruega ❌, Egito-Argentina ✅. Quebra a sequência histórica de 97% de acerto acima de 70% vinda da fase de grupos e do R32 — primeiro furo grande do modelo nessa faixa de confiança.
- **Faixa 50–70%: 3/4 (75%)** — México-Inglaterra ✅, Bélgica-EUA ✅, Espanha-Portugal ✅, Suíça-Colômbia ❌ (o jogo mais parelho do lote, o próprio modelo já sinalizava como moeda ao ar)
- **Aposta derivada (métrica): 4/6 (66,7%)** — 2 jogos sem pick claro (Canadá-Marrocos, Bélgica-EUA). Acertou clean sheet e os dois "under" claros (Espanha-Portugal, Suíça-Colômbia); errou o under de México-Inglaterra e o "not BTTS" de Egito-Argentina
- **Placar exato no Top-3: 3/8 (37,5%)** — acertou nos dois jogos mais fechados (Paraguai-França e Espanha-Portugal, 2º lugar do ranking) e cravou o 0–0 de Suíça-Colômbia como placar Nº1; errou feio nos jogos de "goleada"

## Padrão editorial

As oitavas tiveram mais jogos de placar alto do que o modelo esperava — 3 dos 8 jogos terminaram com 5 gols no total (Bélgica-EUA 4–1, México-Inglaterra 2–3, Egito-Argentina 2–3), todos subestimados pelas apostas de Under/BTTS. Pressão de eliminação parece ter deixado os jogos mais abertos do que a fase de grupos sugeria — hipótese a acompanhar nas quartas.

A zebra do Brasil (84.3% de confiança, perdeu) é o ponto de atenção mais forte: primeira quebra real da calibração de alta confiança do Model5. Vale investigar no relatório de calibração da próxima rodada se foi acaso pontual ou sinal de que os biases por seleção precisam de ajuste (Brasil pode estar superestimado pós-recalibração do R32).

## TODO

- Registrar jogos 95 (Suíça 0–0 Colômbia, PEN) e 96 (Egito 2–3 Argentina) no `output/copa_real_state.json` via `resultado.py`
- Rodar `model_eval.py` para métricas formais (Brier, NLL) incluindo os 8 jogos das oitavas
- Avaliar se a zebra do Brasil justifica uma nova rodada de calibração (`calibrate_sa.py --biases`) antes das quartas
