# TASKS — Estado e Próximos Passos

*Atualizado: 18 jul 2026 — Semifinais encerradas (2/2), Model7 recalibrado (102 jogos, bônus SF/Final), prorrogação modelada explicitamente, odds do 3º lugar e Final geradas*

---

## Estado Atual: Semifinais encerradas → 3º Lugar + Final

- **2/2 jogos das semis** registrados em `copa_real_state.json` (`knockout_results` #101–102): **França 0–2 Espanha** (90'), **Inglaterra 1–2 Argentina** (90', virada) ✅
- **Correção de entrada (18 jul 2026):** o placar de Inglaterra x Argentina foi digitado errado na primeira vez (2–1 Inglaterra, por má interpretação da mensagem do usuário) — corrigido pra 1–2 Argentina antes de qualquer cálculo posterior. Nenhum output tinha sido gerado com o placar errado.
- **Final confirmada: Espanha x Argentina** · **3º lugar: França x Inglaterra**
- **Model6 avaliado out-of-sample nas semis** (pesos de antes desta recalibração) — quem avança 2/2 (100%, mas nenhum jogo bateu 70% de confiança: Espanha 60.5%, Inglaterra 66.3%). Placar exato: Inglaterra x Argentina 2–1 (a virada) foi o top-1 do modelo; França x Espanha 0–2 ficou em 4º/5º lugar (9.0%, empatado com 1–2).
- **Pedido do usuário (18 jul 2026): última recalibração antes da final** — 3 partes: (1) bônus de peso pra SF/Final, (2) modelar prorrogação em vez de pênaltis 50/50 direto, já que a Argentina marcou gols na prorrogação 2x, (3) manter pênaltis como 50/50 quando não há mais o que modelar
- **`ROUND_WEIGHTS` atualizado:** `sf: 1.0→1.5`, `final: 1.0→2.0` (resto sem mudança) — ver "Calibração por Pontos" no `CLAUDE.md`
- **Prorrogação modelada:** `simulate.py::sim_knockout_match` e `match_odds.py::extra_time_breakdown` — xG escalado a 1/3 (30min ≈ 1/3 de 90min) pra quem empata nos 90', pênaltis 50/50 só se continuar empatado depois disso
- **Validação da prorrogação:** contra os 8 empates reais do mata-mata até as semis — 8.72 gols esperados vs 7 observados (bem alinhado). A Argentina marcou nas 2 vezes em que foi à prorrogação (Cabo Verde, Suíça), acima do esperado — não virou bias específico (n=2), mas é dado editorial válido
- **Correção de regra descoberta durante a implementação:** disputa de 3º lugar **não tem prorrogação** (regra FIFA — só a Final tem). `match_odds.py` ganhou a flag `--terceiro-lugar`/`--no-extra-time` pra isso. As odds da França x Inglaterra foram geradas primeiro com prorrogação por engano (`--knockout` sozinho) e depois corrigidas.
- **Model7 recalibrado** — 5 seeds em paralelo (999, 2026, 7, 123, 42), mesma config do Model6 (`--biases --lambda 2.0`, 300k iters × 5 restarts), agora com 102 jogos e os novos pesos de rodada. **Seed 123 venceu em pontos** (77.14/91=84.8%) mas não em NLL/Brier — trade-off como no Model5 (seed 999 melhor Brier, seed 2026 melhor NLL). Decidido por pontos (critério oficial). Logs em `output/model7_seeds/`.
- **Odds geradas com Model7:**
  - 3º lugar (sem prorrogação): **França 70.9% x Inglaterra 29.1%** — `output/odds_france_vs_england.json`
  - Final (com prorrogação): **Espanha 86.5% x Argentina 13.5%** — `output/odds_spain_vs_argentina.json`
- **Pendente:** gerar posts Instagram do 3º lugar e da Final (estilo "Troféu Chegando"), depois publicar. Depois da Final, decidir se vale uma última avaliação out-of-sample do Model7 (só 2 jogos — provavelmente pouco significativo, mas documentar por completude do projeto).

---

## Estado Anterior: Quartas encerradas → Semifinais (histórico, 14 jul 2026)

- **4/4 jogos das quartas** registrados em `copa_real_state.json` (`knockout_results` #97–100): França 2–0 Marrocos, Espanha 2–1 Bélgica, Inglaterra 2–1 Noruega (AET, 1–1 nos 90'), Argentina 3–1 Suíça (AET, 1–1 nos 90') ✅
- **Model6 avaliado out-of-sample nas quartas** (primeiro teste real de generalização) — quem avança 3/4 (75%), confiança ≥70% 1/1 (100%), placar exato top-3 2/4 (50%), aposta derivada 2/4 (50%). Único erro: Argentina x Suíça (51.0% x 49.0%, o azarão venceu, mas o placar 1-1 nos 90' era o top-1 do modelo)
- **Decisão do usuário: NÃO recalibrar após as quartas** — só 4 jogos novos sobre 96 de treino, pouco pra mover o SA; o ponto de congelar o Model6 era ter um teste out-of-sample de verdade, recalibrar a cada rodada mataria isso. Só restam SF+Final.
- **Bug encontrado e corrigido (14 jul 2026):** ver seção "Bug do bracket da semifinal" abaixo
- **Bracket da semifinal confirmado:** SF1 = França x Espanha, SF2 = Inglaterra x Argentina
- **Odds das 2 semifinais geradas com Model6** ✅ — `output/odds_france_vs_spain.json`, `output/odds_england_vs_argentina.json`
- **Simulação 10M pós-quartas** ✅ — Espanha 41.4% campeã, Inglaterra 27.4%, França 22.7%, Argentina 8.5% (`output/simulation_results_model6.json`) — não precisou re-rodar após o fix do bug porque `simulate.py` já estava certo, só `resultado.py` (usado pra exibição/entrada) estava errado
- **Post das semifinais pronto** ✅ — `sf_post.md`, mesmo estilo "Troféu Chegando"

### Bug do bracket da semifinal — CORRIGIDO (14 jul 2026)

`resultado.py::KNOCKOUT_SCHEDULE` tinha os pares 101/102 errados:
```
101: ("Semifinal", "W97", "W98"),   # errado — França x Inglaterra
102: ("Semifinal", "W99", "W100"),  # errado — Espanha x Argentina
```
Isso não batia com `simulate.py::SEMIFINALS = [(101, 97, 99), (102, 98, 100)]`, que já estava correto desde o fix de 04 jul 2026 (ver "Bug do bracket em simulate.py" abaixo — "SF1=QF1×QF2 (metade A), SF2=QF3×QF4 (metade B)"). QF1=match97 (França x Marrocos), QF2=match99 (Espanha x Bélgica) → SF1 real = W97×W99 = **França x Espanha**. QF3=match98 (Noruega x Inglaterra), QF4=match100 (Argentina x Suíça) → SF2 real = W98×W100 = **Inglaterra x Argentina**.

Corrigido em `resultado.py` para `101: (W97, W99)`, `102: (W98, W100)`. `simulate.py` não precisou de mudança — a simulação de 10M já estava certa o tempo todo, só a exibição/entrada de resultados via `resultado.py --list sf` mostrava o pareamento errado. **Lição:** sempre conferir `resultado.py::KNOCKOUT_SCHEDULE` contra `simulate.py::QUARTERFINALS`/`SEMIFINALS` antes de confiar no bracket exibido — o mesmo tipo de dessincronização já tinha acontecido no R16.

---

## Estado Anterior: Oitavas encerradas → Quartas (histórico, 08 jul 2026)

- **8/8 jogos das oitavas** registrados em `copa_real_state.json` (`knockout_results` #89–96) ✅
- **Análise "quem avança" das oitavas** (com Model5, in-sample) salva em `output/r16_wdl_report.md` ✅ — 6/8 (75%), zebra do Brasil (84.3% de confiança, perdeu pra Noruega) quebrou a sequência de 97% acima de 70% de confiança
- **Nova metodologia de calibração: objetivo por pontos** ✅ — ver seção abaixo. `calibrate_sa.py` agora maximiza pontos em vez de minimizar NLL
- **Model6 ativo** — treinado com 96 jogos (72 grupo + 16 R32 + 8 R16), objetivo por pontos, seed 42 (venceu em todas as métricas: pontos 68.0/78=87.2%, NLL 80.39, Brier 0.494) — ver `CLAUDE.md` → Estado Atual e "Calibração por Pontos"
- **A partir de agora o modelo fica congelado** — quartas, semi, 3º lugar e final usam Model6 sem retreinar. Primeira vez no projeto que a performance reportada será genuinamente *out-of-sample* (todos os modelos anteriores foram avaliados nos mesmos jogos em que treinaram)
- **Bracket das quartas em diante CONFIRMADO** (08 jul 2026) ✅ — ver tabela abaixo
- **Odds das 4 quartas geradas com Model6** ✅ — `output/odds_france_vs_morocco.json`, `output/odds_spain_vs_belgium.json`, `output/odds_norway_vs_england.json`, `output/odds_argentina_vs_switzerland.json`
- **Achado:** Argentina x Suíça está praticamente 50/50 (37,2% x 39,0%, leve favoritismo suíço) — bias da Argentina caiu bastante e o da Suíça subiu desde que ela avançou nos pênaltis contra a Colômbia

### Bracket confirmado — Quartas em diante

| Fase | Confronto |
|------|-----------|
| QF1 | França x Marrocos |
| QF2 | Espanha x Bélgica |
| QF3 | Noruega x Inglaterra |
| QF4 | Argentina x Suíça |
| SF1 | vencedor QF1 x vencedor QF2 |
| SF2 | vencedor QF3 x vencedor QF4 |
| Final | vencedor SF1 x vencedor SF2 |

### Resultados das oitavas (R16)

| Jogo | Placar | Vencedor |
|------|--------|----------|
| Canadá x Marrocos | 0–3 | Marrocos |
| Paraguai x França | 0–1 | França |
| Bélgica x EUA | 4–1 | Bélgica |
| Espanha x Portugal | 1–0 | Espanha |
| Brasil x Noruega | 1–2 | Noruega (zebra) |
| México x Inglaterra | 2–3 | Inglaterra |
| Suíça x Colômbia | 0–0 (pênaltis) | Suíça |
| Egito x Argentina | 2–3 | Argentina |

---

## Calibração por Pontos — decisão do usuário (08 jul 2026)

Motivação: em vez de continuar recalibrando NLL a cada rodada (métrica estatística, não o que o projeto realmente quer maximizar), o usuário pediu pra trocar o objetivo do `calibrate_sa.py` por uma pontuação desenhada por ele — acerto de resultado × peso da rodada + bônus de placar exato no mata-mata. Detalhe completo da fórmula e da tabela de pesos por rodada está no `CLAUDE.md` (seção "Calibração por Pontos (Model6)").

### O que mudou no código (`scripts/calibrate_sa.py`)

- `ROUND_WEIGHTS` trocado: r1=r2=0.5, r3=0.25, r32=r16=qf=sf=final=1.0 (SF/Final ainda não jogados, assumido igual ao resto do mata-mata — **revisar se o usuário quiser diferenciar antes do próximo retreino**)
- `ALIVE_BONUS`/`ALIVE_TEAMS`/`_alive_bonus()` removidos por completo (não fazia parte do novo esquema)
- Novas funções: `_pmf` (Poisson pmf sem overhead do scipy, pro loop quente do SA), `_outcome_probs` (win/draw/loss via soma cumulativa O(n)), `_score_bonus` (rank do placar real na grade de probabilidades), `points_score`, `max_possible_points`, `neg_points_loss` (objetivo minimizado pelo SA: `-pontos + λ×regularização`)
- `load_data()` agora também guarda `winner_side` nos jogos de mata-mata (de onde vem o "quem avança" real, incluindo pênaltis) — antes só existia `outcome` baseado no placar de 90'
- Loop do SA e prints trocaram `poisson_nll` por `neg_points_loss`; `poisson_nll`/`evaluate()` continuam existindo só pro diagnóstico final (NLL/Brier reportados por continuidade histórica)
- JSON de saída ganhou `objective`, `top_score_bonus`, `max_points`, `points_default`, `points_sa`, `points_lbfgs`; perdeu `alive_bonus`/`alive_teams`

### Como o Model6 foi treinado

Mesma metodologia de seleção por seeds do Model5: 5 seeds (999, 2026, 7, 123, 42) rodadas em paralelo, mesma config (`--biases --lambda 2.0`, default 300k iters × 5 restarts). Rodou em `output/model6_seeds/`, ~40min por seed (mais lento que uma seed isolada por causa da concorrência de 5 processos em 12 cores). Seed 42 venceu em pontos, NLL e Brier ao mesmo tempo — sem empate, ao contrário da seleção do Model5.

Promovido pra `output/calibrated_weights_sa.json` (ativo) e `output/weights_model6.json` (referência).

**Antes de registrar os resultados das quartas e recalibrar de novo:** confirmar com o usuário os pesos de SF/Final (assumidos 1.0 por enquanto) e se o objetivo por pontos continua ou volta pra NLL.

---

## Bug do bracket em `simulate.py` — CORRIGIDO (04 jul 2026, histórico)

Três problemas encontrados e corrigidos, nessa ordem:

1. **`ROUND16` embaralhado** — pares 1, 2, 3, 7 e 8 não seguiam a ordem sequencial oficial (73&74, 75&76, 77&78, 79&80, 81&82, 83&84, 85&86, 87&88).
2. **`SEMIFINALS` cruzando metades cedo demais** — Brasil (metade B: jogos 81–88) encontrava o lado da França (metade A: 73–80) já na semifinal em vez de só na final. Corrigido: SF1=QF1×QF2 (metade A), SF2=QF3×QF4 (metade B).
3. **`ROUND32` (specs de grupo, ex: "1º E vs 3º ABCDF") dessincronizado dos resultados reais em 15 dos 16 jogos** — a simulação não reconhecia o resultado real e resimulava do zero, deixando times já eliminados (Holanda, Alemanha, Japão) reaparecerem nas odds de campeão. **Fix definitivo:** `simulate_tournament()` não simula mais fase de grupos nem resolve o R32 por specs — usa `REAL_R16_BRACKET`, um dicionário fixo com os 16 times reais das oitavas. Fase de grupos e R32 são fato consumado, não precisam mais ser simulados.

**Atenção:** `megazord.py` ainda usa a lógica antiga (`ROUND32` + specs de grupo) e não foi corrigido — mantém o mesmo bug se for rodado agora. `ROUND16` foi mantido no código (não removido) só por compatibilidade com esse import. **Atualização pendente:** `simulate.py` também vai precisar de um bracket fixo pras quartas em diante (`REAL_QF_BRACKET` ou similar), já que agora as oitavas também são fato consumado.

Validado: Monte Carlo de 10M pós-fix bate com o cálculo exato via recursão de bracket (França 26.70% vs 26.72%, Brasil 20.19% vs 20.16%) — ver `output/oitavas_bracket_probabilidades.md`.

---

## Performance R32 (Model4 S14, histórico)

| Métrica | Resultado |
|---------|-----------|
| W/D/L nos 90' | 10/16 (62.5%) |
| Quem avança (correto) | 12/16 (75%) |
| Empates reais (90') | 5/16 (31%) — modelo nunca previu empate como #1 |
| Confiança ≥70% (W/D/L 90') | 3/5 (60%) — bem abaixo dos 97% da fase de grupos |
| Confiança ≥70% (quem avança) | 7/8 (87.5%) — muito mais próximo do histórico |
| Dark horse do round | Paraguai sobre Alemanha (76.7% de favoritismo revertido nos pênaltis) |

Detalhe completo em `output/r32_wdl_report.md`.

---

## Performance Oitavas (Model5, in-sample)

| Métrica | Resultado |
|---------|-----------|
| Quem avança (correto) | 6/8 (75%) |
| Confiança ≥70% | 3/4 (75%) — zebra do Brasil quebra a sequência histórica de 97% |
| Confiança 50–70% | 3/4 (75%) |
| Aposta derivada (métrica) acertada | 4/6 (66,7%) — 2 jogos sem pick claro |
| Placar exato no Top-3 | 3/8 (37,5%) |

Padrão notado: 3 dos 8 jogos terminaram com 5+ gols no total (Bélgica-EUA, México-Inglaterra, Egito-Argentina) — mais goleadas do que o modelo esperava. Isso motivou parte do salto de `BASE_XG` no Model6 (1.01 → 1.38). Detalhe completo em `output/r16_wdl_report.md`.

---

## Decisão de metodologia — Mata-mata (04 jul 2026, ainda válida)

Como o modelo nunca prevê empate (limitação estrutural do Poisson independente) e placares exatos de baixo score carregam pouca informação, jogos de mata-mata usam "quem avança" em vez de W/D/L — ver `CLAUDE.md` seção "Metodologia de Mata-Mata" pra fórmula e métricas derivadas (over/under, BTTS, clean sheet, vitória por margem). Continua em vigor sem mudanças.

---

## Bugs conhecidos — CORRIGIDOS (histórico)

- `scripts/calibrate_sa.py::_parse_score` quebrava em `score_str` com sufixo `PEN`/`AET` — corrigido pra sempre extrair o placar de 90' (`note='AET'` lê o placar entre parênteses). (04 jul 2026)

---

## Próximos Passos

### 1. Confirmar confrontos das quartas ✅
Bracket confirmado pelo usuário (08 jul 2026) — ver tabela em "Estado Atual" acima.

### 2. Bracket fixo em `simulate.py` pras quartas ✅ (nenhuma mudança necessária)
Testado em 08 jul 2026: `play()` já checa `_REAL_KNOCKOUT_RESULTS` genericamente pra qualquer `match_id`, não só R16 — como os 8 resultados das oitavas já estão em `copa_real_state.json`, o QF já é montado com os vencedores reais automaticamente, sem re-simular. Confirmado rodando 200k simulações: os 8 times vivos saem com 100% em QF/R16 e os 88 eliminados com 0% em tudo. Campeão: Espanha 35.4%, Inglaterra 19.8%, França 16.9%, Suíça 7.1%, Marrocos 5.8%, Argentina 5.6%, Bélgica 5.1%, Noruega 4.4%.

### 3. Gerar odds das quartas com Model6 ✅

```bash
python3 scripts/match_odds.py france morocco 1000000 --knockout
python3 scripts/match_odds.py spain belgium 1000000 --knockout
python3 scripts/match_odds.py norway england 1000000 --knockout
python3 scripts/match_odds.py argentina switzerland 1000000 --knockout
```

Nota: rodado primeiro sem `--knockout` (odds ficaram certas, mas sem o campo `advance`/exibição "quem avança") e depois refeito com a flag — usar sempre `--knockout` no mata-mata daqui pra frente.

### 3b. Probabilidade de campeão — Model6, 10M simulações ✅

```bash
python3 scripts/simulate.py 10000000 output/simulation_results_model6.json
```

Resultado (só os 8 times vivos têm chance >0%): Espanha 35.3%, Inglaterra 19.8%, França 17.0%, Suíça 7.2%, Marrocos 5.8%, Argentina 5.6%, Bélgica 5.2%, Noruega 4.3%.

### 4. Post Instagram quartas ✅

Novo estilo "Troféu Chegando" (aprovado pelo usuário 08 jul 2026) — ver `qf_post.md` e seção "Identidade visual" no `CLAUDE.md`.

- [x] Hook (4 confrontos + linha "path to the final")
- [x] Slide técnico (performance oitavas com Model5: 75% quem avança, zebra do Brasil)
- [x] Slide de probabilidade de campeão (ranking dos 8 times, Model6)
- [x] Slides "O que o modelo aprendeu" (2b + 2c) — cobrem os 8 times vivos, agrupados pelo lado do chaveamento, cada um com att/def bias + 1 linha de comentário citando resultado real (ex: Argentina def=0.55 → empate com Cabo Verde + 2 gols do Egito; Espanha att/def=1.14/1.16 → 0 gols sofridos em 5 jogos)
- [x] Slides por jogo (4) — novo template dourado/serifado

### 5. Após quartas: entrada de resultados + decisão sobre retreino ⬜

```bash
python3 scripts/resultado.py  # entrar 4 resultados (IDs 97–100)
```

Model6 está congelado por design — antes de recalibrar de novo, confirmar com o usuário se quer manter o objetivo por pontos e os pesos de SF/Final assumidos (1.0).

---

## Notas técnicas antigas (referência)

### Times com bias extremo (att_only, Model3 → referência histórica, pré-Model6)
- Altos (≥1.35): Japan 1.44, Canada 1.39, Germany 1.37, Netherlands 1.35
- Baixos (≤0.31): Ecuador 0.20, Turkey 0.20, Belgium 0.27, Panama 0.31

### Dixon-Coles (ainda não testado)
Candidato para melhorar predição de empates de verdade (não só reclassificar via "quem avança") — testar como estratégia S22 no `model_compare.py` quando sobrar tempo entre rodadas.
