#!/usr/bin/env python3
"""
r1_comparison.py — compara modelo anterior vs calibrado em todos os jogos da R1.

Lê os odds antigos (gerados com pesos originais) e roda novas simulações
com os pesos calibrados. Gera output/r1_calibrated_comparison.md.
"""

import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate import GROUPS, compute_xg

N_SIMS = 100_000
TEAM_SCORES_FILE = "output/team_scores.json"
STATE_FILE       = "output/copa_real_state.json"
ODDS_DIR         = "output"
OUT_FILE         = "output/r1_calibrated_comparison.md"

R1_PAIRS = [(0, 1), (2, 3)]

DISPLAY = {
    'united_states_of_america': 'EUA',
    'republic_of_korea':        'Coreia do Sul',
    'bosnia_and_herzegovina':   'Bósnia',
    'cape_verte':               'Cabo Verde',
    'ivory_coast':              "Côte d'Ivoire",
    'ira':                      'Irã',
    'new_zealand':              'Nova Zelândia',
    'saudi_arabia':             'Arábia Saudita',
    'south_africa':             'África do Sul',
    'czech_republic':           'Tchéquia',
    'mexico':                   'México',
    'canada':                   'Canadá',
    'brazil':                   'Brasil',
    'haiti':                    'Haiti',
    'germany':                  'Alemanha',
    'netherlands':              'Holanda',
    'belgium':                  'Bélgica',
    'spain':                    'Espanha',
    'france':                   'França',
    'argentina':                'Argentina',
    'austria':                  'Áustria',
    'ecuador':                  'Equador',
    'scotland':                 'Escócia',
    'switzerland':              'Suíça',
    'morocco':                  'Marrocos',
    'turkey':                   'Turquia',
    'tunisia':                  'Tunísia',
    'sweden':                   'Suécia',
    'egypt':                    'Egito',
    'uruguay':                  'Uruguai',
    'senegal':                  'Senegal',
    'iraq':                     'Iraque',
    'norway':                   'Noruega',
    'algeria':                  'Argélia',
    'jordan':                   'Jordânia',
}


def dn(t):
    return DISPLAY.get(t, t.replace('_', ' ').title())


def load_old_odds(ta, tb):
    path = os.path.join(ODDS_DIR, f"odds_{ta}_vs_{tb}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        d = json.load(f)
    if 'odds' not in d and 'home_win' in d:
        d = {
            'team_a': d.get('home', ta),
            'team_b': d.get('away', tb),
            'odds': {
                d.get('home', ta): d['home_win'],
                'draw':            d['draw'],
                d.get('away', tb): d['away_win'],
            },
            'top_scores': d.get('top_scores', []),
            'xg': {d.get('home', ta): d.get('xg_home', 0),
                   d.get('away', tb): d.get('xg_away', 0)},
        }
    return d


def sim_match(ta, tb, scores):
    xg_a, xg_b = compute_xg(scores[ta], scores[tb])
    goals_a = np.random.poisson(xg_a, N_SIMS)
    goals_b = np.random.poisson(xg_b, N_SIMS)

    # top scores
    from collections import Counter
    score_counts = Counter(zip(goals_a.tolist(), goals_b.tolist()))
    top = sorted(score_counts.items(), key=lambda x: -x[1])[:3]
    top_scores = [{'score': f"{g[0]}-{g[1]}", 'pct': round(c / N_SIMS * 100, 1)}
                  for g, c in top]

    p_a    = float(np.mean(goals_a > goals_b))
    p_draw = float(np.mean(goals_a == goals_b))
    p_b    = float(np.mean(goals_a < goals_b))

    return {
        'xg_a': round(xg_a, 3),
        'xg_b': round(xg_b, 3),
        'p_a': round(p_a * 100, 1),
        'p_draw': round(p_draw * 100, 1),
        'p_b': round(p_b * 100, 1),
        'top_scores': top_scores,
    }


def outcome(ga, gb):
    if ga > gb: return 'a'
    if ga < gb: return 'b'
    return 'draw'


def result_icon(predicted_top1, real):
    pred_g, pred_a = map(int, predicted_top1.split('-'))
    real_g, real_a = real
    if pred_g == real_g and pred_a == real_a:
        return '✅'
    if outcome(pred_g, pred_a) == outcome(real_g, real_a):
        return '🟡'
    return '❌'


def main():
    with open(TEAM_SCORES_FILE) as f:
        scores = json.load(f)
    with open(STATE_FILE) as f:
        state = json.load(f)

    real_results = {}
    for grp, games in state['group_results'].items():
        for key, (ga, gb) in games.items():
            ta, tb = key.split('|')
            real_results[(ta, tb)] = (ga, gb)

    rows = []
    for grp, teams in sorted(GROUPS.items()):
        for i, j in R1_PAIRS:
            ta, tb = teams[i], teams[j]
            real = real_results.get((ta, tb))
            old  = load_old_odds(ta, tb)
            new  = sim_match(ta, tb, scores)
            rows.append((grp, ta, tb, real, old, new))

    lines = []
    lines.append("# Rodada 1 — Modelo Anterior vs Calibrado\n")
    lines.append(f"**Simulações:** {N_SIMS:,} por jogo · **Pesos calibrados:** BASE_XG=1.1192, w_att=0.90, w_def=0.2922, w_gk=0.50\n")
    lines.append("Legenda: ✅ placar exato · 🟡 resultado certo · ❌ errou\n")
    lines.append("---\n")

    # contadores
    old_exact = old_outcome = new_exact = new_outcome = 0
    old_draw_ok = new_draw_ok = 0
    n_draws = 0

    lines.append("| Grp | Jogo | Real | xG ant | Top-1 ant | Res ant | xG cal | Top-1 cal | Res cal |")
    lines.append("|-----|------|------|--------|-----------|---------|--------|-----------|---------|")

    for grp, ta, tb, real, old, new in rows:
        if real is None:
            real_str = "(pendente)"
            old_icon = new_icon = "—"
            old_top1 = new['top_scores'][0]['score'] if new['top_scores'] else "?"
            old_xg = "—"
            new_xg = f"{new['xg_a']} vs {new['xg_b']}"
            lines.append(
                f"| {grp} | {dn(ta)} vs {dn(tb)} | {real_str} "
                f"| {old_xg} | {old_top1} | {old_icon} "
                f"| {new_xg} | {new['top_scores'][0]['score'] if new['top_scores'] else '?'} | {new_icon} |"
            )
            continue

        real_str = f"{real[0]}-{real[1]}"
        real_out = outcome(real[0], real[1])
        if real_out == 'draw':
            n_draws += 1

        # old model
        if old and old.get('top_scores'):
            old_top1 = old['top_scores'][0]['score']
            old_xg_a = old.get('xg', {}).get(old.get('team_a', ta), '?')
            old_xg_b = old.get('xg', {}).get(old.get('team_b', tb), '?')
            old_xg = f"{old_xg_a} vs {old_xg_b}"
            old_icon = result_icon(old_top1, real)
            if old_icon == '✅': old_exact += 1
            if old_icon in ('✅', '🟡'): old_outcome += 1
            if real_out == 'draw' and outcome(*map(int, old_top1.split('-'))) == 'draw':
                old_draw_ok += 1
        else:
            old_top1 = "?"
            old_xg = "?"
            old_icon = "—"

        # new model
        new_top1 = new['top_scores'][0]['score'] if new['top_scores'] else "?"
        new_xg = f"{new['xg_a']} vs {new['xg_b']}"
        new_icon = result_icon(new_top1, real)
        if new_icon == '✅': new_exact += 1
        if new_icon in ('✅', '🟡'): new_outcome += 1
        if real_out == 'draw' and outcome(*map(int, new_top1.split('-'))) == 'draw':
            new_draw_ok += 1

        lines.append(
            f"| {grp} | {dn(ta)} vs {dn(tb)} | **{real_str}** "
            f"| {old_xg} | {old_top1} | {old_icon} "
            f"| {new_xg} | {new_top1} | {new_icon} |"
        )

    n_games = sum(1 for _, _, _, r, _, _ in rows if r is not None)

    lines.append("\n---\n")
    lines.append("## Resumo\n")
    lines.append("| Métrica | Modelo anterior | Calibrado | Δ |")
    lines.append("|---------|-----------------|-----------|---|")
    lines.append(f"| Placar exato | {old_exact}/{n_games} = {old_exact/n_games*100:.1f}% | {new_exact}/{n_games} = {new_exact/n_games*100:.1f}% | {new_exact - old_exact:+d} |")
    lines.append(f"| Resultado certo (W/D/L) | {old_outcome}/{n_games} = {old_outcome/n_games*100:.1f}% | {new_outcome}/{n_games} = {new_outcome/n_games*100:.1f}% | {new_outcome - old_outcome:+d} |")
    lines.append(f"| Empates acertados | {old_draw_ok}/{n_draws} = {old_draw_ok/n_draws*100:.1f}% | {new_draw_ok}/{n_draws} = {new_draw_ok/n_draws*100:.1f}% | {new_draw_ok - old_draw_ok:+d} |")

    lines.append("\n---\n")
    lines.append("## xG por jogo — antes vs depois\n")
    lines.append("| Jogo | Real | xG ant A | xG ant B | xG cal A | xG cal B | Δ xG_A | Δ xG_B |")
    lines.append("|------|------|----------|----------|----------|----------|--------|--------|")

    for grp, ta, tb, real, old, new in rows:
        if real is None:
            continue
        real_str = f"{real[0]}-{real[1]}"
        try:
            old_a = float(old['xg'].get(old.get('team_a', ta), 0)) if old and 'xg' in old else None
            old_b = float(old['xg'].get(old.get('team_b', tb), 0)) if old and 'xg' in old else None
        except Exception:
            old_a = old_b = None

        if old_a is not None:
            da = round(new['xg_a'] - old_a, 3)
            db = round(new['xg_b'] - old_b, 3)
            lines.append(
                f"| {dn(ta)} vs {dn(tb)} | {real_str} "
                f"| {old_a} | {old_b} | {new['xg_a']} | {new['xg_b']} "
                f"| {da:+.3f} | {db:+.3f} |"
            )
        else:
            lines.append(
                f"| {dn(ta)} vs {dn(tb)} | {real_str} "
                f"| — | — | {new['xg_a']} | {new['xg_b']} | — | — |"
            )

    with open(OUT_FILE, 'w') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Salvo em {OUT_FILE}")
    print(f"\nAnterior:  {old_exact}/{n_games} exatos, {old_outcome}/{n_games} resultado, {old_draw_ok}/{n_draws} empates")
    print(f"Calibrado: {new_exact}/{n_games} exatos, {new_outcome}/{n_games} resultado, {new_draw_ok}/{n_draws} empates")


if __name__ == '__main__':
    main()
