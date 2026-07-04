# Model5 vs Model4 — R32 (16 jogos)

> Model5: SA+biases att+def, 88 jogos (72 grupo + 16 R32), λ=2.0, pesos por rodada revisados (r3=0.5, r32=3.0) + bônus `+0.2` por time vivo. Seed 2026 (escolhida entre 5 seeds com NLL/RankScore empatados). Model4: S14, treinado só com os 72 jogos de grupo (não viu o R32).
>
> **Ressalva:** essa comparação é *in-sample* pro Model5 — ele foi treinado incluindo esses mesmos 16 jogos (com peso extra). A melhora é esperada e não mede generalização. O teste real vem nas oitavas.

## Resumo

| | RankScore | Top-1 exato | Top-3 | W/D/L 90' |
|---|-----------|-------------|-------|-----------|
| Model4 (S14) | 51 | 3/16 (18.75%) | 6/16 (37.5%) | 10/16 (62.5%) |
| **Model5** | **98** | **7/16 (43.75%)** | **12/16 (75%)** | **11/16 (68.75%)** |

## Tabela completa — Model5 (previsão vs real)

| Jogo | xG (Model5) | W/D/L (Model5) | Top-3 (Model5) | Real | Rank | RankScore |
|------|-------------|------------------|------------------|------|:---:|:---:|
| África do Sul x Canadá | 0.42–1.27 | 12.3/29.7/57.9 | 0-1 23.4% · 0-0 18.5% · 0-2 14.8% | 0–1 | 1 | 10 |
| Holanda x Marrocos | 1.24–1.23 | 36.7/27.2/36.1 | 1-1 12.9% · 1-0 10.5% · 0-1 10.4% | 1–1 (PEN) | 1 | 10 |
| Alemanha x Paraguai | 1.64–1.00 | 52.1/24.7/23.2 | 1-1 11.7% · 1-0 11.7% · 2-1 9.6% | 1–1 (PEN) | 1 | 10 |
| França x Suécia | 3.14–0.49 | 88.1/8.7/3.2 | 3-0 13.6% · 2-0 13.0% · 4-0 10.7% | 3–0 | 1 | 10 |
| Bélgica x Senegal | 1.72–1.64 | 40.2/22.8/37.0 | 1-1 9.8% · 2-1 8.4% · 1-2 8.0% | 2–2 (AET) | 4 | 1 |
| EUA x Bósnia | 2.46–0.56 | 79.3/14.3/6.5 | 2-0 14.8% · 3-0 12.2% · 1-0 12.0% | 2–0 | 1 | 10 |
| Espanha x Áustria | 2.74–0.36 | 86.8/10.2/3.0 | 2-0 16.8% · 3-0 15.4% · 1-0 12.3% | 3–0 | 2 | 6 |
| Portugal x Croácia | 2.13–0.80 | 68.0/19.1/12.9 | 2-0 12.1% · 1-0 11.4% · 2-1 9.7% | 2–1 | 3 | 3 |
| Brasil x Japão | 1.87–0.77 | 63.6/21.7/14.7 | 1-0 13.4% · 2-0 12.5% · 1-1 10.2% | 2–1 | 4 | 1 |
| Costa do Marfim x Noruega | 1.14–1.98 | 21.5/21.7/56.8 | 1-1 10.0% · 1-2 9.9% · 0-1 8.8% | 1–2 | 2 | 6 |
| México x Equador | 1.44–0.17 | 70.5/25.2/4.3 | 1-0 28.7% · 2-0 20.6% · 0-0 19.9% | 2–0 | 2 | 6 |
| Inglaterra x Congo | 1.94–0.92 | 61.3/21.5/17.2 | 1-0 11.1% · 2-0 10.8% · 1-1 10.2% | 2–1 | 4 | 1 |
| Suíça x Argélia | 2.03–0.51 | 73.4/18.5/8.2 | 2-0 16.3% · 1-0 16.1% · 3-0 11.0% | 2–0 | 1 | 10 |
| Colômbia x Gana | 1.02–0.30 | 53.4/35.6/11.0 | 1-0 27.1% · 0-0 26.7% · 2-0 13.8% | 1–0 | 1 | 10 |
| Austrália x Egito | 0.89–1.03 | 30.5/31.6/37.9 | 0-1 15.1% · 0-0 14.7% · 1-1 13.4% | 1–1 (PEN) | 3 | 3 |
| Argentina x Cabo Verde | 1.22–0.56 | 52.5/30.4/17.0 | 1-0 20.5% · 0-0 16.8% · 2-0 12.6% | 1–1 (AET) | 4 | 1 |

## Destaques

- **Holanda x Marrocos** e **Alemanha x Paraguai** (os dois PEN de maior confiança errada do Model4) agora batem o **Top-1 exato** no Model5 — rank 1 nos dois.
- **Costa do Marfim x Noruega:** Model4 favorecia Costa do Marfim (zebra); Model5 corrige e favorece Noruega (56.8%), que foi quem realmente venceu.
- **Bélgica x Senegal** e **Argentina x Cabo Verde** continuam como os piores casos pros dois modelos (RankScore 1) — são justamente os empates decididos em AET, o ponto cego estrutural que nem a recalibração resolve (não modelamos prorrogação).

## Seleção das seeds do Model5

| Seed | NLL final | RankScore (88 jogos) |
|------|-----------|------------------------|
| 999 | 135.1205 | 312 |
| **2026 (escolhida)** | 135.1224 | 312 |
| 7 | 135.1225 | — |
| 123 | 135.1238 | — |
| 42 | 135.1289 | — |

NLL quase idêntico entre as 5 (diferença de 0.0084 entre a melhor e a pior) — a otimização (500k iters × 5 restarts) já converge de forma robusta ao mesmo mínimo global, independente da seed. RankScore empatado entre as duas melhores (999 e 2026); adotada a seed 2026.
