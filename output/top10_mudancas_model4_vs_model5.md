# Top 10 Campeões — Por que mudou tanto (Model4 pré-R32 → Model5 pós-oitavas)

> Baseado em dados reais: bias por seleção (`output/weights_s14.json` vs `output/weights_model5.json`), resultados reais do R32 (`copa_real_state.json`), e a estrutura corrigida do chaveamento (`output/oitavas_bracket_probabilidades.md`). Nenhum dado inventado.

## Tabela comparativa

| # antes | Time | Antes (Model4) | Agora (Model5) | Δ |
|---|------|:---:|:---:|:---:|
| 1 | Argentina | 22.4% | 6.74% | −15.7pp |
| 2 | Holanda | 15.7% | 0% (eliminada) | −15.7pp |
| 3 | Portugal | 12.3% | 6.62% | −5.7pp |
| 4 | França | 12.0% | 26.70% | +14.7pp |
| 5 | Brasil | 10.0% | 20.19% | +10.2pp |
| 6 | Inglaterra | 9.5% | 6.04% | −3.5pp |
| 7 | Alemanha | 6.3% | 0% (eliminada) | −6.3pp |
| 8 | Colômbia | 1.8% | 4.86% | +3.1pp |
| 9 | Japão | 1.6% | 0% (eliminado) | −1.6pp |
| 10 | EUA | 1.5% | 2.21% | +0.7pp |
| — | Espanha | fora do Top10 | **13.67%** | novo #3 |
| — | Marrocos | fora do Top10 | **6.30%** | novo #6 |
| — | Suíça | fora do Top10 | **2.71%** | novo #9 |

**Top 10 atual (ordem):** França 26.70% · Brasil 20.19% · Espanha 13.67% · Argentina 6.74% · Portugal 6.62% · Marrocos 6.30% · Inglaterra 6.04% · Colômbia 4.86% · Suíça 2.71% · EUA 2.21%

## As 3 forças que explicam a mudança

### 1. Três favoritos foram eliminados de verdade

Holanda (perdeu nos pênaltis pro Marrocos), Alemanha (perdeu nos pênaltis pro Paraguai) e Japão (perdeu 1–2 pro Brasil) somavam **23.6 pontos percentuais** de chance de título. Essa fatia foi redistribuída entre quem sobreviveu — empurra todo mundo pra cima, independente de mérito individual.

### 2. Recalibração de bias — o que o R32 real ensinou o modelo

| Time | Bias ataque (M4→M5) | Bias defesa (M4→M5) | Evento real que explica |
|------|:---:|:---:|--------------------------|
| Argentina | 0.992 → 0.818 | 1.156 → 0.843 | Só empatou 1–1 nos 90' com Cabo Verde (5.7% de chance pré-jogo) |
| Portugal | 0.738 → 0.726 | 1.136 → 0.999 | Sofreu gol da Croácia sendo favorito largo |
| Inglaterra | 0.931 → 0.992 | 0.929 → 0.786 | Sofreu gol do Congo sendo favorito |
| França | 1.052 → 1.055 | 1.022 → 1.260 | Clean sheet 3–0 sobre a Suécia |
| Espanha | 0.745 → 0.922 | 1.228 → 1.392 | Goleada 3–0 sobre a Áustria, acima do esperado |
| Marrocos | 1.115 → 1.022 | 0.947 → 1.141 | Segurou a Holanda 90' e venceu nos pênaltis |
| Colômbia | 0.722 → 0.687 | 1.246 → 1.346 | Clean sheet 1–0 sobre Gana |
| Suíça | 0.892 → 1.000 | 0.774 → 1.019 | Goleada 2–0 sobre a Argélia (defesa que o modelo já via como forte) |
| EUA | 1.350 → 1.371 | 0.732 → 1.104 | Clean sheet 2–0 sobre a Bósnia |
| Brasil | 0.950 → 1.026 | 1.081 → 0.878 | Ataque melhorou, defesa piorou — efeito quase neutro |

**Padrão:** resultado "limpo" (goleada/clean sheet) → bias sobe. Vitória apertada ou sofrendo gol sendo favorito → bias cai. A Argentina teve o pior dos dois mundos: nem venceu de forma limpa, quase perdeu.

### 3. Posição no chaveamento (metade A x metade B)

Chaveamento confirmado em `output/oitavas_bracket_probabilidades.md`: metade A (Canadá, Marrocos, Paraguai, França, Bélgica, EUA, Espanha, Portugal) só encontra a metade B (Brasil, Noruega, México, Inglaterra, Suíça, Colômbia, Egito, Argentina) na final.

- **França** está na metade mais fraca (nenhum outro favorito forte no caminho até a final) — maior beneficiário estrutural.
- **Brasil** está na metade B mas seu grupo direto (México/Inglaterra depois Argentina/Colômbia/Suíça/Egito) não tem nenhum gigante europeu — segundo maior beneficiário.
- **Argentina** está na mesma metade do Brasil — precisa passar pelo próprio Brasil (ou por quem emergir desse lado) pra chegar na final, o que capa seu teto independente do bias.
- **Portugal, Inglaterra e EUA** estão em grupos com concorrentes que melhoraram bastante (Espanha), o que reduz o espaço deles.

## Conclusão

Nenhuma das mudanças veio "do nada": cada subida ou queda tem uma raiz real e rastreável — ou um evento explícito do R32 (clean sheet, zebra, quase-zebra) que moveu o bias, ou uma eliminação real que redistribuiu probabilidade, ou a posição estrutural na chave que ficou clara só depois que os 16 times reais foram conhecidos.
