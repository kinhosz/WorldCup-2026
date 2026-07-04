# Template Mestre — Card de Jogo Individual (Oitavas em diante)

Validado com Canadá x Marrocos. Use esse esqueleto pra gerar qualquer jogo — só troque os `{{PLACEHOLDERS}}`. Texto do card sempre em inglês. Formato 4:5, 1080×1350.

## Como preencher

1. Pegue os dados de `output/odds_{time_a}_vs_{time_b}.json`: `xg`, `advance`, `derived_metrics`, `top_scores`.
2. **Pílula de confiança verde** ("★ TIME ADVANCES · X%"): só incluir se `advance` do favorito ≥ 70%. Abaixo disso, remover essa linha inteira do prompt.
3. **Aposta do modelo**: NÃO pegar automaticamente a maior das 8 métricas em `derived_metrics`. Uma métrica só vira badge se passar nos DOIS critérios:
   - **Longe do aleatório**: métricas binárias (over/under 2.5, BTTS sim/não) precisam de diferença ≥10pp em relação a 50%.
   - **Mais provável que não**: precisa estar ≥50% em valor absoluto. Isso já é automático pras binárias (sempre um dos dois lados passa de 50%), mas métricas de um lado só (clean sheet, vitória por margem) muitas vezes ficam abaixo de 50% mesmo sendo "altas pro padrão" daquele tipo de evento (ex: 48% de clean sheet é ótimo comparado à média de ~30%, mas ainda assim é minoria) — **isso confunde quem lê o post**, então só usar essas métricas de um lado só quando também baterem 50%+.
   Se nenhuma métrica passar nos dois critérios, não incluir o badge "Model's pick" nesse slide — o card fica só com xG + quem avança + top scores.
4. **Bandeiras**: descrever o desenho por extenso (cores + padrão), nunca confiar só no emoji — times como Inglaterra, Costa do Marfim, Senegal, Paraguai já causaram erro.
5. **Jogadores ilustrados**: sempre genéricos/sem semelhança com atleta real específico. **Testamos nomear o craque de cada seleção (ex: "styled after Vinicius Jr.") e o Gemini recusa** — política própria contra depictar figuras públicas reais, sem contorno possível. Não tentar de novo.

## Prompt (copiar e adaptar)

```
IMPORTANT: the final image MUST be exactly 4:5 portrait aspect ratio, 1080×1350 pixels — taller than it is wide, like an Instagram post. Do not generate a landscape or square image. Portrait orientation is mandatory.

Professional sports editorial infographic, 4:5 portrait 1080×1350px. Inter or equivalent sans-serif font, tabular numbers. All text in English. Do not invent any values not listed below. Do not render any of these instructional labels as visible text in the image — only render the exact quoted strings.

BACKGROUND: a real cinematic photo of a packed football stadium at night, floodlights blazing, red pyrotechnic flares/smoke in the crowd. On the left third of the image, an illustrated football player styled after {{PLAYER_A}}, wearing a {{TEAM_A}} kit ({{TEAM_A_KIT_COLORS}}), mid-action celebration pose, recognizable facial features and hairstyle inspired by {{PLAYER_A}} but stylized/illustrated, not photorealistic. On the right third, an illustrated football player styled after {{PLAYER_B}}, wearing a {{TEAM_B}} kit ({{TEAM_B_KIT_COLORS}}), mid-action pose facing toward the center, recognizable facial features and hairstyle inspired by {{PLAYER_B}} but stylized/illustrated, not photorealistic. Both figures partially faded into the dark stadium background, like a dramatic rivalry poster. Apply a dark navy overlay at 78% opacity on top of the whole scene (color #080C18) so it reads as moody and atmospheric behind the UI, not distracting.

Small ribbon/tag near the very top, rotated slightly, red background #EF4444 white bold text reading exactly: "KNOCKOUT STAGE"

Text label below the ribbon, small caps, wide letter-spacing, color #93C5FD, reading exactly: "ROUND OF 16 · FIFA WORLD CUP 2026"

Below that label, two generic shield-shaped crests (rounded-bottom heraldic shield outline, dark #1E293B fill, thin light border, strong drop shadow) side by side, each shield filled edge-to-edge with the team's actual flag design (not the real federation crest). A bright radial spotlight glow (white) directly behind the pair of shields, centered on the "VS". Between the two shields, large bold white text reading exactly "VS" with a subtle red glow. Below each shield, the team name in white bold caps.
LEFT SHIELD: {{TEAM_A}} flag ({{TEAM_A_FLAG_DESCRIPTION}}). Name below: {{TEAM_A_NAME_CAPS}}
RIGHT SHIELD: {{TEAM_B}} flag ({{TEAM_B_FLAG_DESCRIPTION}}). Name below: {{TEAM_B_NAME_CAPS}}

Cards below (#1E293B background, border #334155, semi-opaque so the stadium photo behind is still faintly visible through the dark tone) contain the following, stacked vertically:

A line of centered white medium text reading exactly: "xG {{XG_A}} · · · {{XG_B}} xG"

Small caps label above the bar, muted #94A3B8, wide letter-spacing, reading exactly: "WHO ADVANCES"
Probability bar — single rounded pill, TWO segments only (not three), with the percentage written in bold text directly inside each colored segment (not just below):
LEFT segment: solid red #EF4444, no glow, with "{{ADVANCE_A}}%" in bold white text centered inside the segment.
RIGHT segment: bright green #4ADE80 with neon glow, with "{{ADVANCE_B}}%" in bold dark text centered inside the segment.
[o time com MAIOR % fica sempre do lado verde com glow; o outro fica vermelho sem glow — pode inverter esquerda/direita dependendo de quem é o favorito]
Team name labels below the bar (names only, percentages already shown inside the bar): "{{TEAM_A}}      {{TEAM_B}}"

{{SE FAVORITO ≥70%, incluir; senão remover esse bloco inteiro:}}
Green confidence pill (rounded, background #4ADE80, dark text) reading exactly: "★ {{FAVORITE_NAME_CAPS}} ADVANCES · {{FAVORITE_ADVANCE}}%"

{{SE HOUVER MÉTRICA ASSERTIVA VÁLIDA (ver regra no passo 3); senão remover esse bloco inteiro:}}
Model's pick badge (dark pill #1E293B, gold border #FBBF24) reading exactly: "MODEL'S PICK · {{ASSERTIVE_LABEL}} · {{ASSERTIVE_PCT}}%"

Small caps label "TOP SCORES" followed by 3 chips inline (dark #1E293B background, white bold text): "{{SCORE_1}} {{PCT_1}}%   {{SCORE_2}} {{PCT_2}}%   {{SCORE_3}} {{PCT_3}}%"

Insight card (color #93C5FD text, dark card background) reading exactly: "{{INSIGHT_TEXT}}"

Footer, muted #64748B, very small, reading exactly: "Model5 · 1,000,000 simulations"
```

## Checklist antes de mandar pro Gemini

- [ ] Confiança verde só se favorito ≥70%
- [ ] Aposta do modelo só se a métrica for realmente longe do aleatório (ver regra)
- [ ] Bandeiras descritas por extenso, não só emoji
- [ ] Insight menciona os dois times pelo nome completo (não deixar sujeito implícito cortar)
- [ ] Confirmar 4:5 depois de gerado — às vezes sai paisagem
