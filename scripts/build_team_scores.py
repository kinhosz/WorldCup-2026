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

# Minimum plausible sector score — rejects cross-position FIFA mismatches
# (e.g., a GK matched to a field player gets near-0 GK attrs → rating 7-15)
# Any real GK in FIFA22 has avg GK attrs >> 30; any real outfield player >> 20.
MIN_SECTOR_RATING = {
    'goalkeepers': 30.0,
    'defenders':   35.0,
    'middle':      35.0,
    'attackers':   35.0,
}

TRIM_PCT = 0.30               # bottom fraction of players discarded before log-mean

# Manual overrides: (nation_key, squad_name) → FIFA22 short_name.
# Used for players whose FIFA22 short_name cannot be fuzzy-matched because
# their long_name is stored in non-Latin script (Korean, Japanese, Arabic, etc.)
# or because FIFA22 uses a very different abbreviation.
SQUAD_TO_FIFA_SHORTNAME = {
    ('republic_of_korea', 'Son Heungmin'): 'H. Son',   # FIFA22: "H. Son" / long_name in Korean
    ('spain', 'Mikel MERINO'):             'Merino',    # FIFA22: short_name="Merino"; fuzzy wrongly picks "Mikel Rico" (age 36)
}

# Sector keys (used for iteration and dict structure)
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


def load_fc25_akshay(csv_path: str) -> dict[str, list]:
    """
    Load the akshay FC25 dataset (players_info.csv) and return a name→rows
    index compatible with the FIFA22 index format.

    Column mapping for outfield players:
      pac→pace, sho→shooting, pas→passing, dri→dribbling, def→defending, phy→physic

    Column mapping for GKs (FC25 shows GK attrs in the 6 main slots):
      pac→goalkeeping_diving, sho→goalkeeping_handling,
      dri→goalkeeping_reflexes, phy→goalkeeping_positioning
    """
    idx: dict[str, list] = defaultdict(list)
    with open(csv_path, encoding='utf-8') as f:
        for i, row in enumerate(csv.DictReader(f)):
            name = row.get('player_name', '').strip()
            if not name:
                continue
            is_gk = row.get('position', '').strip().upper() == 'GK'

            norm = {
                'short_name':      name,
                'long_name':       name,
                'nationality_name': row.get('nationality', '').strip(),
                'overall':         row.get('ovr', ''),
                '_source':         'fc25',
                'sofifa_id':       f'fc25_{i}',
            }

            if is_gk:
                norm.update({
                    'goalkeeping_diving':      row.get('pac', '0'),
                    'goalkeeping_handling':    row.get('sho', '0'),
                    'goalkeeping_reflexes':    row.get('dri', '0'),
                    'goalkeeping_positioning': row.get('phy', '0'),
                    'pace': '0', 'shooting': '0', 'passing': '0',
                    'dribbling': '0', 'defending': '0', 'physic': '0',
                })
            else:
                norm.update({
                    'pace':      row.get('pac', ''),
                    'shooting':  row.get('sho', ''),
                    'passing':   row.get('pas', ''),
                    'dribbling': row.get('dri', ''),
                    'defending': row.get('def', ''),
                    'physic':    row.get('phy', ''),
                    'goalkeeping_diving': '0', 'goalkeeping_handling': '0',
                    'goalkeeping_reflexes': '0', 'goalkeeping_positioning': '0',
                })

            key = normalize(name)
            if key:
                idx[key].append(norm)
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


def trim_bottom_log_mean(values: list, trim_pct: float = TRIM_PCT) -> float | None:
    """Log-mean after dropping the bottom trim_pct fraction (by rating). Keeps at least 1."""
    valid = sorted([v for v in values if v and v > 0])
    n_drop = min(round(len(valid) * trim_pct), len(valid) - 1)
    return log_mean(valid[n_drop:])


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

_DISPLAY_NAMES = {
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

_SECTOR_HEADER = {
    'goalkeepers': 'Goalkeepers',
    'defenders':   'Defenders',
    'middle':      'Midfielders',
    'attackers':   'Attackers',
}

_TIER_LABEL = {
    'fc25':  'FC25',
    'fifa22':'FIFA22',
    'tm':    'TM',
    'avg':   'median',
}


def _nation_display(nation: str) -> str:
    return _DISPLAY_NAMES.get(nation, nation.replace('_', ' ').title())


def write_audit_report(
    player_details: dict,
    raw_scores: dict,
    normalized: dict,
    sector_medians: dict,
    result: dict,
    audit_path: str,
) -> None:
    """
    Write output/score_audit.md — per-player breakdown of data sources,
    raw ratings, and which players are in the top-K that drives each sector score.
    """
    import datetime

    lines: list[str] = []

    lines += [
        '# Score Audit — WorldCup 2026',
        '',
        f'Generated: {datetime.date.today().isoformat()}',
        '',
        'This report shows exactly how each team score was built:',
        'which data tier (FIFA22 / TM / global-median) each player used,',
        'the raw rating, and whether that player is in the top-K that feeds',
        'the sector log-mean.',
        '',
    ]

    # ── 1. Coverage summary ───────────────────────────────────────────────
    lines += [
        '## 1. Coverage Summary',
        '',
        'Sorted by median fallback rate (higher = less reliable data).',
        '',
        '| Nation | xG | FIFA | TM | Median | Fallback% |',
        '|--------|----|------|----|--------|-----------|',
    ]

    summary_rows = []
    for nation, sectors in player_details.items():
        total  = sum(len(v) for v in sectors.values())
        n_fifa = sum(sum(1 for p in v if p['tier'] in ('fc25', 'fifa22')) for v in sectors.values())
        n_tm   = sum(sum(1 for p in v if p['tier'] == 'tm')               for v in sectors.values())
        n_avg  = sum(sum(1 for p in v if p['tier'] == 'avg')              for v in sectors.values())
        xg     = result.get(nation, {}).get('xg_vs_average_opponent', 0.0)
        pct    = n_avg / total * 100 if total else 0.0
        summary_rows.append((nation, xg, n_fifa, n_tm, n_avg, total, pct))

    for nation, xg, n_fifa, n_tm, n_avg, total, pct in sorted(summary_rows, key=lambda x: -x[6]):
        lines.append(
            f'| {_nation_display(nation)} | {xg:.3f} | {n_fifa} | {n_tm} | {n_avg} | {pct:.1f}% |'
        )

    lines += ['']

    # ── 2. Global medians ─────────────────────────────────────────────────
    lines += [
        '## 2. Global Sector Medians (Tier-4 fallback value)',
        '',
        'The value assigned to every player with no FIFA22 or TM data.',
        '',
        '| Sector | Median rating |',
        '|--------|---------------|',
    ]
    for sector in ('goalkeepers', 'defenders', 'middle', 'attackers'):
        med = sector_medians.get(sector)
        val = f'{med:.2f}' if med is not None else '—'
        lines.append(f'| {_SECTOR_HEADER[sector]} | {val} |')

    lines += ['']

    # ── 3. Per-nation breakdown ───────────────────────────────────────────
    lines += [
        '## 3. Per-nation Player Breakdown',
        '',
        '**Tier key:** FIFA22 = matched in FIFA 22 dataset · TM = Transfermarket market value'
        ' · median = global sector median (no data found)',
        '',
        f'Score formula: `drop bottom {int(TRIM_PCT*100)}% by rating → log-mean of the rest'
        ' → min-max normalize across 48 nations → [0,1]`.',
        'Players marked **✗** were discarded (bottom 30%).',
        '',
    ]

    for nation in sorted(player_details):
        nat_result = result.get(nation, {})
        xg = nat_result.get('xg_vs_average_opponent', 0.0)

        lines += [
            '---',
            '',
            f'### {_nation_display(nation)}',
            '',
            (
                f'**xG vs avg opponent:** {xg:.4f} &nbsp;|&nbsp; '
                f'GK={nat_result.get("goalkeeper", 0):.4f} &nbsp;|&nbsp; '
                f'DEF={nat_result.get("defense", 0):.4f} &nbsp;|&nbsp; '
                f'MID={nat_result.get("midfield", 0):.4f} &nbsp;|&nbsp; '
                f'ATT={nat_result.get("attack", 0):.4f}'
            ),
            '',
        ]

        for sector in ('goalkeepers', 'defenders', 'middle', 'attackers'):
            raw_val    = raw_scores.get(nation, {}).get(sector)
            norm_val   = normalized.get(nation, {}).get(sector)
            raw_str    = f'{raw_val:.2f}' if raw_val  is not None else '—'
            norm_str   = f'{norm_val:.4f}' if norm_val is not None else '—'
            all_p      = player_details[nation][sector]
            n_total    = len(all_p)
            n_dropped  = sum(1 for p in all_p if p.get('dropped'))
            n_used     = n_total - n_dropped

            lines += [
                f'#### {_SECTOR_HEADER[sector]} &nbsp;({n_used}/{n_total} used · raw log-mean={raw_str} · normalized={norm_str})',
                '',
                '|   | Player | Tier | Matched as | Conf | Rating | MV (€) |',
                '|---|--------|------|------------|------|--------|--------|',
            ]

            sorted_players = sorted(all_p, key=lambda p: -(p['raw_rating'] or 0))
            for p in sorted_players:
                flag    = '✗' if p.get('dropped') else ''
                tier    = _TIER_LABEL.get(p['tier'], p['tier'] or '?')
                matched = p['matched_name'] or '—'
                conf    = f"{p['match_confidence']:.2f}" if p.get('match_confidence') else '—'
                rating  = f"{p['raw_rating']:.1f}" if p['raw_rating'] is not None else '—'
                mv      = f"{p['market_value_eur']:,}" if p.get('market_value_eur') else '—'
                lines.append(f'| {flag} | {p["name"]} | {tier} | {matched} | {conf} | {rating} | {mv} |')

            lines += ['']

    with open(audit_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'\nAudit report saved to {audit_path}')


def main():
    squads_dir        = 'squads'
    tm_path           = 'output/market_value_by_nation.json'
    fifa22_path       = 'datasets/extracted/players_22.csv'
    fc25_path         = 'datasets/extracted/players_25.csv'        # stefanoleone format (if present)
    fc25_akshay_path  = 'datasets/extracted/fc25_akshay/players_info.csv'
    output_path       = 'output/team_scores.json'
    os.makedirs('output', exist_ok=True)

    # ── Load FIFA data ──────────────────────────────────────────────────
    # Cascade: FC25 akshay → FC25 stefanoleone → FIFA 22
    # FC25 rows are prepended in the merged index so fuzzy matching prefers them.
    print('Loading FIFA data...')
    fifa_index   = load_fifa_index(fifa22_path)
    source_label = 'FIFA 22'

    if os.path.exists(fc25_path):
        print(f'  FC25 (stefanoleone) found — merging...')
        fc25_index = load_fifa_index(fc25_path)
        for key, rows in fc25_index.items():
            fifa_index[key] = rows + fifa_index.get(key, [])
        source_label = 'FC25(stefan) + FIFA 22'

    if os.path.exists(fc25_akshay_path):
        print(f'  FC25 (akshay) found — merging (highest priority)...')
        fc25_akshay_index = load_fc25_akshay(fc25_akshay_path)
        for key, rows in fc25_akshay_index.items():
            fifa_index[key] = rows + fifa_index.get(key, [])
        source_label = 'FC25(akshay) + ' + source_label

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
    sources: dict[str, dict[str, dict]] = {}        # {nation: {sector: {fc25,fifa22,tm,avg}}}
    player_details: dict[str, dict[str, list]] = {} # {nation: {sector: [player_dict]}}

    all_sector_ratings: dict[str, list] = defaultdict(list)  # for Tier-4 global median

    for squad_file in sorted(os.listdir(squads_dir)):
        if not squad_file.endswith('.json'):
            continue
        nation = squad_file[:-5]
        with open(os.path.join(squads_dir, squad_file), encoding='utf-8') as f:
            squad = json.load(f)

        nationality = NATIONALITY_MAP.get(nation, nation.replace('_', ' ').title())
        tm_lookup   = tm_by_nation.get(nation, {})

        raw[nation]            = {s: [] for s in TOP_K}
        sources[nation]        = {s: {'fc25': 0, 'fifa22': 0, 'tm': 0, 'unmatched': 0} for s in TOP_K}
        player_details[nation] = {s: [] for s in TOP_K}

        for sector in TOP_K:
            players = squad.get(sector, [])
            if not players and sector == 'middle':
                players = squad.get('midfielders', [])
            if not players and sector == 'attackers':
                players = squad.get('forwards', [])

            for player_name in players:
                rating           = None
                tier             = None
                matched_name     = None
                match_confidence = 0.0
                market_value_eur = None

                # ── Tier 1/2: FIFA match ────────────────────────────
                # Check manual override first (handles non-Latin FIFA22 names)
                override_sname = SQUAD_TO_FIFA_SHORTNAME.get((nation, player_name))
                if override_sname:
                    nat_key = normalize(nationality)
                    target  = normalize(override_sname)
                    fifa_row = next(
                        (r for r in nat_pools.get(nat_key, [])
                         if normalize(r.get('short_name', '')) == target),
                        None
                    )
                    fifa_score = 1.0 if fifa_row else 0.0
                else:
                    fifa_row, fifa_score = find_fifa_match_fast(
                        player_name, nationality, nat_pools
                    )
                if fifa_row:
                    rating = _fifa_sector_score(fifa_row, sector)
                    if rating is not None and rating >= MIN_SECTOR_RATING.get(sector, 0):
                        is_fc25 = fifa_row.get('_source') == 'fc25'
                        tier             = 'fc25' if is_fc25 else 'fifa22'
                        matched_name     = fifa_row.get('short_name', player_name)
                        match_confidence = fifa_score
                    else:
                        rating = None  # wrong match (cross-position or wrong person); fall through

                # ── Tier 3: TM fallback ─────────────────────────────
                if rating is None:
                    mv = tm_lookup.get(player_name)
                    if mv:
                        rating = tm_to_rating(mv)
                        if rating is not None:
                            tier             = 'tm'
                            market_value_eur = int(mv)

                player_details[nation][sector].append({
                    'name':             player_name,
                    'tier':             tier,           # None → filled with 'avg' in median pass
                    'matched_name':     matched_name,
                    'match_confidence': round(match_confidence, 3) if match_confidence else None,
                    'raw_rating':       rating,
                    'market_value_eur': market_value_eur,
                })

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

    # Fill median into player_details and raw for unmatched players
    for nation in player_details:
        for sector in TOP_K:
            unmatched = [p for p in player_details[nation][sector] if p['raw_rating'] is None]
            if unmatched and sector_medians.get(sector):
                median = sector_medians[sector]
                for p in unmatched:
                    p['tier']       = 'avg'
                    p['raw_rating'] = round(median, 2)
                    raw[nation][sector].append(median)
                sources[nation][sector]['avg'] = len(unmatched)
                sources[nation][sector].pop('unmatched', None)

    # ── Compute trimmed log-mean (drop bottom 30%) per sector per nation ──
    raw_scores: dict[str, dict[str, float | None]] = {}
    for nation in raw:
        raw_scores[nation] = {}
        for sector, ratings in raw[nation].items():
            raw_scores[nation][sector] = trim_bottom_log_mean(ratings)

    # ── Mark dropped players (bottom TRIM_PCT by rating) in player_details ─
    for nation in player_details:
        for sector in TOP_K:
            players_list = player_details[nation][sector]
            valid = [p for p in players_list if p['raw_rating'] is not None]
            n_drop = min(round(len(valid) * TRIM_PCT), len(valid) - 1)
            sorted_asc = sorted(valid, key=lambda p: p['raw_rating'])
            dropped_names = {p['name'] for p in sorted_asc[:n_drop]}
            for p in players_list:
                p['dropped'] = p['name'] in dropped_names

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

    # ── Audit report ──────────────────────────────────────────────────────
    audit_path = 'output/score_audit.md'
    write_audit_report(
        player_details=player_details,
        raw_scores=raw_scores,
        normalized=normalized,
        sector_medians=sector_medians,
        result=result,
        audit_path=audit_path,
    )


if __name__ == '__main__':
    main()
