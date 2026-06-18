#!/usr/bin/env python3
"""
outlier_comparison.py — compara predições com/sem outliers no treino vs resultado real.

Processo completo (rodar após cada rodada com novos dados):

  # 1. calibrar SEM outliers → salva em arquivo específico
  python3 scripts/calibrate.py --exclude-outliers --out output/weights_sem_outlier.json

  # 2. calibrar COM outliers → salva em arquivo específico
  python3 scripts/calibrate.py --out output/weights_com_outlier.json

  # 3. gerar comparação
  python3 scripts/outlier_comparison.py

O script lê automaticamente os dois arquivos acima.
Se quiser passar arquivos diferentes: python3 scripts/outlier_comparison.py <sem> <com>
"""

import json
import math
import sys
import os
import numpy as np
from scipy.stats import poisson as sp_poisson

STATE_FILE      = "output/copa_real_state.json"
SCORES_FILE     = "output/team_scores.json"
OUT_FILE        = "output/outlier_comparison.md"
DEFAULT_SEM     = "output/weights_sem_outlier.json"
DEFAULT_COM     = "output/weights_com_outlier.json"

N_SIMS    = 100_000
MAX_GOALS = 12
FALLBACK  = 0.5
RES_FLOOR = 0.10
MAX_XG    = 8.0

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

def dn(t): return DISPLAY.get(t, t.replace('_',' ').title())


def _get(s, key):
    v = s.get(key)
    return v if v is not None else FALLBACK


def compute_xg(s_a, s_b, w):
    w_mid_off = 1.0 - w['OFF_ATT_W']
    w_mid_res = max(1.0 - w['RES_DEF_W'] - w['RES_GK_W'], 0.05)
    off_a = w['OFF_ATT_W'] * _get(s_a,'attack')  + w_mid_off * _get(s_a,'midfield')
    off_b = w['OFF_ATT_W'] * _get(s_b,'attack')  + w_mid_off * _get(s_b,'midfield')
    res_a = max(w['RES_DEF_W'] * _get(s_a,'defense') + w['RES_GK_W'] * _get(s_a,'goalkeeper') + w_mid_res * _get(s_a,'midfield'), RES_FLOOR)
    res_b = max(w['RES_DEF_W'] * _get(s_b,'defense') + w['RES_GK_W'] * _get(s_b,'goalkeeper') + w_mid_res * _get(s_b,'midfield'), RES_FLOOR)
    return min(w['BASE_XG'] * off_a / res_b, MAX_XG), min(w['BASE_XG'] * off_b / res_a, MAX_XG)


def top1_score(xg_a, xg_b):
    pa = np.array([sp_poisson.pmf(k, xg_a) for k in range(MAX_GOALS+1)])
    pb = np.array([sp_poisson.pmf(k, xg_b) for k in range(MAX_GOALS+1)])
    joint = np.outer(pa, pb)
    idx = np.unravel_index(np.argmax(joint), joint.shape)
    return idx[0], idx[1]


def outcome(ga, gb):
    return 'a' if ga > gb else ('d' if ga == gb else 'b')


def icon(pred_g, pred_a, real_g, real_a):
    if pred_g == real_g and pred_a == real_a: return '✅'
    if outcome(pred_g, pred_a) == outcome(real_g, real_a): return '🟡'
    return '❌'


def main(weights_sem, weights_com):
    with open(STATE_FILE)  as f: state  = json.load(f)
    with open(SCORES_FILE) as f: scores = json.load(f)

    real_results = {}
    for grp, games in state['group_results'].items():
        for key, (ga, gb) in games.items():
            ta, tb = key.split('|')
            real_results[(ta, tb)] = (ga, gb)

    # R1 matchups
    from simulate import GROUPS
    R1 = []
    for grp, teams in sorted(GROUPS.items()):
        for i, j in [(0,1),(2,3)]:
            R1.append((grp, teams[i], teams[j]))

    lines = []
    lines.append("# Comparação: Sem Outliers vs Com Outliers vs Real\n")
    lines.append("Treino **sem outlier** = 18 jogos (exclui Germany 7-1 e Sweden 5-1)")
    lines.append("Treino **com outlier** = 20 jogos (todos)\n")
    lines.append("Legenda: ✅ placar exato · 🟡 resultado certo · ❌ errou\n")
    lines.append("---\n")

    # Pesos
    lines.append("## Pesos calibrados\n")
    lines.append("| Parâmetro | Sem outlier | Com outlier | Δ |")
    lines.append("|-----------|-------------|-------------|---|")
    for k in ['BASE_XG','OFF_ATT_W','OFF_MID_W','RES_DEF_W','RES_GK_W','RES_MID_W']:
        vs = weights_sem.get(k, '—')
        vc = weights_com.get(k, '—')
        delta = round(vs - vc, 4) if isinstance(vs, float) and isinstance(vc, float) else '—'
        lines.append(f"| `{k}` | {vs} | {vc} | {delta:+.4f} |" if isinstance(delta, float) else f"| `{k}` | {vs} | {vc} | — |")
    lines.append("")

    lines.append("---\n")
    lines.append("## Predições por jogo\n")
    lines.append("| Grp | Jogo | Sem outlier | Res | Com outlier | Res | Real |")
    lines.append("|-----|------|-------------|-----|-------------|-----|------|")

    # contadores
    sem_exact = sem_ok = com_exact = com_ok = 0
    n_games = 0

    for grp, ta, tb in R1:
        real = real_results.get((ta, tb))
        if real is None:
            lines.append(f"| {grp} | {dn(ta)} vs {dn(tb)} | — | — | — | — | (pendente) |")
            continue

        n_games += 1
        rg, ra = real

        xg_a_sem, xg_b_sem = compute_xg(scores[ta], scores[tb], weights_sem)
        xg_a_com, xg_b_com = compute_xg(scores[ta], scores[tb], weights_com)

        sg, sa_ = top1_score(xg_a_sem, xg_b_sem)
        cg, ca_ = top1_score(xg_a_com, xg_b_com)

        ic_sem = icon(sg, sa_, rg, ra)
        ic_com = icon(cg, ca_, rg, ra)

        if ic_sem == '✅': sem_exact += 1
        if ic_sem in ('✅','🟡'): sem_ok += 1
        if ic_com == '✅': com_exact += 1
        if ic_com in ('✅','🟡'): com_ok += 1

        # destaca outliers
        is_outlier = abs(rg - ra) >= 4
        real_str = f"**{rg}-{ra}**" + (" ⚡" if is_outlier else "")

        lines.append(
            f"| {grp} | {dn(ta)} vs {dn(tb)} "
            f"| {sg}-{sa_} | {ic_sem} "
            f"| {cg}-{ca_} | {ic_com} "
            f"| {real_str} |"
        )

    lines.append("\n---\n")
    lines.append("## Resumo\n")
    lines.append("| Métrica | Sem outlier | Com outlier |")
    lines.append("|---------|-------------|-------------|")
    lines.append(f"| Placar exato | {sem_exact}/{n_games} = {sem_exact/n_games*100:.1f}% | {com_exact}/{n_games} = {com_exact/n_games*100:.1f}% |")
    lines.append(f"| Resultado certo | {sem_ok}/{n_games} = {sem_ok/n_games*100:.1f}% | {com_ok}/{n_games} = {com_ok/n_games*100:.1f}% |")

    with open(OUT_FILE, 'w') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Salvo em {OUT_FILE}")
    print(f"Sem outlier: {sem_exact}/{n_games} exatos, {sem_ok}/{n_games} resultados")
    print(f"Com outlier: {com_exact}/{n_games} exatos, {com_ok}/{n_games} resultados")


def load_weights(path):
    with open(path) as f:
        d = json.load(f)
    w = d['weights']
    w['n_matches'] = d.get('n_matches', '?')
    return w


if __name__ == '__main__':
    sem_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SEM
    com_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_COM

    for p in [sem_path, com_path]:
        if not os.path.exists(p):
            print(f"Arquivo não encontrado: {p}")
            print()
            print("Para gerar os arquivos necessários, rode:")
            print(f"  python3 scripts/calibrate.py --exclude-outliers --out {DEFAULT_SEM}")
            print(f"  python3 scripts/calibrate.py --out {DEFAULT_COM}")
            sys.exit(1)

    weights_sem = load_weights(sem_path)
    weights_com = load_weights(com_path)

    print(f"Sem outlier: {sem_path}  ({weights_sem.get('n_matches', '?')} jogos)")
    print(f"Com outlier: {com_path}  ({weights_com.get('n_matches', '?')} jogos)")

    main(weights_sem, weights_com)
