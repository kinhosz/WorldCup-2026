#!/usr/bin/env python3
"""
round_report.py — relatório visual de uma rodada.

Gera um PNG com todos os jogos da rodada: top-3 placares previstos,
probabilidades de resultado, resultado real e (opcional) palpite do usuário.

Uso:
    python3 scripts/round_report.py 1
    python3 scripts/round_report.py 1 --palpites output/palpites_r1.json
"""

import json
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate import GROUPS

STATE_FILE  = "output/copa_real_state.json"
ODDS_DIR    = "output"
OUT_FILE    = "output/round_{}_report.png"

_DISPLAY = {
    'united_states_of_america': 'USA',
    'republic_of_korea':        'South Korea',
    'bosnia_and_herzegovina':   'Bosnia',
    'cape_verte':               'Cape Verde',
    'ivory_coast':              "Côte d'Ivoire",
    'ira':                      'Iran',
    'new_zealand':              'New Zealand',
    'saudi_arabia':             'Saudi Arabia',
    'south_africa':             'South Africa',
    'czech_republic':           'Czech Rep.',
}

# ── cores ──────────────────────────────────────────────────────────────
BG       = '#0d1117'
CARD_BG  = '#161b22'
CARD_BORDER = '#30363d'
TEXT_H   = '#e6edf3'
TEXT_S   = '#8b949e'
GREEN    = '#3fb950'   # acertou
YELLOW   = '#d29922'   # perto / palpite
RED      = '#f85149'   # errou
BLUE     = '#58a6ff'
ORANGE   = '#f0883e'
PURPLE   = '#bc8cff'


def dn(t):
    return _DISPLAY.get(t, t.replace('_', ' ').title())


def load_odds(ta, tb):
    path = os.path.join(ODDS_DIR, f"odds_{ta}_vs_{tb}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        d = json.load(f)
    # normaliza formato antigo {home/away/home_win/away_win} → novo {team_a/team_b/odds}
    if 'odds' not in d and 'home_win' in d:
        d = {
            'team_a':     d.get('home', ta),
            'team_b':     d.get('away', tb),
            'n_sims':     d.get('n_sims', 0),
            'xg':         {d.get('home', ta): d.get('xg_home', 0),
                           d.get('away', tb): d.get('xg_away', 0)},
            'odds':       {d.get('home', ta): d['home_win'],
                           'draw':            d['draw'],
                           d.get('away', tb): d['away_win']},
            'top_scores': d.get('top_scores', []),
        }
    return d


def load_real_results():
    with open(STATE_FILE) as f:
        state = json.load(f)
    results = {}
    for grp, games in state["group_results"].items():
        for key, (ga, gb) in games.items():
            ta, tb = key.split("|")
            results[(ta, tb)] = (ga, gb)
    return results


def round_matchups(round_num):
    """Retorna os pares de cada rodada. Rodada 1 = primeiro jogo de cada grupo."""
    # Cada grupo de 4 times tem 3 rodadas de fase de grupo.
    # Rodada 1: time[0] vs time[1], time[2] vs time[3]
    # Rodada 2: time[0] vs time[2], time[1] vs time[3]
    # Rodada 3: time[0] vs time[3], time[1] vs time[2]
    schedules = {
        1: [(0, 1), (2, 3)],
        2: [(0, 2), (1, 3)],
        3: [(0, 3), (1, 2)],
    }
    pairs = schedules[round_num]
    matchups = []
    for grp, teams in sorted(GROUPS.items()):
        for i, j in pairs:
            matchups.append((grp, teams[i], teams[j]))
    return matchups


def score_color(predicted_score, real_score, palpite_score=None):
    """Cor para cada placar previsto no top-3."""
    if predicted_score == f"{real_score[0]}-{real_score[1]}":
        return GREEN
    # Verifica se acertou o resultado (W/D/L)
    pg, pa = map(int, predicted_score.split('-'))
    rg, ra = real_score
    pred_outcome = 'w' if pg > pa else ('d' if pg == pa else 'l')
    real_outcome = 'w' if rg > ra else ('d' if rg == ra else 'l')
    if pred_outcome == real_outcome:
        return YELLOW
    return TEXT_S


def draw_game_card(ax, ta, tb, odds, real, palpite, show_real):
    """Desenha um card de jogo no axes dado."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # fundo do card
    card = FancyBboxPatch((0.01, 0.02), 0.98, 0.96,
                          boxstyle="round,pad=0.02",
                          facecolor=CARD_BG, edgecolor=CARD_BORDER, linewidth=1)
    ax.add_patch(card)

    if odds is None:
        ax.text(0.5, 0.5, f"{dn(ta)} vs {dn(tb)}\n(odds não disponíveis)",
                ha='center', va='center', color=TEXT_S, fontsize=8)
        return

    odds_ta = odds.get('team_a', ta)
    odds_tb = odds.get('team_b', tb)
    p_a   = odds['odds'].get(odds_ta, odds['odds'].get(ta, 33)) / 100
    p_d   = odds['odds']['draw'] / 100
    p_b   = odds['odds'].get(odds_tb, odds['odds'].get(tb, 33)) / 100
    top3  = odds['top_scores'][:3]

    # ── nomes dos times ──────────────────────────────────────────────
    ax.text(0.18, 0.88, dn(ta), ha='center', va='center',
            color=TEXT_H, fontsize=7.5, fontweight='bold')
    ax.text(0.82, 0.88, dn(tb), ha='center', va='center',
            color=TEXT_H, fontsize=7.5, fontweight='bold')
    ax.text(0.50, 0.88, 'vs', ha='center', va='center',
            color=TEXT_S, fontsize=7)

    # ── barra de probabilidades ───────────────────────────────────────
    bar_y, bar_h = 0.73, 0.08
    ax.barh(bar_y, p_a,       height=bar_h, left=0.04,           color=BLUE,   alpha=0.85)
    ax.barh(bar_y, p_d,       height=bar_h, left=0.04 + p_a,     color='#484f58', alpha=0.85)
    ax.barh(bar_y, p_b,       height=bar_h, left=0.04 + p_a + p_d, color=ORANGE, alpha=0.85)
    ax.text(0.04 + p_a/2,   bar_y, f"{p_a*100:.0f}%", ha='center', va='center',
            color='white', fontsize=6.5, fontweight='bold')
    ax.text(0.04 + p_a + p_d/2, bar_y, f"{p_d*100:.0f}%", ha='center', va='center',
            color='white', fontsize=6.5)
    ax.text(0.04 + p_a + p_d + p_b/2, bar_y, f"{p_b*100:.0f}%", ha='center', va='center',
            color='white', fontsize=6.5, fontweight='bold')

    # ── top-3 placares ────────────────────────────────────────────────
    ax.text(0.5, 0.62, 'Modelo previu:', ha='center', va='center',
            color=TEXT_S, fontsize=6.5)

    for idx, entry in enumerate(top3):
        score_str = entry['score']
        pct       = entry['pct']
        x_pos     = 0.18 + idx * 0.32

        col = TEXT_S
        if show_real and real:
            col = score_color(score_str, real)

        ax.text(x_pos, 0.50, score_str, ha='center', va='center',
                color=col, fontsize=10, fontweight='bold')
        ax.text(x_pos, 0.40, f"{pct:.1f}%", ha='center', va='center',
                color=col, fontsize=7)

    # ── resultado real ────────────────────────────────────────────────
    if show_real and real:
        real_str = f"{real[0]}–{real[1]}"
        top_scores_list = [e['score'] for e in top3]
        exact = f"{real[0]}-{real[1]}" in top_scores_list

        # acertou outcome?
        rg, ra = real
        real_outcome = 'w' if rg > ra else ('d' if rg == ra else 'l')
        model_top = top3[0]['score']
        pg, pa_g = map(int, model_top.split('-'))
        model_outcome = 'w' if pg > pa_g else ('d' if pg == pa_g else 'l')
        outcome_ok = real_outcome == model_outcome

        res_color = GREEN if exact else (YELLOW if outcome_ok else RED)
        icon = '✓' if exact else ('~' if outcome_ok else '✗')

        ax.text(0.5, 0.27, 'Real:', ha='center', va='center',
                color=TEXT_S, fontsize=6.5)
        ax.text(0.5, 0.16, f"{icon} {real_str}", ha='center', va='center',
                color=res_color, fontsize=11, fontweight='bold')
    else:
        ax.text(0.5, 0.22, '(ainda não jogou)', ha='center', va='center',
                color=TEXT_S, fontsize=7, style='italic')

    # ── palpite do usuário ────────────────────────────────────────────
    if palpite:
        ax.text(0.5, 0.06, f"Palpite: {palpite}", ha='center', va='center',
                color=PURPLE, fontsize=7.5, fontweight='bold')


def generate_round_report(round_num, palpites=None):
    matchups = round_matchups(round_num)
    real     = load_real_results()

    n  = len(matchups)
    cols = 4
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4.2, rows * 3.2))
    fig.patch.set_facecolor(BG)
    fig.suptitle(f'Copa do Mundo 2026 — Rodada {round_num}   '
                 f'(✓ placar exato  ~ acertou resultado  ✗ errou)',
                 color=TEXT_H, fontsize=13, fontweight='bold', y=0.99)

    axes_flat = axes.flatten() if rows > 1 else np.array(axes).flatten()

    for idx, (grp, ta, tb) in enumerate(matchups):
        ax = axes_flat[idx]
        odds    = load_odds(ta, tb)
        result  = real.get((ta, tb))
        palpite = (palpites or {}).get(f"{ta}|{tb}")
        show_real = result is not None
        draw_game_card(ax, ta, tb, odds, result, palpite, show_real)
        ax.set_title(f'Grupo {grp}', color=TEXT_S, fontsize=7.5, pad=2)

    # esconde eixos vazios
    for idx in range(len(matchups), len(axes_flat)):
        axes_flat[idx].axis('off')
        axes_flat[idx].set_facecolor(BG)

    # legenda
    patches = [
        mpatches.Patch(color=GREEN,  label='Placar exato'),
        mpatches.Patch(color=YELLOW, label='Resultado certo (W/D/L)'),
        mpatches.Patch(color=RED,    label='Errou'),
        mpatches.Patch(color=BLUE,   label='Prob. time A'),
        mpatches.Patch(color=ORANGE, label='Prob. time B'),
        mpatches.Patch(color=PURPLE, label='Seu palpite'),
    ]
    fig.legend(handles=patches, loc='lower center', ncol=6,
               facecolor=CARD_BG, edgecolor=CARD_BORDER,
               labelcolor=TEXT_H, fontsize=8, framealpha=1,
               bbox_to_anchor=(0.5, 0.005))

    plt.tight_layout(rect=[0, 0.04, 1, 0.975])
    out = OUT_FILE.format(round_num)
    plt.savefig(out, dpi=140, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f"Relatório salvo em {out}")


def main():
    args = sys.argv[1:]
    if not args:
        print("Uso: python3 scripts/round_report.py <rodada> [--palpites <arquivo.json>]")
        sys.exit(1)

    round_num = int(args[0])
    palpites  = None

    if '--palpites' in args:
        idx = args.index('--palpites')
        with open(args[idx + 1]) as f:
            palpites = json.load(f)

    generate_round_report(round_num, palpites)


if __name__ == '__main__':
    main()
