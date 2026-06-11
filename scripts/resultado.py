#!/usr/bin/env python3
"""
Entrada de resultados da Copa 2026 por ID de jogo.

Uso:
    python scripts/resultado.py           # pergunta qual jogo preencher
    python scripts/resultado.py --list    # lista todos os jogos com IDs
    python scripts/resultado.py --list r1 # filtra: r1 r2 r3 r32 r16 qf sf final
"""

import json
import os
import sys

# ─────────────────────────────────────────────────────────────────────────────
# Estrutura do torneio
# ─────────────────────────────────────────────────────────────────────────────

GROUPS = {
    "A": ["mexico",            "south_africa",         "republic_of_korea",  "czech_republic"],
    "B": ["canada",            "bosnia_and_herzegovina","qatar",              "switzerland"],
    "C": ["brazil",            "morocco",              "haiti",              "scotland"],
    "D": ["united_states_of_america", "paraguay",     "australia",          "turkey"],
    "E": ["germany",           "curacao",              "ivory_coast",        "ecuador"],
    "F": ["netherlands",       "japan",                "sweden",             "tunisia"],
    "G": ["belgium",           "egypt",                "ira",                "new_zealand"],
    "H": ["spain",             "cape_verte",           "saudi_arabia",       "uruguay"],
    "I": ["france",            "senegal",              "iraq",               "norway"],
    "J": ["argentina",         "algeria",              "austria",            "jordan"],
    "K": ["portugal",          "congo",                "uzbekistan",         "colombia"],
    "L": ["england",           "croatia",              "ghana",              "panama"],
}

DISPLAY_NAMES = {
    "united_states_of_america": "USA",
    "republic_of_korea":        "South Korea",
    "bosnia_and_herzegovina":   "Bosnia-Herz.",
    "cape_verte":               "Cape Verde",
    "ivory_coast":              "Côte d'Ivoire",
    "ira":                      "Iran",
    "new_zealand":              "New Zealand",
    "saudi_arabia":             "Saudi Arabia",
    "south_africa":             "South Africa",
    "czech_republic":           "Czech Republic",
}

def dn(t):
    return DISPLAY_NAMES.get(t, t.replace("_", " ").title())


# ─────────────────────────────────────────────────────────────────────────────
# Calendário da fase de grupos  (IDs 1 – 72)
#
# Para cada grupo, os 6 confrontos são distribuídos em 3 rodadas:
#   Rodada 1: times[0] × times[1],  times[2] × times[3]
#   Rodada 2: times[0] × times[2],  times[1] × times[3]
#   Rodada 3: times[0] × times[3],  times[1] × times[2]
#
# Numeração: 2 jogos × 12 grupos por rodada = 24 jogos/rodada
#   Rodada 1 → IDs  1 – 24   (grupos A→L, 2 jogos cada)
#   Rodada 2 → IDs 25 – 48
#   Rodada 3 → IDs 49 – 72
# ─────────────────────────────────────────────────────────────────────────────

RODADA_PAIRS = [
    # (índice_time_casa, índice_time_fora)  dentro de cada grupo
    [(0, 1), (2, 3)],   # Rodada 1
    [(0, 2), (1, 3)],   # Rodada 2
    [(0, 3), (1, 2)],   # Rodada 3
]

GROUP_ORDER = list("ABCDEFGHIJKL")

def _build_group_schedule():
    """Retorna dict: game_id → (round_label, group, home, away)."""
    schedule = {}
    for rodada_idx, pairs in enumerate(RODADA_PAIRS):
        round_label = f"Rodada {rodada_idx + 1}"
        base_id = rodada_idx * 24 + 1
        slot = 0
        for grp in GROUP_ORDER:
            teams = GROUPS[grp]
            for hi, ai in pairs:
                gid = base_id + slot
                schedule[gid] = (round_label, grp, teams[hi], teams[ai])
                slot += 1
    return schedule

GROUP_SCHEDULE = _build_group_schedule()

# ─────────────────────────────────────────────────────────────────────────────
# Calendário do mata-mata  (IDs 73 – 104)
# ─────────────────────────────────────────────────────────────────────────────

KNOCKOUT_SCHEDULE = {
    # Round of 32
    73:  ("Round of 32", "2º A",  "2º B"),
    74:  ("Round of 32", "1º E",  "3º ABCDF"),
    75:  ("Round of 32", "1º F",  "2º C"),
    76:  ("Round of 32", "1º C",  "2º F"),
    77:  ("Round of 32", "1º I",  "3º CDFGH"),
    78:  ("Round of 32", "2º E",  "2º I"),
    79:  ("Round of 32", "1º A",  "3º CEFHI"),
    80:  ("Round of 32", "1º L",  "3º EHIJK"),
    81:  ("Round of 32", "1º D",  "3º BEFIJ"),
    82:  ("Round of 32", "1º G",  "3º AEHIJ"),
    83:  ("Round of 32", "2º K",  "2º L"),
    84:  ("Round of 32", "1º H",  "2º J"),
    85:  ("Round of 32", "1º B",  "3º EFGIJ"),
    86:  ("Round of 32", "1º J",  "2º H"),
    87:  ("Round of 32", "1º K",  "3º DEIJL"),
    88:  ("Round of 32", "2º D",  "2º G"),
    # Round of 16
    89:  ("Oitavas",     "W74",   "W77"),
    90:  ("Oitavas",     "W73",   "W75"),
    91:  ("Oitavas",     "W76",   "W78"),
    92:  ("Oitavas",     "W79",   "W80"),
    93:  ("Oitavas",     "W83",   "W84"),
    94:  ("Oitavas",     "W81",   "W82"),
    95:  ("Oitavas",     "W86",   "W88"),
    96:  ("Oitavas",     "W85",   "W87"),
    # Quartas
    97:  ("Quartas",     "W89",   "W90"),
    98:  ("Quartas",     "W93",   "W94"),
    99:  ("Quartas",     "W91",   "W92"),
    100: ("Quartas",     "W95",   "W96"),
    # Semifinal
    101: ("Semifinal",   "W97",   "W98"),
    102: ("Semifinal",   "W99",   "W100"),
    # Terceiro lugar
    103: ("3º Lugar",    "Perdedor SF101", "Perdedor SF102"),
    # Final
    104: ("Final",       "W101",  "W102"),
}

ROUND_FILTER = {
    "r1":    lambda gid: 1  <= gid <= 24,
    "r2":    lambda gid: 25 <= gid <= 48,
    "r3":    lambda gid: 49 <= gid <= 72,
    "r32":   lambda gid: 73 <= gid <= 88,
    "r16":   lambda gid: 89 <= gid <= 96,
    "qf":    lambda gid: 97 <= gid <= 100,
    "sf":    lambda gid: 101 <= gid <= 102,
    "final": lambda gid: gid in (103, 104),
}

# ─────────────────────────────────────────────────────────────────────────────
# Estado persistido  (compatível com input_copa.py)
# ─────────────────────────────────────────────────────────────────────────────

STATE_FILE = "output/copa_real_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"group_results": {}, "knockout_results": {}}

def save_state(state):
    os.makedirs("output", exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def _mkey(a, b):
    return f"{a}|{b}"

def _get_group_result(state, grp, home, away):
    gr = state["group_results"].get(grp, {})
    return gr.get(_mkey(home, away))

def _get_knockout_result(state, gid):
    return state["knockout_results"].get(str(gid))

# ─────────────────────────────────────────────────────────────────────────────
# Listagem de jogos
# ─────────────────────────────────────────────────────────────────────────────

def _result_str_group(state, grp, home, away):
    r = _get_group_result(state, grp, home, away)
    if r is None:
        return "─ pendente ─"
    return f"{r[0]}–{r[1]}"

def _result_str_knockout(state, gid):
    d = _get_knockout_result(state, gid)
    if d is None:
        return "─ pendente ─"
    return f"{d['score_str']}  [{d['note']}]  → {dn(d['winner'])}"

def print_schedule(state, filter_key=None):
    pred = ROUND_FILTER.get(filter_key) if filter_key else None

    sections = {
        "Rodada 1":    [],
        "Rodada 2":    [],
        "Rodada 3":    [],
        "Round of 32": [],
        "Oitavas":     [],
        "Quartas":     [],
        "Semifinal":   [],
        "3º Lugar":    [],
        "Final":       [],
    }

    for gid in range(1, 73):
        if pred and not pred(gid):
            continue
        round_label, grp, home, away = GROUP_SCHEDULE[gid]
        result = _result_str_group(state, grp, home, away)
        sections[round_label].append((gid, grp, dn(home), dn(away), result))

    for gid in range(73, 105):
        if pred and not pred(gid):
            continue
        round_label, home_slot, away_slot = KNOCKOUT_SCHEDULE[gid]
        result = _result_str_knockout(state, gid)
        sections[round_label].append((gid, None, home_slot, away_slot, result))

    for section, entries in sections.items():
        if not entries:
            continue
        print(f"\n{'═'*70}")
        print(f"  {section.upper()}")
        print(f"{'═'*70}")
        for gid, grp, home, away, result in entries:
            grp_tag = f"[{grp}]" if grp else "    "
            print(f"  {gid:>3}.  {grp_tag}  {home:<22} vs  {away:<22}  {result}")

# ─────────────────────────────────────────────────────────────────────────────
# Entrada de resultados
# ─────────────────────────────────────────────────────────────────────────────

def _ask(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nInterrompido. Estado salvo.")
        sys.exit(0)

def _read_score_group(home, away):
    """Lê placar de jogo de grupo. Retorna (gols_casa, gols_fora)."""
    while True:
        raw = _ask(f"  Resultado (ex: 2-1 ou 2 1): ").replace("–", "-").replace("-", " ")
        parts = raw.split()
        if len(parts) == 2:
            try:
                return int(parts[0]), int(parts[1])
            except ValueError:
                pass
        print("  ✗  Use o formato  gols_casa-gols_fora  (ex: 2-1  ou  0 0)")

def _read_knockout(home_label, away_label, home_key, away_key):
    """Lê placar de mata-mata com prorrogação/pênaltis. Retorna dict de resultado."""
    print(f"  90 minutos:")
    ft_h, ft_a = None, None
    while True:
        raw = _ask(f"  {home_label:<22} vs {away_label}  →  ").replace("–", "-").replace("-", " ")
        parts = raw.split()
        if len(parts) == 2:
            try:
                ft_h, ft_a = int(parts[0]), int(parts[1])
                break
            except ValueError:
                pass
        print("  ✗  Use o formato  gols_casa-gols_fora  (ex: 1-0)")

    if ft_h != ft_a:
        winner = home_key if ft_h > ft_a else away_key
        return {"home": home_key, "away": away_key,
                "score_str": f"{ft_h}–{ft_a}", "note": "90'", "winner": winner}

    print(f"  Empate {ft_h}–{ft_a} após 90 minutos.")
    prorrog = _ask("  Houve prorrogação? (s/n): ").lower().startswith("s")

    if not prorrog:
        pw = _ask(f"  Pênaltis — quem venceu?  (c = {home_label}  /  f = {away_label}): ").lower()
        winner = home_key if pw.startswith("c") else away_key
        score_str = f"{ft_h}–{ft_a} pen."
        return {"home": home_key, "away": away_key,
                "score_str": score_str, "note": "PEN", "winner": winner}

    print(f"  Placar total após prorrogação:")
    et_h, et_a = None, None
    while True:
        raw = _ask(f"  {home_label:<22} vs {away_label}  →  ").replace("–", "-").replace("-", " ")
        parts = raw.split()
        if len(parts) == 2:
            try:
                et_h, et_a = int(parts[0]), int(parts[1])
                break
            except ValueError:
                pass
        print("  ✗  Use o formato  gols_casa-gols_fora")

    if et_h != et_a:
        winner = home_key if et_h > et_a else away_key
        return {"home": home_key, "away": away_key,
                "score_str": f"{et_h}–{et_a} ({ft_h}–{ft_a} AET)", "note": "AET", "winner": winner}

    pw = _ask(f"  Pênaltis — quem venceu?  (c = {home_label}  /  f = {away_label}): ").lower()
    winner = home_key if pw.startswith("c") else away_key
    return {"home": home_key, "away": away_key,
            "score_str": f"{et_h}–{et_a} pen.", "note": "PEN", "winner": winner}


def enter_result(state, gid):
    """Pede e salva o resultado do jogo com ID=gid."""
    if 1 <= gid <= 72:
        round_label, grp, home, away = GROUP_SCHEDULE[gid]
        existing = _get_group_result(state, grp, home, away)

        print(f"\n{'─'*70}")
        print(f"  Jogo #{gid}  |  {round_label}  |  Grupo {grp}")
        print(f"  {dn(home)}  vs  {dn(away)}")
        if existing:
            print(f"  Resultado atual: {existing[0]}–{existing[1]}")
            confirm = _ask("  Sobrescrever? (s/n): ")
            if not confirm.lower().startswith("s"):
                print("  Cancelado.")
                return
        print(f"{'─'*70}")

        ga, gb = _read_score_group(home, away)
        state["group_results"].setdefault(grp, {})[_mkey(home, away)] = [ga, gb]
        save_state(state)
        print(f"\n  ✓  Salvo: {dn(home)} {ga}–{gb} {dn(away)}")

    elif 73 <= gid <= 104:
        round_label, home_slot, away_slot = KNOCKOUT_SCHEDULE[gid]
        existing = _get_knockout_result(state, gid)

        # Tenta resolver times reais a partir dos vencedores anteriores
        ko = state["knockout_results"]
        def resolve_key(slot):
            if slot.startswith("W") and slot[1:].isdigit():
                prev = ko.get(slot[1:])
                return prev["winner"] if prev else None
            return slot  # ex: "1º A" — ainda não resolvível

        home_key = resolve_key(home_slot)
        away_key = resolve_key(away_slot)
        home_label = dn(home_key) if home_key and not home_key.startswith(("W", "1", "2", "3", "P")) else home_slot
        away_label = dn(away_key) if away_key and not away_key.startswith(("W", "1", "2", "3", "P")) else away_slot

        print(f"\n{'─'*70}")
        print(f"  Jogo #{gid}  |  {round_label}")
        print(f"  {home_label}  vs  {away_label}")
        if existing:
            print(f"  Resultado atual: {existing['score_str']}  [{existing['note']}]  → {dn(existing['winner'])}")
            confirm = _ask("  Sobrescrever? (s/n): ")
            if not confirm.lower().startswith("s"):
                print("  Cancelado.")
                return
        print(f"{'─'*70}")

        hk = home_key or home_slot
        ak = away_key or away_slot
        d = _read_knockout(home_label, away_label, hk, ak)
        state["knockout_results"][str(gid)] = d
        save_state(state)
        print(f"\n  ✓  Salvo: {home_label} {d['score_str']} {away_label}  [{d['note']}]  → {dn(d['winner'])}")

    else:
        print(f"  ✗  ID {gid} não existe. Use IDs de 1 a 104.")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if "--list" in args:
        state = load_state()
        idx = args.index("--list")
        filter_key = args[idx + 1].lower() if idx + 1 < len(args) else None
        if filter_key and filter_key not in ROUND_FILTER:
            print(f"Filtro inválido. Use: {', '.join(ROUND_FILTER)}")
            sys.exit(1)
        print_schedule(state, filter_key)
        return

    state = load_state()

    print("═"*70)
    print("  COPA DO MUNDO 2026 — Entrada de Resultado por ID")
    print("  (Use --list para ver todos os jogos e seus IDs)")
    print("═"*70)

    while True:
        print()
        raw = _ask("  ID do jogo (ou 'sair'): ")
        if raw.lower() in ("sair", "q", "exit"):
            break
        if not raw.isdigit():
            print("  ✗  Digite apenas o número do ID.")
            continue
        enter_result(state, int(raw))


if __name__ == "__main__":
    main()
