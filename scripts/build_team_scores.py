#!/usr/bin/env python3
"""
Build team_scores.json — tiered player attribute cascade.

Priority order (per player):
  Tier 1  FC25  — datasets/extracted/players_25.csv  (auto-loaded if present)
  Tier 2  FIFA 22 — datasets/extracted/players_22.csv
  Tier 3  Transfermarket 2025 — output/market_value_by_nation.json (pre-matched)
  Tier 4  Global median for that sector position

Sector attribute mapping (FIFA engine, 0–100 scale):
  GK  → goalkeeping_diving, goalkeeping_reflexes, goalkeeping_handling, goalkeeping_positioning
  DEF → defending, physic
  MID → passing, dribbling
  ATT → shooting, pace

TM market value → synthetic rating (log-linear calibration):
  rating = LO_R + (HI_R - LO_R) * (log(mv) - log(LO_V)) / (log(HI_V) - log(LO_V))
  Anchors: €1M → 65,  €180M → 91
  Clipped to [45, 95].

Usage:
    python scripts/build_team_scores.py

Output: output/team_scores.json
"""

import csv
import json
import math
import os
import re
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher

# ── Constants ─────────────────────────────────────────────────────────────────

BASE_XG       = 1.3
FALLBACK_SCORE = 0.5          # used in xG formula for None sector values

FIFA_MATCH_THRESHOLD = 0.72   # minimum SequenceMatcher ratio for a valid FIFA match

# Top-K players per sector used to compute team score (starter proxies)
TOP_K = {'goalkeepers': 1, 'defenders': 4, 'middle': 4, 'attackers': 3}

# FIFA attributes used per squad sector
FIFA_ATTRS = {
    'goalkeepers': ['goalkeeping_diving', 'goalkeeping_reflexes',
                    'goalkeeping_handling', 'goalkeeping_positioning'],
    'defenders':   ['defending', 'physic'],
    'middle':      ['passing', 'dribbling'],
    'attackers':   ['shooting', 'pace'],
}

# TM → synthetic FIFA rating anchors
_TM_LO_V  = 1_000_000        # €1M
_TM_HI_V  = 180_000_000      # €180M
_TM_LO_R  = 65.0
_TM_HI_R  = 91.0
_TM_LOG_LO = math.log(_TM_LO_V)
_TM_LOG_HI = math.log(_TM_HI_V)

# Squad-file key → canonical name in team_scores.json
SECTOR_CANONICAL = {
    'goalkeepers': 'goalkeeper',
    'defenders':   'defense',
    'middle':      'midfield',
    'attackers':   'attack',
}

# Squad filename → FIFA 22 nationality_name
NATIONALITY_MAP = {
    'algeria':                 'Algeria',
    'argentina':               'Argentina',
    'australia':               'Australia',
    'austria':                 'Austria',
    'belgium':                 'Belgium',
    'bosnia_and_herzegovina':  'Bosnia and Herzegovina',
    'brazil':                  'Brazil',
    'canada':                  'Canada',
    'cape_verte':              'Cape Verde Islands',
    'colombia':                'Colombia',
    'congo':                   'Congo DR',
    'croatia':                 'Croatia',
    'curacao':                 'Curacao',
    'czech_republic':          'Czech Republic',
    'ecuador':                 'Ecuador',
    'egypt':                   'Egypt',
    'england':                 'England',
    'france':                  'France',
    'germany':                 'Germany',
    'ghana':                   'Ghana',
    'haiti':                   'Haiti',
    'ira':                     'Iran',
    'iraq':                    'Iraq',
    'ivory_coast':             "Côte d'Ivoire",
    'japan':                   'Japan',
    'jordan':                  'Jordan',
    'mexico':                  'Mexico',
    'morocco':                 'Morocco',
    'netherlands':             'Netherlands',
    'new_zealand':             'New Zealand',
    'norway':                  'Norway',
    'panama':                  'Panama',
    'paraguay':                'Paraguay',
    'portugal':                'Portugal',
    'qatar':                   'Qatar',
    'republic_of_korea':       'Korea Republic',
    'saudi_arabia':            'Saudi Arabia',
    'scotland':                'Scotland',
    'senegal':                 'Senegal',
    'south_africa':            'South Africa',
    'spain':                   'Spain',
    'sweden':                  'Sweden',
    'switzerland':             'Switzerland',
    'tunisia':                 'Tunisia',
    'turkey':                  'Turkey',
    'united_states_of_america':'United States',
    'uruguay':                 'Uruguay',
    'uzbekistan':              'Uzbekistan',
}

# ── Name normalisation ────────────────────────────────────────────────────────

_CHAR_MAP = str.maketrans({
    'ø': 'o', 'Ø': 'O', 'ı': 'i', 'İ': 'I',
    'ğ': 'g', 'Ğ': 'G', 'ş': 's', 'Ş': 'S',
    'æ': 'ae', 'Æ': 'AE', 'ß': 'ss',
    'ð': 'd', 'Ð': 'D', 'þ': 'th', 'Þ': 'TH',
    'ł': 'l', 'Ł': 'L',
})


def normalize(name: str) -> str:
    name = name.translate(_CHAR_MAP)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    name = name.lower().strip()
    name = re.sub(r"['\-\.\,]", ' ', name)
    return re.sub(r'\s+', ' ', name).strip()


# ── FIFA data loading ─────────────────────────────────────────────────────────

def _fifa_sector_score(row: dict, sector: str) -> float | None:
    """Mean of relevant FIFA attrs for the given squad sector. Returns float or None."""
    attrs = FIFA_ATTRS[sector]
    vals = []
    for attr in attrs:
        raw = row.get(attr, '').strip()
        # Strip position-suffix like "87+3" → take base integer
        base = raw.split('+')[0].split('-')[0].strip()
        try:
            vals.append(float(base))
        except ValueError:
            pass
    return sum(vals) / len(vals) if vals else None


def load_fifa_index(csv_path: str) -> dict[str, list]:
    """
    Build {normalized_name → [row, ...]} index for all players.
    Each row keeps original fields + a pre-computed norm key.
    """
    idx: dict[str, list] = defaultdict(list)
    with open(csv_path, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            for field in ('short_name', 'long_name'):
                key = normalize(row.get(field, ''))
                if key:
                    idx[key].append(row)
    return dict(idx)


def find_fifa_match(
    squad_name: str,
    nationality: str,
    fifa_index: dict,
    threshold: float = FIFA_MATCH_THRESHOLD,
) -> tuple[dict | None, float]:
    """
    Find the best FIFA match for a squad player.

    Strategy:
      1. Build a candidate pool: all FIFA players of the same nationality.
      2. Score each candidate: SequenceMatcher ratio against short_name and long_name.
      3. Return (best_row, score) if score >= threshold, else (None, 0.0).
    """
    squad_norm = normalize(squad_name)
    # Remove 'junior'/'jr'/'senior' suffixes that cause cross-name confusion
    squad_clean = re.sub(r'\b(junior|senior|jr|sr)\b', '', squad_norm).strip()

    # Build nationality-filtered candidate pool on first call via the index
    nat_lower = nationality.lower()
    candidates = [
        row for rows in fifa_index.values() for row in rows
        if nat_lower in normalize(row.get('nationality_name', '')).lower()
    ]
    # Deduplicate by sofifa_id
    seen = set()
    unique = []
    for row in candidates:
        sid = row.get('sofifa_id', '')
        if sid not in seen:
            seen.add(sid)
            unique.append(row)

    best_row, best_score = None, 0.0
    for row in unique:
        for field in ('short_name', 'long_name'):
            fifa_norm = normalize(row.get(field, ''))
            fifa_clean = re.sub(r'\b(junior|senior|jr|sr)\b', '', fifa_norm).strip()

            # Primary: full-string similarity
            ratio = SequenceMatcher(None, squad_norm, fifa_norm).ratio()

            # Secondary: cleaned (suffix-stripped) similarity
            ratio_clean = SequenceMatcher(None, squad_clean, fifa_clean).ratio()

            # Token overlap bonus
            s_tokens = set(squad_clean.split())
            f_tokens = set(fifa_clean.split())
            overlap = len(s_tokens & f_tokens) / max(len(s_tokens), len(f_tokens), 1)

            score = max(ratio, ratio_clean, overlap * 0.8 + ratio * 0.2)
            if score > best_score:
                best_score = score
                best_row = row

    if best_score >= threshold:
        return best_row, best_score
    return None, 0.0


def build_nationality_pools(fifa_index: dict) -> dict[str, list]:
    """Pre-compute nationality-filtered player lists for fast lookup."""
    pools: dict[str, list] = defaultdict(list)
    seen_by_nat: dict[str, set] = defaultdict(set)
    for rows in fifa_index.values():
        for row in rows:
            nat = normalize(row.get('nationality_name', ''))
            sid = row.get('sofifa_id', '')
            if sid and sid not in seen_by_nat[nat]:
                seen_by_nat[nat].add(sid)
                pools[nat].append(row)
    return dict(pools)


def find_fifa_match_fast(
    squad_name: str,
    nationality: str,
    nat_pools: dict,
    threshold: float = FIFA_MATCH_THRESHOLD,
) -> tuple[dict | None, float]:
    """Faster version using pre-built nationality pools."""
    squad_norm = normalize(squad_name)
    squad_clean = re.sub(r'\b(junior|senior|jr|sr)\b', '', squad_norm).strip()
    nat_key = normalize(nationality)
    candidates = nat_pools.get(nat_key, [])

    best_row, best_score = None, 0.0
    for row in candidates:
        for field in ('short_name', 'long_name'):
            fifa_norm = normalize(row.get(field, ''))
            fifa_clean = re.sub(r'\b(junior|senior|jr|sr)\b', '', fifa_norm).strip()

            ratio = SequenceMatcher(None, squad_norm, fifa_norm).ratio()
            ratio_clean = SequenceMatcher(None, squad_clean, fifa_clean).ratio()

            s_tokens = set(squad_clean.split())
            f_tokens = set(fifa_clean.split())
            overlap = len(s_tokens & f_tokens) / max(len(s_tokens), len(f_tokens), 1)

            score = max(ratio, ratio_clean, overlap * 0.8 + ratio * 0.2)
            if score > best_score:
                best_score = score
                best_row = row

    if best_score >= threshold:
        return best_row, best_score
    return None, 0.0


# ── TM conversion ─────────────────────────────────────────────────────────────

def tm_to_rating(mv_eur: float | None) -> float | None:
    """Convert Transfermarket market value (€) to a synthetic 0–100 FIFA-like rating."""
    if not mv_eur or mv_eur <= 0:
        return None
    t = (math.log(mv_eur) - _TM_LOG_LO) / (_TM_LOG_HI - _TM_LOG_LO)
    t = max(0.0, min(1.0, t))
    return _TM_LO_R + t * (_TM_HI_R - _TM_LO_R)


# ── Scoring helpers ───────────────────────────────────────────────────────────

def log_mean(values: list) -> float | None:
    valid = [v for v in values if v and v > 0]
    if not valid:
        return None
    return math.exp(sum(math.log(v) for v in valid) / len(valid))


def top_k_log_mean(values: list, k: int) -> float | None:
    valid = sorted([v for v in values if v and v > 0], reverse=True)
    return log_mean(valid[:k])


def minmax_normalize(values_by_nation: dict) -> dict:
    valid = {n: v for n, v in values_by_nation.items() if v is not None}
    if not valid:
        return {n: None for n in values_by_nation}
    lo, hi = min(valid.values()), max(valid.values())
    result = {}
    for nation, v in values_by_nation.items():
        if v is None:
            result[nation] = None
        elif hi == lo:
            result[nation] = 0.5
        else:
            result[nation] = round((v - lo) / (hi - lo), 4)
    return result


# ── xG formula ────────────────────────────────────────────────────────────────

def compute_xg(scores_a: dict, scores_b: dict) -> tuple[float, float]:
    def get(s, key):
        v = s.get(key)
        return v if v is not None else FALLBACK_SCORE

    off_a = 0.7 * get(scores_a, 'attack')  + 0.3 * get(scores_a, 'midfield')
    off_b = 0.7 * get(scores_b, 'attack')  + 0.3 * get(scores_b, 'midfield')
    res_a = 0.6 * get(scores_a, 'defense') + 0.2 * get(scores_a, 'goalkeeper') + 0.2 * get(scores_a, 'midfield')
    res_b = 0.6 * get(scores_b, 'defense') + 0.2 * get(scores_b, 'goalkeeper') + 0.2 * get(scores_b, 'midfield')
    return round(BASE_XG * off_a / res_b, 4), round(BASE_XG * off_b / res_a, 4)


# ── Main pipeline ─────────────────────────────────────────────────────────────

def main():
    squads_dir   = 'squads'
    tm_path      = 'output/market_value_by_nation.json'
    fifa22_path  = 'datasets/extracted/players_22.csv'
    fc25_path    = 'datasets/extracted/players_25.csv'   # loaded if present
    output_path  = 'output/team_scores.json'
    os.makedirs('output', exist_ok=True)

    # ── Load FIFA data ──────────────────────────────────────────────────
    print('Loading FIFA data...')
    fifa_index = load_fifa_index(fifa22_path)
    source_label = 'FIFA 22'

    if os.path.exists(fc25_path):
        print(f'  FC25 found — merging (FC25 takes priority for matched players)')
        fc25_index = load_fifa_index(fc25_path)
        # Merge: FC25 entries override FIFA22 for the same key
        for key, rows in fc25_index.items():
            if key in fifa_index:
                # Keep FC25 rows first so they get picked as highest overall
                fifa_index[key] = rows + fifa_index[key]
            else:
                fifa_index[key] = rows
        source_label = 'FC25 + FIFA 22'

    nat_pools = build_nationality_pools(fifa_index)
    print(f'  {source_label}: {sum(len(v) for v in nat_pools.values()):,} players indexed')

    # ── Load TM data ────────────────────────────────────────────────────
    print('Loading Transfermarket data...')
    with open(tm_path, encoding='utf-8') as f:
        tm_data = json.load(f)

    # Build per-nation TM lookup: {nation_key: {squad_name → market_value_in_eur}}
    tm_by_nation: dict[str, dict] = {}
    for nation, d in tm_data.items():
        tm_by_nation[nation] = {
            p['squad_name']: p['market_value_in_eur']
            for p in d['matched']
            if p.get('market_value_in_eur')
        }

    # ── Process each squad ──────────────────────────────────────────────
    print('Processing squads...')

    # raw scores: {nation: {sector: [player_rating, ...]}}
    raw: dict[str, dict[str, list]] = {}
    sources: dict[str, dict[str, dict]] = {}   # {nation: {sector: {fc25,fifa22,tm,avg}}}

    all_sector_ratings: dict[str, list] = defaultdict(list)  # for Tier-4 global median

    for squad_file in sorted(os.listdir(squads_dir)):
        if not squad_file.endswith('.json'):
            continue
        nation = squad_file[:-5]
        with open(os.path.join(squads_dir, squad_file), encoding='utf-8') as f:
            squad = json.load(f)

        nationality = NATIONALITY_MAP.get(nation, nation.replace('_', ' ').title())
        tm_lookup   = tm_by_nation.get(nation, {})

        raw[nation]     = {s: [] for s in TOP_K}
        sources[nation] = {s: {'fc25': 0, 'fifa22': 0, 'tm': 0, 'unmatched': 0} for s in TOP_K}

        for sector in TOP_K:
            players = squad.get(sector, [])
            if not players and sector == 'middle':
                players = squad.get('midfielders', [])
            if not players and sector == 'attackers':
                players = squad.get('forwards', [])

            for player_name in players:
                rating = None
                tier   = 'unmatched'

                # ── Tier 1/2: FIFA match ────────────────────────────
                fifa_row, fifa_score = find_fifa_match_fast(
                    player_name, nationality, nat_pools
                )
                if fifa_row:
                    rating = _fifa_sector_score(fifa_row, sector)
                    if rating is not None:
                        is_fc25 = os.path.exists(fc25_path) and fifa_row.get('_source') == 'fc25'
                        tier = 'fc25' if is_fc25 else 'fifa22'

                # ── Tier 3: TM fallback ─────────────────────────────
                if rating is None:
                    mv = tm_lookup.get(player_name)
                    if mv:
                        rating = tm_to_rating(mv)
                        if rating is not None:
                            tier = 'tm'

                if rating is not None:
                    raw[nation][sector].append(rating)
                    all_sector_ratings[sector].append(rating)
                    sources[nation][sector][tier] += 1
                else:
                    sources[nation][sector]['unmatched'] += 1

    # ── Tier 4: fill remaining unmatched with global sector median ──────
    sector_medians: dict[str, float] = {}
    for sector, ratings in all_sector_ratings.items():
        if ratings:
            s = sorted(ratings)
            mid = len(s) // 2
            sector_medians[sector] = s[mid] if len(s) % 2 else (s[mid-1] + s[mid]) / 2

    # Re-process unmatched players in each sector
    for squad_file in sorted(os.listdir(squads_dir)):
        if not squad_file.endswith('.json'):
            continue
        nation = squad_file[:-5]
        with open(os.path.join(squads_dir, squad_file), encoding='utf-8') as f:
            squad = json.load(f)

        nationality = NATIONALITY_MAP.get(nation, nation.replace('_', ' ').title())
        tm_lookup   = tm_by_nation.get(nation, {})

        for sector in TOP_K:
            players = squad.get(sector, [])
            if not players and sector == 'middle':
                players = squad.get('midfielders', [])
            if not players and sector == 'attackers':
                players = squad.get('forwards', [])

            unmatched_count = sources[nation][sector].get('unmatched', 0)
            if unmatched_count > 0 and sector_medians.get(sector):
                median = sector_medians[sector]
                for _ in range(unmatched_count):
                    raw[nation][sector].append(median)
                sources[nation][sector]['avg'] = unmatched_count
                del sources[nation][sector]['unmatched']

    # ── Compute top-K log-mean per sector per nation ─────────────────────
    raw_scores: dict[str, dict[str, float | None]] = {}
    for nation in raw:
        raw_scores[nation] = {}
        for sector, ratings in raw[nation].items():
            raw_scores[nation][sector] = top_k_log_mean(ratings, TOP_K[sector])

    # ── Min-max normalise each sector across all nations ─────────────────
    normalized: dict[str, dict[str, float | None]] = {n: {} for n in raw_scores}
    for sector in TOP_K:
        by_nation = {n: raw_scores[n][sector] for n in raw_scores}
        normed    = minmax_normalize(by_nation)
        for nation in raw_scores:
            normalized[nation][sector] = normed[nation]

    # ── Build output ─────────────────────────────────────────────────────
    avg_scores = {s: FALLBACK_SCORE for s in SECTOR_CANONICAL.values()}
    result = {}
    for nation in sorted(normalized):
        scores = {
            SECTOR_CANONICAL[sec]: normalized[nation][sec]
            for sec in TOP_K
        }
        xg_vs_avg, _ = compute_xg(scores, avg_scores)
        result[nation] = {
            **scores,
            'xg_vs_average_opponent': round(xg_vs_avg, 4),
            '_sources': sources.get(nation, {}),
        }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # ── Print summary ─────────────────────────────────────────────────────
    print(f'\nSaved {len(result)} teams to {output_path}')
    print('\nTop 20 by xG vs average opponent:')
    ranked = sorted(result.items(), key=lambda x: x[1]['xg_vs_average_opponent'], reverse=True)
    for i, (nation, s) in enumerate(ranked[:20], 1):
        src = s.get('_sources', {})
        src_str = '  '.join(
            f"{sec[0].upper()}:{d.get('fc25',0)+d.get('fifa22',0)}F/{d.get('tm',0)}TM/{d.get('avg',0)}avg"
            for sec, d in src.items()
        )
        print(
            f'  {i:2}. {nation:<35}'
            f'  xG={s["xg_vs_average_opponent"]:.3f}'
            f'  att={s["attack"] or 0:.3f}'
            f'  mid={s["midfield"] or 0:.3f}'
            f'  def={s["defense"] or 0:.3f}'
            f'  gk={s["goalkeeper"] or 0:.3f}'
        )

    # Unmatched summary
    print('\nData source coverage (FIFA / TM / median fallback):')
    for nation, s in sorted(result.items()):
        src = s.get('_sources', {})
        totals = {'fc25': 0, 'fifa22': 0, 'tm': 0, 'avg': 0}
        for sec_src in src.values():
            for k in totals:
                totals[k] += sec_src.get(k, 0)
        if totals['tm'] > 0 or totals['avg'] > 0:
            print(
                f'  {nation:<35}'
                f'  FIFA={totals["fc25"]+totals["fifa22"]:2}'
                f'  TM={totals["tm"]:2}'
                f'  avg={totals["avg"]:2}'
            )


if __name__ == '__main__':
    main()
