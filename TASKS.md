# TASKS — Estado e Próximos Passos

*Atualizado: 24 jun 2026 — R2 completa, modelo retreinado, prompts R3 gerados*

---

## Estado da Branch `group-phase/round-2`

### Concluído ✅

- R2 completa: 48/48 jogos entrados em `copa_real_state.json` (R1 + R2 todos os grupos)
- Backup de odds de campeão pré-R3: `output/simulation_results_pre_r3.json`
  - Pré-R2 top: France 19.64%, Argentina 14.15%, Brazil 13.77%
- Calibração retreinada com 48 jogos (`--att-only`, λ=1.5, 5 restarts):
  - SA: NLL=45.67, Brier=0.4327 → `output/calibrated_weights_sa.json`
  - L-BFGS-B: mesmo NLL → `output/calibrated_weights.json`
- `calibrate_sa.py` e `calibrate.py` reescritos com suporte a `--att-only`
- `simulate.py` atualizado com tiebreaker H2H (regras FIFA 2026)
- `group_projection.py` corrigido (bug de double-counting R2 + H2H tiebreaker)
- Simulação 1M pós-R2: `output/simulation_results.json`
  - Top pós-R2: Argentina 19.0%, Netherlands 14.8%, Portugal 14.0%, France 12.2%, Brazil 9.5%
- Projeção de grupo 500k: `output/group_projection.json`
- Odds de todos os 24 jogos R3 (1M sims cada): `output/odds_*.json`
- Post 10 prompts gerados: `image_prompts_post10_tecnico_r2.md` (6 slides: hook, técnico, campeão odds, grupos A-F, grupos G-L, 3ºs + R32)
- Post 11 prompts gerados: `image_prompts_post11_r3_bc.md` (4 slides: hook, técnico R2, previsões Grupo B, previsões Grupo C)

### Performance modelo SA att_only (48 jogos)

| Métrica | R1 | R2 | R1+R2 |
|---------|----|----|--------|
| Probability score | 47.1% | 52.5% | 49.8% |
| Resultado certo | 14/24 (58%) | 15/24 (62%) | 29/48 (60%) |
| Top score correto | 5/24 (21%) | 5/24 (21%) | 10/48 (21%) |

---

## Próximos Passos — Rodada 3

### Urgente ao fim da R3

```bash
# 1. Entrar resultados reais (interativo)
python3 scripts/resultado.py

# 2. Avaliar modelo
python3 scripts/model_eval.py

# 3. Retreinar (com 72 jogos — todos os grupos terminados)
python3 scripts/calibrate_sa.py --att-only --lambda 1.5 --iters 500000 --restarts 5
python3 scripts/calibrate.py --att-only --lambda 1.5

# 4. Nova simulação e projeções
python3 scripts/simulate.py 1000000
python3 scripts/group_projection.py 500000

# 5. Gerar odds R32 (fase playoffs)
python3 scripts/match_odds.py <team_a> <team_b> 1000000
```

### Posts pendentes pós-R3

- [ ] Post 11 (previsões R3 grupos B e C): postar imagens geradas pelo Gemini
- [ ] Post 10 (técnico R2): postar imagens geradas pelo Gemini
- [ ] Posts previsões R3 para grupos D–L (gerar prompts após R3 completo)
- [ ] Post comparação odds de campeão: usar `simulation_results_pre_r3.json` vs novo

---

## Calibração — Notas para R3+

Com 72 jogos (R1+R2+R3), considerar:
- `--att-only` continua recomendado (52 parâmetros, ratio ~0.72 com 72 jogos)
- λ=1.5 pode ser reduzido para λ=1.0 com mais dados
- Verificar se times com 0 gols em 3 jogos ainda têm att_bias no limite inferior (0.20)

---

## Notas técnicas

### att_bias only — por que escolhemos
Com 48 jogos, att+def biases = 100 parâmetros (ratio ~0.48) — underdetermined.
att_only = 52 parâmetros (ratio ~0.54) com λ=1.5 → regularizado adequadamente.

### Empates — ponto fraco estrutural
Poisson com xG > 1.5 gera baixa probabilidade de empate. Biases de defesa podem ajudar (Dixon-Coles como melhoria futura).

### Times com att_bias no limite inferior (0.20)
Ecuador, Turkey, Belgium, Panama — marcaram 0 gols em 2 jogos. NLL minimizado em λ→0.
Com mais jogos esses biases devem convergir para valores mais realistas.
