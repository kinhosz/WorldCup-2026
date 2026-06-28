# Comparação de Modelos — Copa do Mundo 2026

Avaliação sobre 72 jogos reais

```

  Comparação de Modelos — 72 jogos
  ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
  ID    Modelo                          RankScore  Top1  Top3  Top5  Pnlt   Res%  AvgP%  AvgRank   AvgXG      NLL
  ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
  S19   SA+biases att+def λ=2.0 unc          +243    15    42    50    13  63.9%  55.5%      4.7   1.493    64.55 ★
  S14   SA+biases att+def λ=2.0 72g          +241    15    41    50    13  63.9%  55.5%      4.7   1.493    64.55
  S13   SA+biases att+def λ=1.0 72g          +238    12    43    53    12  63.9%  56.5%      4.3   1.493    58.32
  S20   SA+biases att+def λ=1.0 unc          +238    12    43    53    12  63.9%  56.5%      4.3   1.493    58.32
  S15   SA+biases att+def λ=3.0 72g          +223    17    39    47    15  63.9%  54.6%      5.1   1.493    69.85
  S17   SA+biases λ=2.0 72g −outliers        +214    18    40    49    19  65.3%  53.0%      5.7   1.302    77.41
  S09   SA+att_only λ=0.5 72g                +184    14    35    49    18  61.1%  54.2%      5.5   1.493    78.99
  S16   SA+att_only λ=1.5 72g −outliers       +177    17    33    42    22  58.3%  51.3%      6.5   1.306    91.19
  S10   SA+att_only λ=1.0 72g                +175    13    32    49    19  61.1%  53.8%      5.6   1.493    80.15
  S18   SA+att_only λ=1.0 72g −outliers       +174    17    32    44    22  59.7%  51.4%      6.5   1.302    91.61
  S21   SA+att_only λ=2.0 unc                +172    13    31    46    18  62.5%  53.0%      5.7   1.493    83.15
  S11   SA+att_only λ=1.5 72g                +171    12    32    45    17  62.5%  53.4%      5.7   1.493    81.48
  S12   SA+att_only λ=2.5 72g                +162    12    30    43    17  62.5%  52.6%      5.9   1.493    84.74
  S04   S01 + xG×1.40                        +161    16    35    41    28  63.9%  56.3%      7.6   2.070   105.81
  S03   S01 + xG×1.20                        +147    10    33    42    20  63.9%  55.3%      6.6   1.774    96.37
  S05   S01 + xG×1.60                        +131    16    32    37    32  65.3%  57.0%      9.4   2.359   119.52
  S01   SA+att_only 48g λ=1.5                +116     8    28    41    20  66.7%  54.1%      6.4   1.478    92.99
  S02   L-BFGS-B 48g                         +116     8    28    41    20  66.7%  54.1%      6.4   1.479    92.99
  S08   SA global 72g                         +87    11    23    34    26  58.3%  49.7%      7.4   1.493   102.56
  S06   S01 sem biases                        +68     9    20    29    26  59.7%  51.0%      7.8   1.669   105.99
  S07   Default (sem calibração)              +65     8    21    34    29  58.3%  50.8%      7.9   1.751   105.74
  ───────────────────────────────────────────────────────────────────────────────────────────────────────────────

  Legenda:
    RankScore  = pontos totais (rank do placar real na distribuição Poisson)
    Top1/3/5   = nº de jogos onde o placar real estava no rank 1/top3/top5
    Pnlt       = nº de jogos com penalidade (rank>5 e P<5%)
    Res%       = acerto W/D/L  |  AvgP% = prob média do resultado correto
    AvgRank    = rank médio do placar real  |  AvgXG = xG médio por time
    NLL        = Poisson NLL (menor = melhor fit)
```
