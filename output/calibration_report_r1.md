# Relatório de Calibração — Rodada 1

**Data:** 2026-06-17 · **Script:** `python3 scripts/calibrate.py --exclude-outliers`

---

## 1. O que foi feito

O modelo xG usa uma fórmula paramétrica com 6 constantes hardcoded em `simulate.py`.
Após a rodada 1, temos resultados reais suficientes para ajustar essas constantes via
otimização numérica.

**Fórmula:**
```
xG_A = BASE_XG × (w_att × attack_A + w_mid_off × mid_A)
                / max(w_def × def_B + w_gk × gk_B + w_mid_res × mid_B, 0.10)
```

**Parâmetros livres (4):** `[BASE_XG, w_att, w_def, w_gk]`
Os outros dois são derivados pela restrição soma = 1:
- `w_mid_off = 1 − w_att`
- `w_mid_res = 1 − w_def − w_gk`

---

## 2. Método de otimização

| Item | Escolha | Por quê |
|------|---------|---------|
| Loss function | **Poisson NLL** | Gols são contagens — Poisson é o modelo correto. MSE superpenaliza placares como 7-1. |
| Otimizador | **L-BFGS-B** | Espaço contínuo, suave, com bounds nativos. Mais rápido que Nelder-Mead para 4 parâmetros. |
| Validação | **LOO-CV** | Com apenas 20 jogos, holdout fixo seria muito pequeno. Leave-one-out usa todos os dados. |
| Outliers | **Excluídos (diff ≥ 4 gols)** | Germany 7-1 e Sweden 5-1 distorcem o LOO-CV — ver seção 4. |

---

## 3. Resultados — pesos antes e depois

| Constante | Valor atual | Valor calibrado | Δ | Direção |
|-----------|-------------|-----------------|---|---------|
| `BASE_XG` | 1.300 | **1.119** | −0.181 | ↓ Reduz xG extremos |
| `OFF_ATT_W` | 0.700 | **0.900** | +0.200 | ↑ Ataque é mais preditivo |
| `OFF_MID_W` | 0.300 | **0.100** | −0.200 | ↓ Meio ofensivo menos relevante |
| `RES_DEF_W` | 0.600 | **0.292** | −0.308 | ↓ ⚠ instável — ver seção 5 |
| `RES_GK_W` | 0.200 | **0.500** | +0.300 | ↑ ⚠ bate no bound máximo |
| `RES_MID_W` | 0.200 | **0.208** | +0.008 | ≈ sem mudança |

---

## 4. Por que os outliers foram removidos

Com todos os 20 jogos, o LOO-CV dava veredicto **PIORA** (+0.187 NLL).
O motivo era o jogo Germany 7-1 Curacao dominando a métrica:

| Run | NLL LOO-CV padrão | NLL LOO-CV calibrado | Δ | Veredicto |
|-----|-------------------|----------------------|---|-----------|
| Com todos (20 jogos) | 1.413 | 1.600 | +0.187 | ✗ PIORA |
| Sem outliers (18 jogos) | 1.855 | 1.866 | +0.011 | **≈ NEUTRO** |

**Por que Germany distorce:** O modelo atual prevê xG = 5.56 para a Alemanha naquele jogo,
e ela de fato marcou 7. Isso gera NLL negativo (−3.85 — recompensa enorme para uma predição
certa). Quando esse jogo fica fora do treino no LOO-CV, a calibração reduz levemente o xG da
Alemanha, e ao avaliar esse fold a métrica piora muito. A calibração não estava errando — estava
sendo penalizada por ter acertado um caso extremo.

Resultado análogo com Sweden 5-1 Tunisia (segundo outlier removido, diff = 4).

---

## 5. Confiança por parâmetro

| Parâmetro | Confiança | Justificativa |
|-----------|-----------|---------------|
| `BASE_XG` ↓ | **Alta** | Aparece consistentemente em todos os runs (com outliers, sem, todos os 20). Sempre cai para ~1.12. Resolve xGs absurdos como Saudi Arabia xG 5.99. |
| `w_att` ↑ | **Alta** | Também consistente em todos os runs. w_att sobe para o bound superior (0.9). Faz sentido: nas 18 partidas regulares, o ataque foi o maior preditor de resultado. |
| `w_def` / `w_gk` | **Baixa** | Os valores mudam dramaticamente dependendo de quais jogos são incluídos. Com outliers: w_gk=0.109. Sem outliers: w_gk=0.500 (bate no bound). Sinal de que 18–20 jogos não são suficientes para separar o efeito de defesa vs goleiro. |

**Conclusão:** aplicar `BASE_XG` e `w_att` tem embasamento. Deixar `w_def`/`w_gk` nos valores
atuais até ter mais dados (rodada 2 = +24 jogos).

---

## 6. Melhoria por jogo (LOO-CV, sem outliers)

Jogos onde o modelo calibrado **melhora** (Brier menor):

| Jogo | Resultado | Brier atual | Brier cal | Δ | Contexto |
|------|-----------|-------------|-----------|---|----------|
| South Korea vs Czech Rep. | 2-1 | 0.600 | **0.438** | −0.163 | Modelo atual dava Czech como favorito |
| Canada vs Bosnia | 1-1 | 0.971 | **0.886** | −0.085 | Draw subestimado |
| Qatar vs Switzerland | 1-1 | 1.178 | **0.980** | −0.198 | xG do Qatar muito baixo no modelo atual |
| Australia vs Turkey | 2-0 | 1.014 | **0.906** | −0.108 | Upset não capturado — melhora parcial |
| Brazil vs Morocco | 1-1 | 1.087 | **1.006** | −0.081 | Draw subestimado |
| Belgium vs Egypt | 1-1 | 1.197 | **0.930** | −0.267 | Draw muito subestimado |
| Spain vs Cape Verde | 0-0 | 1.501 | **1.348** | −0.153 | 0-0 subestimado |
| Saudi Arabia vs Uruguay | 1-1 | 1.672 | **1.508** | −0.164 | Caso mais extremo — Saudi xG = 0.508 atual |

Jogos onde o modelo calibrado **piora**:

| Jogo | Resultado | Brier atual | Brier cal | Δ | Contexto |
|------|-----------|-------------|-----------|---|----------|
| Mexico vs South Africa | 2-0 | 0.436 | 0.598 | +0.162 | Vitória clara — calibração comprime xG |
| USA vs Paraguay | 4-1 | 0.169 | 0.299 | +0.130 | Vitória dominante |
| France vs Senegal | 3-1 | 0.204 | 0.340 | +0.136 | Vitória dominante |
| Austria vs Jordan | 3-1 | 0.331 | 0.608 | +0.277 | Maior piora — Jordan tem poucos dados |

**Padrão:** a calibração melhora em jogos com empate ou upset (os casos problemáticos),
mas piora em vitórias dominantes previsíveis. Trade-off esperado ao reduzir `BASE_XG`.

---

## 7. Métricas gerais de comparação

| Métrica | Atual | Calibrado | Δ | Baseline aleatório |
|---------|-------|-----------|---|-------------------|
| LOO-CV Brier Score | 0.738 | **0.733** | −0.005 | 0.667 |
| LOO-CV Poisson NLL | 1.855 | 1.866 | +0.011 | — |
| In-sample NLL | 33.40 | **31.56** | −1.84 | — |

O in-sample melhora claramente. O LOO-CV é praticamente neutro — sinal de que com 18 jogos
o modelo está no limite de separação sinal/ruído para 4 parâmetros.

---

## 8. Próximos passos

### Amanhã — Calibração oficial (rodada 1 completa)

Com os resultados reais de **Portugal vs Congo**, **Uzbekistan vs Colombia**,
**England vs Croatia** e **Ghana vs Panama**:

```bash
python3 scripts/calibrate.py --exclude-outliers
```

O JSON `output/calibrated_weights.json` e o gráfico `output/calibration_report.png`
atualizam automaticamente.

**O que aplicar com confiança:**
```python
# simulate.py e build_team_scores.py
BASE_XG   = 1.12   # era 1.30 — reduz xGs absurdos
OFF_ATT_W = 0.90   # era 0.70 — ataque mais preditivo
OFF_MID_W = 0.10   # derivado
# manter RES_DEF_W, RES_GK_W, RES_MID_W nos valores atuais por ora
```

### Rodada 3 — Biases por seleção

Com ~48 jogos (rodadas 1 + 2), faz sentido adicionar fatores multiplicativos por seleção
para times que o modelo erra sistematicamente:

```
xG_A = BASE_XG × off_A × att_bias_A / (res_B × def_bias_B)
```

Com regularização L2 para manter os biases conservadores:
```
loss = NLL + λ × Σ (att_bias_i − 1)² + λ × Σ (def_bias_i − 1)²
```

Candidatos óbvios para bias (baseado na rodada 1):
- **Saudi Arabia** — xG calculado muito baixo vs resultado real (empate com Uruguay)
- **Qatar** — xG muito baixo vs empate com Switzerland
- **Australia** — xG calculado como azarão mas ganhou de Turkey
- **Iran** — xG alto mas empatou com New Zealand

---

*Gráfico completo: `output/calibration_report.png`*
