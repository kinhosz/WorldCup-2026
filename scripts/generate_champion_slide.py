#!/usr/bin/env python3
"""
Gera prompt Gemini para o slide Top-10 Favoritos ao Título (Model-3).
Lê simulation_results.json e produz prompt pronto para copiar no Gemini.

Uso:
    python3 scripts/generate_champion_slide.py <rodada> [n_sims_display]

Exemplo:
    python3 scripts/generate_champion_slide.py 3
    python3 scripts/generate_champion_slide.py 3 "1.000.000"
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate import DISPLAY_NAMES

FLAGS = {
    'argentina':                  '🇦🇷',
    'netherlands':                '🇳🇱',
    'portugal':                   '🇵🇹',
    'france':                     '🇫🇷',
    'brazil':                     '🇧🇷',
    'england':                    '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
    'germany':                    '🇩🇪',
    'colombia':                   '🇨🇴',
    'spain':                      '🇪🇸',
    'japan':                      '🇯🇵',
    'mexico':                     '🇲🇽',
    'morocco':                    '🇲🇦',
    'united_states_of_america':   '🇺🇸',
    'switzerland':                '🇨🇭',
    'canada':                     '🇨🇦',
    'australia':                  '🇦🇺',
    'republic_of_korea':          '🇰🇷',
    'senegal':                    '🇸🇳',
    'norway':                     '🇳🇴',
    'sweden':                     '🇸🇪',
    'uruguay':                    '🇺🇾',
    'croatia':                    '🇭🇷',
    'ivory_coast':                '🇨🇮',
    'belgium':                    '🇧🇪',
    'austria':                    '🇦🇹',
    'ecuador':                    '🇪🇨',
    'south_africa':               '🇿🇦',
    'saudi_arabia':               '🇸🇦',
    'iran':                       '🇮🇷',
    'ira':                        '🇮🇷',
    'iraq':                       '🇮🇶',
    'qatar':                      '🇶🇦',
    'tunisia':                    '🇹🇳',
    'ghana':                      '🇬🇭',
    'panama':                     '🇵🇦',
    'turkey':                     '🇹🇷',
    'scotland':                   '🏴󠁧󠁢󠁳󠁣󠁴󠁿',
    'haiti':                      '🇭🇹',
    'paraguay':                   '🇵🇾',
    'algeria':                    '🇩🇿',
    'jordan':                     '🇯🇴',
    'congo':                      '🇨🇩',
    'uzbekistan':                 '🇺🇿',
    'cape_verte':                 '🇨🇻',
    'curacao':                    '🇨🇼',
    'new_zealand':                '🇳🇿',
    'egypt':                      '🇪🇬',
    'bosnia_and_herzegovina':     '🇧🇦',
    'czech_republic':             '🇨🇿',
}

SIM_FILE = 'output/simulation_results.json'


def bar_pct(value, max_value):
    return round(value / max_value * 100)


def generate_prompt(rodada: str, n_sims_display: str = '1.000.000') -> str:
    if not os.path.exists(SIM_FILE):
        sys.exit(f'Erro: {SIM_FILE} não encontrado. Rode simulate.py primeiro.')

    with open(SIM_FILE, encoding='utf-8') as f:
        data = json.load(f)

    results = data['results']
    top10 = sorted(results.items(), key=lambda x: -x[1]['champion_pct'])[:10]
    max_pct = top10[0][1]['champion_pct']

    header = f'TOP 10 FAVORITOS AO TÍTULO · MODEL-3'
    subheader = f'Pós-R{rodada} · {n_sims_display} sims'
    footer = f'{n_sims_display} simulações · Modelo Monte Carlo · Pós-Rodada {rodada}'

    lines = [
        f'## SLIDE TOP-10 CAMPEÃO — Pós-Rodada {rodada}',
        '',
        f'> Professional sports ranking infographic. Portrait, 4:5, 1080x1350px.',
        f'> Background: deep indigo (#1E1B4B). Typography: modern bold sans-serif (Inter or equivalent). No outer borders.',
        f'>',
        f'> At the very top, centered: small uppercase muted (#93C5FD): "{header}"',
        f'> Below: thin full-width line (#312E81).',
        f'>',
        f'> One elevated dark card (#1E293B) with subtle border (#334155) and rounded corners, ~92% width, centered.',
        f'>',
        f'> Card header row: bold white (#F8FAFC) "{header}" · right-aligned small muted (#94A3B8): "{subheader}"',
        f'> Thin divider line (#334155).',
        f'>',
        f'> Ten evenly-spaced data rows inside the card. Each row has three zones:',
        f'> LEFT: a small rounded badge (background #0F172A) with bold rank number — rank 1 badge in orange (#E95420) | flag emoji | bold white (#F8FAFC) team name',
        f'> RIGHT: a short horizontal bar (height 6px, fully rounded ends) + bold percentage to the right of the bar',
        f'> Bar colors: rank 1 = orange (#E95420) · ranks 2–3 = indigo (#6366F1) · ranks 4–10 = slate (#475569)',
        f'> Bar widths are STRICTLY proportional to the percentage value. Rank 1 bar fills 100% of the right column. Do not widen a bar beyond its proportional value.',
        f'> Rank 1 percentage text in orange (#E95420); all others in white (#F8FAFC).',
        f'>',
    ]

    for rank, (team, v) in enumerate(top10, 1):
        name = DISPLAY_NAMES.get(team, team.replace('_', ' ').title())
        flag = FLAGS.get(team, '🏳')
        pct = v['champion_pct']
        bar = bar_pct(pct, max_pct)
        color_note = ' (ORANGE — rank 1)' if rank == 1 else (' (INDIGO)' if rank <= 3 else ' (SLATE)')
        lines.append(
            f'> Row {rank:>2}: badge "{rank}" | "{flag} {name}" | bar {bar}%{color_note} | "{pct:.1f}%"'
        )

    lines += [
        f'>',
        f'> Thin divider (#334155) at the bottom of the card.',
        f'>',
        f'> Below the card, centered small muted (#93C5FD): "{footer}"',
        f'>',
        f'> Do not invent any values. Render exactly the text and numbers written above.',
    ]

    return '\n'.join(lines)


if __name__ == '__main__':
    rodada = sys.argv[1] if len(sys.argv) > 1 else '?'
    n_sims = sys.argv[2] if len(sys.argv) > 2 else '1.000.000'
    print(generate_prompt(rodada, n_sims))
