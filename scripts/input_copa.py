#!/usr/bin/env python3
"""
Entrada interativa de resultados reais da Copa do Mundo 2026.

Pergunta partida a partida (fase de grupos → mata-mata) e ao final
gera output/COPA_REAL.md.

Estado salvo em output/copa_real_state.json — Ctrl+C a qualquer momento
para sair e retomar depois.

Uso:
    python scripts/input_copa.py              # entra com resultados
    python scripts/input_copa.py --report     # gera .md sem perguntar
    python scripts/input_copa.py --reset      # apaga estado e recomeça
    python scripts/input_copa.py --out NOME.md
"""

import json
import os
import sys
from itertools import combinations

# ─────────────────────────────────────────────────────────────────────────────
# Estrutura do torneio (igual a simulate.py)
# ─────────────────────────────────────────────────────────────────────────────

GROUPS = {
    "A": ["mexico", "south_africa", "republic_of_korea", "czech_republic"],
    "B": ["canada", "bosnia_and_herzegovina", "qatar", "switzerland"],
    "C": ["brazil", "morocco", "haiti", "scotland"],
    "D": ["united_states_of_america", "paraguay", "australia", "turkey"],
    "E": ["germany", "curacao", "ivory_coast", "ecuador"],
    "F": ["netherlands", "japan", "sweden", "tunisia"],
    "G": ["belgium", "egypt", "ira", "new_zealand"],
    "H": ["spain", "cape_verte", "saudi_arabia", "uruguay"],
    "I": ["france", "senegal", "iraq", "norway"],
    "J": ["argentina", "algeria", "austria", "jordan"],
    "K": ["portugal", "congo", "uzbekistan", "colombia"],
    "L": ["england", "croatia", "ghana", "panama"],
}

ROUND32 = [
    (73,  ('2', 'A'),   ('2', 'B')),
    (74,  ('1', 'E'),   ('3rd', 'ABCDF')),
    (75,  ('1', 'F'),   ('2', 'C')),
    (76,  ('1', 'C'),   ('2', 'F')),
    (77,  ('1', 'I'),   ('3rd', 'CDFGH')),
    (78,  ('2', 'E'),   ('2', 'I')),
    (79,  ('1', 'A'),   ('3rd', 'CEFHI')),
    (80,  ('1', 'L'),   ('3rd', 'EHIJK')),
    (81,  ('1', 'D'),   ('3rd', 'BEFIJ')),
    (82,  ('1', 'G'),   ('3rd', 'AEHIJ')),
    (83,  ('2', 'K'),   ('2', 'L')),
    (84,  ('1', 'H'),   ('2', 'J')),
    (85,  ('1', 'B'),   ('3rd', 'EFGIJ')),
    (86,  ('1', 'J'),   ('2', 'H')),
    (87,  ('1', 'K'),   ('3rd', 'DEIJL')),
    (88,  ('2', 'D'),   ('2', 'G')),
]

ROUND16 = [
    (89,  74, 77),
    (90,  73, 75),
    (91,  76, 78),
    (92,  79, 80),
    (93,  83, 84),
    (94,  81, 82),
    (95,  86, 88),
    (96,  85, 87),
]

QUARTERFINALS = [
    (97,   89, 90),
    (98,   93, 94),
    (99,   91, 92),
    (100,  95, 96),
]

SEMIFINALS = [
    (101,  97,  98),
    (102,  99, 100),
]

FINAL_ID = 104

THIRD_PLACE_SLOTS = {
    74: set('ABCDF'),
    77: set('CDFGH'),
    79: set('CEFHI'),
    80: set('EHIJK'),
    81: set('BEFIJ'),
    82: set('AEHIJ'),
    85: set('EFGIJ'),
    87: set('DEIJL'),
}

DISPLAY_NAMES = {
    'united_states_of_america': 'USA',
    'republic_of_korea':        'South Korea',
    'bosnia_and_herzegovina':   'Bosnia-Herzegovina',
    'cape_verte':               'Cape Verde',
    'ivory_coast':              "Côte d'Ivoire",
    'ira':                      'Iran',
    'new_zealand':              'New Zealand',
    'saudi_arabia':             'Saudi Arabia',
    'south_africa':             'South Africa',
    'czech_republic':           'Czech Republic',
}

STATE_FILE = "output/copa_real_state.json"
OUT_FILE   = "output/COPA_REAL.md"


def _name(t):
    return DISPLAY_NAMES.get(t, t.replace('_', ' ').title())


# ─────────────────────────────────────────────────────────────────────────────
# Persistência
# ─────────────────────────────────────────────────────────────────────────────

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding='utf-8') as f:
            return json.load(f)
    return {"group_results": {}, "knockout_results": {}}


def save_state(state):
    os.makedirs("output", exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# Leitura de input
# ─────────────────────────────────────────────────────────────────────────────

def _ask(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nInterrompido. Estado salvo.")
        sys.exit(0)


def read_score(label):
    """Aceita '3 0', '3-0', '3–0'. Retorna (gols_mandante, gols_visitante)."""
    while True:
        raw = _ask(f"  {label}: ").replace('–', '-').replace('-', ' ')
        parts = raw.split()
        if len(parts) == 2:
            try:
                return int(parts[0]), int(parts[1])
            except ValueError:
                pass
        print("  ✗ Use: gols_mandante-gols_visitante  (ex: 2-1  ou  2 1)")


def read_knockout_result(home, away):
    """
    Lê interativamente o resultado de um jogo de mata-mata.
    Retorna dict {home, away, score_str, note, winner}.
    """
    nh, na = _name(home), _name(away)

    ft_h, ft_a = read_score(f"90'  {nh} × {na}")

    if ft_h != ft_a:
        winner = home if ft_h > ft_a else away
        return {"home": home, "away": away,
                "score_str": f"{ft_h}–{ft_a}", "note": "90'", "winner": winner}

    prorrog = _ask("  Prorrogação? (s/n): ").lower().startswith('s')

    if not prorrog:
        pw = _ask(f"  Pênaltis → vencedor  (h={nh}  /  a={na}): ").lower()
        winner = home if pw.startswith('h') else away
        return {"home": home, "away": away,
                "score_str": f"{ft_h}–{ft_a} pen.", "note": "PEN", "winner": winner}

    et_h, et_a = read_score(f"AET  {nh} × {na} (placar total após prorrogação)")

    if et_h != et_a:
        winner = home if et_h > et_a else away
        return {"home": home, "away": away,
                "score_str": f"{et_h}–{et_a} ({ft_h}–{ft_a} AET)",
                "note": "AET", "winner": winner}

    pw = _ask(f"  Pênaltis → vencedor  (h={nh}  /  a={na}): ").lower()
    winner = home if pw.startswith('h') else away
    return {"home": home, "away": away,
            "score_str": f"{et_h}–{et_a} pen.", "note": "PEN", "winner": winner}


# ─────────────────────────────────────────────────────────────────────────────
# Fase de grupos
# ─────────────────────────────────────────────────────────────────────────────

def _mkey(ta, tb):
    return f"{ta}|{tb}"


def _standings(letter, gr):
    """
    Retorna (ranked, matches_done).
    ranked: [(team, pts, gd, gf, wins), ...]  ordenado 1→4.
    matches_done: [(ta, tb, ga, gb), ...]
    """
    teams = GROUPS[letter]
    stats = {t: dict(pts=0, gd=0, gf=0, wins=0) for t in teams}
    matches_done = []

    for ta, tb in combinations(teams, 2):
        r = gr.get(_mkey(ta, tb))
        if r is None:
            continue
        ga, gb = r
        matches_done.append((ta, tb, ga, gb))
        stats[ta]['gf'] += ga
        stats[tb]['gf'] += gb
        stats[ta]['gd'] += ga - gb
        stats[tb]['gd'] += gb - ga
        if ga > gb:
            stats[ta]['pts'] += 3
            stats[ta]['wins'] += 1
        elif gb > ga:
            stats[tb]['pts'] += 3
            stats[tb]['wins'] += 1
        else:
            stats[ta]['pts'] += 1
            stats[tb]['pts'] += 1

    ranked = sorted(teams, key=lambda t: (
        -stats[t]['pts'], -stats[t]['gd'], -stats[t]['gf'], -stats[t]['wins']
    ))
    return (
        [(t, stats[t]['pts'], stats[t]['gd'], stats[t]['gf'], stats[t]['wins']) for t in ranked],
        matches_done,
    )


def run_group_stage(state):
    print("\n" + "═"*62)
    print("  FASE DE GRUPOS")
    print("═"*62)

    for letter in sorted(GROUPS):
        teams = GROUPS[letter]
        pairs = list(combinations(teams, 2))
        gr = state["group_results"].setdefault(letter, {})
        remaining = [(ta, tb) for ta, tb in pairs if _mkey(ta, tb) not in gr]

        if not remaining:
            print(f"\nGrupo {letter}: completo ✓")
            continue

        done_n = len(pairs) - len(remaining)
        print(f"\n{'─'*62}")
        print(f"  Grupo {letter}  ({done_n}/{len(pairs)})  "
              f"{' · '.join(_name(t) for t in teams)}")
        print('─'*62)

        for ta, tb in remaining:
            print(f"\n  {_name(ta)} × {_name(tb)}")
            ga, gb = read_score(f"{_name(ta)}-{_name(tb)}")
            gr[_mkey(ta, tb)] = [ga, gb]
            save_state(state)

        ranked, _ = _standings(letter, gr)
        print(f"\n  Tabela Grupo {letter}:")
        for pos, (team, pts, gd, gf, _) in enumerate(ranked, 1):
            adv = "→ R32" if pos <= 2 else ("3°" if pos == 3 else "✗")
            print(f"    {pos}. {_name(team):<28} {pts:2d}pts  GD{gd:+3d}  GF{gf:2d}  {adv}")


def _groups_complete(state):
    for letter in GROUPS:
        gr = state["group_results"].get(letter, {})
        for ta, tb in combinations(GROUPS[letter], 2):
            if _mkey(ta, tb) not in gr:
                return False
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Bracket: 3ºs lugares
# ─────────────────────────────────────────────────────────────────────────────

def _assign_thirds(qualifying):
    slots = list(THIRD_PLACE_SLOTS.keys())
    assign = {}
    used = [False] * len(qualifying)

    def bt(i):
        if i == len(slots):
            return True
        slot = slots[i]
        for j, (grp, _) in enumerate(qualifying):
            if not used[j] and grp in THIRD_PLACE_SLOTS[slot]:
                assign[slot] = qualifying[j][1]
                used[j] = True
                if bt(i + 1):
                    return True
                del assign[slot]
                used[j] = False
        return False

    if bt(0):
        return assign
    return {slots[i]: qualifying[i % len(qualifying)][1] for i in range(len(slots))}


def _build_bracket(state):
    group_rankings = {}
    thirds = []
    for letter in GROUPS:
        gr = state["group_results"].get(letter, {})
        ranked, _ = _standings(letter, gr)
        group_rankings[letter] = ranked
        t, pts, gd, gf, wins = ranked[2]
        thirds.append((letter, t, pts, gd, gf, wins))

    ranked_thirds = sorted(thirds, key=lambda x: (-x[2], -x[3], -x[4], -x[5]))
    qualifying = [(g, t) for g, t, *_ in ranked_thirds[:8]]
    slot_map = _assign_thirds(qualifying)
    return group_rankings, slot_map, qualifying


def _resolve(spec, grp_rank, slot_map, mid):
    kind, val = spec
    if kind == '1':
        return grp_rank[val][0][0]
    if kind == '2':
        return grp_rank[val][1][0]
    return slot_map.get(mid)


# ─────────────────────────────────────────────────────────────────────────────
# Mata-mata
# ─────────────────────────────────────────────────────────────────────────────

def _play(mid, home, away, state, winners):
    ms = str(mid)
    ko = state["knockout_results"]

    if home is None or away is None:
        print(f"  M{mid}: aguardando partidas anteriores...")
        return

    if ms in ko:
        d = ko[ms]
        wh = "**" if d['winner'] == d['home'] else ""
        wa = "**" if d['winner'] == d['away'] else ""
        print(f"  M{mid}: {wh}{_name(d['home'])}{wh} {d['score_str']} "
              f"{wa}{_name(d['away'])}{wa}  [{d['note']}] ✓")
        winners[mid] = d['winner']
        return

    print(f"\n  M{mid}:")
    d = read_knockout_result(home, away)
    ko[ms] = d
    winners[mid] = d['winner']
    save_state(state)


def run_knockout_stage(state, grp_rank, slot_map):
    winners = {int(k): v['winner'] for k, v in state["knockout_results"].items()}

    print(f"\n{'═'*62}")
    print("  OITAVAS DE FINAL (Round of 32)")
    print('═'*62)
    for mid, spec1, spec2 in ROUND32:
        h = _resolve(spec1, grp_rank, slot_map, mid)
        a = _resolve(spec2, grp_rank, slot_map, mid)
        _play(mid, h, a, state, winners)

    print(f"\n{'═'*62}")
    print("  ROUND OF 16")
    print('═'*62)
    for mid, s1, s2 in ROUND16:
        _play(mid, winners.get(s1), winners.get(s2), state, winners)

    print(f"\n{'═'*62}")
    print("  QUARTAS DE FINAL")
    print('═'*62)
    for mid, s1, s2 in QUARTERFINALS:
        _play(mid, winners.get(s1), winners.get(s2), state, winners)

    print(f"\n{'═'*62}")
    print("  SEMIFINAIS")
    print('═'*62)
    for mid, s1, s2 in SEMIFINALS:
        _play(mid, winners.get(s1), winners.get(s2), state, winners)

    print(f"\n{'═'*62}")
    print("  FINAL")
    print('═'*62)
    sf1, sf2 = SEMIFINALS[0][0], SEMIFINALS[1][0]
    _play(FINAL_ID, winners.get(sf1), winners.get(sf2), state, winners)


# ─────────────────────────────────────────────────────────────────────────────
# Geração do documento
# ─────────────────────────────────────────────────────────────────────────────

def generate_report(state, grp_rank, slot_map, qualifying, out_path):
    lines = []
    a = lines.append

    a("# 🌍 Copa do Mundo 2026 — Resultados Reais")
    a("")
    a("---")
    a("")
    a("### FASE DE GRUPOS")
    a("")

    for letter in sorted(GROUPS):
        gr = state["group_results"].get(letter, {})
        ranked, matches = _standings(letter, gr)

        a(f"**Grupo {letter}**")
        a("")
        a("| # | Seleção | Pts | GD | GP |")
        a("|---|---------|-----|----|----|")
        for pos, (team, pts, gd, gf, _) in enumerate(ranked, 1):
            adv = "→ R32" if pos <= 2 else ("→ R32 (3°)" if pos == 3 else "✗")
            a(f"| {pos} | {_name(team)} | {pts} | {gd:+d} | {gf} | {adv}")
        a("")
        if matches:
            a("Jogos:")
            for ta, tb, ga, gb in matches:
                a(f"- {_name(ta)} {ga}–{gb} {_name(tb)}")
        a("")

    a("**8 melhores 3ºs lugares classificados:**")
    for g, t in qualifying:
        a(f"- {_name(t)} (Grupo {g})")
    a("")

    ko = state["knockout_results"]
    winners = {int(k): v['winner'] for k, v in ko.items()}

    def _fmt(entries, title):
        a(f"### {title}")
        a("")
        a("| Jogo | Mandante | Placar | Visitante | Obs |")
        a("|------|----------|--------|-----------|-----|")
        for entry in entries:
            mid = entry[0]
            ms = str(mid)
            if ms not in ko:
                a(f"| M{mid} | — | — | — | — |")
                continue
            d = ko[ms]
            wh = "**" if d['winner'] == d['home'] else ""
            wa = "**" if d['winner'] == d['away'] else ""
            a(f"| M{mid} | {wh}{_name(d['home'])}{wh} | {d['score_str']} "
              f"| {wa}{_name(d['away'])}{wa} | {d['note']} |")
        a("")

    _fmt(ROUND32, "OITAVAS DE FINAL (Round of 32)")
    _fmt(ROUND16, "ROUND OF 16")
    _fmt(QUARTERFINALS, "QUARTAS DE FINAL")
    _fmt(SEMIFINALS, "SEMIFINAIS")

    ms = str(FINAL_ID)
    a("### FINAL")
    a("")
    if ms in ko:
        d = ko[ms]
        a(f"**{_name(d['home'])}** {d['score_str']} **{_name(d['away'])}**")
        a("")
        a(f"🏆 **CAMPEÃO: {_name(d['winner']).upper()}**")
    else:
        a("*(ainda não disputada)*")
    a("")

    os.makedirs("output", exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"\n  Documento gerado: {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    only_report = "--report" in args
    reset       = "--reset"  in args
    out_path    = OUT_FILE

    if "--out" in args:
        idx = args.index("--out")
        name = args[idx + 1]
        out_path = name if name.startswith("output/") else f"output/{name}"

    if reset and os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
        print("Estado apagado. Começando do zero.")

    state = load_state()

    if only_report:
        grp_rank, slot_map, qualifying = _build_bracket(state)
        generate_report(state, grp_rank, slot_map, qualifying, out_path)
        return

    done_g = sum(len(r) for r in state["group_results"].values())
    done_k = len(state["knockout_results"])

    print("═"*62)
    print("  COPA DO MUNDO 2026 — Entrada de Resultados Reais")
    if done_g or done_k:
        print(f"  Retomando: {done_g} jogo(s) de grupo + {done_k} mata-mata")
    print("  Ctrl+C salva e sai. Retome com o mesmo comando.")
    print("═"*62)

    run_group_stage(state)

    if not _groups_complete(state):
        resp = _ask("\n  Fase de grupos incompleta. Gerar relatório parcial? (s/n): ")
        if resp.lower().startswith('s'):
            grp_rank, slot_map, qualifying = _build_bracket(state)
            generate_report(state, grp_rank, slot_map, qualifying, out_path)
        return

    grp_rank, slot_map, qualifying = _build_bracket(state)

    print("\n  8 melhores 3ºs lugares classificados:")
    for g, t in qualifying:
        print(f"    Grupo {g}: {_name(t)}")

    run_knockout_stage(state, grp_rank, slot_map)

    generate_report(state, grp_rank, slot_map, qualifying, out_path)


if __name__ == "__main__":
    main()
