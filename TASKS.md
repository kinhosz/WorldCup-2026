# TASKS — Estado e Próximos Passos

*Atualizado: 28 jun 2026 — Fase de grupos encerrada, Model4 ativo, iniciando R32*

---

## Estado Atual: R32 — Mata-mata iniciando

- **72/72 jogos** fase de grupos em `copa_real_state.json` ✅
- **Model4 (S14) ativo** em `output/calibrated_weights_sa.json` ✅
- **Bracket R32 salvo** em `output/r32_bracket.json` ✅
- **Odds R32 calculadas** com Model3 — recalcular com Model4 ⬜

### Bracket R32 (na ordem FIFA)

| # | Jogo | # | Jogo |
|---|------|---|------|
| 1 | Africa do Sul vs Canada | 9  | Brasil vs Japão |
| 2 | Países Baixos vs Marrocos | 10 | Costa do Marfim vs Noruega |
| 3 | Alemanha vs Paraguai | 11 | México vs Equador |
| 4 | França vs Suécia | 12 | Inglaterra vs Congo |
| 5 | Bélgica vs Senegal | 13 | Suíça vs Argélia |
| 6 | EUA vs Bósnia | 14 | Colômbia vs Gana |
| 7 | Espanha vs Áustria | 15 | Austrália vs Egito |
| 8 | Portugal vs Croácia | 16 | Argentina vs Cabo Verde |

**R16:** W1 vs W2, W3 vs W4, W5 vs W6, W7 vs W8, W9 vs W10, W11 vs W12, W13 vs W14, W15 vs W16

---

## Performance Completa — Fase de Grupos

### Model4 (S14) — att+def biases, 72 jogos, λ=2.0 — ATIVO

| Rodada | Jogos | W/D/L correto | Nota |
|--------|-------|---------------|------|
| R1 | 24 | 14/24 (58%) | — |
| R2 | 24 | 17/24 (71%) | — |
| R3 | 24 | 15/24 (62%) | — |
| **Total** | **72** | **46/72 (64%)** | — |

**Calibração de confiança:**
- ≥70%: 28/29 (97%), 0 zebras
- 60–69%: 81%, 0 zebras
- <60%: zona incerta (44%)
- Empates: 0/20 acertados — limitação estrutural Poisson (não predizível sem Dixon-Coles)

### Destaques fase de grupos
- Colômbia 1ª no Grupo K (Portugal 2º) — maior surpresa
- Senegal como melhor 3º (5-0 no Iraq garantiu GF alto)
- Belgium bias 0.27 (att_only) → deve subir no R32 com att+def

---

## Próximos Passos — R32

### 1. Recalcular odds R32 com Model4 ⬜

```bash
# 16 jogos do bracket
python3 scripts/match_odds.py south_africa canada 1000000
python3 scripts/match_odds.py netherlands morocco 1000000
# ... (todos os 16 jogos)
```

### 2. Simulação R32 1M com Model4 ⬜

```bash
python3 scripts/simulate.py 1000000
```

### 3. Posts Instagram R32 ⬜

- [ ] Post previsões R32: hook + slide técnico (W/D/L 64%, calibração ≥70%→97%) + slides por jogo
- [ ] Post odds de campeão pós-grupos

### 4. Após rodada R32: entrada de resultados + retreino ⬜

```bash
python3 scripts/resultado.py  # entrar 16 resultados
python3 scripts/calibrate_sa.py --biases --lambda 2.0 --iters 500000 --restarts 5 --output output/weights_r32.json
```

---

## Notas técnicas para R32

### Slide técnico do post R32
- Usar dados de `output/model4_wdl_report.md`
- Highlight: ≥70% → 97% confiança, 64% geral, empates como ponto cego
- Mencionar que fase mata-mata não tem empate regular → modelo favorecido

### Calibração futura
- Mata-mata tem prorrogação + pênaltis → adaptar `resultado.py` e `calibrate_sa.py`
- Prorrogação modelada como 50/50 (atual) — revisar se necessário
- Dixon-Coles correction: candidato para melhorar predição de empates (relevante para mata-mata com possibilidade de empate no tempo normal)

### Times com bias extremo (att_only, Model3 → referência)
- Altos (≥1.35): Japan 1.44, Canada 1.39, Germany 1.37, Netherlands 1.35
- Baixos (≤0.31): Ecuador 0.20, Turkey 0.20, Belgium 0.27, Panama 0.31
