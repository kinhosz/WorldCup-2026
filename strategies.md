# Estratégias de Modelo — Plano de Comparação

**Copa do Mundo 2026 — Mata-Mata**

Avaliadas com `python scripts/model_compare.py` contra os 72 jogos reais (R1+R2+R3).

---

## Sistema de Pontuação (RankScore)

Para cada jogo, o modelo calcula a distribuição Poisson completa e rankeia todos os placares possíveis. O placar real recebe:

| Posição na distribuição | Pontos |
|-------------------------|--------|
| Rank 1 (predição exata mais provável) | **+10** |
| Rank 2 | **+6** |
| Rank 3 | **+3** |
| Rank 4 ou 5 | **+1** |
| Rank 6+ e P(placar) ≥ 5% | **0** |
| Rank 6+ e P(placar) ∈ [2%, 5%) | **−2** |
| Rank 6+ e P(placar) < 2% | **−5** |

**RankScore total** = soma sobre os 72 jogos. Máximo teórico = 720 (acerta rank 1 sempre).

Métricas adicionais reportadas: Top1/Top3/Top5 (contagens), Penalidades, Acerto W/D/L (%), P% média do resultado correto, Rank médio do placar real, xG médio por time, NLL Poisson.

---

## Tabela de Estratégias

| ID | Modelo | Dados treino | Config | Arquivo |
|----|--------|-------------|--------|---------|
| **S01** | SA + att_only λ=1.5 | 48 jogos R1+R2 | Biases só ataque | `output/calibrated_weights_sa.json` ✅ |
| **S02** | L-BFGS-B | 48 jogos R1+R2 | Sem biases | `output/calibrated_weights.json` ✅ |
| **S03** | S01 + xG×1.20 | — | BASE_XG escalado | derivado de S01 ✅ |
| **S04** | S01 + xG×1.40 | — | BASE_XG escalado | derivado de S01 ✅ |
| **S05** | S01 + xG×1.60 | — | BASE_XG escalado | derivado de S01 ✅ |
| **S06** | S01 sem biases | — | biases removidos | derivado de S01 ✅ |
| **S07** | Default (sem calibração) | — | pesos originais | inline ✅ |
| **S08** | SA global sem biases | 72 jogos R1+R2+R3 | θ = 4 globais | `output/weights_s08.json` ⏳ |
| **S09** | SA + att_only λ=0.5 | 72 jogos | biases agressivos | `output/weights_s09.json` ⏳ |
| **S10** | SA + att_only λ=1.0 | 72 jogos | biases moderados | `output/weights_s10.json` ⏳ |
| **S11** | SA + att_only λ=1.5 | 72 jogos | mesmo setup de S01 | `output/weights_s11.json` ⏳ |
| **S12** | SA + att_only λ=2.5 | 72 jogos | biases conservadores | `output/weights_s12.json` ⏳ |
| **S13** | SA + biases att+def λ=1.0 | 72 jogos | biases completos | `output/weights_s13.json` ⏳ |
| **S14** | SA + biases att+def λ=2.0 | 72 jogos | biases completos | `output/weights_s14.json` ⏳ |
| **S15** | SA + biases att+def λ=3.0 | 72 jogos | alta regularização | `output/weights_s15.json` ⏳ |
| **S16** | SA + att_only λ=1.5 sem outliers | 72 jogos −Δ≥4 | remove 7–1, 6–0, etc. | `output/weights_s16.json` ⏳ |
| **S17** | SA + biases λ=2.0 sem outliers | 72 jogos −Δ≥4 | biases att+def | `output/weights_s17.json` ⏳ |
| **S18** | SA + att_only λ=1.0 sem outliers | 72 jogos −Δ≥4 | biases só ataque | `output/weights_s18.json` ⏳ |

✅ = disponível agora | ⏳ = precisa rodar calibração

---

## O que cada dimensão testa

### Dimensão 1 — Método de calibração (S01 vs S08–S12)
S08 (sem biases) é o baseline limpo. S09–S12 variam λ.
λ baixo → biases agressivos, melhor fit mas risco de overfitting.
λ alto → biases próximos de 1.0, mais suave, generaliza melhor.

**Hipótese:** com 72 jogos, o SA vai convergir para biases mais estáveis. O melhor λ deve estar em [1.0, 2.0].

### Dimensão 2 — att_only vs att+def biases (S10 vs S13)
att_only: 52 parâmetros para 144 observações (ratio 0.36) → ok.
att+def:  100 parâmetros para 144 observações (ratio 0.69) → precisa λ ≥ 2.0.
Com 72 jogos (vs 48), agora é mais seguro ativar def_bias.

**Hipótese:** S13/S14 vão capturar time como Marrocos (boa defesa, atacou pouco) que att_only não capta.

### Dimensão 3 — Outliers (S11 vs S16, S14 vs S17)
Jogos com Δ ≥ 4 gols: Germany 7–1 Curacao, Canada 6–0 Qatar, France 4–1 Iraq, etc.
Incluir: modelo aprende que existem goleadas. Excluir: modelo foca em jogos "normais".

**Hipótese:** no mata-mata com times completos, goleadas são raras. S16/S17/S18 podem generalizar melhor para esse contexto.

### Dimensão 4 — xG boost (S03–S05)
S01 tem BASE_XG=1.144, gerando muitos top-scores 0–0 / 1–0 / 0–1.
Média real dos jogos: verificar avg_xg na tabela de resultados.
S03–S05 forçam mais gols esperados → distribuição mais espalhada → menos dominância do 0–0.

**Hipótese:** se avg_xg real > 1.5, S04 (×1.4) deve performar melhor.

---

## Comandos de Calibração

Rodar da raiz do projeto (`/home/odoo/workspace/party/WorldCup-2026`):

```bash
# S08 — SA global, sem biases
python scripts/calibrate_sa.py --iters 500000 --restarts 5 --output output/weights_s08.json

# S09 — SA att_only, λ=0.5
python scripts/calibrate_sa.py --att-only --lambda 0.5 --iters 500000 --restarts 5 --output output/weights_s09.json

# S10 — SA att_only, λ=1.0
python scripts/calibrate_sa.py --att-only --lambda 1.0 --iters 500000 --restarts 5 --output output/weights_s10.json

# S11 — SA att_only, λ=1.5 (rerun com 72g)
python scripts/calibrate_sa.py --att-only --lambda 1.5 --iters 500000 --restarts 5 --output output/weights_s11.json

# S12 — SA att_only, λ=2.5
python scripts/calibrate_sa.py --att-only --lambda 2.5 --iters 500000 --restarts 5 --output output/weights_s12.json

# S13 — SA biases att+def, λ=1.0
python scripts/calibrate_sa.py --biases --lambda 1.0 --iters 500000 --restarts 5 --output output/weights_s13.json

# S14 — SA biases att+def, λ=2.0
python scripts/calibrate_sa.py --biases --lambda 2.0 --iters 500000 --restarts 5 --output output/weights_s14.json

# S15 — SA biases att+def, λ=3.0
python scripts/calibrate_sa.py --biases --lambda 3.0 --iters 500000 --restarts 5 --output output/weights_s15.json

# S16 — SA att_only λ=1.5, sem outliers
python scripts/calibrate_sa.py --att-only --lambda 1.5 --exclude-outliers --iters 500000 --restarts 5 --output output/weights_s16.json

# S17 — SA biases λ=2.0, sem outliers
python scripts/calibrate_sa.py --biases --lambda 2.0 --exclude-outliers --iters 500000 --restarts 5 --output output/weights_s17.json

# S18 — SA att_only λ=1.0, sem outliers
python scripts/calibrate_sa.py --att-only --lambda 1.0 --exclude-outliers --iters 500000 --restarts 5 --output output/weights_s18.json
```

Ou rodar tudo de uma vez (sequencial, ~20–30 min):
```bash
python scripts/model_compare.py --calibrate
```

---

## Como usar

```bash
# Avalia modelos já disponíveis (S01–S07)
python scripts/model_compare.py

# Roda calibrações pendentes e avalia tudo
python scripts/model_compare.py --calibrate

# Salva resultado em output/model_comparison.md
python scripts/model_compare.py --save

# Mostra detalhes jogo a jogo para um modelo específico
python scripts/model_compare.py --verbose S01

# Tudo junto
python scripts/model_compare.py --calibrate --save
```

---

## Notas sobre mata-mata

- Sem rotação de jogadores → times jogam com força total → outliers menos prováveis (favorece S16–S18)
- Sem necessidade de poupar para a próxima rodada → xG deve subir em relação à fase de grupos
- Pênaltis são 50/50 no modelo atual (OK para mata-mata)
- O modelo vencedor será aplicado como novo `calibrated_weights_sa.json` antes da R32

---

## Decisão final

Após rodar `model_compare.py --calibrate --save`, escolher o modelo com:
1. **Maior RankScore** (critério principal)
2. Maior Top3 (acertou o placar exato no top-3)
3. Menor número de Penalidades (não foi pego de surpresa)
4. AvgXG próximo de 1.3–1.6 (realista para mata-mata)

O vencedor vira o novo `calibrated_weights_sa.json`.
