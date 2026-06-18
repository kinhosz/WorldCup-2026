# WorldCup-2026 — Guia do Projeto

Simulador Monte Carlo da Copa do Mundo 2026. Usa atributos de jogadores (FC25/FIFA22/Transfermarket) para calcular força por seleção, simula o torneio via distribuição de Poisson, acompanha resultados reais e calibra os pesos iterativamente a cada rodada.

**Estado detalhado da sessão atual → [TASKS.md](TASKS.md)**

---

## Estado Atual (18 jun 2026)

- **Branch:** `fase-grupos/rodada-2` — pronta para trancar, próxima será `rodada-3`
- **Rodada 1:** 24/24 jogos completos ✅
- **Rodada 2:** 4 jogos iniciados (Grupos A e B), previsões geradas ✅
- **Calibração:** SA+biases com 24 jogos (λ=3.0, com outliers) — **aplicada em `simulate.py`**
  - Pesos lidos dinamicamente de `output/calibrated_weights_sa.json`
  - Performance R1: 6/24 placares exatos (25%), 18/24 resultados (75%)
- **Próximo passo (R3):** re-calibrar com 44 jogos, comparar SA vs L-BFGS-B

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

**Constantes atuais** — SA+biases calibrado R1 com 24 jogos (inclui outliers), aplicado em `simulate.py`:

| Constante | Valor aplicado | Anterior |
|-----------|----------------|----------|
| `BASE_XG` | **1.172** | 1.1192 |
| `OFF_ATT_W` | **0.8527** | 0.90 |
| `OFF_MID_W` | **0.1473** | 0.10 |
| `RES_DEF_W` | **0.5496** | 0.2922 |
| `RES_GK_W` | **0.2804** | 0.50 |
| `RES_MID_W` | **0.17** | 0.2078 |

**Biases por seleção:** carregados dinamicamente de `output/calibrated_weights_sa.json` (λ=3.0). Biases notáveis: Spain att=0.66, Portugal att=0.83, Belgium att=0.83, England att=1.17, USA att=1.17, Germany att=1.20, Croatia def=0.72, Paraguay def=0.72.

**Performance R1 com modelo SA+biases:** 6/24 placares exatos (25%), 18/24 resultados corretos (75%). Erros justificados por fatores extra-modelo (Brazil-Morocco, Spain-Cape Verde, Iran-NZ, Saudi-Uruguay, Qatar-Switzerland, Czech-South Korea).

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
  - Útil a partir da R3 (~48 jogos)
- Logs a cada 10k iterações: temperatura, taxa de aceitação, NLL, pesos

### Plano de calibração
- **R1 → R2:** pesos globais calibrados — **feito** ✅
- **R2 → R3:** re-calibrar com 44 jogos, comparar SA vs L-BFGS-B
- **R3 em diante:** biases por seleção com `calibrate_sa.py --biases`
  - Candidatos a bias: Saudi Arabia, Qatar, Australia, Iran (erros sistemáticos R1)

---

## Scripts

| Script | Uso | Output |
|--------|-----|--------|
| `build_team_scores.py` | Calcula scores por seleção | `output/team_scores.json` |
| `simulate.py` | Monte Carlo N simulações | `output/simulation_results.json` |
| `resultado.py` | Entrar resultados reais (interativo) | `output/copa_real_state.json` |
| `calibrate.py` | Calibrar via Poisson NLL + L-BFGS-B | `output/calibrated_weights.json` |
| `calibrate_sa.py` | Calibrar via Simulated Annealing (com suporte a biases) | `output/calibrated_weights_sa.json` |
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

### Rodada 1 — modelo SA+biases (24 jogos)

| Métrica | Valor |
|---------|-------|
| Placar exato | 6/24 = 25% |
| Resultado correto | 18/24 = 75% |

**Ponto fraco principal:** empates — difíceis com Poisson puro.

---

## Arquivos de Output Importantes

| Arquivo | Conteúdo |
|---------|----------|
| `output/team_scores.json` | Scores GK/DEF/MID/ATT por seleção |
| `output/copa_real_state.json` | Resultados reais (24 jogos R1) |
| `output/calibrated_weights_sa.json` | Pesos SA+biases ativos (lidos por simulate.py e match_odds.py) |
| `output/calibrated_weights.json` | Pesos L-BFGS-B (referência, não aplicado) |
| `output/simulation_results.json` | Última simulação (50k, pós-R1) |
| `output/group_projection.json` | Probabilidades de classificação por grupo (pós-R1) |
| `output/champion_odds_original.json` | Odds de campeão pré-R1 (baseline histórico) |
| `output/model_eval.json` | Avaliação formal R1 |
| `output/score_audit.md` | Breakdown por jogador (tier, rating, dropped?) |
| `output/round_1_comparison.md` | Previsão vs real R1 (20 jogos) |
| `output/calibration_report_r1.md` | Relatório completo calibração R1 |
| `output/calibration_report.png` | Gráfico da calibração |
| `output/odds_czech_republic_vs_south_africa.json` | Odds R2 — Grupo A |
| `output/odds_mexico_vs_republic_of_korea.json` | Odds R2 — Grupo A |
| `output/odds_switzerland_vs_bosnia_and_herzegovina.json` | Odds R2 — Grupo B |
| `output/odds_canada_vs_qatar.json` | Odds R2 — Grupo B |

---

## Social Media — Posts Instagram

Gerador: **Gemini**. Formato: **4:5 retrato, 1080×1350 px**. Arquivo de prompts por post.

### Convenção de temas por tipo de post

| Tipo | Tema | Fundo | Accent |
|------|------|-------|--------|
| Pós-rodada (resultados/classificação) | Dark navy | `#080C18` | verde `#00E676` |
| Pré-rodada (previsões) | Branco | `#FFFFFF` | azul `#2563EB` / coral `#FB923C` |

### Estrutura — Post de Previsões (pré-rodada) ✅ VALIDADO R2
3 slides: Hook → 1 slide por grupo (2 jogos por slide). Cada slide de grupo tem 2 match cards elevados empilhados. Cada card contém:
- xG dos dois times (pequeno, centralizado)
- Flag emoji + nome · "vs" · flag + nome
- Barra pill arredondada (azul=favorito / cinza=empate / coral=azarão) com % dentro em bold
- `"TOP:"` + 3 score chips inline (rounded dark rectangle, texto branco)

**Framing de prompt Gemini:** `"Professional sports editorial infographic"` + `"Inter or equivalent"` + `"white elevated card with subtle drop shadow"` — NÃO descrever como HTML.

**Referência validada:** `image_prompts_post3_previsoes_r2.md` ✅

**Regra de neutralidade:** sem labels de julgamento ("ZEBRA?", "SURPRESA"). Dados apenas.

**Regra obrigatória nos prompts:** todo texto, número e nome que aparece na imagem deve estar explicitamente dentro do bloco `>`. Gemini inventa valores se ficarem fora.

### Fluxo por rodada
1. **Pré-rodada:** `match_odds.py` para cada jogo → gerar `image_prompts_post{N}_previsoes_r{X}.md`
2. **Pós-rodada:** `resultado.py` → `group_projection.py` → `simulate.py` → gerar `image_prompts_post{N}_classificacao.md`

---

## Preferências de Desenvolvimento

- **Relatórios:** MD para dados tabulares, PNG só para gráficos/visuais
- **Calibração:** não aplicar automaticamente — sempre revisar LOO-CV antes
- **Scripts novos:** standalone, sem modificar pipeline existente quando for experimento
- **CLAUDE.md + TASKS.md:** atualizar ao fim de cada sessão ou tarefa relevante
