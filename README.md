# WorldCup 2026 — Simulação Monte Carlo

Simulação completa da Copa do Mundo 2026 usando atributos de jogadores do FIFA 22 como proxy de força, xG derivado de Poisson para modelar partidas, e Monte Carlo para estimar probabilidades de título.

**Resultados (10.000 simulações):** França 20.7% · Portugal 15.1% · Argentina 10.1% · Brasil 8.8%

---

## 🏆 Nossa aposta — Seed 303

> **Holanda campeã.** Esta é a nossa aposta para a Copa 2026.

Na simulação determinística com seed `303`, a Holanda vence o torneio inteiro:
bate a França nas quartas, derrota a Espanha nas semis e conquista o título na final contra a Argentina.

```
QF   França     1–2   Holanda   ✓
SF   Holanda    3–0   Espanha   ✓
F    Holanda    2–0   Argentina 🏆
```

Relatório completo: [`output/JOGO_303.md`](output/JOGO_303.md)

Para rodar você mesmo:
```bash
python scripts/play_simulation.py 303
```

---

## Estrutura do projeto

```
WorldCup-2026/
├── squads/                          # Convocações das 48 seleções
│   └── <nacao>.json
├── datasets/
│   ├── extracted/players_22.csv    # FIFA 22 — atributos por jogador
│   └── readme.md
├── transfermarket/                  # Dataset TM 2025 (local, não versionado)
│   ├── players.csv
│   └── national_teams.csv
├── scripts/
│   ├── match_transfermarket.py      # Cruza squads com TM (gera market_value_by_nation.json)
│   ├── build_team_scores.py         # Calcula scores por setor (gera team_scores.json)
│   ├── simulate.py                  # Monte Carlo — roda N torneios completos
│   ├── trace_simulation.py          # Roda um torneio com bracket completo
│   └── generate_report.py          # Gera SIMULACAO.md com resultados atuais
├── output/
│   ├── market_value_by_nation.json  # Match TM por seleção (intermediário)
│   ├── team_scores.json             # Scores finais — input da simulação
│   └── simulation_results.json     # Resultado das N simulações Monte Carlo
└── SIMULACAO.md                     # Relatório completo com metodologia e resultados
```

---

## Como rodar

### Simulação (ponto de entrada principal)

```bash
python3 scripts/simulate.py 10000
```

Roda 10.000 torneios completos e imprime a tabela de probabilidades. Resultado salvo em `output/simulation_results.json`.

### Regenerar o relatório

```bash
python3 scripts/generate_report.py
```

Lê `output/simulation_results.json` e gera `SIMULACAO.md` com a tabela de probabilidades atualizada e 4 simulações de exemplo (aleatória, Brasil vence, França vence, azarão vence).

### Simulação individual com bracket completo

```bash
python3 scripts/trace_simulation.py                   # aleatória
python3 scripts/trace_simulation.py --champion brazil
python3 scripts/trace_simulation.py --champion france
python3 scripts/trace_simulation.py --dark-horse      # time fora do top-8 vence
```

---

## Pipeline de dados

```
squads/*.json
    │
    ▼
match_transfermarket.py              (requer transfermarket/ local)
    │  Fuzzy matching nome × TM, filtrado por pool nacional + cidadania
    ▼
output/market_value_by_nation.json
    │
    ▼
build_team_scores.py
    │  Tier 1: FIFA 22 (datasets/extracted/players_22.csv)
    │  Tier 2: Transfermarket market value → rating log-linear
    │  Tier 3: mediana global do setor
    │  Top-K por setor → log-mean → min-max normalização [0,1]
    ▼
output/team_scores.json
    │
    ▼
simulate.py  →  output/simulation_results.json
```

> O `match_transfermarket.py` requer o dataset TM localmente (`transfermarket/`).
> Os demais scripts rodam com o que já está versionado.

---

## Fórmula xG

```
offense_A    = 0.7 × attack_A    + 0.3 × midfield_A
resistance_B = 0.6 × defense_B  + 0.2 × goalkeeper_B + 0.2 × midfield_B

xG_A = 1.3 × (offense_A / resistance_B)   [máx 8.0, piso resistência 0.1]
```

Gols simulados via Poisson(xG). Empate no tempo normal → prorrogação (xG × 0.35) → pênaltis (50/50).

---

## Scores atuais (top 10)

| Seleção | xG vs médio | Ataque | Meio | Defesa | Goleiro |
|---------|------------|--------|------|--------|---------|
| França | 2.497 | 1.000 | 0.867 | 0.830 | 0.796 |
| Portugal | 2.108 | 0.765 | 0.916 | 0.934 | 0.699 |
| Argentina | 2.057 | 0.788 | 0.799 | 0.785 | 0.817 |
| Brasil | 1.928 | 0.761 | 0.696 | 0.848 | 0.979 |
| Senegal | 1.886 | 0.817 | 0.512 | 0.690 | 0.753 |
| Países Baixos | 1.885 | 0.680 | 0.829 | 1.000 | 0.376 |
| Espanha | 1.860 | 0.730 | 0.680 | 0.773 | 0.731 |
| Bélgica | 1.821 | 0.606 | 0.922 | 0.604 | 0.935 |
| Inglaterra | 1.821 | 0.669 | 0.774 | 0.890 | 0.720 |
| Colômbia | 1.748 | 0.625 | 0.782 | 0.605 | 0.591 |

Scores são relativos entre si (min-max). `1.0` = melhor do torneio naquele setor.

---

## Resultados — 10.000 simulações

| # | Seleção | Campeão | Finalista | Semi | QF |
|---|---------|---------|-----------|------|----|
| 1 | França | 20.7% | 32.4% | 48.7% | 71.4% |
| 2 | Portugal | 15.1% | 26.3% | 43.2% | 67.3% |
| 3 | Argentina | 10.1% | 19.3% | 35.4% | 60.5% |
| 4 | Brasil | 8.8% | 16.5% | 28.9% | 48.7% |
| 5 | Países Baixos | 8.0% | 15.6% | 26.9% | 50.4% |
| 6 | Inglaterra | 7.5% | 15.4% | 29.5% | 53.5% |
| 7 | Bélgica | 7.4% | 15.2% | 33.0% | 63.7% |
| 8 | Senegal | 5.1% | 11.7% | 24.0% | 43.0% |
| 9 | Espanha | 4.8% | 10.3% | 21.5% | 38.0% |
| 10 | Colômbia | 2.9% | 7.5% | 18.0% | 36.3% |

Para o relatório completo com metodologia e simulações individuais, veja [SIMULACAO.md](SIMULACAO.md).
