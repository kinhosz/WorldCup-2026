#!/usr/bin/env python3
"""
Match squad players against Transfermarket dataset using fuzzy name matching.
Outputs: market_value_by_nation.json with matched/unmatched players per nation.
"""

import json
import csv
import os
import re
import unicodedata
from difflib import SequenceMatcher

NATIONALITY_MAP = {
    "algeria": "Algeria",
    "argentina": "Argentina",
    "australia": "Australia",
    "austria": "Austria",
    "belgium": "Belgium",
    "bosnia_and_herzegovina": "Bosnia-Herzegovina",
    "brazil": "Brazil",
    "canada": "Canada",
    "cape_verte": "Cape Verde Islands",
    "colombia": "Colombia",
    "congo": "DR Congo",
    "croatia": "Croatia",
    "curacao": "Curaçao",
    "czech_republic": "Czech Republic",
    "ecuador": "Ecuador",
    "egypt": "Egypt",
    "england": "England",
    "france": "France",
    "germany": "Germany",
    "ghana": "Ghana",
    "haiti": "Haiti",
    "ira": "Iran",
    "iraq": "Iraq",
    "ivory_coast": "Ivory Coast",
    "japan": "Japan",
    "jordan": "Jordan",
    "mexico": "Mexico",
    "morocco": "Morocco",
    "netherlands": "Netherlands",
    "new_zealand": "New Zealand",
    "norway": "Norway",
    "panama": "Panama",
    "paraguay": "Paraguay",
    "portugal": "Portugal",
    "qatar": "Qatar",
    "republic_of_korea": "Korea, South",
    "saudi_arabia": "Saudi Arabia",
    "scotland": "Scotland",
    "senegal": "Senegal",
    "south_africa": "South Africa",
    "spain": "Spain",
    "sweden": "Sweden",
    "switzerland": "Switzerland",
    "tunisia": "Tunisia",
    "turkey": "Turkey",
    "united_states_of_america": "United States",
    "uruguay": "Uruguay",
    "uzbekistan": "Uzbekistan",
}

# Fallback: citizenship strings used in TM players.csv country_of_citizenship column
CITIZENSHIP_MAP = {
    "algeria": "Algeria",
    "argentina": "Argentina",
    "australia": "Australia",
    "austria": "Austria",
    "belgium": "Belgium",
    "bosnia_and_herzegovina": "Bosnia-Herzegovina",
    "brazil": "Brazil",
    "canada": "Canada",
    "cape_verte": "Cape Verde",
    "colombia": "Colombia",
    "congo": "DR Congo",
    "croatia": "Croatia",
    "curacao": "Curacao",
    "czech_republic": "Czech Republic",
    "ecuador": "Ecuador",
    "egypt": "Egypt",
    "england": "England",
    "france": "France",
    "germany": "Germany",
    "ghana": "Ghana",
    "haiti": "Haiti",
    "ira": "Iran",
    "iraq": "Iraq",
    "ivory_coast": "Ivory Coast",
    "japan": "Japan",
    "jordan": "Jordan",
    "mexico": "Mexico",
    "morocco": "Morocco",
    "netherlands": "Netherlands",
    "new_zealand": "New Zealand",
    "norway": "Norway",
    "panama": "Panama",
    "paraguay": "Paraguay",
    "portugal": "Portugal",
    "qatar": "Qatar",
    "republic_of_korea": "Korea, South",
    "saudi_arabia": "Saudi Arabia",
    "scotland": "Scotland",
    "senegal": "Senegal",
    "south_africa": "South Africa",
    "spain": "Spain",
    "sweden": "Sweden",
    "switzerland": "Switzerland",
    "tunisia": "Tunisia",
    "turkey": "Turkey",
    "united_states_of_america": "United States",
    "uruguay": "Uruguay",
    "uzbekistan": "Uzbekistan",
}

POSITION_GROUPS = {
    "goalkeepers": "goalkeepers",
    "defenders": "defenders",
    "middle": "midfielders",
    "midfielders": "midfielders",
    "attackers": "forwards",
    "forwards": "forwards",
}

MATCH_THRESHOLD = 0.70


_CHAR_MAP = str.maketrans({
    "ø": "o", "Ø": "O",
    "ı": "i", "İ": "I",
    "ğ": "g", "Ğ": "G",
    "ş": "s", "Ş": "S",
    "æ": "ae", "Æ": "AE",
    "ß": "ss",
    "ð": "d", "Ð": "D",
    "þ": "th", "Þ": "TH",
    "ł": "l", "Ł": "L",
})


def normalize_name(name: str) -> str:
    """Replace non-ASCII chars, strip accents, lowercase, remove punctuation."""
    name = name.translate(_CHAR_MAP)
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower().strip()
    name = re.sub(r"['\-\.\,]", " ", name)
    name = re.sub(r"\s+", " ", name)
    return name


def name_similarity(norm_a: str, norm_b: str) -> float:
    return SequenceMatcher(None, norm_a, norm_b).ratio()


def best_match(squad_name: str, candidates: list, norm_candidates: list) -> tuple:
    squad_norm = normalize_name(squad_name)
    squad_tokens = set(squad_norm.split())
    squad_joined = "".join(sorted(squad_tokens))
    best_score = 0.0
    best_row = None

    for row, tm_norm in zip(candidates, norm_candidates):
        tm_tokens = set(tm_norm.split())
        tm_joined = "".join(sorted(tm_tokens))

        token_overlap = len(squad_tokens & tm_tokens) / max(len(squad_tokens), 1)
        seq_score = name_similarity(squad_norm, tm_norm)
        # Also compare with all tokens joined (catches "Son Heungmin" vs "Son Heung-min")
        joined_score = name_similarity(squad_joined, tm_joined)
        combined = max(seq_score, joined_score, token_overlap * 0.85 + seq_score * 0.15)

        if combined > best_score:
            best_score = combined
            best_row = row

    return best_row, best_score


def load_national_teams(csv_path: str) -> dict:
    """Build mapping: national_team_id -> country_name."""
    teams = {}
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            teams[row["national_team_id"]] = row["name"]
    return teams


def load_transfermarket(players_path: str, national_teams: dict) -> tuple:
    """
    Load players grouped by national team and by citizenship.
    Returns: (by_nation, by_citizenship, global_exact_index)
    by_nation/by_citizenship: {name: [(row, norm_name), ...]}
    global_exact_index: {norm_name: row}
    """
    by_nation = {}
    by_citizenship = {}
    global_exact = {}

    with open(players_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            norm = normalize_name(row["name"])
            global_exact[norm] = row

            team_id = row.get("current_national_team_id", "").strip()
            if team_id:
                team_name = national_teams.get(team_id)
                if team_name:
                    if team_name not in by_nation:
                        by_nation[team_name] = []
                    by_nation[team_name].append((row, norm))

            citizenship = row.get("country_of_citizenship", "").strip()
            if citizenship:
                if citizenship not in by_citizenship:
                    by_citizenship[citizenship] = []
                by_citizenship[citizenship].append((row, norm))

    return by_nation, by_citizenship, global_exact


def load_squads(squads_dir: str) -> list:
    """Load all squad JSON files."""
    all_players = []
    for filename in sorted(os.listdir(squads_dir)):
        if not filename.endswith(".json"):
            continue
        squad_key = filename.replace(".json", "")
        path = os.path.join(squads_dir, filename)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        nation = data["name"]
        for raw_key, std_key in POSITION_GROUPS.items():
            for player_name in data.get(raw_key, []):
                all_players.append({
                    "squad_nation": nation,
                    "squad_file": squad_key,
                    "position_group": std_key,
                    "squad_name": player_name,
                })
    return all_players


def parse_market_value(val: str):
    try:
        v = float(val)
        return int(v) if v == int(v) else v
    except (ValueError, TypeError):
        return None


def main():
    squads_dir = "squads"
    players_path = "transfermarket/players.csv"
    national_teams_path = "transfermarket/national_teams.csv"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    print("Loading national teams...")
    national_teams = load_national_teams(national_teams_path)

    print("Loading Transfermarket players...")
    tm_by_nation, tm_by_citizenship, global_exact = load_transfermarket(players_path, national_teams)
    print(f"Nations with TM data: {len(tm_by_nation)}")
    print(f"Global name index: {len(global_exact)} players")

    print("Loading squad files...")
    squad_players = load_squads(squads_dir)
    print(f"Total squad players: {len(squad_players)}")

    result = {}
    total_matched = 0
    total_unmatched = 0

    for entry in squad_players:
        squad_key = entry["squad_file"]
        nation_key = entry["squad_nation"]
        squad_name = entry["squad_name"]
        squad_norm = normalize_name(squad_name)
        tm_nation = NATIONALITY_MAP.get(squad_key)

        if nation_key not in result:
            result[nation_key] = {"matched": [], "unmatched": []}

        best_row = None
        score = 0.0

        # Try exact match in global index first
        if squad_norm in global_exact:
            best_row = global_exact[squad_norm]
            score = 1.0
        else:
            # Build candidate pool: national team + citizenship (union, deduped by player_id)
            citizenship = CITIZENSHIP_MAP.get(squad_key, "")
            nat_pairs = tm_by_nation.get(tm_nation, [])
            cit_pairs = tm_by_citizenship.get(citizenship, [])
            seen_ids = set()
            candidates_pairs = []
            for p in nat_pairs + cit_pairs:
                pid = p[0].get("player_id", "")
                if pid not in seen_ids:
                    seen_ids.add(pid)
                    candidates_pairs.append(p)
            if candidates_pairs:
                rows = [p[0] for p in candidates_pairs]
                norms = [p[1] for p in candidates_pairs]
                best_row, score = best_match(squad_name, rows, norms)

        if best_row and score >= MATCH_THRESHOLD:
            result[nation_key]["matched"].append({
                "squad_name": squad_name,
                "transfermarket_name": best_row["name"],
                "position_group": entry["position_group"],
                "market_value_in_eur": parse_market_value(best_row.get("market_value_in_eur")),
                "highest_market_value_in_eur": parse_market_value(best_row.get("highest_market_value_in_eur")),
                "confidence": round(score, 3),
            })
            total_matched += 1
        else:
            hint = best_row["name"] if best_row else None
            result[nation_key]["unmatched"].append({
                "squad_name": squad_name,
                "position_group": entry["position_group"],
                "best_match_hint": hint,
                "best_match_score": round(score, 3) if best_row else None,
            })
            total_unmatched += 1

    out_path = os.path.join(output_dir, "market_value_by_nation.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nMatched:   {total_matched}")
    print(f"Unmatched: {total_unmatched}")
    print(f"\nSaved to {out_path}")

    print("\n=== UNMATCHED PLAYERS ===")
    for nation, data in sorted(result.items()):
        for p in data["unmatched"]:
            hint = p.get("best_match_hint") or "—"
            score = p.get("best_match_score") or 0.0
            print(f"  [{nation}] {p['squad_name']} — best hint: {hint} ({score:.2f})")


if __name__ == "__main__":
    main()
