# UFC 330: Makhachev vs. Machado Garry — 2026-08-15

Point-in-time predictions from 8665 historical fights. Educational output — NOT betting advice; the backtest shows this model does not beat the market.

Name spellings resolved against ufcstats: Kauê Fernandes -> Kaue Fernandes

## Islam Makhachev vs. Ian Machado Garry — Welterweight
P(Islam Makhachev wins) = 0.759  ->  pick: Islam Makhachev (76%)
- context: YouTube lean -0.56 (n=10) noted but not applied — skill already decisive (0.58)
- shipped number is the market-aware stack: vig-free market P(Islam Makhachev) = 0.741, skill-only model = 0.582 (gap -0.159)
- method: Islam Makhachev by KO 15% / sub 24% / dec 37%; Ian Machado Garry by KO 10% / sub 2% / dec 12%
- how it ends: finish 51% (R1 17% / R2 15% / R3 10% / R4 5% / R5 4%) vs. decision 49%
- likeliest endings: Islam Makhachev by decision (37%), Ian Machado Garry by decision (12%), Islam Makhachev by submission, round 1 (7%)
- drivers (log-odds): diff_age -0.22, diff_elo +0.19, diff_grapple_elo +0.13, diff_opp_elo_l5 +0.11, f1_age -0.10

| ending | R1 | R2 | R3 | R4 | R5 | any round |
|---|---|---|---|---|---|---|
| Islam Makhachev by KO/TKO | 5.4% | 4.4% | 2.7% | 1.5% | 1.3% | **15.3%** |
| Islam Makhachev by submission | 7.1% | 6.8% | 4.8% | 2.8% | 2.0% | **23.6%** |
| Ian Machado Garry by KO/TKO | 3.9% | 2.9% | 1.7% | 0.9% | 0.8% | **10.1%** |
| Ian Machado Garry by submission | 0.7% | 0.6% | 0.4% | 0.2% | 0.2% | **2.0%** |
| decision (either fighter) | — | — | — | — | — | **49.1%** |

## Mackenzie Dern vs. Gillian Robertson — Women's Strawweight
P(Mackenzie Dern wins) = 0.643  ->  pick: Mackenzie Dern (64%)
- shipped number is the market-aware stack: vig-free market P(Mackenzie Dern) = 0.657, skill-only model = 0.449 (gap -0.208)
- method: Mackenzie Dern by KO 8% / sub 22% / dec 34%; Gillian Robertson by KO 8% / sub 6% / dec 22%
- how it ends: finish 44% (R1 16% / R2 13% / R3 8% / R4 4% / R5 3%) vs. decision 56%
- likeliest endings: Mackenzie Dern by decision (34%), Gillian Robertson by decision (22%), Mackenzie Dern by submission, round 1 (8%)
- drivers (log-odds): diff_grapple_elo -0.15, diff_age -0.12, diff_opp_elo_l5 +0.12, diff_strike_elo +0.12, diff_sapm_l5 -0.07

| ending | R1 | R2 | R3 | R4 | R5 | any round |
|---|---|---|---|---|---|---|
| Mackenzie Dern by KO/TKO | 3.3% | 2.4% | 1.3% | 0.7% | 0.5% | **8.1%** |
| Mackenzie Dern by submission | 7.8% | 6.4% | 4.1% | 2.2% | 1.3% | **21.8%** |
| Gillian Robertson by KO/TKO | 2.7% | 2.3% | 1.4% | 0.8% | 0.7% | **7.9%** |
| Gillian Robertson by submission | 1.9% | 1.8% | 1.3% | 0.7% | 0.5% | **6.2%** |
| decision (either fighter) | — | — | — | — | — | **56.0%** |

## Jalin Turner vs. Kaue Fernandes — Lightweight
P(Jalin Turner wins) = 0.581  ->  pick: Jalin Turner (58%)
- shipped number is the market-aware stack: vig-free market P(Jalin Turner) = 0.583, skill-only model = 0.493 (gap -0.090)
- method: Jalin Turner by KO 20% / sub 15% / dec 23%; Kaue Fernandes by KO 18% / sub 5% / dec 19%
- how it ends: finish 58% (R1 32% / R2 18% / R3 8%) vs. decision 42%
- likeliest endings: Jalin Turner by decision (23%), Kaue Fernandes by decision (19%), Kaue Fernandes by KO/TKO, round 1 (11%)
- drivers (log-odds): diff_sapm_l5 -0.13, diff_elo +0.10, diff_opp_elo_l5 +0.08, diff_reach_cm +0.07, diff_strike_elo +0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Jalin Turner by KO/TKO | 10.5% | 6.4% | 3.3% | **20.3%** |
| Jalin Turner by submission | 7.5% | 4.9% | 2.5% | **15.0%** |
| Kaue Fernandes by KO/TKO | 10.9% | 5.2% | 2.1% | **18.1%** |
| Kaue Fernandes by submission | 2.8% | 1.4% | 0.6% | **4.8%** |
| decision (either fighter) | — | — | — | **41.9%** |

## Mansur Abdul-Malik vs. Dustin Stoltzfus — Middleweight
P(Mansur Abdul-Malik wins) = 0.862  ->  pick: Mansur Abdul-Malik (86%)
- shipped number is the market-aware stack: vig-free market P(Mansur Abdul-Malik) = 0.837, skill-only model = 0.661 (gap -0.176)
- method: Mansur Abdul-Malik by KO 48% / sub 17% / dec 22%; Dustin Stoltzfus by KO 4% / sub 2% / dec 8%
- how it ends: finish 70% (R1 40% / R2 22% / R3 9%) vs. decision 30%
- likeliest endings: Mansur Abdul-Malik by KO/TKO, round 1 (28%), Mansur Abdul-Malik by decision (22%), Mansur Abdul-Malik by KO/TKO, round 2 (14%)
- drivers (log-odds): diff_age +0.26, diff_elo +0.20, f1_age +0.11, diff_strike_elo -0.08, diff_opp_elo_l5 -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Mansur Abdul-Malik by KO/TKO | 27.5% | 14.4% | 5.7% | **47.7%** |
| Mansur Abdul-Malik by submission | 9.3% | 5.2% | 2.1% | **16.6%** |
| Dustin Stoltzfus by KO/TKO | 1.8% | 1.4% | 0.7% | **4.0%** |
| Dustin Stoltzfus by submission | 0.9% | 0.8% | 0.4% | **2.1%** |
| decision (either fighter) | — | — | — | **29.5%** |

## Edson Barboza vs. Esteban Ribovics — Lightweight
P(Edson Barboza wins) = 0.133  ->  pick: Esteban Ribovics (87%)
- shipped number is the market-aware stack: vig-free market P(Edson Barboza) = 0.168, skill-only model = 0.278 (gap +0.110)
- method: Edson Barboza by KO 4% / sub 2% / dec 7%; Esteban Ribovics by KO 30% / sub 5% / dec 52%
- how it ends: finish 41% (R1 21% / R2 13% / R3 7%) vs. decision 59%
- likeliest endings: Esteban Ribovics by decision (52%), Esteban Ribovics by KO/TKO, round 1 (16%), Esteban Ribovics by KO/TKO, round 2 (9%)
- drivers (log-odds): diff_age -0.38, diff_strike_elo -0.15, f1_age -0.14, f2_age -0.08, bout_max_age -0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Edson Barboza by KO/TKO | 2.1% | 1.3% | 0.9% | **4.3%** |
| Edson Barboza by submission | 0.9% | 0.6% | 0.4% | **1.9%** |
| Esteban Ribovics by KO/TKO | 15.6% | 9.1% | 5.1% | **29.8%** |
| Esteban Ribovics by submission | 2.7% | 1.7% | 1.0% | **5.4%** |
| decision (either fighter) | — | — | — | **58.6%** |

## Chidi Njokuani vs. Joel Alvarez — Welterweight
P(Chidi Njokuani wins) = 0.615  ->  pick: Chidi Njokuani (62%)
- context: f2 flagged late replacement — confidence dampened
- shipped number is the market-aware stack: vig-free market P(Chidi Njokuani) = 0.722, skill-only model = 0.333 (gap -0.389)
- method: Chidi Njokuani by KO 28% / sub 6% / dec 28%; Joel Alvarez by KO 20% / sub 8% / dec 11%
- how it ends: finish 61% (R1 32% / R2 20% / R3 9%) vs. decision 39%
- likeliest endings: Chidi Njokuani by decision (28%), Chidi Njokuani by KO/TKO, round 1 (14%), Joel Alvarez by KO/TKO, round 1 (11%)
- drivers (log-odds): diff_elo -0.16, diff_age -0.15, diff_opp_elo_l5 -0.12, diff_strike_elo +0.10, f2_age -0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Chidi Njokuani by KO/TKO | 14.0% | 9.4% | 4.6% | **27.9%** |
| Chidi Njokuani by submission | 2.7% | 2.0% | 1.0% | **5.6%** |
| Joel Alvarez by KO/TKO | 11.0% | 6.0% | 2.6% | **19.6%** |
| Joel Alvarez by submission | 4.3% | 2.6% | 1.1% | **8.1%** |
| decision (either fighter) | — | — | — | **38.8%** |

## Charles Johnson vs. Eduardo Chapolin — Catch Weight
P(Charles Johnson wins) = 0.506  ->  pick: Charles Johnson (51%)
- CAUTION: no UFC history for Eduardo Chapolin (debut or misspelled name?) — prediction is weak.
- context: f2 flagged short notice — confidence dampened
- context: YouTube lean -0.16 (n=8) nudged p by -0.009 — skill was near a coin flip
- shipped number is the market-aware stack: vig-free market P(Charles Johnson) = 0.526, skill-only model = 0.493 (gap -0.033)
- method: Charles Johnson by KO 14% / sub 5% / dec 31%; Eduardo Chapolin by KO 14% / sub 10% / dec 25%
- how it ends: finish 44% (R1 24% / R2 13% / R3 7%) vs. decision 56%
- likeliest endings: Charles Johnson by decision (31%), Eduardo Chapolin by decision (25%), Eduardo Chapolin by KO/TKO, round 1 (8%)
- drivers (log-odds): diff_age -0.16, diff_strike_elo +0.14, f1_age -0.09, diff_elo +0.07, diff_grapple_elo -0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Charles Johnson by KO/TKO | 6.9% | 4.3% | 2.5% | **13.7%** |
| Charles Johnson by submission | 2.6% | 1.8% | 1.0% | **5.4%** |
| Eduardo Chapolin by KO/TKO | 8.3% | 4.0% | 1.8% | **14.1%** |
| Eduardo Chapolin by submission | 5.8% | 3.1% | 1.4% | **10.4%** |
| decision (either fighter) | — | — | — | **56.4%** |

## Donte Johnson vs. Eric McConico — Middleweight
P(Donte Johnson wins) = 0.758  ->  pick: Donte Johnson (76%)
- context: YouTube lean +0.60 (n=5) noted but not applied — skill already decisive (0.74)
- shipped number is the market-aware stack: vig-free market P(Donte Johnson) = 0.696, skill-only model = 0.741 (gap +0.045)
- method: Donte Johnson by KO 20% / sub 13% / dec 43%; Eric McConico by KO 9% / sub 4% / dec 12%
- how it ends: finish 45% (R1 24% / R2 15% / R3 7%) vs. decision 55%
- likeliest endings: Donte Johnson by decision (43%), Eric McConico by decision (12%), Donte Johnson by KO/TKO, round 1 (11%)
- drivers (log-odds): diff_age +0.35, diff_strike_elo +0.11, diff_elo +0.10, diff_grapple_elo +0.10, f1_age +0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Donte Johnson by KO/TKO | 11.1% | 6.4% | 2.6% | **20.2%** |
| Donte Johnson by submission | 6.7% | 4.2% | 1.7% | **12.6%** |
| Eric McConico by KO/TKO | 4.2% | 3.1% | 1.8% | **9.0%** |
| Eric McConico by submission | 1.6% | 1.2% | 0.7% | **3.5%** |
| decision (either fighter) | — | — | — | **54.7%** |

## Vicente Luque vs. Tresean Gore — Middleweight
P(Vicente Luque wins) = 0.491  ->  pick: Tresean Gore (51%)
- shipped number is the market-aware stack: vig-free market P(Vicente Luque) = 0.474, skill-only model = 0.556 (gap +0.083)
- method: Vicente Luque by KO 17% / sub 10% / dec 22%; Tresean Gore by KO 28% / sub 7% / dec 15%
- how it ends: finish 63% (R1 33% / R2 20% / R3 9%) vs. decision 37%
- likeliest endings: Vicente Luque by decision (22%), Tresean Gore by decision (15%), Tresean Gore by KO/TKO, round 1 (15%)
- drivers (log-odds): diff_strike_elo +0.22, diff_elo +0.21, diff_td_acc_l5 -0.12, diff_age -0.12, diff_opp_elo_l5 +0.11

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Vicente Luque by KO/TKO | 9.5% | 5.4% | 2.5% | **17.3%** |
| Vicente Luque by submission | 5.1% | 3.2% | 1.5% | **9.8%** |
| Tresean Gore by KO/TKO | 14.9% | 9.3% | 4.0% | **28.2%** |
| Tresean Gore by submission | 3.8% | 2.5% | 1.1% | **7.4%** |
| decision (either fighter) | — | — | — | **37.3%** |

## Rafael Tobias vs. Lucas Fernando — Light Heavyweight
P(Rafael Tobias wins) = 0.292  ->  pick: Lucas Fernando (71%)
- CAUTION: no UFC history for Lucas Fernando (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 13-3-0.
- shipped number is the market-aware stack: vig-free market P(Rafael Tobias) = 0.282, skill-only model = 0.538 (gap +0.256)
- method: Rafael Tobias by KO 12% / sub 6% / dec 12%; Lucas Fernando by KO 29% / sub 11% / dec 31%
- how it ends: finish 57% (R1 32% / R2 17% / R3 8%) vs. decision 43%
- likeliest endings: Lucas Fernando by decision (31%), Lucas Fernando by KO/TKO, round 1 (16%), Rafael Tobias by decision (12%)
- drivers (log-odds): diff_age +0.25, diff_elo -0.09, diff_reach_cm -0.06, f2_age +0.05, diff_grapple_elo +0.05

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Rafael Tobias by KO/TKO | 6.6% | 3.5% | 1.6% | **11.7%** |
| Rafael Tobias by submission | 3.1% | 1.8% | 0.8% | **5.7%** |
| Lucas Fernando by KO/TKO | 16.4% | 8.4% | 4.0% | **28.9%** |
| Lucas Fernando by submission | 5.9% | 3.3% | 1.6% | **10.8%** |
| decision (either fighter) | — | — | — | **42.9%** |

## Neil Magny vs. Ramiz Brahimaj — Welterweight
P(Neil Magny wins) = 0.469  ->  pick: Ramiz Brahimaj (53%)
- shipped number is the market-aware stack: vig-free market P(Neil Magny) = 0.449, skill-only model = 0.567 (gap +0.119)
- method: Neil Magny by KO 14% / sub 7% / dec 25%; Ramiz Brahimaj by KO 16% / sub 12% / dec 25%
- how it ends: finish 50% (R1 27% / R2 16% / R3 8%) vs. decision 50%
- likeliest endings: Neil Magny by decision (25%), Ramiz Brahimaj by decision (25%), Ramiz Brahimaj by KO/TKO, round 1 (10%)
- drivers (log-odds): diff_elo +0.26, diff_reach_cm +0.18, diff_strike_elo +0.12, diff_age -0.12, diff_opp_elo_l5 +0.11

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Neil Magny by KO/TKO | 6.4% | 4.9% | 2.9% | **14.2%** |
| Neil Magny by submission | 3.2% | 2.7% | 1.6% | **7.5%** |
| Ramiz Brahimaj by KO/TKO | 10.0% | 4.6% | 1.7% | **16.3%** |
| Ramiz Brahimaj by submission | 7.2% | 3.6% | 1.4% | **12.2%** |
| decision (either fighter) | — | — | — | **49.9%** |

## Jeremiah Wells vs. Myktybek Orolbai — Welterweight
P(Jeremiah Wells wins) = 0.104  ->  pick: Myktybek Orolbai (90%)
- shipped number is the market-aware stack: vig-free market P(Jeremiah Wells) = 0.124, skill-only model = 0.337 (gap +0.213)
- method: Jeremiah Wells by KO 4% / sub 2% / dec 5%; Myktybek Orolbai by KO 34% / sub 23% / dec 33%
- how it ends: finish 62% (R1 30% / R2 21% / R3 11%) vs. decision 38%
- likeliest endings: Myktybek Orolbai by decision (33%), Myktybek Orolbai by KO/TKO, round 1 (16%), Myktybek Orolbai by KO/TKO, round 2 (11%)
- drivers (log-odds): diff_age -0.35, diff_strike_elo +0.23, diff_elo -0.16, f2_age -0.11, f1_age -0.11

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Jeremiah Wells by KO/TKO | 1.8% | 1.2% | 0.7% | **3.7%** |
| Jeremiah Wells by submission | 0.9% | 0.7% | 0.4% | **2.0%** |
| Myktybek Orolbai by KO/TKO | 16.4% | 11.2% | 5.9% | **33.5%** |
| Myktybek Orolbai by submission | 10.7% | 7.9% | 4.1% | **22.7%** |
| decision (either fighter) | — | — | — | **38.1%** |

---
*Simulation/educational project. No betting advice. The market knows more than this model.*