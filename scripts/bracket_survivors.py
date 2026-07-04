#!/usr/bin/env python3
"""
Side quest: filtro de "linhas sobreviventes" do mata-mata real (R32 -> Final).

Ideia: simula o bracket real (output/r32_bracket.json) do zero N vezes com o
Model4 — SEM plugar os resultados reais já conhecidos, ou seja, cada linha é
um universo independente. Depois filtra e descarta toda linha cujo vencedor
de algum jogo do R32 já decidido na vida real não bate com o resultado real.
O que sobra mostra o que essas linhas "compatíveis com a realidade" apostam
pro resto do bracket (jogos pendentes do R32, R16, QF, SF e campeão).

Nota estatística: como cada partida é um sorteio de Poisson independente,
esse filtro não muda a probabilidade de jogos entre times que não jogaram
ainda (são estatisticamente independentes dos jogos já decididos). O ganho
real é (1) a distribuição condicional do resto do bracket dado o que já
aconteceu — equivalente (por rejection sampling) ao que simulate.py já faz
plugando os resultados reais direto — e (2) a fração de sobreviventes serve
como "índice de surpresa": quão raro foi, segundo o modelo, a sequência real
observada até agora.

Uso:
    python scripts/bracket_survivors.py [N_SIMULACOES]

Default: 1.000.000 simulações. Resultado salvo em
output/bracket_survivors.json (só as linhas sobreviventes + estatísticas
agregadas — as descartadas não são persistidas).
"""

import json
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from simulate import compute_xg, DISPLAY_NAMES  # noqa: E402  (reusa Model4)

ROOT = os.path.join(os.path.dirname(__file__), "..")


def _name(t):
    return DISPLAY_NAMES.get(t, t.replace("_", " ").title())


with open(os.path.join(ROOT, "output", "team_scores.json"), encoding="utf-8") as f:
    SCORES = json.load(f)

with open(os.path.join(ROOT, "output", "r32_bracket.json"), encoding="utf-8") as f:
    BRACKET = json.load(f)

with open(os.path.join(ROOT, "output", "copa_real_state.json"), encoding="utf-8") as f:
    REAL_KNOCKOUT = json.load(f)["knockout_results"]

# ── Estrutura do bracket real (fixa) ──────────────────────────────────────
R32_MATCHES = {m["id"]: (m["home"], m["away"]) for m in BRACKET["matches"]}
R16_PAIRS = {p["r16_id"]: tuple(p["r32_ids"]) for p in BRACKET["r16_pairs"]}
QF_PAIRS = {1: (1, 2), 2: (3, 4), 3: (5, 6), 4: (7, 8)}
SF_PAIRS = {1: (1, 2), 2: (3, 4)}

# gid do jogo de R32 na numeração do resultado.py/copa_real_state.json = 72 + id
KNOWN_WINNERS = {}
for rid in R32_MATCHES:
    gid = str(72 + rid)
    if gid in REAL_KNOCKOUT:
        KNOWN_WINNERS[rid] = REAL_KNOCKOUT[gid]["winner"]

# xG dos jogos de R32 é fixo (times já conhecidos) — pré-computa uma vez
R32_XG = {rid: compute_xg(SCORES[ta], SCORES[tb], ta, tb) for rid, (ta, tb) in R32_MATCHES.items()}

# compute_xg é determinístico (só depende de scores/biases) — cacheia entre
# simulações pra evitar recalcular a mesma dupla de times milhares de vezes.
_XG_CACHE = {}


def _cached_xg(ta, tb):
    key = (ta, tb)
    xg = _XG_CACHE.get(key)
    if xg is None:
        xg = compute_xg(SCORES[ta], SCORES[tb], ta, tb)
        _XG_CACHE[key] = xg
    return xg


def play(ta, tb, xg=None):
    """Simula um jogo de mata-mata. Retorna (vencedor, ga, gb, nota)."""
    xg_a, xg_b = xg if xg is not None else _cached_xg(ta, tb)
    ga = int(np.random.poisson(xg_a))
    gb = int(np.random.poisson(xg_b))
    if ga != gb:
        return (ta if ga > gb else tb), ga, gb, "90'"
    # empate -> prorrogação + pênaltis: 50/50 (mesma regra do simulate.py)
    winner = ta if random.random() < 0.5 else tb
    return winner, ga, gb, "PEN"


def simulate_line():
    r32_w, r32_score = {}, {}
    for rid, (ta, tb) in R32_MATCHES.items():
        w, ga, gb, note = play(ta, tb, xg=R32_XG[rid])
        r32_w[rid] = w
        r32_score[rid] = (ga, gb, note)

    r16_w = {}
    for gid, (a, b) in R16_PAIRS.items():
        w, ga, gb, note = play(r32_w[a], r32_w[b])
        r16_w[gid] = w

    qf_w = {}
    for gid, (a, b) in QF_PAIRS.items():
        w, ga, gb, note = play(r16_w[a], r16_w[b])
        qf_w[gid] = w

    sf_w = {}
    for gid, (a, b) in SF_PAIRS.items():
        w, ga, gb, note = play(qf_w[a], qf_w[b])
        sf_w[gid] = w

    champion, ga, gb, note = play(sf_w[1], sf_w[2])

    return {"r32": r32_w, "r32_score": r32_score, "r16": r16_w, "qf": qf_w, "sf": sf_w, "champion": champion}


def matches_reality(line):
    return all(line["r32"][rid] == w for rid, w in KNOWN_WINNERS.items())


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000

    print(f"Jogos do R32 já decididos na vida real: {len(KNOWN_WINNERS)}/16")
    for rid, w in sorted(KNOWN_WINNERS.items()):
        ta, tb = R32_MATCHES[rid]
        print(f"  #{rid:>2}  {_name(ta):<22} vs {_name(tb):<22}  ->  {_name(w)}")
    print(f"\nSimulando {n:,} linhas (R32 -> Final, sem plugar dados reais)...")

    survivors = []
    for i in range(n):
        if i % 50_000 == 0 and i > 0:
            print(f"  {i:>9,} / {n:,}  ({len(survivors):,} sobreviventes até aqui)", end="\r", flush=True)
        line = simulate_line()
        if matches_reality(line):
            survivors.append(line)

    n_surv = len(survivors)
    print(f"\n\nSobreviventes: {n_surv:,} / {n:,}  ({n_surv / n * 100:.4f}%)")
    if n_surv == 0:
        print("Nenhuma linha bateu com a realidade — aumente N.")
        return

    def pct_table(stage_key, ids_universe):
        table = {}
        for gid in ids_universe:
            counts = {}
            for line in survivors:
                w = line[stage_key][gid] if gid in line[stage_key] else None
                if w is None:
                    continue
                counts[w] = counts.get(w, 0) + 1
            table[gid] = {t: round(c / n_surv * 100, 2) for t, c in sorted(counts.items(), key=lambda x: -x[1])}
        return table

    pending_r32 = [rid for rid in R32_MATCHES if rid not in KNOWN_WINNERS]

    r32_pending_probs = pct_table("r32", pending_r32)
    r16_probs = pct_table("r16", R16_PAIRS.keys())
    qf_probs = pct_table("qf", QF_PAIRS.keys())
    sf_probs = pct_table("sf", SF_PAIRS.keys())

    champ_counts = {}
    for line in survivors:
        champ_counts[line["champion"]] = champ_counts.get(line["champion"], 0) + 1
    champ_probs = {t: round(c / n_surv * 100, 2) for t, c in sorted(champ_counts.items(), key=lambda x: -x[1])}

    print("\nJogos do R32 ainda pendentes — probabilidade entre as sobreviventes:")
    for rid in pending_r32:
        ta, tb = R32_MATCHES[rid]
        probs = r32_pending_probs[rid]
        print(f"  #{rid:>2}  {_name(ta):<22} vs {_name(tb):<22}  ->  " +
              "  ".join(f"{_name(t)} {p:.1f}%" for t, p in probs.items()))

    print("\nCampeão — top 10 entre as sobreviventes:")
    for t, p in list(champ_probs.items())[:10]:
        print(f"  {_name(t):<22} {p:.2f}%")

    out = {
        "n_simulations": n,
        "n_survivors": n_surv,
        "survival_rate_pct": round(n_surv / n * 100, 4),
        "known_r32_winners": {str(rid): w for rid, w in KNOWN_WINNERS.items()},
        "pending_r32_probs": {str(k): v for k, v in r32_pending_probs.items()},
        "r16_probs": {str(k): v for k, v in r16_probs.items()},
        "qf_probs": {str(k): v for k, v in qf_probs.items()},
        "sf_probs": {str(k): v for k, v in sf_probs.items()},
        "champion_probs": champ_probs,
        "sample_survivor_lines": [
            {
                "r32_scores": {str(rid): sc for rid, sc in line["r32_score"].items()},
                "r16": {str(k): v for k, v in line["r16"].items()},
                "qf": {str(k): v for k, v in line["qf"].items()},
                "sf": {str(k): v for k, v in line["sf"].items()},
                "champion": line["champion"],
            }
            for line in survivors[:50]
        ],
    }
    out_path = os.path.join(ROOT, "output", "bracket_survivors.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nSalvo em {out_path} ({n_surv:,} sobreviventes, amostra de 50 linhas completas).")


if __name__ == "__main__":
    main()
