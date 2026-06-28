# Model4 — Report de Performance por Seleção

> Modelo S14: SA+biases att+def λ=2.0 | 72 jogos | NLL=64.55 | RankScore=+241

## Resumo Geral

| Métrica | Valor |
|---------|-------|
| Jogos | 72 |
| Placar exato #1 ★ | 15 (21%) |
| Placar no top-3 | 41 (57%) |
| Resultado (V/E/D) correto | 46 (64%) |
| Penalidades ◄ | 13 (18%) |

## Times que o modelo mais acerta (top-3 por jogo)

| Seleção | Jogos | ★ Top1 | Top3 | Top3% | Penalt | RankScore | xG err/jogo |
|---------|-------|--------|------|-------|--------|-----------|-------------|
| Mexico 🟢 | 3 | 1 | 3 | 100% | 0 | +22 | 0.62 |
| South Africa 🟢 | 3 | 1 | 3 | 100% | 0 | +22 | 0.35 |
| Republic Of Korea | 3 | 1 | 3 | 100% | 0 | +22 | 0.61 |
| Czech Republic | 3 | 1 | 3 | 100% | 0 | +22 | 0.21 |
| Brazil 🟢 | 3 | 1 | 3 | 100% | 0 | +22 | 0.74 |
| Scotland | 3 | 2 | 3 | 100% | 0 | +26 | 0.30 |
| Ivory Coast 🟢 | 3 | 1 | 3 | 100% | 0 | +22 | 0.33 |
| Egypt 🟢 | 3 | 0 | 3 | 100% | 0 | +18 | 0.36 |
| Portugal 🟢 | 3 | 0 | 3 | 100% | 0 | +18 | 0.88 |
| Panama | 3 | 3 | 3 | 100% | 0 | +30 | 0.32 |
| Canada 🟢 | 3 | 0 | 2 | 67% | 1 | +10 | 1.26 |
| Australia 🟢 | 3 | 1 | 2 | 67% | 0 | +16 | 0.96 |
| Morocco 🟢 | 3 | 1 | 2 | 67% | 1 | +11 | 0.65 |
| Haiti | 3 | 2 | 2 | 67% | 1 | +15 | 0.79 |
| Curacao | 3 | 1 | 2 | 67% | 1 | +14 | 0.35 |
| Ecuador 🟢 | 3 | 0 | 2 | 67% | 0 | +12 | 0.97 |
| Japan 🟢 | 3 | 0 | 2 | 67% | 0 | +12 | 0.89 |
| Belgium 🟢 | 3 | 0 | 2 | 67% | 0 | +12 | 1.01 |
| Ira | 3 | 0 | 2 | 67% | 1 | +10 | 0.34 |
| Spain 🟢 | 3 | 1 | 2 | 67% | 0 | +19 | 1.13 |
| Cape Verte 🟢 | 3 | 0 | 2 | 67% | 1 | +10 | 0.95 |
| France 🟢 | 3 | 1 | 2 | 67% | 0 | +16 | 0.73 |
| Argentina 🟢 | 3 | 1 | 2 | 67% | 0 | +16 | 0.19 |
| Algeria 🟢 | 3 | 1 | 2 | 67% | 1 | +14 | 0.72 |
| Congo 🟢 | 3 | 1 | 2 | 67% | 0 | +19 | 0.38 |
| Colombia 🟢 | 3 | 1 | 2 | 67% | 0 | +16 | 0.30 |
| Croatia 🟢 | 3 | 1 | 2 | 67% | 1 | +14 | 0.75 |
| Ghana 🟢 | 3 | 1 | 2 | 67% | 0 | +19 | 0.26 |
| Bosnia And Herzegovina 🟢 | 3 | 0 | 1 | 33% | 1 | +7 | 0.42 |
| Switzerland 🟢 | 3 | 0 | 1 | 33% | 2 | +2 | 1.46 |
| United States Of America 🟢 | 3 | 0 | 1 | 33% | 2 | +2 | 0.86 |
| Paraguay 🟢 | 3 | 1 | 1 | 33% | 1 | +11 | 0.32 |
| Germany 🟢 | 3 | 0 | 1 | 33% | 1 | +4 | 1.13 |
| Sweden 🟢 | 3 | 0 | 1 | 33% | 2 | +2 | 0.74 |
| Tunisia | 3 | 0 | 1 | 33% | 1 | +4 | 0.34 |
| New Zealand | 3 | 0 | 1 | 33% | 1 | +4 | 0.48 |
| Saudi Arabia | 3 | 0 | 1 | 33% | 0 | +12 | 0.40 |
| Uruguay | 3 | 1 | 1 | 33% | 1 | +11 | 0.80 |
| Iraq | 3 | 1 | 1 | 33% | 0 | +13 | 0.32 |
| Norway 🟢 | 3 | 0 | 1 | 33% | 0 | +12 | 0.26 |
| Austria 🟢 | 3 | 1 | 1 | 33% | 1 | +11 | 0.79 |
| Jordan | 3 | 1 | 1 | 33% | 0 | +13 | 0.36 |
| Uzbekistan | 3 | 0 | 1 | 33% | 0 | +9 | 0.37 |
| England 🟢 | 3 | 1 | 1 | 33% | 1 | +11 | 1.15 |
| Qatar | 3 | 0 | 0 | 0% | 2 | -1 | 0.53 |
| Turkey | 3 | 0 | 0 | 0% | 1 | +1 | 1.23 |
| Netherlands 🟢 | 3 | 0 | 0 | 0% | 1 | -2 | 1.28 |
| Senegal 🟢 | 3 | 0 | 0 | 0% | 0 | +3 | 0.92 |

_🟢 = classificado para R32_

## Top-10 melhores previsões (por RankScore acumulado)

| # | Seleção | RankScore | Top1 | Top3% | xG err/jogo |
|---|---------|-----------|------|-------|-------------|
| 1 | Panama | +30 | 3 | 100% | 0.32 |
| 2 | Scotland | +26 | 2 | 100% | 0.30 |
| 3 | Mexico 🟢 | +22 | 1 | 100% | 0.62 |
| 4 | South Africa 🟢 | +22 | 1 | 100% | 0.35 |
| 5 | Republic Of Korea | +22 | 1 | 100% | 0.61 |
| 6 | Czech Republic | +22 | 1 | 100% | 0.21 |
| 7 | Brazil 🟢 | +22 | 1 | 100% | 0.74 |
| 8 | Ivory Coast 🟢 | +22 | 1 | 100% | 0.33 |
| 9 | Spain 🟢 | +19 | 1 | 67% | 1.13 |
| 10 | Congo 🟢 | +19 | 1 | 67% | 0.38 |

## Top-10 piores previsões (por RankScore acumulado)

| # | Seleção | RankScore | Penalt | Top3% | xG err/jogo |
|---|---------|-----------|--------|-------|-------------|
| 1 | Netherlands 🟢 | -2 | 1 | 0% | 1.28 |
| 2 | Qatar | -1 | 2 | 0% | 0.53 |
| 3 | Turkey | +1 | 1 | 0% | 1.23 |
| 4 | Switzerland 🟢 | +2 | 2 | 33% | 1.46 |
| 5 | United States Of America 🟢 | +2 | 2 | 33% | 0.86 |
| 6 | Sweden 🟢 | +2 | 2 | 33% | 0.74 |
| 7 | Senegal 🟢 | +3 | 0 | 0% | 0.92 |
| 8 | Germany 🟢 | +4 | 1 | 33% | 1.13 |
| 9 | Tunisia | +4 | 1 | 33% | 0.34 |
| 10 | New Zealand | +4 | 1 | 33% | 0.48 |

## Classificados para R32 — performance do modelo

| Seleção | Jogos | ★ Top1 | Top3 | Top3% | Penalt | RankScore |
|---------|-------|--------|------|-------|--------|-----------|
| Mexico | 3 | 1 | 3 | 100% | 0 | +22 |
| South Africa | 3 | 1 | 3 | 100% | 0 | +22 |
| Brazil | 3 | 1 | 3 | 100% | 0 | +22 |
| Ivory Coast | 3 | 1 | 3 | 100% | 0 | +22 |
| Egypt | 3 | 0 | 3 | 100% | 0 | +18 |
| Portugal | 3 | 0 | 3 | 100% | 0 | +18 |
| Canada | 3 | 0 | 2 | 67% | 1 | +10 |
| Australia | 3 | 1 | 2 | 67% | 0 | +16 |
| Morocco | 3 | 1 | 2 | 67% | 1 | +11 |
| Ecuador | 3 | 0 | 2 | 67% | 0 | +12 |
| Japan | 3 | 0 | 2 | 67% | 0 | +12 |
| Belgium | 3 | 0 | 2 | 67% | 0 | +12 |
| Spain | 3 | 1 | 2 | 67% | 0 | +19 |
| Cape Verte | 3 | 0 | 2 | 67% | 1 | +10 |
| France | 3 | 1 | 2 | 67% | 0 | +16 |
| Argentina | 3 | 1 | 2 | 67% | 0 | +16 |
| Algeria | 3 | 1 | 2 | 67% | 1 | +14 |
| Congo | 3 | 1 | 2 | 67% | 0 | +19 |
| Colombia | 3 | 1 | 2 | 67% | 0 | +16 |
| Croatia | 3 | 1 | 2 | 67% | 1 | +14 |
| Ghana | 3 | 1 | 2 | 67% | 0 | +19 |
| Bosnia And Herzegovina | 3 | 0 | 1 | 33% | 1 | +7 |
| Switzerland | 3 | 0 | 1 | 33% | 2 | +2 |
| United States Of America | 3 | 0 | 1 | 33% | 2 | +2 |
| Paraguay | 3 | 1 | 1 | 33% | 1 | +11 |
| Germany | 3 | 0 | 1 | 33% | 1 | +4 |
| Sweden | 3 | 0 | 1 | 33% | 2 | +2 |
| Norway | 3 | 0 | 1 | 33% | 0 | +12 |
| Austria | 3 | 1 | 1 | 33% | 1 | +11 |
| England | 3 | 1 | 1 | 33% | 1 | +11 |
| Netherlands | 3 | 0 | 0 | 0% | 1 | -2 |
| Senegal | 3 | 0 | 0 | 0% | 0 | +3 |

## Maiores erros de xG (jogo inteiro, xG previsto vs gols reais)

| Jogo | Placar | xG prev | Gols reais | Erro | Tier |
|------|--------|---------|------------|------|------|
| Germany × Curacao | **7–1** | 4.63+0.55=5.18 | 8 | 2.82 | #13 ◄ |
| England × Croatia | **4–2** | 2.40+0.97=3.37 | 6 | 2.63 | #15 ◄ |
| Morocco × Haiti | **4–2** | 2.99+0.54=3.53 | 6 | 2.47 | #17 ◄ |
| England × Ghana | **0–0** | 1.79+0.56=2.35 | 0 | 2.35 | #4  |
| Algeria × Austria | **3–3** | 1.75+2.07=3.82 | 6 | 2.18 | #15 ◄ |
| Bosnia And Herzegovina × Switzerland | **1–4** | 0.71+2.12=2.83 | 5 | 2.17 | #10 ◄ |
| Uruguay × Cape Verte | **2–2** | 1.07+0.78=1.85 | 4 | 2.15 | #10 ◄ |
| Belgium × Ira | **0–0** | 1.56+0.56=2.12 | 0 | 2.12 | #3  |
| United States Of America × Paraguay | **4–1** | 2.10+0.82=2.91 | 5 | 2.09 | #12 ◄ |
| Qatar × Switzerland | **1–1** | 0.56+3.39=3.95 | 2 | 1.95 | #11 ◄ |

## Placares exatos acertados (★ rank #1)

| Jogo | Placar | Probabilidade | xG |
|------|--------|---------------|----|
| Ghana × Panama | **1–0** | 26.8% | 1.03–0.32 |
| Paraguay × Australia | **0–0** | 26.2% | 0.53–0.80 |
| England × Panama | **2–0** | 22.1% | 2.06–0.20 |
| Mexico × Republic Of Korea | **1–0** | 22.0% | 1.20–0.50 |
| Croatia × Panama | **1–0** | 19.7% | 1.76–0.43 |
| Haiti × Scotland | **0–1** | 19.6% | 0.63–1.09 |
| Curacao × Ivory Coast | **0–2** | 19.6% | 0.30–2.30 |
| Spain × Uruguay | **1–0** | 19.2% | 1.62–0.51 |
| Morocco × Scotland | **1–0** | 18.0% | 1.71–0.54 |
| Congo × Colombia | **0–1** | 17.1% | 0.74–1.24 |
| Brazil × Haiti | **3–0** | 16.3% | 3.48–0.28 |
| France × Iraq | **3–0** | 15.3% | 3.99–0.25 |
| Argentina × Austria | **2–0** | 13.9% | 2.31–0.65 |
| South Africa × Czech Republic | **1–1** | 12.7% | 1.39–1.04 |
| Algeria × Jordan | **2–1** | 9.3% | 2.24–1.36 |

## Penalidades — jogos onde o modelo mais errou (◄)

| Jogo | Placar real | Top-3 previsto | xG | Rank |
|------|-------------|----------------|----|------|
| Morocco × Haiti | **4–2** | 2–0(13%) / 3–0(13%) / 4–0(10%) | 2.99–0.54 | #17 |
| Qatar × Switzerland | **1–1** | 0–3(12%) / 0–2(11%) / 0–4(11%) | 0.56–3.39 | #11 |
| Canada × Qatar | **6–0** | 3–1(8%) / 3–0(8%) / 2–1(7%) | 3.33–1.01 | #15 |
| Bosnia And Herzegovina × Switzerland | **1–4** | 0–2(13%) / 0–1(12%) / 1–2(9%) | 0.71–2.12 | #10 |
| United States Of America × Paraguay | **4–1** | 2–0(12%) / 1–0(11%) / 2–1(10%) | 2.10–0.82 | #12 |
| United States Of America × Turkey | **2–3** | 2–1(9%) / 1–1(8%) / 3–1(7%) | 2.35–1.42 | #12 |
| Germany × Curacao | **7–1** | 4–0(11%) / 5–0(10%) / 3–0(9%) | 4.63–0.55 | #13 |
| Sweden × Tunisia | **5–1** | 3–1(8%) / 3–0(7%) / 2–1(7%) | 3.33–1.09 | #7 |
| Netherlands × Sweden | **5–1** | 3–1(8%) / 2–1(8%) / 4–1(6%) | 3.05–1.34 | #12 |
| Ira × New Zealand | **2–2** | 2–1(10%) / 2–0(10%) / 1–1(8%) | 2.30–1.02 | #7 |
| Uruguay × Cape Verte | **2–2** | 1–0(17%) / 0–0(16%) / 1–1(13%) | 1.07–0.78 | #10 |
| Algeria × Austria | **3–3** | 1–2(8%) / 1–1(8%) / 2–2(7%) | 1.75–2.07 | #15 |
| England × Croatia | **4–2** | 2–0(10%) / 2–1(10%) / 1–0(8%) | 2.40–0.97 | #15 |

## Empates — ponto fraco do modelo Poisson

Empates reais: **20** | modelo previu empate como mais provável: **0** (0%)

| Jogo | Placar | Previsão #1 | xG | Tier |
|------|--------|-------------|----|------|
| South Africa × Czech Republic | **1–1** | 1–1 (13%) | 1.39–1.04 | ★ |
| Canada × Bosnia And Herzegovina | **1–1** | 2–1 (10%) | 2.08–1.28 | #2 |
| Qatar × Switzerland | **1–1** | 0–3 (12%) | 0.56–3.39 | ◄ |
| Paraguay × Australia | **0–0** | 0–0 (26%) | 0.53–0.80 | ★ |
| Brazil × Morocco | **1–1** | 1–0 (14%) | 1.72–0.78 | #3 |
| Ecuador × Curacao | **0–0** | 1–0 (26%) | 1.32–0.31 | #2 |
| Netherlands × Japan | **2–2** | 1–1 (11%) | 1.67–1.27 | #7 |
| Japan × Sweden | **1–1** | 2–1 (10%) | 2.11–1.22 | #2 |
| Belgium × Egypt | **1–1** | 1–0 (15%) | 1.42–0.86 | #2 |
| Ira × New Zealand | **2–2** | 2–1 (10%) | 2.30–1.02 | ◄ |
| Belgium × Ira | **0–0** | 1–0 (19%) | 1.56–0.56 | #3 |
| Egypt × Ira | **1–1** | 1–0 (15%) | 1.39–0.83 | #2 |
| Spain × Cape Verte | **0–0** | 1–0 (24%) | 1.45–0.34 | #3 |
| Saudi Arabia × Uruguay | **1–1** | 0–1 (15%) | 0.63–1.97 | #4 |
| Uruguay × Cape Verte | **2–2** | 1–0 (17%) | 1.07–0.78 | ◄ |
| Cape Verte × Saudi Arabia | **0–0** | 1–0 (20%) | 1.29–0.56 | #2 |
| Algeria × Austria | **3–3** | 1–2 (8%) | 1.75–2.07 | ◄ |
| Portugal × Congo | **1–1** | 1–0 (17%) | 1.70–0.62 | #3 |
| Portugal × Colombia | **0–0** | 1–0 (20%) | 1.01–0.61 | #2 |
| England × Ghana | **0–0** | 1–0 (17%) | 1.79–0.56 | #4 |
