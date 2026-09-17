# UFC 331: Van vs. Pantoja 2 — 2026-09-19

Point-in-time predictions from 8731 historical fights. Educational output — NOT betting advice; the backtest shows this model does not beat the market.

Prediction mode: **skill_only**. Odds, ranking nudges and social sentiment do not change these probabilities.
Historical results available through 2026-09-12.

## Joshua Van vs. Alexandre Pantoja — Flyweight
P(Joshua Van wins) = 0.678  ->  pick: Joshua Van (68%)
- research: Wrestling contrast: Alexandre Pantoja lands 5.0 takedowns/15 into Joshua Van's 73% TDD.
- research: Form: Joshua Van holds the pre-fight-expectation-adjusted form edge (hot vs mixed over the last 5).
- research: Style record: Alexandre Pantoja is 71% against strikers in the UFC.
- research: Rematch: they have met 1 time previously; Joshua Van won the last one 287 days ago.
- research: Common opponents: 1 shared names on the record.
- recent fights, Joshua Van: 2026-05-09 win vs Tatsuro Taira (KO/TKO); 2025-12-06 win vs Alexandre Pantoja (KO/TKO); 2025-06-28 win vs Brandon Royval (U-DEC)
- recent fights, Alexandre Pantoja: 2025-12-06 loss vs Joshua Van (KO/TKO); 2025-06-28 win vs Kai Kara-France (SUB); 2024-12-07 win vs Kai Asakura (SUB)
- independent model votes for Joshua Van: logistic 66.3%, calibrated GBM 68.5%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Joshua Van | Alexandre Pantoja |
|---|---:|---:|
| Age | 24.94 | 36.43 |
| Reach (cm) | 165.10 | 170.18 |
| UFC fights | 11.00 | 18.00 |
| Days since UFC fight | 133.00 | 287.00 |
| Last 3: sig. strikes landed/min | 9.12 | 4.12 |
| Last 3: sig. strikes absorbed/min | 7.47 | 2.93 |
| Last 5: takedowns/15 min | 0.23 | 4.97 |
| Last 5: takedown defense (fraction) | 0.73 | 0.89 |
| Last 5: control-time fraction | 0.05 | 0.49 |
| Last 5: opponent pre-fight Elo | 1651.69 | 1622.62 |

- skill-only research model P(Joshua Van) = 0.678; vig-free market = 0.550 (gap +0.128). Market shown for comparison only.
- method: Joshua Van by KO 29% / sub 7% / dec 32%; Alexandre Pantoja by KO 6% / sub 8% / dec 17%
- pick outcome: Joshua Van by decision (32%)
- how it ends: finish 51% (R1 18% / R2 14% / R3 9% / R4 5% / R5 4%) vs. decision 49%
- likeliest endings: Joshua Van by decision (32%), Alexandre Pantoja by decision (17%), Joshua Van by KO/TKO, round 1 (11%)
- drivers (log-odds): diff_age +0.41, diff_strike_elo -0.16, diff_career_win_pct +0.11, diff_age_past_prime +0.08, diff_td15_l5 -0.07

| ending | R1 | R2 | R3 | R4 | R5 | any round |
|---|---|---|---|---|---|---|
| Joshua Van by KO/TKO | 10.8% | 8.1% | 5.0% | 2.7% | 2.7% | **29.3%** |
| Joshua Van by submission | 2.2% | 1.9% | 1.4% | 0.8% | 0.6% | **6.9%** |
| Alexandre Pantoja by KO/TKO | 2.3% | 1.9% | 1.1% | 0.6% | 0.5% | **6.4%** |
| Alexandre Pantoja by submission | 2.6% | 2.5% | 1.7% | 0.9% | 0.7% | **8.4%** |
| decision (either fighter) | — | — | — | — | — | **49.1%** |

## Arman Tsarukyan vs. Mauricio Ruffy — Lightweight
P(Arman Tsarukyan wins) = 0.752  ->  pick: Arman Tsarukyan (75%)
- research: Wrestling contrast: Arman Tsarukyan lands 4.2 takedowns/15 into Mauricio Ruffy's 85% TDD.
- research: Form: Arman Tsarukyan holds the pre-fight-expectation-adjusted form edge (hot vs hot over the last 5).
- research: Style record: Arman Tsarukyan is 83% against strikers in the UFC.
- recent fights, Arman Tsarukyan: 2025-11-22 win vs Dan Hooker (SUB); 2024-04-13 win vs Charles Oliveira (S-DEC); 2023-12-02 win vs Beneil Dariush (KO/TKO)
- recent fights, Mauricio Ruffy: 2026-06-14 win vs Michael Chandler (KO/TKO); 2026-01-31 win vs Rafael Fiziev (KO/TKO); 2025-09-06 loss vs Benoit Saint Denis (SUB)
- independent model votes for Arman Tsarukyan: logistic 70.0%, calibrated GBM 77.4%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Arman Tsarukyan | Mauricio Ruffy |
|---|---:|---:|
| Age | 29.94 | 30.26 |
| Reach (cm) | 182.88 | 190.50 |
| UFC fights | 12.00 | 6.00 |
| Days since UFC fight | 301.00 | 97.00 |
| Last 3: sig. strikes landed/min | 4.02 | 3.60 |
| Last 3: sig. strikes absorbed/min | 1.26 | 2.56 |
| Last 5: takedowns/15 min | 4.24 | 0.00 |
| Last 5: takedown defense (fraction) | unavailable | 0.85 |
| Last 5: control-time fraction | 0.63 | 0.05 |
| Last 5: opponent pre-fight Elo | 1743.24 | 1582.80 |

- skill-only research model P(Arman Tsarukyan) = 0.752; vig-free market = 0.739 (gap +0.013). Market shown for comparison only.
- method: Arman Tsarukyan by KO 28% / sub 14% / dec 33%; Mauricio Ruffy by KO 15% / sub 2% / dec 8%
- pick outcome: Arman Tsarukyan by decision (33%)
- how it ends: finish 59% (R1 21% / R2 18% / R3 11% / R4 6% / R5 4%) vs. decision 41%
- likeliest endings: Arman Tsarukyan by decision (33%), Arman Tsarukyan by KO/TKO, round 1 (10%), Arman Tsarukyan by KO/TKO, round 2 (9%)
- drivers (log-odds): diff_strike_elo +0.37, diff_opp_elo_l5 +0.20, diff_elo +0.17, diff_td15_l5 +0.11, diff_age +0.08

| ending | R1 | R2 | R3 | R4 | R5 | any round |
|---|---|---|---|---|---|---|
| Arman Tsarukyan by KO/TKO | 10.0% | 9.0% | 5.0% | 2.5% | 2.0% | **28.5%** |
| Arman Tsarukyan by submission | 4.1% | 4.3% | 2.8% | 1.5% | 1.0% | **13.8%** |
| Mauricio Ruffy by KO/TKO | 5.9% | 4.5% | 2.5% | 1.4% | 1.2% | **15.5%** |
| Mauricio Ruffy by submission | 0.6% | 0.5% | 0.3% | 0.2% | 0.1% | **1.7%** |
| decision (either fighter) | — | — | — | — | — | **40.5%** |

## Patricio Freire vs. Dooho Choi — Featherweight
P(Patricio Freire wins) = 0.373  ->  pick: Dooho Choi (63%)
- research: Wrestling contrast: Patricio Freire lands 3.0 takedowns/15 into Dooho Choi's 63% TDD.
- research: Form: Patricio Freire holds the pre-fight-expectation-adjusted form edge (hot vs mixed over the last 5).
- recent fights, Patricio Freire: 2025-07-19 win vs Dan Ige (U-DEC); 2025-04-12 loss vs Yair Rodriguez (U-DEC); 2024-03-22 win vs Jeremy Kennedy (KO/TKO)
- recent fights, Dooho Choi: 2026-05-16 win vs Daniel Santos (KO/TKO); 2024-12-07 win vs Nate Landwehr (KO/TKO); 2024-07-20 win vs Bill Algeo (KO/TKO)
- independent model votes for Patricio Freire: logistic 38.7%, calibrated GBM 36.7%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Patricio Freire | Dooho Choi |
|---|---:|---:|
| Age | 39.20 | 35.44 |
| Reach (cm) | 170.18 | 177.80 |
| UFC fights | 2.00 | 10.00 |
| Days since UFC fight | 427.00 | 126.00 |
| Last 3: sig. strikes landed/min | 2.40 | 5.43 |
| Last 3: sig. strikes absorbed/min | 3.90 | 3.62 |
| Last 5: takedowns/15 min | 3.00 | 1.61 |
| Last 5: takedown defense (fraction) | 0.00 | 0.63 |
| Last 5: control-time fraction | 0.13 | 0.25 |
| Last 5: opponent pre-fight Elo | 1684.19 | 1530.63 |

- method: Patricio Freire by KO 10% / sub 11% / dec 16%; Dooho Choi by KO 28% / sub 6% / dec 29%
- pick outcome: Dooho Choi by decision (29%)
- how it ends: finish 54% (R1 28% / R2 17% / R3 9%) vs. decision 46%
- likeliest endings: Dooho Choi by decision (29%), Patricio Freire by decision (16%), Dooho Choi by KO/TKO, round 1 (14%)
- drivers (log-odds): diff_strike_elo -0.23, diff_age -0.15, diff_opp_elo_l5 +0.11, diff_elo -0.08, f2_pre_ufc_elo +0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Patricio Freire by KO/TKO | 5.2% | 3.1% | 1.5% | **9.7%** |
| Patricio Freire by submission | 5.7% | 3.7% | 1.8% | **11.3%** |
| Dooho Choi by KO/TKO | 14.2% | 8.5% | 5.0% | **27.7%** |
| Dooho Choi by submission | 2.8% | 1.8% | 1.1% | **5.7%** |
| decision (either fighter) | — | — | — | **45.6%** |

## Gable Steveson vs. Sean Sharaf — Heavyweight
P(Gable Steveson wins) = 0.712  ->  pick: Gable Steveson (71%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Gable Steveson is the volume striker (16.3 vs 7.4 SLpM).
- research: Form: Gable Steveson holds the pre-fight-expectation-adjusted form edge (hot vs cold over the last 5).
- recent fights, Gable Steveson: 2026-07-11 win vs Elisha Ellison (KO/TKO); 2026-02-19 win vs Hugo Lezama (KO/TKO); 2025-11-23 win vs Kevin Hein (KO/TKO)
- recent fights, Sean Sharaf: 2025-12-13 loss vs Steven Asplund (KO/TKO); 2024-10-12 loss vs Junior Tafa (KO/TKO); 2024-09-06 win vs L.J. Torres (KO/TKO)
- independent model votes for Gable Steveson: logistic 89.7%, calibrated GBM 63.3%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Gable Steveson | Sean Sharaf |
|---|---:|---:|
| Age | 26.30 | 33.19 |
| Reach (cm) | unavailable | 195.58 |
| UFC fights | 1.00 | 2.00 |
| Days since UFC fight | 70.00 | 280.00 |
| Last 3: sig. strikes landed/min | 16.29 | 7.41 |
| Last 3: sig. strikes absorbed/min | 5.17 | 15.00 |
| Last 5: takedowns/15 min | 0.00 | 0.93 |
| Last 5: takedown defense (fraction) | unavailable | unavailable |
| Last 5: control-time fraction | 0.07 | 0.05 |
| Last 5: opponent pre-fight Elo | 1460.00 | 1468.61 |

- skill-only research model P(Gable Steveson) = 0.712; vig-free market = 0.919 (gap -0.207). Market shown for comparison only.
- method: Gable Steveson by KO 50% / sub 6% / dec 16%; Sean Sharaf by KO 14% / sub 5% / dec 10%
- pick outcome: Gable Steveson by KO/TKO, round 1 (method 50%; round given method 63%; exact outcome 31%)
- how it ends: finish 74% (R1 46% / R2 20% / R3 8%) vs. decision 26%
- likeliest endings: Gable Steveson by KO/TKO, round 1 (31%), Gable Steveson by decision (16%), Gable Steveson by KO/TKO, round 2 (13%)
- drivers (log-odds): f2_reach_cm -0.38, diff_strike_elo +0.34, f1_reach_cm -0.24, diff_age +0.18, diff_height_cm +0.18

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Gable Steveson by KO/TKO | 31.1% | 13.1% | 5.5% | **49.7%** |
| Gable Steveson by submission | 3.4% | 1.5% | 0.7% | **5.6%** |
| Sean Sharaf by KO/TKO | 8.4% | 4.0% | 1.6% | **14.0%** |
| Sean Sharaf by submission | 2.8% | 1.5% | 0.6% | **4.9%** |
| decision (either fighter) | — | — | — | **25.7%** |

## Alonzo Menifield vs. Iwo Baraniewski — Light Heavyweight
P(Alonzo Menifield wins) = 0.232  ->  pick: Iwo Baraniewski (77%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Iwo Baraniewski is the volume striker (11.3 vs 3.7 SLpM).
- research: Form: Iwo Baraniewski holds the pre-fight-expectation-adjusted form edge (mixed vs hot over the last 5).
- research: Style record: Alonzo Menifield is 50% against strikers in the UFC.
- recent fights, Alonzo Menifield: 2026-05-30 win vs Zhang Mingyang (KO/TKO); 2025-11-22 loss vs Volkan Oezdemir (KO/TKO); 2025-06-14 win vs Oumar Sy (U-DEC)
- recent fights, Iwo Baraniewski: 2026-06-06 win vs Junior Tafa (KO/TKO); 2026-03-21 win vs Austen Lane (KO/TKO); 2025-12-06 win vs Ibo Aslan (KO/TKO)
- independent model votes for Alonzo Menifield: logistic 24.5%, calibrated GBM 22.6%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Alonzo Menifield | Iwo Baraniewski |
|---|---:|---:|
| Age | 38.92 | 27.83 |
| Reach (cm) | 193.04 | 185.42 |
| UFC fights | 18.00 | 3.00 |
| Days since UFC fight | 112.00 | 105.00 |
| Last 3: sig. strikes landed/min | 2.85 | 11.29 |
| Last 3: sig. strikes absorbed/min | 3.04 | 8.91 |
| Last 5: takedowns/15 min | 0.00 | 0.00 |
| Last 5: takedown defense (fraction) | 0.87 | 1.00 |
| Last 5: control-time fraction | 0.08 | 0.16 |
| Last 5: opponent pre-fight Elo | 1579.51 | 1446.15 |

- skill-only research model P(Alonzo Menifield) = 0.232; vig-free market = 0.318 (gap -0.086). Market shown for comparison only.
- method: Alonzo Menifield by KO 13% / sub 2% / dec 8%; Iwo Baraniewski by KO 51% / sub 8% / dec 18%
- pick outcome: Iwo Baraniewski by KO/TKO, round 1 (method 51%; round given method 66%; exact outcome 34%)
- how it ends: finish 74% (R1 47% / R2 19% / R3 8%) vs. decision 26%
- likeliest endings: Iwo Baraniewski by KO/TKO, round 1 (34%), Iwo Baraniewski by decision (18%), Iwo Baraniewski by KO/TKO, round 2 (12%)
- drivers (log-odds): diff_age -0.41, diff_strike_elo -0.20, diff_elo +0.08, f2_age_past_prime -0.07, diff_career_win_pct -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Alonzo Menifield by KO/TKO | 7.6% | 3.9% | 1.6% | **13.1%** |
| Alonzo Menifield by submission | 1.0% | 0.5% | 0.2% | **1.7%** |
| Iwo Baraniewski by KO/TKO | 33.7% | 12.5% | 5.2% | **51.4%** |
| Iwo Baraniewski by submission | 4.8% | 2.0% | 0.9% | **7.6%** |
| decision (either fighter) | — | — | — | **26.2%** |

## Marlon Vera vs. Charles Jourdain — Bantamweight
P(Marlon Vera wins) = 0.296  ->  pick: Charles Jourdain (70%)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Charles Jourdain holds the pre-fight-expectation-adjusted form edge (cold vs hot over the last 5).
- research: Style record: Marlon Vera is 55% against strikers in the UFC.
- research: Common opponents (2): Charles Jourdain's record against them is better.
- recent fights, Marlon Vera: 2026-02-28 loss vs David Martinez (U-DEC); 2025-10-18 loss vs Aiemann Zahabi (S-DEC); 2024-08-03 loss vs Deiveson Figueiredo (U-DEC)
- recent fights, Charles Jourdain: 2026-04-18 win vs Kyler Phillips (U-DEC); 2025-10-18 win vs Davey Grant (SUB); 2024-11-02 win vs Victor Henry (SUB)
- independent model votes for Marlon Vera: logistic 25.1%, calibrated GBM 31.5%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Marlon Vera | Charles Jourdain |
|---|---:|---:|
| Age | 33.80 | 30.81 |
| Reach (cm) | 177.80 | 175.26 |
| UFC fights | 26.00 | 17.00 |
| Days since UFC fight | 203.00 | 154.00 |
| Last 3: sig. strikes landed/min | 3.33 | 4.55 |
| Last 3: sig. strikes absorbed/min | 4.38 | 2.57 |
| Last 5: takedowns/15 min | 0.00 | 1.25 |
| Last 5: takedown defense (fraction) | 0.79 | 0.45 |
| Last 5: control-time fraction | 0.00 | 0.09 |
| Last 5: opponent pre-fight Elo | 1711.53 | 1589.29 |

- skill-only research model P(Marlon Vera) = 0.296; vig-free market = 0.338 (gap -0.042). Market shown for comparison only.
- method: Marlon Vera by KO 8% / sub 3% / dec 19%; Charles Jourdain by KO 17% / sub 7% / dec 47%
- pick outcome: Charles Jourdain by decision (47%)
- how it ends: finish 34% (R1 16% / R2 11% / R3 7%) vs. decision 66%
- likeliest endings: Charles Jourdain by decision (47%), Marlon Vera by decision (19%), Charles Jourdain by KO/TKO, round 1 (8%)
- drivers (log-odds): diff_strike_elo -0.32, diff_age -0.14, diff_opp_elo_l5 +0.11, diff_career_win_pct -0.07, diff_quality_win_rate +0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Marlon Vera by KO/TKO | 3.6% | 2.4% | 1.5% | **7.5%** |
| Marlon Vera by submission | 1.2% | 0.9% | 0.5% | **2.6%** |
| Charles Jourdain by KO/TKO | 8.1% | 5.3% | 3.3% | **16.7%** |
| Charles Jourdain by submission | 3.2% | 2.3% | 1.4% | **7.0%** |
| decision (either fighter) | — | — | — | **66.1%** |

## Tai Tuivasa vs. Robelis Despaigne — Heavyweight
P(Tai Tuivasa wins) = 0.418  ->  pick: Robelis Despaigne (58%)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Robelis Despaigne holds the pre-fight-expectation-adjusted form edge (cold vs cold over the last 5).
- research: Style record: Tai Tuivasa is 41% against strikers in the UFC.
- recent fights, Tai Tuivasa: 2026-05-02 loss vs Louie Sutherland (U-DEC); 2026-01-31 loss vs Tallison Teixeira (U-DEC); 2024-08-17 loss vs Jairzinho Rozenstruik (S-DEC)
- recent fights, Robelis Despaigne: 2026-05-16 win vs Junior dos Santos (KO/TKO); 2024-10-19 loss vs Austen Lane (U-DEC); 2024-05-11 loss vs Waldo Cortes Acosta (U-DEC)
- independent model votes for Tai Tuivasa: logistic 41.0%, calibrated GBM 42.2%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Tai Tuivasa | Robelis Despaigne |
|---|---:|---:|
| Age | 33.51 | 38.03 |
| Reach (cm) | 190.50 | 213.36 |
| UFC fights | 18.00 | 3.00 |
| Days since UFC fight | 140.00 | 700.00 |
| Last 3: sig. strikes landed/min | 2.04 | 2.11 |
| Last 3: sig. strikes absorbed/min | 3.62 | 2.54 |
| Last 5: takedowns/15 min | 0.00 | 0.00 |
| Last 5: takedown defense (fraction) | 0.64 | 0.50 |
| Last 5: control-time fraction | 0.08 | 0.01 |
| Last 5: opponent pre-fight Elo | 1602.40 | 1480.02 |

- skill-only research model P(Tai Tuivasa) = 0.418; vig-free market = 0.157 (gap +0.261). Market shown for comparison only.
- method: Tai Tuivasa by KO 21% / sub 4% / dec 17%; Robelis Despaigne by KO 29% / sub 4% / dec 25%
- pick outcome: Robelis Despaigne by KO/TKO, round 1 (method 29%; round given method 58%; exact outcome 17%)
- how it ends: finish 59% (R1 33% / R2 18% / R3 8%) vs. decision 41%
- likeliest endings: Robelis Despaigne by decision (25%), Robelis Despaigne by KO/TKO, round 1 (17%), Tai Tuivasa by decision (17%)
- drivers (log-odds): diff_style_reach_striker -0.27, diff_strike_elo -0.23, diff_age +0.15, diff_opp_elo_l5 +0.14, diff_reach_cm -0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Tai Tuivasa by KO/TKO | 11.1% | 6.8% | 3.1% | **21.0%** |
| Tai Tuivasa by submission | 2.2% | 1.4% | 0.7% | **4.3%** |
| Robelis Despaigne by KO/TKO | 17.1% | 8.7% | 3.5% | **29.2%** |
| Robelis Despaigne by submission | 2.3% | 1.3% | 0.5% | **4.1%** |
| decision (either fighter) | — | — | — | **41.5%** |

## Michael Aswell vs. JooSang Yoo — Featherweight
P(Michael Aswell wins) = 0.496  ->  pick: JooSang Yoo (50%; close fight)
- CAUTION: no UFC history for Michael Aswell (debut or misspelled name?) — prediction is weak.
- research: Last fights: JooSang Yoo lost last time out.
- recent fights, JooSang Yoo: 2025-10-04 loss vs Daniel Santos (KO/TKO); 2025-06-07 win vs Jeka Saragih (KO/TKO)
- independent model votes for Michael Aswell: logistic 48.8%, calibrated GBM 50.0%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Michael Aswell | JooSang Yoo |
|---|---:|---:|
| Age | 25.98 | 32.66 |
| Reach (cm) | 175.26 | 180.34 |
| UFC fights | 0.00 | 2.00 |
| Days since UFC fight | unavailable | 350.00 |
| Last 3: sig. strikes landed/min | unavailable | 6.36 |
| Last 3: sig. strikes absorbed/min | unavailable | 4.99 |
| Last 5: takedowns/15 min | unavailable | 0.00 |
| Last 5: takedown defense (fraction) | unavailable | 0.50 |
| Last 5: control-time fraction | unavailable | 0.00 |
| Last 5: opponent pre-fight Elo | unavailable | 1523.60 |

- skill-only research model P(Michael Aswell) = 0.496; vig-free market = 0.326 (gap +0.170). Market shown for comparison only.
- method: Michael Aswell by KO 21% / sub 10% / dec 19%; JooSang Yoo by KO 19% / sub 6% / dec 25%
- pick outcome: JooSang Yoo by decision (25%)
- how it ends: finish 56% (R1 32% / R2 16% / R3 7%) vs. decision 44%
- likeliest endings: JooSang Yoo by decision (25%), Michael Aswell by decision (19%), Michael Aswell by KO/TKO, round 1 (12%)
- drivers (log-odds): diff_strike_elo -0.21, diff_age +0.21, f1_clinch_share_l5 -0.03, diff_avg_end_round -0.02, f2_age +0.02

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Michael Aswell by KO/TKO | 12.4% | 5.9% | 2.5% | **20.7%** |
| Michael Aswell by submission | 5.9% | 3.0% | 1.3% | **10.1%** |
| JooSang Yoo by KO/TKO | 10.9% | 5.8% | 2.7% | **19.4%** |
| JooSang Yoo by submission | 3.1% | 1.8% | 0.8% | **5.7%** |
| decision (either fighter) | — | — | — | **44.1%** |

## Ryan Gandra vs. Ozzy Diaz — Middleweight
P(Ryan Gandra wins) = 0.755  ->  pick: Ryan Gandra (75%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Ryan Gandra is the volume striker (12.4 vs 6.4 SLpM).
- research: Form: Ryan Gandra holds the pre-fight-expectation-adjusted form edge (hot vs mixed over the last 5).
- research: Style record: Ryan Gandra is 100% against strikers in the UFC.
- recent fights, Ryan Gandra: 2026-07-11 win vs Zach Reese (KO/TKO); 2026-02-28 win vs Jose Daniel Medina (KO/TKO); 2025-08-26 win vs Trent Miller (KO/TKO)
- recent fights, Ozzy Diaz: 2026-05-09 loss vs Ateba Gautier (KO/TKO); 2025-03-08 win vs Djorden Santos (U-DEC); 2024-11-23 loss vs Zhang Mingyang (KO/TKO)
- independent model votes for Ryan Gandra: logistic 83.1%, calibrated GBM 72.2%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Ryan Gandra | Ozzy Diaz |
|---|---:|---:|
| Age | 31.37 | 35.82 |
| Reach (cm) | 187.96 | 200.66 |
| UFC fights | 2.00 | 3.00 |
| Days since UFC fight | 70.00 | 133.00 |
| Last 3: sig. strikes landed/min | 12.41 | 6.36 |
| Last 3: sig. strikes absorbed/min | 2.59 | 7.25 |
| Last 5: takedowns/15 min | 0.00 | 0.00 |
| Last 5: takedown defense (fraction) | unavailable | 0.67 |
| Last 5: control-time fraction | 0.04 | 0.04 |
| Last 5: opponent pre-fight Elo | 1451.44 | 1555.17 |

- method: Ryan Gandra by KO 52% / sub 6% / dec 18%; Ozzy Diaz by KO 14% / sub 3% / dec 8%
- pick outcome: Ryan Gandra by KO/TKO, round 1 (method 52%; round given method 63%; exact outcome 32%)
- how it ends: finish 74% (R1 44% / R2 20% / R3 9%) vs. decision 26%
- likeliest endings: Ryan Gandra by KO/TKO, round 1 (32%), Ryan Gandra by decision (18%), Ryan Gandra by KO/TKO, round 2 (13%)
- drivers (log-odds): diff_strike_elo +0.29, diff_age +0.16, diff_opp_elo_l5 -0.08, diff_career_win_pct +0.06, f2_reach_cm -0.05

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Ryan Gandra by KO/TKO | 32.3% | 13.5% | 5.8% | **51.5%** |
| Ryan Gandra by submission | 3.4% | 1.5% | 0.7% | **5.6%** |
| Ozzy Diaz by KO/TKO | 7.2% | 4.4% | 2.3% | **13.8%** |
| Ozzy Diaz by submission | 1.3% | 0.9% | 0.5% | **2.6%** |
| decision (either fighter) | — | — | — | **26.4%** |

## Edmen Shahbazyan vs. Brunno Ferreira — Middleweight
P(Edmen Shahbazyan wins) = 0.585  ->  pick: Edmen Shahbazyan (59%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Edmen Shahbazyan is the volume striker (4.9 vs 2.9 SLpM).
- research: Last fights: Edmen Shahbazyan lost last time out; Brunno Ferreira lost last time out.
- research: Style record: Edmen Shahbazyan is 50% against strikers in the UFC.
- recent fights, Edmen Shahbazyan: 2026-06-06 loss vs Brendan Allen (U-DEC); 2025-10-04 win vs Andre Muniz (KO/TKO); 2025-06-14 win vs Andre Petroski (U-DEC)
- recent fights, Brunno Ferreira: 2026-06-27 loss vs Ikram Aliskerov (U-DEC); 2026-03-07 loss vs Gregory Rodrigues (KO/TKO); 2025-12-06 win vs Marvin Vettori (U-DEC)
- independent model votes for Edmen Shahbazyan: logistic 60.3%, calibrated GBM 57.8%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Edmen Shahbazyan | Brunno Ferreira |
|---|---:|---:|
| Age | 28.83 | 33.87 |
| Reach (cm) | 190.50 | 182.88 |
| UFC fights | 15.00 | 10.00 |
| Days since UFC fight | 105.00 | 84.00 |
| Last 3: sig. strikes landed/min | 4.80 | 3.08 |
| Last 3: sig. strikes absorbed/min | 3.95 | 4.31 |
| Last 5: takedowns/15 min | 0.00 | 1.34 |
| Last 5: takedown defense (fraction) | 0.74 | 0.45 |
| Last 5: control-time fraction | 0.08 | 0.06 |
| Last 5: opponent pre-fight Elo | 1612.64 | 1602.84 |

- skill-only research model P(Edmen Shahbazyan) = 0.585; vig-free market = 0.611 (gap -0.026). Market shown for comparison only.
- method: Edmen Shahbazyan by KO 32% / sub 5% / dec 21%; Brunno Ferreira by KO 17% / sub 9% / dec 15%
- pick outcome: Edmen Shahbazyan by KO/TKO, round 1 (method 32%; round given method 60%; exact outcome 19%)
- how it ends: finish 64% (R1 38% / R2 18% / R3 8%) vs. decision 36%
- likeliest endings: Edmen Shahbazyan by decision (21%), Edmen Shahbazyan by KO/TKO, round 1 (19%), Brunno Ferreira by decision (15%)
- drivers (log-odds): diff_strike_elo +0.29, diff_age +0.17, f1_pre_ufc_ko_rate -0.14, f2_pre_ufc_ko_rate -0.08, diff_elo +0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Edmen Shahbazyan by KO/TKO | 19.4% | 9.1% | 3.9% | **32.5%** |
| Edmen Shahbazyan by submission | 3.0% | 1.5% | 0.7% | **5.1%** |
| Brunno Ferreira by KO/TKO | 10.3% | 4.9% | 2.0% | **17.2%** |
| Brunno Ferreira by submission | 5.1% | 2.7% | 1.1% | **8.9%** |
| decision (either fighter) | — | — | — | **36.2%** |

## Casey O'Neill vs. Eduarda Moura — Women's Flyweight
P(Casey O'Neill wins) = 0.583  ->  pick: Casey O'Neill (58%)
- research: Wrestling contrast: Eduarda Moura lands 3.6 takedowns/15 into Casey O'Neill's 71% TDD.
- research: Last fights: Casey O'Neill won last time out; Eduarda Moura lost last time out.
- research: Style record: Eduarda Moura is 50% against strikers in the UFC.
- recent fights, Casey O'Neill: 2026-03-28 win vs Gabriella Fernandes (KO/TKO); 2024-08-17 win vs Luana Santos (U-DEC); 2023-12-16 loss vs Ariane da Silva (SUB)
- recent fights, Eduarda Moura: 2026-02-07 loss vs Wang Cong (U-DEC); 2025-07-12 win vs Lauren Murphy (U-DEC); 2024-11-16 win vs Veronica Hardy (U-DEC)
- independent model votes for Casey O'Neill: logistic 59.4%, calibrated GBM 57.8%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Casey O'Neill | Eduarda Moura |
|---|---:|---:|
| Age | 28.95 | 32.56 |
| Reach (cm) | 175.26 | 170.18 |
| UFC fights | 8.00 | 5.00 |
| Days since UFC fight | 175.00 | 224.00 |
| Last 3: sig. strikes landed/min | 5.68 | 2.27 |
| Last 3: sig. strikes absorbed/min | 4.62 | 2.73 |
| Last 5: takedowns/15 min | 0.00 | 3.57 |
| Last 5: takedown defense (fraction) | 0.71 | 0.80 |
| Last 5: control-time fraction | 0.05 | 0.41 |
| Last 5: opponent pre-fight Elo | 1542.90 | 1544.28 |

- skill-only research model P(Casey O'Neill) = 0.583; vig-free market = 0.666 (gap -0.084). Market shown for comparison only.
- method: Casey O'Neill by KO 11% / sub 7% / dec 40%; Eduarda Moura by KO 6% / sub 8% / dec 27%
- pick outcome: Casey O'Neill by decision (40%)
- how it ends: finish 33% (R1 16% / R2 11% / R3 6%) vs. decision 67%
- likeliest endings: Casey O'Neill by decision (40%), Eduarda Moura by decision (27%), Casey O'Neill by KO/TKO, round 1 (6%)
- drivers (log-odds): diff_strike_elo +0.24, diff_age +0.18, diff_grapple_elo -0.09, diff_td15_l5 -0.08, diff_career_win_pct +0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Casey O'Neill by KO/TKO | 5.8% | 3.6% | 1.9% | **11.2%** |
| Casey O'Neill by submission | 3.3% | 2.3% | 1.2% | **6.9%** |
| Eduarda Moura by KO/TKO | 3.3% | 2.1% | 1.1% | **6.4%** |
| Eduarda Moura by submission | 3.9% | 2.7% | 1.5% | **8.1%** |
| decision (either fighter) | — | — | — | **67.4%** |

## Giga Chikadze vs. Joanderson Brito — Featherweight
P(Giga Chikadze wins) = 0.387  ->  pick: Joanderson Brito (61%)
- research: Wrestling contrast: Joanderson Brito lands 3.1 takedowns/15 into Giga Chikadze's 58% TDD.
- research: Form: Joanderson Brito holds the pre-fight-expectation-adjusted form edge (cold vs mixed over the last 5).
- research: Style record: Joanderson Brito is 57% against strikers in the UFC.
- recent fights, Giga Chikadze: 2025-12-13 loss vs Kevin Vallejos (KO/TKO); 2025-04-26 loss vs David Onama (U-DEC); 2024-07-27 loss vs Arnold Allen (U-DEC)
- recent fights, Joanderson Brito: 2026-06-06 win vs Jordan Leavitt (SUB); 2025-12-13 win vs Isaac Thomson (U-DEC); 2025-04-05 loss vs Pat Sabatini (U-DEC)
- independent model votes for Giga Chikadze: logistic 43.5%, calibrated GBM 36.7%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Giga Chikadze | Joanderson Brito |
|---|---:|---:|
| Age | 38.07 | 31.60 |
| Reach (cm) | 187.96 | 182.88 |
| UFC fights | 12.00 | 10.00 |
| Days since UFC fight | 280.00 | 105.00 |
| Last 3: sig. strikes landed/min | 2.55 | 1.19 |
| Last 3: sig. strikes absorbed/min | 3.56 | 1.52 |
| Last 5: takedowns/15 min | 0.00 | 3.11 |
| Last 5: takedown defense (fraction) | 0.58 | 0.60 |
| Last 5: control-time fraction | 0.00 | 0.36 |
| Last 5: opponent pre-fight Elo | 1652.85 | 1595.11 |

- skill-only research model P(Giga Chikadze) = 0.387; vig-free market = 0.230 (gap +0.157). Market shown for comparison only.
- method: Giga Chikadze by KO 14% / sub 2% / dec 22%; Joanderson Brito by KO 16% / sub 18% / dec 28%
- pick outcome: Joanderson Brito by decision (28%)
- how it ends: finish 50% (R1 26% / R2 16% / R3 8%) vs. decision 50%
- likeliest endings: Joanderson Brito by decision (28%), Giga Chikadze by decision (22%), Joanderson Brito by submission, round 1 (10%)
- drivers (log-odds): diff_age -0.25, diff_strike_elo +0.16, diff_td15_l5 -0.11, diff_elo -0.10, diff_opp_elo_l5 +0.10

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Giga Chikadze by KO/TKO | 6.4% | 4.9% | 3.1% | **14.4%** |
| Giga Chikadze by submission | 1.0% | 0.8% | 0.5% | **2.4%** |
| Joanderson Brito by KO/TKO | 9.1% | 4.8% | 2.0% | **16.0%** |
| Joanderson Brito by submission | 9.6% | 5.6% | 2.4% | **17.6%** |
| decision (either fighter) | — | — | — | **49.7%** |

---
*Simulation/educational project. No betting advice. The market knows more than this model.*