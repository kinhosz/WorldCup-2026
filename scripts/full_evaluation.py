#!/usr/bin/env python3
"""
Reavaliação retroativa de todas as partidas já disputadas com o modelo ATIVO
(lido dinamicamente de output/calibrated_weights_sa.json — hoje o Model7).

Gera:
  output/model7_full_evaluation.md
  output/model7_evaluation.html

Uso:
    python3 scripts/full_evaluation.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simulate import compute_xg, DISPLAY_NAMES
from calibrate_sa import (
    GROUPS, _group_round, _parse_score, _pmf, _outcome_probs, _score_bonus,
    MAX_GOALS, SCORE_BONUS_GRID,
)

STATE_FILE   = "output/copa_real_state.json"
SCORES_FILE  = "output/team_scores.json"
WEIGHTS_FILE = "output/calibrated_weights_sa.json"
OUT_MD       = "output/model7_full_evaluation.md"
OUT_HTML     = "output/model7_evaluation.html"

ROUND_LABELS = {
    'r1': 'Rodada 1', 'r2': 'Rodada 2', 'r3': 'Rodada 3',
    'r32': 'Round of 32', 'r16': 'Oitavas de Final',
    'qf': 'Quartas de Final', 'sf': 'Semifinal', 'final': 'Final + 3º Lugar',
}
GROUP_ROUNDS    = ['r1', 'r2', 'r3']
KNOCKOUT_ROUNDS = ['r32', 'r16', 'qf', 'sf']
ROUND_ORDER     = GROUP_ROUNDS + KNOCKOUT_ROUNDS

# Jogos ainda não disputados — lidos direto dos odds já gerados por match_odds.py,
# sem recomputar nada (garante consistência com o que já foi comunicado/salvo).
PENDING_FILES = [
    ("output/odds_france_vs_england.json", "3º Lugar"),
    ("output/odds_spain_vs_argentina.json", "Final"),
]


def build_team_table(scores, weights):
    """Ranking das 48 seleções só com números do Model7: scores de setor
    (team_scores.json, sem relação com o modelo) + biases + xG vs adversário
    médio (recomputado aqui com compute_xg do Model7 — o xg_vs_average_opponent
    salvo em team_scores.json é de uma calibração antiga, não usar)."""
    all_teams = sorted({t for members in GROUPS.values() for t in members})
    team_group = {t: g for g, members in GROUPS.items() for t in members}

    sectors = ['goalkeeper', 'defense', 'midfield', 'attack']
    avg_scores = {
        s: sum(scores[t][s] for t in all_teams if t in scores) / len([t for t in all_teams if t in scores])
        for s in sectors
    }

    biases = weights.get('biases', {})
    rows = []
    for t in all_teams:
        if t not in scores:
            continue
        xg_avg, _ = compute_xg(scores[t], avg_scores, t, None)
        b = biases.get(t, {'att_bias': 1.0, 'def_bias': 1.0})
        att_b, def_b = b['att_bias'], b['def_bias']
        notes = []
        if att_b - 1 > 0.15:
            notes.append("ataque bem acima do esperado")
        elif att_b - 1 < -0.15:
            notes.append("ataque bem abaixo do esperado")
        if def_b - 1 > 0.15:
            notes.append("defesa bem acima do esperado")
        elif def_b - 1 < -0.15:
            notes.append("defesa bem abaixo do esperado")
        rows.append({
            'team': t, 'group': team_group[t],
            'gk': scores[t]['goalkeeper'], 'def': scores[t]['defense'],
            'mid': scores[t]['midfield'], 'att': scores[t]['attack'],
            'att_bias': att_b, 'def_bias': def_b,
            'xg_avg': xg_avg, 'note': " · ".join(notes),
        })
    rows.sort(key=lambda r: -r['xg_avg'])
    return rows


def render_teams_md(rows, model_label):
    lines = [
        f"## Seleções — Scores e Biases ({model_label})",
        "",
        f"Ranking das 48 seleções só com dados do {model_label}: scores de setor (GK/DEF/MID/ATT, 0.1–1.0, de `team_scores.json`) "
        f"+ biases por seleção calibrados pelo {model_label} + xG contra um adversário médio (recomputado com os pesos e biases "
        f"ativos — não usa o `xg_vs_average_opponent` salvo em `team_scores.json`, que é de uma calibração antiga sem biases).",
        "",
        "| # | Seleção | Grupo | GK | DEF | MID | ATT | Att Bias | Def Bias | xG vs média | Nota |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        lines.append(
            f"| {i} | {dn(r['team'])} | {r['group']} | {r['gk']:.3f} | {r['def']:.3f} | {r['mid']:.3f} | {r['att']:.3f} | "
            f"{r['att_bias']:.2f} | {r['def_bias']:.2f} | {r['xg_avg']:.2f} | {r['note']} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_teams_panel_html(rows, model_label):
    def bias_cls(v):
        if v - 1 > 0.15: return 'ok'
        if v - 1 < -0.15: return 'no'
        return 'muted'

    rows_html = []
    for i, r in enumerate(rows, 1):
        rows_html.append(
            f'<tr>'
            f'<td class="mono">{i}</td>'
            f'<td class="teams">{dn(r["team"])}</td>'
            f'<td>{r["group"]}</td>'
            f'<td class="mono">{r["gk"]:.3f}</td>'
            f'<td class="mono">{r["def"]:.3f}</td>'
            f'<td class="mono">{r["mid"]:.3f}</td>'
            f'<td class="mono">{r["att"]:.3f}</td>'
            f'<td class="mono"><span class="pill {bias_cls(r["att_bias"])}">{r["att_bias"]:.2f}</span></td>'
            f'<td class="mono"><span class="pill {bias_cls(r["def_bias"])}">{r["def_bias"]:.2f}</span></td>'
            f'<td class="mono">{r["xg_avg"]:.2f}</td>'
            f'<td class="note">{r["note"]}</td>'
            f'</tr>'
        )
    head = ('<th>#</th><th>Seleção</th><th>Grupo</th><th>GK</th><th>DEF</th><th>MID</th><th>ATT</th>'
            '<th>Att Bias</th><th>Def Bias</th><th>xG vs média</th><th>Nota</th>')
    return (
        f'<section class="panel" id="panel-teams">'
        f'<div class="panel-head"><h2>Seleções — Scores e Biases</h2>'
        f'<span class="panel-stat">48 seleções &middot; ranqueadas por xG vs adversário médio ({model_label})</span></div>'
        f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(rows_html)}</tbody></table></div>'
        f'</section>'
    )


def load_pending():
    pending = []
    for path, label in PENDING_FILES:
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        d['label'] = label
        pending.append(d)
    return pending


def dn(t):
    return DISPLAY_NAMES.get(t, t.replace("_", " ").title())


def _knockout_round(match_id):
    mid = int(match_id)
    if mid <= 88:  return 'r32'
    if mid <= 96:  return 'r16'
    if mid <= 100: return 'qf'
    if mid <= 102: return 'sf'
    return 'final'


def top_scores_grid(pa, pb, n=3):
    grid = [((i, j), pa[i] * pb[j]) for i in range(len(pa)) for j in range(len(pb))]
    grid.sort(key=lambda x: -x[1])
    return grid[:n]


def bonus_label(bonus):
    if bonus >= 0.999:  return "top-1"
    if bonus >= 0.666:  return "top-2"
    if bonus >= 0.443:  return "top-3"
    return "fora do top-3"


def build_matches(state, scores):
    matches = []

    for grp, games in state['group_results'].items():
        for key, (ga, gb) in games.items():
            ta, tb = key.split('|')
            if ta not in scores or tb not in scores:
                continue
            rnd = f"r{_group_round(ta, tb)}"
            outcome = 'a' if ga > gb else ('b' if ga < gb else 'draw')
            matches.append({'round': rnd, 'team_a': ta, 'team_b': tb,
                            'goals_a': ga, 'goals_b': gb, 'outcome': outcome,
                            'score_display': f"{ga}–{gb}", 'note': None})

    for mid, game in state.get('knockout_results', {}).items():
        ta, tb = game['home'], game['away']
        if ta not in scores or tb not in scores:
            continue
        ga, gb = _parse_score(game['score_str'], game.get('note'))
        rnd = _knockout_round(mid)
        if rnd == 'final':
            continue
        winner_side = 'a' if game['winner'] == ta else 'b'
        note = game.get('note')
        score_display = f"{ga}–{gb}"
        if note in ('AET', 'PEN'):
            score_display += f" ({note})"
        matches.append({'round': rnd, 'team_a': ta, 'team_b': tb,
                        'goals_a': ga, 'goals_b': gb, 'winner_side': winner_side,
                        'winner': game['winner'], 'score_display': score_display,
                        'note': note, 'match_id': int(mid)})

    return matches


def evaluate(matches, scores):
    for m in matches:
        xg_a, xg_b = compute_xg(scores[m['team_a']], scores[m['team_b']], m['team_a'], m['team_b'])
        pa = _pmf(xg_a, MAX_GOALS)
        pb = _pmf(xg_b, MAX_GOALS)
        win_a, draw, win_b = _outcome_probs(pa, pb)
        top3 = top_scores_grid(pa, pb, 3)

        m['xg_a'], m['xg_b'] = xg_a, xg_b
        m['top3'] = top3

        if m['round'] in KNOCKOUT_ROUNDS:
            adv_a = win_a + 0.5 * draw
            adv_b = win_b + 0.5 * draw
            pick_side = 'a' if adv_a >= 0.5 else 'b'
            m['pick_team'] = m[f'team_{pick_side}']
            m['confidence'] = max(adv_a, adv_b)
            m['correct'] = (pick_side == m['winner_side'])
            bonus = _score_bonus(pa, pb, m['goals_a'], m['goals_b'], grid=SCORE_BONUS_GRID)
            m['rank_label'] = bonus_label(bonus)
            m['bonus'] = bonus
        else:
            probs = {'a': win_a, 'draw': draw, 'b': win_b}
            pick_cat = max(probs, key=probs.get)
            m['pick_team'] = {'a': m['team_a'], 'b': m['team_b'], 'draw': 'Empate'}[pick_cat]
            m['confidence'] = probs[pick_cat]
            m['correct'] = (pick_cat == m['outcome'])

    return matches


# ─────────────────────────────────────────────────────────────────────────────
# Markdown
# ─────────────────────────────────────────────────────────────────────────────

def render_pending_md(pending):
    lines = ["## Final + 3º Lugar (previsões — ainda não disputados)", ""]
    for d in pending:
        ta, tb = d['team_a'], d['team_b']
        xg = d['xg']
        top3s = "  ".join(f"{s['score']} {s['pct']:.1f}%" for s in d['top_scores'][:3])
        lines.append(f"### {d['label']}: {dn(ta)} x {dn(tb)}")
        lines.append("")
        lines.append(f"- **xG:** {xg[ta]:.2f} – {xg[tb]:.2f}")
        lines.append(f"- **90':** {dn(ta)} {d['odds'][ta]:.1f}% · Empate {d['odds']['draw']:.1f}% · {dn(tb)} {d['odds'][tb]:.1f}%")
        if d.get('extra_time'):
            et = d['extra_time']
            lines.append(f"- **Prorrogação (dado empate nos 90'):** {dn(ta)} {et[ta]:.1f}% · ainda empatado {et['draw']:.1f}% · {dn(tb)} {et[tb]:.1f}% (pênaltis 50/50 resolvem o resto)")
        else:
            lines.append("- **Sem prorrogação** (regra FIFA do 3º lugar) — empate nos 90' vai direto pra pênaltis 50/50")
        lines.append(f"- **Quem avança:** {dn(ta)} {d['advance'][ta]:.1f}% x {dn(tb)} {d['advance'][tb]:.1f}%")
        lines.append(f"- **Aposta assertiva:** {d['assertive_bet']['label']} — {d['assertive_bet']['pct']:.1f}%")
        lines.append(f"- **Top-3 placares:** {top3s}")
        lines.append("")
    return "\n".join(lines)


def render_md(matches, model_label, n_matches, points_sa, max_points, pending, team_rows):
    by_round = {r: [m for m in matches if m['round'] == r] for r in ROUND_ORDER}

    total_correct = sum(m['correct'] for m in matches)
    group_matches = [m for m in matches if m['round'] in GROUP_ROUNDS]
    ko_matches    = [m for m in matches if m['round'] in KNOCKOUT_ROUNDS]
    group_correct = sum(m['correct'] for m in group_matches)
    ko_correct    = sum(m['correct'] for m in ko_matches)
    top1 = sum(1 for m in ko_matches if m['rank_label'] == 'top-1')
    top3 = sum(1 for m in ko_matches if m['rank_label'] in ('top-1', 'top-2', 'top-3'))

    lines = [
        f"# {model_label} — Reavaliação Retroativa das {n_matches} Partidas",
        "",
        f"Todas as partidas já disputadas da Copa 2026, reavaliadas com os pesos **ativos** do {model_label} "
        f"(objetivo por pontos, treinado nesses mesmos {n_matches} jogos). Avaliação **in-sample** — mede ajuste "
        "do modelo, não generalização. 3º lugar e Final aparecem como previsão (ainda não disputados).",
        "",
        "## Resumo",
        "",
        f"- **Acerto geral:** {total_correct}/{n_matches} ({total_correct/n_matches*100:.1f}%)",
        f"- **Pontos ({model_label}):** {points_sa:.2f}/{max_points:.0f} ({points_sa/max_points*100:.1f}%)",
        f"- **Grupo (W/D/L):** {group_correct}/{len(group_matches)} ({group_correct/len(group_matches)*100:.1f}%)",
        f"- **Mata-mata (quem avança):** {ko_correct}/{len(ko_matches)} ({ko_correct/len(ko_matches)*100:.1f}%)",
        f"- **Placar exato top-1 (mata-mata):** {top1}/{len(ko_matches)}",
        f"- **Placar exato top-3 (mata-mata):** {top3}/{len(ko_matches)}",
        "",
    ]

    for rnd in ROUND_ORDER:
        ms = by_round[rnd]
        if not ms:
            continue
        correct = sum(m['correct'] for m in ms)
        lines.append(f"## {ROUND_LABELS[rnd]} ({correct}/{len(ms)} acertos)")
        lines.append("")
        if rnd in GROUP_ROUNDS:
            lines.append("| Confronto | Placar | Pick | Confiança | xG | Top-3 placares | Resultado |")
            lines.append("|---|---|---|---|---|---|---|")
            for m in ms:
                top3s = "  ".join(f"{i}-{j} {p*100:.1f}%" for (i, j), p in m['top3'])
                lines.append(
                    f"| {dn(m['team_a'])} x {dn(m['team_b'])} | {m['score_display']} | "
                    f"{dn(m['pick_team']) if m['pick_team'] != 'Empate' else 'Empate'} | "
                    f"{m['confidence']*100:.1f}% | {m['xg_a']:.2f}–{m['xg_b']:.2f} | {top3s} | "
                    f"{'✅' if m['correct'] else '❌'} |"
                )
        else:
            lines.append("| Confronto | Placar (90') | Vencedor real | Pick | Confiança | xG | Top-3 placares | Rank placar real | Resultado |")
            lines.append("|---|---|---|---|---|---|---|---|---|")
            for m in ms:
                top3s = "  ".join(f"{i}-{j} {p*100:.1f}%" for (i, j), p in m['top3'])
                bonus_str = f"{m['rank_label']} (+{m['bonus']:.2f}pt)" if m['bonus'] else m['rank_label']
                lines.append(
                    f"| {dn(m['team_a'])} x {dn(m['team_b'])} | {m['score_display']} | {dn(m['winner'])} | "
                    f"{dn(m['pick_team'])} | {m['confidence']*100:.1f}% | {m['xg_a']:.2f}–{m['xg_b']:.2f} | "
                    f"{top3s} | {bonus_str} | {'✅' if m['correct'] else '❌'} |"
                )
        lines.append("")

    if pending:
        lines.append(render_pending_md(pending))

    lines.append(render_teams_md(team_rows, model_label))

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# HTML
# ─────────────────────────────────────────────────────────────────────────────

HTML_HEAD = """<title>{model_label} — Raio-X das {n_matches} Partidas</title>
<style>
:root {{
  --bg: #f4f6f5; --surface: #ffffff; --surface-alt: #eef2f0; --border: #d8dedc;
  --text: #10161b; --text-muted: #5b6b70; --accent: #0f7a4c; --accent-soft: #e4f5ec;
  --good: #128a4a; --bad: #c4433a; --gold: #a8730f; --gold-soft: #f7ecd6;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #0a0f0d; --surface: #121815; --surface-alt: #161d19; --border: #26312b;
    --text: #e7efea; --text-muted: #8fa39a; --accent: #34d399; --accent-soft: rgba(52,211,153,0.12);
    --good: #34d399; --bad: #f87171; --gold: #f2c14e; --gold-soft: rgba(242,193,78,0.14);
  }}
}}
:root[data-theme="dark"] {{
  --bg: #0a0f0d; --surface: #121815; --surface-alt: #161d19; --border: #26312b;
  --text: #e7efea; --text-muted: #8fa39a; --accent: #34d399; --accent-soft: rgba(52,211,153,0.12);
  --good: #34d399; --bad: #f87171; --gold: #f2c14e; --gold-soft: rgba(242,193,78,0.14);
}}
:root[data-theme="light"] {{
  --bg: #f4f6f5; --surface: #ffffff; --surface-alt: #eef2f0; --border: #d8dedc;
  --text: #10161b; --text-muted: #5b6b70; --accent: #0f7a4c; --accent-soft: #e4f5ec;
  --good: #128a4a; --bad: #c4433a; --gold: #a8730f; --gold-soft: #f7ecd6;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--text); font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.4; }}
.mono {{ font-family: ui-monospace, "SF Mono", "Roboto Mono", Consolas, monospace; font-variant-numeric: tabular-nums; }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding: 2.5rem 1.5rem 5rem; }}
header.hero {{ border-top: 4px solid var(--accent); background: var(--surface); padding: 2rem 2rem 1.6rem; margin-bottom: 1.75rem; }}
.eyebrow {{ text-transform: uppercase; letter-spacing: 0.12em; font-size: 0.72rem; color: var(--accent); font-weight: 700; }}
h1 {{ font-family: "Archivo Black", "Arial Black", -apple-system, sans-serif; font-size: clamp(1.6rem, 3.2vw, 2.4rem); margin: 0.35rem 0 0.4rem; letter-spacing: -0.01em; text-wrap: balance; }}
.hero-sub {{ color: var(--text-muted); font-size: 0.98rem; max-width: 62ch; }}
.hero-sub b {{ color: var(--text); }}
.scoreboard {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(155px, 1fr)); gap: 1px; background: var(--border); border: 1px solid var(--border); margin-bottom: 2rem; }}
.stat {{ background: var(--surface); padding: 1.1rem 1.2rem; }}
.stat .label {{ font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 0.35rem; }}
.stat .value {{ font-family: ui-monospace, "SF Mono", "Roboto Mono", monospace; font-variant-numeric: tabular-nums; font-size: 1.6rem; font-weight: 700; }}
.stat .sub {{ font-size: 0.76rem; color: var(--text-muted); margin-top: 0.15rem; }}
.tabs {{ display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 0.9rem; }}
.tab-btn {{ font: inherit; font-size: 0.82rem; font-weight: 600; background: var(--surface); color: var(--text-muted); border: 1px solid var(--border); padding: 0.45rem 0.9rem; cursor: pointer; }}
.tab-btn.active {{ background: var(--accent); color: #06120c; border-color: var(--accent); }}
.tab-btn:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
.panel {{ display: none; margin-bottom: 2rem; }}
.panel.active {{ display: block; }}
.panel-head {{ display: flex; align-items: baseline; justify-content: space-between; gap: 1rem; margin-bottom: 0.75rem; flex-wrap: wrap; }}
.panel-head h2 {{ font-size: 1.15rem; margin: 0; }}
.panel-stat {{ font-size: 0.82rem; color: var(--text-muted); font-weight: 600; }}
.table-wrap {{ overflow-x: auto; border: 1px solid var(--border); }}
table {{ border-collapse: collapse; width: 100%; min-width: 760px; background: var(--surface); }}
thead th {{ text-align: left; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-muted); background: var(--surface-alt); padding: 0.55rem 0.75rem; border-bottom: 1px solid var(--border); white-space: nowrap; position: sticky; top: 0; }}
tbody td {{ padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--border); font-size: 0.85rem; vertical-align: middle; }}
tbody tr:nth-child(even) {{ background: var(--surface-alt); }}
tbody tr.no {{ background: color-mix(in srgb, var(--bad) 6%, var(--surface)); }}
tbody tr.no:nth-child(even) {{ background: color-mix(in srgb, var(--bad) 10%, var(--surface)); }}
.teams {{ font-weight: 600; white-space: nowrap; }}
.vs {{ color: var(--text-muted); font-weight: 400; }}
.score {{ white-space: nowrap; }}
.note {{ color: var(--text-muted); font-size: 0.78rem; }}
.arrow {{ color: var(--text-muted); }}
.xg {{ color: var(--text-muted); white-space: nowrap; }}
.conf-bar {{ display: inline-block; width: 60px; height: 6px; background: var(--border); vertical-align: middle; margin-right: 0.4rem; overflow: hidden; }}
.bar-fill {{ height: 100%; background: var(--text-muted); }}
.bar-fill.bar-good {{ background: var(--good); }}
.bar-fill.bar-bad {{ background: var(--bad); }}
.pct {{ font-size: 0.78rem; color: var(--text-muted); }}
.chips {{ white-space: nowrap; }}
.chip {{ display: inline-block; font-size: 0.72rem; font-family: ui-monospace, "SF Mono", monospace; background: var(--surface-alt); border: 1px solid var(--border); padding: 0.12rem 0.4rem; margin-right: 0.25rem; white-space: nowrap; }}
.chip b {{ font-weight: 700; }}
.pill {{ display: inline-block; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; padding: 0.15rem 0.5rem; }}
.pill.ok {{ background: var(--accent-soft); color: var(--good); }}
.pill.no {{ background: color-mix(in srgb, var(--bad) 16%, transparent); color: var(--bad); }}
.pill.muted {{ background: var(--surface-alt); color: var(--text-muted); }}
.bonus {{ font-size: 0.72rem; color: var(--gold); }}
.outcome-cell {{ text-align: right; }}
.predict-card {{ background: var(--surface); border: 1px solid var(--border); border-top: 3px solid var(--gold); padding: 1.2rem 1.4rem; margin-bottom: 1.25rem; }}
.predict-card h3 {{ margin: 0 0 0.9rem; font-size: 1.05rem; }}
.predict-card .tag {{ display: inline-block; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--gold); background: var(--gold-soft); padding: 0.15rem 0.5rem; margin-bottom: 0.6rem; }}
.predict-row {{ display: flex; align-items: center; gap: 0.6rem; margin: 0.5rem 0; font-size: 0.86rem; }}
.predict-row .rlabel {{ width: 200px; color: var(--text-muted); flex-shrink: 0; }}
.predict-bar {{ flex: 1; display: flex; height: 22px; overflow: hidden; border: 1px solid var(--border); min-width: 160px; }}
.predict-bar .seg {{ display: flex; align-items: center; justify-content: center; font-size: 0.68rem; font-weight: 700; color: #06120c; white-space: nowrap; overflow: hidden; }}
.predict-bar .seg.a {{ background: var(--gold); }}
.predict-bar .seg.d {{ background: var(--text-muted); color: var(--surface); }}
.predict-bar .seg.b {{ background: var(--border); color: var(--text); }}
.predict-foot {{ font-size: 0.8rem; color: var(--text-muted); margin-top: 0.7rem; }}
footer {{ color: var(--text-muted); font-size: 0.78rem; margin-top: 2.5rem; border-top: 1px solid var(--border); padding-top: 1rem; }}
</style>
"""


def render_bar(pct_a, pct_d, pct_b, label_a, label_b, label_d="Empate"):
    def seg(cls, pct, label):
        return f'<div class="seg {cls}" style="width:{pct}%">{label} {pct:.1f}%</div>' if pct >= 6 else f'<div class="seg {cls}" style="width:{pct}%"></div>'
    return (
        f'<div class="predict-bar">{seg("a", pct_a, label_a)}{seg("d", pct_d, label_d)}{seg("b", pct_b, label_b)}</div>'
    )


def render_pending_panel(pending):
    cards = []
    for d in pending:
        ta, tb = d['team_a'], d['team_b']
        na, nb = dn(ta), dn(tb)
        xg = d['xg']
        top3s = "".join(f'<span class="chip">{s["score"]} <b>{s["pct"]:.1f}%</b></span>' for s in d['top_scores'][:3])
        et_html = ""
        if d.get('extra_time'):
            et = d['extra_time']
            et_html = (
                f'<div class="predict-row"><span class="rlabel">Prorrogação (dado empate 90\')</span>'
                f'{render_bar(et[ta], et["draw"], et[tb], na, nb)}</div>'
            )
        else:
            et_html = '<div class="predict-foot">Sem prorrogação — regra FIFA do 3º lugar. Empate nos 90\' vai direto pra pênaltis 50/50.</div>'
        cards.append(
            f'<div class="predict-card">'
            f'<span class="tag">{d["label"]}</span>'
            f'<h3>{na} <span class="vs">x</span> {nb}</h3>'
            f'<div class="predict-row"><span class="rlabel">xG</span><span class="mono">{xg[ta]:.2f} – {xg[tb]:.2f}</span></div>'
            f'<div class="predict-row"><span class="rlabel">90 minutos</span>{render_bar(d["odds"][ta], d["odds"]["draw"], d["odds"][tb], na, nb)}</div>'
            f'{et_html}'
            f'<div class="predict-row"><span class="rlabel">Quem avança</span>{render_bar(d["advance"][ta], 0, d["advance"][tb], na, nb)}</div>'
            f'<div class="predict-row"><span class="rlabel">Top-3 placares</span><span class="chips">{top3s}</span></div>'
            f'<div class="predict-foot">Aposta assertiva: <b>{d["assertive_bet"]["label"]}</b> — {d["assertive_bet"]["pct"]:.1f}%</div>'
            f'</div>'
        )
    return (
        f'<section class="panel" id="panel-final">'
        f'<div class="panel-head"><h2>Final + 3º Lugar</h2><span class="panel-stat">previsão &middot; ainda não disputados</span></div>'
        f'{"".join(cards)}'
        f'</section>'
    )


def render_row_group(m):
    cls = 'ok' if m['correct'] else 'no'
    bar = 'bar-good' if m['correct'] else 'bar-bad'
    pick_name = 'Empate' if m['pick_team'] == 'Empate' else dn(m['pick_team'])
    top3s = "".join(f'<span class="chip">{i}-{j} <b>{p*100:.1f}%</b></span>' for (i, j), p in m['top3'])
    pill = '<span class="pill ok">ACERTOU</span>' if m['correct'] else '<span class="pill no">ERROU</span>'
    return (
        f'<tr class="{cls}">'
        f'<td class="teams">{dn(m["team_a"])} <span class="vs">x</span> {dn(m["team_b"])}</td>'
        f'<td class="mono score">{m["score_display"]}</td>'
        f'<td>{pick_name}</td>'
        f'<td class="mono"><div class="conf-bar"><div class="bar-fill {bar}" style="width:{m["confidence"]*100:.1f}%"></div></div><span class="pct">{m["confidence"]*100:.1f}%</span></td>'
        f'<td class="mono xg">{m["xg_a"]:.2f} – {m["xg_b"]:.2f}</td>'
        f'<td class="chips">{top3s}</td>'
        f'<td class="outcome-cell">{pill}</td>'
        f'</tr>'
    )


def render_row_ko(m):
    cls = 'ok' if m['correct'] else 'no'
    bar = 'bar-good' if m['correct'] else 'bar-bad'
    note_span = f' <span class="note">({m["note"]})</span>' if m['note'] else ''
    top3s = "".join(f'<span class="chip">{i}-{j} <b>{p*100:.1f}%</b></span>' for (i, j), p in m['top3'])
    pill = '<span class="pill ok">ACERTOU</span>' if m['correct'] else '<span class="pill no">ERROU</span>'
    rank_pill_cls = 'ok' if m['rank_label'] == 'top-1' else ('muted' if m['rank_label'] == 'fora do top-3' else 'ok')
    bonus_txt = f' <span class="bonus">+{m["bonus"]:.2f}pt</span>' if m['bonus'] else ''
    return (
        f'<tr class="{cls}">'
        f'<td class="teams">{dn(m["team_a"])} <span class="vs">x</span> {dn(m["team_b"])}</td>'
        f'<td class="mono score">{m["goals_a"]}–{m["goals_b"]}{note_span} <span class="arrow">&rarr;</span> {dn(m["winner"])}</td>'
        f'<td>{dn(m["pick_team"])}</td>'
        f'<td class="mono"><div class="conf-bar"><div class="bar-fill {bar}" style="width:{m["confidence"]*100:.1f}%"></div></div><span class="pct">{m["confidence"]*100:.1f}%</span></td>'
        f'<td class="mono xg">{m["xg_a"]:.2f} – {m["xg_b"]:.2f}</td>'
        f'<td class="chips">{top3s}</td>'
        f'<td class="mono"><span class="pill {rank_pill_cls}">{m["rank_label"]}</span>{bonus_txt}</td>'
        f'<td class="outcome-cell">{pill}</td>'
        f'</tr>'
    )


def render_html(matches, model_label, n_matches, points_sa, max_points, pending, team_rows):
    by_round = {r: [m for m in matches if m['round'] == r] for r in ROUND_ORDER}

    total_correct = sum(m['correct'] for m in matches)
    group_matches = [m for m in matches if m['round'] in GROUP_ROUNDS]
    ko_matches    = [m for m in matches if m['round'] in KNOCKOUT_ROUNDS]
    group_correct = sum(m['correct'] for m in group_matches)
    ko_correct    = sum(m['correct'] for m in ko_matches)
    top1 = sum(1 for m in ko_matches if m['rank_label'] == 'top-1')
    top3 = sum(1 for m in ko_matches if m['rank_label'] in ('top-1', 'top-2', 'top-3'))

    extra_tabs = ""
    if pending:
        extra_tabs += '<button class="tab-btn" data-tab="final">Final + 3º Lugar</button>'
    extra_tabs += '<button class="tab-btn" data-tab="teams">Seleções</button>'
    tabs = "".join(f'<button class="tab-btn" data-tab="{r}">{ROUND_LABELS[r]}</button>' for r in ROUND_ORDER if by_round[r])
    tabs += extra_tabs

    panels = []
    for rnd in ROUND_ORDER:
        ms = by_round[rnd]
        if not ms:
            continue
        correct = sum(m['correct'] for m in ms)
        if rnd in GROUP_ROUNDS:
            head = '<th>Confronto</th><th>Placar real</th><th>Pick do modelo</th><th>Confiança</th><th>xG</th><th>Top-3 placares</th><th>Resultado</th>'
            rows = "".join(render_row_group(m) for m in ms)
        else:
            head = '<th>Confronto</th><th>Placar real</th><th>Pick</th><th>Confiança</th><th>xG</th><th>Top-3 placares</th><th>Rank placar</th><th>Resultado</th>'
            rows = "".join(render_row_ko(m) for m in ms)
        panels.append(
            f'<section class="panel" id="panel-{rnd}">'
            f'<div class="panel-head"><h2>{ROUND_LABELS[rnd]}</h2>'
            f'<span class="panel-stat">{correct}/{len(ms)} acertos &middot; {correct/len(ms)*100:.1f}%</span></div>'
            f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
            f'</section>'
        )

    if pending:
        panels.append(render_pending_panel(pending))
    panels.append(render_teams_panel_html(team_rows, model_label))

    html = HTML_HEAD.format(model_label=model_label, n_matches=n_matches)
    html += f"""
<div class="wrap">
  <header class="hero">
    <div class="eyebrow">{model_label} &middot; Avaliação retroativa &middot; in-sample</div>
    <h1>{n_matches} partidas, um modelo só: como o {model_label} se saiu</h1>
    <p class="hero-sub">Todos os jogos já disputados da Copa 2026 reavaliados com os pesos <b>ativos</b> do {model_label} (objetivo por pontos, bônus de peso pra SF/Final). Como esses mesmos {n_matches} jogos fizeram parte do treino, os números abaixo medem <b>ajuste</b>, não generalização. 3º lugar e Final aparecem como previsão, e todas as 48 seleções ficam com scores e biases na aba "Seleções".</p>
  </header>

  <div class="scoreboard">
    <div class="stat"><div class="label">Acerto geral</div><div class="value">{total_correct}/{n_matches}</div><div class="sub">{total_correct/n_matches*100:.1f}%</div></div>
    <div class="stat"><div class="label">Pontos ({model_label})</div><div class="value">{points_sa:.1f}/{max_points:.0f}</div><div class="sub">{points_sa/max_points*100:.1f}% do máximo</div></div>
    <div class="stat"><div class="label">Grupo &middot; W/D/L</div><div class="value">{group_correct}/{len(group_matches)}</div><div class="sub">{group_correct/len(group_matches)*100:.1f}%</div></div>
    <div class="stat"><div class="label">Mata-mata &middot; quem avança</div><div class="value">{ko_correct}/{len(ko_matches)}</div><div class="sub">{ko_correct/len(ko_matches)*100:.1f}%</div></div>
    <div class="stat"><div class="label">Placar exato top-1</div><div class="value">{top1}/{len(ko_matches)}</div><div class="sub">mata-mata</div></div>
    <div class="stat"><div class="label">Placar exato top-3</div><div class="value">{top3}/{len(ko_matches)}</div><div class="sub">mata-mata</div></div>
  </div>

  <nav class="tabs">{tabs}</nav>

  {''.join(panels)}

  <footer>{model_label} &middot; SA por pontos, biases att+def, {n_matches} jogos de treino, bônus SF/Final &middot; pesos em output/calibrated_weights_sa.json</footer>
</div>

<script>
const buttons = document.querySelectorAll('.tab-btn');
const panels = document.querySelectorAll('.panel');
function activate(key) {{
  buttons.forEach(b => b.classList.toggle('active', b.dataset.tab === key));
  panels.forEach(p => p.classList.toggle('active', p.id === 'panel-' + key));
}}
buttons.forEach(b => b.addEventListener('click', () => activate(b.dataset.tab)));
activate(buttons[0].dataset.tab);
</script>
"""
    return html


def main():
    with open(STATE_FILE, encoding="utf-8") as f:
        state = json.load(f)
    with open(SCORES_FILE, encoding="utf-8") as f:
        scores = json.load(f)
    with open(WEIGHTS_FILE, encoding="utf-8") as f:
        weights = json.load(f)

    model_label = "Model7"
    n_matches   = weights['n_matches']
    points_sa   = weights['points_sa']
    max_points  = weights['max_points']

    matches = build_matches(state, scores)
    matches = evaluate(matches, scores)
    pending = load_pending()
    team_rows = build_team_table(scores, weights)

    md = render_md(matches, model_label, n_matches, points_sa, max_points, pending, team_rows)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Salvo em {OUT_MD}")

    html = render_html(matches, model_label, n_matches, points_sa, max_points, pending, team_rows)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Salvo em {OUT_HTML}")


if __name__ == "__main__":
    main()
