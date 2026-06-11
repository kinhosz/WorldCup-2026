# Score Audit — WorldCup 2026

Generated: 2026-06-09

This report shows exactly how each team score was built:
which data tier (FIFA22 / TM / global-median) each player used,
the raw rating, and whether that player is in the top-K that feeds
the sector log-mean.

## 1. Coverage Summary

Sorted by median fallback rate (higher = less reliable data).

| Nation | xG | FIFA | TM | Median | Fallback% |
|--------|----|------|----|--------|-----------|
| Jordan | 0.831 | 2 | 0 | 28 | 93.3% |
| South Africa | 0.693 | 3 | 0 | 23 | 88.5% |
| Qatar | 0.658 | 0 | 6 | 28 | 82.4% |
| Cape Verde | 0.607 | 9 | 0 | 17 | 65.4% |
| Iraq | 0.492 | 9 | 3 | 22 | 64.7% |
| Uzbekistan | 0.663 | 7 | 5 | 18 | 60.0% |
| Egypt | 1.743 | 6 | 5 | 16 | 59.3% |
| Haiti | 0.236 | 8 | 9 | 9 | 34.6% |
| Iran | 0.758 | 12 | 5 | 9 | 34.6% |
| Panama | 0.809 | 15 | 2 | 9 | 34.6% |
| Tunisia | 0.707 | 13 | 4 | 9 | 34.6% |
| Bosnia-Herzegovina | 0.582 | 12 | 8 | 6 | 23.1% |
| Paraguay | 0.392 | 18 | 2 | 6 | 23.1% |
| Algeria | 1.196 | 17 | 4 | 5 | 19.2% |
| Curacao | 0.167 | 12 | 10 | 4 | 15.4% |
| Ghana | 1.272 | 18 | 4 | 4 | 15.4% |
| Czech Republic | 0.935 | 25 | 0 | 4 | 13.8% |
| Japan | 1.120 | 22 | 1 | 3 | 11.5% |
| Mexico | 0.609 | 21 | 2 | 3 | 11.5% |
| Australia | 0.795 | 22 | 2 | 2 | 7.7% |
| Congo | 1.653 | 18 | 6 | 2 | 7.7% |
| Morocco | 1.612 | 16 | 8 | 2 | 7.7% |
| Uruguay | 1.199 | 24 | 0 | 2 | 7.7% |
| Saudi Arabia | 0.634 | 28 | 0 | 2 | 6.7% |
| Canada | 0.867 | 22 | 2 | 1 | 4.0% |
| Austria | 0.849 | 23 | 2 | 1 | 3.8% |
| Brazil | 2.344 | 25 | 0 | 1 | 3.8% |
| Croatia | 1.159 | 25 | 0 | 1 | 3.8% |
| Ecuador | 0.767 | 24 | 1 | 1 | 3.8% |
| Côte d'Ivoire | 1.474 | 22 | 3 | 1 | 3.8% |
| New Zealand | 0.571 | 25 | 0 | 1 | 3.8% |
| Spain | 1.891 | 23 | 2 | 1 | 3.8% |
| Turkey | 0.855 | 25 | 0 | 1 | 3.8% |
| Senegal | 1.554 | 24 | 3 | 1 | 3.6% |
| Argentina | 1.821 | 26 | 0 | 0 | 0.0% |
| Belgium | 1.798 | 25 | 1 | 0 | 0.0% |
| Colombia | 1.945 | 26 | 0 | 0 | 0.0% |
| England | 2.042 | 25 | 1 | 0 | 0.0% |
| France | 2.074 | 25 | 1 | 0 | 0.0% |
| Germany | 1.540 | 25 | 1 | 0 | 0.0% |
| Netherlands | 1.893 | 24 | 2 | 0 | 0.0% |
| Norway | 2.099 | 26 | 0 | 0 | 0.0% |
| Portugal | 2.296 | 27 | 0 | 0 | 0.0% |
| South Korea | 1.755 | 25 | 1 | 0 | 0.0% |
| Scotland | 0.812 | 23 | 3 | 0 | 0.0% |
| Sweden | 1.427 | 24 | 1 | 0 | 0.0% |
| Switzerland | 1.205 | 26 | 0 | 0 | 0.0% |
| USA | 1.171 | 26 | 0 | 0 | 0.0% |

## 2. Global Sector Medians (Tier-4 fallback value)

The value assigned to every player with no FIFA22 or TM data.

| Sector | Median rating |
|--------|---------------|
| Goalkeepers | 71.88 |
| Defenders | 71.94 |
| Midfielders | 70.50 |
| Attackers | 74.00 |

## 3. Per-nation Player Breakdown

**Tier key:** FIFA22 = matched in FIFA 22 dataset · TM = Transfermarket market value · median = global sector median (no data found)

Score formula: `drop bottom 30% by rating → log-mean of the rest → min-max normalize across 48 nations → [0,1]`.
Players marked **✗** were discarded (bottom 30%).

---

### Algeria

**xG vs avg opponent:** 1.1964 &nbsp;|&nbsp; GK=0.3882 &nbsp;|&nbsp; DEF=0.2928 &nbsp;|&nbsp; MID=0.4887 &nbsp;|&nbsp; ATT=0.4479

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=71.88 · normalized=0.3882)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Oussama Benbot | median | — | — | 71.9 | — |
|  | Melvin Mastil | median | — | — | 71.9 | — |
| ✗ | Luca Zidane | TM | — | — | 68.5 | 2,000,000 |

#### Defenders &nbsp;(6/9 used · raw log-mean=73.14 · normalized=0.2928)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Ramy Bensebaïni | FIFA22 | R. Bensebaini | 1.00 | 78.5 | — |
|  | Aissa Mandi | FIFA22 | A. Mandi | 1.00 | 77.5 | — |
|  | Achref Abada | median | — | — | 71.9 | — |
|  | Samir Chergui | median | — | — | 71.9 | — |
|  | Rayan Ait-Nouri | FC25 | Rayan Aït-Nouri | 1.00 | 71.5 | — |
|  | Jaouen Hadjam | FC25 | Jaouen Hadjam | 1.00 | 68.0 | — |
| ✗ | Zineddine Belaid | FC25 | Zineddine Belaïd | 1.00 | 67.5 | — |
| ✗ | Rafik Belghali | FC25 | Rafik Belghali | 1.00 | 59.5 | — |
| ✗ | Mohamed Tougai | FC25 | Mohamed Amoura | 0.79 | 50.5 | — |

#### Midfielders &nbsp;(5/7 used · raw log-mean=75.87 · normalized=0.4887)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Nabil Bentaleb | FC25 | Nabil Bentaleb | 1.00 | 78.0 | — |
|  | Houssem Aouar | FC25 | Houssem Aouar | 1.00 | 77.0 | — |
|  | Fares Chaibi | FC25 | Farès Chaïbi | 1.00 | 77.0 | — |
|  | Hicham Boudaoui | FIFA22 | H. Boudaoui | 1.00 | 75.0 | — |
|  | Ramiz Zerrouki | FC25 | Ramiz Zerrouki | 1.00 | 72.5 | — |
| ✗ | Yacine Titraoui | FC25 | Yacine Titraoui | 1.00 | 66.0 | — |
| ✗ | Ibrahim Maza | TM | — | — | 65.0 | 600,000 |

#### Attackers &nbsp;(5/7 used · raw log-mean=76.19 · normalized=0.4479)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mohamed Amoura | FC25 | Mohamed Amoura | 1.00 | 85.0 | — |
|  | Riyad Mahrez | FIFA22 | R. Mahrez | 1.00 | 80.0 | — |
|  | Amine Gouiri | FC25 | Amine Gouiri | 1.00 | 78.5 | — |
|  | Adil Boulbina | median | — | — | 74.0 | — |
| ✗ | Nadhir Benbouali | TM | — | — | 65.0 | 600,000 |
|  | Fares Ghedjemis | TM | — | — | 65.0 | 600,000 |
| ✗ | Anis Hadj Moussa | FC25 | Anis Hadj-Moussa | 1.00 | 62.5 | — |

---

### Argentina

**xG vs avg opponent:** 1.8208 &nbsp;|&nbsp; GK=0.8208 &nbsp;|&nbsp; DEF=0.8381 &nbsp;|&nbsp; MID=0.7871 &nbsp;|&nbsp; ATT=0.6631

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=82.21 · normalized=0.8208)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Emiliano Martínez | FC25 | Emiliano Martínez | 1.00 | 84.8 | — |
|  | Juan Musso | FC25 | Juan Musso | 1.00 | 79.8 | — |
| ✗ | Geronimo Rulli | FIFA22 | G. Rulli | 1.00 | 79.5 | — |

#### Defenders &nbsp;(6/8 used · raw log-mean=80.14 · normalized=0.8381)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Cristian Romero | FC25 | Cristian Romero | 1.00 | 83.0 | — |
|  | Nicolas Otamendi | FC25 | Nicolás Otamendi | 1.00 | 83.0 | — |
|  | Lisandro Martinez | FIFA22 | L. Martínez | 1.00 | 79.5 | — |
|  | Facundo Medina | FC25 | Facundo Medina | 1.00 | 79.5 | — |
|  | Leonardo Balerdi | FC25 | Leonardo Balerdi | 1.00 | 78.5 | — |
|  | Nicolas Tagliafico | FC25 | Nicolás Tagliafico | 1.00 | 77.5 | — |
| ✗ | Nahuel Molina | FC25 | Nahuel Molina | 1.00 | 74.5 | — |
| ✗ | Gonzalo Montiel | FC25 | Gonzalo Montiel | 1.00 | 73.0 | — |

#### Midfielders &nbsp;(5/7 used · raw log-mean=81.39 · normalized=0.7871)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Rodrigo De Paul | FC25 | Rodrigo De Paul | 1.00 | 82.5 | — |
|  | Giovani Lo Celso | FIFA22 | G. Lo Celso | 1.00 | 82.5 | — |
|  | Enzo Fernandez | FC25 | Enzo Fernández | 1.00 | 81.0 | — |
|  | Leandro Paredes | FC25 | Leandro Paredes | 1.00 | 80.5 | — |
|  | Exequiel Palacios | FC25 | Exequiel Palacios | 1.00 | 80.5 | — |
| ✗ | Alexis Mac Allister | FIFA22 | A. Mac Allister | 1.00 | 75.5 | — |
| ✗ | Valentin Barco | FIFA22 | V. Barco | 1.00 | 59.0 | — |

#### Attackers &nbsp;(6/8 used · raw log-mean=78.94 · normalized=0.6631)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Lautaro Martinez | FC25 | Lautaro Martínez | 1.00 | 85.0 | — |
|  | Lionel Messi | FC25 | Lionel Messi | 1.00 | 82.0 | — |
|  | Nicolas Gonzalez | FC25 | Nicolás González | 1.00 | 80.5 | — |
|  | Julian Alvarez | FIFA22 | J. Álvarez | 1.00 | 79.0 | — |
|  | Thiago Almada | FIFA22 | T. Almada | 0.76 | 78.0 | — |
|  | Giuliano Simeone | FIFA22 | G. Simeone | 1.00 | 70.0 | — |
| ✗ | Jose Manuel Lopez | FIFA22 | J. López | 0.81 | 60.5 | — |
| ✗ | Nicolas Paz | FC25 | Nicolás Paz | 1.00 | 55.0 | — |

---

### Australia

**xG vs avg opponent:** 0.7953 &nbsp;|&nbsp; GK=0.4406 &nbsp;|&nbsp; DEF=0.2452 &nbsp;|&nbsp; MID=0.1505 &nbsp;|&nbsp; ATT=0.3725

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=73.13 · normalized=0.4406)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mathew Ryan | FC25 | Mathew Ryan | 1.00 | 77.5 | — |
|  | Paul Izzo | FC25 | Paul Izzo | 1.00 | 69.0 | — |
| ✗ | Patrick Beach | FC25 | Patrick Beach | 1.00 | 55.5 | — |

#### Defenders &nbsp;(7/10 used · raw log-mean=72.53 · normalized=0.2452)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Milos Degenek | FIFA22 | M. Degenek | 1.00 | 77.0 | — |
|  | Cameron Burgess | FC25 | Cameron Burgess | 1.00 | 76.0 | — |
|  | Alessandro Circati | FC25 | Alessandro Circati | 1.00 | 74.0 | — |
|  | Harry Souttar | FC25 | Harry Souttar | 1.00 | 74.0 | — |
|  | Lucas Herrington | median | — | — | 71.9 | — |
|  | Jason Geria | FC25 | Jason Geria | 1.00 | 71.0 | — |
|  | Aziz Behich | FC25 | Aziz Behich | 1.00 | 64.5 | — |
| ✗ | Kai Trewin | FIFA22 | K. Trewin | 1.00 | 63.5 | — |
| ✗ | Jordan Bos | FIFA22 | J. Bos | 1.00 | 51.0 | — |
| ✗ | Jacob Italiano | FC25 | Jacob Italiano | 1.00 | 45.5 | — |

#### Midfielders &nbsp;(4/6 used · raw log-mean=69.62 · normalized=0.1505)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Paul Okon-Engstler | median | — | — | 70.5 | — |
|  | Ajdin Hrustic | FIFA22 | A. Hrustić | 1.00 | 70.0 | — |
|  | Jackson Irvine | FC25 | Jackson Irvine | 1.00 | 70.0 | — |
|  | Connor Metcalfe | FC25 | Connor Metcalfe | 1.00 | 68.0 | — |
| ✗ | Cameron Devlin | FC25 | Cameron Devlin | 1.00 | 67.5 | — |
| ✗ | Aiden O'Neill | FIFA22 | A. O'Neill | 1.00 | 64.0 | — |

#### Attackers &nbsp;(5/7 used · raw log-mean=75.23 · normalized=0.3725)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Nestory Irankunda | FC25 | Nestory Irankunda | 1.00 | 82.0 | — |
|  | Mathew Leckie | FC25 | Mathew Leckie | 1.00 | 75.0 | — |
|  | Awer Mabil | FC25 | Awer Mabil | 1.00 | 74.5 | — |
|  | Cristian Volpato | TM | — | — | 72.5 | 4,500,000 |
|  | Mohamed Toure | FC25 | Mohamed Touré | 1.00 | 72.5 | — |
| ✗ | Tete Yengi | TM | — | — | 65.0 | 400,000 |
| ✗ | Nishan Velupillay | FIFA22 | N. Velupillay | 1.00 | 60.5 | — |

---

### Austria

**xG vs avg opponent:** 0.8490 &nbsp;|&nbsp; GK=0.4221 &nbsp;|&nbsp; DEF=0.4462 &nbsp;|&nbsp; MID=0.5875 &nbsp;|&nbsp; ATT=0.2147

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=72.68 · normalized=0.4221)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Alexander Schlager | FIFA22 | A. Schlager | 1.00 | 73.5 | — |
|  | Florian Wiegele | median | — | — | 71.9 | — |
| ✗ | Patrick Pentz | FIFA22 | P. Pentz | 1.00 | 71.0 | — |

#### Defenders &nbsp;(6/9 used · raw log-mean=75.11 · normalized=0.4462)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | David Alaba | FC25 | David Alaba | 1.00 | 81.0 | — |
|  | Philipp Lienhart | FIFA22 | P. Lienhart | 1.00 | 75.5 | — |
|  | Stefan Posch | FIFA22 | S. Posch | 1.00 | 75.0 | — |
|  | Marco Friedl | FIFA22 | M. Friedl | 1.00 | 74.5 | — |
|  | Kevin Danso | FIFA22 | K. Danso | 1.00 | 74.0 | — |
|  | Michael Svoboda | FIFA22 | M. Svoboda | 1.00 | 71.0 | — |
| ✗ | David Affengruber | FIFA22 | D. Affengruber | 1.00 | 64.5 | — |
| ✗ | Phillipp Mwene | FIFA22 | P. Mwene | 1.00 | 63.0 | — |
| ✗ | Alexander Prass | FIFA22 | A. Prass | 1.00 | 59.5 | — |

#### Midfielders &nbsp;(8/11 used · raw log-mean=77.70 · normalized=0.5875)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Carney Chukwuemeka | TM | — | — | 81.1 | 25,000,000 |
|  | Marcel Sabitzer | FIFA22 | M. Sabitzer | 1.00 | 80.5 | — |
|  | Paul Wanner | TM | — | — | 78.2 | 14,000,000 |
|  | Florian Grillitsch | FIFA22 | F. Grillitsch | 1.00 | 77.5 | — |
|  | Konrad Laimer | FIFA22 | K. Laimer | 1.00 | 77.5 | — |
|  | Christoph Baumgartner | FIFA22 | C. Baumgartner | 1.00 | 76.5 | — |
|  | Romano Schmid | FC25 | Romano Schmid | 1.00 | 75.5 | — |
|  | Xaver Schlager | FIFA22 | X. Schlager | 1.00 | 75.0 | — |
| ✗ | Alessandro Schopf | FIFA22 | A. Schöpf | 1.00 | 70.0 | — |
| ✗ | Nicolas Seiwald | FIFA22 | N. Seiwald | 1.00 | 67.5 | — |
| ✗ | Patrick Wimmer | FIFA22 | P. Wimmer | 1.00 | 64.0 | — |

#### Attackers &nbsp;(2/3 used · raw log-mean=73.21 · normalized=0.2147)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Marko Arnautovic | FIFA22 | M. Arnautović | 1.00 | 80.0 | — |
|  | Sasa Kalajdzic | FIFA22 | S. Kalajdžić | 1.00 | 67.0 | — |
| ✗ | Michael Gregoritsch | FIFA22 | M. Gregoritsch | 1.00 | 66.5 | — |

---

### Belgium

**xG vs avg opponent:** 1.7979 &nbsp;|&nbsp; GK=0.5409 &nbsp;|&nbsp; DEF=0.3920 &nbsp;|&nbsp; MID=0.8455 &nbsp;|&nbsp; ATT=0.6255

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=75.52 · normalized=0.5409)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Thibaut Courtois | FIFA22 | T. Courtois | 1.00 | 86.8 | — |
|  | Mike Penders | FC25 | Mike Penders | 1.00 | 65.8 | — |
| ✗ | Senne Lammens | FIFA22 | S. Lammens | 1.00 | 63.8 | — |

#### Defenders &nbsp;(6/9 used · raw log-mean=74.41 · normalized=0.3920)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Arthur Theate | FC25 | Arthur Theate | 1.00 | 79.0 | — |
|  | Brandon Mechele | FIFA22 | B. Mechele | 1.00 | 78.0 | — |
|  | Thomas Meunier | FIFA22 | T. Meunier | 1.00 | 76.5 | — |
|  | Timothy Castagne | FIFA22 | T. Castagne | 1.00 | 72.5 | — |
|  | Koni De Winter | FC25 | Koni De Winter | 1.00 | 72.0 | — |
|  | Maxim De Cuyper | FC25 | Maxim De Cuyper | 1.00 | 69.0 | — |
| ✗ | Zeno Debast | FIFA22 | Z. Debast | 1.00 | 62.0 | — |
| ✗ | Nathan Ngoy | FIFA22 | N. Ngoy | 1.00 | 59.0 | — |
| ✗ | Joaquin Seys | FC25 | Joaquin Seys | 1.00 | 54.0 | — |

#### Midfielders &nbsp;(4/6 used · raw log-mean=82.48 · normalized=0.8455)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Kevin De Bruyne | FIFA22 | K. De Bruyne | 1.00 | 90.5 | — |
|  | Youri Tielemans | FIFA22 | Y. Tielemans | 1.00 | 83.0 | — |
|  | Axel Witsel | FIFA22 | A. Witsel | 1.00 | 80.0 | — |
|  | Hans Vanaken | FIFA22 | H. Vanaken | 1.00 | 77.0 | — |
| ✗ | Nicolas Raskin | FC25 | Nicolas Raskin | 1.00 | 74.0 | — |
| ✗ | Amadou Onana | FC25 | Amadou Onana | 1.00 | 71.5 | — |

#### Attackers &nbsp;(6/8 used · raw log-mean=78.46 · normalized=0.6255)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Romelu Lukaku | FC25 | Romelu Lukaku | 1.00 | 80.5 | — |
|  | Dodi Lukebakio | FIFA22 | D. Lukébakio | 1.00 | 79.5 | — |
|  | Diego Moreira | TM | — | — | 79.5 | 18,000,000 |
|  | Jeremy Doku | FIFA22 | J. Doku | 1.00 | 79.0 | — |
|  | Leandro Trossard | FIFA22 | L. Trossard | 1.00 | 79.0 | — |
|  | Alexis Saelemekars | FIFA22 | A. Saelemaekers | 0.92 | 73.5 | — |
| ✗ | Charles De Ketelaere | FIFA22 | C. De Ketelaere | 1.00 | 72.0 | — |
| ✗ | Matias Fernandez-Pardo | FC25 | Matias Fernandez-Pardo | 1.00 | 69.5 | — |

---

### Bosnia-Herzegovina

**xG vs avg opponent:** 0.5816 &nbsp;|&nbsp; GK=0.3882 &nbsp;|&nbsp; DEF=0.1302 &nbsp;|&nbsp; MID=0.0778 &nbsp;|&nbsp; ATT=0.2862

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=71.88 · normalized=0.3882)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Martin Zlomislic | median | — | — | 71.9 | — |
|  | Osman Hadzikic | median | — | — | 71.9 | — |
| ✗ | Nikola Vasilj | FIFA22 | N. Vasilj | 1.00 | 65.5 | — |

#### Defenders &nbsp;(4/6 used · raw log-mean=71.05 · normalized=0.1302)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Sead Kolasinac | FIFA22 | S. Kolašinac | 1.00 | 78.5 | — |
|  | Stjepan Radeljic | median | — | — | 71.9 | — |
|  | Nihad Mujakic | TM | — | — | 68.5 | 2,000,000 |
| ✗ | Nikola Katic | TM | — | — | 65.9 | 1,200,000 |
|  | Tarik Muharemovic | TM | — | — | 65.9 | 1,200,000 |
| ✗ | Amar Dedic | FIFA22 | A. Dedić | 1.00 | 60.5 | — |

#### Midfielders &nbsp;(8/11 used · raw log-mean=68.27 · normalized=0.0778)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Kerim Alajbegovic | TM | — | — | 75.4 | 8,000,000 |
|  | Esmir Bajraktarevic | TM | — | — | 73.1 | 5,000,000 |
|  | Amir Hadziahmetovic | FIFA22 | A. Hadžiahmetović | 1.00 | 69.5 | — |
|  | Armin Gigovic | FC25 | Armin Gigović | 1.00 | 67.0 | — |
|  | Benjamin Tahirovic | FC25 | Benjamin Tahirović | 1.00 | 66.5 | — |
|  | Amar Memic | FIFA22 | A. Dedić | 0.80 | 65.5 | — |
| ✗ | Nidal Celik | TM | — | — | 65.0 | 1,000,000 |
|  | Ivan Basic | TM | — | — | 65.0 | 1,000,000 |
|  | Dzenis Burnic | TM | — | — | 65.0 | 550,000 |
| ✗ | Dennis Hadzikadunic | FC25 | Dennis Hadžikadunić | 1.00 | 51.5 | — |
| ✗ | Ivan Sunjic | FIFA22 | T. Šunjić | 0.74 | 43.0 | — |

#### Attackers &nbsp;(4/6 used · raw log-mean=74.12 · normalized=0.2862)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Edin Dzeko | FIFA22 | E. Džeko | 1.00 | 74.5 | — |
|  | Ermin Mahmic | median | — | — | 74.0 | — |
|  | Jovo Lukic | median | — | — | 74.0 | — |
|  | Samed Bazdar | median | — | — | 74.0 | — |
| ✗ | Ermedin Demirovic | FIFA22 | E. Demirović | 1.00 | 71.0 | — |
| ✗ | Haris Tabakovic | FC25 | Haris Tabaković | 1.00 | 68.0 | — |

---

### Brazil

**xG vs avg opponent:** 2.3435 &nbsp;|&nbsp; GK=1.0000 &nbsp;|&nbsp; DEF=0.9670 &nbsp;|&nbsp; MID=0.7635 &nbsp;|&nbsp; ATT=0.9604

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=86.49 · normalized=1.0000)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Alisson | FC25 | Alisson | 1.00 | 87.5 | — |
|  | Ederson | FC25 | Ederson | 1.00 | 85.5 | — |
| ✗ | Weverton | median | — | — | 71.9 | — |

#### Defenders &nbsp;(6/9 used · raw log-mean=81.79 · normalized=0.9670)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Bremer | FC25 | Bremer | 1.00 | 85.5 | — |
|  | Marquinhos | FC25 | Marquinhos | 1.00 | 85.0 | — |
|  | Ibañez | FC25 | Ibañez | 1.00 | 81.5 | — |
|  | Danilo | FC25 | Danilo | 1.00 | 80.5 | — |
|  | Gabriel Magalhães | FIFA22 | Gabriel | 0.76 | 80.0 | — |
|  | Alex Sandro | FIFA22 | Alex Sandro | 1.00 | 78.5 | — |
| ✗ | Douglas Santos | FC25 | Douglas Augusto | 0.76 | 76.5 | — |
| ✗ | Wesley | FIFA22 | Wesley | 1.00 | 60.0 | — |
| ✗ | Léo Pereira | FIFA22 | Leandro Pereira | 0.85 | 58.5 | — |

#### Midfielders &nbsp;(3/5 used · raw log-mean=80.96 · normalized=0.7635)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Bruno Guimarães | FC25 | Bruno Guimarães | 1.00 | 83.5 | — |
|  | Lucas Paquetá | FC25 | Lucas Paquetá | 1.00 | 82.0 | — |
|  | Fabinho | FC25 | Fabinho | 1.00 | 77.5 | — |
| ✗ | Casemiro | FC25 | Casemiro | 1.00 | 73.0 | — |
| ✗ | Danilo Santos | FIFA22 | Adílio Santos | 0.85 | 63.5 | — |

#### Attackers &nbsp;(6/9 used · raw log-mean=82.74 · normalized=0.9604)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Raphinha | FC25 | Raphinha | 1.00 | 85.0 | — |
|  | Gabriel Martinelli | FC25 | Gabriel Martinelli | 1.00 | 83.5 | — |
|  | Endrick | FC25 | Endrick | 1.00 | 82.5 | — |
|  | Vinicius Junior | FIFA22 | Vinícius Jr. | 1.00 | 82.5 | — |
|  | Neymar Junior | FC25 | Neymar Jr | 1.00 | 82.0 | — |
|  | Matheus Cunha | FC25 | Matheus Cunha | 1.00 | 81.0 | — |
| ✗ | Luiz Henrique | FC25 | Luis Henrique | 0.92 | 74.5 | — |
| ✗ | Igor Thiago | FC25 | Igor Thiago | 1.00 | 74.0 | — |
| ✗ | Rayan | FIFA22 | Yan | 0.75 | 66.0 | — |

---

### Canada

**xG vs avg opponent:** 0.8673 &nbsp;|&nbsp; GK=0.3086 &nbsp;|&nbsp; DEF=0.0000 &nbsp;|&nbsp; MID=0.0883 &nbsp;|&nbsp; ATT=0.4387

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=69.97 · normalized=0.3086)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Maxime Crepeau | FIFA22 | M. Crépeau | 1.00 | 72.0 | — |
|  | Dayne St. Clair | FIFA22 | D. St. Clair | 1.00 | 68.0 | — |
| ✗ | Owen Goodman | TM | — | — | 65.0 | 150,000 |

#### Defenders &nbsp;(6/9 used · raw log-mean=69.38 · normalized=0.0000)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Alphonso Davies | FC25 | Alphonso Davies | 1.00 | 74.0 | — |
|  | Derek Cornelius | FIFA22 | D. Cornelius | 1.00 | 71.0 | — |
|  | Alfie Jones | TM | — | — | 69.6 | 2,500,000 |
|  | Richie Laryea | FC25 | Richie Laryea | 1.00 | 68.5 | — |
|  | Moise Bombito | FC25 | Moïse Bombito | 1.00 | 68.0 | — |
|  | Alistair Johnston | FIFA22 | A. Johnston | 1.00 | 65.5 | — |
| ✗ | Joel Waterman | FIFA22 | J. Waterman | 1.00 | 65.0 | — |
| ✗ | Niko Sigur | FC25 | Niko Sigur | 1.00 | 64.5 | — |
| ✗ | Luc de Fougerolles | FC25 | Luc De Fougerolles | 1.00 | 59.0 | — |

#### Midfielders &nbsp;(6/9 used · raw log-mean=68.47 · normalized=0.0883)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Stephen Eustaquio | FC25 | Stephen Eustáquio | 1.00 | 74.0 | — |
|  | Jonathan Osorio | FIFA22 | J. Osorio | 1.00 | 72.0 | — |
|  | Ismael Kone | FC25 | Ismaël Koné | 1.00 | 69.5 | — |
|  | Liam Millar | FC25 | Liam Millar | 1.00 | 69.0 | — |
|  | Tajon Buchanan | FIFA22 | T. Buchanan | 1.00 | 64.0 | — |
|  | Ali Ahmed | FC25 | Ali Ahmed | 1.00 | 63.0 | — |
| ✗ | Mathieu Choiniere | FIFA22 | M. Choinière | 1.00 | 62.5 | — |
| ✗ | Jacob Shaffelburg | FIFA22 | J. Shaffelburg | 1.00 | 58.0 | — |
| ✗ | Nathan-Dylan Saliba | FIFA22 | N. Saliba | 1.00 | 47.5 | — |

#### Attackers &nbsp;(3/4 used · raw log-mean=76.07 · normalized=0.4387)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Jonathan David | FC25 | Jonathan David | 1.00 | 81.5 | — |
|  | Tani Oluwaseyi | median | — | — | 74.0 | — |
|  | Cyle Larin | FC25 | Cyle Larin | 1.00 | 73.0 | — |
| ✗ | Promise David | FC25 | Promise David | 1.00 | 62.0 | — |

---

### Cape Verde

**xG vs avg opponent:** 0.6066 &nbsp;|&nbsp; GK=0.3882 &nbsp;|&nbsp; DEF=0.2384 &nbsp;|&nbsp; MID=0.2704 &nbsp;|&nbsp; ATT=0.2174

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=71.88 · normalized=0.3882)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | VOZINHA | median | — | — | 71.9 | — |
|  | MARCIO ROSA | median | — | — | 71.9 | — |
|  | CJ DOS SANTOS | median | — | — | 71.9 | — |

#### Defenders &nbsp;(6/8 used · raw log-mean=72.44 · normalized=0.2384)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | LOGAN COSTA | FC25 | Logan Costa | 1.00 | 75.0 | — |
|  | STOPIRA | median | — | — | 71.9 | — |
|  | DINEY BORGES | median | — | — | 71.9 | — |
|  | PICO LOPES | median | — | — | 71.9 | — |
|  | SIDNY LOPES CABRAL | median | — | — | 71.9 | — |
|  | KELVIN PIRES | median | — | — | 71.9 | — |
| ✗ | STEVEN MOREIRA | FC25 | Steven Moreira | 1.00 | 71.0 | — |
| ✗ | WAGNER PINA | FC25 | Wagner Pina | 1.00 | 57.5 | — |

#### Midfielders &nbsp;(8/12 used · raw log-mean=71.84 · normalized=0.2704)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | JOVANE CABRAL | FIFA22 | Jovane Cabral | 1.00 | 76.5 | — |
|  | JAMIRO MONTEIRO | FIFA22 | Jamiro Monteiro | 1.00 | 75.5 | — |
| ✗ | KEVIN PINA | median | — | — | 70.5 | — |
| ✗ | JOAO PAULO | median | — | — | 70.5 | — |
|  | GARRY RODRIGUES | median | — | — | 70.5 | — |
|  | DEROY DUARTE | median | — | — | 70.5 | — |
|  | LAROS DUARTE | median | — | — | 70.5 | — |
|  | YANNICK SEMEDO | median | — | — | 70.5 | — |
|  | WILLY SEMEDO | median | — | — | 70.5 | — |
|  | HELIO VARELA | median | — | — | 70.5 | — |
| ✗ | NUNO DA COSTA | FC25 | Nuno da Costa | 1.00 | 67.5 | — |
| ✗ | TELMO ARCANJO | FC25 | Telmo Arcanjo | 1.00 | 62.0 | — |

#### Attackers &nbsp;(2/3 used · raw log-mean=73.25 · normalized=0.2174)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | RYAN MENDES | median | — | — | 74.0 | — |
|  | GILSON BENCHIMOL | FIFA22 | Gilson Tavares | 0.80 | 72.5 | — |
| ✗ | DAILON LIVRAMENTO | FC25 | Dailon Rocha Livramento | 0.85 | 72.0 | — |

---

### Colombia

**xG vs avg opponent:** 1.9453 &nbsp;|&nbsp; GK=0.5973 &nbsp;|&nbsp; DEF=0.5972 &nbsp;|&nbsp; MID=0.3949 &nbsp;|&nbsp; ATT=0.8996

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=76.87 · normalized=0.5973)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | David Ospina | FC25 | David Ospina | 1.00 | 77.8 | — |
|  | Alvaro Montero | FC25 | Álvaro Montero | 1.00 | 76.0 | — |
| ✗ | Camilo Vargas | FIFA22 | C. Vargas | 0.76 | 75.2 | — |

#### Defenders &nbsp;(6/8 used · raw log-mean=77.05 · normalized=0.5972)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Davinson Sanchez | FC25 | Davinson Sánchez | 1.00 | 80.5 | — |
|  | Daniel Munoz | FC25 | Daniel Muñoz | 1.00 | 78.5 | — |
|  | Jhon Lucumi | FC25 | Jhon Lucumí | 1.00 | 78.0 | — |
|  | Yerry Mina | FC25 | Yerry Mina | 1.00 | 77.0 | — |
|  | Santiago Arias | FIFA22 | S. Arias | 0.78 | 75.5 | — |
|  | Deiver Machado | FC25 | Deiver Machado | 1.00 | 73.0 | — |
| ✗ | Johan Mojica | FC25 | Johan Mojica | 1.00 | 71.0 | — |
| ✗ | Willer Ditta | FIFA22 | W. Ditta | 0.74 | 70.0 | — |

#### Midfielders &nbsp;(7/10 used · raw log-mean=74.14 · normalized=0.3949)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | James Rodriguez | FIFA22 | J. Rodríguez | 0.85 | 86.0 | — |
|  | Juan Fernando Quintero | FC25 | Juan Fernando Quintero | 1.00 | 80.0 | — |
|  | Jorge Carrascal | FIFA22 | J. Carrascal | 0.85 | 75.5 | — |
|  | Jaminton Campaz | FC25 | Jaminton Campaz | 1.00 | 74.5 | — |
|  | Jefferson Lerma | FC25 | Jefferson Lerma | 1.00 | 72.5 | — |
|  | Juan Portilla | FC25 | Juan Camilo Portilla | 0.79 | 67.0 | — |
|  | Richard Rios | FIFA22 | R. Rios | 1.00 | 65.5 | — |
| ✗ | Gustavo Puerta | FC25 | Gustavo Puerta | 1.00 | 64.0 | — |
| ✗ | Kevin Castano | FIFA22 | M. Castaño | 0.73 | 59.5 | — |
| ✗ | Jhon Arias | FIFA22 | J. Arias | 0.82 | 58.5 | — |

#### Attackers &nbsp;(3/5 used · raw log-mean=81.96 · normalized=0.8996)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Luis Diaz | FC25 | Luis Díaz | 1.00 | 85.0 | — |
|  | Luis Suarez | FIFA22 | L. Suárez | 0.84 | 82.0 | — |
|  | Juan Camilo Hernandez | FIFA22 | J. Hernández | 0.86 | 79.0 | — |
| ✗ | Carlos Gomez | FC25 | Andrés Gómez | 0.75 | 72.0 | — |
| ✗ | Jhon Cordoba | FIFA22 | B. Córdoba | 0.76 | 43.0 | — |

---

### Congo

**xG vs avg opponent:** 1.6528 &nbsp;|&nbsp; GK=0.1895 &nbsp;|&nbsp; DEF=0.4699 &nbsp;|&nbsp; MID=0.1760 &nbsp;|&nbsp; ATT=0.8327

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=67.12 · normalized=0.1895)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Lionel Mpasi | FC25 | Lionel Mpasi | 1.00 | 67.2 | — |
|  | Thimothy Fayulu | FC25 | Timothy Fayulu | 0.97 | 67.0 | — |
| ✗ | Matthieu Epolo | TM | — | — | 65.0 | 800,000 |

#### Defenders &nbsp;(6/9 used · raw log-mean=75.41 · normalized=0.4699)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Chancel Mbemba | FC25 | Chancel Mbemba | 1.00 | 80.5 | — |
|  | Aaron Wan-Bissaka | TM | — | — | 80.5 | 22,000,000 |
|  | Dylan Batubinsika | FC25 | Dylan Batubinsika | 1.00 | 73.5 | — |
|  | Gédéon Kalulu | FC25 | Gédéon Kalulu | 1.00 | 73.5 | — |
|  | Alex Tuanzebe | TM | — | — | 73.1 | 5,000,000 |
|  | Steve Kapuadi | median | — | — | 71.9 | — |
| ✗ | Arthur Masuaku | FIFA22 | A. Masuaku | 1.00 | 70.0 | — |
| ✗ | Joris Kayembe | FC25 | Joris Kayembe | 1.00 | 69.5 | — |
| ✗ | Aaron Tshibola | TM | — | — | 65.0 | 450,000 |

#### Midfielders &nbsp;(6/9 used · raw log-mean=70.09 · normalized=0.1760)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Gael Kakuta | FIFA22 | G. Kakuta | 1.00 | 79.5 | — |
|  | Meschack Elia | FC25 | Meschack Elia | 1.00 | 72.5 | — |
|  | Samuel Moutoussamy | FIFA22 | S. Moutoussamy | 1.00 | 69.5 | — |
|  | Nathanael Mbuku | TM | — | — | 68.5 | 2,000,000 |
|  | Charles Pickel | FC25 | Charles Pickel | 1.00 | 66.5 | — |
|  | Edo Kayembe | FIFA22 | E. Kayembe | 1.00 | 65.0 | — |
| ✗ | Brian Cipenga | FC25 | Brian Cipenga | 1.00 | 64.0 | — |
| ✗ | Noah Sadiki | FC25 | Noah Sadiki | 1.00 | 63.5 | — |
| ✗ | Ngal'ayel Mukau | FC25 | Ngal'ayel Mukau | 1.00 | 61.0 | — |

#### Attackers &nbsp;(3/5 used · raw log-mean=81.11 · normalized=0.8327)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Cedric Bakambu | FIFA22 | C. Bakambu | 1.00 | 85.0 | — |
|  | Yoane Wissa | FIFA22 | Y. Wissa | 1.00 | 81.0 | — |
|  | Simon Banza | FC25 | Simon Banza | 1.00 | 77.5 | — |
| ✗ | Fiston Mayele | median | — | — | 74.0 | — |
| ✗ | Theo Bongonda | TM | — | — | 73.1 | 5,000,000 |

---

### Croatia

**xG vs avg opponent:** 1.1594 &nbsp;|&nbsp; GK=0.6530 &nbsp;|&nbsp; DEF=0.4383 &nbsp;|&nbsp; MID=0.5851 &nbsp;|&nbsp; ATT=0.3863

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=78.20 · normalized=0.6530)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Dominik Livakovic | FIFA22 | D. Livaković | 1.00 | 81.0 | — |
|  | Dominik Kotarski | FC25 | Dominik Kotarski | 1.00 | 75.5 | — |
| ✗ | Ivor Pandur | FIFA22 | I. Pandur | 1.00 | 71.5 | — |

#### Defenders &nbsp;(5/7 used · raw log-mean=75.01 · normalized=0.4383)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Duje Caleta-Car | FIFA22 | D. Ćaleta-Car | 1.00 | 80.5 | — |
|  | Josko Gvardiol | FIFA22 | J. Gvardiol | 1.00 | 77.0 | — |
|  | Marin Pongracic | FIFA22 | M. Pongračić | 1.00 | 76.0 | — |
|  | Martin Erlic | FIFA22 | M. Erlić | 1.00 | 72.0 | — |
|  | Josip Sutalo | FIFA22 | J. Šutalo | 1.00 | 70.0 | — |
| ✗ | Luka Vuskovic | FC25 | Luka Vušković | 1.00 | 67.0 | — |
| ✗ | Josip Stanisic | FIFA22 | J. Stanišić | 1.00 | 62.0 | — |

#### Midfielders &nbsp;(7/10 used · raw log-mean=77.66 · normalized=0.5851)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Luka Modric | FIFA22 | L. Modrić | 1.00 | 88.5 | — |
|  | Mateo Kovacic | FIFA22 | M. Kovačić | 1.00 | 85.5 | — |
|  | Nikola Vlasic | FIFA22 | N. Vlašić | 1.00 | 80.0 | — |
|  | Mario Pasalic | FIFA22 | M. Pašalić | 1.00 | 76.0 | — |
|  | Nikola Moro | FC25 | Nikola Moro | 1.00 | 74.5 | — |
|  | Petar Sucic | FC25 | Petar Sučić | 1.00 | 70.5 | — |
|  | Toni Fruk | median | — | — | 70.5 | — |
| ✗ | Luka Sucic | FIFA22 | L. Sučić | 1.00 | 70.0 | — |
| ✗ | Martin Baturina | FIFA22 | M. Baturina | 1.00 | 67.0 | — |
| ✗ | Kristijan Jakic | FIFA22 | K. Jakić | 1.00 | 65.0 | — |

#### Attackers &nbsp;(4/6 used · raw log-mean=75.40 · normalized=0.3863)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Ivan Perisic | FIFA22 | I. Perišić | 1.00 | 80.0 | — |
|  | Andrej Kramaric | FIFA22 | A. Kramarić | 1.00 | 78.5 | — |
|  | Petar Musa | FIFA22 | P. Musa | 1.00 | 72.0 | — |
|  | Ante Budimir | FIFA22 | A. Budimir | 1.00 | 71.5 | — |
| ✗ | Marco Pasalic | FIFA22 | M. Pašalić | 1.00 | 67.0 | — |
| ✗ | Igor Matanovic | FC25 | Igor Matanović | 1.00 | 66.0 | — |

---

### Curacao

**xG vs avg opponent:** 0.1665 &nbsp;|&nbsp; GK=0.4117 &nbsp;|&nbsp; DEF=0.0714 &nbsp;|&nbsp; MID=0.0660 &nbsp;|&nbsp; ATT=0.0632

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=72.44 · normalized=0.4117)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Eloy Room | FIFA22 | E. Room | 0.80 | 73.0 | — |
|  | Tyrick Bodack | median | — | — | 71.9 | — |
| ✗ | Trevor Doornbusch | TM | — | — | 65.0 | 100,000 |

#### Defenders &nbsp;(6/8 used · raw log-mean=70.30 · normalized=0.0714)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Deveron Fonville | median | — | — | 71.9 | — |
|  | Joshua Brenet | TM | — | — | 71.3 | 3,500,000 |
|  | Armando Obispo | TM | — | — | 70.5 | 3,000,000 |
|  | Riechedly Bazoer | TM | — | — | 70.2 | 2,800,000 |
|  | Sherel Floranus | FC25 | Sherel Floranus | 1.00 | 69.5 | — |
|  | Shurandy Sambo | TM | — | — | 68.5 | 2,000,000 |
| ✗ | Jurien Gaari | FIFA22 | J. Gaari | 0.74 | 66.5 | — |
| ✗ | Roshon van Eijma | FC25 | Roshon van Eijma | 1.00 | 64.0 | — |

#### Midfielders &nbsp;(5/7 used · raw log-mean=68.05 · normalized=0.0660)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Juninho Bacuna | FIFA22 | J. Bacuna | 1.00 | 71.0 | — |
|  | Tyrese Noslin | median | — | — | 70.5 | — |
|  | Leandro Bacuna | FC25 | Leandro Bacuna | 1.00 | 68.5 | — |
|  | Ar'jany Martha | FC25 | Ar'jany Martha | 1.00 | 65.5 | — |
|  | Livano Comenencia | TM | — | — | 65.0 | 800,000 |
| ✗ | Godfried Roemeratoe | FC25 | Godfried Roemeratoe | 1.00 | 60.5 | — |
| ✗ | Kevin Felida | FC25 | Kevin Felida | 1.00 | 59.0 | — |

#### Attackers &nbsp;(6/8 used · raw log-mean=71.28 · normalized=0.0632)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Jearl Margaritha | median | — | — | 74.0 | — |
|  | Tahith Chong | TM | — | — | 74.0 | 6,000,000 |
|  | Kenji Gorre | FIFA22 | K. Gorré | 0.81 | 73.0 | — |
|  | Sontje Hansen | TM | — | — | 70.5 | 3,000,000 |
|  | Jeremy Antonisse | FC25 | Jeremy Antonisse | 1.00 | 68.5 | — |
|  | Jurgen Locadia | TM | — | — | 67.9 | 1,800,000 |
| ✗ | Gervane Kastaneer | FIFA22 | G. Kastaneer | 0.79 | 67.5 | — |
| ✗ | Brandley Kuwas | TM | — | — | 65.0 | 450,000 |

---

### Czech Republic

**xG vs avg opponent:** 0.9354 &nbsp;|&nbsp; GK=0.5239 &nbsp;|&nbsp; DEF=0.5907 &nbsp;|&nbsp; MID=0.3272 &nbsp;|&nbsp; ATT=0.3737

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=75.12 · normalized=0.5239)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Matej Kovar | FC25 | Matěj Kovář | 1.00 | 76.2 | — |
|  | Jindrich Stanrk | FIFA22 | J. Staněk | 0.93 | 74.0 | — |
| ✗ | Lukas Hornicek | FIFA22 | L. Hornicek | 1.00 | 64.8 | — |

#### Defenders &nbsp;(6/9 used · raw log-mean=76.96 · normalized=0.5907)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Vladimir Coufal | FIFA22 | V. Coufal | 1.00 | 79.5 | — |
|  | Tomas Holes | FIFA22 | T. Holeš | 1.00 | 79.5 | — |
|  | Ladislav Krejci | FIFA22 | L. Krejčí | 1.00 | 78.5 | — |
|  | David Zima | FIFA22 | D. Zima | 1.00 | 76.0 | — |
|  | Robin Hranac | FC25 | Robin Hranáč | 1.00 | 75.5 | — |
|  | Jaroslav Zeleny | FC25 | Jaroslav Zelený | 1.00 | 73.0 | — |
| ✗ | Stepan Chaloupek | FC25 | Štěpán Chaloupek | 1.00 | 72.0 | — |
| ✗ | David Jurasek | FC25 | David Jurásek | 1.00 | 71.0 | — |
| ✗ | David Doudera | FC25 | David Douděra | 1.00 | 66.0 | — |

#### Midfielders &nbsp;(8/11 used · raw log-mean=72.89 · normalized=0.3272)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Lukas Provod | FIFA22 | L. Provod | 1.00 | 77.0 | — |
|  | Vladimir Darida | FIFA22 | V. Darida | 1.00 | 76.0 | — |
|  | Pavel Bucha | FIFA22 | P. Bucha | 1.00 | 75.0 | — |
|  | Tomas Soucek | FIFA22 | T. Souček | 1.00 | 74.0 | — |
|  | Hugo Sochurek | median | — | — | 70.5 | — |
|  | Alexandr Sojka | median | — | — | 70.5 | — |
|  | Denis Visinsky | median | — | — | 70.5 | — |
|  | Pavel Sulc | FIFA22 | P. Šulc | 1.00 | 70.0 | — |
| ✗ | Michal Sadilek | FIFA22 | M. Sadílek | 1.00 | 69.0 | — |
| ✗ | Lukas Cerv | FC25 | Lukáš Červ | 1.00 | 67.0 | — |
| ✗ | Tomas Ladra | FIFA22 | T. Kalas | 0.73 | 59.0 | — |

#### Attackers &nbsp;(4/6 used · raw log-mean=75.24 · normalized=0.3737)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Adam Hlozek | FIFA22 | A. Hložek | 1.00 | 76.5 | — |
|  | Jan Kuchta | FIFA22 | J. Kuchta | 1.00 | 76.0 | — |
|  | Patrik Schick | FIFA22 | P. Schick | 1.00 | 74.5 | — |
|  | Christophe Kabongo | median | — | — | 74.0 | — |
| ✗ | Mojmir Chytil | FC25 | Mojmír Chytil | 1.00 | 72.5 | — |
| ✗ | Tomas Chory | FIFA22 | T. Chorý | 1.00 | 57.5 | — |

---

### Ecuador

**xG vs avg opponent:** 0.7671 &nbsp;|&nbsp; GK=0.4614 &nbsp;|&nbsp; DEF=0.4304 &nbsp;|&nbsp; MID=0.1460 &nbsp;|&nbsp; ATT=0.3589

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=73.62 · normalized=0.4614)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Hernán Galíndez | FC25 | Hernán Galíndez | 1.00 | 74.2 | — |
|  | Moisés Ramírez | FC25 | Moisés Ramírez | 1.00 | 73.0 | — |
| ✗ | Gonzalo Valle | FC25 | Gonzalo Valle | 1.00 | 65.2 | — |

#### Defenders &nbsp;(6/8 used · raw log-mean=74.91 · normalized=0.4304)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Piero Hincapié | FC25 | Piero Hincapié | 1.00 | 80.5 | — |
|  | Willian Pacho | FC25 | Willian Pacho | 1.00 | 79.0 | — |
|  | Pervis Estupiñán | FC25 | Pervis Estupiñán | 1.00 | 76.0 | — |
|  | Jackson Porozo | FC25 | Jackson Porozo | 1.00 | 72.5 | — |
|  | Joel Ordóñez | FC25 | Joel Ordoñez | 1.00 | 71.0 | — |
|  | Félix Torres | FIFA22 | F. Torres | 0.80 | 71.0 | — |
| ✗ | Ángelo Preciado | FC25 | Ángelo Preciado | 1.00 | 69.0 | — |
| ✗ | Yaimar Medina | FC25 | Yaimar Medina | 1.00 | 57.0 | — |

#### Midfielders &nbsp;(7/10 used · raw log-mean=69.54 · normalized=0.1460)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Moisés Caicedo | FC25 | Moisés Caicedo | 1.00 | 76.5 | — |
|  | Gonzalo Plata | TM | — | — | 73.1 | 5,000,000 |
|  | Alan Franco | median | — | — | 70.5 | — |
|  | Kendry Páez | FC25 | Kendry Páez | 1.00 | 70.5 | — |
|  | Alan Minda | FC25 | Alan Minda | 1.00 | 67.5 | — |
|  | Pedro Vite | FC25 | Pedro Vite | 1.00 | 65.5 | — |
| ✗ | Jordy Alcívar | FIFA22 | J. Alcívar | 0.82 | 64.0 | — |
|  | John Yeboah | FC25 | John Yeboah | 1.00 | 64.0 | — |
| ✗ | Denil Castillo | FC25 | Denil Castillo | 1.00 | 53.5 | — |
| ✗ | Nilson Angulo | FIFA22 | N. Angulo | 1.00 | 52.0 | — |

#### Attackers &nbsp;(3/5 used · raw log-mean=75.05 · normalized=0.3589)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Enner Valencia | FIFA22 | E. Valencia | 0.83 | 81.0 | — |
|  | Kevin Rodríguez | FC25 | Kevin Rodríguez | 1.00 | 73.0 | — |
|  | Anthony Valencia | FC25 | Anthony Valencia | 1.00 | 71.5 | — |
| ✗ | Jeremy Arévalo | FC25 | Jeremy Sarmiento | 0.73 | 70.5 | — |
| ✗ | Jordy Caicedo | FC25 | Jordy Caicedo | 1.00 | 69.5 | — |

---

### Egypt

**xG vs avg opponent:** 1.7430 &nbsp;|&nbsp; GK=0.5237 &nbsp;|&nbsp; DEF=0.1351 &nbsp;|&nbsp; MID=0.1981 &nbsp;|&nbsp; ATT=0.8728

#### Goalkeepers &nbsp;(3/4 used · raw log-mean=75.11 · normalized=0.5237)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mohamed Alaa | TM | — | — | 82.0 | 30,000,000 |
|  | Mohamed El Shenawy | median | — | — | 71.9 | — |
|  | El Mahdy Soliman | median | — | — | 71.9 | — |
| ✗ | Mostafa Shobeir | TM | — | — | 65.0 | 100,000 |

#### Defenders &nbsp;(6/8 used · raw log-mean=71.12 · normalized=0.1351)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Hossam Abdelmagid | median | — | — | 71.9 | — |
|  | Tarek Alaa | median | — | — | 71.9 | — |
|  | Ahmed Fatouh | median | — | — | 71.9 | — |
|  | Yasser Ibrahim | median | — | — | 71.9 | — |
|  | Mohamed Abdelmonem | TM | — | — | 70.5 | 3,000,000 |
|  | Karim Hafez | FIFA22 | K. Hafez | 0.78 | 68.5 | — |
| ✗ | Rami Rabia | TM | — | — | 65.0 | 400,000 |
| ✗ | Mohamed Hany | FC25 | Mohamed Salah | 0.72 | 60.0 | — |

#### Midfielders &nbsp;(7/10 used · raw log-mean=70.50 · normalized=0.1981)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Marwan Attia | median | — | — | 70.5 | — |
|  | Nabil Emad | median | — | — | 70.5 | — |
|  | Hamdi Fathi | median | — | — | 70.5 | — |
|  | Mohannad Lashin | median | — | — | 70.5 | — |
|  | Mahmoud Saber | median | — | — | 70.5 | — |
|  | Mostafa Zico | median | — | — | 70.5 | — |
|  | Ahmed Sayed | median | — | — | 70.5 | — |
| ✗ | Emam Ashour | TM | — | — | 68.5 | 2,000,000 |
| ✗ | Haitham Hassan | FIFA22 | A. Hassan | 0.73 | 63.0 | — |
| ✗ | Mahmoud Hassan | FIFA22 | A. Hassan | 0.73 | 63.0 | — |

#### Attackers &nbsp;(3/5 used · raw log-mean=81.62 · normalized=0.8728)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mohamed Salah | FC25 | Mohamed Salah | 1.00 | 88.0 | — |
|  | Omar Marmoush | FC25 | Omar Marmoush | 1.00 | 83.5 | — |
| ✗ | Aqtay Abdullah | median | — | — | 74.0 | — |
| ✗ | Hamza Abdulkarim | median | — | — | 74.0 | — |
|  | Ibrahim Adel | median | — | — | 74.0 | — |

---

### England

**xG vs avg opponent:** 2.0424 &nbsp;|&nbsp; GK=0.7541 &nbsp;|&nbsp; DEF=0.7716 &nbsp;|&nbsp; MID=0.6696 &nbsp;|&nbsp; ATT=0.8352

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=80.62 · normalized=0.7541)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Jordan PICKFORD | FIFA22 | J. Pickford | 1.00 | 81.8 | — |
|  | Dean Henderson | FIFA22 | D. Henderson | 1.00 | 79.5 | — |
| ✗ | James TRAFFORD | FIFA22 | J. Trafford | 1.00 | 58.2 | — |

#### Defenders &nbsp;(6/9 used · raw log-mean=79.29 · normalized=0.7716)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Nico OREILLY | TM | — | — | 83.5 | 40,000,000 |
|  | John STONES | FIFA22 | J. Stones | 1.00 | 81.0 | — |
|  | Ezri KONSA | FC25 | Ezri Konsa | 1.00 | 80.5 | — |
|  | Reece JAMES | FIFA22 | R. James | 1.00 | 78.0 | — |
|  | Dan BURN | FIFA22 | D. Burn | 1.00 | 77.5 | — |
|  | Jarell QUANSAH | FC25 | Jarell Quansah | 1.00 | 75.5 | — |
| ✗ | Tino LIVRAMENTO | FC25 | Tino Livramento | 1.00 | 73.5 | — |
| ✗ | Marc GUEHI | FIFA22 | M. Guéhi | 1.00 | 73.0 | — |
| ✗ | Djed SPENCE | FIFA22 | D. Spence | 1.00 | 58.5 | — |

#### Midfielders &nbsp;(5/7 used · raw log-mean=79.22 · normalized=0.6696)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Jude BELLINGHAM | FC25 | Jude Bellingham | 1.00 | 85.5 | — |
|  | Jordan HENDERSON | FIFA22 | J. Henderson | 1.00 | 81.0 | — |
|  | Kobbie MAINOO | FC25 | Kobbie Mainoo | 1.00 | 77.5 | — |
|  | Eberechi EZE | FIFA22 | E. Eze | 1.00 | 77.0 | — |
|  | Elliot ANDERSON | FC25 | Elliot Anderson | 1.00 | 75.5 | — |
| ✗ | Declan RICE | FIFA22 | D. Rice | 1.00 | 72.5 | — |
| ✗ | Morgan ROGERS | FIFA22 | M. Rogers | 1.00 | 62.5 | — |

#### Attackers &nbsp;(5/7 used · raw log-mean=81.14 · normalized=0.8352)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Marcus RASHFORD | FIFA22 | M. Rashford | 1.00 | 87.0 | — |
|  | Noni MADUEKE | FC25 | Noni Madueke | 1.00 | 81.0 | — |
|  | Harry KANE | FIFA22 | H. Kane | 1.00 | 80.5 | — |
|  | Ollie WATKINS | FIFA22 | O. Watkins | 1.00 | 80.0 | — |
|  | Ivan TONEY | FIFA22 | I. Toney | 1.00 | 77.5 | — |
| ✗ | Bukayo SAKA | FIFA22 | B. Saka | 1.00 | 76.0 | — |
| ✗ | Anthony GORDON | FIFA22 | A. Gordon | 1.00 | 70.0 | — |

---

### France

**xG vs avg opponent:** 2.0737 &nbsp;|&nbsp; GK=0.8379 &nbsp;|&nbsp; DEF=1.0000 &nbsp;|&nbsp; MID=0.7376 &nbsp;|&nbsp; ATT=0.8233

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=82.62 · normalized=0.8379)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mike Maignan | FIFA22 | M. Maignan | 1.00 | 83.5 | — |
|  | Brice Samba | FC25 | Brice Samba | 1.00 | 81.8 | — |
| ✗ | Robin Risser | FC25 | Robin Risser | 1.00 | 67.0 | — |

#### Defenders &nbsp;(6/9 used · raw log-mean=82.22 · normalized=1.0000)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Theo Hernandez | FC25 | Theo Hernández | 1.00 | 85.0 | — |
|  | William Saliba | FC25 | William Saliba | 1.00 | 85.0 | — |
|  | Dayot Upamecano | FC25 | Dayot Upamecano | 1.00 | 83.0 | — |
|  | Lucas Hernandez | FC25 | Lucas Hernández | 1.00 | 81.0 | — |
|  | Jules Kounde | FIFA22 | J. Koundé | 1.00 | 81.0 | — |
|  | Maxence Lacroix | FIFA22 | M. Lacroix | 1.00 | 78.5 | — |
| ✗ | Lucas Digne | FIFA22 | L. Digne | 1.00 | 78.0 | — |
| ✗ | Ibrahima Konate | FIFA22 | I. Konaté | 1.00 | 78.0 | — |
| ✗ | Malo Gusto | FIFA22 | M. Gusto | 1.00 | 62.5 | — |

#### Midfielders &nbsp;(3/5 used · raw log-mean=80.48 · normalized=0.7376)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Manu Kone | TM | — | — | 84.6 | 50,000,000 |
|  | N'Golo Kante | FIFA22 | N. Kanté | 1.00 | 78.5 | — |
|  | Warren Zaire-Emery | FC25 | Warren Zaïre-Emery | 1.00 | 78.5 | — |
| ✗ | Adrien Rabiot | FIFA22 | A. Rabiot | 1.00 | 78.0 | — |
| ✗ | Aurelien Tchouameni | FIFA22 | A. Tchouaméni | 1.00 | 76.0 | — |

#### Attackers &nbsp;(6/9 used · raw log-mean=80.99 · normalized=0.8233)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Kylian Mbappe | FC25 | Kylian Mbappé | 1.00 | 93.5 | — |
|  | Ousmane Dembele | FIFA22 | O. Dembélé | 1.00 | 85.0 | — |
|  | Marcus Thuram | FC25 | Marcus Thuram | 1.00 | 84.0 | — |
|  | Bradley Barcola | FC25 | Bradley Barcola | 1.00 | 81.0 | — |
|  | Desire Doue | FC25 | Désiré Doué | 1.00 | 73.5 | — |
| ✗ | Maghnes Akliouche | FC25 | Maghnes Akliouche | 1.00 | 71.0 | — |
| ✗ | Jean-Philippe Mateta | FIFA22 | J. Mateta | 1.00 | 71.0 | — |
|  | Michael Olise | FIFA22 | M. Olise | 1.00 | 71.0 | — |
| ✗ | Rayan Cherki | FC25 | Rayan Cherki | 1.00 | 67.5 | — |

---

### Germany

**xG vs avg opponent:** 1.5396 &nbsp;|&nbsp; GK=0.8165 &nbsp;|&nbsp; DEF=0.7326 &nbsp;|&nbsp; MID=0.6581 &nbsp;|&nbsp; ATT=0.5639

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=82.11 · normalized=0.8165)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Manuel Neuer | FC25 | Manuel Neuer | 1.00 | 83.8 | — |
|  | Oliver Baumann | FIFA22 | O. Baumann | 1.00 | 80.5 | — |
| ✗ | Alexander Nübel | FIFA22 | A. Nübel | 1.00 | 75.2 | — |

#### Defenders &nbsp;(6/8 used · raw log-mean=78.78 · normalized=0.7326)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Antonio Rüdiger | FIFA22 | A. Rüdiger | 1.00 | 84.0 | — |
|  | Jonathan Tah | FIFA22 | J. Tah | 1.00 | 80.0 | — |
|  | Joshua Kimmich | FC25 | Joshua Kimmich | 1.00 | 79.0 | — |
|  | Waldemar Anton | FIFA22 | W. Anton | 1.00 | 77.5 | — |
|  | Malick Thiaw | FC25 | Malick Thiaw | 1.00 | 77.5 | — |
|  | Nico Schlotterbeck | FIFA22 | N. Schlotterbeck | 1.00 | 75.0 | — |
| ✗ | David Raum | FIFA22 | D. Raum | 1.00 | 67.0 | — |
| ✗ | Nathaniel Brown | FC25 | Nathaniel Brown | 1.00 | 55.0 | — |

#### Midfielders &nbsp;(6/9 used · raw log-mean=79.01 · normalized=0.6581)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Lennart Karl | TM | — | — | 85.5 | 60,000,000 |
|  | Leon Goretzka | FC25 | Leon Goretzka | 1.00 | 80.5 | — |
|  | Nadiem Amiri | FIFA22 | N. Amiri | 1.00 | 80.0 | — |
|  | Pascal Gross | FIFA22 | P. Groß | 1.00 | 77.5 | — |
|  | Jamal Musiala | FIFA22 | J. Musiala | 1.00 | 75.5 | — |
|  | Felix Nmecha | FC25 | Felix Nmecha | 1.00 | 75.5 | — |
| ✗ | Aleksandar Pavlovic | FC25 | Aleksandar Pavlović | 1.00 | 73.5 | — |
| ✗ | Angelo Stiller | FIFA22 | A. Stiller | 1.00 | 69.5 | — |
| ✗ | Jamie Leweling | FIFA22 | J. Leweling | 1.00 | 65.0 | — |

#### Attackers &nbsp;(4/6 used · raw log-mean=77.67 · normalized=0.5639)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Leroy Sané | FC25 | Leroy Sané | 1.00 | 86.5 | — |
|  | Florian Wirtz | FC25 | Florian Wirtz | 1.00 | 79.5 | — |
|  | Kai Havertz | FC25 | Kai Havertz | 1.00 | 79.0 | — |
|  | Deniz Undav | FIFA22 | D. Undav | 1.00 | 67.0 | — |
| ✗ | Maximilian Beier | FIFA22 | M. Beier | 1.00 | 65.0 | — |
| ✗ | Nick Woltemade | FIFA22 | N. Woltemade | 1.00 | 61.0 | — |

---

### Ghana

**xG vs avg opponent:** 1.2720 &nbsp;|&nbsp; GK=0.3435 &nbsp;|&nbsp; DEF=0.2145 &nbsp;|&nbsp; MID=0.2947 &nbsp;|&nbsp; ATT=0.5726

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=70.80 · normalized=0.3435)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Benjamin ASARE | median | — | — | 71.9 | — |
|  | Lawrence Ati ZIGI | FIFA22 | L. Zigi | 1.00 | 69.8 | — |
| ✗ | Joseph ANANG | TM | — | — | 65.0 | 300,000 |

#### Defenders &nbsp;(6/9 used · raw log-mean=72.14 · normalized=0.2145)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Jerome OPOKU | FC25 | Jerome Opoku | 1.00 | 76.0 | — |
|  | Baba RAHMAN | FC25 | Baba Rahman | 1.00 | 72.0 | — |
|  | Kojo Peprah OPPONG | median | — | — | 71.9 | — |
|  | Abdul MUMIN | FC25 | Abdul Mumin | 1.00 | 71.5 | — |
|  | Alidu SEIDU | FC25 | Alidu Seidu | 1.00 | 71.0 | — |
|  | Marvin SENAYA | TM | — | — | 70.5 | 3,000,000 |
| ✗ | Derrick LUCKASSEN | TM | — | — | 65.9 | 1,200,000 |
| ✗ | Gideon MENSAH | FIFA22 | G. Mensah | 1.00 | 65.0 | — |
| ✗ | Jonas ADJETEY | FC25 | Jonas Adjetey | 1.00 | 64.5 | — |

#### Midfielders &nbsp;(4/6 used · raw log-mean=72.29 · normalized=0.2947)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Thomas PARTEY | FIFA22 | T. Partey | 1.00 | 81.5 | — |
|  | Antoine SEMENYO | FC25 | Antoine Semenyo | 1.00 | 72.0 | — |
|  | Caleb YIRENKYI | median | — | — | 70.5 | — |
|  | Elisha OWUSU | FC25 | Elisha Owusu | 1.00 | 66.0 | — |
| ✗ | Kwasi SIBO | FC25 | Kwasi Sibo | 1.00 | 59.5 | — |
| ✗ | Augustine BOAKYE | FIFA22 | A. Boakye | 1.00 | 55.5 | — |

#### Attackers &nbsp;(6/8 used · raw log-mean=77.79 · normalized=0.5726)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Inaki WILLIAMS | FC25 | Iñaki Williams | 1.00 | 87.5 | — |
|  | Kamaldeen SULEMANA | FIFA22 | K. Sulemana | 1.00 | 79.5 | — |
|  | Brandon THOMAS-ASANTE | FC25 | Brandon Thomas-Asante | 1.00 | 76.0 | — |
|  | Ernest NUAMAH | FC25 | Ernest Nuamah | 1.00 | 76.0 | — |
|  | Christopher Bonsu BAAH | FC25 | Christopher Bonsu Baah | 1.00 | 74.5 | — |
|  | Fatawu ISSAHAKU | median | — | — | 74.0 | — |
| ✗ | Jordan AYEW | FC25 | Jordan Ayew | 1.00 | 72.0 | — |
| ✗ | Prince ADU | TM | — | — | 71.3 | 3,500,000 |

---

### Haiti

**xG vs avg opponent:** 0.2361 &nbsp;|&nbsp; GK=0.2408 &nbsp;|&nbsp; DEF=0.2066 &nbsp;|&nbsp; MID=0.3027 &nbsp;|&nbsp; ATT=0.0000

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=68.35 · normalized=0.2408)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Josue Duverger | median | — | — | 71.9 | — |
| ✗ | Alexandre Pierre | TM | — | — | 65.0 | 100,000 |
|  | Johny Placide | FIFA22 | J. Placide | 1.00 | 65.0 | — |

#### Defenders &nbsp;(6/8 used · raw log-mean=72.03 · normalized=0.2066)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Jean-Kevin Duverne | FC25 | Jean-Kévin Duverne | 1.00 | 72.5 | — |
|  | Hannes Delcroix | TM | — | — | 71.9 | 4,000,000 |
| ✗ | Ricardo Ade | median | — | — | 71.9 | — |
|  | Martin Experience | median | — | — | 71.9 | — |
|  | Duke Lacroix | median | — | — | 71.9 | — |
|  | Wilguens Paugain | median | — | — | 71.9 | — |
|  | Keeto Thermoncy | median | — | — | 71.9 | — |
| ✗ | Carlens Arcus | FC25 | Carlens Arcus | 1.00 | 67.0 | — |

#### Midfielders &nbsp;(4/6 used · raw log-mean=72.43 · normalized=0.3027)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Jean-Ricner Bellegarde | TM | — | — | 78.6 | 15,000,000 |
|  | Carl Fred Sainte | median | — | — | 70.5 | — |
|  | Woodensky Pierre | median | — | — | 70.5 | — |
|  | Dominique Simon | median | — | — | 70.5 | — |
| ✗ | Danley Jean Jacques | FC25 | Danley Jean Jacques | 1.00 | 66.0 | — |
| ✗ | Leverton Pierre | FIFA22 | L. Pierre | 1.00 | 61.5 | — |

#### Attackers &nbsp;(6/9 used · raw log-mean=70.47 · normalized=0.0000)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Wilson Isidor | TM | — | — | 79.5 | 18,000,000 |
|  | Duckens Nazon | FC25 | Duckens Nazon | 1.00 | 72.0 | — |
|  | Josue Casimir | TM | — | — | 71.3 | 3,500,000 |
|  | Derrick Etienne Jr. | FIFA22 | D. Etienne Jr. | 1.00 | 68.5 | — |
|  | Frantzdy Pierrot | FIFA22 | F. Pierrot | 1.00 | 66.5 | — |
|  | Louicius Deedson | TM | — | — | 65.9 | 1,200,000 |
| ✗ | Yassin Fortune | TM | — | — | 65.0 | 400,000 |
| ✗ | Lenny Joseph | TM | — | — | 65.0 | 500,000 |
| ✗ | Ruben Providence | TM | — | — | 65.0 | 300,000 |

---

### Iran

**xG vs avg opponent:** 0.7583 &nbsp;|&nbsp; GK=0.2573 &nbsp;|&nbsp; DEF=0.1538 &nbsp;|&nbsp; MID=0.2738 &nbsp;|&nbsp; ATT=0.2993

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=68.75 · normalized=0.2573)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Alireza Beiranvand | FIFA22 | A. Beiranvand | 0.86 | 69.5 | — |
|  | Payam Niazmand | FIFA22 | S. Niazmand | 0.82 | 68.0 | — |
| ✗ | Hossein Hosseini | TM | — | — | 65.0 | 700,000 |

#### Defenders &nbsp;(6/8 used · raw log-mean=71.36 · normalized=0.1538)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Daniyal Eiri | median | — | — | 71.9 | — |
|  | Saleh Hardani | median | — | — | 71.9 | — |
|  | Hossein Kanaani | median | — | — | 71.9 | — |
|  | Shoja Khalilzadeh | median | — | — | 71.9 | — |
|  | Ali Nemati | median | — | — | 71.9 | — |
|  | Ehsan Hajsafi | FIFA22 | E. Haji Safi | 0.93 | 68.5 | — |
| ✗ | Milad Mohammadi | TM | — | — | 66.3 | 1,300,000 |
| ✗ | Ramin Rezaeian | TM | — | — | 65.0 | 450,000 |

#### Midfielders &nbsp;(7/10 used · raw log-mean=71.90 · normalized=0.2738)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mehdi Ghayedi | FIFA22 | M. Taremi | 0.72 | 75.0 | — |
|  | Mehdi Torabi | FIFA22 | M. Taremi | 0.75 | 75.0 | — |
|  | Alireza Jahanbakhsh | FIFA22 | A. Jahanbakhsh | 1.00 | 72.0 | — |
|  | Rouzbeh Cheshmi | median | — | — | 70.5 | — |
|  | Amir Mohammad Razzaghinia | median | — | — | 70.5 | — |
|  | Aria Yousefi | median | — | — | 70.5 | — |
|  | Saman Ghoddos | FIFA22 | S. Ghoddos | 1.00 | 70.0 | — |
| ✗ | Mohammad Ghorbani | FIFA22 | M. Mohebi | 0.75 | 64.0 | — |
| ✗ | Mohammad Mohebi | FIFA22 | M. Mohebi | 1.00 | 64.0 | — |
| ✗ | Saeid Ezatolahi | FIFA22 | S. Ezatolahi | 0.85 | 61.0 | — |

#### Attackers &nbsp;(3/5 used · raw log-mean=74.29 · normalized=0.2993)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mehdi Taremi | FIFA22 | M. Taremi | 1.00 | 77.5 | — |
|  | Dennis Dargahi | median | — | — | 74.0 | — |
|  | Ali Alipour | FIFA22 | A. Alipour | 1.00 | 71.5 | — |
| ✗ | Amirhossein Hosseinzadeh | TM | — | — | 65.0 | 700,000 |
| ✗ | Shahriyar Moghanlou | TM | — | — | 65.0 | 900,000 |

---

### Iraq

**xG vs avg opponent:** 0.4918 &nbsp;|&nbsp; GK=0.3882 &nbsp;|&nbsp; DEF=0.1994 &nbsp;|&nbsp; MID=0.1396 &nbsp;|&nbsp; ATT=0.2104

#### Goalkeepers &nbsp;(3/4 used · raw log-mean=71.88 · normalized=0.3882)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Ahmed Basil | median | — | — | 71.9 | — |
|  | Jalal Hassan | median | — | — | 71.9 | — |
|  | Kumel Saadi | median | — | — | 71.9 | — |
|  | Fahad Talib | median | — | — | 71.9 | — |

#### Defenders &nbsp;(8/12 used · raw log-mean=71.94 · normalized=0.1994)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Merchas Doski | median | — | — | 71.9 | — |
|  | Akam Hashem | median | — | — | 71.9 | — |
|  | Maytham Jabbar | median | — | — | 71.9 | — |
|  | Ahmed Maknzi | median | — | — | 71.9 | — |
|  | Dario Naamo | median | — | — | 71.9 | — |
|  | Mustafa Saadoon | median | — | — | 71.9 | — |
|  | Rebin Sulaka | median | — | — | 71.9 | — |
|  | Zaid Tahseen | median | — | — | 71.9 | — |
|  | Manaf Younis | median | — | — | 71.9 | — |
| ✗ | Frans Putros | FIFA22 | F. Putros | 0.80 | 64.5 | — |
| ✗ | Hussein Ali | FC25 | Hussein Ali | 1.00 | 59.5 | — |
| ✗ | Ahmed Yahya | FIFA22 | A. Yasin | 0.73 | 54.5 | — |

#### Midfielders &nbsp;(10/14 used · raw log-mean=69.42 · normalized=0.1396)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Hasan Abdulkareem | median | — | — | 70.5 | — |
|  | Ibrahim Bayesh | median | — | — | 70.5 | — |
|  | Marko Farji | median | — | — | 70.5 | — |
|  | Zaid Ismail | median | — | — | 70.5 | — |
|  | Ali Jassim | median | — | — | 70.5 | — |
|  | Karar Nabeel | median | — | — | 70.5 | — |
|  | Jussef Nasrawe | median | — | — | 70.5 | — |
|  | Kevin Yakob | FC25 | Kevin Yakob | 1.00 | 70.5 | — |
|  | Zidane Iqbal | FC25 | Zidane Iqbal | 1.00 | 65.5 | — |
| ✗ | Amir Al Ammari | FC25 | Amir Al-Ammari | 1.00 | 65.0 | — |
| ✗ | Peter Gwargis | TM | — | — | 65.0 | 250,000 |
| ✗ | Ahmed Qasim | FIFA22 | A. Yasin | 0.82 | 65.0 | — |
|  | Aimar Sher | TM | — | — | 65.0 | 750,000 |
| ✗ | Youssef Amyn | FC25 | Youssef Amyn | 1.00 | 64.0 | — |

#### Attackers &nbsp;(3/4 used · raw log-mean=73.16 · normalized=0.2104)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Aymen Hussein | median | — | — | 74.0 | — |
|  | Ali Yousef | median | — | — | 74.0 | — |
|  | Ali Al Hamadi | FC25 | Ali Al Hamadi | 1.00 | 71.5 | — |
| ✗ | Mohanad Ali | TM | — | — | 65.0 | 350,000 |

---

### Côte d'Ivoire

**xG vs avg opponent:** 1.4742 &nbsp;|&nbsp; GK=0.3619 &nbsp;|&nbsp; DEF=0.5165 &nbsp;|&nbsp; MID=0.4314 &nbsp;|&nbsp; ATT=0.6251

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=71.25 · normalized=0.3619)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Yahia Fofana | FC25 | Yahia Fofana | 1.00 | 72.0 | — |
|  | Alban Lafont | TM | — | — | 70.5 | 3,000,000 |
| ✗ | Mohamed Kone | FC25 | Mohamed Koné | 1.00 | 65.5 | — |

#### Defenders &nbsp;(6/8 used · raw log-mean=76.01 · normalized=0.5165)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Ousmane Diomande | FC25 | Ousmane Diomande | 1.00 | 80.0 | — |
|  | Wilfried Singo | FC25 | Wilfried Singo | 1.00 | 80.0 | — |
|  | Evan Ndicka | FC25 | Evan Ndicka | 1.00 | 77.0 | — |
|  | Odilon Kossounou | FIFA22 | O. Kossounou | 1.00 | 75.5 | — |
|  | Emmanuel Agbadou | FIFA22 | E. Agbadou | 1.00 | 72.5 | — |
|  | Guela Doue | FC25 | Guéla Doué | 1.00 | 71.5 | — |
| ✗ | Ghislain Konan | FIFA22 | G. Konan | 1.00 | 70.5 | — |
| ✗ | Clement Akpa | FC25 | Clément Akpa | 1.00 | 61.0 | — |

#### Midfielders &nbsp;(4/6 used · raw log-mean=74.81 · normalized=0.4314)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Jean Michael Seri | FIFA22 | J. Seri | 1.00 | 77.5 | — |
|  | Franck Kessie | FIFA22 | F. Kessié | 0.77 | 77.0 | — |
|  | Seko Fofana | FIFA22 | S. Fofana | 1.00 | 75.0 | — |
|  | Ibrahim Sangare | FIFA22 | I. Sangaré | 1.00 | 70.0 | — |
| ✗ | Parfait Guiagon | FC25 | Parfait Guiagon | 1.00 | 69.5 | — |
| ✗ | Christ Inao Oulai | FC25 | Christian Kouan Oulaï | 0.74 | 66.5 | — |

#### Attackers &nbsp;(6/9 used · raw log-mean=78.46 · normalized=0.6251)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Nicolas Pepe | FIFA22 | N. Pépé | 1.00 | 83.5 | — |
|  | Bazoumana Toure | TM | — | — | 81.1 | 25,000,000 |
|  | Amad Diallo | FC25 | Amad Diallo | 1.00 | 78.0 | — |
|  | Elye Wahi | TM | — | — | 77.4 | 12,000,000 |
|  | Evann Guessand | FC25 | Evann Guessand | 1.00 | 76.0 | — |
|  | Oumar Diakite | FC25 | Oumar Diakité | 1.00 | 75.0 | — |
| ✗ | Ange-Yoan Bonny | median | — | — | 74.0 | — |
| ✗ | Simon Adingra | FIFA22 | S. Adingra | 1.00 | 66.0 | — |
| ✗ | Yan Diomande | FIFA22 | S. Diomande | 0.82 | 54.5 | — |

---

### Japan

**xG vs avg opponent:** 1.1196 &nbsp;|&nbsp; GK=0.3593 &nbsp;|&nbsp; DEF=0.4856 &nbsp;|&nbsp; MID=0.5601 &nbsp;|&nbsp; ATT=0.3751

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=71.18 · normalized=0.3593)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Keisuke Osako | median | — | — | 71.9 | — |
|  | Zion Suzuki | FC25 | Zion Suzuki | 1.00 | 70.5 | — |
| ✗ | Tomoki Hayakawa | FIFA22 | T. Hayakawa | 0.80 | 55.8 | — |

#### Defenders &nbsp;(6/9 used · raw log-mean=75.61 · normalized=0.4856)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Takehiro Tomiyasu | FC25 | Takehiro Tomiyasu | 1.00 | 80.0 | — |
|  | Hiroki Ito | FC25 | Hiroki Ito | 1.00 | 77.5 | — |
|  | Tsuyoshi Watanabe | FC25 | Tsuyoshi Watanabe | 1.00 | 75.5 | — |
|  | Ko Itakura | FC25 | Ko Itakura | 1.00 | 75.0 | — |
|  | Shogo Taniguchi | FC25 | Shogo Taniguchi | 1.00 | 74.0 | — |
|  | Junnosuke Suzuki | median | — | — | 71.9 | — |
| ✗ | Yukinari Sugawara | FC25 | Yukinari Sugawara | 1.00 | 71.0 | — |
| ✗ | Ayumu Seko | FC25 | Ayumu Seko | 1.00 | 69.0 | — |
| ✗ | Yuto Nagatomo | FIFA22 | Y. Nagatomo | 0.87 | 68.5 | — |

#### Midfielders &nbsp;(6/8 used · raw log-mean=77.19 · normalized=0.5601)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Daichi Kamada | FC25 | Daichi Kamada | 1.00 | 81.5 | — |
|  | Takefusa Kubo | FC25 | Takefusa Kubo | 1.00 | 79.5 | — |
|  | Ritsu Doan | FC25 | Ritsu Doan | 1.00 | 78.5 | — |
|  | Junya Ito | FC25 | Junya Ito | 1.00 | 76.5 | — |
|  | Wataru Endo | FC25 | Wataru Endo | 1.00 | 74.5 | — |
|  | Keito Nakamura | FC25 | Keito Nakamura | 1.00 | 73.0 | — |
| ✗ | Ao Tanaka | FC25 | Ao Tanaka | 1.00 | 70.5 | — |
| ✗ | Kaishu Sano | FC25 | Kaishū Sano | 1.00 | 67.0 | — |

#### Attackers &nbsp;(4/6 used · raw log-mean=75.26 · normalized=0.3751)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Daizen Maeda | FC25 | Daizen Maeda | 1.00 | 82.0 | — |
|  | Ayase Ueda | FC25 | Ayase Ueda | 1.00 | 75.0 | — |
|  | Keisuke Goto | median | — | — | 74.0 | — |
|  | Yuito Suzuki | FC25 | Yuito Suzuki | 1.00 | 70.5 | — |
| ✗ | Kento Shiogai | TM | — | — | 69.6 | 2,500,000 |
| ✗ | Koki Ogawa | FC25 | Koki Ogawa | 1.00 | 59.0 | — |

---

### Jordan

**xG vs avg opponent:** 0.8312 &nbsp;|&nbsp; GK=0.3882 &nbsp;|&nbsp; DEF=0.1994 &nbsp;|&nbsp; MID=0.1981 &nbsp;|&nbsp; ATT=0.3718

#### Goalkeepers &nbsp;(3/4 used · raw log-mean=71.88 · normalized=0.3882)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Yazid Abulaila | median | — | — | 71.9 | — |
|  | Abdallah Al Fakhouri | median | — | — | 71.9 | — |
|  | Ahmad Al Juaidi | median | — | — | 71.9 | — |
|  | Nour Bani Attiah | median | — | — | 71.9 | — |

#### Defenders &nbsp;(9/13 used · raw log-mean=71.94 · normalized=0.1994)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Mohammad Abualnadi | median | — | — | 71.9 | — |
| ✗ | Yousef Abu Al Jazar | median | — | — | 71.9 | — |
| ✗ | Husam Abu Dahab | median | — | — | 71.9 | — |
|  | Mohammad Abu Hashish | median | — | — | 71.9 | — |
|  | Mohannad Abu Taha | median | — | — | 71.9 | — |
|  | Saed Al Rosan | median | — | — | 71.9 | — |
|  | Ahmad Assaf | median | — | — | 71.9 | — |
|  | Anas Badawi | median | — | — | 71.9 | — |
|  | Abdallah Nasib | median | — | — | 71.9 | — |
|  | Ehsan Haddad | median | — | — | 71.9 | — |
|  | Saleem Obaid | median | — | — | 71.9 | — |
|  | Mohammad Taha | median | — | — | 71.9 | — |
| ✗ | Yazan Al Arab | FC25 | Yazan Al-Arab | 1.00 | 66.5 | — |

#### Midfielders &nbsp;(5/7 used · raw log-mean=70.50 · normalized=0.1981)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Mohammad Al Dawoud | median | — | — | 70.5 | — |
| ✗ | Nizar Al Rashdan | median | — | — | 70.5 | — |
|  | Noor Al Rawabdeh | median | — | — | 70.5 | — |
|  | Rajaei Ayed | median | — | — | 70.5 | — |
|  | Amer Jamous | median | — | — | 70.5 | — |
|  | Yousef Qashi | median | — | — | 70.5 | — |
|  | Ibrahim Sadeh | median | — | — | 70.5 | — |

#### Attackers &nbsp;(4/6 used · raw log-mean=75.22 · normalized=0.3718)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mousa Al Tamari | FC25 | Musa Al Tamari | 0.97 | 79.0 | — |
| ✗ | Mohammad Abu Zraiq | median | — | — | 74.0 | — |
| ✗ | Ali Azaizeh | median | — | — | 74.0 | — |
|  | Odeh Fakhoury | median | — | — | 74.0 | — |
|  | Ali Olwan | median | — | — | 74.0 | — |
|  | Ibrahim Sabra | median | — | — | 74.0 | — |

---

### Mexico

**xG vs avg opponent:** 0.6088 &nbsp;|&nbsp; GK=0.4734 &nbsp;|&nbsp; DEF=0.5204 &nbsp;|&nbsp; MID=0.2130 &nbsp;|&nbsp; ATT=0.2432

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=73.91 · normalized=0.4734)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Carlos Acevedo | FIFA22 | C. Acevedo | 0.82 | 76.0 | — |
|  | Raul Rangel | median | — | — | 71.9 | — |
| ✗ | Guillermo Ochoa | TM | — | — | 65.0 | 1,000,000 |

#### Defenders &nbsp;(5/7 used · raw log-mean=76.06 · normalized=0.5204)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Edson Alvarez | FC25 | Edson Álvarez | 1.00 | 85.0 | — |
|  | Cesar Montes | FC25 | César Montes | 1.00 | 76.0 | — |
|  | Jorge Sanchez | FIFA22 | J. Sánchez | 0.82 | 74.5 | — |
|  | Johan Vasquez | FC25 | Johan Vásquez | 1.00 | 74.5 | — |
|  | Jesus Gallardo | FIFA22 | J. Gallardo | 0.83 | 71.0 | — |
| ✗ | Israel Reyes | FIFA22 | I. Reyes | 0.77 | 61.5 | — |
| ✗ | Mateo Chavez | FIFA22 | O. Chávez | 0.80 | 60.5 | — |

#### Midfielders &nbsp;(6/8 used · raw log-mean=70.77 · normalized=0.2130)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Orbelin Pineda | FC25 | Orbelín Pineda | 1.00 | 76.5 | — |
|  | Alvaro Fidalgo | TM | — | — | 74.7 | 7,000,000 |
|  | Luis Chavez | FIFA22 | L. Chávez | 0.84 | 70.5 | — |
|  | Gilberto Mora | median | — | — | 70.5 | — |
|  | Brian Gutierrez | FIFA22 | A. Gutiérrez | 0.85 | 66.5 | — |
|  | Obed Vargas | FC25 | Obed Vargas | 1.00 | 66.5 | — |
| ✗ | Erik Lira | FIFA22 | E. Lira | 0.80 | 66.0 | — |
| ✗ | Luis Romo | FIFA22 | L. Romo | 0.80 | 65.0 | — |

#### Attackers &nbsp;(6/8 used · raw log-mean=73.58 · normalized=0.2432)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Julian Quinones | FC25 | Julian Quiñones | 1.00 | 83.0 | — |
|  | Santiago Gimenez | FC25 | Santiago Giménez | 1.00 | 79.5 | — |
|  | Alexis Vega | median | — | — | 74.0 | — |
|  | Roberto Alvarado | FIFA22 | R. Alvarado | 0.77 | 73.5 | — |
|  | Cesar Huerta | FIFA22 | C. Huerta | 0.80 | 68.0 | — |
|  | Raul Jimenez | FC25 | Raúl Jiménez | 1.00 | 65.0 | — |
| ✗ | Armando Gonzalez | FIFA22 | S. González | 0.79 | 57.0 | — |
| ✗ | Guillermo Martinez | FIFA22 | G. Martínez | 0.86 | 55.5 | — |

---

### Morocco

**xG vs avg opponent:** 1.6119 &nbsp;|&nbsp; GK=0.5833 &nbsp;|&nbsp; DEF=0.4746 &nbsp;|&nbsp; MID=0.5594 &nbsp;|&nbsp; ATT=0.6459

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=76.54 · normalized=0.5833)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Yassine Bounou | FIFA22 | Y. Bounou | 1.00 | 81.5 | — |
|  | Reda Tagnaouti | median | — | — | 71.9 | — |
| ✗ | Munir El Kajoui | TM | — | — | 65.0 | 1,000,000 |

#### Defenders &nbsp;(6/9 used · raw log-mean=75.47 · normalized=0.4746)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Anass Salah-Eddine | TM | — | — | 77.4 | 12,000,000 |
|  | Issa Diop | TM | — | — | 76.5 | 10,000,000 |
|  | Achraf Hakimi | FC25 | Achraf Hakimi | 1.00 | 76.5 | — |
|  | Nayef Aguerd | FIFA22 | N. Aguerd | 1.00 | 76.5 | — |
|  | Noussair Mazraoui | FIFA22 | N. Mazraoui | 1.00 | 73.0 | — |
|  | Chadi Riad | FC25 | Chadi Riad | 1.00 | 73.0 | — |
| ✗ | Redouane Halhal | TM | — | — | 65.0 | 100,000 |
| ✗ | Zakaria El Ouahdi | FC25 | Zakaria El Ouahdi | 1.00 | 60.0 | — |
| ✗ | Youssef Belammari | FIFA22 | Y. El Arabi | 0.79 | 53.5 | — |

#### Midfielders &nbsp;(5/7 used · raw log-mean=77.18 · normalized=0.5594)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Ayyoub Bouaddi | TM | — | — | 83.5 | 40,000,000 |
|  | Bilal El Khannouss | FC25 | Bilal El Khannouss | 1.00 | 79.5 | — |
|  | Ismael Saibari | FC25 | Ismael Saibari | 1.00 | 75.5 | — |
|  | Samir El Mourabet | TM | — | — | 75.4 | 8,000,000 |
|  | Sofyan Amrabat | FIFA22 | S. Amrabat | 1.00 | 72.5 | — |
| ✗ | Neil El Aynaoui | FC25 | Neil El Aynaoui | 1.00 | 72.0 | — |
| ✗ | Azzedine Ounahi | FIFA22 | A. Ounahi | 1.00 | 57.0 | — |

#### Attackers &nbsp;(5/7 used · raw log-mean=78.72 · normalized=0.6459)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Brahim Díaz | TM | — | — | 83.5 | 40,000,000 |
|  | Chemsdine Talbi | TM | — | — | 80.5 | 22,000,000 |
|  | Soufiane Rahimi | FIFA22 | S. Rahimi | 1.00 | 79.5 | — |
|  | Abde Ezzalzouli | FC25 | Abdessamad Ezzalzouli | 0.83 | 76.5 | — |
|  | Gessime Yassine | median | — | — | 74.0 | — |
| ✗ | Ayoub El Kaabi | FIFA22 | A. El Kaabi | 1.00 | 69.5 | — |
| ✗ | Ayoube Amaimouni | FC25 | Ayoub Amraoui | 0.83 | 57.0 | — |

---

### Netherlands

**xG vs avg opponent:** 1.8930 &nbsp;|&nbsp; GK=0.2779 &nbsp;|&nbsp; DEF=0.9492 &nbsp;|&nbsp; MID=0.5721 &nbsp;|&nbsp; ATT=0.7949

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=69.24 · normalized=0.2779)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mark Flekken | FIFA22 | M. Flekken | 1.00 | 73.8 | — |
|  | Bart Verbruggen | FIFA22 | B. Verbruggen | 1.00 | 65.0 | — |
| ✗ | Robin Roefs | FIFA22 | R. Roefs | 1.00 | 56.2 | — |

#### Defenders &nbsp;(5/7 used · raw log-mean=81.57 · normalized=0.9492)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Virgil van Dijk | FIFA22 | V. van Dijk | 1.00 | 87.5 | — |
|  | Denzel Dumfries | FIFA22 | D. Dumfries | 0.80 | 83.5 | — |
|  | Jorrel Hato | TM | — | — | 82.8 | 35,000,000 |
|  | Nathan Aké | FIFA22 | N. Aké | 1.00 | 77.5 | — |
|  | Jurriën Timber | FIFA22 | J. Timber | 0.73 | 77.0 | — |
| ✗ | Jan Paul van Hecke | FIFA22 | J. van Hecke | 1.00 | 71.0 | — |
| ✗ | Micky van de Ven | FIFA22 | M. van de Ven | 1.00 | 70.0 | — |

#### Midfielders &nbsp;(6/8 used · raw log-mean=77.42 · normalized=0.5721)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Frenkie de Jong | FIFA22 | F. de Jong | 1.00 | 86.5 | — |
|  | Mats Wieffer | TM | — | — | 81.1 | 25,000,000 |
|  | Ryan Gravenberch | FIFA22 | R. Gravenberch | 0.90 | 79.5 | — |
|  | Teun Koopmeiners | FIFA22 | T. Koopmeiners | 1.00 | 75.5 | — |
|  | Marten de Roon | FIFA22 | M. de Roon | 0.85 | 72.0 | — |
|  | Guus Til | FIFA22 | G. Til | 0.77 | 71.0 | — |
| ✗ | Tijjani Reijnders | FIFA22 | T. Reijnders | 1.00 | 68.5 | — |
| ✗ | Quinten Timber | FIFA22 | Q. Timber | 0.73 | 68.5 | — |

#### Attackers &nbsp;(6/8 used · raw log-mean=80.63 · normalized=0.7949)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Donyell Malen | FIFA22 | D. Malen | 1.00 | 84.5 | — |
|  | Memphis Depay | FIFA22 | M. Depay | 1.00 | 82.5 | — |
|  | Cody Gakpo | FIFA22 | C. Gakpo | 0.82 | 81.5 | — |
|  | Justin Kluivert | FIFA22 | J. Kluivert | 1.00 | 80.5 | — |
|  | Noa Lang | FIFA22 | N. Lang | 0.86 | 78.0 | — |
|  | Brian Brobbey | FIFA22 | B. Brobbey | 0.82 | 77.0 | — |
| ✗ | Crysencio Summerville | FIFA22 | C. Summerville | 1.00 | 74.5 | — |
| ✗ | Wout Weghorst | FIFA22 | W. Weghorst | 1.00 | 73.0 | — |

---

### New Zealand

**xG vs avg opponent:** 0.5709 &nbsp;|&nbsp; GK=0.0000 &nbsp;|&nbsp; DEF=0.1042 &nbsp;|&nbsp; MID=0.0000 &nbsp;|&nbsp; ATT=0.3137

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=62.60 · normalized=0.0000)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Max CROCOMBE | FC25 | Max Crocombe | 1.00 | 64.5 | — |
|  | Michael WOUD | FC25 | Michael Woud | 1.00 | 60.8 | — |
| ✗ | Alex PAULSEN | FIFA22 | A. Paulsen | 1.00 | 56.5 | — |

#### Defenders &nbsp;(6/9 used · raw log-mean=70.72 · normalized=0.1042)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Michael BOXALL | FC25 | Michael Boxall | 1.00 | 73.5 | — |
|  | Liberato CACACE | FC25 | Liberato Cacace | 1.00 | 72.0 | — |
|  | Tim PAYNE | FC25 | Tim Payne | 1.00 | 71.5 | — |
|  | Finn SURMAN | FC25 | Finn Surman | 1.00 | 71.5 | — |
|  | Tyler BINDON | FC25 | Tyler Bindon | 1.00 | 68.5 | — |
|  | Nando PIJNAKER | FC25 | Nando Pijnaker | 1.00 | 67.5 | — |
| ✗ | Francis DE VRIES | FC25 | Francis de Vries | 1.00 | 66.0 | — |
| ✗ | Tommy SMITH | FC25 | Tommy Smith | 1.00 | 63.5 | — |
| ✗ | Callan ELLIOT | FC25 | Callan Elliot | 1.00 | 59.0 | — |

#### Midfielders &nbsp;(7/10 used · raw log-mean=66.83 · normalized=0.0000)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Marko STAMENIC | FC25 | Marko Stamenić | 1.00 | 70.0 | — |
|  | Ryan THOMAS | FC25 | Ryan Thomas | 1.00 | 68.5 | — |
|  | Sarpreet SINGH | FIFA22 | S. Singh | 1.00 | 67.5 | — |
|  | Joe BELL | FC25 | Joe Bell | 1.00 | 66.0 | — |
|  | Alex RUFER | FC25 | Alex Rufer | 1.00 | 66.0 | — |
|  | Ben OLD | FC25 | Ben Old | 1.00 | 65.0 | — |
|  | Callum McCOWATT | FC25 | Callum McCowatt | 1.00 | 65.0 | — |
| ✗ | Matthew GARBETT | FC25 | Matthew Garbett | 1.00 | 63.5 | — |
| ✗ | Elijah JUST | FIFA22 | E. Just | 0.79 | 63.5 | — |
| ✗ | Lachlan BAYLISS | FC25 | Lachlan Bayliss | 1.00 | 55.5 | — |

#### Attackers &nbsp;(3/4 used · raw log-mean=74.48 · normalized=0.3137)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Kosta BARBAROUSES | FIFA22 | K. Barbarouses | 1.00 | 77.0 | — |
|  | Jesse RANDALL | median | — | — | 74.0 | — |
|  | Ben WAINE | FC25 | Ben Waine | 1.00 | 72.5 | — |
| ✗ | Chris WOOD | FC25 | Chris Wood | 1.00 | 63.5 | — |

---

### Norway

**xG vs avg opponent:** 2.0995 &nbsp;|&nbsp; GK=0.1799 &nbsp;|&nbsp; DEF=0.1355 &nbsp;|&nbsp; MID=0.3583 &nbsp;|&nbsp; ATT=1.0000

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=66.89 · normalized=0.1799)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Orjan Haskjold Nyland | FIFA22 | Ø. Nyland | 1.00 | 70.8 | — |
|  | Egil Selvik | FIFA22 | E. Selvik | 1.00 | 63.2 | — |
| ✗ | Sander Tangvik | FIFA22 | S. Tangvik | 1.00 | 52.8 | — |

#### Defenders &nbsp;(6/9 used · raw log-mean=71.12 · normalized=0.1355)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Kristoffer Vassbakk Ajer | FIFA22 | K. Ajer | 1.00 | 79.0 | — |
|  | Leo Ostigard | FC25 | Leo Østigård | 1.00 | 75.0 | — |
|  | Fredrik Bjorkan | FIFA22 | F. Bjørkan | 0.83 | 69.5 | — |
|  | Julian Ryerson | FIFA22 | J. Ryerson | 1.00 | 69.5 | — |
|  | Sondre Langas | FC25 | Sondre Langås | 1.00 | 68.0 | — |
|  | Torbjorn Heggem | FC25 | Torbjørn L. Heggem | 0.94 | 66.5 | — |
| ✗ | Marcus Holmgren Pedersen | FIFA22 | M. Pedersen | 1.00 | 61.5 | — |
| ✗ | David Moller Wolfe | FIFA22 | D. Wolfe | 1.00 | 54.0 | — |
| ✗ | Henrik Falchener | FIFA22 | H. Falchener | 0.81 | 45.0 | — |

#### Midfielders &nbsp;(8/11 used · raw log-mean=73.46 · normalized=0.3583)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Martin Odegaard | FIFA22 | M. Ødegaard | 1.00 | 83.5 | — |
|  | Oscar Bobb | FC25 | Oscar Bobb | 1.00 | 75.0 | — |
|  | Jens Petter Hauge | FIFA22 | J. Hauge | 1.00 | 72.5 | — |
|  | Patrick Berg | FIFA22 | P. Berg | 1.00 | 72.0 | — |
|  | Sander Berge | FC25 | Sander Berge | 1.00 | 72.0 | — |
|  | Antonio Nusa | FC25 | Antonio Nusa | 1.00 | 72.0 | — |
|  | Andreas Schjelderup | FC25 | Andreas Schjelderup | 1.00 | 71.0 | — |
|  | Fredrik Aursnes | FIFA22 | F. Aursnes | 1.00 | 70.5 | — |
| ✗ | Kristian Thorstvedt | FIFA22 | K. Thorstvedt | 1.00 | 70.0 | — |
| ✗ | Morten Thorsby | FIFA22 | M. Thorsby | 1.00 | 69.5 | — |
| ✗ | Thelonious Aasgaard | FC25 | Thelo Aasgaard | 0.85 | 65.5 | — |

#### Attackers &nbsp;(2/3 used · raw log-mean=83.25 · normalized=1.0000)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Erling Haaland | FC25 | Erling Haaland | 1.00 | 90.0 | — |
|  | Alexander Sorloth | FIFA22 | A. Sørloth | 1.00 | 77.0 | — |
| ✗ | Jorgen Strand Larsen | FIFA22 | J. Larsen | 1.00 | 64.5 | — |

---

### Panama

**xG vs avg opponent:** 0.8093 &nbsp;|&nbsp; GK=0.3882 &nbsp;|&nbsp; DEF=0.1954 &nbsp;|&nbsp; MID=0.1240 &nbsp;|&nbsp; ATT=0.3915

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=71.88 · normalized=0.3882)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Orlando Mosquera | median | — | — | 71.9 | — |
|  | Cesar Samudio | median | — | — | 71.9 | — |
| ✗ | Luis Mejia | FC25 | Luis Mejía | 1.00 | 69.5 | — |

#### Defenders &nbsp;(7/10 used · raw log-mean=71.89 · normalized=0.1954)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Andres Andrade | FC25 | Andrés Andrade | 1.00 | 75.0 | — |
|  | Cesar Blackman | median | — | — | 71.9 | — |
|  | Jorge Gutierrez | median | — | — | 71.9 | — |
|  | Eric Davis | median | — | — | 71.9 | — |
|  | Fidel Escobar | FIFA22 | F. Escobar | 0.82 | 71.5 | — |
|  | Amir Murillo | FC25 | Amir Murillo | 1.00 | 71.0 | — |
|  | Jiovany Ramos | FC25 | Jiovany Ramos | 1.00 | 70.0 | — |
| ✗ | Jose Cordoba | FC25 | José Córdoba | 1.00 | 67.5 | — |
| ✗ | Edgardo Farina | TM | — | — | 65.0 | 1,000,000 |
| ✗ | Roderick Miller | TM | — | — | 65.0 | 200,000 |

#### Midfielders &nbsp;(6/9 used · raw log-mean=69.13 · normalized=0.1240)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Adalberto Carrasquilla | FC25 | Adalberto Carrasquilla | 1.00 | 72.0 | — |
|  | Cristian Martinez | median | — | — | 70.5 | — |
|  | Azarias Londono | median | — | — | 70.5 | — |
|  | Alberto Quintero | FIFA22 | A. Quintero | 0.77 | 69.5 | — |
|  | Yoel Barcenas | FIFA22 | Y. Bárcenas | 0.87 | 67.5 | — |
|  | Anibal Godoy | FC25 | Aníbal Godoy | 1.00 | 65.0 | — |
| ✗ | Jose Luis Rodriguez | FIFA22 | J. Rodríguez | 0.83 | 63.5 | — |
| ✗ | Cesar Yanis | FIFA22 | C. Yanis | 1.00 | 63.0 | — |
| ✗ | Carlos Harvey | FC25 | Carlos Harvey | 1.00 | 53.0 | — |

#### Attackers &nbsp;(3/4 used · raw log-mean=75.47 · normalized=0.3915)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Ismael Diaz | FC25 | Ismael Díaz | 1.00 | 78.5 | — |
|  | Cecilio Waterman | median | — | — | 74.0 | — |
|  | Tomas Rodriguez | median | — | — | 74.0 | — |
| ✗ | Jose Fajardo | FC25 | José Fajardo | 1.00 | 68.5 | — |

---

### Paraguay

**xG vs avg opponent:** 0.3915 &nbsp;|&nbsp; GK=0.3882 &nbsp;|&nbsp; DEF=0.2637 &nbsp;|&nbsp; MID=0.1109 &nbsp;|&nbsp; ATT=0.1676

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=71.88 · normalized=0.3882)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Orlando Gill | median | — | — | 71.9 | — |
|  | Roberto Fernández | median | — | — | 71.9 | — |
|  | Gastón Olveira | median | — | — | 71.9 | — |

#### Defenders &nbsp;(6/8 used · raw log-mean=72.77 · normalized=0.2637)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Omar Alderete | FC25 | Omar Alderete | 1.00 | 78.0 | — |
|  | Gustavo Gómez | TM | — | — | 75.7 | 8,500,000 |
|  | Gustavo Velázquez | FC25 | Gustavo Velázquez | 1.00 | 75.0 | — |
|  | Alexandro Maidana | median | — | — | 71.9 | — |
|  | José Canale | FIFA22 | J. Canale | 0.84 | 69.5 | — |
|  | Fabián Balbuena | TM | — | — | 67.0 | 1,500,000 |
| ✗ | Junior Alonso | FC25 | Wildo Alonso | 0.72 | 59.0 | — |
| ✗ | Juan Cáceres | FIFA22 | A. Cáceres | 0.86 | 49.0 | — |

#### Midfielders &nbsp;(5/7 used · raw log-mean=68.89 · normalized=0.1109)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mauricio Magalhães | median | — | — | 70.5 | — |
|  | Damián Bobadilla | median | — | — | 70.5 | — |
|  | Andrés Cubas | FC25 | Andrés Cubas | 1.00 | 68.5 | — |
|  | Braian Ojeda | FC25 | Braian Ojeda | 1.00 | 68.0 | — |
|  | Diego Gómez | FC25 | Diego Gómez | 1.00 | 67.0 | — |
| ✗ | Matías Galarza | FC25 | Matías Galarza | 1.00 | 62.5 | — |
| ✗ | Alejandro Gamarra | FIFA22 | M. Gamarra | 0.73 | 47.0 | — |

#### Attackers &nbsp;(6/8 used · raw log-mean=72.61 · normalized=0.1676)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Miguel Almirón | FC25 | Miguel Almirón | 1.00 | 81.0 | — |
|  | Antonio Sanabria | FC25 | Antonio Sanabria | 1.00 | 75.0 | — |
|  | Ramón Sosa | FC25 | Ramón Sosa | 1.00 | 74.0 | — |
|  | Gabriel Ávalos | FC25 | Gabriel Ávalos | 1.00 | 70.5 | — |
|  | Alex Arce | FC25 | Alex Arce | 1.00 | 68.0 | — |
|  | Isidro Pitta | FIFA22 | I. Pitta | 0.74 | 68.0 | — |
| ✗ | Gustavo Caballero | FC25 | Gustavo Caballero | 1.00 | 65.0 | — |
| ✗ | Julio Enciso | FIFA22 | J. Enciso | 0.80 | 61.5 | — |

---

### Portugal

**xG vs avg opponent:** 2.2962 &nbsp;|&nbsp; GK=0.7520 &nbsp;|&nbsp; DEF=0.7605 &nbsp;|&nbsp; MID=1.0000 &nbsp;|&nbsp; ATT=0.8331

#### Goalkeepers &nbsp;(3/4 used · raw log-mean=80.57 · normalized=0.7520)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Diogo Costa | FC25 | Diogo Costa | 1.00 | 82.5 | — |
|  | Rui Silva | FC25 | Rui Silva | 1.00 | 80.8 | — |
|  | Jose Sa | FC25 | José Sá | 1.00 | 78.5 | — |
| ✗ | Ricardo Velho | FC25 | Ricardo Velho | 1.00 | 73.2 | — |

#### Defenders &nbsp;(6/9 used · raw log-mean=79.14 · normalized=0.7605)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Ruben Dias | FC25 | Rúben Dias | 1.00 | 88.0 | — |
|  | Goncalo Inacio | FC25 | Gonçalo Inácio | 1.00 | 80.0 | — |
|  | Diogo Dalot | FC25 | Diogo Dalot | 1.00 | 79.0 | — |
|  | Nuno Mendes | FC25 | Nuno Mendes | 1.00 | 77.0 | — |
|  | Joao Cancelo | FC25 | João Cancelo | 1.00 | 76.0 | — |
|  | Tomas Araujo | FC25 | Tomás Araújo | 1.00 | 75.5 | — |
| ✗ | Matheus Nunes | FC25 | Matheus Nunes | 1.00 | 74.5 | — |
| ✗ | Nelson Semedo | FC25 | Nélson Semedo | 1.00 | 73.5 | — |
| ✗ | Renato Veiga | FC25 | Renato Veiga | 1.00 | 71.0 | — |

#### Midfielders &nbsp;(4/6 used · raw log-mean=85.33 · normalized=1.0000)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Bernardo Silva | FC25 | Bernardo Silva | 1.00 | 89.0 | — |
|  | Bruno Fernandes | FC25 | Bruno Fernandes | 1.00 | 85.5 | — |
|  | Vitinha | FC25 | Vitinha | 1.00 | 85.5 | — |
|  | Ruben Neves | FC25 | Rúben Neves | 1.00 | 81.5 | — |
| ✗ | Joao Neves | FC25 | João Neves | 1.00 | 77.5 | — |
| ✗ | Samuel Costa | FC25 | Samú Costa | 0.91 | 67.5 | — |

#### Attackers &nbsp;(6/8 used · raw log-mean=81.11 · normalized=0.8331)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Rafael Leao | FC25 | Rafael Leão | 1.00 | 86.5 | — |
|  | Cristiano Ronaldo | FC25 | Cristiano Ronaldo | 1.00 | 82.5 | — |
|  | Goncalo Guedes | FC25 | Gonçalo Guedes | 1.00 | 81.0 | — |
|  | Pedro Neto | FC25 | Pedro Neto | 1.00 | 81.0 | — |
|  | Joao Felix | FC25 | João Félix | 1.00 | 79.0 | — |
|  | Francisco Conceicao | FC25 | Francisco Conceição | 1.00 | 77.0 | — |
| ✗ | Goncalo Ramos | FC25 | Gonçalo Ramos | 1.00 | 76.5 | — |
| ✗ | Francisco Trincao | FC25 | Francisco Ramos | 0.81 | 60.5 | — |

---

### Qatar

**xG vs avg opponent:** 0.6576 &nbsp;|&nbsp; GK=0.3882 &nbsp;|&nbsp; DEF=0.1994 &nbsp;|&nbsp; MID=0.1981 &nbsp;|&nbsp; ATT=0.2764

#### Goalkeepers &nbsp;(3/4 used · raw log-mean=71.88 · normalized=0.3882)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Mahmoud Abunada | median | — | — | 71.9 | — |
|  | Shehab Al Lithi | median | — | — | 71.9 | — |
|  | Meshaal Barsham | median | — | — | 71.9 | — |
|  | Salah Zakaria | median | — | — | 71.9 | — |

#### Defenders &nbsp;(8/11 used · raw log-mean=71.94 · normalized=0.1994)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Ryan Al Ali | median | — | — | 71.9 | — |
|  | Al Hashemi Al Hussein | median | — | — | 71.9 | — |
|  | Ayub Al Alawi | median | — | — | 71.9 | — |
|  | Bassam Al Rawi | median | — | — | 71.9 | — |
|  | Sultan Al Brake | median | — | — | 71.9 | — |
|  | Boualem Khoukhi | median | — | — | 71.9 | — |
|  | Pedro Miguel | median | — | — | 71.9 | — |
|  | Tarek Salman | median | — | — | 71.9 | — |
| ✗ | Hommam Al Amin | TM | — | — | 65.0 | 500,000 |
| ✗ | Niall Mason | TM | — | — | 65.0 | 150,000 |
| ✗ | Lucas Mendes | TM | — | — | 65.0 | 500,000 |

#### Midfielders &nbsp;(6/9 used · raw log-mean=70.50 · normalized=0.1981)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Karim Boudiaf | median | — | — | 70.5 | — |
| ✗ | Ahmed Fathi | median | — | — | 70.5 | — |
|  | Jassem Gaber | median | — | — | 70.5 | — |
|  | Abdulaziz Hatem | median | — | — | 70.5 | — |
|  | Issa Lay | median | — | — | 70.5 | — |
|  | Mohammed Manaai | median | — | — | 70.5 | — |
|  | Tahsin Mohammed | median | — | — | 70.5 | — |
|  | Mohammed Waad | median | — | — | 70.5 | — |
| ✗ | Assim Madibo | TM | — | — | 65.0 | 300,000 |

#### Attackers &nbsp;(7/10 used · raw log-mean=74.00 · normalized=0.2764)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Youssef Abdelrisaq | median | — | — | 74.0 | — |
|  | Ahmed Alaaeldin | median | — | — | 74.0 | — |
|  | Hassan Al Haydos | median | — | — | 74.0 | — |
|  | Almoez Ali | median | — | — | 74.0 | — |
|  | Ahmed Al Janhi | median | — | — | 74.0 | — |
|  | Mohammed Muntari | median | — | — | 74.0 | — |
|  | Mubarak Shannan | median | — | — | 74.0 | — |
|  | Sebastián Soria | median | — | — | 74.0 | — |
| ✗ | Akram Afif | TM | — | — | 72.5 | 4,500,000 |
| ✗ | Edmilson Júnior | TM | — | — | 70.5 | 3,000,000 |

---

### South Korea

**xG vs avg opponent:** 1.7552 &nbsp;|&nbsp; GK=0.4503 &nbsp;|&nbsp; DEF=0.1561 &nbsp;|&nbsp; MID=0.3750 &nbsp;|&nbsp; ATT=0.8037

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=73.36 · normalized=0.4503)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Jo Hyeonwoo | FC25 | Jo Hyeon Woo | 0.96 | 75.0 | — |
|  | Kim Seung-gyu | FC25 | Kim Seung Gyu | 1.00 | 71.8 | — |
| ✗ | Song Bumkeun | FIFA22 | Song Bum Keun | 0.96 | 66.8 | — |

#### Defenders &nbsp;(7/10 used · raw log-mean=71.39 · normalized=0.1561)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Kim Minjae | FC25 | Kim Min Jae | 0.95 | 84.0 | — |
|  | Park Jinseob | FC25 | Park Jin Seob | 0.96 | 77.0 | — |
|  | Lee Hanbeom | FC25 | Lee Han Beom | 0.96 | 71.0 | — |
|  | Lee Kihyuk | FC25 | Lee Gi Hyeok | 0.73 | 70.0 | — |
|  | Cho Yumin | FIFA22 | Cho Yu Min | 0.95 | 68.5 | — |
|  | Jens Castrop | TM | — | — | 67.0 | 1,500,000 |
|  | Kim Moonhwan | FC25 | Kim Moon Hwan | 0.96 | 64.0 | — |
| ✗ | Lee Taeseok | FC25 | Lee Tae Suk | 0.82 | 63.5 | — |
| ✗ | Kim Taehyeon | FIFA22 | Kim Tae Hyeon | 0.96 | 59.5 | — |
| ✗ | Seol Youngwoo | FIFA22 | Seol Young Woo | 0.96 | 59.5 | — |

#### Midfielders &nbsp;(7/10 used · raw log-mean=73.77 · normalized=0.3750)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Lee Kangin | FC25 | Lee Kang In | 0.95 | 81.0 | — |
|  | Lee Jaesung | FC25 | Lee Jae Sung | 0.96 | 76.5 | — |
|  | Hwang Heechan | FC25 | Hwang Hee Chan | 0.96 | 74.0 | — |
|  | Lee Donggyeong | FC25 | Lee Dong Kyeong | 0.90 | 73.5 | — |
|  | Paik Seungho | FC25 | Paik Seung Ho | 0.96 | 71.5 | — |
|  | Bae Junho | FC25 | Bae Jun Ho | 0.95 | 70.5 | — |
|  | Yang Hyunjun | FC25 | Yang Hyun Jun | 0.96 | 70.0 | — |
| ✗ | Eom Jisung | FC25 | Eom Ji Sung | 0.95 | 69.0 | — |
| ✗ | Kim Jingyu | FC25 | Kim Jin Kyu | 0.86 | 68.5 | — |
| ✗ | Hwang Inbeom | FIFA22 | An Jin Beom | 0.78 | 60.5 | — |

#### Attackers &nbsp;(2/3 used · raw log-mean=80.74 · normalized=0.8037)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Son Heungmin | FIFA22 | H. Son | 1.00 | 87.5 | — |
|  | Cho Guesung | FC25 | Cho Gue Sung | 0.96 | 74.5 | — |
| ✗ | Oh Hyeongyu | FC25 | Oh Hyeon Gyu | 0.96 | 72.0 | — |

---

### Saudi Arabia

**xG vs avg opponent:** 0.6345 &nbsp;|&nbsp; GK=0.1783 &nbsp;|&nbsp; DEF=0.0969 &nbsp;|&nbsp; MID=0.0043 &nbsp;|&nbsp; ATT=0.3468

#### Goalkeepers &nbsp;(3/4 used · raw log-mean=66.86 · normalized=0.1783)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mohammed Al Owais | FIFA22 | M. Al Owais | 1.00 | 70.0 | — |
|  | Nawaf Al Aqidi | FC25 | Nawaf Al Aqidi | 1.00 | 67.5 | — |
|  | Ahmed Al Kassar | FC25 | Ahmed Al Kassar | 1.00 | 63.2 | — |
| ✗ | Abdulqudus Attia | FC25 | Abdulquddus Attiah | 0.94 | 60.8 | — |

#### Defenders &nbsp;(8/12 used · raw log-mean=70.62 · normalized=0.0969)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Saud Abdulhamid | FC25 | Saud Abdulhamid | 1.00 | 74.0 | — |
|  | Abdulelah Al Amri | FC25 | Abdulelah Al Amri | 1.00 | 74.0 | — |
|  | Hassan Tambakti | FC25 | Hassan Tombakti | 0.93 | 74.0 | — |
|  | Hassan Kadesh | FC25 | Hassan Kadish | 0.92 | 72.5 | — |
|  | Jehad Thikri | median | — | — | 71.9 | — |
|  | Ali Lajami | FC25 | Ali Lajami | 1.00 | 71.5 | — |
|  | Nawaf Boushal | FIFA22 | N. Boushal | 1.00 | 64.5 | — |
|  | Ali Majrashi | FIFA22 | A. Majrashi | 1.00 | 63.5 | — |
| ✗ | Zakaria Hawsawi | FC25 | Zakaria Hawsawi | 1.00 | 59.0 | — |
| ✗ | Mohammed Abu Al Shamat | FC25 | Mohammed Abdulrahman | 0.76 | 56.5 | — |
| ✗ | Moteb Al Harbi | FIFA22 | M. Al Harbi | 0.93 | 52.0 | — |
| ✗ | Khalid Al Ghannam | FC25 | Khalid Al Ghannam | 1.00 | 36.5 | — |

#### Midfielders &nbsp;(6/9 used · raw log-mean=66.91 · normalized=0.0043)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mohammed Kanno | FC25 | Mohammed Kanno | 1.00 | 71.5 | — |
|  | Saleh Abu Al Shamat | median | — | — | 70.5 | — |
|  | Nasser Al Dawsari | FC25 | Nasser Al Dawsari | 1.00 | 68.5 | — |
|  | Abdullah Al Khaibari | FC25 | Abdullah Al Khaibari | 1.00 | 65.5 | — |
|  | Sultan Mandash | FC25 | Sultan Mandash | 1.00 | 63.5 | — |
|  | Alaa Al Hajji | FC25 | Alaa Al Hajji | 1.00 | 62.5 | — |
| ✗ | Ayman Yahya | FC25 | Ayman Yahya | 1.00 | 62.0 | — |
| ✗ | Ziyad Al Johani | FIFA22 | Z. Al Johani | 1.00 | 54.5 | — |
| ✗ | Musab Al Juwayr | FIFA22 | M. Al Juwair | 0.93 | 51.0 | — |

#### Attackers &nbsp;(3/5 used · raw log-mean=74.90 · normalized=0.3468)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Salem Al Dawsari | FC25 | Salem Al Dawsari | 1.00 | 80.0 | — |
|  | Feras Al Brikan | FC25 | Firas Al Birekan | 0.84 | 74.5 | — |
|  | Abdullah Al Hamdan | FIFA22 | A. Al Hamdan | 1.00 | 70.5 | — |
| ✗ | Saleh Al Shehri | FC25 | Saleh Al Shehri | 1.00 | 65.5 | — |
| ✗ | Abdullah Al Salem | FIFA22 | A. Al Salem | 1.00 | 62.0 | — |

---

### Scotland

**xG vs avg opponent:** 0.8118 &nbsp;|&nbsp; GK=0.3824 &nbsp;|&nbsp; DEF=0.3654 &nbsp;|&nbsp; MID=0.3903 &nbsp;|&nbsp; ATT=0.2788

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=71.73 · normalized=0.3824)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Angus Gunn | FC25 | Angus Gunn | 1.00 | 73.2 | — |
|  | Craig Gordon | FC25 | Craig Gordon | 1.00 | 70.2 | — |
| ✗ | Liam Kelly | TM | — | — | 65.0 | 200,000 |

#### Defenders &nbsp;(7/10 used · raw log-mean=74.07 · normalized=0.3654)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Andy Robertson | FIFA22 | A. Robertson | 0.88 | 79.0 | — |
|  | Kieran Tierney | FIFA22 | K. Tierney | 1.00 | 77.0 | — |
|  | Scott McKenna | FIFA22 | S. McKenna | 1.00 | 75.5 | — |
|  | Grant Hanley | FIFA22 | G. Hanley | 1.00 | 75.0 | — |
|  | Jack Hendry | FIFA22 | J. Hendry | 1.00 | 72.5 | — |
|  | Dom Hyam | FIFA22 | D. Hyam | 0.86 | 71.0 | — |
|  | John Souttar | FIFA22 | J. Souttar | 1.00 | 69.0 | — |
| ✗ | Nathan Patterson | FIFA22 | N. Patterson | 1.00 | 65.5 | — |
| ✗ | Anthony Ralston | FIFA22 | A. Ralston | 1.00 | 64.0 | — |
| ✗ | Aaron Hickey | FIFA22 | A. Hickey | 1.00 | 61.0 | — |

#### Midfielders &nbsp;(6/8 used · raw log-mean=74.06 · normalized=0.3903)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Ben Gannon-Doak | TM | — | — | 76.5 | 10,000,000 |
|  | John McGinn | FIFA22 | J. McGinn | 1.00 | 76.5 | — |
|  | Scott McTominay | FIFA22 | S. McTominay | 1.00 | 75.0 | — |
|  | Ryan Christie | FIFA22 | R. Christie | 1.00 | 74.0 | — |
|  | Billy Gilmour | FIFA22 | B. Gilmour | 1.00 | 71.5 | — |
|  | Kenny McLean | FIFA22 | K. McLean | 1.00 | 71.0 | — |
| ✗ | Lewis Ferguson | FIFA22 | L. Ferguson | 1.00 | 69.5 | — |
| ✗ | Findlay Curtis | TM | — | — | 65.0 | 750,000 |

#### Attackers &nbsp;(3/5 used · raw log-mean=74.03 · normalized=0.2788)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Che Adams | FIFA22 | C. Adams | 1.00 | 80.5 | — |
|  | Ross Stewart | FC25 | Ross Stewart | 1.00 | 72.0 | — |
|  | Lawrence Shankland | FIFA22 | L. Shankland | 1.00 | 70.0 | — |
| ✗ | Lyndon Dykes | FC25 | Lyndon Dykes | 1.00 | 67.0 | — |
| ✗ | George Hirst | FC25 | George Byers | 0.75 | 59.5 | — |

---

### Senegal

**xG vs avg opponent:** 1.5545 &nbsp;|&nbsp; GK=0.6812 &nbsp;|&nbsp; DEF=0.4752 &nbsp;|&nbsp; MID=0.2782 &nbsp;|&nbsp; ATT=0.7349

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=78.88 · normalized=0.6812)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Edouard Mendy | FIFA22 | É. Mendy | 1.00 | 82.5 | — |
|  | Yehvann Diouf | TM | — | — | 75.4 | 8,000,000 |
| ✗ | Mory Diaw | FC25 | Mory Diaw | 1.00 | 75.2 | — |

#### Defenders &nbsp;(7/10 used · raw log-mean=75.48 · normalized=0.4752)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Kalidou Koulibaly | FIFA22 | K. Koulibaly | 1.00 | 86.0 | — |
|  | Mamadou Sarr | TM | — | — | 81.1 | 25,000,000 |
|  | Abdoulaye Seck | FIFA22 | A. Seck | 1.00 | 78.0 | — |
|  | Moussa Niakhate | FC25 | Moussa Niakhaté | 1.00 | 76.0 | — |
|  | Antoine Mendy | TM | — | — | 71.9 | 4,000,000 |
|  | El Hadji Malick Diouf | FC25 | El Hadji Malick Diouf | 1.00 | 69.0 | — |
|  | Ismail Jakobs | FC25 | Ismail Jakobs | 1.00 | 68.0 | — |
| ✗ | Moustapha Mbow | FIFA22 | M. Mbow | 1.00 | 62.0 | — |
| ✗ | Ilay Camara | FC25 | Lamine Camara | 0.75 | 58.0 | — |
| ✗ | Krepin Diatta | FIFA22 | K. Diatta | 1.00 | 58.0 | — |

#### Midfielders &nbsp;(5/7 used · raw log-mean=71.98 · normalized=0.2782)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Idrissa Gana Gueye | FIFA22 | I. Gueye | 1.00 | 74.5 | — |
|  | Lamine Camara | FC25 | Lamine Camara | 1.00 | 73.5 | — |
|  | Habib Diarra | FC25 | Habib Diarra | 1.00 | 71.0 | — |
|  | Pape Gueye | FC25 | Pape Gueye | 1.00 | 70.5 | — |
|  | Bara Sapoko Ndiaye | median | — | — | 70.5 | — |
| ✗ | Pape Matar Sarr | FIFA22 | P. Sarr | 1.00 | 69.5 | — |
| ✗ | Pathe Ciss | FC25 | Pathé Ciss | 1.00 | 62.0 | — |

#### Attackers &nbsp;(6/8 used · raw log-mean=79.86 · normalized=0.7349)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Sadio Mane | FIFA22 | S. Mané | 1.00 | 87.0 | — |
|  | Ismaila Sarr | FIFA22 | I. Sarr | 1.00 | 85.0 | — |
|  | Nicolas Jackson | FC25 | Nicolas Jackson | 1.00 | 80.5 | — |
|  | Iliman Ndiaye | FC25 | Iliman Ndiaye | 1.00 | 78.0 | — |
|  | Bamba Dieng | FC25 | Bamba Dieng | 1.00 | 76.0 | — |
|  | Assane Diao | FIFA22 | A. Ndao | 0.83 | 73.5 | — |
| ✗ | Cherif Ndiaye | FIFA22 | C. Ndiaye | 0.84 | 71.5 | — |
| ✗ | Ibrahim Mbaye | FIFA22 | I. Mbaye | 0.93 | 58.5 | — |

---

### South Africa

**xG vs avg opponent:** 0.6929 &nbsp;|&nbsp; GK=0.3882 &nbsp;|&nbsp; DEF=0.1994 &nbsp;|&nbsp; MID=0.1981 &nbsp;|&nbsp; ATT=0.2958

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=71.88 · normalized=0.3882)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Ronwen Williams | median | — | — | 71.9 | — |
|  | Ricardo Goss | median | — | — | 71.9 | — |
|  | Sipho Chaine | median | — | — | 71.9 | — |

#### Defenders &nbsp;(8/11 used · raw log-mean=71.94 · normalized=0.1994)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Khuliso Mudau | median | — | — | 71.9 | — |
| ✗ | Bradley Cross | median | — | — | 71.9 | — |
|  | Thabang Matuludi | median | — | — | 71.9 | — |
|  | Nkosinathi Sibisi | median | — | — | 71.9 | — |
|  | Aubrey Modiba | median | — | — | 71.9 | — |
|  | Khulumani Ndamane | median | — | — | 71.9 | — |
|  | Ime Okon | median | — | — | 71.9 | — |
|  | Samukele Kabini | median | — | — | 71.9 | — |
|  | Kamogelo Sebelebele | median | — | — | 71.9 | — |
|  | Mbekezeli Mbokazi | median | — | — | 71.9 | — |
| ✗ | Olwethu Makhanya | FC25 | Olwethu Makhanya | 1.00 | 52.0 | — |

#### Midfielders &nbsp;(3/4 used · raw log-mean=70.50 · normalized=0.1981)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Teboho Mokoena | median | — | — | 70.5 | — |
|  | Jayden Adams | median | — | — | 70.5 | — |
|  | Thalente Mbatha | median | — | — | 70.5 | — |
| ✗ | Sphephelo Sithole | FC25 | Sphephelo Sithole | 1.00 | 61.5 | — |

#### Attackers &nbsp;(6/8 used · raw log-mean=74.25 · normalized=0.2958)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Lyle Foster | FC25 | Lyle Foster | 1.00 | 75.5 | — |
| ✗ | Oswin Appollis | median | — | — | 74.0 | — |
| ✗ | Tshepang Moremi | median | — | — | 74.0 | — |
|  | Evidence Makgopa | median | — | — | 74.0 | — |
|  | Iqraam Rayners | median | — | — | 74.0 | — |
|  | Relebohile Mofokeng | median | — | — | 74.0 | — |
|  | Themba Zwane | median | — | — | 74.0 | — |
|  | Thapelo Maseko | median | — | — | 74.0 | — |

---

### Spain

**xG vs avg opponent:** 1.8915 &nbsp;|&nbsp; GK=0.8481 &nbsp;|&nbsp; DEF=0.6257 &nbsp;|&nbsp; MID=0.8509 &nbsp;|&nbsp; ATT=0.6746

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=82.86 · normalized=0.8481)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Unai SIMON | FC25 | Unai Simón | 1.00 | 84.2 | — |
|  | David RAYA | FC25 | David Raya | 1.00 | 81.5 | — |
| ✗ | Joan GARCIA | FC25 | Joan García | 1.00 | 75.2 | — |

#### Defenders &nbsp;(6/8 used · raw log-mean=77.41 · normalized=0.6257)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Aymeric LAPORTE | FIFA22 | A. Laporte | 1.00 | 83.0 | — |
|  | Marcos LLORENTE | FC25 | Marcos Llorente | 1.00 | 80.0 | — |
|  | Pedro PORRO | FC25 | Pedro Porro | 1.00 | 77.5 | — |
|  | Marc CUCURELLA | FC25 | Marc Cucurella | 1.00 | 77.0 | — |
|  | Eric GARCIA | FC25 | Eric García | 1.00 | 75.5 | — |
|  | Marc PUBILL | TM | — | — | 71.9 | 4,000,000 |
| ✗ | Pau CUBARSI | FC25 | Pau Cubarsí | 1.00 | 68.5 | — |
| ✗ | Alex GRIMALDO | TM | — | — | 65.0 | 100,000 |

#### Midfielders &nbsp;(5/7 used · raw log-mean=82.58 · normalized=0.8509)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | RODRI | FC25 | Rodri | 1.00 | 85.0 | — |
|  | PEDRI | FC25 | Pedri | 1.00 | 85.0 | — |
|  | Mikel MERINO | FIFA22 | Merino | 1.00 | 81.5 | — |
|  | GAVI | FC25 | Gavi | 1.00 | 81.5 | — |
|  | Fabian RUIZ | FC25 | Fabián Ruiz | 1.00 | 80.0 | — |
| ✗ | Alex BAENA | FC25 | Álex Baena | 1.00 | 79.0 | — |
| ✗ | Martin ZUBIMENDI | FIFA22 | Zubimendi | 0.82 | 71.0 | — |

#### Attackers &nbsp;(6/8 used · raw log-mean=79.09 · normalized=0.6746)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Nico WILLIAMS | FC25 | Nico Williams | 1.00 | 84.0 | — |
|  | Mikel OYARZABAL | FIFA22 | Oyarzabal | 0.81 | 82.0 | — |
|  | Ferran TORRES | FC25 | Ferran Torres | 1.00 | 81.0 | — |
|  | Lamine YAMAL | FC25 | Lamine Yamal | 1.00 | 78.5 | — |
|  | Dani OLMO | FC25 | Dani Olmo | 1.00 | 75.0 | — |
|  | Yeremy PINO | FC25 | Yeremy Pino | 1.00 | 74.5 | — |
| ✗ | Victor MUNOZ | median | — | — | 74.0 | — |
| ✗ | Borja IGLESIAS | FC25 | Borja Iglesias | 1.00 | 71.0 | — |

---

### Sweden

**xG vs avg opponent:** 1.4272 &nbsp;|&nbsp; GK=0.3486 &nbsp;|&nbsp; DEF=0.4000 &nbsp;|&nbsp; MID=0.1215 &nbsp;|&nbsp; ATT=0.7321

#### Goalkeepers &nbsp;(3/4 used · raw log-mean=70.93 · normalized=0.3486)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Viktor Johansson | FC25 | Viktor Johansson | 1.00 | 74.0 | — |
|  | Gustaf Lagerbielke | TM | — | — | 73.1 | 5,000,000 |
|  | Kristoffer Nordfeldt | FC25 | Kristoffer Nordfeldt | 1.00 | 66.0 | — |
| ✗ | Jacob Zetterström | FIFA22 | J. Zetterström | 0.87 | 58.2 | — |

#### Defenders &nbsp;(5/7 used · raw log-mean=74.51 · normalized=0.4000)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Isak Hien | FC25 | Isak Hien | 1.00 | 78.0 | — |
|  | Victor Lindelöf | FC25 | Victor Lindelöf | 1.00 | 77.0 | — |
|  | Eric Smith | FC25 | Eric Smith | 1.00 | 75.0 | — |
|  | Carl Starfelt | FC25 | Carl Starfelt | 1.00 | 75.0 | — |
|  | Gabriel Gudmundsson | FIFA22 | G. Gudmundsson | 1.00 | 68.0 | — |
| ✗ | Hjalmar Ekdal | FIFA22 | H. Ekdal | 1.00 | 65.0 | — |
| ✗ | Daniel Svensson | FIFA22 | D. Svensson | 1.00 | 54.0 | — |

#### Midfielders &nbsp;(6/8 used · raw log-mean=69.08 · normalized=0.1215)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mattias Svanberg | FC25 | Mattias Svanberg | 1.00 | 76.0 | — |
|  | Lucas Bergvall | FC25 | Lucas Bergvall | 1.00 | 70.0 | — |
|  | Ken Sema | FC25 | Ken Sema | 1.00 | 69.5 | — |
|  | Yasin Ayari | FC25 | Yasin Ayari | 1.00 | 67.5 | — |
|  | Benjamin Nygren | FC25 | Benjamin Nygren | 1.00 | 67.0 | — |
|  | Jesper Karlström | FIFA22 | J. Karlström | 1.00 | 65.0 | — |
| ✗ | Elliot Stroud | FC25 | Elliot Stroud | 1.00 | 63.0 | — |
| ✗ | Besfort Zeneli | FC25 | Besfort Zeneli | 1.00 | 57.5 | — |

#### Attackers &nbsp;(4/6 used · raw log-mean=79.82 · normalized=0.7321)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Viktor Gyökeres | FC25 | Viktor Gyökeres | 1.00 | 86.5 | — |
|  | Alexander Isak | FIFA22 | A. Isak | 1.00 | 83.0 | — |
|  | Anthony Elanga | FC25 | Anthony Elanga | 1.00 | 78.0 | — |
|  | Gustaf Nilsson | FC25 | Gustaf Nilsson | 1.00 | 72.5 | — |
| ✗ | Taha Ali | FC25 | Taha Ayari | 0.78 | 64.5 | — |
| ✗ | Alexander Bernhardsson | FIFA22 | A. Bernhardsson | 1.00 | 64.0 | — |

---

### Switzerland

**xG vs avg opponent:** 1.2049 &nbsp;|&nbsp; GK=0.6391 &nbsp;|&nbsp; DEF=0.5883 &nbsp;|&nbsp; MID=0.4178 &nbsp;|&nbsp; ATT=0.4830

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=77.87 · normalized=0.6391)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Gregor Kobel | FIFA22 | G. Kobel | 1.00 | 78.8 | — |
|  | Yvon Mvogo | FC25 | Yvon Mvogo | 1.00 | 77.0 | — |
| ✗ | Marvin Keller | FC25 | Marvin Keller | 1.00 | 70.5 | — |

#### Defenders &nbsp;(6/8 used · raw log-mean=76.93 · normalized=0.5883)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Manuel Akanji | FC25 | Manuel Akanji | 1.00 | 83.5 | — |
|  | Nico Elvedi | FIFA22 | N. Elvedi | 1.00 | 78.5 | — |
|  | Ricardo Rodríguez | FC25 | Ricardo Rodríguez | 1.00 | 76.5 | — |
|  | Eray Cömert | FC25 | Eray Cömert | 1.00 | 75.0 | — |
|  | Aurèle Amenda | FC25 | Aurèle Amenda | 1.00 | 74.5 | — |
|  | Silvan Widmer | FC25 | Silvan Widmer | 1.00 | 74.0 | — |
| ✗ | Miro Muheim | FC25 | Miro Muheim | 1.00 | 70.0 | — |
| ✗ | Luca Jaquez | FC25 | Luca Jaquez | 1.00 | 69.0 | — |

#### Midfielders &nbsp;(6/9 used · raw log-mean=74.56 · normalized=0.4178)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Djibril Sow | FIFA22 | D. Sow | 1.00 | 76.5 | — |
|  | Remo Freuler | FC25 | Remo Freuler | 1.00 | 76.5 | — |
|  | Michel Aebischer | FIFA22 | M. Aebischer | 1.00 | 75.0 | — |
|  | Granit Xhaka | FIFA22 | G. Xhaka | 1.00 | 74.0 | — |
|  | Denis Zakaria | FC25 | Denis Zakaria | 1.00 | 74.0 | — |
|  | Christian Fassnacht | FIFA22 | C. Fassnacht | 1.00 | 71.5 | — |
| ✗ | Fabian Rieder | FIFA22 | F. Rieder | 1.00 | 66.5 | — |
| ✗ | Cedric Itten | FC25 | Cedric Itten | 1.00 | 64.5 | — |
| ✗ | Ardon Jashari | FIFA22 | A. Jashari | 1.00 | 57.5 | — |

#### Attackers &nbsp;(4/6 used · raw log-mean=76.64 · normalized=0.4830)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Noah Okafor | FC25 | Noah Okafor | 1.00 | 82.5 | — |
|  | Breel Embolo | FC25 | Breel Embolo | 1.00 | 77.5 | — |
|  | Rubén Vargas | FC25 | Ruben Vargas | 1.00 | 76.0 | — |
|  | Dan Ndoye | FIFA22 | D. Ndoye | 1.00 | 71.0 | — |
| ✗ | Zeki Amdouni | FIFA22 | Z. Amdouni | 1.00 | 67.5 | — |
| ✗ | Johan Manzambi | FC25 | Johan Manzambi | 1.00 | 57.0 | — |

---

### Tunisia

**xG vs avg opponent:** 0.7071 &nbsp;|&nbsp; GK=0.3882 &nbsp;|&nbsp; DEF=0.1467 &nbsp;|&nbsp; MID=0.1893 &nbsp;|&nbsp; ATT=0.3074

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=71.88 · normalized=0.3882)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Aymen Dahmen | median | — | — | 71.9 | — |
|  | Sabri Ben Hassen | median | — | — | 71.9 | — |
|  | Abdelmouhib Chamakh | median | — | — | 71.9 | — |

#### Defenders &nbsp;(6/9 used · raw log-mean=71.26 · normalized=0.1467)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Montassar Talbi | FC25 | Montassar Talbi | 1.00 | 74.5 | — |
|  | Dylan Bronn | FC25 | Dylan Bronn | 1.00 | 72.5 | — |
|  | Moutaz Neffati | median | — | — | 71.9 | — |
|  | Adem Arous | median | — | — | 71.9 | — |
|  | Yan Valéry | FC25 | Yan Valery | 1.00 | 71.0 | — |
|  | Ali Abdi | FIFA22 | A. Abdi | 1.00 | 66.0 | — |
| ✗ | Omar Rekik | FC25 | Omar Rekik | 1.00 | 65.5 | — |
| ✗ | Raed Chikhaoui | TM | — | — | 65.0 | 1,000,000 |
| ✗ | Mohamed Ben Hmida | TM | — | — | 65.0 | 100,000 |

#### Midfielders &nbsp;(5/7 used · raw log-mean=70.34 · normalized=0.1893)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Ismaël Gharbi | TM | — | — | 74.7 | 7,000,000 |
|  | Ellyes Skhiri | FC25 | Ellyes Skhiri | 1.00 | 74.5 | — |
|  | Hannbial | FC25 | Hannibal | 0.88 | 70.0 | — |
|  | Rani Khedira | TM | — | — | 68.5 | 2,000,000 |
|  | Anis Ben Slimane | FIFA22 | A. Slimane | 1.00 | 64.5 | — |
| ✗ | Mohamed Hadj-Mahmoud | FC25 | Mohamed Belhadj Mahmoud | 0.93 | 64.0 | — |
| ✗ | Mortadha Ben Ouanes | FIFA22 | M. Ben Ouanes | 1.00 | 55.5 | — |

#### Attackers &nbsp;(5/7 used · raw log-mean=74.40 · normalized=0.3074)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Elias Achouri | FC25 | Elias Achouri | 1.00 | 76.0 | — |
|  | Khalil Ayari | median | — | — | 74.0 | — |
|  | Hazem Mastouri | median | — | — | 74.0 | — |
|  | Firas Chawat | median | — | — | 74.0 | — |
|  | Rayan Elloumi | median | — | — | 74.0 | — |
| ✗ | Elias Saäd | FC25 | Elias Saad | 1.00 | 69.5 | — |
| ✗ | Sebastian Tounekti | FIFA22 | S. Tounekti | 1.00 | 63.0 | — |

---

### Turkey

**xG vs avg opponent:** 0.8553 &nbsp;|&nbsp; GK=0.6549 &nbsp;|&nbsp; DEF=0.5506 &nbsp;|&nbsp; MID=0.5666 &nbsp;|&nbsp; ATT=0.2271

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=78.25 · normalized=0.6549)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Ugurcan Cakir | FIFA22 | U. Çakır | 1.00 | 79.0 | — |
|  | Altay Bayindir | FIFA22 | A. Bayındır | 1.00 | 77.5 | — |
| ✗ | Mert Günok | FC25 | Mert Günok | 1.00 | 76.2 | — |

#### Defenders &nbsp;(6/9 used · raw log-mean=76.45 · normalized=0.5506)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Caglar Soyuncu | FIFA22 | Ç. Söyüncü | 1.00 | 80.0 | — |
|  | Merih Demiral | FIFA22 | M. Demiral | 1.00 | 79.5 | — |
|  | Ozan Kabak | FC25 | Ozan Kabak | 1.00 | 77.5 | — |
|  | Ferdi Kadıoğlu | FC25 | Ferdi Kadıoğlu | 1.00 | 75.5 | — |
|  | Zeki Celik | FC25 | Zeki Çelik | 1.00 | 74.5 | — |
|  | Abdulkerim Bardakci | FIFA22 | A. Bardakcı | 1.00 | 72.0 | — |
| ✗ | Eren Elmalı | FC25 | Eren Elmalı | 1.00 | 70.5 | — |
| ✗ | Mert Müldür | FIFA22 | M. Müldür | 1.00 | 69.5 | — |
| ✗ | Akaydin | FIFA22 | S. Akaydin | 0.88 | 64.5 | — |

#### Midfielders &nbsp;(3/5 used · raw log-mean=77.32 · normalized=0.5666)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Hakan Calhanoglu | FIFA22 | H. Çalhanoğlu | 1.00 | 84.5 | — |
|  | Orkun Kökçü | FIFA22 | O. Kökçü | 1.00 | 76.5 | — |
|  | Ismail Yuksek | FC25 | İsmail Yüksek | 1.00 | 71.5 | — |
| ✗ | Salih Ozcan | FC25 | Salih Özcan | 1.00 | 71.0 | — |
| ✗ | Kaan Ayhan | FIFA22 | K. Ayhan | 1.00 | 69.5 | — |

#### Attackers &nbsp;(6/9 used · raw log-mean=73.37 · normalized=0.2271)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Kerem Akturkoglu | FC25 | Kerem Aktürkoğlu | 1.00 | 79.0 | — |
|  | Deniz Gül | median | — | — | 74.0 | — |
|  | Arda Güler | FC25 | Arda Güler | 1.00 | 72.5 | — |
|  | Irfan Can Kahveci | FIFA22 | İ. Kahveci | 1.00 | 72.5 | — |
|  | Yunus Akgun | FIFA22 | Y. Akgün | 1.00 | 71.5 | — |
|  | Can Uzun | FC25 | Can Uzun | 1.00 | 71.0 | — |
| ✗ | Barış Alper Yılmaz | FIFA22 | B. Yılmaz | 1.00 | 70.5 | — |
| ✗ | Kenan Yildiz | FC25 | Kenan Yıldız | 1.00 | 68.0 | — |
| ✗ | Oguz Aydin | FIFA22 | O. Aydın | 1.00 | 61.0 | — |

---

### USA

**xG vs avg opponent:** 1.1713 &nbsp;|&nbsp; GK=0.3501 &nbsp;|&nbsp; DEF=0.3192 &nbsp;|&nbsp; MID=0.4675 &nbsp;|&nbsp; ATT=0.4432

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=70.96 · normalized=0.3501)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Matt Turner | FC25 | Matt Turner | 1.00 | 73.2 | — |
|  | Chris Brady | FC25 | Chris Brady | 1.00 | 68.8 | — |
| ✗ | Matt Freese | FC25 | Matt Freese | 1.00 | 67.8 | — |

#### Defenders &nbsp;(7/10 used · raw log-mean=73.48 · normalized=0.3192)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Mark McKenzie | FC25 | Mark McKenzie | 1.00 | 75.5 | — |
|  | Chris Richards | FC25 | Chris Richards | 1.00 | 75.0 | — |
|  | Auston Trusty | FC25 | Auston Trusty | 1.00 | 75.0 | — |
|  | Miles Robinson | FC25 | Miles Robinson | 1.00 | 74.0 | — |
|  | Tim Ream | FC25 | Tim Ream | 1.00 | 73.0 | — |
|  | Joe Scally | FC25 | Joe Scally | 1.00 | 71.5 | — |
|  | Sergino Dest | FC25 | Sergiño Dest | 1.00 | 70.5 | — |
| ✗ | Antonee Robinson | FIFA22 | A. Robinson | 1.00 | 69.0 | — |
| ✗ | Max Arfsten | FC25 | Maximilian Arfsten | 0.76 | 55.5 | — |
| ✗ | Alex Freeman | FC25 | Alexander Freeman | 0.83 | 54.5 | — |

#### Midfielders &nbsp;(7/10 used · raw log-mean=75.48 · normalized=0.4675)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Christian Pulisic | FC25 | Christian Pulisic | 1.00 | 82.0 | — |
|  | Gio Reyna | FIFA22 | G. Reyna | 0.88 | 78.0 | — |
|  | Weston McKennie | FC25 | Weston McKennie | 1.00 | 77.5 | — |
|  | Malik Tillman | FC25 | Malik Tillman | 1.00 | 76.0 | — |
|  | Brenden Aaronson | FC25 | Brenden Aaronson | 1.00 | 73.0 | — |
|  | Alejandro Zendejas | FIFA22 | A. Bedoya | 0.77 | 71.5 | — |
|  | Timothy Weah | FC25 | Timothy Weah | 1.00 | 71.0 | — |
| ✗ | Tyler Adams | FC25 | Tyler Adams | 1.00 | 70.0 | — |
| ✗ | Cristian Roldan | FC25 | Cristian Roldan | 1.00 | 70.0 | — |
| ✗ | Sebastian Berhalter | FIFA22 | S. Berhalter | 1.00 | 59.5 | — |

#### Attackers &nbsp;(2/3 used · raw log-mean=76.13 · normalized=0.4432)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Folarin Balogun | FC25 | Folarin Balogun | 1.00 | 80.5 | — |
|  | Ricardo Pepi | FC25 | Ricardo Pepi | 1.00 | 72.0 | — |
| ✗ | Haji Wright | FIFA22 | H. Wright | 1.00 | 71.5 | — |

---

### Uruguay

**xG vs avg opponent:** 1.1993 &nbsp;|&nbsp; GK=0.6800 &nbsp;|&nbsp; DEF=0.6647 &nbsp;|&nbsp; MID=0.4477 &nbsp;|&nbsp; ATT=0.4671

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=78.85 · normalized=0.6800)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Fernando MUSLERA | FC25 | Fernando Muslera | 1.00 | 81.0 | — |
|  | Sergio ROCHET | FIFA22 | S. Rochet | 0.76 | 76.8 | — |
| ✗ | Santiago MELE | FC25 | Santiago Mele | 1.00 | 72.2 | — |

#### Defenders &nbsp;(5/7 used · raw log-mean=77.91 · normalized=0.6647)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Ronald ARAUJO | FC25 | Ronald Araujo | 1.00 | 84.5 | — |
|  | Jose Maria GIMENEZ | FC25 | José María Giménez | 1.00 | 83.5 | — |
|  | Santiago BUENO | FC25 | Santiago Bueno | 1.00 | 78.0 | — |
|  | Mathias OLIVERA | FC25 | Mathías Olivera | 1.00 | 74.0 | — |
|  | Sebastian CACERES | FC25 | Martín Cáceres | 0.77 | 70.5 | — |
| ✗ | Matias VINA | FIFA22 | M. Viña | 1.00 | 69.0 | — |
| ✗ | Guillermo VARELA | FIFA22 | G. Pereira | 0.79 | 54.0 | — |

#### Midfielders &nbsp;(8/11 used · raw log-mean=75.12 · normalized=0.4477)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Federico VALVERDE | FC25 | Federico Valverde | 1.00 | 84.0 | — |
|  | Rodrigo BENTANCUR | FC25 | Rodrigo Bentancur | 1.00 | 81.0 | — |
|  | Nicolas DE LA CRUZ | FIFA22 | N. De la Cruz | 0.80 | 79.0 | — |
|  | Rodrigo ZALAZAR | FC25 | Rodrigo Zalazar | 1.00 | 75.5 | — |
|  | Manuel UGARTE | FC25 | Manuel Ugarte | 1.00 | 75.0 | — |
|  | Giorgian DE ARRASCAETA | median | — | — | 70.5 | — |
|  | Joaquin PIQUEREZ | median | — | — | 70.5 | — |
| ✗ | Agustin CANOBBIO | FIFA22 | A. Canobbio | 0.82 | 67.0 | — |
|  | Emiliano MARTINEZ | FC25 | Emiliano Martínez | 1.00 | 67.0 | — |
| ✗ | Juan Manuel SANABRIA | FIFA22 | J. Sanabria | 0.85 | 64.0 | — |
| ✗ | Maxi ARAUJO | FIFA22 | M. Araújo | 0.84 | 58.5 | — |

#### Attackers &nbsp;(3/5 used · raw log-mean=76.44 · normalized=0.4671)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Darwin NUNEZ | FC25 | Darwin Núñez | 1.00 | 85.0 | — |
|  | Rodrigo AGUIRRE | FIFA22 | R. Aguirre | 0.75 | 74.0 | — |
|  | Facundo PELLISTRI | FC25 | Facundo Pellistri | 1.00 | 71.0 | — |
| ✗ | Brian RODRIGUEZ | FIFA22 | Á. Rodriguez | 0.85 | 63.5 | — |
| ✗ | Federico VINAS | FC25 | Federico Ricca | 0.79 | 57.0 | — |

---

### Uzbekistan

**xG vs avg opponent:** 0.6635 &nbsp;|&nbsp; GK=0.3882 &nbsp;|&nbsp; DEF=0.1994 &nbsp;|&nbsp; MID=0.1243 &nbsp;|&nbsp; ATT=0.3113

#### Goalkeepers &nbsp;(2/3 used · raw log-mean=71.88 · normalized=0.3882)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
| ✗ | Botirali Ergashev | median | — | — | 71.9 | — |
|  | Abduvohid Nematov | median | — | — | 71.9 | — |
|  | Utkir Yusupov | median | — | — | 71.9 | — |

#### Defenders &nbsp;(8/12 used · raw log-mean=71.94 · normalized=0.1994)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Abdullah Abdullaev | median | — | — | 71.9 | — |
|  | Khojiakbar Alijonov | median | — | — | 71.9 | — |
|  | Umarbek Eshmuradov | median | — | — | 71.9 | — |
|  | Bekhruz Karimov | median | — | — | 71.9 | — |
|  | Sherzod Nasrullaev | median | — | — | 71.9 | — |
|  | Farrukh Sayfiev | median | — | — | 71.9 | — |
|  | Avazbek Ulmasaliev | median | — | — | 71.9 | — |
|  | Jakhongir Urozov | median | — | — | 71.9 | — |
| ✗ | Abdukodir Khusanov | FC25 | Abdukodir Khusanov | 1.00 | 71.5 | — |
| ✗ | Rustamjon Ashurmatov | FIFA22 | R. Ashurmatov | 0.93 | 70.0 | — |
| ✗ | Umaraali Rakhmonaliev | TM | — | — | 65.0 | 600,000 |
| ✗ | Ruslanbek Yiyanov | TM | — | — | 65.0 | 400,000 |

#### Midfielders &nbsp;(6/8 used · raw log-mean=69.13 · normalized=0.1243)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Sherzod Esanov | median | — | — | 70.5 | — |
|  | Azizbek Ganiev | median | — | — | 70.5 | — |
|  | Odiljon Hamrobekov | median | — | — | 70.5 | — |
|  | Akmal Mozgovoy | median | — | — | 70.5 | — |
|  | Otabek Shukurov | FC25 | Otabek Shukurov | 1.00 | 68.0 | — |
| ✗ | Dostonbek Hamdamov | TM | — | — | 65.0 | 750,000 |
|  | Jashur Jaloliddinov | TM | — | — | 65.0 | 700,000 |
| ✗ | Jamshid Iskanderov | FIFA22 | J. Iskanderov | 1.00 | 61.5 | — |

#### Attackers &nbsp;(5/7 used · raw log-mean=74.45 · normalized=0.3113)

|   | Player | Tier | Matched as | Conf | Rating | MV (€) |
|---|--------|------|------------|------|--------|--------|
|  | Eldor Shomurodov | FIFA22 | E. Shomurodov | 1.00 | 75.5 | — |
|  | Abbosbek Fayzullaev | TM | — | — | 74.7 | 7,000,000 |
|  | Azizbek Amonov | median | — | — | 74.0 | — |
|  | Igor Sergeev | median | — | — | 74.0 | — |
|  | Sherzod Temirov | median | — | — | 74.0 | — |
| ✗ | Jaloliddin Masharipov | FIFA22 | J. Masharipov | 1.00 | 72.0 | — |
| ✗ | Oston Urunov | FIFA22 | D. Tursunov | 0.80 | 42.5 | — |
