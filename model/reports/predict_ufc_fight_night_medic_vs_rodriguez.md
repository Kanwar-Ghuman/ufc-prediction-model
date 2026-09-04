# UFC Fight Night: Medić vs. Rodriguez — 2026-08-01

Point-in-time predictions from 8639 historical fights. Educational output — NOT betting advice; the backtest shows this model does not beat the market.

Name spellings resolved against ufcstats: Uroš Medić -> Uros Medic; Jan Błachowicz -> Jan Blachowicz; Aleksandar Rakić -> Aleksandar Rakic; Duško Todorović -> Dusko Todorovic; Ľudovít Klein -> Ludovit Klein; Mateusz Rębecki -> Mateusz Rebecki

## Uros Medic vs. Daniel Rodriguez — Welterweight
P(Uros Medic wins) = 0.785  ->  pick: Uros Medic (78%)
- shipped number is the market-aware stack: vig-free market P(Uros Medic) = 0.757, skill-only model = 0.629 (gap -0.129)
- method: Uros Medic by KO 41% / sub 7% / dec 31%; Daniel Rodriguez by KO 8% / sub 3% / dec 10%
- how it ends: finish 59% (R1 24% / R2 16% / R3 10% / R4 5% / R5 4%) vs. decision 41%
- likeliest endings: Uros Medic by decision (31%), Uros Medic by KO/TKO, round 1 (17%), Uros Medic by KO/TKO, round 2 (11%)
- drivers (log-odds): diff_age +0.22, diff_strike_elo -0.17, f2_age +0.13, f1_age +0.11, diff_elo -0.07

| ending | R1 | R2 | R3 | R4 | R5 | any round |
|---|---|---|---|---|---|---|
| Uros Medic by KO/TKO | 17.4% | 11.0% | 6.3% | 3.3% | 2.6% | **40.6%** |
| Uros Medic by submission | 2.7% | 2.0% | 1.4% | 0.8% | 0.5% | **7.3%** |
| Daniel Rodriguez by KO/TKO | 3.1% | 2.4% | 1.4% | 0.7% | 0.6% | **8.2%** |
| Daniel Rodriguez by submission | 0.9% | 0.8% | 0.6% | 0.3% | 0.2% | **2.9%** |
| decision (either fighter) | — | — | — | — | — | **41.0%** |

## Jan Blachowicz vs. Navajo Stirling — Light Heavyweight
P(Jan Blachowicz wins) = 0.326  ->  pick: Navajo Stirling (67%)
- context: f2 flagged late replacement — confidence dampened
- shipped number is the market-aware stack: vig-free market P(Jan Blachowicz) = 0.267, skill-only model = 0.352 (gap +0.086)
- method: Jan Blachowicz by KO 16% / sub 4% / dec 12%; Navajo Stirling by KO 32% / sub 4% / dec 31%
- how it ends: finish 56% (R1 32% / R2 17% / R3 8%) vs. decision 44%
- likeliest endings: Navajo Stirling by decision (31%), Navajo Stirling by KO/TKO, round 1 (18%), Jan Blachowicz by decision (12%)
- drivers (log-odds): diff_age -0.41, f2_age -0.15, f1_age -0.14, diff_elo +0.06, diff_losses -0.05

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Jan Blachowicz by KO/TKO | 9.3% | 4.8% | 2.3% | **16.3%** |
| Jan Blachowicz by submission | 2.3% | 1.3% | 0.6% | **4.2%** |
| Navajo Stirling by KO/TKO | 18.3% | 9.7% | 4.4% | **32.4%** |
| Navajo Stirling by submission | 1.9% | 1.1% | 0.5% | **3.6%** |
| decision (either fighter) | — | — | — | **43.5%** |

## Aleksandar Rakic vs. Marcin Tybura — Heavyweight
P(Aleksandar Rakic wins) = 0.778  ->  pick: Aleksandar Rakic (78%)
- shipped number is the market-aware stack: vig-free market P(Aleksandar Rakic) = 0.744, skill-only model = 0.649 (gap -0.095)
- method: Aleksandar Rakic by KO 41% / sub 8% / dec 28%; Marcin Tybura by KO 10% / sub 3% / dec 10%
- how it ends: finish 62% (R1 34% / R2 19% / R3 9%) vs. decision 38%
- likeliest endings: Aleksandar Rakic by decision (28%), Aleksandar Rakic by KO/TKO, round 1 (23%), Aleksandar Rakic by KO/TKO, round 2 (12%)
- drivers (log-odds): diff_strike_elo +0.26, diff_age +0.18, diff_opp_elo_l5 +0.11, f1_age +0.05, diff_losses +0.04

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Aleksandar Rakic by KO/TKO | 23.4% | 12.4% | 5.5% | **41.4%** |
| Aleksandar Rakic by submission | 4.3% | 2.5% | 1.1% | **8.0%** |
| Marcin Tybura by KO/TKO | 5.1% | 3.2% | 1.6% | **9.9%** |
| Marcin Tybura by submission | 1.3% | 0.9% | 0.4% | **2.6%** |
| decision (either fighter) | — | — | — | **38.2%** |

## Dusko Todorovic vs. Robert Valentin — Middleweight
P(Dusko Todorovic wins) = 0.390  ->  pick: Robert Valentin (61%)
- shipped number is the market-aware stack: vig-free market P(Dusko Todorovic) = 0.400, skill-only model = 0.465 (gap +0.064)
- method: Dusko Todorovic by KO 10% / sub 4% / dec 26%; Robert Valentin by KO 26% / sub 14% / dec 21%
- how it ends: finish 54% (R1 30% / R2 16% / R3 7%) vs. decision 46%
- likeliest endings: Dusko Todorovic by decision (26%), Robert Valentin by decision (21%), Robert Valentin by KO/TKO, round 1 (15%)
- drivers (log-odds): diff_strike_elo +0.15, diff_td15_l5 +0.12, diff_age -0.09, diff_opp_elo_l5 -0.08, diff_sapm_l3 -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Dusko Todorovic by KO/TKO | 4.8% | 3.1% | 1.6% | **9.6%** |
| Dusko Todorovic by submission | 1.8% | 1.3% | 0.7% | **3.8%** |
| Robert Valentin by KO/TKO | 15.3% | 7.6% | 3.3% | **26.3%** |
| Robert Valentin by submission | 7.9% | 4.3% | 1.9% | **14.0%** |
| decision (either fighter) | — | — | — | **46.4%** |

## Vlasto Čepo vs. Gilbert Urbina — Middleweight
P(Vlasto Čepo wins) = 0.745  ->  pick: Vlasto Čepo (75%)
- CAUTION: no UFC history for Vlasto Čepo (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 14-3-0.
- shipped number is the market-aware stack: vig-free market P(Vlasto Čepo) = 0.748, skill-only model = 0.495 (gap -0.252)
- method: Vlasto Čepo by KO 38% / sub 17% / dec 19%; Gilbert Urbina by KO 9% / sub 6% / dec 11%
- how it ends: finish 70% (R1 43% / R2 19% / R3 8%) vs. decision 30%
- likeliest endings: Vlasto Čepo by KO/TKO, round 1 (24%), Vlasto Čepo by decision (19%), Gilbert Urbina by decision (11%)
- drivers (log-odds): f1_reach_cm -0.39, f2_reach_cm -0.34, diff_height_cm +0.30, diff_elo +0.16, f1_age -0.15

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Vlasto Čepo by KO/TKO | 24.0% | 10.0% | 4.2% | **38.1%** |
| Vlasto Čepo by submission | 10.2% | 4.6% | 2.0% | **16.9%** |
| Gilbert Urbina by KO/TKO | 5.7% | 2.4% | 1.0% | **9.1%** |
| Gilbert Urbina by submission | 3.4% | 1.6% | 0.7% | **5.6%** |
| decision (either fighter) | — | — | — | **30.3%** |

## Noah Gugnon vs. Miloš Janičić — Lightweight
P(Noah Gugnon wins) = 0.480  ->  pick: Miloš Janičić (52%)
- CAUTION: no UFC history for Noah Gugnon (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 9-2-0.
- CAUTION: no UFC history for Miloš Janičić (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 19-3-0.
- shipped number is the market-aware stack: vig-free market P(Noah Gugnon) = 0.478, skill-only model = 0.505 (gap +0.026)
- method: Noah Gugnon by KO 20% / sub 13% / dec 14%; Miloš Janičić by KO 22% / sub 14% / dec 16%
- how it ends: finish 70% (R1 42% / R2 20% / R3 8%) vs. decision 30%
- likeliest endings: Miloš Janičić by decision (16%), Noah Gugnon by decision (14%), Miloš Janičić by KO/TKO, round 1 (13%)
- drivers (log-odds): f1_age +0.20, f2_age +0.15, diff_height_cm -0.06, diff_age +0.05, f1_reach_cm +0.04

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Noah Gugnon by KO/TKO | 12.3% | 5.6% | 2.4% | **20.3%** |
| Noah Gugnon by submission | 7.8% | 3.9% | 1.7% | **13.4%** |
| Miloš Janičić by KO/TKO | 13.3% | 6.1% | 2.6% | **22.0%** |
| Miloš Janičić by submission | 8.5% | 4.2% | 1.8% | **14.5%** |
| decision (either fighter) | — | — | — | **29.9%** |

## Ludovit Klein vs. Tofiq Musayev — Lightweight
P(Ludovit Klein wins) = 0.713  ->  pick: Ludovit Klein (71%)
- shipped number is the market-aware stack: vig-free market P(Ludovit Klein) = 0.675, skill-only model = 0.642 (gap -0.033)
- method: Ludovit Klein by KO 24% / sub 12% / dec 36%; Tofiq Musayev by KO 7% / sub 4% / dec 18%
- how it ends: finish 46% (R1 24% / R2 15% / R3 7%) vs. decision 54%
- likeliest endings: Ludovit Klein by decision (36%), Tofiq Musayev by decision (18%), Ludovit Klein by KO/TKO, round 1 (13%)
- drivers (log-odds): diff_age +0.22, diff_elo +0.16, diff_strike_elo +0.14, diff_grapple_elo +0.09, f2_age +0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Ludovit Klein by KO/TKO | 12.6% | 7.4% | 3.8% | **23.9%** |
| Ludovit Klein by submission | 6.0% | 3.9% | 2.0% | **11.9%** |
| Tofiq Musayev by KO/TKO | 3.6% | 2.0% | 1.0% | **6.6%** |
| Tofiq Musayev by submission | 2.1% | 1.3% | 0.6% | **4.0%** |
| decision (either fighter) | — | — | — | **53.6%** |

## Oban Elliott vs. Michael Oliveira — Welterweight
P(Oban Elliott wins) = 0.269  ->  pick: Michael Oliveira (73%)
- CAUTION: no UFC history for Michael Oliveira (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 9-0-0.
- shipped number is the market-aware stack: vig-free market P(Oban Elliott) = 0.252, skill-only model = 0.562 (gap +0.310)
- method: Oban Elliott by KO 12% / sub 4% / dec 11%; Michael Oliveira by KO 25% / sub 17% / dec 30%
- how it ends: finish 59% (R1 33% / R2 17% / R3 8%) vs. decision 41%
- likeliest endings: Michael Oliveira by decision (30%), Michael Oliveira by KO/TKO, round 1 (15%), Oban Elliott by decision (11%)
- drivers (log-odds): f2_reach_cm +0.35, f1_reach_cm +0.34, diff_height_cm -0.30, f2_height_cm -0.16, diff_strike_elo +0.16

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Oban Elliott by KO/TKO | 6.7% | 3.7% | 1.8% | **12.2%** |
| Oban Elliott by submission | 2.0% | 1.2% | 0.6% | **3.7%** |
| Michael Oliveira by KO/TKO | 15.0% | 7.3% | 3.2% | **25.5%** |
| Michael Oliveira by submission | 9.7% | 5.2% | 2.4% | **17.3%** |
| decision (either fighter) | — | — | — | **41.4%** |

## Borislav Nikolić vs. Mark Vologdin — Bantamweight
P(Borislav Nikolić wins) = 0.509  ->  pick: Borislav Nikolić (51%)
- CAUTION: no UFC history for Borislav Nikolić (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 16-2-0.
- shipped number is the market-aware stack: vig-free market P(Borislav Nikolić) = 0.580, skill-only model = 0.289 (gap -0.291)
- method: Borislav Nikolić by KO 17% / sub 9% / dec 25%; Mark Vologdin by KO 21% / sub 12% / dec 17%
- how it ends: finish 59% (R1 34% / R2 17% / R3 8%) vs. decision 41%
- likeliest endings: Borislav Nikolić by decision (25%), Mark Vologdin by decision (17%), Mark Vologdin by KO/TKO, round 1 (12%)
- drivers (log-odds): f1_age -0.22, f2_age -0.18, diff_strike_elo +0.17, f1_reach_cm -0.13, f2_reach_cm -0.13

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Borislav Nikolić by KO/TKO | 9.9% | 4.8% | 2.2% | **16.9%** |
| Borislav Nikolić by submission | 5.2% | 2.8% | 1.3% | **9.2%** |
| Mark Vologdin by KO/TKO | 12.0% | 5.9% | 2.7% | **20.6%** |
| Mark Vologdin by submission | 6.6% | 3.6% | 1.6% | **11.8%** |
| decision (either fighter) | — | — | — | **41.5%** |

## Dennis Buzukja vs. Bogdan Grad — Featherweight
P(Dennis Buzukja wins) = 0.294  ->  pick: Bogdan Grad (71%)
- shipped number is the market-aware stack: vig-free market P(Dennis Buzukja) = 0.355, skill-only model = 0.289 (gap -0.067)
- method: Dennis Buzukja by KO 8% / sub 4% / dec 18%; Bogdan Grad by KO 12% / sub 10% / dec 48%
- how it ends: finish 35% (R1 17% / R2 11% / R3 6%) vs. decision 65%
- likeliest endings: Bogdan Grad by decision (48%), Dennis Buzukja by decision (18%), Bogdan Grad by KO/TKO, round 1 (6%)
- drivers (log-odds): diff_elo -0.10, diff_strike_elo -0.09, diff_grapple_elo -0.09, diff_age +0.09, diff_opp_elo_l5 -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Dennis Buzukja by KO/TKO | 3.9% | 2.6% | 1.6% | **8.0%** |
| Dennis Buzukja by submission | 1.7% | 1.2% | 0.8% | **3.7%** |
| Bogdan Grad by KO/TKO | 6.5% | 3.9% | 2.0% | **12.5%** |
| Bogdan Grad by submission | 5.2% | 3.4% | 1.8% | **10.4%** |
| decision (either fighter) | — | — | — | **65.4%** |

## Mateusz Rebecki vs. Kyle Prepolec — Lightweight
P(Mateusz Rebecki wins) = 0.833  ->  pick: Mateusz Rebecki (83%)
- shipped number is the market-aware stack: vig-free market P(Mateusz Rebecki) = 0.808, skill-only model = 0.642 (gap -0.165)
- method: Mateusz Rebecki by KO 22% / sub 19% / dec 43%; Kyle Prepolec by KO 6% / sub 2% / dec 9%
- how it ends: finish 48% (R1 25% / R2 16% / R3 7%) vs. decision 52%
- likeliest endings: Mateusz Rebecki by decision (43%), Mateusz Rebecki by KO/TKO, round 1 (11%), Mateusz Rebecki by submission, round 1 (9%)
- drivers (log-odds): diff_strike_elo +0.24, diff_elo +0.15, diff_opp_elo_l5 +0.14, diff_age +0.13, diff_grapple_elo +0.10

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Mateusz Rebecki by KO/TKO | 11.4% | 7.1% | 3.2% | **21.7%** |
| Mateusz Rebecki by submission | 9.4% | 6.4% | 2.9% | **18.6%** |
| Kyle Prepolec by KO/TKO | 3.0% | 1.8% | 0.9% | **5.7%** |
| Kyle Prepolec by submission | 1.1% | 0.7% | 0.4% | **2.2%** |
| decision (either fighter) | — | — | — | **51.8%** |

## Nina Nikolija Milošević vs. Hailey Cowan — Women's Bantamweight
P(Nina Nikolija Milošević wins) = 0.758  ->  pick: Nina Nikolija Milošević (76%)
- CAUTION: no UFC history for Nina Nikolija Milošević (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 8-1-0.
- shipped number is the market-aware stack: vig-free market P(Nina Nikolija Milošević) = 0.777, skill-only model = 0.425 (gap -0.352)
- method: Nina Nikolija Milošević by KO 23% / sub 16% / dec 37%; Hailey Cowan by KO 5% / sub 6% / dec 13%
- how it ends: finish 50% (R1 29% / R2 15% / R3 7%) vs. decision 50%
- likeliest endings: Nina Nikolija Milošević by decision (37%), Nina Nikolija Milošević by KO/TKO, round 1 (13%), Hailey Cowan by decision (13%)
- drivers (log-odds): f1_reach_cm -0.34, f2_reach_cm -0.28, diff_height_cm +0.28, diff_elo +0.16, diff_strike_elo +0.14

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Nina Nikolija Milošević by KO/TKO | 13.5% | 6.7% | 3.1% | **23.2%** |
| Nina Nikolija Milošević by submission | 9.0% | 4.8% | 2.2% | **16.1%** |
| Hailey Cowan by KO/TKO | 3.1% | 1.5% | 0.7% | **5.3%** |
| Hailey Cowan by submission | 3.2% | 1.7% | 0.8% | **5.8%** |
| decision (either fighter) | — | — | — | **49.7%** |

## Jovan Leka vs. Alexander Poppeck — Heavyweight
P(Jovan Leka wins) = 0.642  ->  pick: Jovan Leka (64%)
- CAUTION: no UFC history for Jovan Leka (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 13-2-0.
- CAUTION: no UFC history for Alexander Poppeck (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 21-5-0.
- shipped number is the market-aware stack: vig-free market P(Jovan Leka) = 0.657, skill-only model = 0.449 (gap -0.208)
- method: Jovan Leka by KO 31% / sub 21% / dec 13%; Alexander Poppeck by KO 18% / sub 8% / dec 10%
- how it ends: finish 77% (R1 44% / R2 23% / R3 11%) vs. decision 23%
- likeliest endings: Jovan Leka by KO/TKO, round 1 (18%), Jovan Leka by decision (13%), Jovan Leka by submission, round 1 (12%)
- drivers (log-odds): diff_age +0.29, f1_reach_cm -0.10, f2_age +0.08, f2_reach_cm -0.08, f1_age +0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Jovan Leka by KO/TKO | 17.7% | 8.8% | 4.0% | **30.6%** |
| Jovan Leka by submission | 11.6% | 6.2% | 2.9% | **20.7%** |
| Alexander Poppeck by KO/TKO | 10.2% | 5.4% | 2.6% | **18.1%** |
| Alexander Poppeck by submission | 4.2% | 2.4% | 1.1% | **7.8%** |
| decision (either fighter) | — | — | — | **22.8%** |

## Stephanie Luciano vs. Marina Spasić — Women's Strawweight
P(Stephanie Luciano wins) = 0.735  ->  pick: Stephanie Luciano (74%)
- CAUTION: no UFC history for Marina Spasić (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 7-1-0.
- shipped number is the market-aware stack: vig-free market P(Stephanie Luciano) = 0.710, skill-only model = 0.606 (gap -0.103)
- method: Stephanie Luciano by KO 29% / sub 15% / dec 29%; Marina Spasić by KO 6% / sub 6% / dec 15%
- how it ends: finish 56% (R1 33% / R2 16% / R3 7%) vs. decision 44%
- likeliest endings: Stephanie Luciano by decision (29%), Stephanie Luciano by KO/TKO, round 1 (17%), Marina Spasić by decision (15%)
- drivers (log-odds): f2_reach_cm +0.30, f1_reach_cm +0.30, diff_height_cm -0.26, f2_height_cm -0.18, diff_strike_elo +0.18

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Stephanie Luciano by KO/TKO | 17.4% | 8.4% | 3.6% | **29.5%** |
| Stephanie Luciano by submission | 8.6% | 4.5% | 2.0% | **15.1%** |
| Marina Spasić by KO/TKO | 3.5% | 1.6% | 0.7% | **5.7%** |
| Marina Spasić by submission | 3.3% | 1.7% | 0.8% | **5.8%** |
| decision (either fighter) | — | — | — | **43.9%** |

---
*Simulation/educational project. No betting advice. The market knows more than this model.*