# WorldCup-2026 — Guia do Projeto

Simulador Monte Carlo da Copa do Mundo 2026. Usa atributos de jogadores (FC25/FIFA22/Transfermarket) para calcular força por seleção, simula o torneio via distribuição de Poisson, acompanha resultados reais e calibra os pesos iterativamente a cada rodada.

**Estado detalhado da sessão atual → [TASKS.md](TASKS.md)**

---

## Estado Atual (28 jun 2026)

- **Branch:** `group-phase/round-2` — fase de grupos ENCERRADA (72/72 jogos)
- **Fase de grupos:** ✅ completa — bracket R32 salvo em `output/r32_bracket.json`
- **Modelo ativo: Model4 (S14)** — SA+biases att+def, λ=2.0, treinado com 72 jogos
  - Método: `--biases` att+def (att_bias + def_bias por seleção, 100 parâmetros)
  - NLL=64.55, RankScore=+241; escolhido após comparação de 21 estratégias (S01–S21)
  - Pesos lidos dinamicamente de `output/calibrated_weights_sa.json`
  - Performance fase de grupos: 46/72 W/D/L (64%), ≥70% de confiança → 97% de acerto
- **Próximo passo:** odds R32 com Model4, posts Instagram R32

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

**Constantes atuais — Model4 (S14)** — SA+biases att+def, 72 jogos, λ=2.0:

| Constante | Model4 (ativo) | Model3 (R1+R2) |
|-----------|----------------|----------------|
| `BASE_XG` | **1.1438** | 1.1438 |
| `OFF_ATT_W` | **0.7146** | 0.7146 |
| `OFF_MID_W` | **0.2854** | 0.2854 |
| `RES_DEF_W` | **0.4474** | 0.4474 |
| `RES_GK_W` | **0.05** | 0.05 |
| `RES_MID_W` | **0.5026** | 0.5026 |

Pesos globais convergiram ao mesmo mínimo; diferença principal em relação ao Model3: biases att+def treinados com 72 jogos (antes: att_only, 48 jogos).

**Biases por seleção (att+def):** carregados de `output/calibrated_weights_sa.json` (= `output/weights_s14.json`).

**Performance fase de grupos com Model4:** 46/72 W/D/L (64%) — vitórias: 37/41 (90%), empates: 0/20 (0% — limitação estrutural Poisson), derrotas: 9/11 (82%). Acima de 70% de confiança: 97% de acerto, 0 zebras.

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
- Mesma loss, explora espaço globalmente (não segue gradiente local)
- **Modo padrão:** 4 parâmetros globais
- **`--biases`:** adiciona `att_bias` e `def_bias` por seleção com regularização L2
  - `xG_A = BASE_XG × (off_A × att_bias_A) / (res_B × def_bias_B)`
  - `loss = NLL + λ × Σ(bias − 1)²`
  - Perturbação: 50% globais, 50% biases
- **`--att-only`:** só `att_bias` por seleção (sem def_bias), 52 parâmetros
- **`--unconstrained`:** remove restrições de soma (w_mid_off = 1−w_att etc.), libera 5 pesos independentes com BASE_XG fixo em 1.0. Testado em S19–S21; convergiu ao mesmo mínimo que constrained → não muda resultado na prática.
- Logs a cada 10k iterações: temperatura, taxa de aceitação, NLL, pesos

### Histórico de calibração
- **R1 → R2:** pesos globais — ✅
- **R2 → R3:** att_only 48 jogos λ=1.5 (Model3) — ✅
- **R3 → R32:** att+def 72 jogos λ=2.0 → **Model4 (S14)** — ✅ ativo

### Comparação de estratégias (`model_compare.py`)
21 estratégias testadas (S01–S21) com RankScore como métrica principal. Vencedor: **S14** (SA+biases att+def, λ=2.0, 72 jogos, RankScore=+241). Resultado salvo em `output/model_comparison.md`.

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
| `match_odds.py` | Odds de um jogo específico (usa biases) | `output/odds_{a}_vs_{b}.json` |
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
| `output/copa_real_state.json` | Resultados reais — 72 jogos fase de grupos |
| `output/calibrated_weights_sa.json` | **Model4 (S14)** — pesos ativos (lidos por simulate.py e match_odds.py) |
| `output/weights_s14.json` | Cópia de referência do Model4 |
| `output/calibrated_weights.json` | Pesos L-BFGS-B (referência, não aplicado) |
| `output/simulation_results.json` | Última simulação 1M (pós-R3, Model3 — recalcular com Model4) |
| `output/simulation_results_pre_r3.json` | Backup odds campeão pré-R3 |
| `output/r32_bracket.json` | 32 times classificados para o mata-mata |
| `output/model_comparison.md` | Tabela completa 21 estratégias (S01–S21) com RankScore |
| `output/model4_vs_reality.md` | Top-3 predições vs resultado real — 72 jogos |
| `output/model4_report.md` | Análise por time: acertos, erros, classificados, placares exatos |
| `output/model4_wdl_report.md` | Análise W/D/L: matriz de confusão, calibração, zebras |
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
