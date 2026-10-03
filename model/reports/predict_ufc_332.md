# UFC 332 — 2026-10-03

Point-in-time predictions from 8731 historical fights. Educational output — NOT betting advice; the backtest shows this model does not beat the market.

Name spellings resolved against ufcstats: Natália Silva -> Natalia Silva; Imanol Rodríguez -> Imanol Rodriguez; Rafael dos Anjos -> Rafael Dos Anjos

Prediction mode: **skill_only**. Odds, ranking nudges and social sentiment do not change these probabilities.
Historical results available through 2026-09-12.

## Natalia Silva vs. Wang Cong — Women's Flyweight
P(Natalia Silva wins) = 0.642  ->  pick: Natalia Silva (64%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Wang Cong is the volume striker (6.8 vs 4.5 SLpM).
- research: Form: Natalia Silva holds the pre-fight-expectation-adjusted form edge (hot vs hot over the last 5).
- research: Style record: Natalia Silva is 100% against strikers in the UFC.
- research: Common opponents: 1 shared names on the record.
- recent fights, Natalia Silva: 2026-01-24 win vs Rose Namajunas (U-DEC); 2025-05-10 win vs Alexa Grasso (U-DEC); 2024-09-07 win vs Jessica Andrade (U-DEC)
- recent fights, Wang Cong: 2026-07-11 win vs Tracy Cortez (U-DEC); 2026-02-07 win vs Eduarda Moura (U-DEC); 2025-06-07 win vs Ariane da Silva (U-DEC)
- independent model votes for Natalia Silva: logistic 66.3%, calibrated GBM 63.2%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Natalia Silva | Wang Cong |
|---|---:|---:|
| Age | 29.66 | 34.38 |
| Reach (cm) | 165.10 | 167.64 |
| UFC fights | 8.00 | 6.00 |
| Days since UFC fight | 252.00 | 84.00 |
| Last 3: sig. strikes landed/min | 5.18 | 7.09 |
| Last 3: sig. strikes absorbed/min | 2.69 | 3.27 |
| Last 5: takedowns/15 min | 0.20 | 0.44 |
| Last 5: takedown defense (fraction) | 0.88 | 0.86 |
| Last 5: control-time fraction | 0.03 | 0.07 |
| Last 5: opponent pre-fight Elo | 1646.44 | 1548.00 |

- skill-only research model P(Natalia Silva) = 0.642; vig-free market = 0.643 (gap -0.002). Market shown for comparison only.
- method: Natalia Silva by KO 14% / sub 8% / dec 43%; Wang Cong by KO 10% / sub 2% / dec 23%
- pick outcome: Natalia Silva by decision (43%)
- how it ends: finish 34% (R1 12% / R2 10% / R3 6% / R4 3% / R5 3%) vs. decision 66%
- likeliest endings: Natalia Silva by decision (43%), Wang Cong by decision (23%), Natalia Silva by KO/TKO, round 1 (6%)
- drivers (log-odds): diff_elo +0.17, diff_strike_elo -0.16, diff_age +0.16, diff_opp_elo_l5 +0.12, f1_career_streak +0.06

| ending | R1 | R2 | R3 | R4 | R5 | any round |
|---|---|---|---|---|---|---|
| Natalia Silva by KO/TKO | 5.5% | 4.1% | 2.2% | 1.1% | 0.9% | **13.8%** |
| Natalia Silva by submission | 2.6% | 2.2% | 1.4% | 0.8% | 0.5% | **7.6%** |
| Wang Cong by KO/TKO | 3.5% | 2.8% | 1.8% | 1.0% | 0.9% | **10.0%** |
| Wang Cong by submission | 0.8% | 0.7% | 0.5% | 0.3% | 0.2% | **2.5%** |
| decision (either fighter) | — | — | — | — | — | **66.1%** |

## Deiveson Figueiredo vs. Payton Talbott — Bantamweight
P(Deiveson Figueiredo wins) = 0.246  ->  pick: Payton Talbott (75%)
- research: Style: Deiveson Figueiredo profiles as a wrestler; Payton Talbott as a striker.
- research: Pace: Payton Talbott is the volume striker (6.6 vs 1.3 SLpM).
- research: Form: Payton Talbott holds the pre-fight-expectation-adjusted form edge (cold vs hot over the last 5).
- research: Style record: Deiveson Figueiredo is 67% against strikers in the UFC.
- recent fights, Deiveson Figueiredo: 2026-05-30 loss vs Song Yadong (SUB); 2026-01-24 loss vs Umar Nurmagomedov (U-DEC); 2025-10-11 win vs Montel Jackson (S-DEC)
- recent fights, Payton Talbott: 2025-12-06 win vs Henry Cejudo (U-DEC); 2025-06-28 win vs Felipe Lima (U-DEC); 2025-01-18 loss vs Raoni Barcelos (U-DEC)
- independent model votes for Deiveson Figueiredo: logistic 20.8%, calibrated GBM 26.3%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Deiveson Figueiredo | Payton Talbott |
|---|---:|---:|
| Age | 38.79 | 28.07 |
| Reach (cm) | 172.72 | 177.80 |
| UFC fights | 22.00 | 6.00 |
| Days since UFC fight | 126.00 | 301.00 |
| Last 3: sig. strikes landed/min | 1.01 | 5.38 |
| Last 3: sig. strikes absorbed/min | 2.22 | 3.29 |
| Last 5: takedowns/15 min | 1.42 | 1.18 |
| Last 5: takedown defense (fraction) | 0.50 | 0.70 |
| Last 5: control-time fraction | 0.09 | 0.20 |
| Last 5: opponent pre-fight Elo | 1740.50 | 1584.16 |

- skill-only research model P(Deiveson Figueiredo) = 0.246; vig-free market = 0.153 (gap +0.094). Market shown for comparison only.
- method: Deiveson Figueiredo by KO 4% / sub 6% / dec 15%; Payton Talbott by KO 27% / sub 8% / dec 40%
- pick outcome: Payton Talbott by decision (40%)
- how it ends: finish 45% (R1 23% / R2 14% / R3 7%) vs. decision 55%
- likeliest endings: Payton Talbott by decision (40%), Payton Talbott by KO/TKO, round 1 (15%), Deiveson Figueiredo by decision (15%)
- drivers (log-odds): diff_age -0.36, diff_strike_elo -0.31, diff_sig_acc_l5 -0.08, diff_opp_elo_l5 +0.07, diff_career_win_pct -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Deiveson Figueiredo by KO/TKO | 1.8% | 1.3% | 0.8% | **4.0%** |
| Deiveson Figueiredo by submission | 2.6% | 2.0% | 1.3% | **6.0%** |
| Payton Talbott by KO/TKO | 14.9% | 8.3% | 3.9% | **27.0%** |
| Payton Talbott by submission | 4.2% | 2.5% | 1.2% | **7.9%** |
| decision (either fighter) | — | — | — | **55.1%** |

## King Green vs. Esteban Ribovics — Lightweight
P(King Green wins) = 0.521  ->  pick: King Green (52%; close fight)
- research: Wrestling contrast: King Green lands 2.1 takedowns/15 into Esteban Ribovics's 76% TDD.
- research: Last fights: King Green won last time out; Esteban Ribovics won last time out.
- research: Style record: King Green is 54% against strikers in the UFC.
- research: Common opponents: 4 shared names on the record.
- recent fights, King Green: 2026-07-11 win vs Terrance McKinney (KO/TKO); 2026-05-09 win vs Jeremy Stephens (SUB); 2026-02-28 win vs Daniel Zellhuber (KO/TKO)
- recent fights, Esteban Ribovics: 2026-08-15 win vs Edson Barboza (KO/TKO); 2026-04-11 loss vs Mateusz Gamrot (SUB); 2025-08-02 win vs Elves Brener (U-DEC)
- independent model votes for King Green: logistic 57.1%, calibrated GBM 50.0%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | King Green | Esteban Ribovics |
|---|---:|---:|
| Age | 40.07 | 30.43 |
| Reach (cm) | 180.34 | 175.26 |
| UFC fights | 31.00 | 8.00 |
| Days since UFC fight | 84.00 | 49.00 |
| Last 3: sig. strikes landed/min | 9.67 | 6.13 |
| Last 3: sig. strikes absorbed/min | 3.48 | 5.38 |
| Last 5: takedowns/15 min | 2.06 | 0.00 |
| Last 5: takedown defense (fraction) | 0.25 | 0.76 |
| Last 5: control-time fraction | 0.12 | 0.02 |
| Last 5: opponent pre-fight Elo | 1522.94 | 1619.05 |

- skill-only research model P(King Green) = 0.521; vig-free market = 0.362 (gap +0.160). Market shown for comparison only.
- method: King Green by KO 17% / sub 7% / dec 28%; Esteban Ribovics by KO 23% / sub 5% / dec 19%
- pick outcome: King Green by decision (28%)
- how it ends: finish 53% (R1 29% / R2 17% / R3 8%) vs. decision 47%
- likeliest endings: King Green by decision (28%), Esteban Ribovics by decision (19%), Esteban Ribovics by KO/TKO, round 1 (14%)
- drivers (log-odds): diff_age -0.34, diff_strike_elo +0.32, diff_opp_elo_l5 -0.12, diff_age_past_prime -0.10, diff_career_win_pct -0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| King Green by KO/TKO | 8.8% | 5.7% | 2.9% | **17.4%** |
| King Green by submission | 3.4% | 2.4% | 1.2% | **7.0%** |
| Esteban Ribovics by KO/TKO | 13.6% | 6.8% | 2.8% | **23.3%** |
| Esteban Ribovics by submission | 3.0% | 1.6% | 0.7% | **5.2%** |
| decision (either fighter) | — | — | — | **47.1%** |

## Roberto Soldić vs. Khaos Williams — Welterweight
P(Roberto Soldić wins) = 0.274  ->  pick: Khaos Williams (73%)
- CAUTION: no UFC history for Roberto Soldić (debut or misspelled name?) — prediction is weak.
- research: Last fights: Khaos Williams won last time out.
- recent fights, Khaos Williams: 2026-05-16 win vs Nikolay Veretennikov (KO/TKO); 2025-06-07 loss vs Andreas Gustafsson (U-DEC); 2025-02-15 loss vs Gabriel Bonfim (SUB)
- independent model votes for Roberto Soldić: logistic 38.6%, calibrated GBM 22.6%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Roberto Soldić | Khaos Williams |
|---|---:|---:|
| Age | unavailable | 32.51 |
| Reach (cm) | unavailable | 195.58 |
| UFC fights | 0.00 | 11.00 |
| Days since UFC fight | unavailable | 140.00 |
| Last 3: sig. strikes landed/min | unavailable | 2.81 |
| Last 3: sig. strikes absorbed/min | unavailable | 5.13 |
| Last 5: takedowns/15 min | unavailable | 0.00 |
| Last 5: takedown defense (fraction) | unavailable | 0.43 |
| Last 5: control-time fraction | unavailable | 0.11 |
| Last 5: opponent pre-fight Elo | unavailable | 1540.88 |

- skill-only research model P(Roberto Soldić) = 0.274; vig-free market = 0.656 (gap -0.382). Market shown for comparison only.
- method: Roberto Soldić by KO 12% / sub 6% / dec 9%; Khaos Williams by KO 40% / sub 8% / dec 25%
- pick outcome: Khaos Williams by KO/TKO, round 1 (method 40%; round given method 65%; exact outcome 26%)
- how it ends: finish 66% (R1 43% / R2 17% / R3 7%) vs. decision 34%
- likeliest endings: Khaos Williams by KO/TKO, round 1 (26%), Khaos Williams by decision (25%), Khaos Williams by KO/TKO, round 2 (10%)
- drivers (log-odds): f2_reach_cm -0.47, f1_reach_cm -0.40, diff_strike_elo -0.21, diff_height_cm +0.21, f2_height_cm +0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Roberto Soldić by KO/TKO | 8.1% | 2.9% | 1.1% | **12.1%** |
| Roberto Soldić by submission | 4.2% | 1.6% | 0.7% | **6.4%** |
| Khaos Williams by KO/TKO | 25.8% | 10.0% | 4.1% | **39.9%** |
| Khaos Williams by submission | 5.0% | 2.1% | 0.9% | **7.9%** |
| decision (either fighter) | — | — | — | **33.6%** |

## Ateba Gautier vs. Roman Kopylov — Middleweight
P(Ateba Gautier wins) = 0.737  ->  pick: Ateba Gautier (74%)
- research: Form: Ateba Gautier holds the pre-fight-expectation-adjusted form edge (hot vs mixed over the last 5).
- research: Style record: Roman Kopylov is 64% against strikers in the UFC.
- recent fights, Ateba Gautier: 2026-05-09 win vs Ozzy Diaz (KO/TKO); 2026-01-24 win vs Andrey Pulyaev (U-DEC); 2025-10-04 win vs Tre'ston Vines (KO/TKO)
- recent fights, Roman Kopylov: 2026-05-09 win vs Marco Tulio (U-DEC); 2025-11-15 loss vs Gregory Rodrigues (U-DEC); 2025-07-19 loss vs Paulo Costa (U-DEC)
- independent model votes for Ateba Gautier: logistic 65.1%, calibrated GBM 77.4%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Ateba Gautier | Roman Kopylov |
|---|---:|---:|
| Age | 24.48 | 35.42 |
| Reach (cm) | 205.74 | 190.50 |
| UFC fights | 5.00 | 12.00 |
| Days since UFC fight | 147.00 | 147.00 |
| Last 3: sig. strikes landed/min | 2.76 | 3.58 |
| Last 3: sig. strikes absorbed/min | 2.84 | 5.58 |
| Last 5: takedowns/15 min | 0.54 | 1.80 |
| Last 5: takedown defense (fraction) | 1.00 | 1.00 |
| Last 5: control-time fraction | 0.00 | 0.17 |
| Last 5: opponent pre-fight Elo | 1479.38 | 1598.54 |

- skill-only research model P(Ateba Gautier) = 0.737; vig-free market = 0.676 (gap +0.061). Market shown for comparison only.
- method: Ateba Gautier by KO 41% / sub 5% / dec 27%; Roman Kopylov by KO 12% / sub 2% / dec 12%
- pick outcome: Ateba Gautier by KO/TKO, round 1 (method 41%; round given method 52%; exact outcome 21%)
- how it ends: finish 60% (R1 31% / R2 19% / R3 10%) vs. decision 40%
- likeliest endings: Ateba Gautier by decision (27%), Ateba Gautier by KO/TKO, round 1 (21%), Ateba Gautier by KO/TKO, round 2 (13%)
- drivers (log-odds): diff_age +0.36, diff_strike_elo +0.25, diff_style_reach_striker +0.19, diff_opp_elo_l5 -0.08, diff_elo +0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Ateba Gautier by KO/TKO | 21.3% | 12.7% | 6.9% | **40.9%** |
| Ateba Gautier by submission | 2.6% | 1.7% | 1.0% | **5.3%** |
| Roman Kopylov by KO/TKO | 5.8% | 4.1% | 2.0% | **11.9%** |
| Roman Kopylov by submission | 1.1% | 0.8% | 0.4% | **2.3%** |
| decision (either fighter) | — | — | — | **39.6%** |

## Imanol Rodriguez vs. Alden Coria — Flyweight
P(Imanol Rodriguez wins) = 0.420  ->  pick: Alden Coria (58%)
- research: Last fights: Imanol Rodriguez won last time out; Alden Coria won last time out.
- research: Style record: Alden Coria is 100% against strikers in the UFC.
- recent fights, Imanol Rodriguez: 2026-02-28 win vs Kevin Borjas (KO/TKO); 2025-10-07 win vs Roque Conceicao Moreira Junior (KO/TKO); 2024-09-22 win vs Alberto Trujillo (KO/TKO)
- recent fights, Alden Coria: 2026-07-18 win vs Stewart Nicoll (U-DEC); 2026-02-21 win vs Luis Gurule (U-DEC); 2025-09-13 win vs Alessandro Costa (KO/TKO)
- independent model votes for Imanol Rodriguez: logistic 47.2%, calibrated GBM 39.7%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Imanol Rodriguez | Alden Coria |
|---|---:|---:|
| Age | 26.88 | 28.44 |
| Reach (cm) | unavailable | 170.18 |
| UFC fights | 1.00 | 3.00 |
| Days since UFC fight | 217.00 | 77.00 |
| Last 3: sig. strikes landed/min | 4.92 | 4.05 |
| Last 3: sig. strikes absorbed/min | 2.35 | 2.21 |
| Last 5: takedowns/15 min | 1.60 | 2.21 |
| Last 5: takedown defense (fraction) | unavailable | 0.56 |
| Last 5: control-time fraction | 0.38 | 0.18 |
| Last 5: opponent pre-fight Elo | 1441.40 | 1442.11 |

- skill-only research model P(Imanol Rodriguez) = 0.420; vig-free market = 0.565 (gap -0.145). Market shown for comparison only.
- method: Imanol Rodriguez by KO 12% / sub 6% / dec 24%; Alden Coria by KO 15% / sub 13% / dec 30%
- pick outcome: Alden Coria by decision (30%)
- how it ends: finish 46% (R1 21% / R2 15% / R3 10%) vs. decision 54%
- likeliest endings: Alden Coria by decision (30%), Imanol Rodriguez by decision (24%), Alden Coria by KO/TKO, round 1 (7%)
- drivers (log-odds): f2_reach_cm -0.45, f1_reach_cm -0.32, diff_height_cm +0.21, diff_strike_elo -0.20, f2_height_cm +0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Imanol Rodriguez by KO/TKO | 6.4% | 3.8% | 2.1% | **12.3%** |
| Imanol Rodriguez by submission | 2.8% | 1.8% | 1.0% | **5.7%** |
| Alden Coria by KO/TKO | 6.8% | 5.2% | 3.5% | **15.5%** |
| Alden Coria by submission | 5.4% | 4.4% | 3.0% | **12.8%** |
| decision (either fighter) | — | — | — | **53.8%** |

## Damian Pinas vs. Andrey Pulyaev — Middleweight
P(Damian Pinas wins) = 0.641  ->  pick: Damian Pinas (64%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Damian Pinas is the volume striker (5.5 vs 2.5 SLpM).
- research: Form: Damian Pinas holds the pre-fight-expectation-adjusted form edge (hot vs cold over the last 5).
- research: Style record: Andrey Pulyaev is 25% against strikers in the UFC.
- recent fights, Damian Pinas: 2026-07-11 win vs Cesar Almeida (KO/TKO); 2026-02-28 win vs Wes Schultz (KO/TKO); 2025-09-30 win vs Vitor Costa (KO/TKO)
- recent fights, Andrey Pulyaev: 2026-06-27 loss vs Nursulton Ruziboev (SUB); 2026-01-24 loss vs Ateba Gautier (U-DEC); 2025-08-02 win vs Nick Klein (KO/TKO)
- independent model votes for Damian Pinas: logistic 71.6%, calibrated GBM 60.9%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Damian Pinas | Andrey Pulyaev |
|---|---:|---:|
| Age | 24.56 | 29.06 |
| Reach (cm) | 200.66 | 198.12 |
| UFC fights | 2.00 | 4.00 |
| Days since UFC fight | 84.00 | 98.00 |
| Last 3: sig. strikes landed/min | 5.53 | 3.30 |
| Last 3: sig. strikes absorbed/min | 5.53 | 1.77 |
| Last 5: takedowns/15 min | 0.00 | 0.00 |
| Last 5: takedown defense (fraction) | 0.86 | 0.45 |
| Last 5: control-time fraction | 0.12 | 0.05 |
| Last 5: opponent pre-fight Elo | 1512.35 | 1552.33 |

- skill-only research model P(Damian Pinas) = 0.641; vig-free market = 0.818 (gap -0.176). Market shown for comparison only.
- method: Damian Pinas by KO 38% / sub 11% / dec 15%; Andrey Pulyaev by KO 16% / sub 4% / dec 16%
- pick outcome: Damian Pinas by KO/TKO, round 1 (method 38%; round given method 57%; exact outcome 22%)
- how it ends: finish 68% (R1 38% / R2 20% / R3 10%) vs. decision 32%
- likeliest endings: Damian Pinas by KO/TKO, round 1 (22%), Andrey Pulyaev by decision (16%), Damian Pinas by decision (15%)
- drivers (log-odds): diff_strike_elo -0.19, diff_elo +0.18, diff_age +0.18, diff_career_win_pct +0.09, diff_opp_elo_l5 -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Damian Pinas by KO/TKO | 21.8% | 10.8% | 5.3% | **38.0%** |
| Damian Pinas by submission | 5.9% | 3.2% | 1.7% | **10.8%** |
| Andrey Pulyaev by KO/TKO | 8.7% | 5.0% | 2.2% | **15.9%** |
| Andrey Pulyaev by submission | 1.9% | 1.2% | 0.5% | **3.7%** |
| decision (either fighter) | — | — | — | **31.7%** |

## Marcus McGhee vs. Anthony Romero — Featherweight
P(Marcus McGhee wins) = 0.600  ->  pick: Marcus McGhee (60%)
- CAUTION: no UFC history for Anthony Romero (debut or misspelled name?) — prediction is weak.
- research: Last fights: Marcus McGhee won last time out.
- recent fights, Marcus McGhee: 2026-06-06 win vs John Yannis (U-DEC); 2025-07-26 loss vs Petr Yan (U-DEC); 2024-11-16 win vs Jonathan Martinez (U-DEC)
- independent model votes for Marcus McGhee: logistic 59.4%, calibrated GBM 60.3%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Marcus McGhee | Anthony Romero |
|---|---:|---:|
| Age | 36.41 | 29.60 |
| Reach (cm) | 175.26 | 177.80 |
| UFC fights | 6.00 | 0.00 |
| Days since UFC fight | 119.00 | unavailable |
| Last 3: sig. strikes landed/min | 5.44 | unavailable |
| Last 3: sig. strikes absorbed/min | 4.09 | unavailable |
| Last 5: takedowns/15 min | 0.27 | unavailable |
| Last 5: takedown defense (fraction) | 0.75 | unavailable |
| Last 5: control-time fraction | 0.04 | unavailable |
| Last 5: opponent pre-fight Elo | 1579.43 | unavailable |

- skill-only research model P(Marcus McGhee) = 0.600; vig-free market = 0.809 (gap -0.209). Market shown for comparison only.
- method: Marcus McGhee by KO 21% / sub 6% / dec 33%; Anthony Romero by KO 18% / sub 7% / dec 15%
- pick outcome: Marcus McGhee by decision (33%)
- how it ends: finish 52% (R1 29% / R2 15% / R3 7%) vs. decision 48%
- likeliest endings: Marcus McGhee by decision (33%), Anthony Romero by decision (15%), Marcus McGhee by KO/TKO, round 1 (11%)
- drivers (log-odds): diff_strike_elo +0.32, diff_age -0.22, diff_elo +0.13, diff_age_past_prime -0.06, f1_age -0.05

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Marcus McGhee by KO/TKO | 11.5% | 6.3% | 3.1% | **20.9%** |
| Marcus McGhee by submission | 3.1% | 1.8% | 0.9% | **5.8%** |
| Anthony Romero by KO/TKO | 11.0% | 5.0% | 2.1% | **18.1%** |
| Anthony Romero by submission | 3.9% | 2.0% | 0.9% | **6.8%** |
| decision (either fighter) | — | — | — | **48.4%** |

## Anthony Wint vs. Lucas Armand — Heavyweight
P(Anthony Wint wins) = 0.731  ->  pick: Anthony Wint (73%)
- CAUTION: no UFC history for Lucas Armand (debut or misspelled name?) — prediction is weak.
- research: Last fights: Anthony Wint won last time out.
- recent fights, Anthony Wint: 2026-08-22 win vs Terrance Chatman (SUB); 2026-03-15 win vs Jamahl Tatum (KO/TKO); 2025-11-21 win vs Miles Banks (KO/TKO)
- independent model votes for Anthony Wint: logistic 62.9%, calibrated GBM 77.4%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Anthony Wint | Lucas Armand |
|---|---:|---:|
| Age | 31.05 | 30.94 |
| Reach (cm) | unavailable | unavailable |
| UFC fights | 1.00 | 0.00 |
| Days since UFC fight | 42.00 | unavailable |
| Last 3: sig. strikes landed/min | 1.12 | unavailable |
| Last 3: sig. strikes absorbed/min | 0.22 | unavailable |
| Last 5: takedowns/15 min | 3.35 | unavailable |
| Last 5: takedown defense (fraction) | unavailable | unavailable |
| Last 5: control-time fraction | 0.60 | unavailable |
| Last 5: opponent pre-fight Elo | 1500.00 | unavailable |

- skill-only research model P(Anthony Wint) = 0.731; vig-free market = 0.813 (gap -0.082). Market shown for comparison only.
- method: Anthony Wint by KO 20% / sub 27% / dec 26%; Lucas Armand by KO 11% / sub 5% / dec 11%
- pick outcome: Anthony Wint by submission, round 1 (method 27%; round given method 59%; exact outcome 16%)
- how it ends: finish 63% (R1 38% / R2 18% / R3 8%) vs. decision 37%
- likeliest endings: Anthony Wint by decision (26%), Anthony Wint by submission, round 1 (16%), Anthony Wint by KO/TKO, round 1 (12%)
- drivers (log-odds): diff_strike_elo +0.17, f2_reach_cm +0.14, diff_wins +0.09, f1_reach_cm +0.08, f1_pre_ufc_ko_rate +0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Anthony Wint by KO/TKO | 12.3% | 5.6% | 2.3% | **20.2%** |
| Anthony Wint by submission | 15.9% | 7.8% | 3.4% | **27.0%** |
| Lucas Armand by KO/TKO | 7.0% | 3.0% | 1.2% | **11.2%** |
| Lucas Armand by submission | 3.0% | 1.4% | 0.6% | **5.0%** |
| decision (either fighter) | — | — | — | **36.6%** |

## Johnny Walker vs. Mick Parkin — Heavyweight
P(Johnny Walker wins) = 0.551  ->  pick: Johnny Walker (55%; close fight)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Mick Parkin holds the pre-fight-expectation-adjusted form edge (mixed vs hot over the last 5).
- research: Style record: Johnny Walker is 53% against strikers in the UFC.
- recent fights, Johnny Walker: 2026-04-11 loss vs Dominick Reyes (S-DEC); 2025-08-23 win vs Zhang Mingyang (KO/TKO); 2024-06-22 loss vs Volkan Oezdemir (KO/TKO)
- recent fights, Mick Parkin: 2025-03-22 loss vs Marcin Tybura (U-DEC); 2024-07-27 win vs Lukasz Brzeski (KO/TKO); 2024-03-23 win vs Mohammed Usman (U-DEC)
- independent model votes for Johnny Walker: logistic 60.1%, calibrated GBM 53.0%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Johnny Walker | Mick Parkin |
|---|---:|---:|
| Age | 34.51 | 31.00 |
| Reach (cm) | 208.28 | 200.66 |
| UFC fights | 16.00 | 5.00 |
| Days since UFC fight | 175.00 | 560.00 |
| Last 3: sig. strikes landed/min | 4.27 | 4.97 |
| Last 3: sig. strikes absorbed/min | 3.63 | 4.25 |
| Last 5: takedowns/15 min | 0.00 | 0.95 |
| Last 5: takedown defense (fraction) | 0.00 | 0.75 |
| Last 5: control-time fraction | 0.04 | 0.16 |
| Last 5: opponent pre-fight Elo | 1699.35 | 1555.00 |

- method: Johnny Walker by KO 29% / sub 4% / dec 23%; Mick Parkin by KO 25% / sub 3% / dec 17%
- pick outcome: Johnny Walker by KO/TKO, round 1 (method 29%; round given method 50%; exact outcome 14%)
- how it ends: finish 60% (R1 31% / R2 19% / R3 9%) vs. decision 40%
- likeliest endings: Johnny Walker by decision (23%), Mick Parkin by decision (17%), Johnny Walker by KO/TKO, round 1 (14%)
- drivers (log-odds): diff_strike_elo +0.33, diff_opp_elo_l5 +0.17, diff_age -0.15, f2_quality_win_rate +0.08, diff_n_fights -0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Johnny Walker by KO/TKO | 14.4% | 9.3% | 5.0% | **28.7%** |
| Johnny Walker by submission | 1.8% | 1.2% | 0.7% | **3.7%** |
| Mick Parkin by KO/TKO | 13.7% | 7.9% | 3.4% | **24.9%** |
| Mick Parkin by submission | 1.4% | 0.9% | 0.4% | **2.6%** |
| decision (either fighter) | — | — | — | **40.1%** |

## Jacobe Smith vs. Bruce Whitehead — Welterweight
P(Jacobe Smith wins) = 0.812  ->  pick: Jacobe Smith (81%)
- CAUTION: no UFC history for Bruce Whitehead (debut or misspelled name?) — prediction is weak.
- research: Last fights: Jacobe Smith won last time out.
- recent fights, Jacobe Smith: 2026-02-21 win vs Josiah Harrell (KO/TKO); 2025-06-28 win vs Niko Price (SUB); 2025-01-11 win vs Preston Parsons (KO/TKO)
- independent model votes for Jacobe Smith: logistic 77.7%, calibrated GBM 82.8%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Jacobe Smith | Bruce Whitehead |
|---|---:|---:|
| Age | 30.71 | unavailable |
| Reach (cm) | 182.88 | unavailable |
| UFC fights | 3.00 | 0.00 |
| Days since UFC fight | 224.00 | unavailable |
| Last 3: sig. strikes landed/min | 6.85 | unavailable |
| Last 3: sig. strikes absorbed/min | 3.61 | unavailable |
| Last 5: takedowns/15 min | 4.52 | unavailable |
| Last 5: takedown defense (fraction) | 1.00 | unavailable |
| Last 5: control-time fraction | 0.47 | unavailable |
| Last 5: opponent pre-fight Elo | 1505.07 | unavailable |

- skill-only research model P(Jacobe Smith) = 0.812; vig-free market = 0.887 (gap -0.075). Market shown for comparison only.
- method: Jacobe Smith by KO 38% / sub 20% / dec 24%; Bruce Whitehead by KO 10% / sub 3% / dec 5%
- pick outcome: Jacobe Smith by KO/TKO, round 1 (method 38%; round given method 68%; exact outcome 26%)
- how it ends: finish 71% (R1 48% / R2 16% / R3 7%) vs. decision 29%
- likeliest endings: Jacobe Smith by KO/TKO, round 1 (26%), Jacobe Smith by decision (24%), Jacobe Smith by submission, round 1 (13%)
- drivers (log-odds): f2_reach_cm +0.40, f1_reach_cm +0.33, diff_strike_elo +0.29, diff_height_cm -0.19, f1_age_past_prime +0.10

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Jacobe Smith by KO/TKO | 26.0% | 8.6% | 3.4% | **38.0%** |
| Jacobe Smith by submission | 13.0% | 4.7% | 1.9% | **19.6%** |
| Bruce Whitehead by KO/TKO | 7.2% | 2.3% | 0.9% | **10.4%** |
| Bruce Whitehead by submission | 2.2% | 0.8% | 0.3% | **3.3%** |
| decision (either fighter) | — | — | — | **28.8%** |

## Rafael Dos Anjos vs. Alexander Hernandez — Lightweight
P(Rafael Dos Anjos wins) = 0.374  ->  pick: Alexander Hernandez (63%)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Alexander Hernandez holds the pre-fight-expectation-adjusted form edge (cold vs hot over the last 5).
- research: Style record: Rafael Dos Anjos is 57% against strikers in the UFC.
- research: Common opponents (2): Rafael Dos Anjos's record against them is better.
- recent fights, Rafael Dos Anjos: 2024-10-26 loss vs Geoff Neal (KO/TKO); 2024-03-09 loss vs Mateusz Gamrot (U-DEC); 2023-08-12 loss vs Vicente Luque (U-DEC)
- recent fights, Alexander Hernandez: 2026-04-25 loss vs Rafa Garcia (U-DEC); 2025-09-13 win vs Diego Ferreira (KO/TKO); 2025-08-16 win vs Chase Hooper (KO/TKO)
- independent model votes for Rafael Dos Anjos: logistic 33.5%, calibrated GBM 39.1%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Rafael Dos Anjos | Alexander Hernandez |
|---|---:|---:|
| Age | 41.94 | 34.00 |
| Reach (cm) | 177.80 | 182.88 |
| UFC fights | 36.00 | 18.00 |
| Days since UFC fight | 707.00 | 161.00 |
| Last 3: sig. strikes landed/min | 2.55 | 3.38 |
| Last 3: sig. strikes absorbed/min | 3.54 | 3.55 |
| Last 5: takedowns/15 min | 1.71 | 1.02 |
| Last 5: takedown defense (fraction) | 0.38 | 0.81 |
| Last 5: control-time fraction | 0.24 | 0.13 |
| Last 5: opponent pre-fight Elo | 1688.60 | 1578.29 |

- skill-only research model P(Rafael Dos Anjos) = 0.374; vig-free market = 0.300 (gap +0.074). Market shown for comparison only.
- method: Rafael Dos Anjos by KO 11% / sub 9% / dec 17%; Alexander Hernandez by KO 26% / sub 5% / dec 31%
- pick outcome: Alexander Hernandez by decision (31%)
- how it ends: finish 51% (R1 25% / R2 17% / R3 9%) vs. decision 49%
- likeliest endings: Alexander Hernandez by decision (31%), Rafael Dos Anjos by decision (17%), Alexander Hernandez by KO/TKO, round 1 (14%)
- drivers (log-odds): diff_age -0.22, diff_strike_elo -0.17, diff_opp_elo_l5 +0.12, diff_career_fights_24m -0.07, diff_sig_acc_l5 +0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Rafael Dos Anjos by KO/TKO | 4.9% | 3.7% | 2.1% | **10.6%** |
| Rafael Dos Anjos by submission | 4.1% | 3.3% | 2.0% | **9.4%** |
| Alexander Hernandez by KO/TKO | 13.6% | 8.3% | 4.5% | **26.4%** |
| Alexander Hernandez by submission | 2.4% | 1.6% | 0.9% | **4.8%** |
| decision (either fighter) | — | — | — | **48.8%** |

## Marvin Vettori vs. Ismail Naurdiev — Middleweight
P(Marvin Vettori wins) = 0.392  ->  pick: Ismail Naurdiev (61%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Marvin Vettori is the volume striker (6.0 vs 4.1 SLpM).
- research: Form: Ismail Naurdiev holds the pre-fight-expectation-adjusted form edge (cold vs hot over the last 5).
- research: Style record: Marvin Vettori is 53% against strikers in the UFC.
- recent fights, Marvin Vettori: 2025-12-06 loss vs Brunno Ferreira (U-DEC); 2025-07-19 loss vs Brendan Allen (U-DEC); 2025-03-15 loss vs Roman Dolidze (U-DEC)
- recent fights, Ismail Naurdiev: 2025-11-22 win vs Ryan Loder (KO/TKO); 2025-06-21 loss vs JunYong Park (U-DEC); 2024-10-26 win vs Bruno Silva (U-DEC)
- independent model votes for Marvin Vettori: logistic 39.4%, calibrated GBM 39.1%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Marvin Vettori | Ismail Naurdiev |
|---|---:|---:|
| Age | 33.03 | 30.12 |
| Reach (cm) | 187.96 | 187.96 |
| UFC fights | 18.00 | 7.00 |
| Days since UFC fight | 301.00 | 315.00 |
| Last 3: sig. strikes landed/min | 5.60 | 4.61 |
| Last 3: sig. strikes absorbed/min | 5.98 | 2.61 |
| Last 5: takedowns/15 min | 0.32 | 1.71 |
| Last 5: takedown defense (fraction) | 0.58 | 0.70 |
| Last 5: control-time fraction | 0.03 | 0.22 |
| Last 5: opponent pre-fight Elo | 1690.30 | 1561.43 |

- skill-only research model P(Marvin Vettori) = 0.392; vig-free market = 0.438 (gap -0.046). Market shown for comparison only.
- method: Marvin Vettori by KO 9% / sub 4% / dec 26%; Ismail Naurdiev by KO 17% / sub 5% / dec 39%
- pick outcome: Ismail Naurdiev by decision (39%)
- how it ends: finish 35% (R1 17% / R2 11% / R3 7%) vs. decision 65%
- likeliest endings: Ismail Naurdiev by decision (39%), Marvin Vettori by decision (26%), Ismail Naurdiev by KO/TKO, round 1 (9%)
- drivers (log-odds): diff_strike_elo -0.20, diff_age -0.17, diff_opp_elo_l5 +0.13, diff_career_win_pct -0.07, diff_quality_win_rate +0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Marvin Vettori by KO/TKO | 4.5% | 3.1% | 1.9% | **9.5%** |
| Marvin Vettori by submission | 1.8% | 1.4% | 0.9% | **4.1%** |
| Ismail Naurdiev by KO/TKO | 8.5% | 5.4% | 3.0% | **16.8%** |
| Ismail Naurdiev by submission | 2.3% | 1.6% | 0.9% | **4.8%** |
| decision (either fighter) | — | — | — | **64.8%** |

## Court McGee vs. Eric Nolan — Welterweight
P(Court McGee wins) = 0.458  ->  pick: Eric Nolan (54%; close fight)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Court McGee holds the pre-fight-expectation-adjusted form edge (cold vs cold over the last 5).
- research: Style record: Court McGee is 48% against strikers in the UFC.
- recent fights, Court McGee: 2025-06-14 loss vs Michael Chiesa (U-DEC); 2024-10-05 win vs Tim Means (SUB); 2024-04-06 loss vs Alex Morono (U-DEC)
- recent fights, Eric Nolan: 2026-06-27 loss vs Farman Hasanov (U-DEC); 2025-08-16 loss vs Baisangur Susurkaev (SUB)
- independent model votes for Court McGee: logistic 35.9%, calibrated GBM 50.0%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Court McGee | Eric Nolan |
|---|---:|---:|
| Age | 41.81 | 29.05 |
| Reach (cm) | 190.50 | 187.96 |
| UFC fights | 24.00 | 2.00 |
| Days since UFC fight | 476.00 | 98.00 |
| Last 3: sig. strikes landed/min | 3.39 | 1.68 |
| Last 3: sig. strikes absorbed/min | 3.45 | 2.59 |
| Last 5: takedowns/15 min | 1.15 | 0.00 |
| Last 5: takedown defense (fraction) | 1.00 | 0.44 |
| Last 5: control-time fraction | 0.20 | 0.02 |
| Last 5: opponent pre-fight Elo | 1603.77 | 1500.00 |

- skill-only research model P(Court McGee) = 0.458; vig-free market = 0.332 (gap +0.126). Market shown for comparison only.
- method: Court McGee by KO 8% / sub 13% / dec 25%; Eric Nolan by KO 21% / sub 5% / dec 28%
- pick outcome: Eric Nolan by decision (28%)
- how it ends: finish 46% (R1 25% / R2 14% / R3 7%) vs. decision 54%
- likeliest endings: Eric Nolan by decision (28%), Court McGee by decision (25%), Eric Nolan by KO/TKO, round 1 (13%)
- drivers (log-odds): diff_age -0.35, diff_strike_elo +0.31, diff_opp_elo_l5 +0.08, diff_age_past_prime -0.08, f2_age_past_prime -0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Court McGee by KO/TKO | 4.0% | 2.5% | 1.2% | **7.8%** |
| Court McGee by submission | 6.3% | 4.3% | 2.1% | **12.7%** |
| Eric Nolan by KO/TKO | 12.5% | 6.0% | 2.7% | **21.2%** |
| Eric Nolan by submission | 2.6% | 1.3% | 0.6% | **4.5%** |
| decision (either fighter) | — | — | — | **53.8%** |

---
*Simulation/educational project. No betting advice. The market knows more than this model.*