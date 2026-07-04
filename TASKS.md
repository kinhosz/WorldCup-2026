# TASKS — Estado e Próximos Passos

*Atualizado: 04 jul 2026 — R32 encerrado (16/16), decidida nova metodologia de mata-mata, Model5 ativo, iniciando oitavas*

---

## Estado Atual: R32 encerrado → Oitavas (R16)

- **16/16 jogos do R32** registrados em `copa_real_state.json` (`knockout_results` #73–88) ✅
- **Análise W/D/L do R32** salva em `output/r32_wdl_report.md` ✅
- **Model5 ativo** — treinado com 88 jogos (72 grupo + 16 R32), pesos de rodada revisados + bônus time vivo ✅ (ver `CLAUDE.md` → Estado Atual e `output/model5_vs_model4_r32.md`)
- **Bracket das oitavas definido** (a partir dos vencedores reais) ⬜ odds pendentes

### Oitavas (R16) — confrontos definidos

| Jogo | Confronto |
|------|-----------|
| R16 #1 | Canadá x Marrocos |
| R16 #2 | Paraguai x França |
| R16 #3 | Bélgica x EUA |
| R16 #4 | Espanha x Portugal |
| R16 #5 | Brasil x Noruega |
| R16 #6 | México x Inglaterra |
| R16 #7 | Suíça x Colômbia |
| R16 #8 | Egito x Argentina |

---

## Performance R32 (Model4 S14)

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

## Decisão de metodologia — Mata-mata (04 jul 2026)

Discussão completa: como o modelo nunca prevê empate (limitação estrutural do Poisson independente) e placares exatos de baixo score (0–1, 1–0, 1–1) carregam pouca informação, decidimos mudar a abordagem de previsão **só para jogos de mata-mata**:

### 1. "Quem avança" substitui W/D/L

```
P(avança_A) = P(vence_A) + 0.5 × P(empate)
P(avança_B) = P(vence_B) + 0.5 × P(empate)
```

- Pênaltis tratados como **50/50** — não modelar prorrogação.
- **Por quê:** prorrogação dependeria de squad com reservas/banco, mas `build_team_scores.py` só usa o "top-K" (melhor XI), sem dados de profundidade de elenco — modelar isso introduziria mais ruído que sinal.
- Matematicamente não muda quem é o favorito (soma a mesma fatia dos dois lados), mas resolve dois problemas reais:
  - Mede a coisa certa: jogos que empataram nos 90' mas o favorito avançou (Egito x Austrália, Argentina x Cabo Verde) contam como **acerto**, não erro.
  - Corrige a calibração de confiança: bucket ≥70% sobe de 60% (W/D/L) para **87.5%** (quem avança) no R32.
- **Só se aplica a jogos de mata-mata** — fase de grupos continua usando W/D/L normal (lá o empate é um resultado final válido).

### 2. Métricas derivadas para "aposta assertiva" (complementam o top-score, não substituem)

Calculadas de graça a partir dos dois xG de Poisson já existentes (sem retreinar nada):

| Métrica | Fórmula | Vantagem |
|---------|---------|----------|
| Over/Under gols (ex: 2.5) | soma das duas Poisson | Indiferente a quem ganha — funciona mesmo em empate |
| Ambas marcam (BTTS) | `(1-P(A=0)) × (1-P(B=0))` | Idem |
| Clean sheet | `P(oponente=0)` | Forte quando um time tem defesa muito acima da média |
| Vitória por margem (2+) | soma da diagonal da matriz | Mais assertivo que placar exato |

Regra: calcular todas + W/D/L, escolher a de **maior probabilidade** como "aposta do modelo" daquele jogo. Top-3 score continua no post, mas como detalhe/curiosidade — não mais como a aposta principal.

### Pendente: implementar no `match_odds.py`

⬜ Ainda não implementado — próxima tarefa antes de gerar as odds das oitavas no formato novo.

---

## Bug conhecido — CORRIGIDO (04 jul 2026)

`scripts/calibrate_sa.py::_parse_score` quebrava em `score_str` com sufixo `PEN`/`AET` — corrigido pra sempre extrair o placar de 90' (`note='AET'` lê o placar entre parênteses).

---

## Model5 — como foi feito

- Pesos por rodada revisados: `r3: 0.7→0.5`, `r32: 2.0→3.0` (r1/r2 seguem 1.0)
- Bônus `+0.2` por time ainda vivo no torneio, somado ao peso do jogo (até `+0.4` se os dois times do confronto estiverem vivos) — implementado em `ALIVE_TEAMS`/`_alive_bonus()` em `calibrate_sa.py`
- Rodado com 5 seeds em paralelo (999, 2026, 7, 123, 42), mesma config do Model4 (`--biases --lambda 2.0 --iters 500000 --restarts 5`) — NLL final quase idêntico entre todas (convergência robusta), RankScore empatado entre as 2 melhores → adotada seed 2026
- Ativado em `output/calibrated_weights_sa.json`; cópia de referência em `output/weights_model5.json`
- **Importante:** ao reajustar `ALIVE_TEAMS` nas próximas rodadas (oitavas em diante), atualizar a lista de times vivos em `calibrate_sa.py` antes de recalibrar de novo

---

## Próximos Passos

### 1. Implementar "quem avança" + métricas derivadas no `match_odds.py` ⬜

### 2. Gerar odds das oitavas (8 jogos) com Model5 no formato novo ⬜

```bash
python3 scripts/match_odds.py canada morocco 1000000
python3 scripts/match_odds.py paraguay france 1000000
python3 scripts/match_odds.py belgium united_states_of_america 1000000
python3 scripts/match_odds.py spain portugal 1000000
python3 scripts/match_odds.py brazil norway 1000000
python3 scripts/match_odds.py mexico england 1000000
python3 scripts/match_odds.py switzerland colombia 1000000
python3 scripts/match_odds.py egypt argentina 1000000
```

### 3. Post Instagram oitavas ⬜

- [ ] Hook + slide técnico (performance R32: 75% quem avança, 87.5% em ≥70%)
- [ ] Slides por jogo — novo formato: "X avança: XX%" + aposta assertiva + top-3 score

### 4. Após oitavas: entrada de resultados + retreino (Model6?) ⬜

```bash
python3 scripts/resultado.py  # entrar 8 resultados
# atualizar ALIVE_TEAMS em calibrate_sa.py pros 8 sobreviventes das oitavas antes de rodar
python3 scripts/calibrate_sa.py --biases --lambda 2.0 --iters 500000 --restarts 5 --output output/weights_r16.json
```

---

## Notas técnicas antigas (R32, referência)

### Times com bias extremo (att_only, Model3 → referência)
- Altos (≥1.35): Japan 1.44, Canada 1.39, Germany 1.37, Netherlands 1.35
- Baixos (≤0.31): Ecuador 0.20, Turkey 0.20, Belgium 0.27, Panama 0.31

### Dixon-Coles (ainda não testado)
Candidato para melhorar predição de empates de verdade (não só reclassificar via "quem avança") — testar como estratégia S22 no `model_compare.py` quando sobrar tempo entre rodadas.
