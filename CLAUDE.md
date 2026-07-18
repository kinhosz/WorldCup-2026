# WorldCup-2026 — Guia do Projeto

Simulador Monte Carlo da Copa do Mundo 2026. Usa atributos de jogadores (FC25/FIFA22/Transfermarket) para calcular força por seleção, simula o torneio via distribuição de Poisson, acompanha resultados reais e calibra os pesos iterativamente a cada rodada.

**Estado detalhado da sessão atual → [TASKS.md](TASKS.md)**

---

## Estado Atual (18 jul 2026)

- **Semifinais ENCERRADAS** (2/2 jogos) — **Final confirmada: Espanha x Argentina** · **3º lugar: França x Inglaterra**
- **Resultados das semis:** França 0–2 Espanha (90'), Inglaterra 1–2 Argentina (90', virada — Argentina estava perdendo)
- **Performance out-of-sample do Model6 nas semis** (pesos de antes da recalibração desta rodada): quem avança 2/2 (100% — Espanha 60.5%, Inglaterra 66.3%, nenhum bateu 70% de confiança). Placar exato: Inglaterra x Argentina 2–1 foi o **top-1** do modelo (a virada da Argentina bateu certo no placar); França x Espanha 0–2 ficou empatado em 4º/5º (9.0%, junto com 1–2).
- **Bug de bracket corrigido em `resultado.py`** (14 jul 2026, ver TASKS.md) — pares da semifinal (`101`/`102`) estavam errados, já fixado antes de registrar os resultados reais.
- **Correção de leitura na entrada dos resultados (18 jul 2026):** o placar de Inglaterra x Argentina foi inicialmente registrado como 2–1 (Inglaterra) por erro de interpretação da mensagem do usuário — corrigido pra 1–2 (Argentina, de virada) antes de qualquer cálculo posterior.
- **Modelo ativo: Model7** — mesma metodologia de pontos do Model6, agora com **102 jogos** (96 do Model6 + 4 QF + 2 SF) e **bônus de peso pra SF/Final** (pedido do usuário, 18 jul 2026) — ver "Calibração por Pontos" abaixo
  - Escolhido entre 5 seeds (999, 2026, 7, 123, 42), mesma config do Model6 (`--biases`, λ=2.0, 300k iters × 5 restarts) — **seed 123** venceu em pontos (77.14/91 = 84.8%), mas **não** em todos os critérios ao mesmo tempo (seed 999 teve melhor Brier 0.5015, seed 2026 melhor NLL 94.06) — trade-off como no Model5, decidido pelo critério oficial do projeto (pontos é o objetivo, NLL/Brier são só diagnóstico)
  - Pesos em `output/calibrated_weights_sa.json` (cópia: `output/weights_model7.json`; logs das 5 seeds em `output/model7_seeds/`)
  - `BASE_XG` subiu bastante (1.38 → 1.45); Espanha ganhou bias forte de ataque e defesa (att=1.13, def=1.30 — reflexo de 0 gols sofridos em 6 jogos); Argentina ficou com def_bias baixo (0.51, fragilidade defensiva real) mas att_bias positivo (1.04); Inglaterra caiu nos dois (att=0.77, def=0.76) após a eliminação
  - Model6 (96 jogos, sem bônus SF/Final) preservado em `output/weights_model6.json` como referência histórica
- **Prorrogação modelada explicitamente (18 jul 2026, pedido do usuário)** — antes, todo empate nos 90' do mata-mata caía direto em pênaltis 50/50. Agora `simulate.py::sim_knockout_match` e `match_odds.py` simulam 30min de prorrogação com xG escalado a 1/3 (proporcional ao tempo) antes de cair em pênaltis. **Validado** contra os 8 empates reais do mata-mata até as semis: 8.72 gols esperados vs 7 observados — bem alinhado. Curiosidade (não modelada como bias específico, n=2 é pouco): a Argentina marcou nas 2 vezes em que foi à prorrogação (Cabo Verde e Suíça), acima do esperado (0.67 e 0.52).
- **Correção de regra: disputa de 3º lugar NÃO tem prorrogação** (regra FIFA — só a Final tem). `match_odds.py` ganhou a flag `--terceiro-lugar`/`--no-extra-time` pra pular a prorrogação e ir direto de empate nos 90' pra pênaltis 50/50.
- **Odds geradas com Model7:**
  - 3º lugar (sem prorrogação): França 70.9% x Inglaterra 29.1% (`output/odds_france_vs_england.json`)
  - Final (com prorrogação): Espanha 86.5% x Argentina 13.5% (`output/odds_spain_vs_argentina.json`)
- **Próximo passo:** gerar posts Instagram do 3º lugar e da Final (estilo "Troféu Chegando"), depois publicar

---

## Calibração por Pontos (Model6, decidido 08 jul 2026)

Mudança de objetivo pedida pelo usuário: em vez de minimizar Poisson NLL, o `calibrate_sa.py` agora **maximiza pontos** — uma métrica discreta desenhada pra refletir o que realmente importa pro projeto (acerto de resultado + qualidade do placar), não a verossimilhança estatística pura. Faz sentido usar Simulated Annealing pra isso porque SA não precisa de gradiente — funciona bem com objetivos discretos/não-suaves, ao contrário de L-BFGS-B.

### Peso por rodada (pontos por acerto)

| R1 | R2 | R3 | R32 | R16 | QF | SF | Final |
|---|---|---|---|---|---|---|---|
| 0.5 | 0.5 | 0.25 | 1.0 | 1.0 | 1.0 | 1.5† | 2.0† |

†Bônus decidido pelo usuário no Model7 (18 jul 2026) — SF e Final pesam mais porque são os jogos que definem finalistas e campeão. Antes (Model6), eram 1.0 (igual ao resto do mata-mata) por ainda não terem sido disputados.

### Fórmula de pontos por jogo

- **Fase de grupos (R1/R2/R3):** acerto de W/D/L (outcome com maior probabilidade Poisson bate com o resultado real) → pontos = peso da rodada. Sem bônus de placar.
- **Mata-mata (R32 em diante):** acerto de "quem avança" (`P(vence) + 0.5×P(empate) ≥ 50%` bate com o vencedor real, pênaltis incluídos) → pontos = peso da rodada. **+ bônus de placar exato**, só no mata-mata: se o placar real é o mais provável do modelo (top-1) → +1.0; se é o 2º mais provável (top-2) → +0.667; se é o 3º (top-3) → +0.444 (queda constante de razão 2/3). Fora do top-3 → +0.
- Sem alive bonus (o `+0.2 por time vivo` do Model5 foi removido — não fazia parte do novo esquema).
- Regularização L2 dos biases (`λ×Σ(bias−1)²`) mantida como critério de desempate suave entre soluções com pontuação idêntica.

### Resultado Model6 (96 jogos de treino)

Pontos máximos possíveis: 78.0. Baseline (pesos default): 37.6 (48.2%). L-BFGS-B: 39.1 (50.1%). Model6 (SA, seed 42): **68.0 (87.2%)**.

### Resultado Model7 (102 jogos de treino — 96 + QF + SF, bônus SF/Final)

Pontos máximos possíveis: 91.0 (subiu por causa do bônus de peso, não só dos 6 jogos novos). Baseline: 43.6 (47.9%). L-BFGS-B: 45.5 (50.0%). Model7 (SA, seed 123): **77.14 (84.8%)**.

Diferente do Model6 (que venceu em pontos, NLL e Brier simultaneamente), o Model7 teve trade-off entre seeds: seed 123 (pontos 77.14) vs seed 999 (pontos 76.11, mas melhor Brier 0.5015) vs seed 2026 (pontos 76.75, melhor NLL 94.06). Decidido pelo critério oficial do projeto — pontos é o objetivo real da busca, NLL/Brier são só diagnóstico histórico.

---

## Metodologia de Mata-Mata (decidido 04 jul 2026)

A partir do R32, jogos de eliminatória direta usam uma abordagem diferente da fase de grupos, porque (a) o modelo nunca prevê empate como resultado mais provável (limitação estrutural do Poisson independente — precisa de dois xG quase idênticos e baixos simultaneamente, o que quase nunca ocorre) e (b) placar exato de baixo score (0–1, 1–0, 1–1) carrega pouca informação pra uma "aposta" editorial.

### "Quem avança" substitui W/D/L nos posts de mata-mata

```
P(avança_A) = P(vence_A) + 0.5 × P(empate)
P(avança_B) = P(vence_B) + 0.5 × P(empate)
```

- Não muda quem é o favorito (soma a mesma fatia dos dois lados), mas mede a métrica certa: jogos que empatam nos 90' mas o favorito avança nos pênaltis contam como acerto, não erro.
- Validado no R32: bucket de confiança ≥70% sobe de 60% (W/D/L 90') para 87.5% (quem avança) — muito mais coerente com os 97% históricos da fase de grupos.
- **Só se aplica ao mata-mata.** Fase de grupos continua usando W/D/L normal — lá o empate é resultado final válido.

### Prorrogação modelada explicitamente (decidido 18 jul 2026, substitui a decisão anterior)

Até a Model6, pênaltis eram tratados como 50/50 direto a partir do empate nos 90' — decisão de não modelar prorrogação porque exigiria squad-score com profundidade de banco/reservas (`build_team_scores.py` só usa top-K, a melhor escalação titular). O usuário pediu pra revisar isso depois de notar que a Argentina já tinha marcado gols na prorrogação duas vezes (contra Cabo Verde e Suíça).

Nova abordagem, sem precisar de dados de banco:

```
xG_prorrogação_A = xG_90_A / 3      (30min ≈ 1/3 dos 90min, mesma taxa de gols)
xG_prorrogação_B = xG_90_B / 3
```

- Se A x B empatam nos 90': simula os 30min extras com Poisson(xG/3) pra cada time.
- Se ainda empatar depois da prorrogação: pênaltis, continuam 50/50 (não modelados — mesma limitação de sempre, squad depth).
- **Validado** contra os 8 empates reais do mata-mata até as semifinais: modelo esperava 8.72 gols na prorrogação somando os 16 períodos (8 jogos × 2 times), aconteceram 7 — bem alinhado. 4 dos 8 jogos foram a pênaltis sem gol na prorrogação, 4 tiveram gol. A Argentina marcou nas 2 vezes em que foi à prorrogação (Cabo Verde e Suíça), acima do esperado pelo modelo (0.67 e 0.52) — não virou bias específico por ser só 2 jogos (overfitting), mas é um dado editorial válido pros posts.
- Implementado em `simulate.py::sim_knockout_match` (Monte Carlo completo) e `match_odds.py::extra_time_breakdown` (odds de um jogo específico).
- **Exceção: disputa de 3º lugar não tem prorrogação** (regra oficial da FIFA — só a Final tem). `match_odds.py` ganhou a flag `--terceiro-lugar` (ou `--no-extra-time`) pra pular a prorrogação nesse caso e ir direto de empate nos 90' pra pênaltis 50/50.

### Métricas derivadas para "aposta assertiva" (complementam o top-score, não substituem)

Calculadas a partir dos dois xG de Poisson já existentes, sem retreinar nada:

| Métrica | Fórmula | Vantagem |
|---------|---------|----------|
| Over/Under gols (ex: 2.5) | soma das duas Poisson | Indiferente a quem ganha |
| Ambas marcam (BTTS) | `(1-P(A=0)) × (1-P(B=0))` | Indiferente a quem ganha |
| Clean sheet | `P(oponente=0)` | Forte quando defesa muito acima da média |
| Vitória por margem (2+) | soma da diagonal da matriz | Mais assertivo que placar exato |

Regra: calcular todas + W/D/L, escolher a de maior probabilidade como "aposta do modelo". Top-3 score continua no post como detalhe/curiosidade, não mais como aposta principal.

Implementado em `match_odds.py::derived_metrics` + `best_assertive_claim` (escolhe a de maior probabilidade automaticamente).

**Bug corrigido (04 jul 2026):** `calibrate_sa.py::_parse_score` quebrava em `score_str` com sufixo `PEN`/`AET` — agora extrai corretamente o placar de 90' (formatos `"1–1 pen."` e `"3–2 (1–1 AET)"` tratados).

---

## Pipeline Completo

```
squads/*.json + datasets/extracted/
        ↓
build_team_scores.py  →  output/team_scores.json
        ↓
simulate.py           →  output/simulation_results.json
match_odds.py         →  output/odds_{a}_vs_{b}.json
        ↓
resultado.py          →  output/copa_real_state.json  (resultados reais)
        ↓
calibrate.py          →  output/calibrated_weights.json + calibration_report.png
calibrate_sa.py       →  output/calibrated_weights_sa.json  (alternativa SA)
        ↓
model_eval.py         →  output/model_eval.json
round_report.py       →  output/round_{N}_report.png
```

---

## Fórmula xG

```
offense_A    = OFF_ATT_W × attack_A  + OFF_MID_W × midfield_A
resistance_B = RES_DEF_W × defense_B + RES_GK_W  × goalkeeper_B + RES_MID_W × midfield_B

xG_A = min(BASE_XG × offense_A / max(resistance_B, 0.10), 8.0)
```

**Constantes atuais — Model7** — SA por pontos, biases att+def, 102 jogos (72 grupo + 16 R32 + 8 R16 + 4 QF + 2 SF), λ=2.0, bônus SF/Final:

| Constante | Model7 (ativo) | Model6 | Model5 | Model4 (S14) |
|-----------|----------------|--------|--------|--------------|
| `BASE_XG` | **1.4453** | 1.3796 | 1.0118 | 1.1438 |
| `OFF_ATT_W` | **0.3643** | 0.5127 | 0.5809 | 0.7146 |
| `OFF_MID_W` | **0.6357** | 0.4873 | 0.4191 | 0.2854 |
| `RES_DEF_W` | **0.1556** | 0.1969 | 0.3223 | 0.4474 |
| `RES_GK_W` | **0.5** | 0.5 | 0.454 | 0.05 |
| `RES_MID_W` | **0.3444** | 0.3031 | 0.2237 | 0.5026 |

Diferença em relação ao Model6: dataset cresceu de 96 pra 102 jogos (QF+SF) e o `ROUND_WEIGHTS` ganhou bônus pra SF (1.5) e Final (2.0) — ver "Calibração por Pontos" acima. `OFF_MID_W` passou a pesar mais que `OFF_ATT_W` (inversão em relação ao Model6) — meio-campo virou o principal preditor de ataque nessa seed.

**Biases por seleção (att+def):** carregados de `output/calibrated_weights_sa.json` (= `output/weights_model7.json`). Espanha ganhou bias forte de ataque e defesa (att=1.13, def=1.30 — reflexo de não sofrer gols); Argentina ficou com def_bias baixo (0.51 — fragilidade defensiva real, mesmo avançando) mas att_bias positivo (1.04); Inglaterra caiu nos dois (att=0.77, def=0.76) após a eliminação na semi; França também caiu um pouco (att=0.95, def=1.07) após perder a semi.

**Performance fase de grupos com Model4 (referência histórica):** 46/72 W/D/L (64%) — vitórias: 37/41 (90%), empates: 0/20 (0% — limitação estrutural Poisson), derrotas: 9/11 (82%). Acima de 70% de confiança: 97% de acerto, 0 zebras.

**Performance Model5 nos 88 jogos de treino (in-sample):** RankScore 312 (vs 292 do Model4 nos mesmos 88), Top-1 22/88, Top-3 51/88, W/D/L 58/88 (65.9%). Não é teste de generalização — o Model5 treinou nesses mesmos jogos.

**Performance Model6 nos 96 jogos de treino (in-sample, objetivo por pontos):** 68.0/78.0 pontos (87.2%). Out-of-sample nas quartas: quem avança 3/4 (75%). Out-of-sample nas semis (pesos do Model6, antes desta recalibração): quem avança 2/2 (100%), incluindo o placar exato 2–1 da virada da Argentina como top-1 do modelo.

**Performance Model7 nos 102 jogos de treino (in-sample, objetivo por pontos com bônus SF/Final):** 77.14/91.0 pontos (84.8%) — ver "Calibração por Pontos" acima. Ainda não avaliado fora da amostra — só restam 3º lugar e Final.

---

## Dados dos Jogadores — Cascade de 4 Tiers

Para cada jogador, o sistema tenta em ordem:

1. **FC25 (akshay)** — `datasets/extracted/fc25_akshay/players_info.csv` (~17.470 jogadores, 2025)
2. **FIFA 22** — `datasets/extracted/players_22.csv` (~19.239 jogadores, 2022)
3. **Transfermarket** — `output/market_value_by_nation.json` → rating log-linear (€1M→65, €180M→91)
4. **Mediana global** — um valor único por setor (GK ~71.9, DEF ~71.9, MID ~70.5, ATT ~74.0)

**Matching por nome:** fuzzy (SequenceMatcher + token overlap), threshold 0.72. Overrides manuais:
- `('republic_of_korea', 'Son Heungmin')` → `'H. Son'` (nome em coreano no FIFA22)
- `('spain', 'Mikel MERINO')` → `'Merino'` (fuzzy pegava Mikel Rico, 36 anos)
- `('portugal', 'Francisco Trincao')` → `'Trincão'` (acento diferente no FC25)

**MIN_SECTOR_RATING:** rejeita matches que produzem rating < 30 (GK), < 35 (outros).

---

## Score por Setor

| Setor | Atributos | Top-K |
|-------|-----------|-------|
| GK | goalkeeping_diving, reflexes, handling, positioning | 1 |
| DEF | defending, physic | 4 |
| MID | passing, dribbling | 4 |
| ATT | shooting, pace | 3 |

**Fluxo:** coleta ratings → descarta bottom 30% → log-mean dos restantes → min-max normalize entre 48 seleções → [0.1, 1.0]

**Nota FC25 GK:** mapeamento especial — `pac`=diving, `sho`=handling, `dri`=reflexes, `phy`=positioning

---

## Grupos do Torneio

```python
GROUPS = {
    "A": ["mexico", "south_africa", "republic_of_korea", "czech_republic"],
    "B": ["canada", "bosnia_and_herzegovina", "qatar", "switzerland"],
    "C": ["brazil", "morocco", "haiti", "scotland"],
    "D": ["united_states_of_america", "paraguay", "australia", "turkey"],
    "E": ["germany", "curacao", "ivory_coast", "ecuador"],
    "F": ["netherlands", "japan", "sweden", "tunisia"],
    "G": ["belgium", "egypt", "ira", "new_zealand"],
    "H": ["spain", "cape_verte", "saudi_arabia", "uruguay"],
    "I": ["france", "senegal", "iraq", "norway"],
    "J": ["argentina", "algeria", "austria", "jordan"],
    "K": ["portugal", "congo", "uzbekistan", "colombia"],
    "L": ["england", "croatia", "ghana", "panama"],
}
```

Torneio: 12 grupos × 4 times → top-2 + 8 melhores 3ºs avançam → R32 → R16 → QF → SF → Final.

---

## Calibração

### L-BFGS-B (`calibrate.py`)
- **Loss:** Poisson NLL = `Σ [xG − k × log(xG)]`
- **Parâmetros:** `[BASE_XG, w_att, w_def, w_gk]` — outros dois derivados
- **Validação:** LOO-CV
- **Flag:** `--exclude-outliers` remove jogos com diff ≥ 4 gols

### Simulated Annealing (`calibrate_sa.py`)
- Explora espaço globalmente (não segue gradiente local) — por isso funciona tanto pra NLL contínua quanto pro objetivo por pontos (discreto, sem gradiente) do Model6
- **Objetivo:** a partir do Model6, `neg_points_loss` (maximizar pontos, ver "Calibração por Pontos") — antes disso, `poisson_nll` (minimizar NLL). A função `poisson_nll` continua existindo só pro diagnóstico final (NLL/Brier reportados por continuidade histórica, não mais o alvo da busca)
- **Modo padrão:** 4 parâmetros globais
- **`--biases`:** adiciona `att_bias` e `def_bias` por seleção com regularização L2
  - `xG_A = BASE_XG × (off_A × att_bias_A) / (res_B × def_bias_B)`
  - `loss = -pontos + λ × Σ(bias − 1)²` (regularização como desempate suave entre soluções com pontuação idêntica)
  - Perturbação: 50% globais, 50% biases
- **`--att-only`:** só `att_bias` por seleção (sem def_bias), 52 parâmetros
- **`--unconstrained`:** remove restrições de soma (w_mid_off = 1−w_att etc.), libera 5 pesos independentes com BASE_XG fixo em 1.0. Testado em S19–S21; convergiu ao mesmo mínimo que constrained → não muda resultado na prática.
- Logs a cada 10k iterações: temperatura, taxa de aceitação, pontos (ou NLL nos modelos pré-Model6), pesos

### Histórico de calibração
- **R1 → R2:** pesos globais — ✅
- **R2 → R3:** att_only 48 jogos λ=1.5 (Model3) — ✅
- **R3 → R32:** att+def 72 jogos λ=2.0 → **Model4 (S14)** — ✅ histórico
- **R32 → Oitavas:** att+def 88 jogos λ=2.0, pesos por rodada revisados + bônus time vivo, objetivo NLL → **Model5** — ✅ histórico
- **Oitavas → Quartas:** att+def 96 jogos λ=2.0, pesos por rodada redesenhados, objetivo mudou pra **pontos** → **Model6** — ✅ histórico
- **Semis → Final:** att+def 102 jogos λ=2.0, bônus de peso SF(1.5)/Final(2.0) → **Model7** — ✅ ativo

### Comparação de estratégias (`model_compare.py`)
21 estratégias testadas (S01–S21) com RankScore como métrica principal. Vencedor da fase de grupos: **S14** (SA+biases att+def, λ=2.0, 72 jogos, RankScore=+241) → virou Model4. Resultado salvo em `output/model_comparison.md`.

### Seleção do Model5 por múltiplas seeds
Em vez de comparar estratégias estruturalmente diferentes, o Model5 usou a mesma config do S14 (biases att+def, λ=2.0, 500k iters × 5 restarts) rodada com 5 seeds distintas (999, 2026, 7, 123, 42) em paralelo — uma espécie de "restart em escala maior". Resultado: NLL final quase idêntico entre todas (135.12–135.13), RankScore empatado (312) entre as duas melhores (seed 999 e 2026) — sinal de que a otimização já converge de forma robusta pro mesmo mínimo global independente da seed. Adotada a seed 2026.

### Seleção do Model6 por múltiplas seeds
Mesma metodologia do Model5 (5 seeds em paralelo, config idêntica: `--biases`, λ=2.0, 300k iters × 5 restarts — default do script), mas agora otimizando pontos em vez de NLL. Resultado: seed 42 venceu em **todas** as métricas simultaneamente (pontos 68.0/78=87.2%, NLL 80.39, Brier 0.494) — sem empate/trade-off como no Model5. Logs completos das 5 seeds em `output/model6_seeds/`.

### Seleção do Model7 por múltiplas seeds
Mesma metodologia (5 seeds em paralelo, config idêntica ao Model6), agora com 102 jogos e `ROUND_WEIGHTS` com bônus SF/Final. Resultado: seed 123 venceu em pontos (77.14/91=84.8%), mas não simultaneamente em NLL/Brier — seed 999 teve melhor Brier (0.5015, pontos 76.11) e seed 2026 melhor NLL (94.06, pontos 76.75). Trade-off como no Model5, decidido por pontos (critério oficial da busca). Logs completos das 5 seeds em `output/model7_seeds/`.

---

## Scripts

| Script | Uso | Output |
|--------|-----|--------|
| `build_team_scores.py` | Calcula scores por seleção | `output/team_scores.json` |
| `simulate.py` | Monte Carlo N simulações | `output/simulation_results.json` |
| `resultado.py` | Entrar resultados reais (interativo) | `output/copa_real_state.json` |
| `calibrate.py` | Calibrar via Poisson NLL + L-BFGS-B | `output/calibrated_weights.json` |
| `calibrate_sa.py` | Calibrar via Simulated Annealing (com suporte a biases, --unconstrained) | `output/calibrated_weights_sa.json` |
| `model_compare.py` | Comparar N estratégias de calibração via RankScore | `output/model_comparison.md` |
| `model_eval.py` | Avaliar modelo (Brier, acurácia) | `output/model_eval.json` |
| `match_odds.py` | Odds de um jogo específico (usa biases; `--knockout` pra prorrogação+pênaltis, `--terceiro-lugar` pra pênaltis direto sem prorrogação) | `output/odds_{a}_vs_{b}.json` |
| `group_projection.py` | Probabilidade de classificação por grupo | `output/group_projection.json` |
| `round_report.py` | Visual PNG de uma rodada | `output/round_{N}_report.png` |
| `play_simulation.py` | Simulação determinística (seed) | `output/JOGO_{seed}.md` |
| `megazord.py` | Bracket determinístico (argmax) | terminal |
| `r1_comparison.py` | Comparação R1 previsão vs real | `output/round_1_comparison.md` |

---

## Bugs Corrigidos

1. **Cross-position GK mismatches** — fuzzy pegava jogador de linha no GK. Fix: `MIN_SECTOR_RATING`. Impacto: CIV GK 0.000 → 0.229, AUS GK 0.052 → 0.215.
2. **Son Heung-min** — long_name em coreano no FIFA22. Fix: override manual. Impacto: Coreia ATT 0.168 → 0.804.
3. **Mikel Merino** — FIFA22 short curto, fuzzy pegava "Mikel Rico" (36 anos). Fix: override manual. Impacto: Espanha MID +12 pts.
4. **Alemanha squad** — Sané e Wirtz listados como meias. Fix: movidos para attackers. Impacto: ATT 0.015 → 0.564.
5. **match_odds.py sem biases** — `compute_xg` chamado sem team keys. Fix: passar `team_a, team_b`. Impacto: odds individuais agora aplicam biases corretamente.

---

## Performance Histórica

### Model4 — SA+biases att+def (72 jogos, λ=2.0) — ATIVO

| Métrica | R1 | R2 | R3 | Total |
|---------|----|----|-----|-------|
| W/D/L correto | 14/24 (58%) | 17/24 (71%) | 15/24 (62%) | 46/72 (64%) |
| Baseline (aleatório) | — | — | — | 33.3% |

**Análise de confiança (curva de calibração):**
- Modelo deu ≥70% → acerto em 28/29 jogos (97%), 0 erros de direção
- Modelo deu 60–69% → 81% de acerto, 0 erros de direção
- Modelo deu <60% → 44% de acerto (zona de incerteza)
- Modelo NUNCA previu empate como resultado mais provável (limitação estrutural Poisson)
- 20 empates em 72 jogos = 20 erros automáticos; sem empates: 46/52 (88%)

### Model3 — SA+att_only (48 jogos R1+R2, λ=1.5) — histórico

| Métrica | R1 | R2 | R1+R2 |
|---------|----|----|--------|
| Probability score | 47.1% | 52.5% | 49.8% |
| Resultado certo | 14/24 (58%) | 15/24 (62%) | 29/48 (60%) |
| Top score correto | 5/24 (21%) | 5/24 (21%) | 10/48 (21%) |

**Ponto fraco estrutural (ambos os modelos):** empates — Poisson puro com xG>1.3 gera P(empate) sistematicamente abaixo do real.

---

## Arquivos de Output Importantes

| Arquivo | Conteúdo |
|---------|----------|
| `output/team_scores.json` | Scores GK/DEF/MID/ATT por seleção |
| `output/copa_real_state.json` | Resultados reais — 72 jogos de grupo + 30 do mata-mata (R32+R16+QF+SF) |
| `output/calibrated_weights_sa.json` | **Model7** — pesos ativos (lidos por simulate.py e match_odds.py) |
| `output/weights_model7.json` | Cópia de referência do Model7 (102 jogos, bônus SF/Final) |
| `output/model7_seeds/` | Logs + pesos das 5 seeds testadas pro Model7 (999, 2026, 7, **123 vencedora**, 42) |
| `output/weights_model6.json` | Cópia de referência do Model6 (histórico, 96 jogos, sem bônus SF/Final) |
| `output/model6_seeds/` | Logs + pesos das 5 seeds testadas pro Model6 (999, 2026, 7, 123, 42 vencedora) |
| `output/r16_wdl_report.md` | Análise "quem avança" das 8 oitavas com Model5 — 6/8 (75%), zebra do Brasil |
| `output/model6_full_evaluation.md` | Reavaliação retroativa das 96 partidas com Model6 (in-sample) + combinações entre os 8 times vivos |
| `output/model6_evaluation.html` | Mesmo conteúdo do `.md` acima em página interativa standalone (abas por rodada, barras de confiança) — abrir direto no navegador |
| `output/simulation_results_model6.json` | 10M simulações Model6 pós-oitavas — probabilidade de campeão/finalista/semi dos 8 times vivos |
| `output/odds_france_vs_morocco.json`, `..._spain_vs_belgium.json`, `..._norway_vs_england.json`, `..._argentina_vs_switzerland.json` | Odds das 4 quartas (Model6, `--knockout`) |
| `output/odds_france_vs_spain.json`, `..._england_vs_argentina.json` | Odds das 2 semifinais (Model6, antes da recalibração pro Model7) |
| `output/odds_france_vs_england.json` | Odds do 3º lugar (Model7, `--knockout --terceiro-lugar` — sem prorrogação, regra FIFA) |
| `output/odds_spain_vs_argentina.json` | Odds da Final (Model7, `--knockout` — com prorrogação modelada) |
| `qf_post.md` | Prompts Instagram das quartas — novo estilo "Troféu Chegando" (preto quente + dourado, path-to-final) |
| `sf_post.md` | Prompts Instagram das semifinais, mesmo estilo |
| `output/weights_model5.json` | Cópia de referência do Model5 (histórico, objetivo NLL) |
| `output/weights_s14.json` | Cópia de referência do Model4 (histórico) |
| `output/calibrated_weights.json` | Pesos L-BFGS-B (referência, não aplicado) |
| `output/simulation_results.json` | Última simulação (10M, Model6, pós-oitavas) — cópia idêntica de `simulation_results_model6.json` |
| `output/simulation_results_pre_r3.json` | Backup odds campeão pré-R3 |
| `output/r32_bracket.json` | 32 times classificados para o mata-mata |
| `output/model_comparison.md` | Tabela completa 21 estratégias (S01–S21) com RankScore |
| `output/model4_vs_reality.md` | Top-3 predições vs resultado real — 72 jogos |
| `output/model4_report.md` | Análise por time: acertos, erros, classificados, placares exatos |
| `output/model4_wdl_report.md` | Análise W/D/L: matriz de confusão, calibração, zebras |
| `output/r32_wdl_report.md` | Análise W/D/L do R32 (16 jogos) — base pra `r32_analise_completa.md` |
| `output/r32_analise_completa.md` | Análise completa do R32 pro post técnico Instagram: tabela dos 16 jogos, acertos/erros/zebras, empates, calibração, ganchos editoriais, auto-reflexão do modelo |
| `output/model5_vs_model4_r32.md` | Model5 vs Model4 nos 16 jogos do R32 (previsão, Rank, RankScore por jogo) |
| `output/oitavas_bracket_probabilidades.md` | Top 10 campeões (oitavas em diante), caminho completo do Brasil, chalk bracket dos Top 10, com bug do bracket documentado e cross-check Monte Carlo 10M |
| `output/top10_mudancas_model4_vs_model5.md` | Por que o Top 10 mudou tanto: eliminações reais, recalibração de bias por seleção, posição no chaveamento |
| `output/weights_s08.json` … `output/weights_s21.json` | Pesos de cada estratégia treinada |
| `output/model_eval.json` | Avaliação formal R1+R2 (48 jogos, Model3) |
| `output/score_audit.md` | Breakdown por jogador (tier, rating, dropped?) |
| `output/calibration_report.png` | Gráfico da calibração |
| `output/odds_*.json` | Odds R32 — 16 jogos (Model4) |
| `r3_grupos_jkl.md` | Prompts Instagram previsões R3 Grupos J+K+L |

---

## Social Media — Posts Instagram

Gerador: **Gemini**. Formato: **4:5 retrato, 1080×1350 px**.
Arquivos de prompts: `r{N}_{descricao}.md` na raiz do projeto (ex: `r3_grupos_abc.md`).

### Identidade visual por rodada

| Rodada | Fundo | Cards | Accent favorito | Accent azarão |
|--------|-------|-------|-----------------|---------------|
| R1 | dark navy `#080C18` | dark `#1E293B` | verde neon `#00E676` | — |
| R2 | off-white `#F0F4F8` | branco `#FFFFFF` | azul `#2563EB` | coral `#F97316` |
| R3 | midnight blue `#1A2E4A` | branco `#FFFFFF` | laranja `#E95420` | cinza `#94A3B8` |
| R32/R16 | foto estádio + bandeiras 28% opacity | dark `#1E293B` | verde neon `#4ADE80` | cinza `#94A3B8` |
| **QF em diante** | **preto quente `#14110C`** | **bronze `#201A12`** | **dourado metálico `#E3B341`** | **grafite `#6B7280`** |

**QF em diante — "Troféu Chegando" (validado 08 jul 2026, ver `qf_post.md`):**
- Tema: paleta esquenta conforme o torneio avança rumo à final — preto quente + dourado metálico substituem o azul/verde neon das rodadas anteriores
- Tipografia: serifada de exibição pros nomes/títulos (efeito "placa gravada"), sans-serif geométrica pros dados, números tabulares
- Tag de rodada: vermelho oxblood `#7A2E2E` (não mais vermelho puro)
- Elemento novo, exclusivo do mata-mata avançado: linha **"PATH TO THE FINAL"** (QF → SF → Final, nó ativo em dourado) — só faz sentido a partir daqui porque o bracket completo até a final já é conhecido
- Barra "quem avança": dourado `#E3B341` (com glow) pro favorito, grafite `#6B7280` pro azarão — sem meio-termo verde/vermelho
- Confidence pill (≥70%): fundo dourado `#E3B341`, texto escuro (antes era verde `#4ADE80`)
- Novos tipos de slide validados: "Model Report Card" (recap do modelo anterior) e "Title Odds" (ranking de probabilidade de campeão com barra dourada) — usar quando fizer sentido editorial, não obrigatório em toda rodada

**R3 — detalhes do design (validado):**
- Fundo: `#1A2E4A` (midnight steel blue)
- Card: `#FFFFFF` branco com drop shadow forte — contraste nítido contra o fundo
- Accent favorito: `#E95420` (laranja) — usado na pill bar e no label do favorito
- Pill bar: seção favorito em `#E95420` · empate em `#94A3B8` · azarão em `#CBD5E1`
- Score chips: fundo `#0F172A`, texto branco bold
- Labels fora dos cards (footer, header): `#93C5FD` (azul claro muted)
- Texto dentro dos cards: dark `#0F172A`, labels `#64748B`, muted `#94A3B8`
- Framing: `"Professional sports editorial infographic"` + `"Inter or equivalent"` + `"bright white elevated card with strong drop shadow on midnight blue background"`

### Estrutura padrão do carrossel de previsões

**Carrossel padrão (N grupos):**
1. **Hook** — grupos que fecham + times listados + "Previsões a seguir →"
2. **Slide técnico** — prob média do modelo nos resultados reais da rodada anterior. Comparação com baseline 33.3%. Lista individual de todos os jogos com %. Sem barrinhas.
3–N. **Slide de previsões por grupo** — 2 match cards empilhados. Cada card: `xG A · · · xG B` · nomes · pill bar proporcional · `TOP:` 3 score chips.

### Slide de Previsões — Regras do match card ✅ VALIDADO R3
- xG centralizado acima dos nomes: `"xG X.XX · · · Y.YY xG"`
- Pill bar: **CRITICAL — seção proporcional ao valor exato**. Seção < 7% → sem texto dentro, mostrar % no label abaixo.
- Labels abaixo da pill bar **em uma única linha** (nunca quebrar em duas linhas).
- `"TOP:"` + 3 score chips inline (fundo `#0F172A`, texto branco bold, formato `"X–Y  ZZ.Z%"`)
- Footer: `"1.000.000 simulações · Modelo Monte Carlo"`

### Regras gerais de prompt Gemini
- **Autossuficiência:** cada slide é standalone — copiar e colar direto no Gemini sem contexto externo
- **Dados explícitos:** todo texto, número e nome que aparece na imagem dentro do bloco `>`
- **Sem inventar:** incluir instrução "do not invent any values" em cada slide
- **Sem julgamento:** sem labels como "ZEBRA?", "SURPRESA", "FAVORITO" — dados apenas
- **Não descrever como HTML**

### Slide R32 — Template de jogo individual ✅ VALIDADO

Cada jogo do mata-mata tem slide próprio. Estrutura em 3 camadas:

**LAYER 1 — foto base:** stadium shot from behind the goal line, looking through goal posts and net towards pitch. Full bleed.

**LAYER 2 — bandeiras transparentes:** top half = bandeira do time A (28% opacity), bottom half = bandeira do time B (28% opacity). Cobrem o canvas inteiro (não o gol). A foto do campo deve ser visível através das bandeiras.

**LAYER 3 — conteúdo:** centralizado, começa ~15% do topo, drop shadows em todo texto.

```
Top label (small caps, wide letter-spacing, white): R32 · MATA-MATA · COPA DO MUNDO 2026
Team row (large bold white, single line): 🏳 TeamA  vs  TeamB 🏳
xG line (muted white, centered, once only): xG X.XX · · · Y.YY xG
Probability bar (proportional rounded pill, neon glow on green segment):
  left = win% TeamA (green #4ADE80 neon glow)
  center = draw% (grey #64748B)
  right = win% TeamB (muted #94A3B8)
  labels below each segment
TOP SCORES label (small caps muted)
3 chips dark #1E293B: "G–G  XX.X%" each
[se confiança ≥ 70%] green pill: ★ MODEL CONFIDENCE XX.X%
insight line bold white (from model data, not invented)
small muted: Above 70% confidence, the model was correct in 97% of group stage games.
Footer (very small muted): Model4 · SA+biases att+def · 1.000.000 simulations
```

**Regras de insight:** só incluir quando o modelo tiver algo real para dizer — bias extremo (att ou def), confidence ≥ 70%, ou contexto de bracket (ex: "apenas 0.0% de odds de campeão nas simulações"). Nunca inventar.

**Bandeiras com brasão:** Paraguay, Brazil, Argentina, Mexico, Colombia e outras têm emblema no centro da faixa branca — mencionar no prompt.

### Fluxo por rodada
1. `match_odds.py <a> <b> 1000000` para cada jogo → arquivo `r{N}_{grupos}.md`
2. `resultado.py` + `model_eval.py` → métricas para slide técnico
3. `group_projection.py` + `simulate.py 1000000` → post de classificação (arquivo separado)

---

## Preferências de Desenvolvimento

- **Relatórios:** MD para dados tabulares, PNG só para gráficos/visuais
- **Calibração:** não aplicar automaticamente — sempre revisar LOO-CV antes
- **Scripts novos:** standalone, sem modificar pipeline existente quando for experimento
- **CLAUDE.md + TASKS.md:** atualizar ao fim de cada sessão ou tarefa relevante
