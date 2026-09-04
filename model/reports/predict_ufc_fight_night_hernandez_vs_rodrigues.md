# UFC Fight Night: Hernandez vs. Rodrigues — 2026-08-22

Point-in-time predictions from 8677 historical fights. Educational output — NOT betting advice; the backtest shows this model does not beat the market.

## Anthony Hernandez vs. Gregory Rodrigues — Middleweight
P(Anthony Hernandez wins) = 0.700  ->  pick: Anthony Hernandez (70%)
- shipped number is the market-aware stack: vig-free market P(Anthony Hernandez) = 0.637, skill-only model = 0.749 (gap +0.112)
- method: Anthony Hernandez by KO 25% / sub 17% / dec 27%; Gregory Rodrigues by KO 16% / sub 3% / dec 11%
- how it ends: finish 62% (R1 21% / R2 19% / R3 11% / R4 6% / R5 5%) vs. decision 38%
- likeliest endings: Anthony Hernandez by decision (27%), Gregory Rodrigues by decision (11%), Anthony Hernandez by KO/TKO, round 1 (8%)
- drivers (log-odds): diff_strike_elo +0.16, diff_opp_elo_l5 +0.16, diff_td15_l5 +0.11, diff_age +0.09, diff_grapple_elo +0.09

| ending | R1 | R2 | R3 | R4 | R5 | any round |
|---|---|---|---|---|---|---|
| Anthony Hernandez by KO/TKO | 8.4% | 7.8% | 4.6% | 2.4% | 2.1% | **25.4%** |
| Anthony Hernandez by submission | 5.0% | 5.3% | 3.5% | 2.0% | 1.4% | **17.2%** |
| Gregory Rodrigues by KO/TKO | 6.8% | 4.6% | 2.6% | 1.3% | 1.1% | **16.5%** |
| Gregory Rodrigues by submission | 1.1% | 0.8% | 0.5% | 0.3% | 0.2% | **3.0%** |
| decision (either fighter) | — | — | — | — | — | **37.9%** |

## Serghei Spivac vs. Vitor Petrino — Heavyweight
P(Serghei Spivac wins) = 0.361  ->  pick: Vitor Petrino (64%)
- context: YouTube lean +0.43 (n=7) noted but not applied — skill already decisive (0.32)
- shipped number is the market-aware stack: vig-free market P(Serghei Spivac) = 0.408, skill-only model = 0.317 (gap -0.091)
- method: Serghei Spivac by KO 13% / sub 11% / dec 12%; Vitor Petrino by KO 28% / sub 7% / dec 29%
- how it ends: finish 59% (R1 30% / R2 20% / R3 9%) vs. decision 41%
- likeliest endings: Vitor Petrino by decision (29%), Vitor Petrino by KO/TKO, round 1 (16%), Serghei Spivac by decision (12%)
- drivers (log-odds): diff_age -0.21, diff_strike_elo -0.16, diff_opp_elo_l5 +0.10, diff_sapm_l5 -0.10, diff_sig_acc_l5 -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Serghei Spivac by KO/TKO | 6.2% | 4.3% | 2.3% | **12.8%** |
| Serghei Spivac by submission | 5.1% | 3.9% | 2.1% | **11.1%** |
| Vitor Petrino by KO/TKO | 15.5% | 9.2% | 3.7% | **28.5%** |
| Vitor Petrino by submission | 3.5% | 2.2% | 0.9% | **6.6%** |
| decision (either fighter) | — | — | — | **41.1%** |

## Reinier de Ridder vs. Roman Dolidze — Light Heavyweight
P(Reinier de Ridder wins) = 0.807  ->  pick: Reinier de Ridder (81%)
- shipped number is the market-aware stack: vig-free market P(Reinier de Ridder) = 0.766, skill-only model = 0.706 (gap -0.060)
- method: Reinier de Ridder by KO 19% / sub 26% / dec 36%; Roman Dolidze by KO 11% / sub 2% / dec 7%
- how it ends: finish 57% (R1 29% / R2 19% / R3 10%) vs. decision 43%
- likeliest endings: Reinier de Ridder by decision (36%), Reinier de Ridder by submission, round 1 (13%), Reinier de Ridder by KO/TKO, round 1 (10%)
- drivers (log-odds): diff_strike_elo +0.17, diff_age +0.17, f1_opp_elo_l5 +0.06, diff_opp_elo_l5 +0.06, diff_sig_acc_l5 +0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Reinier de Ridder by KO/TKO | 9.9% | 6.2% | 3.3% | **19.5%** |
| Reinier de Ridder by submission | 12.5% | 8.5% | 4.6% | **25.7%** |
| Roman Dolidze by KO/TKO | 5.4% | 3.5% | 1.6% | **10.5%** |
| Roman Dolidze by submission | 0.9% | 0.6% | 0.3% | **1.8%** |
| decision (either fighter) | — | — | — | **42.6%** |

## MarQuel Mederos vs. Mason Jones — Lightweight
P(MarQuel Mederos wins) = 0.237  ->  pick: Mason Jones (76%)
- shipped number is the market-aware stack: vig-free market P(MarQuel Mederos) = 0.259, skill-only model = 0.410 (gap +0.151)
- method: MarQuel Mederos by KO 8% / sub 3% / dec 13%; Mason Jones by KO 15% / sub 7% / dec 54%
- how it ends: finish 33% (R1 15% / R2 11% / R3 7%) vs. decision 67%
- likeliest endings: Mason Jones by decision (54%), MarQuel Mederos by decision (13%), Mason Jones by KO/TKO, round 1 (7%)
- drivers (log-odds): diff_strike_elo -0.27, diff_age +0.10, diff_td15_l5 -0.10, diff_grapple_elo -0.08, diff_reach_cm -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| MarQuel Mederos by KO/TKO | 3.6% | 2.7% | 1.8% | **8.1%** |
| MarQuel Mederos by submission | 1.2% | 0.9% | 0.6% | **2.7%** |
| Mason Jones by KO/TKO | 7.2% | 5.1% | 2.9% | **15.2%** |
| Mason Jones by submission | 3.0% | 2.3% | 1.3% | **6.7%** |
| decision (either fighter) | — | — | — | **67.3%** |

## Carli Judice vs. Jeisla Chaves — Women's Flyweight
P(Carli Judice wins) = 0.842  ->  pick: Carli Judice (84%)
- shipped number is the market-aware stack: vig-free market P(Carli Judice) = 0.818, skill-only model = 0.635 (gap -0.182)
- method: Carli Judice by KO 27% / sub 8% / dec 49%; Jeisla Chaves by KO 3% / sub 3% / dec 11%
- how it ends: finish 40% (R1 20% / R2 13% / R3 7%) vs. decision 60%
- likeliest endings: Carli Judice by decision (49%), Carli Judice by KO/TKO, round 1 (14%), Jeisla Chaves by decision (11%)
- drivers (log-odds): diff_strike_elo +0.31, diff_age +0.13, diff_style_grapple_strike -0.08, diff_slpm_l5 -0.07, diff_grapple_elo -0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Carli Judice by KO/TKO | 13.6% | 8.4% | 5.1% | **27.1%** |
| Carli Judice by submission | 3.7% | 2.5% | 1.5% | **7.6%** |
| Jeisla Chaves by KO/TKO | 1.3% | 0.9% | 0.5% | **2.6%** |
| Jeisla Chaves by submission | 1.3% | 0.9% | 0.5% | **2.6%** |
| decision (either fighter) | — | — | — | **60.0%** |

## Anthony Wint vs. Terrance Chatman — Heavyweight
P(Anthony Wint wins) = 0.892  ->  pick: Anthony Wint (89%)
- CAUTION: no UFC history for Anthony Wint (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 6-0-0.
- CAUTION: no UFC history for Terrance Chatman (debut or misspelled name?) — prediction is weak.
- shipped number is the market-aware stack: vig-free market P(Anthony Wint) = 0.872, skill-only model = 0.644 (gap -0.229)
- method: Anthony Wint by KO 50% / sub 20% / dec 20%; Terrance Chatman by KO 5% / sub 2% / dec 4%
- how it ends: finish 76% (R1 51% / R2 18% / R3 7%) vs. decision 24%
- likeliest endings: Anthony Wint by KO/TKO, round 1 (34%), Anthony Wint by decision (20%), Anthony Wint by submission, round 1 (13%)
- drivers (log-odds): f1_age +0.17, f2_age +0.14, f2_pre_ufc_win_pct +0.09, diff_height_cm -0.08, f1_pre_ufc_win_pct +0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Anthony Wint by KO/TKO | 33.6% | 11.6% | 4.5% | **49.7%** |
| Anthony Wint by submission | 12.9% | 4.7% | 1.9% | **19.5%** |
| Terrance Chatman by KO/TKO | 3.2% | 1.1% | 0.4% | **4.8%** |
| Terrance Chatman by submission | 1.2% | 0.4% | 0.2% | **1.8%** |
| decision (either fighter) | — | — | — | **24.2%** |

## Jamall Emmers vs. Lerryan Douglas — Featherweight
P(Jamall Emmers wins) = 0.218  ->  pick: Lerryan Douglas (78%)
- shipped number is the market-aware stack: vig-free market P(Jamall Emmers) = 0.234, skill-only model = 0.434 (gap +0.200)
- method: Jamall Emmers by KO 6% / sub 2% / dec 14%; Lerryan Douglas by KO 50% / sub 6% / dec 21%
- how it ends: finish 65% (R1 39% / R2 18% / R3 8%) vs. decision 35%
- likeliest endings: Lerryan Douglas by KO/TKO, round 1 (31%), Lerryan Douglas by decision (21%), Jamall Emmers by decision (14%)
- drivers (log-odds): diff_age -0.32, diff_strike_elo +0.26, diff_opp_elo_l5 -0.15, diff_grapple_elo +0.07, f1_opp_elo_l5 -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Jamall Emmers by KO/TKO | 3.2% | 1.8% | 0.8% | **5.9%** |
| Jamall Emmers by submission | 1.2% | 0.7% | 0.3% | **2.2%** |
| Lerryan Douglas by KO/TKO | 31.0% | 13.5% | 5.9% | **50.4%** |
| Lerryan Douglas by submission | 3.8% | 1.8% | 0.8% | **6.4%** |
| decision (either fighter) | — | — | — | **35.2%** |

## Shamil Gaziev vs. Kennedy Nzechukwu — Heavyweight
P(Shamil Gaziev wins) = 0.541  ->  no call (54% lean Shamil Gaziev)
- shipped number is the market-aware stack: vig-free market P(Shamil Gaziev) = 0.549, skill-only model = 0.462 (gap -0.087)
- method: Shamil Gaziev by KO 22% / sub 9% / dec 23%; Kennedy Nzechukwu by KO 32% / sub 3% / dec 11%
- how it ends: finish 66% (R1 36% / R2 21% / R3 9%) vs. decision 34%
- likeliest endings: Shamil Gaziev by decision (23%), Kennedy Nzechukwu by KO/TKO, round 1 (17%), Shamil Gaziev by KO/TKO, round 1 (12%)
- drivers (log-odds): diff_age -0.18, diff_strike_elo -0.17, diff_opp_elo_l5 +0.14, diff_grapple_elo +0.08, diff_td_def_l3 -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Shamil Gaziev by KO/TKO | 12.4% | 6.8% | 2.9% | **22.1%** |
| Shamil Gaziev by submission | 4.7% | 2.8% | 1.2% | **8.7%** |
| Kennedy Nzechukwu by KO/TKO | 17.2% | 10.3% | 4.5% | **32.1%** |
| Kennedy Nzechukwu by submission | 1.5% | 1.0% | 0.4% | **2.9%** |
| decision (either fighter) | — | — | — | **34.3%** |

## Nasrat Haqparast vs. Chris Padilla — Lightweight
P(Nasrat Haqparast wins) = 0.482  ->  no call (52% lean Chris Padilla)
- shipped number is the market-aware stack: vig-free market P(Nasrat Haqparast) = 0.500, skill-only model = 0.428 (gap -0.072)
- method: Nasrat Haqparast by KO 19% / sub 7% / dec 23%; Chris Padilla by KO 23% / sub 6% / dec 23%
- how it ends: finish 54% (R1 28% / R2 17% / R3 9%) vs. decision 46%
- likeliest endings: Chris Padilla by decision (23%), Nasrat Haqparast by decision (23%), Chris Padilla by KO/TKO, round 1 (13%)
- drivers (log-odds): diff_opp_elo_l5 +0.10, diff_slpm_l5 -0.08, diff_sapm_l5 -0.08, diff_age +0.06, diff_sig_acc_l5 -0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Nasrat Haqparast by KO/TKO | 8.8% | 6.2% | 3.5% | **18.5%** |
| Nasrat Haqparast by submission | 3.1% | 2.3% | 1.3% | **6.7%** |
| Chris Padilla by KO/TKO | 12.9% | 6.8% | 3.3% | **23.0%** |
| Chris Padilla by submission | 3.0% | 1.7% | 0.8% | **5.6%** |
| decision (either fighter) | — | — | — | **46.1%** |

## Marcio Barbosa vs. Ryan Kuse — Featherweight
P(Marcio Barbosa wins) = 0.874  ->  pick: Marcio Barbosa (87%)
- CAUTION: no UFC history for Ryan Kuse (debut or misspelled name?) — prediction is weak.
- shipped number is the market-aware stack: vig-free market P(Marcio Barbosa) = 0.855, skill-only model = 0.621 (gap -0.234)
- method: Marcio Barbosa by KO 41% / sub 13% / dec 33%; Ryan Kuse by KO 4% / sub 2% / dec 7%
- how it ends: finish 59% (R1 36% / R2 17% / R3 7%) vs. decision 41%
- likeliest endings: Marcio Barbosa by decision (33%), Marcio Barbosa by KO/TKO, round 1 (25%), Marcio Barbosa by KO/TKO, round 2 (11%)
- drivers (log-odds): diff_height_cm -0.44, f2_reach_cm +0.31, f1_reach_cm +0.31, diff_strike_elo -0.23, diff_age +0.12

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Marcio Barbosa by KO/TKO | 25.0% | 11.3% | 4.8% | **41.1%** |
| Marcio Barbosa by submission | 7.7% | 3.7% | 1.6% | **13.1%** |
| Ryan Kuse by KO/TKO | 2.1% | 1.0% | 0.5% | **3.6%** |
| Ryan Kuse by submission | 0.9% | 0.5% | 0.2% | **1.6%** |
| decision (either fighter) | — | — | — | **40.6%** |

## Gauge Young vs. Stan Dorsainvil — Lightweight
P(Gauge Young wins) = 0.596  ->  pick: Gauge Young (60%)
- CAUTION: no UFC history for Stan Dorsainvil (debut or misspelled name?) — prediction is weak.
- context: f2 flagged short notice — confidence dampened
- shipped number is the market-aware stack: vig-free market P(Gauge Young) = 0.598, skill-only model = 0.695 (gap +0.098)
- method: Gauge Young by KO 20% / sub 9% / dec 31%; Stan Dorsainvil by KO 12% / sub 8% / dec 20%
- how it ends: finish 49% (R1 26% / R2 15% / R3 7%) vs. decision 51%
- likeliest endings: Gauge Young by decision (31%), Stan Dorsainvil by decision (20%), Gauge Young by KO/TKO, round 1 (10%)
- drivers (log-odds): f2_reach_cm +0.36, diff_height_cm -0.33, f1_reach_cm +0.31, diff_strike_elo +0.21, diff_elo +0.10

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Gauge Young by KO/TKO | 10.4% | 6.1% | 3.1% | **19.6%** |
| Gauge Young by submission | 4.5% | 2.8% | 1.4% | **8.7%** |
| Stan Dorsainvil by KO/TKO | 7.0% | 3.8% | 1.7% | **12.5%** |
| Stan Dorsainvil by submission | 4.5% | 2.6% | 1.3% | **8.4%** |
| decision (either fighter) | — | — | — | **50.8%** |

## Jackson McVey vs. Wes Schultz — Middleweight
P(Jackson McVey wins) = 0.634  ->  pick: Jackson McVey (63%)
- shipped number is the market-aware stack: vig-free market P(Jackson McVey) = 0.616, skill-only model = 0.566 (gap -0.050)
- method: Jackson McVey by KO 25% / sub 26% / dec 12%; Wes Schultz by KO 9% / sub 19% / dec 8%
- how it ends: finish 80% (R1 46% / R2 24% / R3 11%) vs. decision 20%
- likeliest endings: Jackson McVey by KO/TKO, round 1 (14%), Jackson McVey by submission, round 1 (14%), Jackson McVey by decision (12%)
- drivers (log-odds): diff_strike_elo +0.34, diff_age +0.17, f2_sig_def_l5 -0.07, diff_elo -0.07, diff_slpm_l5 -0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Jackson McVey by KO/TKO | 14.3% | 7.7% | 3.4% | **25.5%** |
| Jackson McVey by submission | 14.3% | 8.3% | 3.7% | **26.3%** |
| Wes Schultz by KO/TKO | 5.6% | 2.7% | 1.1% | **9.4%** |
| Wes Schultz by submission | 11.3% | 5.7% | 2.3% | **19.4%** |
| decision (either fighter) | — | — | — | **19.5%** |

## Shanelle Dyer vs. Elise Reed — Women's Strawweight
P(Shanelle Dyer wins) = 0.897  ->  pick: Shanelle Dyer (90%)
- shipped number is the market-aware stack: vig-free market P(Shanelle Dyer) = 0.858, skill-only model = 0.791 (gap -0.066)
- method: Shanelle Dyer by KO 29% / sub 14% / dec 47%; Elise Reed by KO 1% / sub 3% / dec 6%
- how it ends: finish 46% (R1 25% / R2 14% / R3 7%) vs. decision 54%
- likeliest endings: Shanelle Dyer by decision (47%), Shanelle Dyer by KO/TKO, round 1 (16%), Shanelle Dyer by KO/TKO, round 2 (9%)
- drivers (log-odds): diff_age +0.39, diff_strike_elo +0.24, diff_grapple_elo +0.11, diff_elo +0.10, f2_age +0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Shanelle Dyer by KO/TKO | 15.7% | 8.6% | 4.3% | **28.6%** |
| Shanelle Dyer by submission | 7.4% | 4.3% | 2.1% | **13.8%** |
| Elise Reed by KO/TKO | 0.7% | 0.5% | 0.2% | **1.4%** |
| Elise Reed by submission | 1.2% | 0.9% | 0.5% | **2.6%** |
| decision (either fighter) | — | — | — | **53.7%** |

---
*Simulation/educational project. No betting advice. The market knows more than this model.*