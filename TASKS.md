# TASKS — Estado e Próximos Passos

*Atualizado: 08 jul 2026 — Oitavas encerradas (8/8), Model6 treinado com novo objetivo por pontos, modelo congelado pras quartas em diante*

---

## Estado Atual: Oitavas encerradas → Quartas

- **8/8 jogos das oitavas** registrados em `copa_real_state.json` (`knockout_results` #89–96) ✅
- **Análise "quem avança" das oitavas** (com Model5, in-sample) salva em `output/r16_wdl_report.md` ✅ — 6/8 (75%), zebra do Brasil (84.3% de confiança, perdeu pra Noruega) quebrou a sequência de 97% acima de 70% de confiança
- **Nova metodologia de calibração: objetivo por pontos** ✅ — ver seção abaixo. `calibrate_sa.py` agora maximiza pontos em vez de minimizar NLL
- **Model6 ativo** — treinado com 96 jogos (72 grupo + 16 R32 + 8 R16), objetivo por pontos, seed 42 (venceu em todas as métricas: pontos 68.0/78=87.2%, NLL 80.39, Brier 0.494) — ver `CLAUDE.md` → Estado Atual e "Calibração por Pontos"
- **A partir de agora o modelo fica congelado** — quartas, semi, 3º lugar e final usam Model6 sem retreinar. Primeira vez no projeto que a performance reportada será genuinamente *out-of-sample* (todos os modelos anteriores foram avaliados nos mesmos jogos em que treinaram)
- Odds das quartas (`match_odds.py` por jogo) ⬜ pendente — falta saber os 4 confrontos (dependem de quem passou nas oitavas, já sabemos os 8 times: Marrocos, França, Bélgica, Espanha, Noruega, Inglaterra, Suíça, Argentina)

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

### 1. Confirmar confrontos das quartas ⬜
Times classificados: Marrocos, França, Bélgica, Espanha, Noruega, Inglaterra, Suíça, Argentina. Falta saber o chaveamento oficial — confirmar contra a fonte oficial da FIFA, não assumir.

### 2. Atualizar bracket fixo em `simulate.py` pras quartas ⬜
Mesmo fix do R32→oitavas, agora precisa incorporar os resultados reais das oitavas (não re-simular).

### 3. Gerar odds das quartas com Model6 ⬜

```bash
python3 scripts/match_odds.py <time_a> <time_b> 1000000   # repetir pros 4 jogos
```

### 4. Post Instagram quartas ⬜

- [ ] Hook + slide técnico (performance oitavas: 75% quem avança, zebra do Brasil)
- [ ] Slides por jogo — mesmo formato validado nas oitavas

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
