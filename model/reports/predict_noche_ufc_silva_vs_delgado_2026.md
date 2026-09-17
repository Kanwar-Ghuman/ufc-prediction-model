# Noche UFC: Silva vs. Delgado — 2026-09-12

Point-in-time predictions from 8717 historical fights. Educational output — NOT betting advice; the backtest shows this model does not beat the market.

Name spellings resolved against ufcstats: Waldo Cortes-Acosta -> Waldo Cortes Acosta

Prediction mode: **skill_only**. Odds, ranking nudges and social sentiment do not change these probabilities.
Historical results available through 2026-09-05.

## Jean Silva vs. Jose Delgado — Featherweight
P(Jean Silva wins) = 0.504  ->  pick: Jean Silva (50%; close fight)
- verified context, Jose Delgado: Accepted the Silva main event as a replacement for Yair Rodriguez. The shorter camp and five-round assignment add uncertainty. His last two wins were over Andre Fili and Austin Bashi. [Source](https://www.ufc.com/news/jose-miguel-delgado-everything-has-built-moment-noche-ufc).
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Jose Delgado is the volume striker (6.1 vs 4.4 SLpM).
- research: Last fights: Jean Silva won last time out; Jose Delgado won last time out.
- research: Style record: Jean Silva is 83% against strikers in the UFC.
- recent fights, Jean Silva: 2026-01-24 win vs Arnold Allen (U-DEC); 2025-09-13 loss vs Diego Lopes (KO/TKO); 2025-04-12 win vs Bryce Mitchell (SUB)
- recent fights, Jose Delgado: 2026-07-18 win vs Austin Bashi (U-DEC); 2026-03-14 win vs Andre Fili (S-DEC); 2025-10-25 loss vs Nathaniel Wood (U-DEC)
- independent model votes for Jean Silva: logistic 65.0%, calibrated GBM 42.5%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Jean Silva | Jose Delgado |
|---|---:|---:|
| Age | unavailable | 28.39 |
| Reach (cm) | unavailable | 187.96 |
| UFC fights | 7.00 | 5.00 |
| Days since UFC fight | 231.00 | 56.00 |
| Last 3: sig. strikes landed/min | 4.28 | 5.84 |
| Last 3: sig. strikes absorbed/min | 4.93 | 4.29 |
| Last 5: takedowns/15 min | 1.21 | 0.62 |
| Last 5: takedown defense (fraction) | 0.82 | 0.59 |
| Last 5: control-time fraction | 0.02 | 0.09 |
| Last 5: opponent pre-fight Elo | 1669.54 | 1568.66 |

- method: Jean Silva by KO 30% / sub 6% / dec 14%; Jose Delgado by KO 32% / sub 4% / dec 14%
- pick outcome: Jean Silva by KO/TKO, round 1 (method 30%; round given method 47%; exact outcome 14%)
- how it ends: finish 72% (R1 33% / R2 20% / R3 10% / R4 5% / R5 3%) vs. decision 28%
- likeliest endings: Jose Delgado by KO/TKO, round 1 (15%), Jean Silva by decision (14%), Jean Silva by KO/TKO, round 1 (14%)
- drivers (log-odds): f1_reach_cm -0.34, diff_strike_elo -0.30, f2_reach_cm -0.25, diff_height_cm +0.23, diff_opp_elo_l5 +0.09

| ending | R1 | R2 | R3 | R4 | R5 | any round |
|---|---|---|---|---|---|---|
| Jean Silva by KO/TKO | 14.2% | 8.7% | 4.2% | 1.9% | 1.4% | **30.4%** |
| Jean Silva by submission | 2.3% | 1.6% | 0.9% | 0.5% | 0.2% | **5.6%** |
| Jose Delgado by KO/TKO | 14.7% | 8.9% | 4.7% | 2.2% | 1.6% | **32.2%** |
| Jose Delgado by submission | 1.6% | 1.1% | 0.7% | 0.4% | 0.2% | **3.9%** |
| decision (either fighter) | — | — | — | — | — | **28.0%** |

## Brandon Moreno vs. Joseph Morales — Flyweight
P(Brandon Moreno wins) = 0.645  ->  pick: Brandon Moreno (64%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Brandon Moreno is the volume striker (3.9 vs 2.0 SLpM).
- research: Form: Joseph Morales holds the pre-fight-expectation-adjusted form edge (cold vs mixed over the last 5).
- research: Style record: Brandon Moreno is 61% against strikers in the UFC.
- research: Common opponents (1): Brandon Moreno's record against them is better.
- recent fights, Brandon Moreno: 2026-02-28 loss vs Lone'er Kavanagh (U-DEC); 2025-12-06 loss vs Tatsuro Taira (KO/TKO); 2025-03-29 win vs Steve Erceg (U-DEC)
- recent fights, Joseph Morales: 2025-11-08 win vs Matt Schnell (SUB); 2025-08-16 win vs Alibi Idiris (SUB); 2023-02-03 win vs Anthony Do (SUB)
- independent model votes for Brandon Moreno: logistic 66.2%, calibrated GBM 63.5%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Brandon Moreno | Joseph Morales |
|---|---:|---:|
| Age | 32.76 | 32.06 |
| Reach (cm) | 177.80 | 175.26 |
| UFC fights | 20.00 | 5.00 |
| Days since UFC fight | 196.00 | 308.00 |
| Last 3: sig. strikes landed/min | 3.08 | 2.23 |
| Last 3: sig. strikes absorbed/min | 4.20 | 1.85 |
| Last 5: takedowns/15 min | 0.56 | 1.14 |
| Last 5: takedown defense (fraction) | 0.73 | 0.27 |
| Last 5: control-time fraction | 0.11 | 0.17 |
| Last 5: opponent pre-fight Elo | 1613.53 | 1509.38 |

- method: Brandon Moreno by KO 14% / sub 12% / dec 38%; Joseph Morales by KO 9% / sub 9% / dec 18%
- pick outcome: Brandon Moreno by decision (38%)
- how it ends: finish 44% (R1 22% / R2 15% / R3 8%) vs. decision 56%
- likeliest endings: Brandon Moreno by decision (38%), Joseph Morales by decision (18%), Brandon Moreno by KO/TKO, round 1 (6%)
- drivers (log-odds): diff_strike_elo +0.15, diff_age -0.13, diff_opp_elo_l5 +0.11, diff_elo +0.09, diff_career_win_pct -0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Brandon Moreno by KO/TKO | 6.5% | 5.0% | 2.8% | **14.2%** |
| Brandon Moreno by submission | 5.3% | 4.4% | 2.5% | **12.2%** |
| Joseph Morales by KO/TKO | 4.9% | 2.5% | 1.1% | **8.5%** |
| Joseph Morales by submission | 4.9% | 2.7% | 1.2% | **8.8%** |
| decision (either fighter) | — | — | — | **56.3%** |

## Tommy McMillen vs. Marwan Rahiki — Featherweight
P(Tommy McMillen wins) = 0.641  ->  pick: Tommy McMillen (64%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Tommy McMillen is the volume striker (18.7 vs 8.8 SLpM).
- research: Last fights: Tommy McMillen won last time out; Marwan Rahiki won last time out.
- research: Style record: Tommy McMillen is 100% against strikers in the UFC.
- recent fights, Tommy McMillen: 2026-07-18 win vs Alberto Montes (KO/TKO); 2026-04-04 win vs Manolo Zecchini (KO/TKO); 2025-09-02 win vs David Mgoyan (DEC)
- recent fights, Marwan Rahiki: 2026-05-02 win vs Ollie Schmid (KO/TKO); 2026-03-14 win vs Harry Hardwick (KO/TKO); 2025-10-14 win vs Ananias Mulumba (KO/TKO)
- independent model votes for Tommy McMillen: logistic 65.0%, calibrated GBM 63.5%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Tommy McMillen | Marwan Rahiki |
|---|---:|---:|
| Age | 28.74 | unavailable |
| Reach (cm) | 187.96 | unavailable |
| UFC fights | 2.00 | 2.00 |
| Days since UFC fight | 56.00 | 133.00 |
| Last 3: sig. strikes landed/min | 18.70 | 8.76 |
| Last 3: sig. strikes absorbed/min | 4.36 | 5.79 |
| Last 5: takedowns/15 min | 0.00 | 0.00 |
| Last 5: takedown defense (fraction) | unavailable | 1.00 |
| Last 5: control-time fraction | 0.06 | 0.13 |
| Last 5: opponent pre-fight Elo | 1496.82 | 1482.29 |

- method: Tommy McMillen by KO 34% / sub 10% / dec 20%; Marwan Rahiki by KO 22% / sub 3% / dec 11%
- pick outcome: Tommy McMillen by KO/TKO, round 1 (method 34%; round given method 65%; exact outcome 22%)
- how it ends: finish 69% (R1 44% / R2 17% / R3 7%) vs. decision 31%
- likeliest endings: Tommy McMillen by KO/TKO, round 1 (22%), Tommy McMillen by decision (20%), Marwan Rahiki by KO/TKO, round 1 (14%)
- drivers (log-odds): diff_strike_elo +0.31, f1_reach_cm +0.30, f2_reach_cm +0.27, diff_height_cm -0.20, f2_height_cm -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Tommy McMillen by KO/TKO | 21.9% | 8.5% | 3.5% | **34.0%** |
| Tommy McMillen by submission | 6.1% | 2.6% | 1.1% | **9.8%** |
| Marwan Rahiki by KO/TKO | 14.2% | 5.4% | 2.2% | **21.7%** |
| Marwan Rahiki by submission | 2.2% | 0.9% | 0.4% | **3.5%** |
| decision (either fighter) | — | — | — | **31.0%** |

## Manon Fiorot vs. Alexa Grasso — Women's Flyweight
P(Manon Fiorot wins) = 0.629  ->  pick: Manon Fiorot (63%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Manon Fiorot is the volume striker (5.1 vs 2.5 SLpM).
- research: Form: Manon Fiorot holds the pre-fight-expectation-adjusted form edge (hot vs hot over the last 5).
- research: Style record: Manon Fiorot is 86% against strikers in the UFC.
- research: Common opponents (1): Alexa Grasso's record against them is better.
- recent fights, Manon Fiorot: 2025-10-18 win vs Jasmine Jasudavicius (KO/TKO); 2025-05-10 loss vs Valentina Shevchenko (U-DEC); 2024-03-30 win vs Erin Blanchfield (U-DEC)
- recent fights, Alexa Grasso: 2026-03-28 win vs Maycee Barber (KO/TKO); 2025-05-10 loss vs Natalia Silva (U-DEC); 2024-09-14 loss vs Valentina Shevchenko (U-DEC)
- independent model votes for Manon Fiorot: logistic 61.7%, calibrated GBM 63.5%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Manon Fiorot | Alexa Grasso |
|---|---:|---:|
| Age | 36.57 | 33.09 |
| Reach (cm) | 165.10 | 167.64 |
| UFC fights | 9.00 | 15.00 |
| Days since UFC fight | 329.00 | 168.00 |
| Last 3: sig. strikes landed/min | 5.06 | 1.76 |
| Last 3: sig. strikes absorbed/min | 3.98 | 2.69 |
| Last 5: takedowns/15 min | 0.55 | 0.34 |
| Last 5: takedown defense (fraction) | 0.89 | 0.36 |
| Last 5: control-time fraction | 0.11 | 0.06 |
| Last 5: opponent pre-fight Elo | 1746.49 | 1775.38 |

- method: Manon Fiorot by KO 9% / sub 4% / dec 50%; Alexa Grasso by KO 12% / sub 4% / dec 21%
- pick outcome: Manon Fiorot by decision (50%)
- how it ends: finish 29% (R1 15% / R2 9% / R3 5%) vs. decision 71%
- likeliest endings: Manon Fiorot by decision (50%), Alexa Grasso by decision (21%), Alexa Grasso by KO/TKO, round 1 (6%)
- drivers (log-odds): diff_strike_elo +0.36, diff_age -0.18, diff_opp_elo_l5 -0.09, diff_elo +0.08, diff_age_past_prime -0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Manon Fiorot by KO/TKO | 5.0% | 2.8% | 1.5% | **9.4%** |
| Manon Fiorot by submission | 2.0% | 1.2% | 0.7% | **3.9%** |
| Alexa Grasso by KO/TKO | 6.0% | 3.7% | 1.9% | **11.6%** |
| Alexa Grasso by submission | 2.2% | 1.5% | 0.8% | **4.5%** |
| decision (either fighter) | — | — | — | **70.7%** |

## Waldo Cortes Acosta vs. Curtis Blaydes — Heavyweight
P(Waldo Cortes Acosta wins) = 0.599  ->  pick: Waldo Cortes Acosta (60%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Curtis Blaydes is the volume striker (6.7 vs 3.8 SLpM).
- research: Form: Waldo Cortes Acosta holds the pre-fight-expectation-adjusted form edge (mixed vs cold over the last 5).
- research: Style record: Waldo Cortes Acosta is 77% against strikers in the UFC.
- research: Common opponents: 3 shared names on the record.
- recent fights, Waldo Cortes Acosta: 2026-05-09 loss vs Alexander Volkov (U-DEC); 2026-01-24 win vs Derrick Lewis (KO/TKO); 2025-11-22 win vs Shamil Gaziev (KO/TKO)
- recent fights, Curtis Blaydes: 2026-04-11 loss vs Josh Hokit (U-DEC); 2025-06-21 win vs Rizvan Kuniev (S-DEC); 2024-07-27 loss vs Tom Aspinall (KO/TKO)
- independent model votes for Waldo Cortes Acosta: logistic 53.3%, calibrated GBM 63.5%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Waldo Cortes Acosta | Curtis Blaydes |
|---|---:|---:|
| Age | unavailable | 35.56 |
| Reach (cm) | unavailable | 203.20 |
| UFC fights | 13.00 | 21.00 |
| Days since UFC fight | 126.00 | 154.00 |
| Last 3: sig. strikes landed/min | 4.39 | 7.58 |
| Last 3: sig. strikes absorbed/min | 4.15 | 7.61 |
| Last 5: takedowns/15 min | 0.34 | 1.51 |
| Last 5: takedown defense (fraction) | 1.00 | 0.36 |
| Last 5: control-time fraction | 0.05 | 0.19 |
| Last 5: opponent pre-fight Elo | 1677.49 | 1654.27 |

- method: Waldo Cortes Acosta by KO 38% / sub 4% / dec 19%; Curtis Blaydes by KO 14% / sub 2% / dec 24%
- pick outcome: Waldo Cortes Acosta by KO/TKO, round 1 (method 38%; round given method 57%; exact outcome 21%)
- how it ends: finish 57% (R1 32% / R2 17% / R3 8%) vs. decision 43%
- likeliest endings: Curtis Blaydes by decision (24%), Waldo Cortes Acosta by KO/TKO, round 1 (21%), Waldo Cortes Acosta by decision (19%)
- drivers (log-odds): f2_reach_cm -0.32, f1_reach_cm -0.31, diff_height_cm +0.30, diff_career_fights_24m +0.09, diff_opp_elo_l5 +0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Waldo Cortes Acosta by KO/TKO | 21.4% | 11.0% | 5.2% | **37.6%** |
| Waldo Cortes Acosta by submission | 2.0% | 1.1% | 0.5% | **3.6%** |
| Curtis Blaydes by KO/TKO | 7.5% | 4.4% | 2.0% | **13.8%** |
| Curtis Blaydes by submission | 1.1% | 0.7% | 0.3% | **2.2%** |
| decision (either fighter) | — | — | — | **42.9%** |

## David Martinez vs. Dan Ige — Bantamweight
P(David Martinez wins) = 0.823  ->  pick: David Martinez (82%)
- verified context, Dan Ige: Moving from featherweight to bantamweight for this fight; his historical featherweight performance may not transfer directly to 135 pounds. [Source](https://www.ufc.com/news/david-martinez-step-fire-zone-noche-ufc).
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: David Martinez is the volume striker (4.6 vs 3.0 SLpM).
- research: Form: David Martinez holds the pre-fight-expectation-adjusted form edge (hot vs cold over the last 5).
- research: Style record: David Martinez is 100% against strikers in the UFC.
- recent fights, David Martinez: 2026-02-28 win vs Marlon Vera (U-DEC); 2025-09-13 win vs Rob Font (U-DEC); 2025-03-29 win vs Saimon Oliveira (KO/TKO)
- recent fights, Dan Ige: 2026-02-21 loss vs Melquizael Costa (KO/TKO); 2025-07-19 loss vs Patricio Freire (U-DEC); 2025-04-12 win vs Sean Woodson (KO/TKO)
- independent model votes for David Martinez: logistic 84.6%, calibrated GBM 81.1%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | David Martinez | Dan Ige |
|---|---:|---:|
| Age | 28.11 | 35.10 |
| Reach (cm) | 170.18 | 180.34 |
| UFC fights | 3.00 | 21.00 |
| Days since UFC fight | 196.00 | 203.00 |
| Last 3: sig. strikes landed/min | 4.62 | 3.15 |
| Last 3: sig. strikes absorbed/min | 2.83 | 4.01 |
| Last 5: takedowns/15 min | 0.87 | 0.49 |
| Last 5: takedown defense (fraction) | 1.00 | 0.47 |
| Last 5: control-time fraction | 0.09 | 0.14 |
| Last 5: opponent pre-fight Elo | 1601.12 | 1645.25 |

- method: David Martinez by KO 22% / sub 4% / dec 56%; Dan Ige by KO 6% / sub 2% / dec 9%
- pick outcome: David Martinez by decision (56%)
- how it ends: finish 35% (R1 17% / R2 11% / R3 6%) vs. decision 65%
- likeliest endings: David Martinez by decision (56%), David Martinez by KO/TKO, round 1 (11%), Dan Ige by decision (9%)
- drivers (log-odds): diff_age +0.23, diff_strike_elo +0.19, diff_elo +0.09, diff_opp_elo_l5 -0.08, diff_career_win_pct +0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| David Martinez by KO/TKO | 11.3% | 7.1% | 3.6% | **22.0%** |
| David Martinez by submission | 2.1% | 1.4% | 0.8% | **4.3%** |
| Dan Ige by KO/TKO | 2.6% | 2.1% | 1.5% | **6.2%** |
| Dan Ige by submission | 0.9% | 0.8% | 0.6% | **2.3%** |
| decision (either fighter) | — | — | — | **65.3%** |

## Tim Elliott vs. Edgar Chairez — Catch Weight
P(Tim Elliott wins) = 0.363  ->  pick: Edgar Chairez (64%)
- research: Style: both profile as strikers — a same-look fight.
- research: Wrestling contrast: Tim Elliott lands 3.2 takedowns/15 into Edgar Chairez's 50% TDD.
- research: Form: Edgar Chairez holds the pre-fight-expectation-adjusted form edge (mixed vs hot over the last 5).
- research: Style record: Tim Elliott is 53% against strikers in the UFC.
- recent fights, Tim Elliott: 2026-05-02 loss vs Steve Erceg (U-DEC); 2025-08-16 win vs Kai Asakura (SUB); 2023-12-09 win vs Sumudaerji (SUB)
- recent fights, Edgar Chairez: 2026-06-06 win vs Bruno Silva (SUB); 2026-02-28 win vs Felipe Bunes (S-DEC); 2025-03-29 win vs CJ Vergara (SUB)
- independent model votes for Tim Elliott: logistic 35.9%, calibrated GBM 36.5%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Tim Elliott | Edgar Chairez |
|---|---:|---:|
| Age | 39.72 | 30.63 |
| Reach (cm) | 167.64 | 180.34 |
| UFC fights | 22.00 | 7.00 |
| Days since UFC fight | 133.00 | 98.00 |
| Last 3: sig. strikes landed/min | 4.43 | 4.51 |
| Last 3: sig. strikes absorbed/min | 5.82 | 3.55 |
| Last 5: takedowns/15 min | 3.17 | 0.00 |
| Last 5: takedown defense (fraction) | 0.50 | 0.50 |
| Last 5: control-time fraction | 0.32 | 0.03 |
| Last 5: opponent pre-fight Elo | 1549.78 | 1455.81 |

- method: Tim Elliott by KO 5% / sub 10% / dec 22%; Edgar Chairez by KO 14% / sub 22% / dec 28%
- pick outcome: Edgar Chairez by decision (28%)
- how it ends: finish 50% (R1 27% / R2 16% / R3 7%) vs. decision 50%
- likeliest endings: Edgar Chairez by decision (28%), Tim Elliott by decision (22%), Edgar Chairez by submission, round 1 (12%)
- drivers (log-odds): diff_age -0.37, diff_strike_elo +0.16, diff_opp_elo_l5 +0.12, diff_career_win_pct -0.11, diff_td15_l5 +0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Tim Elliott by KO/TKO | 2.2% | 1.7% | 0.9% | **4.8%** |
| Tim Elliott by submission | 4.3% | 3.5% | 1.9% | **9.7%** |
| Edgar Chairez by KO/TKO | 8.1% | 4.1% | 1.8% | **14.0%** |
| Edgar Chairez by submission | 12.1% | 6.7% | 2.9% | **21.7%** |
| decision (either fighter) | — | — | — | **49.8%** |

## Ignacio Bahamondes vs. Muslim Salikhov — Welterweight
P(Ignacio Bahamondes wins) = 0.675  ->  pick: Ignacio Bahamondes (67%)
- verified context, Ignacio Bahamondes: This is his UFC welterweight debut after consecutive losses at lightweight; the division change adds uncertainty to historical rate comparisons. [Source](https://www.ufc.com/news/fight-fight-preview-noche-ufc-phoenix-silva-delgado-2026).
- research: Style: both profile as strikers — a same-look fight.
- research: Last fights: Ignacio Bahamondes lost last time out; Muslim Salikhov lost last time out.
- research: Style record: Ignacio Bahamondes is 60% against strikers in the UFC.
- recent fights, Ignacio Bahamondes: 2026-03-28 loss vs Tofiq Musayev (U-DEC); 2025-06-21 loss vs Rafael Fiziev (U-DEC); 2025-03-08 win vs Jalin Turner (SUB)
- recent fights, Muslim Salikhov: 2025-11-08 loss vs Uros Medic (KO/TKO); 2025-07-26 win vs Carlos Leal (KO/TKO); 2024-11-23 win vs Song Kenan (KO/TKO)
- independent model votes for Ignacio Bahamondes: logistic 74.9%, calibrated GBM 63.5%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Ignacio Bahamondes | Muslim Salikhov |
|---|---:|---:|
| Age | 29.04 | 42.26 |
| Reach (cm) | 190.50 | 177.80 |
| UFC fights | 10.00 | 14.00 |
| Days since UFC fight | 168.00 | 308.00 |
| Last 3: sig. strikes landed/min | 2.83 | 4.49 |
| Last 3: sig. strikes absorbed/min | 3.17 | 3.95 |
| Last 5: takedowns/15 min | 0.00 | 0.00 |
| Last 5: takedown defense (fraction) | 0.30 | 0.67 |
| Last 5: control-time fraction | 0.08 | 0.00 |
| Last 5: opponent pre-fight Elo | 1561.22 | 1598.33 |

- method: Ignacio Bahamondes by KO 36% / sub 9% / dec 22%; Muslim Salikhov by KO 13% / sub 2% / dec 18%
- pick outcome: Ignacio Bahamondes by KO/TKO, round 1 (method 36%; round given method 54%; exact outcome 19%)
- how it ends: finish 60% (R1 32% / R2 19% / R3 10%) vs. decision 40%
- likeliest endings: Ignacio Bahamondes by decision (22%), Ignacio Bahamondes by KO/TKO, round 1 (19%), Muslim Salikhov by decision (18%)
- drivers (log-odds): diff_age +0.38, diff_strike_elo +0.27, diff_career_win_pct -0.09, diff_grapple_elo -0.09, diff_career_fights_24m +0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Ignacio Bahamondes by KO/TKO | 19.3% | 11.2% | 5.5% | **36.0%** |
| Ignacio Bahamondes by submission | 4.6% | 2.9% | 1.5% | **9.0%** |
| Muslim Salikhov by KO/TKO | 6.7% | 4.1% | 2.2% | **13.1%** |
| Muslim Salikhov by submission | 0.9% | 0.6% | 0.3% | **1.9%** |
| decision (either fighter) | — | — | — | **40.1%** |

## Yousri Belgaroui vs. Djorden Santos — Middleweight
P(Yousri Belgaroui wins) = 0.715  ->  pick: Yousri Belgaroui (72%)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Yousri Belgaroui holds the pre-fight-expectation-adjusted form edge (hot vs mixed over the last 5).
- research: Style record: Yousri Belgaroui is 100% against strikers in the UFC.
- recent fights, Yousri Belgaroui: 2026-03-28 win vs Mansur Abdul-Malik (KO/TKO); 2025-10-18 win vs Azamat Bekoev (KO/TKO); 2024-09-10 win vs Taiga Iwasaki (KO/TKO)
- recent fights, Djorden Santos: 2026-05-09 loss vs Baisangur Susurkaev (SUB); 2025-10-18 win vs Danny Barlow (U-DEC); 2025-03-08 loss vs Ozzy Diaz (U-DEC)
- independent model votes for Yousri Belgaroui: logistic 82.4%, calibrated GBM 65.7%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Yousri Belgaroui | Djorden Santos |
|---|---:|---:|
| Age | 34.28 | 29.11 |
| Reach (cm) | 200.66 | 190.50 |
| UFC fights | 2.00 | 3.00 |
| Days since UFC fight | 168.00 | 126.00 |
| Last 3: sig. strikes landed/min | 7.98 | 6.97 |
| Last 3: sig. strikes absorbed/min | 1.63 | 7.58 |
| Last 5: takedowns/15 min | 0.61 | 0.34 |
| Last 5: takedown defense (fraction) | 0.56 | 0.80 |
| Last 5: control-time fraction | 0.07 | 0.06 |
| Last 5: opponent pre-fight Elo | 1586.71 | 1523.90 |

- method: Yousri Belgaroui by KO 28% / sub 6% / dec 38%; Djorden Santos by KO 9% / sub 5% / dec 14%
- pick outcome: Yousri Belgaroui by decision (38%)
- how it ends: finish 48% (R1 24% / R2 15% / R3 9%) vs. decision 52%
- likeliest endings: Yousri Belgaroui by decision (38%), Djorden Santos by decision (14%), Yousri Belgaroui by KO/TKO, round 1 (14%)
- drivers (log-odds): diff_strike_elo +0.33, diff_age -0.19, diff_elo +0.16, diff_opp_elo_l5 +0.11, diff_sapm_l5 +0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Yousri Belgaroui by KO/TKO | 13.7% | 8.5% | 5.7% | **27.9%** |
| Yousri Belgaroui by submission | 2.8% | 1.9% | 1.3% | **6.0%** |
| Djorden Santos by KO/TKO | 4.8% | 2.8% | 1.3% | **8.9%** |
| Djorden Santos by submission | 2.8% | 1.8% | 0.9% | **5.5%** |
| decision (either fighter) | — | — | — | **51.7%** |

## Drakkar Klose vs. Tommy Gantt — Lightweight
P(Drakkar Klose wins) = 0.230  ->  pick: Tommy Gantt (77%)
- verified context, Tommy Gantt: UFC bills him as Tommy Gantt; Sherdog uses Thomas Gantt. The verified profile matches his Minev and Livingston fights. His wrestling background is substantial, but he has only one UFC bout. [Source](https://www.ufc.com/athlete/thomas-gantt).
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Tommy Gantt holds the pre-fight-expectation-adjusted form edge (hot vs hot over the last 5).
- research: Style record: Drakkar Klose is 73% against strikers in the UFC.
- recent fights, Drakkar Klose: 2025-08-16 win vs Edson Barboza (U-DEC); 2024-12-14 loss vs Joel Alvarez (KO/TKO); 2024-05-04 win vs Joaquim Silva (U-DEC)
- recent fights, Tommy Gantt: 2026-05-16 win vs Artur Minev (KO/TKO); 2025-09-16 win vs Adam Livingston (SUB); 2025-02-08 win vs Deven Paulsen (KO/TKO)
- independent model votes for Drakkar Klose: logistic 23.2%, calibrated GBM 22.9%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Drakkar Klose | Tommy Gantt |
|---|---:|---:|
| Age | 38.51 | 33.67 |
| Reach (cm) | 177.80 | 193.04 |
| UFC fights | 13.00 | 1.00 |
| Days since UFC fight | 392.00 | 119.00 |
| Last 3: sig. strikes landed/min | 3.96 | 3.57 |
| Last 3: sig. strikes absorbed/min | 4.57 | 1.02 |
| Last 5: takedowns/15 min | 0.91 | 11.46 |
| Last 5: takedown defense (fraction) | 0.71 | 1.00 |
| Last 5: control-time fraction | 0.24 | 0.67 |
| Last 5: opponent pre-fight Elo | 1600.53 | 1500.00 |

- method: Drakkar Klose by KO 7% / sub 2% / dec 14%; Tommy Gantt by KO 32% / sub 11% / dec 34%
- pick outcome: Tommy Gantt by decision (34%)
- how it ends: finish 52% (R1 26% / R2 16% / R3 10%) vs. decision 48%
- likeliest endings: Tommy Gantt by decision (34%), Tommy Gantt by KO/TKO, round 1 (17%), Drakkar Klose by decision (14%)
- drivers (log-odds): diff_age -0.22, diff_strike_elo -0.15, diff_elo +0.10, diff_opp_elo_l5 +0.10, diff_sapm_l5 -0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Drakkar Klose by KO/TKO | 3.3% | 2.5% | 1.7% | **7.4%** |
| Drakkar Klose by submission | 0.7% | 0.6% | 0.4% | **1.6%** |
| Tommy Gantt by KO/TKO | 16.7% | 9.8% | 5.8% | **32.3%** |
| Tommy Gantt by submission | 5.5% | 3.5% | 2.1% | **11.0%** |
| decision (either fighter) | — | — | — | **47.6%** |

## Rafa Garcia vs. Rongzhu — Lightweight
P(Rafa Garcia wins) = 0.694  ->  pick: Rafa Garcia (69%)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Rafa Garcia holds the pre-fight-expectation-adjusted form edge (hot vs hot over the last 5).
- research: Style record: Rafa Garcia is 60% against strikers in the UFC.
- recent fights, Rafa Garcia: 2026-04-25 win vs Alexander Hernandez (U-DEC); 2025-09-13 win vs Jared Gordon (KO/TKO); 2025-03-29 win vs Vinc Pichel (U-DEC)
- recent fights, Rongzhu: 2025-08-23 win vs Austin Hubbard (U-DEC); 2025-02-08 win vs Kody Steele (U-DEC); 2024-09-07 loss vs Chris Padilla (KO/TKO)
- independent model votes for Rafa Garcia: logistic 69.4%, calibrated GBM 69.5%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Rafa Garcia | Rongzhu |
|---|---:|---:|
| Age | 32.10 | 26.52 |
| Reach (cm) | 177.80 | 180.34 |
| UFC fights | 11.00 | 6.00 |
| Days since UFC fight | 140.00 | 385.00 |
| Last 3: sig. strikes landed/min | 5.04 | 7.01 |
| Last 3: sig. strikes absorbed/min | 4.57 | 5.15 |
| Last 5: takedowns/15 min | 1.87 | 1.60 |
| Last 5: takedown defense (fraction) | 0.79 | 0.82 |
| Last 5: control-time fraction | 0.10 | 0.16 |
| Last 5: opponent pre-fight Elo | 1645.01 | 1496.11 |

- method: Rafa Garcia by KO 16% / sub 15% / dec 38%; Rongzhu by KO 10% / sub 2% / dec 18%
- pick outcome: Rafa Garcia by decision (38%)
- how it ends: finish 44% (R1 22% / R2 14% / R3 7%) vs. decision 56%
- likeliest endings: Rafa Garcia by decision (38%), Rongzhu by decision (18%), Rafa Garcia by KO/TKO, round 1 (8%)
- drivers (log-odds): diff_age -0.26, diff_strike_elo +0.19, diff_elo +0.14, diff_opp_elo_l5 +0.11, diff_grapple_elo +0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Rafa Garcia by KO/TKO | 8.1% | 5.3% | 2.7% | **16.2%** |
| Rafa Garcia by submission | 7.2% | 5.2% | 2.7% | **15.1%** |
| Rongzhu by KO/TKO | 5.5% | 3.0% | 1.5% | **10.0%** |
| Rongzhu by submission | 1.2% | 0.7% | 0.4% | **2.2%** |
| decision (either fighter) | — | — | — | **56.5%** |

## Jessie Rosas vs. Sean King — Featherweight
P(Jessie Rosas wins) = 0.378  ->  pick: Sean King (62%)
- CAUTION: no UFC history for Jessie Rosas (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 8-1-0.
- CAUTION: no UFC history for Sean King (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 6-0-0.
- recent fights, Jessie Rosas: 2026-06-07 win vs Erick Ruano (SUB); 2025-10-19 win vs Luciano Ramos (KO/TKO); 2024-08-02 win vs Kaleb Petereit (DEC)
- recent fights, Sean King: 2026-07-24 win vs Dimitre Ivy (KO/TKO); 2026-04-12 win vs Cristian Lopez (SUB); 2026-02-06 win vs Dumar Roa (KO/TKO)
- independent model votes for Jessie Rosas: logistic 29.3%, calibrated GBM 42.4%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Jessie Rosas | Sean King |
|---|---:|---:|
| Age | 23.77 | 22.90 |
| Reach (cm) | unavailable | unavailable |
| UFC fights | 0.00 | 0.00 |
| Days since UFC fight | unavailable | unavailable |
| Last 3: sig. strikes landed/min | unavailable | unavailable |
| Last 3: sig. strikes absorbed/min | unavailable | unavailable |
| Last 5: takedowns/15 min | unavailable | unavailable |
| Last 5: takedown defense (fraction) | unavailable | unavailable |
| Last 5: control-time fraction | unavailable | unavailable |
| Last 5: opponent pre-fight Elo | unavailable | unavailable |

- method: Jessie Rosas by KO 11% / sub 10% / dec 17%; Sean King by KO 29% / sub 8% / dec 24%
- pick outcome: Sean King by KO/TKO, round 1 (method 29%; round given method 54%; exact outcome 16%)
- how it ends: finish 59% (R1 32% / R2 18% / R3 9%) vs. decision 41%
- likeliest endings: Sean King by decision (24%), Jessie Rosas by decision (17%), Sean King by KO/TKO, round 1 (16%)
- drivers (log-odds): f1_pre_ufc_layoff_days +0.11, f2_pre_ufc_layoff_days +0.10, diff_pre_ufc_major_org_share -0.09, f1_reach_cm +0.06, diff_career_win_pct -0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Jessie Rosas by KO/TKO | 5.8% | 3.2% | 1.7% | **10.6%** |
| Jessie Rosas by submission | 5.4% | 3.2% | 1.7% | **10.3%** |
| Sean King by KO/TKO | 15.9% | 8.7% | 4.6% | **29.3%** |
| Sean King by submission | 4.4% | 2.6% | 1.4% | **8.5%** |
| decision (either fighter) | — | — | — | **41.3%** |

## JJ Aldrich vs. Regina Tarin — Women's Flyweight
P(JJ Aldrich wins) = 0.373  ->  pick: Regina Tarin (63%)
- verified context, Regina Tarin: UFC profile still uses the Regina Malpica Rivera URL. Her February win over Ernesta Kareckaite is included; this is her second UFC appearance. [Source](https://www.ufc.com/athlete/regina-malpica-rivera).
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Regina Tarin is the volume striker (7.6 vs 3.8 SLpM).
- research: Form: Regina Tarin holds the pre-fight-expectation-adjusted form edge (hot vs hot over the last 5).
- research: Style record: JJ Aldrich is 60% against strikers in the UFC.
- recent fights, JJ Aldrich: 2026-04-18 win vs Jamey-Lyn Horth (U-DEC); 2025-03-01 win vs Andrea Lee (U-DEC); 2024-05-11 loss vs Veronica Hardy (U-DEC)
- recent fights, Regina Tarin: 2026-02-28 win vs Ernesta Kareckaite (U-DEC); 2025-11-29 win vs Yurivia Jimenez (KO/TKO); 2025-06-19 win vs Kaytlin Neil (KO/TKO)
- independent model votes for JJ Aldrich: logistic 33.4%, calibrated GBM 39.4%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | JJ Aldrich | Regina Tarin |
|---|---:|---:|
| Age | 33.95 | 21.90 |
| Reach (cm) | 170.18 | unavailable |
| UFC fights | 17.00 | 1.00 |
| Days since UFC fight | 147.00 | 196.00 |
| Last 3: sig. strikes landed/min | 3.36 | 7.60 |
| Last 3: sig. strikes absorbed/min | 3.53 | 7.00 |
| Last 5: takedowns/15 min | 0.43 | 1.00 |
| Last 5: takedown defense (fraction) | 0.56 | 0.50 |
| Last 5: control-time fraction | 0.18 | 0.07 |
| Last 5: opponent pre-fight Elo | 1485.69 | 1504.58 |

- method: JJ Aldrich by KO 5% / sub 6% / dec 26%; Regina Tarin by KO 20% / sub 7% / dec 36%
- pick outcome: Regina Tarin by decision (36%)
- how it ends: finish 38% (R1 18% / R2 12% / R3 7%) vs. decision 62%
- likeliest endings: Regina Tarin by decision (36%), JJ Aldrich by decision (26%), Regina Tarin by KO/TKO, round 1 (10%)
- drivers (log-odds): diff_age -0.34, f2_reach_cm +0.33, diff_height_cm -0.29, f1_reach_cm +0.27, diff_strike_elo -0.22

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| JJ Aldrich by KO/TKO | 2.3% | 1.6% | 0.9% | **4.8%** |
| JJ Aldrich by submission | 2.9% | 2.1% | 1.3% | **6.4%** |
| Regina Tarin by KO/TKO | 9.9% | 6.1% | 3.9% | **20.0%** |
| Regina Tarin by submission | 3.2% | 2.1% | 1.3% | **6.6%** |
| decision (either fighter) | — | — | — | **62.3%** |

---
*Simulation/educational project. No betting advice. The market knows more than this model.*