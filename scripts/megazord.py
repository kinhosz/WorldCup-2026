#!/usr/bin/env python3
"""
megazord.py — "Bracket Consenso" da Copa do Mundo 2026.

Para cada jogo, encontra a MODA dos resultados em N simulações Monte Carlo
e constrói um único torneio determinístico seguindo os desfechos mais prováveis.

Uso:
    python scripts/megazord.py [N_SIMS]
    python scripts/megazord.py 50000   (padrão)

Saída: output/megazord_report.md
"""

import json
import os
import random
import sys
import time
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from simulate import (
    GROUPS, ROUND32, ROUND16, QUARTERFINALS, SEMIFINALS, FINAL_ID,
    THIRD_PLACE_SLOTS, ET_FACTOR, BASE_XG, RES_FLOOR, MAX_XG,
    compute_xg, sim_group_match, _assign_thirds, DISPLAY_NAMES,
)

SCORES_PATH = "output/team_scores.json"
OUT_PATH    = "output/megazord_report.md"
K_KO        = 10_000  # sub-simulações por jogo de mata-mata


def _name(team):
    return DISPLAY_NAMES.get(team, team.replace('_', ' ').title())


def load_scores():
    with open(SCORES_PATH, encoding='utf-8') as f:
        return json.load(f)


# ─── Fase 1: Coletar distribuições da fase de grupos ─────────────────────────

def collect_groups(scores, n, seed=2026):
    """
    Roda N simulações da fase de grupos, coletando:
      rank_ctr[g]        : Counter de tuplas (1°,2°,3°,4°)
      match_ctr[g][(a,b)]: Counter de (ga,gb), canônico a < b alfabeticamente
      third_stat[g][team]: lista de (pts,gd,gf,wins) quando team fica em 3°
    """
    random.seed(seed)
    np.random.seed(seed % (2 ** 32))

    rank_ctr   = {g: Counter() for g in GROUPS}
    match_ctr  = {g: {} for g in GROUPS}
    third_stat = {g: defaultdict(list) for g in GROUPS}

    for g, teams in GROUPS.items():
        for a, b in combinations(sorted(teams), 2):
            match_ctr[g][(a, b)] = Counter()

    t0 = time.time()
    for i in range(n):
        if i % 5000 == 0 and i:
            elapsed = time.time() - t0
            print(f"  grupos: {i:,}/{n:,}  ({elapsed:.1f}s)", end='\r', flush=True)

        for g, teams in GROUPS.items():
            st = {t: {'pts': 0, 'gd': 0, 'gf': 0, 'wins': 0} for t in teams}

            for a, b in combinations(sorted(teams), 2):
                ga, gb = sim_group_match(a, b, scores)
                match_ctr[g][(a, b)][(ga, gb)] += 1
                st[a]['gf'] += ga;  st[b]['gf'] += gb
                st[a]['gd'] += ga - gb;  st[b]['gd'] += gb - ga
                if ga > gb:
                    st[a]['pts'] += 3;  st[a]['wins'] += 1
                elif gb > ga:
                    st[b]['pts'] += 3;  st[b]['wins'] += 1
                else:
                    st[a]['pts'] += 1;  st[b]['pts'] += 1

            ranked = sorted(
                teams,
                key=lambda t: (-st[t]['pts'], -st[t]['gd'],
                               -st[t]['gf'], -st[t]['wins'], random.random()),
            )
            rank_ctr[g][tuple(ranked)] += 1
            s3 = st[ranked[2]]
            third_stat[g][ranked[2]].append((s3['pts'], s3['gd'], s3['gf'], s3['wins']))

    elapsed = time.time() - t0
    print(f"  grupos: {n:,}/{n:,}  concluído em {elapsed:.1f}s          ")
    return rank_ctr, match_ctr, third_stat


# ─── Fase 2: Derivar moda dos grupos ─────────────────────────────────────────

def modal_groups(rank_ctr, match_ctr):
    """
    Retorna:
      order[g]   = [1°, 2°, 3°, 4°]        (moda do ranking completo)
      mscores[g] = {(a,b): (ga,gb)}          (placar mais frequente)
      stats[g]   = {team: {pts,gd,gf,wins}}  (calculado a partir dos placares modais)
      freq[g]    = frequência da moda (0–1)
    """
    order   = {}
    mscores = {}
    stats   = {}
    freq    = {}

    for g, teams in GROUPS.items():
        top, cnt = rank_ctr[g].most_common(1)[0]
        order[g] = list(top)
        freq[g]  = cnt / sum(rank_ctr[g].values())

        mscores[g] = {}
        st = {t: {'pts': 0, 'gd': 0, 'gf': 0, 'wins': 0} for t in teams}
        for (a, b), ctr in match_ctr[g].items():
            ga, gb = ctr.most_common(1)[0][0]
            mscores[g][(a, b)] = (ga, gb)
            st[a]['gf'] += ga;  st[b]['gf'] += gb
            st[a]['gd'] += ga - gb;  st[b]['gd'] += gb - ga
            if ga > gb:
                st[a]['pts'] += 3;  st[a]['wins'] += 1
            elif gb > ga:
                st[b]['pts'] += 3;  st[b]['wins'] += 1
            else:
                st[a]['pts'] += 1;  st[b]['pts'] += 1
        stats[g] = st

    return order, mscores, stats, freq


def best_thirds(order, stats):
    """
    Para cada grupo, pega o 3° colocado modal e usa as estatísticas
    derivadas diretamente dos placares modais (não médias).
    Retorna lista completa de 12 times, ordenada do melhor ao pior.
    """
    thirds = []
    for g, ranking in order.items():
        team = ranking[2]
        s    = stats[g][team]
        thirds.append((g, team, s['pts'], s['gd'], s['gf'], s['wins']))

    return sorted(thirds, key=lambda x: (-x[2], -x[3], -x[4], -x[5]))


# ─── Fase 3: Simular partidas de mata-mata pela moda ─────────────────────────

def modal_ko(ta, tb, scores, k=K_KO, seed_off=0):
    """
    Roda K simulações de um jogo de mata-mata.
    Retorna (vencedor, ga, gb, método, win_pct) onde ga/gb é o placar modal
    *condicionado* ao vencedor modal vencer.
    """
    random.seed(2026 + seed_off)
    np.random.seed((2026 + seed_off) % (2 ** 32))

    xg_a, xg_b = compute_xg(scores[ta], scores[tb])
    outcomes    = Counter()

    for _ in range(k):
        ga = int(np.random.poisson(xg_a))
        gb = int(np.random.poisson(xg_b))
        if ga != gb:
            outcomes[(ta if ga > gb else tb, ga, gb, "90'")] += 1
        else:
            ea = int(np.random.poisson(xg_a * ET_FACTOR))
            eb = int(np.random.poisson(xg_b * ET_FACTOR))
            if ea != eb:
                w = ta if ea > eb else tb
                outcomes[(w, ga + ea, gb + eb, "AET")] += 1
            else:
                w = ta if random.random() < 0.5 else tb
                outcomes[(w, ga, gb, "PEN")] += 1

    win_cnt = Counter()
    for (w, *_), cnt in outcomes.items():
        win_cnt[w] += cnt

    winner  = win_cnt.most_common(1)[0][0]
    win_pct = win_cnt[winner] / k * 100

    # Placar modal condicionado ao vencedor modal
    winner_oc           = Counter({key: v for key, v in outcomes.items() if key[0] == winner})
    (_, ga_m, gb_m, meth), _ = winner_oc.most_common(1)[0]

    return winner, ga_m, gb_m, meth, win_pct


# ─── Fase 4: Montar o bracket completo ───────────────────────────────────────

def build_bracket(order, thirds_ranked, scores):
    """
    Monta e simula todo o mata-mata com os resultados modais.
    Retorna (match_results, winners) onde:
      match_results[mid] = {home, away, winner, loser, ga, gb, method, win_pct}
      winners[mid]       = equipe vencedora
    """
    qualifying     = [(g, t) for g, t, *_ in thirds_ranked[:8]]
    third_slot_map = _assign_thirds(qualifying)

    match_teams = {}
    for mid, spec1, spec2 in ROUND32:
        def resolve(spec, mid=mid):
            kind, val = spec
            if kind == '1':   return order[val][0]
            if kind == '2':   return order[val][1]
            return third_slot_map.get(mid)
        match_teams[mid] = (resolve(spec1), resolve(spec2))

    match_results = {}
    winners       = {}

    rounds_info = [
        ("Oitavas (R32)", ROUND32, lambda mid, *_: None),
        ("Round of 16",   ROUND16, None),
        ("Quartas",       QUARTERFINALS, None),
        ("Semifinais",    SEMIFINALS, None),
    ]

    def play(mid, seed_off):
        ta, tb = match_teams[mid]
        w, ga, gb, meth, pct = modal_ko(ta, tb, scores, seed_off=seed_off)
        winners[mid] = w
        match_results[mid] = {
            'home': ta, 'away': tb, 'winner': w,
            'loser': tb if w == ta else ta,
            'ga': ga, 'gb': gb, 'method': meth, 'win_pct': pct,
        }

    total_ko = len(ROUND32) + len(ROUND16) + len(QUARTERFINALS) + len(SEMIFINALS) + 1
    done     = 0

    for mid, _, _ in ROUND32:
        play(mid, seed_off=mid)
        done += 1
        print(f"  mata-mata: {done}/{total_ko}", end='\r', flush=True)

    for mid, src1, src2 in ROUND16:
        match_teams[mid] = (winners[src1], winners[src2])
        play(mid, seed_off=mid)
        done += 1
        print(f"  mata-mata: {done}/{total_ko}", end='\r', flush=True)

    for mid, src1, src2 in QUARTERFINALS:
        match_teams[mid] = (winners[src1], winners[src2])
        play(mid, seed_off=mid)
        done += 1
        print(f"  mata-mata: {done}/{total_ko}", end='\r', flush=True)

    for mid, src1, src2 in SEMIFINALS:
        match_teams[mid] = (winners[src1], winners[src2])
        play(mid, seed_off=mid)
        done += 1
        print(f"  mata-mata: {done}/{total_ko}", end='\r', flush=True)

    match_teams[FINAL_ID] = (winners[SEMIFINALS[0][0]], winners[SEMIFINALS[1][0]])
    play(FINAL_ID, seed_off=FINAL_ID)
    done += 1
    print(f"  mata-mata: {done}/{total_ko}  ✓          ")

    return match_results, winners, qualifying


# ─── Fase 5: Gerar relatório Markdown ────────────────────────────────────────

def format_score(r):
    ga, gb = r['ga'], r['gb']
    if r['method'] == 'PEN':
        return f"{ga}–{gb} pen."
    if r['method'] == 'AET':
        return f"{ga}–{gb} (AET)"
    return f"{ga}–{gb}"


def generate_report(order, mscores, stats, freq,
                    thirds_ranked, qualifying, match_results, winners, n_sims):
    lines = []
    nl    = lines.append
    qual_groups = {g for g, _ in qualifying}

    nl("# MEGAZORD — Bracket Consenso Copa do Mundo 2026")
    nl("")
    nl(f"*Baseado em {n_sims:,} simulações Monte Carlo.*  ")
    nl("*Fase de grupos: ranking + placares mais frequentes (moda) em cada jogo.*  ")
    nl(f"*Mata-mata: vencedor modal de {K_KO:,} sub-simulações por partida.*")
    nl("")
    nl("---")
    nl("")

    # ── Fase de grupos ───────────────────────────────────────────────────
    nl("## FASE DE GRUPOS")
    nl("")

    for g in sorted(GROUPS):
        ranked = order[g]
        st     = stats[g]
        nl(f"### Grupo {g}")
        nl("")
        nl(f"*Classificação modal: ocorre em **{freq[g]*100:.1f}%** das simulações*")
        nl("")
        nl("| # | Seleção | Pts | GD | GP | |")
        nl("|---|---------|-----|----|----|---|")
        for pos, team in enumerate(ranked, 1):
            s = st[team]
            if pos == 1:
                clf = "→ R32 (1°)"
            elif pos == 2:
                clf = "→ R32 (2°)"
            elif pos == 3:
                clf = f"→ R32 (3°?)" if g in qual_groups else "✗"
            else:
                clf = "✗"
            nl(f"| {pos} | **{_name(team)}** | {s['pts']} | {s['gd']:+d} | {s['gf']} | {clf} |")
        nl("")
        nl("**Placares modais:**")
        nl("")
        for (a, b), (ga, gb) in sorted(mscores[g].items()):
            if ga > gb:
                line = f"- **{_name(a)}** {ga}–{gb} {_name(b)}"
            elif gb > ga:
                line = f"- {_name(a)} {ga}–{gb} **{_name(b)}**"
            else:
                line = f"- {_name(a)} {ga}–{gb} {_name(b)}  *(empate)*"
            nl(line)
        nl("")

    # ── 8 melhores terceiros ──────────────────────────────────────────────
    nl("---")
    nl("")
    nl("## 8 MELHORES TERCEIROS LUGARES CLASSIFICADOS")
    nl("")
    nl("| # | Seleção | Grupo | Pts | GD | GF |")
    nl("|---|---------|-------|-----|----|----|")
    for rank, (g, team, pts, gd, gf, _) in enumerate(thirds_ranked[:8], 1):
        nl(f"| {rank} | **{_name(team)}** | {g} | {pts} | {gd:+d} | {gf} |")
    nl("")
    nl("*(Estatísticas derivadas dos placares modais da fase de grupos)*")
    nl("")

    # ── Mata-mata ─────────────────────────────────────────────────────────
    def fmt_round(round_ids, title):
        nl("---")
        nl("")
        nl(f"## {title}")
        nl("")
        nl("| Jogo | Mandante | Placar | Visitante | Fase | Prob. vitória |")
        nl("|------|----------|--------|-----------|------|--------------|")
        for mid in round_ids:
            r  = match_results[mid]
            h, a, w = r['home'], r['away'], r['winner']
            bh = "**" if w == h else ""
            ba = "**" if w == a else ""
            sc = format_score(r)
            nl(f"| M{mid} | {bh}{_name(h)}{bh} | {sc} | {ba}{_name(a)}{ba} | {r['method']} | {_name(w)} ({r['win_pct']:.0f}%) |")
        nl("")

    fmt_round([m for m, *_ in ROUND32],       "OITAVAS DE FINAL (Round of 32)")
    fmt_round([m for m, *_ in ROUND16],       "ROUND OF 16")
    fmt_round([m for m, *_ in QUARTERFINALS], "QUARTAS DE FINAL")
    fmt_round([m for m, *_ in SEMIFINALS],    "SEMIFINAIS")

    # ── Final ────────────────────────────────────────────────────────────
    nl("---")
    nl("")
    nl("## FINAL")
    nl("")
    r  = match_results[FINAL_ID]
    sc = format_score(r)
    nl(f"| {_name(r['home'])} | **{sc}** | {_name(r['away'])} | {r['method']} |")
    nl("|---|---|---|---|")
    nl("")
    champion = winners[FINAL_ID]
    runner_up = r['loser']
    nl(f"## CAMPEAO: **{_name(champion).upper()}**")
    nl("")
    nl(f"Placar: **{_name(r['home'])} {sc} {_name(r['away'])}**  ")
    nl(f"Método: {r['method']} | Probabilidade de vitória do campeão na final: **{r['win_pct']:.0f}%**")
    nl("")
    nl("---")
    nl("")
    nl("## RESUMO DO BRACKET")
    nl("")
    nl(f"| Fase | Vencedor |")
    nl(f"|------|---------|")
    for mid, src1, src2 in SEMIFINALS:
        nl(f"| Semifinal M{mid} | **{_name(winners[mid])}** |")
    nl(f"| Vice-campeão | {_name(runner_up)} |")
    nl(f"| **CAMPEÃO** | **{_name(champion)}** |")
    nl("")

    return "\n".join(lines)


# ─── Entry point ─────────────────────────────────────────────────────────────

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000
    scores = load_scores()

    print(f"Megazord — coletando dados de grupos ({n:,} simulações)...")
    rank_ctr, match_ctr, third_stat = collect_groups(scores, n)

    print("Derivando moda dos grupos...")
    order, mscores, stats, freq = modal_groups(rank_ctr, match_ctr)

    print("Ranqueando terceiros lugares...")
    thirds_ranked = best_thirds(order, stats)

    print(f"Simulando mata-mata ({K_KO:,} sub-sims por jogo)...")
    match_results, winners, qualifying = build_bracket(order, thirds_ranked, scores)

    print("Gerando relatório...")
    report = generate_report(
        order, mscores, stats, freq,
        thirds_ranked, qualifying, match_results, winners, n,
    )

    os.makedirs("output", exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)

    champion  = winners[FINAL_ID]
    runner_up = match_results[FINAL_ID]['loser']
    print(f"\nRelatório salvo em {OUT_PATH}")
    print(f"\n{'═'*50}")
    print(f"  CAMPEAO MEGAZORD : {_name(champion).upper()}")
    print(f"  Vice-campeão     : {_name(runner_up).upper()}")
    print(f"{'═'*50}\n")


if __name__ == '__main__':
    main()
