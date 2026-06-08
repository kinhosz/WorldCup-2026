# WorldCup 2026 — Simulação Monte Carlo

Simulação completa da Copa do Mundo 2026 usando atributos de jogadores do FC25 e FIFA22 como proxy de força, xG via Poisson, e Monte Carlo para estimar probabilidades de título.

**Resultados (1.000.000 simulações):** Brasil 20.8% · Portugal 17.1% · França 16.9% · Inglaterra 9.3% · Argentina 8.2%

---

## Documentos

| Documento | Conteúdo |
|-----------|----------|
| [SIMULACAO.md](SIMULACAO.md) | Metodologia completa, scores, resultados e simulações de exemplo |
| [ANALISE.md](ANALISE.md) | Análise profunda: bugs corrigidos, impacto do FC25, interpretação dos resultados |
| [output/score_audit.md](output/score_audit.md) | Breakdown por jogador — qual fonte de dados e rating foi usado em cada seleção |

---

## Como rodar

```bash
python3 scripts/build_team_scores.py   # gera output/team_scores.json
python3 scripts/simulate.py 100000     # roda 100k simulações
python3 scripts/generate_report.py     # gera SIMULACAO.md atualizado
```

---

## Pipeline

```
squads/*.json
    │
    ▼
build_team_scores.py
    │  Tier 1: FC25    (datasets/extracted/fc25_akshay/players_info.csv)
    │  Tier 2: FIFA22  (datasets/extracted/players_22.csv)
    │  Tier 3: Transfermarket market value → rating log-linear
    │  Tier 4: mediana global do setor
    ▼
output/team_scores.json  →  simulate.py  →  output/simulation_results.json
```

---

## Resultados — 1.000.000 simulações

| # | Seleção | Campeão | Finalista | Semi | QF |
|---|---------|---------|-----------|------|----|
| 1 | Brasil | 20.82% | 31.96% | 48.03% | 68.09% |
| 2 | Portugal | 17.09% | 28.49% | 49.87% | 71.28% |
| 3 | França | 16.89% | 30.04% | 44.63% | 65.29% |
| 4 | Inglaterra | 9.32% | 17.88% | 33.11% | 63.48% |
| 5 | Argentina | 8.18% | 15.79% | 31.93% | 55.64% |
| 6 | Países Baixos | 7.00% | 15.56% | 26.80% | 51.82% |
| 7 | Espanha | 6.95% | 15.45% | 32.05% | 47.38% |
| 8 | Colômbia | 3.45% | 9.45% | 23.71% | 41.85% |
| 9 | Alemanha | 3.24% | 8.23% | 16.60% | 31.81% |
| 10 | Bélgica | 2.65% | 8.63% | 24.26% | 58.66% |

Para análise completa: [ANALISE.md](ANALISE.md)
