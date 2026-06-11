# Guia de Posts Instagram — Copa do Mundo 2026

Documento de referência para geração de prompts de imagem e legendas dos posts da Copa.
Leia este arquivo antes de criar qualquer prompt de imagem para o projeto.

---

## Fluxo de produção

Os posts são gerados em dois momentos por rodada:

1. **Antes dos jogos** — post de previsões do modelo
2. **Depois dos jogos** — post de resultado comparando previsão vs real

---

## Estilo visual padrão (ambas as imagens)

Identidade visual consistente em todos os posts:

- **Formato:** Instagram 1:1 square
- **Fundo:** preto com textura sutil de bola de futebol (hexágonos)
- **Borda:** fina, dourada
- **Tipografia:** bold moderna, branca para destaque, cinza claro para secundário
- **Acentos:** dourado para labels e detalhes
- **Sem:** emojis robô, confetes, fotos de jogadores reais, excesso de texto na imagem
- **Sensação:** clean, premium, estilo card esportivo (referência: ESPN / Sofascore dark mode)

> O texto longo vai na **legenda**, não na imagem. A imagem deve ser lida em 2 segundos.

---

## Workflow recomendado

Usar o gerador de imagem (Gemini / Midjourney / DALL-E) **só para o visual base**.
O texto final (placares, nomes, bandeiras) deve ser sobreposto no **Canva** ou no próprio Instagram, pois geradores de imagem erram letras e números com frequência.

Estratégia no prompt: descrever o layout e estilo sem depender de texto gerado pela IA.

---

## Tipo 1 — Post de Previsões (antes dos jogos)

### Estrutura da imagem

```
┌─────────────────────────────────────────┐
│  COPA DO MUNDO 2026 • RODADA X          │  ← label gold, topo
│              PREVISÕES                  │  ← título bold branco
├─────────────────────────────────────────┤
│  [Bandeira]  Nome    X × X    Nome  [Bandeira] │  ← linha por jogo
│  [Bandeira]  Nome    X × X    Nome  [Bandeira] │
│  [Bandeira]  Nome    X × X    Nome  [Bandeira] │
├─────────────────────────────────────────┤
│  Monte Carlo · 1M simulações            │  ← rodapé gold, pequeno
│  Segue pra ver os resultados ↓          │
└─────────────────────────────────────────┘
```

- Bandeiras: verticais, grandes, uma de cada lado da linha
- Nomes completos em português (não abreviações)
- Placar centralizado, bold, branco
- Separadores finos dourados entre as linhas de jogos

### Estrutura da legenda

```
⚽ Previsões do modelo — Copa 2026 • Rodada X

🏳️ Time A  X × X  Time B 🏳️
🏳️ Time C  X × X  Time D 🏳️
...

Modelo Monte Carlo com 1 milhão de simulações.
Comenta o que você acha que vai acontecer 👇

Me segue pra ver os resultados logo depois dos jogos!

#Copa2026 #WorldCup2026 #Previsões #DataScience #Futebol #MonteCarlo
```

---

## Tipo 2 — Post de Resultado (depois dos jogos)

### Estrutura da imagem

```
┌─────────────────────────────────────────┐
│  COPA DO MUNDO 2026 • RODADA X          │  ← label gold, topo
├─────────────────────────────────────────┤
│  [Bandeira]           [Bandeira]        │
│   Nome do Time    Nome do Time          │
├─────────────────────────────────────────┤
│  PREVISÃO          1 × 0               │  ← cinza/muted
│  RESULTADO         2 × 0               │  ← branco bold, destacado
├─────────────────────────────────────────┤
│  Mensagem honesta de uma linha          │  ← itálico branco, centralizado
│  Segue pra acompanhar a calibragem ↓   │  ← gold, pequeno
└─────────────────────────────────────────┘
```

- Um jogo por card (uma imagem por partida)
- Bandeiras grandes, lado a lado, com nome completo abaixo
- Duas linhas de placar: PREVISÃO (apagado) e RESULTADO (destaque)
- Mensagem honesta de uma linha — sem exagero, sem vitimismo

### Mensagens honetas sugeridas (escolher a que se aplicar)

| Situação | Mensagem |
|----------|----------|
| Acertou vencedor, errou placar | "Acertamos o vencedor. Erramos o placar." |
| Acertou tudo | "Previsão exata. O modelo agradece." |
| Errou o vencedor | "Erramos desta vez. A calibragem continua." |
| Empate não previsto | "Não previmos o empate. Dados atualizados." |

### Estrutura da legenda

```
🏳️ Time A  X × X  Time B 🏳️

Nosso modelo previu X×X — [frase honesta de uma linha].
Transparência total: cada jogo calibra o modelo.

Vou atualizando ao longo de toda a Copa.
Me segue pra acompanhar ao vivo 👇

#Copa2026 #WorldCup2026 #DataScience #Futebol #ModeloPreditivo
```

---

## Checklist antes de gerar o prompt

- [ ] Definir: é post de previsão ou de resultado?
- [ ] Listar os jogos com placar real e/ou previsto
- [ ] Usar nomes completos dos países em português
- [ ] Mencionar as bandeiras dos dois times em cada linha
- [ ] Manter o estilo visual padrão descrito acima
- [ ] Lembrar: texto vai no Canva, não na imagem gerada
