#!/usr/bin/env python3
"""
Generate SIMULACAO.md from existing simulation results + fresh trace examples.

Requires:
    output/team_scores.json        (run scripts/build_team_scores.py first)
    output/simulation_results.json (run scripts/simulate.py first)

Usage:
    python3 scripts/simulate.py 10000
    python3 scripts/generate_report.py
"""

import json
import os
import sys
from datetime import date

# Allow importing from the same directory
sys.path.insert(0, os.path.dirname(__file__))

from trace_simulation import (
    GROUPS, ROUND32, ROUND16, QUARTERFINALS, SEMIFINALS, FINAL_ID,
    DISPLAY_NAMES, _GROUP_OF, _name, simulate_tournament_traced,
    format_trace, run_until, FAMOUS,
)


# ── Load data ──────────────────────────────────────────────────────────────────

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ── Static sections ────────────────────────────────────────────────────────────

HEADER = """\
# Copa do Mundo 2026 — Simulação Monte Carlo

**Data:** {today}
**Simulações realizadas:** {n_sims:,}
**Seed:** aleatória (resultados variam a cada execução)

---

## 1. O que fizemos

Construímos um simulador da Copa do Mundo 2026 capaz de jogar um torneio completo — fase de grupos, oitavas, round of 16, quartas, semis e final — usando dados reais dos jogadores convocados como base para calcular a força de cada seleção.

O objetivo foi estimar probabilidades de título para cada um dos 48 países, levando em conta o chaveamento oficial da FIFA, a regra dos melhores 8 terceiros colocados e os detalhes do bracket de mata-mata.

---

## 2. Pipeline de dados

### 2.1 Fonte dos scores

Para cada seleção, calculamos um score em quatro setores: **goleiro**, **defesa**, **meio-campo** e **ataque**. A estratégia em cascata foi:

| Tier | Fonte | Cobertura |
|------|-------|-----------|
| 1° | **FIFA 22** — atributos por setor | ~80% dos jogadores |
| 2° | **Transfermarket** — valor de mercado convertido para rating | complemento |
| 3° | **Mediana global do setor** | jogadores sem dados em nenhuma fonte |

A conversão de valor de mercado para rating usa uma fórmula log-linear calibrada nos extremos:
- €1M → 65 pontos
- €180M → 91 pontos

### 2.2 Atributos FIFA 22 por setor

| Setor | Atributos usados |
|-------|-----------------|
| Goleiro | `goalkeeping_diving`, `goalkeeping_reflexes`, `goalkeeping_handling`, `goalkeeping_positioning` |
| Defesa | `defending`, `physic` |
| Meio | `passing`, `dribbling` |
| Ataque | `shooting`, `pace` |

### 2.3 Top-K por setor

Para cada setor, pegamos os **K melhores jogadores** (por rating) e calculamos a média geométrica (log-mean):

| Setor | K |
|-------|---|
| Goleiro | 1 |
| Defesa | 4 |
| Meio | 4 |
| Ataque | 3 |

Os scores brutos são então normalizados com **min-max** entre as 48 seleções → intervalo [0, 1].

### 2.4 Matching de nomes

O matching entre nomes dos arquivos de convocação e os datasets (FIFA 22 / TM) usa:
- `SequenceMatcher` (ratio de similaridade de strings)
- Token overlap (interseção de palavras)
- Filtro por nacionalidade (pool da seleção nacional + cidadania)
- Strip de sufixos como *Junior*, *Sr*, *Jr*
- Threshold mínimo de 0.72

---

## 3. Fórmula xG

Para um confronto **A × B**, o xG (gols esperados) de cada time é:

```
offense_A    = 0.7 × attack_A    + 0.3 × midfield_A
resistance_B = 0.6 × defense_B  + 0.2 × goalkeeper_B + 0.2 × midfield_B

xG_A = 1.3 × (offense_A / resistance_B)
```

Constantes de segurança:
- `BASE_XG = 1.3` — média histórica de gols por time por jogo em Copas
- `RES_FLOOR = 0.10` — piso da resistência (evita divisão por zero)
- `MAX_XG = 8.0` — teto dos gols esperados

---

## 4. Estrutura da simulação

### Fase de grupos
- 12 grupos de 4 times (A–L), round-robin
- Pontuação: vitória=3, empate=1, derrota=0
- Classificam: 1º e 2º de cada grupo (24 times) + 8 melhores terceiros
- Gols simulados via distribuição de Poisson com o xG calculado
- Critérios de desempate: pontos → saldo de gols → gols pró → vitórias → aleatório

### Mata-mata
- **Round of 32** → Round of 16 → Quartas → Semis → Final
- Bracket oficial da FIFA (partidas 73–104)
- Empate no tempo normal → prorrogação (30 min, xG × 0.35) → pênaltis (50/50)
- Atribuição dos slots de 3°s colocados via backtracking com as restrições oficiais de grupos elegíveis

### Execução
```bash
python3 scripts/build_team_scores.py   # gera output/team_scores.json
python3 scripts/simulate.py 10000      # roda 10k simulações
python3 scripts/generate_report.py     # gera este documento
```

---
"""

FOOTER = """\

## 8. Limitações e próximos passos

### Limitações atuais

| Limitação | Impacto |
|-----------|---------|
| Cobertura irregular no FIFA 22 (Jordan 1 jogador, Qatar 0) | Times com muita mediana fallback têm scores menos confiáveis |
| Pênaltis como 50/50 puro | Não reflete histórico de pênaltis por seleção |
| `BASE_XG = 1.3` fixo para todos | Não captura estilos de jogo (defensivo vs ofensivo) |
| Lesões/suspensões não modeladas | Todos os convocados sempre disponíveis |
| Forma recente não considerada | Scores baseados apenas em atributos estáticos |

### Próximos passos potenciais

1. **FC25 como Tier 1** — dataset do EA FC 25 (~18k jogadores, cobertura global) já disponível em `datasets/extracted/`, basta plugar no pipeline e substituir FIFA 22. Resolveria a cobertura deficiente de Jordan, Qatar, etc.
2. **Pênaltis ponderados** — incorporar histórico de pênaltis por seleção em Copas anteriores
3. **Forma recente** — multiplicador baseado no ranking FIFA atual
4. **Variância de home advantage** — pequeno boost para times anfitriões (EUA, Canadá, México)
"""


# ── Dynamic sections ───────────────────────────────────────────────────────────

def section_scores(scores, top_n=13):
    lines = ["## 5. Scores atuais das seleções", ""]
    lines.append("| Seleção | xG vs médio | Ataque | Meio | Defesa | Goleiro |")
    lines.append("|---------|------------|--------|------|--------|---------|")
    ranked = sorted(scores.items(), key=lambda x: -x[1].get('xg_vs_average_opponent', 0))
    for team, s in ranked[:top_n]:
        lines.append(
            f"| {_name(team)} "
            f"| {s.get('xg_vs_average_opponent', 0):.3f} "
            f"| {s.get('attack', 0):.3f} "
            f"| {s.get('midfield', 0):.3f} "
            f"| {s.get('defense', 0):.3f} "
            f"| {s.get('goalkeeper', 0):.3f} |"
        )
    return "\n".join(lines)


def section_results(sim_results, n_sims, top_n=20):
    lines = [f"## 6. Resultados — {n_sims:,} simulações", ""]
    lines.append("| # | Seleção | Grupo | Campeão | Finalista | Semi | QF | R16 |")
    lines.append("|---|---------|-------|---------|-----------|------|----|-----|")

    ranked = sorted(sim_results.items(), key=lambda x: -x[1]['champion_pct'])
    for i, (team, s) in enumerate(ranked[:top_n], 1):
        g = _GROUP_OF.get(team, '?')
        lines.append(
            f"| {i} | {_name(team)} | {g} "
            f"| {s['champion_pct']:.1f}% "
            f"| {s['finalist_pct']:.1f}% "
            f"| {s['semifinalist_pct']:.1f}% "
            f"| {s['quarterfinalist_pct']:.1f}% "
            f"| {s['r16_pct']:.1f}% |"
        )

    lines += ["", "### Classificação por grupo (R32)", ""]
    lines.append("| Grupo | 1° aprox. | 2° aprox. | 3° aprox. | 4° aprox. |")
    lines.append("|-------|-----------|-----------|-----------|-----------|")
    for letter in sorted(GROUPS):
        teams = GROUPS[letter]
        by_r32 = sorted(teams, key=lambda t: -sim_results.get(t, {}).get('r32_pct', 0))
        cells = " | ".join(f"{_name(t)} {sim_results.get(t,{}).get('r32_pct',0):.0f}%" for t in by_r32)
        lines.append(f"| {letter} | {cells} |")

    return "\n".join(lines)


def section_traces(scores):
    lines = ["## 7. Simulações individuais", ""]
    lines.append("Quatro exemplos de torneios completos rodados individualmente.")
    lines.append("O vencedor de cada partida está em **negrito**. Placar sempre mandante–visitante.")
    lines.append("")

    configs = [
        ("7.1 Simulação aleatória", None,        False, ""),
        ("7.2 Brasil campeão 🇧🇷",   "brazil",    False, ""),
        ("7.3 França campeã 🇫🇷",    "france",    False, ""),
        ("7.4 Azarão campeão",        None,        True,  ""),
    ]

    for title, champion, dark_horse, _ in configs:
        lines.append(f"---\n\n### {title}\n")
        print(f"  Rodando trace: {title}...", file=sys.stderr)

        if dark_horse:
            result = run_until(scores, lambda c: c not in FAMOUS)
        elif champion:
            result = run_until(scores, lambda c: c == champion)
        else:
            result = simulate_tournament_traced(scores)

        champ = result['champion']
        lines.append(f"**Campeão: {_name(champ)}**\n")
        lines.append(format_trace(result, scores))

    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    scores_path = "output/team_scores.json"
    results_path = "output/simulation_results.json"

    for p in (scores_path, results_path):
        if not os.path.exists(p):
            sys.exit(f"Arquivo não encontrado: {p}\nRode primeiro: python3 scripts/simulate.py")

    print("Carregando dados...", file=sys.stderr)
    scores = load_json(scores_path)
    sim_data = load_json(results_path)

    n_sims = sim_data.get('n_simulations', 10000)
    sim_results = sim_data['results']

    print("Gerando seções estáticas...", file=sys.stderr)
    header = HEADER.format(today=date.today().strftime("%d/%m/%Y"), n_sims=n_sims)

    print("Gerando tabela de scores...", file=sys.stderr)
    scores_section = section_scores(scores)

    print("Gerando tabela de resultados...", file=sys.stderr)
    results_section = section_results(sim_results, n_sims)

    print("Rodando 4 simulações de exemplo...", file=sys.stderr)
    traces_section = section_traces(scores)

    doc = "\n\n---\n\n".join([
        header.rstrip(),
        scores_section,
        results_section,
        traces_section,
        FOOTER.strip(),
    ])

    out_path = "SIMULACAO.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc + "\n")

    print(f"\nDocumento gerado: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
