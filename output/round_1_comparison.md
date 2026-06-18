# Rodada 1 — Previsão vs Realidade

**20 jogos disputados** · 4 pendentes (grupos K e L)

Legenda: ✅ placar exato · 🟡 resultado certo (W/D/L) · ❌ errou

---

## Jogos por grupo

| Grupo | Jogo | Publicado | Modelo (top-1) | Real | Resultado |
|-------|------|-----------|----------------|------|-----------|
| A | México vs África do Sul | 1-0 | 1-0 | **2-0** | 🟡 vencedor certo |
| A | Coreia do Sul vs Tchéquia | 1-1 | 1-1 | **2-1** | ❌ previu empate |
| B | Canadá vs Bósnia | 2-2 | 2-2 | **1-1** | 🟡 empate certo |
| B | Qatar vs Suíça | — | 0-2 | **1-1** | ❌ previu Suíça |
| C | Brasil vs Marrocos | — | 2-0 | **1-1** | ❌ previu Brasil |
| C | Haiti vs Escócia | — | 0-1 | **0-1** | ✅ placar exato |
| D | EUA vs Paraguai | 2-0 | 2-0 | **4-1** | 🟡 vencedor certo |
| D | Austrália vs Turquia | — | 0-1 | **2-0** | ❌ previu Turquia |
| E | Alemanha vs Curaçao | 3-0 | 5-0 | **7-1** | 🟡 vencedor certo |
| E | Côte d'Ivoire vs Equador | 1-0 | 1-0 | **1-0** | ✅ placar exato |
| F | Holanda vs Japão | 1-0 | 2-0 | **2-2** | ❌ previu Holanda |
| F | Suécia vs Tunísia | 2-1 | 3-1 | **5-1** | 🟡 vencedor certo |
| G | Bélgica vs Egito | 4-1 | 4-1 | **1-1** | ❌ previu Bélgica |
| G | Irã vs Nova Zelândia | 3-1 | 3-1 | **2-2** | ❌ previu Irã |
| H | Espanha vs Cabo Verde | 3-0 | 3-0 | **0-0** | ❌ previu Espanha |
| H | Arábia Saudita vs Uruguai | 0-6 | 0-6 | **1-1** | ❌ previu Uruguai |
| I | França vs Senegal | — | 2-0 | **3-1** | 🟡 vencedor certo |
| I | Iraque vs Noruega | — | 1-4 | **1-4** | ✅ placar exato |
| J | Argentina vs Argélia | — | 2-0 | **3-0** | 🟡 vencedor certo |
| J | Áustria vs Jordânia | — | 1-0 | **3-1** | 🟡 vencedor certo |

---

## Resumo de acertos — modelo (top-1 score)

| Métrica | 16 jogos (batches 1-4) | 20 jogos (completo) |
|---------|----------------------|---------------------|
| ✅ Placar exato | 2/16 = **12.5%** | 3/20 = **15%** |
| 🟡 Resultado certo (W/D/L) | 7/16 = **43.8%** | 11/20 = **55%** |
| ❌ Errou | 9/16 = 56.2% | 9/20 = 45% |

> Os 4 jogos extras (I e J) foram todos acertos de resultado — todos os favoritos ganharam. Isso inflou o número. Os batches 1-4 são o retrato mais honesto: **43.8%**.

---

## O que o modelo erra sistematicamente

### Empates — o ponto mais fraco

9 dos 20 jogos terminaram em empate. O modelo previu **zero** dos 9.

| Jogo | Previu | Real |
|------|--------|------|
| Qatar vs Suíça | 0-2 Suíça | 1-1 |
| Brasil vs Marrocos | 2-0 Brasil | 1-1 |
| Canadá vs Bósnia | 2-2 | 1-1 *(acertou empate, errou placar)* |
| Holanda vs Japão | 2-0 Holanda | 2-2 |
| Bélgica vs Egito | 4-1 Bélgica | 1-1 |
| Irã vs Nova Zelândia | 3-1 Irã | 2-2 |
| Espanha vs Cabo Verde | 3-0 Espanha | 0-0 |
| Arábia Saudita vs Uruguai | 0-6 Uruguai | 1-1 |
| Coreia do Sul vs Tchéquia | 1-1 | 2-1 *(previu empate, foi vitória)* |

O modelo Poisson com xG extremos comprime a probabilidade de empate. Saudi 0-6 é o caso
mais gritante — o modelo calculava 0.3% de chance de Saudi ganhar ou empatar.

### Upsets — azarões que venceram

| Jogo | Previu | Real | xG do modelo |
|------|--------|------|--------------|
| Austrália vs Turquia | 0-1 Turquia | **2-0 Austrália** | AUS 0.69 · TUR 1.61 |
| Coreia do Sul vs Tchéquia | 1-1 | **2-1 Coreia** | KOR 1.67 · CZE 1.81 |

### Placares que acertou com folga

| Jogo | Previu | Real |
|------|--------|------|
| Haiti vs Escócia | 0-1 | **0-1** ✅ |
| Côte d'Ivoire vs Equador | 1-0 | **1-0** ✅ |
| Iraque vs Noruega | 1-4 | **1-4** ✅ |

---

## Jogos publicados no Instagram (12 jogos)

| Jogo | Publicado | Real | Resultado |
|------|-----------|------|-----------|
| México vs África do Sul | 1-0 | 2-0 | 🟡 vencedor |
| Coreia do Sul vs Tchéquia | 1-1 | 2-1 | ❌ |
| Canadá vs Bósnia | 2-2 | 1-1 | 🟡 empate |
| EUA vs Paraguai | 2-0 | 4-1 | 🟡 vencedor |
| Alemanha vs Curaçao | 3-0 | 7-1 | 🟡 vencedor |
| Côte d'Ivoire vs Equador | 1-0 | 1-0 | ✅ exato |
| Holanda vs Japão | 1-0 | 2-2 | ❌ |
| Suécia vs Tunísia | 2-1 | 5-1 | 🟡 vencedor |
| Espanha vs Cabo Verde | 3-0 | 0-0 | ❌ |
| Bélgica vs Egito | 4-1 | 1-1 | ❌ |
| Arábia Saudita vs Uruguai | 0-6 | 1-1 | ❌ |
| Irã vs Nova Zelândia | 3-1 | 2-2 | ❌ |

**Publicados: 1 exato · 5 resultado certo · 6 errou (50% de erro)**

---

## O que mudou com a calibração (preview)

A calibração ainda **não foi aplicada** — os pesos atuais em `simulate.py` são os originais.
O que o `calibrate.py` encontrou como direção:

| Constante | Atual | Calibrado | Efeito esperado |
|-----------|-------|-----------|-----------------|
| `BASE_XG` | 1.30 | **1.12** | xGs extremos diminuem (Saudi 0-6 → menos absurdo) |
| `w_att` | 0.70 | **0.90** | Ataque pesa mais → favoritos ainda ganham mas com xG menor |

Não há "antes vs depois" real ainda — a calibração oficial acontece amanhã com os 4 resultados dos grupos K e L.

---

*Gerado em 2026-06-17 · 20/24 jogos da rodada 1*
