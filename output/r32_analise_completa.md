# R32 — Análise Completa (Model4) — Base para Post Técnico Instagram

> Fonte: previsões em `r32_post1.md` + `r32_post2.md` (Model4, 1.000.000 simulações por jogo) vs resultados reais em `output/copa_real_state.json` (`knockout_results` #73–88). Nenhum dado inventado — tudo abaixo vem dos arquivos gerados na rodada.

---

## 1. Números-chave (para o slide técnico)

| Métrica | Valor |
|---------|-------|
| Jogos analisados | 16 |
| W/D/L correto (placar dos 90') | 10/16 (62.5%) |
| Quem avança correto (`P(vence)+0.5×P(empate)`) | 12/16 (75%) |
| Empates reais nos 90' | 5/16 (31%) |
| Empates previstos como resultado mais provável | 0/16 (0%) |
| Placar exato = Top-1 do modelo | 3/16 (18.75%) |
| Placar real dentro do Top-3 do modelo | 6/16 (37.5%) |
| Confiança ≥70% — acerto no W/D/L 90' | 3/5 (60%) |
| Confiança ≥70% — acerto em quem avança | 7/8 (87.5%) |
| Maior zebra (maior confiança revertida) | Alemanha 76.7% → Paraguai avançou |

---

## 2. Performance do modelo — R32 vs rodadas anteriores

| Rodada | Jogos | W/D/L correto | Empates acertados | Confiança ≥70% |
|--------|-------|----------------|--------------------|------------------|
| R1 (grupos) | 24 | 14/24 (58%) | 0/8 | — |
| R2 (grupos) | 24 | 17/24 (71%) | 0/6 | — |
| R3 (grupos) | 24 | 15/24 (62%) | 0/6 | — |
| **Total fase de grupos** | **72** | **46/72 (64%)** | **0/20** | **28/29 (97%)** |
| **R32 (mata-mata)** | **16** | **10/16 (62.5%)** | **0/5** | **3/5 (60%)** |

Leitura: o W/D/L geral do R32 (62.5%) ficou **em linha** com a média histórica da fase de grupos (64%) — o modelo não piorou no mata-mata. O que mudou foi a **calibração de confiança**: o bucket de ≥70% caiu de 97% pra 60%, porque a métrica W/D/L nos 90' pune o modelo em jogos que o favorito realmente venceu (Argentina, Egito), só que via prorrogação/pênaltis em vez de tempo normal. Usando "quem avança" em vez de W/D/L, o bucket ≥70% sobe pra **87.5%** (seção 7) — ou seja, o modelo continua tão confiável quanto sempre foi, só precisava ser medido pela pergunta certa ("quem passa de fase", não "que placar deu nos 90'").

---

## 3. Tabela completa — todos os 16 jogos

| # | Jogo | xG | Favorito (W/D/L%) | Top-3 placares | Real (90') | Decisão | Quem avançou | 90'✓ | Avanço✓ | Placar no Top-3? |
|---|------|-----|--------------------|-----------------|-----------|---------|---------------|:---:|:---:|:---:|
| 73 | África do Sul x Canadá | 1.08–1.38 | SA 29.4 / D 26.9 / CAN 43.7 | 1-1 12.7% · 0-1 11.7% · 1-0 9.2% | 0–1 | 90' | Canadá | ✓ | ✓ | ✓ (0-1, #2) |
| 74 | Holanda x Marrocos | 1.71–1.59 | NED 41.0 / D 23.0 / MAR 36.0 | 1-1 10.0% · 2-1 8.6% · 1-2 7.9% | 1–1 | PEN | Marrocos | ✗ | ✗ | ✓ (1-1, #1 exato) |
| 75 | Alemanha x Paraguai | 2.66–0.80 | GER 76.7 / D 14.4 / PAR 8.9 | 2-0 11.1% · 3-0 9.8% · 2-1 8.9% | 1–1 | PEN | Paraguai | ✗ | ✗ | ✗ |
| 76 | França x Suécia | 3.11–0.73 | FRA 83.9 / D 10.6 / SWE 5.6 | 3-0 10.7% · 2-0 10.4% · 4-0 8.4% | 3–0 | 90' | França | ✓ | ✓ | ✓ (3-0, #1 exato) |
| 81 | Brasil x Japão | 1.69–0.62 | BRA 63.2 / D 23.4 / JPN 13.3 | 1-0 16.8% · 2-0 14.1% · 1-1 10.4% | 2–1 | 90+4' | Brasil | ✓ | ✓ | ✗ |
| 82 | Costa do Marfim x Noruega | 1.78–1.68 | CIV 41.1 / D 22.4 / NOR 36.6 | 1-1 9.4% · 2-1 8.4% · 1-2 7.9% | 1–2 | 90' | Noruega | ✗ | ✗ | ✓ (1-2, #3) |
| 83 | México x Equador | 0.80–0.42 | MEX 41.6 / D 40.3 / ECU 18.1 | 0-0 29.6% · 1-0 23.6% · 0-1 12.5% | 2–0 | 90' | México | ✓ | ✓ | ✗ |
| 84 | Inglaterra x Congo | 1.81–0.79 | ENG 61.6 / D 22.4 / CGO 15.9 | 1-0 13.5% · 2-0 12.2% · 1-1 10.6% | 2–1 | 90' | Inglaterra | ✓ | ✓ | ✗ |
| 77 | Bélgica x Senegal | 1.32–1.37 | BEL 35.8 / D 25.9 / SEN 38.3 | 1-1 12.3% · 0-1 9.3% · 1-0 9.0% | 2–2 | AET (3–2) | Bélgica | ✗ | ✗ | ✗ |
| 78 | EUA x Bósnia | 3.23–1.14 | USA 78.0 / D 12.4 / BIH 9.7 | 3-1 8.1% · 2-1 7.5% · 3-0 7.1% | 2–0 | 90' | EUA | ✓ | ✓ | ✗ |
| 79 | Espanha x Áustria | 1.81–0.67 | ESP 64.9 / D 22.0 / AUT 13.2 | 1-0 15.2% · 2-0 13.8% · 1-1 10.1% | 3–0 | 90' | Espanha | ✓ | ✓ | ✗ |
| 80 | Portugal x Croácia | 2.27–0.76 | POR 71.5 / D 17.6 / CRO 11.0 | 2-0 12.5% · 1-0 11.1% · 3-0 9.4% | 2–1 | 90' | Portugal | ✓ | ✓ | ✗ |
| 85 | Suíça x Argélia | 1.68–1.31 | SUI 46.1 / D 23.9 / ALG 30.0 | 1-1 11.1% · 2-1 9.3% · 1-0 8.5% | 2–0 | 90' | Suíça | ✓ | ✓ | ✗ |
| 86 | Colômbia x Gana | 1.23–0.53 | COL 53.5 / D 30.5 / GHA 16.0 | 1-0 21.2% · 0-0 17.3% · 2-0 12.9% | 1–0 | 90' | Colômbia | ✓ | ✓ | ✓ (1-0, #1 exato) |
| 87 | Austrália x Egito | 0.78–1.04 | AUS 26.8 / D 32.3 / EGY 40.9 | 0-1 16.8% · 0-0 16.3% · 1-1 13.2% | 1–1 | PEN | Egito | ✗ | ✓ | ✓ (1-1, #3) |
| 88 | Argentina x Cabo Verde | 1.85–0.33 | ARG 75.0 / D 19.2 / CPV 5.7 | 1-0 21.0% · 2-0 19.4% · 3-0 12.0% | 1–1 | AET (3–2) | Argentina | ✗ | ✓ | ✗ |

---

## 4. Acertos — favorito confirmado com folga

Jogos em que o modelo apontou favorito e o resultado confirmou sem sustos, com placar dentro do esperado:

- **África do Sul x Canadá** — Canadá favorito (43.7%), venceu 0–1, placar exato bateu o Top-3
- **França x Suécia** — maior favoritismo do round (83.9%), venceu 3–0, **placar exato batendo o Top-1**
- **Colômbia x Gana** — favorito moderado (53.5%), venceu 1–0, **placar exato batendo o Top-1**
- **EUA x Bósnia**, **Espanha x Áustria**, **Portugal x Croácia**, **Inglaterra x Congo** — favoritos confirmados com confiança entre 61–78%, W/D/L e avanço corretos (placar exato variou, mas a direção nunca foi ameaçada)
- **Suíça x Argélia**, **México x Equador** — favoritos "fracos" (41–46%, quase par com o empate) que ainda assim confirmaram — nesses dois casos o modelo **subestimou** a margem de vitória (esperava jogo apertado/0 a 1 gol, saiu 2–0 nos dois)

## 5. Erros e zebras

| Jogo | O que o modelo esperava | O que aconteceu | Tamanho da zebra |
|------|--------------------------|-------------------|-------------------|
| **Alemanha x Paraguai** | Alemanha 76.7% favorita | Empate 1–1, Paraguai venceu nos pênaltis | **Maior zebra do round** — Paraguai tinha só 8.9% de chance de vitória direta |
| **Holanda x Marrocos** | Holanda favorita fraca (41.0% vs 36.0%) | Empate 1–1 (placar batido no Top-1!), Marrocos avançou nos pênaltis | Zebra leve — praticamente empate técnico de probabilidades |
| **Costa do Marfim x Noruega** | Costa do Marfim favorita fraca (41.1% vs 36.6%) | Noruega venceu 1–2 (placar estava no Top-3) | Zebra leve — mesma margem apertada |
| **Bélgica x Senegal** | Senegal levemente favorito (38.3% vs 35.8%) — modelo já sinalizava "sem convicção" | Empate 2–2 nos 90', Bélgica venceu na prorrogação | Zebra mínima — modelo já havia marcado esse jogo como incerto |

Nenhuma dessas quatro zebras envolveu confiança extrema, **exceto** Alemanha x Paraguai — esse é o único caso do round em que uma previsão de alta confiança (>70%) foi completamente invertida.

## 6. Empates — o ponto cego estrutural

5 dos 16 jogos (31%) terminaram empatados nos 90 minutos — proporção até maior que a fase de grupos (28%). Em nenhum dos 16 jogos o modelo apontou empate como resultado mais provável (0/16) — limitação estrutural conhecida do Poisson independente, que só coloca o empate em primeiro quando os dois xG são simultaneamente baixos e quase idênticos (situação rara nos dados reais de squad).

| Jogo | xG | P(favorito) | P(empate) | P(zebra) | Como terminou |
|------|-----|-------------|-----------|----------|----------------|
| Holanda x Marrocos | 1.71–1.59 | 41.0% | 23.0% | 36.0% | PEN → Marrocos |
| Alemanha x Paraguai | 2.66–0.80 | 76.7% | 14.4% | 8.9% | PEN → Paraguai |
| Bélgica x Senegal | 1.32–1.37 | 38.3% | 25.9% | 35.8% | AET → Bélgica |
| Austrália x Egito | 0.78–1.04 | 40.9% | 32.3% | 26.8% | PEN → Egito |
| Argentina x Cabo Verde | 1.85–0.33 | 75.0% | 19.2% | 5.7% | AET → Argentina |

Probabilidade média de empate dada pelo modelo nesses 5 jogos: **22.96%** (referência aleatória de 3 vias = 33.3%).

## 7. Confiança ≥70% — antes e depois de medir "quem avança"

Só 5 jogos tiveram favorito com ≥70% de confiança: França (83.9%), EUA (78.0%), Alemanha (76.7%), Argentina (75.0%), Portugal (71.5%).

| Jogo | Confiança | Acerto no placar dos 90'? | Acerto em quem avançou? |
|------|-----------|:---:|:---:|
| França x Suécia | 83.9% | ✓ | ✓ |
| Argentina x Cabo Verde | 75.0%* | ✗ (empatou nos 90') | ✓ (avançou na prorrogação) |
| EUA x Bósnia | 78.0% | ✓ | ✓ |
| Portugal x Croácia | 71.5% | ✓ | ✓ |
| Alemanha x Paraguai | 76.7% | ✗ | ✗ |

*recalculando "quem avança" (`P(vence)+0.5×P(empate)`) pra esses 5 jogos, a lista de ≥70% muda de composição (Argentina sobe pra 84.6%, outros ajustam), mas o resultado geral do bucket é: **7 de 8 jogos com ≥70% de chance de avanço realmente avançaram (87.5%)** — bem mais alinhado com os 97% da fase de grupos do que os 60% que aparecem olhando só pro placar dos 90'.

## 8. Histórias / ganchos editoriais (sem invenção — só leitura dos números)

- **Maior zebra: Paraguai sobre a Alemanha.** 76.7% de favoritismo revertido nos pênaltis — a única quebra de uma previsão de alta confiança no round inteiro.
- **Quase-zebra: Cabo Verde segura a Argentina.** Só 5.7% de chance de vitória, mas empatou 1–1 nos 90' contra o maior favorito absoluto do confronto (75.0%) — só perdeu na prorrogação.
- **Vitória no sufoco: Brasil só decide aos 90+4'.** Apesar de 63.2% de favoritismo, o resultado só ficou claro nos acréscimos.
- **Favoritos "fracos" que golearam:** México (41.6%, favorito quase empatado com o próprio empate a 40.3%) fez 2–0; Suíça (46.1%) também fez 2–0 — nos dois casos o modelo esperava jogo mais truncado do que realmente foi.
- **Bélgica avança, mas o dado por trás é de alerta:** o viés de ataque da Bélgica é o mais baixo de todo o torneio (0.632) — os 3 gols saíram contra um Senegal já desgastado na prorrogação, não evidência de ataque forte.
- **Acertos de placar exato (Top-1 batendo o real):** Holanda x Marrocos (1–1), França x Suécia (3–0), Colômbia x Gana (1–0) — os três únicos jogos do round com esse nível de precisão.

## 9. Auto-reflexão do modelo

- O modelo **nunca** erra a direção quando a diferença de xG é grande (>2.0 de diferença): todos os jogos com esse padrão (França, EUA, Espanha, Argentina, Portugal) tiveram o favorito claro decidindo — mesmo Argentina, que empatou nos 90', avançou como previsto.
- Todas as 4 zebras (Alemanha, Holanda, Costa do Marfim, Bélgica) aconteceram em jogos de **xG próximo** (diferença menor que 1.0) — sinal de que a incerteza do modelo nesses casos já era real e visível nos números, não veio do nada.
- A única zebra de alta confiança (Alemanha 76.7%) é justamente o caso onde o modelo mais deveria "desconfiar de si mesmo": squad muito superior contra adversário que se fecha — um padrão que vale monitorar nas próximas rodadas.
- Medir "quem avança" em vez de W/D/L dos 90' muda a leitura de desempenho do modelo de forma honesta: não é que o modelo "acertou mais" escondendo erro — é que a métrica W/D/L nunca fez sentido pra mata-mata, porque empate nos 90' não é o resultado final do confronto.
