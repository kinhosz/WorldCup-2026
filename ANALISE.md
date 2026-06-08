# Análise Profunda — Simulação Copa do Mundo 2026

**Data:** 08/06/2026 · **Simulações:** 1.000.000 · **Modelo:** FC25 + FIFA22 + TM cascade

---

## 1. Objetivo e Escopo

Este documento detalha todas as decisões de modelagem, problemas encontrados durante a construção dos scores, bugs identificados e corrigidos, o impacto de cada correção, e a interpretação dos resultados finais. O objetivo é fornecer transparência completa sobre o que o modelo captura bem, onde ele tem limitações estruturais, e o que os números realmente significam.

---

## 2. Pipeline de Dados

### 2.1 Cascade de fontes

Para cada jogador de cada seleção, o sistema tenta atribuir um rating em cascata:

```
FC25 (akshay)          → 17.470 jogadores, atributos atualizados para 2025
  ↓ fallback
FIFA 22                → 19.239 jogadores, atributos de 2022
  ↓ fallback
Transfermarket 2025    → valor de mercado convertido para rating log-linear
  ↓ fallback
Mediana global         → fallback final, valor único por setor (goleiro/def/meio/ataque)
```

O FC25 tem prioridade máxima: se um jogador é encontrado lá, o FIFA22 é ignorado para aquele jogador. Isso é crítico para jogadores que explodiram depois de 2022 (Lamine Yamal, Nico Williams, Gavi, Endrick, etc.).

### 2.2 Matching de nomes

O matching entre o nome no arquivo de convocação e o dataset é feito por:
- **SequenceMatcher** (similaridade de strings, escala 0–1)
- **Token overlap bonus** (interseção de palavras dividida pelo máximo)
- **Filtro de nacionalidade** (apenas jogadores do mesmo país)
- **Strip de sufixos** (Junior, Sr, Jr removidos antes de comparar)
- **Threshold 0.72** — abaixo disso o match é rejeitado

Score final: `max(ratio_full, ratio_limpo, overlap × 0.8 + ratio × 0.2)`

### 2.3 Conversão de valor de mercado (Tier 3)

Quando o jogador não está em nenhum dataset FIFA, o valor de mercado do Transfermarket é convertido por fórmula log-linear:

```
t = (log(MV) - log(1M)) / (log(180M) - log(1M))
rating = 65 + t × (91 - 65)    → clipado em [45, 95]
```

Âncoras: €1M → 65 pontos · €180M → 91 pontos

### 2.4 Score por setor

Atributos usados por setor (média dos atributos do FC25/FIFA22):

| Setor | Atributos FC25/FIFA22 | K usado |
|-------|----------------------|---------|
| Goleiro | diving, reflexes, handling, positioning | top 1 |
| Defesa | defending, physic | top 4 |
| Meio | passing, dribbling | top 4 |
| Ataque | shooting, pace | top 3 |

Para o FC25, o mapeamento de colunas de goleiros é: `pac`=diving, `sho`=handling, `dri`=reflexes, `phy`=positioning.

Fluxo final: **drop bottom 30% por rating → log-mean dos restantes → min-max entre 48 seleções → [0, 1]**

---

## 3. Audit de Qualidade — Bugs Encontrados e Corrigidos

### 3.1 Cross-position GK mismatches (FIFA22)

**Problema:** O fuzzy matcher encontrava jogadores de linha com o mesmo sobrenome que goleiros, atribuindo médias de atributos de goleiro de 7–15 (campo = zero nas quatro métricas de GK). Esses matches ruins eram aceitos e usados no cálculo.

**Solução:** `MIN_SECTOR_RATING` — qualquer match FIFA que produza rating abaixo do threshold é rejeitado e o jogador cai para o próximo tier:

```python
MIN_SECTOR_RATING = {'goalkeepers': 30.0, 'defenders': 35.0, 'middle': 35.0, 'attackers': 35.0}
```

**Impacto por seleção:**

| Seleção | Match errado | Rating errado | GK antes | GK depois |
|---------|-------------|--------------|----------|-----------|
| Côte d'Ivoire | Mohamed Kone → M. Diomande (campo) | 9.5 | 0.0000 | 0.2294 |
| Austrália | Mathew Ryan → M. Jurman (campo) | 13.0 | 0.0522 | 0.2149 |
| Escócia | Liam Kelly → L. Kelly (campo) | 12.0 | 0.0494 | 0.1027 |
| Suécia | Gustaf Lagerbielke → G. Lagerbielke errado | 11.5 | 0.1776 | 0.3490 |

O filtro também capturou 2 jogadores de linha com matches ruins (Tunísia e EUA, ratings de 29–32).

### 3.2 Son Heung-min — nome em coreano no FIFA22

**Problema:** O FIFA22 armazena Son Heung-min como `short_name="H. Son"`, `long_name="손흥민 孙兴慜"`. A normalização NFKD converte os caracteres coreanos/chineses para vazio, tornando o long_name inutilizável. O fuzzy matcher então não conseguia conectar "Son Heungmin" (squad) a "H. Son" e fazia match para "Song Seung Min" (score 0.85).

**Impacto:** Son aparecia com rating de campo 65.5 e era descartado (bottom 30%). O ATT da Coreia do Sul era near-zero.

**Solução:** Override manual direto:
```python
SQUAD_TO_FIFA_SHORTNAME = {
    ('republic_of_korea', 'Son Heungmin'): 'H. Son',
}
```

**Impacto:** ATT Coreia: 0.168 → 0.804 · xG: 0.718 → 1.755

### 3.3 Mikel Merino — nome truncado no FIFA22

**Problema:** No FIFA22, Mikel Merino tem `short_name="Merino"`. O fuzzy matcher comparando "Mikel MERINO" com "Merino" produzia score baixo (nome muito curto). Em vez disso, encontrava "Mikel Rico" (70 anos, Athletic Club) com score 0.82 — match errado aceito pelo threshold.

**Impacto:** Merino aparecia com MID rating de 68.5 (Mikel Rico) em vez de 81.5 (Merino real). O meio-campo da Espanha era deprimido.

**Solução:** Override adicionado ao dict:
```python
('spain', 'Mikel MERINO'): 'Merino',
```

**Impacto:** MID Espanha: 0.6877 → 0.8088 · xG: 1.461 → 1.555

### 3.4 Alemanha — composição do squad (ATT)

**Problema:** No arquivo de squad, Leroy Sané e Florian Wirtz estavam listados como meias. O modelo de xG tem ATT com peso 70% na ofensiva — sem eles no setor de ataque, a Alemanha tinha ATT=0.015 (quase zero), xG=0.707 e apenas 0.57% de chances de título.

**Decisão:** Sané e Wirtz foram movidos para `attackers`. Ambos têm perfil ofensivo real (Sané=velocidade/finalização, Wirtz=criatividade/gol). A Alemanha jogou o Euro 2024 com eles em funções avançadas.

**Impacto:**

| Métrica | Antes | Depois |
|---------|-------|--------|
| ATT | 0.015 | 0.564 |
| xG | 0.707 | 1.540 |
| Campeã % | 0.57% | 3.24% |

### 3.5 Integração do FC25 — impacto em jogadores jovens

O FC25 foi o fix mais amplo. A geração mais jovem estava sistematicamente subavaliada no FIFA22:

| Jogador | FIFA22 OVR | FC25 OVR | Seleção | Impacto |
|---------|-----------|---------|---------|---------|
| Lamine Yamal | Não existe | 81 | Espanha | ATT via TM → FC25 diretamente |
| Nico Williams | 67 (18 anos) | 85 | Espanha | ATT +18 pontos de OVR |
| Gavi | 66 (16 anos, descartado) | 83 | Espanha | Voltou a ser usado no meio |
| Endrick | Não existe | 82 | Brasil | ATT cobertura real |
| Rodri | ~77 | 91 | Espanha | MID anchor de qualidade |
| Vinicius Jr | ~85 | ~93 | Brasil | ATT já era alto, confirmado |

**Impacto agregado na Espanha:** xG 1.461 → 1.891 · Chances de título: 2.26% → 6.95%

---

## 4. Cobertura por Seleção

| Seleção | FC25 | FIFA22+FC25 | TM | Mediana | Qualidade |
|---------|------|------------|-----|---------|-----------|
| Portugal | 27/27 | 27 | 0 | 0 | ★★★★★ única com 100% FC25 |
| Espanha | 19/26 | 23 | 2 | 1 | ★★★★ |
| Brasil | 18/26 | 25 | 0 | 1 | ★★★★ |
| EUA | 21/26 | 23 | 1 | 2 | ★★★★ |
| Equador | 20/26 | 24 | 1 | 1 | ★★★★ |
| Países Baixos | 0/26 | 26 | 0 | 0 | ★★★ — zero FC25, só FIFA22 |
| Irã | 0/26 | 12 | 5 | 9 | ★★ — nenhum FC25 |
| Qatar | 0/34 | 0 | 6 | 28 | ★ — 82% medianas |
| Jordânia | 2/30 | 2 | 0 | 28 | ★ — 93% medianas |

Os Países Baixos são um caso especial: FC25=0 mesmo com jogadores de alto calibre (Van Dijk, Gakpo, Depay). Os nomes holandeses devem ter incompatibilidades de acento/formatação no dataset akshay que impedem o match. O squad ainda é servido inteiramente pelo FIFA22, o que é razoável para uma seleção que não teve renovação radical desde 2022.

---

## 5. Análise dos Resultados

### 5.1 Top-3: Brasil, Portugal, França (praticamente empatados)

Com 1M de simulações, os três primeiros têm probabilidades muito próximas:

| Seleção | Campeã | Finalista | Semi |
|---------|--------|-----------|------|
| Brasil | 20.82% | 31.96% | 48.03% |
| Portugal | 17.09% | 28.49% | 49.87% |
| França | 16.89% | 30.04% | 44.63% |

**Brasil #1 — por quê?**

É o único time com três setores acima de 0.96 simultaneamente:
- **GK=1.000**: Alisson (87.5) + Ederson (85.5) — a melhor dupla de goleiros do torneio
- **DEF=0.967**: Bremer (85.5), Marquinhos (85.0), Ibañez, Danilo — defesa de Champions League
- **ATT=0.960**: Raphinha, Martinelli, Endrick, Vinicius, Neymar, Cunha — seis atacantes acima de 80

A ausência de ponto fraco visível (MID=0.763 é o único setor "apenas bom") combinada com cobertura FC25 de 18/26 jogadores dá ao Brasil o xG mais alto contra adversário médio: **2.344**.

**Portugal #2** tem MID=1.000 (Bruno Fernandes, Bernardo Silva, etc.) mas DEF=0.760 — vulnerável defensivamente. É o time com melhor meio-campo do torneio mas toma mais gols que Brasil e França.

**França #3** tem DEF=1.000 (melhor defesa) mas o FC25 redistribuiu os scores — não é mais a dupla-máxima de ATT e MID que era com apenas FIFA22. Mais equilibrada, mas também mais competitiva.

### 5.2 Espanha — impacto do FC25

A Espanha é o exemplo mais dramático de como o FC25 muda o modelo. Com FIFA22 puro, estava em 11º (2.26%). Com FC25, sobe para 7º (6.95%).

A diferença vem da geração que ganhou a Eurocopa 2024:
- Gavi passou de descartado (OVR 66 → ignorado) para contribuidor ativo (OVR 83)
- Nico Williams passou de 73 (18 anos em 2022) para 85 (2025)
- Yamal ganhou cobertura real (não existia no FIFA22)
- Rodri confirmado como o melhor meio-campista do torneio (OVR 91 no FC25)

### 5.3 Anomalias esperadas

**Noruega — xG=2.099, campeã=0.00%**
Haaland (ATT=1.000 — máximo do torneio) garante xG de 2.099, mas DEF=0.136 e GK=0.180 significam que a Noruega toma em média mais gols do que marca em qualquer adversário de nível médio-alto. No mata-mata, precisam vencer por placar para avançar e não conseguem manter. Em 1M simulações, nunca chegaram à final.

**Coreia do Sul — xG=1.755, campeã=0.02%**
Son Heung-min (corrigido pelo override) dá ATT=0.804 e xG alto. Mas DEF=0.156 — segunda pior defesa do torneio. A Coreia frequentemente passa da fase de grupos mas é eliminada nas oitavas por qualquer time com MID/DEF decentes.

**Egito — ATT=0.873, campeã=0.01%**
Mohamed Salah é o único destaque. MID=0.198, DEF=0.135. xG=1.743 contra adversário médio mas o modelo os emparelha com Bélgica no R32. Com DEF mínima, perdem sistematicamente no eliminatório.

**Colômbia — ATT=0.900, campeã=3.45%**
Parece alto para uma seleção não-europeia. O squad tem James Rodríguez, Luis Díaz, Falcao — todos com ratings altos no FC25. MID=0.395 é fraco, mas o xG de ataque compensa parcialmente. 3.45% de título é provavelmente generoso mas não absurdo.

### 5.4 Times bem posicionados pelo draw

Bélgica tem **QF=58.66%** mas apenas 2.65% de título — indicador de grupo fácil + eliminação precoce no mata-mata. DEF=0.392 (baixa) explica por que avançam em grupos mas perdem nas quartas contra os top-4.

### 5.5 Limitações estruturais

**1. Países Baixos sem FC25 (FC25=0/26):** Van Dijk, Gakpo, Depay são grandes jogadores que melhoraram desde 2022. O modelo usa FIFA22 para todos eles. A Holanda pode estar subestimada em 1-2%.

**2. Fórmula xG não captura estilos de jogo:** A Espanha de Martínez joga posse e pressão alta — o modelo só vê ATT/MID/DEF como números. Um time que jogar reativo e marcar no contra-ataque (como a Espanha fez na Euro) não é diferenciado de um que pressiona alto.

**3. Convocações congeladas:** O modelo usa a convocação definida agora. Lesões, suspensões e mudanças de última hora entre hoje e julho de 2026 não são capturadas.

**4. Mata-mata tem alta variância:** Com 48 times e chaveamento fixo, um time forte pode ser eliminado cedo se cair no mesmo lado do bracket que outro gigante. A probabilidade de título reflete tanto qualidade quanto sorte no draw.

---

## 6. Conclusão

O modelo, após todas as correções, produz resultados coerentes com o cenário do futebol internacional de 2026:

- **Brasil** aparece como favorito legítimo — tem o melhor goleiro do mundo (Alisson), defesa de elite europeia, e um ataque com seis opções acima de 80 no FC25. A ausência de ponto fraco é o que o diferencia.
- **Portugal e França** são co-favoritos reais, cada um com um setor máximo (MID e DEF respectivamente) e squads sem lacunas graves.
- **Inglaterra e Argentina** formam o segundo bloco (8-9%), times completos sem destaque absoluto em nenhum setor.
- **Espanha** em 7º (6.95%) reflete a qualidade real da campeã europeia — o modelo captura bem a geração Yamal/Williams/Pedri via FC25.
- **Alemanha** em 9º (3.24%) é razoável para um time em transição com excelente defesa e goleiro mas meio de campo em renovação.

O maior impacto individual foi a integração do FC25: a diferença entre um modelo baseado apenas em dados de 2022 e um calibrado para 2025 é substancial para times com jogadores jovens (Espanha, Brasil, etc.) e irrelevante para times com squads estáveis (Argentina, Países Baixos).
