# TASKS — Estado e Próximos Passos

*Atualizado: 18 jun 2026 — branch rodada-2 pronta para trancar*

---

## Estado da Branch `fase-grupos/rodada-2`

### Concluído ✅

- R1 completo: 24/24 jogos entrados em `copa_real_state.json`
- Calibração SA+biases (λ=3.0, com outliers, 24 jogos) aplicada em `simulate.py`
- Pesos lidos dinamicamente de `output/calibrated_weights_sa.json`
- Performance R1: 6/24 exatos (25%), 18/24 resultados (75%)
- Bug fix: `match_odds.py` agora passa team keys para `compute_xg` (biases aplicados)
- Simulação 50k pós-R1 com resultados reais travados
- Odds dos 4 jogos R2 (Grupos A e B): Czech/RSA, Swiss/BIH, Canada/Qatar, Mexico/KOR
- Post 2 (classificação + odds campeão): postado ✅
- Post 3 (previsões R2): prompts gerados em `image_prompts_post3_previsoes_r2.md` — **pendente validação no Gemini**
- Limpeza da branch: removidos arquivos obsoletos, odds R1 e posts já publicados

### Pendente nesta branch

- [ ] Validar `image_prompts_post3_previsoes_r2.md` no Gemini e postar

---

## Rodada 3 — Planejamento

Quando tivermos ~44-48 jogos (fim da R2):

### Fluxo padrão por rodada

```bash
# 1. Entrar resultados reais
python3 scripts/resultado.py

# 2. Atualizar simulação e projeções
python3 scripts/simulate.py 50000
python3 scripts/group_projection.py 50000

# 3. Gerar odds dos próximos jogos
python3 scripts/match_odds.py <time_a> <time_b> 200000

# 4. Calibrar (pós-R2, com 44 jogos)
python3 scripts/calibrate_sa.py --exclude-outliers
python3 scripts/calibrate.py --exclude-outliers   # comparar
```

### Calibração R3 com biases
```bash
python3 scripts/calibrate_sa.py --biases --exclude-outliers --lambda 1.0
```
Candidatos a bias: Saudi Arabia, Qatar, Australia, Iran (erros sistemáticos R1).
Ajustar `--lambda`: maior → biases conservadores, menor → biases agressivos.

### Decisão sobre outliers
Após cada rodada, checar se `--exclude-outliers` continua válido:
```bash
python3 scripts/calibrate.py --exclude-outliers --out /tmp/sem.json
python3 scripts/calibrate.py --out /tmp/com.json
```
Manter "sem outlier" enquanto: exatos(sem) >= exatos(com) **e** resultados(sem) >= resultados(com).

---

## Notas técnicas para referência futura

### Por que SA para biases
L-BFGS-B em espaço de 100+ parâmetros com regularização L2 tende a ficar preso em mínimos locais. SA explora globalmente — mais robusto para espaços não-convexos. Para 4 parâmetros globais, ambos convergem igual.

### Empates — ponto fraco estrutural
Poisson com xG > 1.5 gera baixa probabilidade de empate. Possíveis melhorias:
- Biases de defesa para times que empatam muito
- Modelo de Dixon-Coles (inflate de draw explícito) — futuro

### Interpretação do LOO-CV NEUTRO
Com 18-24 jogos e 4 parâmetros, o LOO-CV não tem poder estatístico para distinguir sinal de ruído. "NEUTRO" = "sem evidência de piora", não "sem melhora". O in-sample melhora claramente.
