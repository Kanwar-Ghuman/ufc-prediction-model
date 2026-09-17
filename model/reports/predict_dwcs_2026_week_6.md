# Dana White's Contender Series 2026: Week 6 — 2026-09-15

Point-in-time predictions from 8731 historical fights. Educational output — NOT betting advice; the backtest shows this model does not beat the market.

Prediction mode: **skill_only**. Odds, ranking nudges and social sentiment do not change these probabilities.
Historical results available through 2026-09-12.

## Mayton Perea vs. Zevan Hunt — Welterweight
P(Mayton Perea wins) = 0.360  ->  pick: Zevan Hunt (64%)
- CAUTION: no UFC history for Mayton Perea (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 8-3-0.
- CAUTION: no UFC history for Zevan Hunt (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 7-0-0.
- recent fights, Mayton Perea: 2026-05-27 win vs Wellington Madeira (KO/TKO); 2026-02-25 win vs Bruno Rodriguez (KO/TKO); 2025-11-22 win vs Cristian Chere Minda (KO/TKO)
- recent fights, Zevan Hunt: 2026-03-21 win vs Devin Smyth (SUB); 2026-01-17 win vs Brian Grinnell (KO/TKO); 2025-02-22 win vs Jared McLoughlin (SUB)
- independent model votes for Mayton Perea: logistic 34.4%, calibrated GBM 36.7%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Mayton Perea | Zevan Hunt |
|---|---:|---:|
| Age | 26.08 | 27.77 |
| Reach (cm) | unavailable | unavailable |
| UFC fights | 0.00 | 0.00 |
| Days since UFC fight | unavailable | unavailable |
| Last 3: sig. strikes landed/min | unavailable | unavailable |
| Last 3: sig. strikes absorbed/min | unavailable | unavailable |
| Last 5: takedowns/15 min | unavailable | unavailable |
| Last 5: takedown defense (fraction) | unavailable | unavailable |
| Last 5: control-time fraction | unavailable | unavailable |
| Last 5: opponent pre-fight Elo | unavailable | unavailable |

- method: Mayton Perea by KO 14% / sub 5% / dec 17%; Zevan Hunt by KO 28% / sub 15% / dec 21%
- pick outcome: Zevan Hunt by KO/TKO, round 1 (method 28%; round given method 56%; exact outcome 16%)
- how it ends: finish 63% (R1 34% / R2 19% / R3 10%) vs. decision 37%
- likeliest endings: Zevan Hunt by decision (21%), Mayton Perea by decision (17%), Zevan Hunt by KO/TKO, round 1 (16%)
- drivers (log-odds): diff_pre_ufc_finish_loss_rate -0.40, f2_reach_cm -0.06, diff_career_win_pct -0.05, f1_reach_cm +0.04, f2_career_win_pct -0.04

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Mayton Perea by KO/TKO | 7.4% | 4.3% | 2.3% | **14.0%** |
| Mayton Perea by submission | 2.7% | 1.6% | 0.9% | **5.2%** |
| Zevan Hunt by KO/TKO | 15.8% | 8.4% | 4.1% | **28.2%** |
| Zevan Hunt by submission | 8.2% | 4.6% | 2.3% | **15.1%** |
| decision (either fighter) | — | — | — | **37.5%** |

## Igor Cavalcanti vs. Oscar Ravello — Middleweight
P(Igor Cavalcanti wins) = 0.647  ->  pick: Igor Cavalcanti (65%)
- CAUTION: no UFC history for Igor Cavalcanti (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 13-2-0.
- CAUTION: no UFC history for Oscar Ravello (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 13-3-1.
- recent fights, Igor Cavalcanti: 2026-05-30 win vs Marek Jakimowicz (KO/TKO); 2026-04-11 win vs Emanuel Lopez (KO/TKO); 2025-11-29 loss vs Kamil Kraska (SUB)
- recent fights, Oscar Ravello: 2026-04-16 win vs Fernando Ataide Gomes (SUB); 2025-12-05 win vs Naif Tadeu Correa Junior (KO/TKO); 2025-10-30 loss vs Fabricio Jonas da Silva Martins (KO/TKO)
- independent model votes for Igor Cavalcanti: logistic 56.0%, calibrated GBM 68.5%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Igor Cavalcanti | Oscar Ravello |
|---|---:|---:|
| Age | 28.93 | 27.97 |
| Reach (cm) | 200.66 | unavailable |
| UFC fights | 0.00 | 0.00 |
| Days since UFC fight | unavailable | unavailable |
| Last 3: sig. strikes landed/min | unavailable | unavailable |
| Last 3: sig. strikes absorbed/min | unavailable | unavailable |
| Last 5: takedowns/15 min | unavailable | unavailable |
| Last 5: takedown defense (fraction) | unavailable | unavailable |
| Last 5: control-time fraction | unavailable | unavailable |
| Last 5: opponent pre-fight Elo | unavailable | unavailable |

- method: Igor Cavalcanti by KO 31% / sub 10% / dec 24%; Oscar Ravello by KO 16% / sub 5% / dec 14%
- pick outcome: Igor Cavalcanti by KO/TKO, round 1 (method 31%; round given method 55%; exact outcome 17%)
- how it ends: finish 61% (R1 34% / R2 19% / R3 9%) vs. decision 39%
- likeliest endings: Igor Cavalcanti by decision (24%), Igor Cavalcanti by KO/TKO, round 1 (17%), Oscar Ravello by decision (14%)
- drivers (log-odds): f2_reach_cm +0.51, f1_reach_cm +0.41, diff_height_cm -0.22, f1_height_cm -0.12, f2_height_cm -0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Igor Cavalcanti by KO/TKO | 17.2% | 9.3% | 4.5% | **31.0%** |
| Igor Cavalcanti by submission | 5.1% | 3.0% | 1.5% | **9.6%** |
| Oscar Ravello by KO/TKO | 8.8% | 4.7% | 2.2% | **15.7%** |
| Oscar Ravello by submission | 2.8% | 1.6% | 0.8% | **5.1%** |
| decision (either fighter) | — | — | — | **38.6%** |

## Akbar Abdullaev vs. Ednilson Barros Santos — Lightweight
P(Akbar Abdullaev wins) = 0.724  ->  pick: Akbar Abdullaev (72%)
- CAUTION: no UFC history for Akbar Abdullaev (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 13-0-0.
- CAUTION: no UFC history for Ednilson Barros Santos (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 14-7-1.
- recent fights, Akbar Abdullaev: 2025-09-05 win vs Ibragim Dauev (KO/TKO); 2025-01-10 win vs Kai Tang (KO/TKO); 2024-05-03 win vs Halil Amir (KO/TKO)
- recent fights, Ednilson Barros Santos: 2026-05-22 win vs Shaheen Santana (DEC); 2025-03-22 loss vs Dylan Mantello (KO/TKO); 2024-11-08 win vs Kamuela Kirk (DEC)
- independent model votes for Akbar Abdullaev: logistic 72.8%, calibrated GBM 72.2%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Akbar Abdullaev | Ednilson Barros Santos |
|---|---:|---:|
| Age | 28.99 | unavailable |
| Reach (cm) | unavailable | unavailable |
| UFC fights | 0.00 | 0.00 |
| Days since UFC fight | unavailable | unavailable |
| Last 3: sig. strikes landed/min | unavailable | unavailable |
| Last 3: sig. strikes absorbed/min | unavailable | unavailable |
| Last 5: takedowns/15 min | unavailable | unavailable |
| Last 5: takedown defense (fraction) | unavailable | unavailable |
| Last 5: control-time fraction | unavailable | unavailable |
| Last 5: opponent pre-fight Elo | unavailable | unavailable |

- method: Akbar Abdullaev by KO 40% / sub 11% / dec 22%; Ednilson Barros Santos by KO 12% / sub 4% / dec 12%
- pick outcome: Akbar Abdullaev by KO/TKO, round 1 (method 40%; round given method 65%; exact outcome 26%)
- how it ends: finish 66% (R1 42% / R2 17% / R3 7%) vs. decision 34%
- likeliest endings: Akbar Abdullaev by KO/TKO, round 1 (26%), Akbar Abdullaev by decision (22%), Ednilson Barros Santos by decision (12%)
- drivers (log-odds): f2_reach_cm +0.16, f2_age +0.14, f1_age +0.13, f1_age_past_prime +0.10, diff_pre_ufc_finish_loss_rate +0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Akbar Abdullaev by KO/TKO | 25.8% | 9.8% | 4.0% | **39.5%** |
| Akbar Abdullaev by submission | 6.9% | 2.8% | 1.2% | **10.8%** |
| Ednilson Barros Santos by KO/TKO | 7.3% | 3.2% | 1.4% | **11.9%** |
| Ednilson Barros Santos by submission | 2.2% | 1.0% | 0.5% | **3.7%** |
| decision (either fighter) | — | — | — | **34.0%** |

## Hugo Guillon vs. Luis Hernandez — Middleweight
P(Hugo Guillon wins) = 0.396  ->  pick: Luis Hernandez (60%)
- CAUTION: no UFC history for Hugo Guillon (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 7-1-0.
- CAUTION: no UFC history for Luis Hernandez (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 7-0-0.
- recent fights, Hugo Guillon: 2025-11-15 win vs Kamil Smetoch (KO/TKO); 2025-05-16 win vs Vladislav Gutu (KO/TKO); 2023-12-15 win vs Shakhbulat Abuev (SUB)
- recent fights, Luis Hernandez: 2025-10-11 win vs Paulo Machado (KO/TKO); 2025-06-29 win vs Miles Hunsinger (SUB); 2025-04-30 win vs Joaquin Campos (SUB)
- independent model votes for Hugo Guillon: logistic 33.7%, calibrated GBM 42.2%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Hugo Guillon | Luis Hernandez |
|---|---:|---:|
| Age | 29.43 | 30.06 |
| Reach (cm) | unavailable | unavailable |
| UFC fights | 0.00 | 0.00 |
| Days since UFC fight | unavailable | unavailable |
| Last 3: sig. strikes landed/min | unavailable | unavailable |
| Last 3: sig. strikes absorbed/min | unavailable | unavailable |
| Last 5: takedowns/15 min | unavailable | unavailable |
| Last 5: takedown defense (fraction) | unavailable | unavailable |
| Last 5: control-time fraction | unavailable | unavailable |
| Last 5: opponent pre-fight Elo | unavailable | unavailable |

- method: Hugo Guillon by KO 17% / sub 5% / dec 17%; Luis Hernandez by KO 22% / sub 16% / dec 23%
- pick outcome: Luis Hernandez by decision (23%)
- how it ends: finish 60% (R1 33% / R2 18% / R3 9%) vs. decision 40%
- likeliest endings: Luis Hernandez by decision (23%), Hugo Guillon by decision (17%), Luis Hernandez by KO/TKO, round 1 (12%)
- drivers (log-odds): diff_pre_ufc_finish_loss_rate -0.06, f2_reach_cm -0.06, diff_career_win_pct -0.05, diff_career_fights_24m -0.05, f1_reach_cm +0.05

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Hugo Guillon by KO/TKO | 9.5% | 5.2% | 2.6% | **17.3%** |
| Hugo Guillon by submission | 2.7% | 1.6% | 0.8% | **5.1%** |
| Luis Hernandez by KO/TKO | 12.4% | 6.5% | 3.0% | **21.9%** |
| Luis Hernandez by submission | 8.6% | 4.8% | 2.3% | **15.7%** |
| decision (either fighter) | — | — | — | **39.9%** |

## Antônio Monteiro vs. Tyshawn Williams — Featherweight
P(Antônio Monteiro wins) = 0.320  ->  pick: Tyshawn Williams (68%)
- CAUTION: no UFC history for Antônio Monteiro (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 18-5-1.
- CAUTION: no UFC history for Tyshawn Williams (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 8-0-0.
- recent fights, Antônio Monteiro: 2025-06-27 win vs Savio de Souza (SUB); 2024-10-15 loss vs Yadier Del Valle (DEC); 2023-11-17 win vs Lucas Tavares (DEC)
- recent fights, Tyshawn Williams: 2026-01-22 win vs Khabibullo Azizov (KO/TKO); 2025-03-14 win vs Alfred Walker (DEC); 2024-12-08 win vs Alex Cunuhay (KO/TKO)
- independent model votes for Antônio Monteiro: logistic 38.8%, calibrated GBM 29.1%. Their spread is a sensitivity check, not a confidence interval.

| Pre-fight evidence | Antônio Monteiro | Tyshawn Williams |
|---|---:|---:|
| Age | unavailable | 30.06 |
| Reach (cm) | unavailable | unavailable |
| UFC fights | 0.00 | 0.00 |
| Days since UFC fight | unavailable | unavailable |
| Last 3: sig. strikes landed/min | unavailable | unavailable |
| Last 3: sig. strikes absorbed/min | unavailable | unavailable |
| Last 5: takedowns/15 min | unavailable | unavailable |
| Last 5: takedown defense (fraction) | unavailable | unavailable |
| Last 5: control-time fraction | unavailable | unavailable |
| Last 5: opponent pre-fight Elo | unavailable | unavailable |

- method: Antônio Monteiro by KO 11% / sub 7% / dec 14%; Tyshawn Williams by KO 31% / sub 8% / dec 29%
- pick outcome: Tyshawn Williams by KO/TKO, round 1 (method 31%; round given method 66%; exact outcome 20%)
- how it ends: finish 57% (R1 37% / R2 14% / R3 6%) vs. decision 43%
- likeliest endings: Tyshawn Williams by decision (29%), Tyshawn Williams by KO/TKO, round 1 (20%), Antônio Monteiro by decision (14%)
- drivers (log-odds): f2_reach_cm -0.18, f2_age -0.14, f1_age -0.12, f1_age_past_prime -0.11, f1_reach_cm -0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Antônio Monteiro by KO/TKO | 6.9% | 2.9% | 1.3% | **11.1%** |
| Antônio Monteiro by submission | 4.0% | 1.8% | 0.8% | **6.6%** |
| Tyshawn Williams by KO/TKO | 20.5% | 7.6% | 3.1% | **31.2%** |
| Tyshawn Williams by submission | 5.1% | 2.0% | 0.9% | **8.0%** |
| decision (either fighter) | — | — | — | **43.1%** |

---
*Simulation/educational project. No betting advice. The market knows more than this model.*