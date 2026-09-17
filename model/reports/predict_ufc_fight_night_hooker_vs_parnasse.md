# UFC Fight Night: Hooker vs. Parnasse — 2026-09-05

Point-in-time predictions from 8690 historical fights. Educational output — NOT betting advice; the backtest shows this model does not beat the market.

## Salahdine Parnasse vs. Dan Hooker — Lightweight
P(Salahdine Parnasse wins) = 0.736  ->  pick: Salahdine Parnasse (74%)
- CAUTION: no UFC history for Salahdine Parnasse (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 23-2-0.
- context: YouTube lean -0.77 (n=7) nudged p by -0.046 — skill was near a coin flip
- research: Last fights: Dan Hooker lost last time out.
- skill-only research model P(Salahdine Parnasse) = 0.559; vig-free market = 0.822 (gap -0.262). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Salahdine Parnasse by KO 38% / sub 19% / dec 16%; Dan Hooker by KO 10% / sub 5% / dec 11%
- pick outcome: Salahdine Parnasse by KO/TKO, round 1 (method 38%; round given method 48%; exact outcome 18%)
- how it ends: finish 72% (R1 32% / R2 20% / R3 11% / R4 6% / R5 4%) vs. decision 28%
- likeliest endings: Salahdine Parnasse by KO/TKO, round 1 (18%), Salahdine Parnasse by decision (16%), Dan Hooker by decision (11%)
- drivers (log-odds): f2_reach_cm -0.38, diff_height_cm +0.30, f1_reach_cm -0.28, diff_strike_elo -0.21, diff_age +0.17

| ending | R1 | R2 | R3 | R4 | R5 | any round |
|---|---|---|---|---|---|---|
| Salahdine Parnasse by KO/TKO | 18.2% | 10.2% | 5.2% | 2.5% | 1.8% | **37.9%** |
| Salahdine Parnasse by submission | 8.4% | 5.2% | 3.1% | 1.6% | 0.9% | **19.3%** |
| Dan Hooker by KO/TKO | 4.0% | 3.0% | 1.7% | 0.9% | 0.8% | **10.4%** |
| Dan Hooker by submission | 1.6% | 1.3% | 0.9% | 0.5% | 0.3% | **4.6%** |
| decision (either fighter) | — | — | — | — | — | **27.8%** |

## Fares Ziam vs. Axel Sola — Lightweight
P(Fares Ziam wins) = 0.578  ->  no call (58% lean Fares Ziam)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Axel Sola is the volume striker (4.5 vs 2.5 SLpM).
- research: Form: Fares Ziam holds the quality-weighted form edge (hot vs hot over the last 5).
- research: Style record: Fares Ziam is 67% against strikers in the UFC.
- skill-only research model P(Fares Ziam) = 0.532; vig-free market = 0.580 (gap -0.049). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Fares Ziam by KO 17% / sub 10% / dec 31%; Axel Sola by KO 14% / sub 9% / dec 19%
- pick outcome: Fares Ziam by decision (31%)
- how it ends: finish 50% (R1 24% / R2 17% / R3 9%) vs. decision 50%
- likeliest endings: Fares Ziam by decision (31%), Axel Sola by decision (19%), Fares Ziam by KO/TKO, round 1 (8%)
- drivers (log-odds): diff_strike_elo +0.17, diff_elo +0.15, diff_opp_elo_l5 +0.12, diff_career_win_pct -0.10, diff_age -0.10

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Fares Ziam by KO/TKO | 7.9% | 6.1% | 3.6% | **17.5%** |
| Fares Ziam by submission | 4.2% | 3.5% | 2.1% | **9.8%** |
| Axel Sola by KO/TKO | 7.5% | 4.3% | 2.1% | **13.9%** |
| Axel Sola by submission | 4.8% | 2.9% | 1.4% | **9.0%** |
| decision (either fighter) | — | — | — | **49.8%** |

## Michael Page vs. Nursulton Ruziboev — Middleweight
P(Michael Page wins) = 0.635  ->  pick: Michael Page (64%)
- research: Style: both profile as strikers — a same-look fight.
- research: Last fights: Michael Page won last time out; Nursulton Ruziboev won last time out.
- research: Style record: Michael Page is 80% against strikers in the UFC.
- skill-only research model P(Michael Page) = 0.623; vig-free market = 0.611 (gap +0.011). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Michael Page by KO 25% / sub 7% / dec 32%; Nursulton Ruziboev by KO 12% / sub 10% / dec 15%
- pick outcome: Michael Page by decision (32%)
- how it ends: finish 53% (R1 26% / R2 17% / R3 10%) vs. decision 47%
- likeliest endings: Michael Page by decision (32%), Nursulton Ruziboev by decision (15%), Michael Page by KO/TKO, round 1 (11%)
- drivers (log-odds): diff_age -0.22, diff_strike_elo +0.19, diff_sig_acc_l5 +0.08, f2_form_l3 +0.08, diff_career_win_pct +0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Michael Page by KO/TKO | 10.9% | 8.4% | 5.3% | **24.6%** |
| Michael Page by submission | 2.8% | 2.3% | 1.5% | **6.6%** |
| Nursulton Ruziboev by KO/TKO | 6.8% | 3.7% | 1.7% | **12.2%** |
| Nursulton Ruziboev by submission | 5.2% | 3.0% | 1.4% | **9.6%** |
| decision (either fighter) | — | — | — | **47.0%** |

## Punahele Soriano vs. Daniil Donchenko — Welterweight
P(Punahele Soriano wins) = 0.300  ->  pick: Daniil Donchenko (70%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Daniil Donchenko is the volume striker (8.1 vs 4.9 SLpM).
- research: Form: Daniil Donchenko holds the quality-weighted form edge (hot vs hot over the last 5).
- research: Style record: Punahele Soriano is 70% against strikers in the UFC.
- skill-only research model P(Punahele Soriano) = 0.343; vig-free market = 0.326 (gap +0.016). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Punahele Soriano by KO 10% / sub 7% / dec 13%; Daniil Donchenko by KO 35% / sub 6% / dec 30%
- pick outcome: Daniil Donchenko by KO/TKO, round 1 (method 35%; round given method 59%; exact outcome 20%)
- how it ends: finish 57% (R1 32% / R2 18% / R3 7%) vs. decision 43%
- likeliest endings: Daniil Donchenko by decision (30%), Daniil Donchenko by KO/TKO, round 1 (20%), Punahele Soriano by decision (13%)
- drivers (log-odds): diff_age -0.35, diff_strike_elo -0.16, diff_career_win_pct -0.08, diff_td15_l5 +0.07, diff_sig_def_l5 -0.03

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Punahele Soriano by KO/TKO | 5.0% | 3.2% | 1.4% | **9.6%** |
| Punahele Soriano by submission | 3.5% | 2.4% | 1.1% | **7.0%** |
| Daniil Donchenko by KO/TKO | 20.2% | 10.3% | 4.1% | **34.6%** |
| Daniil Donchenko by submission | 3.1% | 1.7% | 0.7% | **5.5%** |
| decision (either fighter) | — | — | — | **43.2%** |

## Kurtis Campbell vs. Trevor Peek — Featherweight
P(Kurtis Campbell wins) = 0.803  ->  pick: Kurtis Campbell (80%)
- research: Style: both profile as strikers — a same-look fight.
- research: Wrestling contrast: Kurtis Campbell lands 5.4 takedowns/15 into Trevor Peek's 53% TDD.
- research: Form: Trevor Peek holds the quality-weighted form edge (cold vs mixed over the last 5).
- research: Style record: Trevor Peek is 33% against strikers in the UFC.
- skill-only research model P(Kurtis Campbell) = 0.719; vig-free market = 0.766 (gap -0.047). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Kurtis Campbell by KO 26% / sub 17% / dec 37%; Trevor Peek by KO 8% / sub 2% / dec 9%
- pick outcome: Kurtis Campbell by decision (37%)
- how it ends: finish 53% (R1 26% / R2 17% / R3 10%) vs. decision 47%
- likeliest endings: Kurtis Campbell by decision (37%), Kurtis Campbell by KO/TKO, round 1 (13%), Trevor Peek by decision (9%)
- drivers (log-odds): diff_age +0.23, diff_strike_elo -0.19, f2_pre_ufc_ko_rate +0.16, f1_pre_ufc_ko_rate +0.15, diff_td15_l5 +0.11

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Kurtis Campbell by KO/TKO | 12.7% | 8.3% | 4.6% | **25.6%** |
| Kurtis Campbell by submission | 8.2% | 5.8% | 3.2% | **17.3%** |
| Trevor Peek by KO/TKO | 4.2% | 2.6% | 1.4% | **8.2%** |
| Trevor Peek by submission | 1.1% | 0.7% | 0.4% | **2.2%** |
| decision (either fighter) | — | — | — | **46.8%** |

## Losene Keita vs. Muhammad Naimov — Featherweight
P(Losene Keita wins) = 0.779  ->  pick: Losene Keita (78%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Losene Keita is the volume striker (3.5 vs 1.9 SLpM).
- research: Form: Muhammad Naimov holds the quality-weighted form edge (cold vs mixed over the last 5).
- research: Style record: Muhammad Naimov is 80% against strikers in the UFC.
- research: Common opponents (1): Muhammad Naimov's record against them is better.
- skill-only research model P(Losene Keita) = 0.627; vig-free market = 0.763 (gap -0.137). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Losene Keita by KO 30% / sub 5% / dec 43%; Muhammad Naimov by KO 5% / sub 2% / dec 15%
- pick outcome: Losene Keita by decision (43%)
- how it ends: finish 42% (R1 23% / R2 13% / R3 6%) vs. decision 58%
- likeliest endings: Losene Keita by decision (43%), Losene Keita by KO/TKO, round 1 (17%), Muhammad Naimov by decision (15%)
- drivers (log-odds): diff_age +0.19, diff_strike_elo +0.16, diff_elo -0.12, diff_opp_elo_l5 +0.11, diff_career_win_pct +0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Losene Keita by KO/TKO | 16.8% | 8.9% | 4.1% | **29.8%** |
| Losene Keita by submission | 2.8% | 1.6% | 0.8% | **5.3%** |
| Muhammad Naimov by KO/TKO | 2.6% | 1.6% | 0.9% | **5.1%** |
| Muhammad Naimov by submission | 1.0% | 0.6% | 0.4% | **2.0%** |
| decision (either fighter) | — | — | — | **57.8%** |

## Morgan Charriere vs. Felipe Lima — Featherweight
P(Morgan Charriere wins) = 0.313  ->  pick: Felipe Lima (69%)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Felipe Lima holds the quality-weighted form edge (mixed vs hot over the last 5).
- research: Style record: Morgan Charriere is 40% against strikers in the UFC.
- skill-only research model P(Morgan Charriere) = 0.311; vig-free market = 0.359 (gap -0.048). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Morgan Charriere by KO 14% / sub 4% / dec 14%; Felipe Lima by KO 14% / sub 7% / dec 47%
- pick outcome: Felipe Lima by decision (47%)
- how it ends: finish 38% (R1 19% / R2 12% / R3 7%) vs. decision 62%
- likeliest endings: Felipe Lima by decision (47%), Morgan Charriere by decision (14%), Felipe Lima by KO/TKO, round 1 (7%)
- drivers (log-odds): diff_strike_elo -0.17, diff_age -0.16, f2_quality_win_rate -0.08, diff_opp_elo_l5 -0.07, diff_career_win_pct -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Morgan Charriere by KO/TKO | 6.1% | 4.3% | 3.2% | **13.7%** |
| Morgan Charriere by submission | 1.5% | 1.1% | 0.9% | **3.5%** |
| Felipe Lima by KO/TKO | 7.4% | 4.5% | 2.1% | **14.0%** |
| Felipe Lima by submission | 3.7% | 2.4% | 1.2% | **7.3%** |
| decision (either fighter) | — | — | — | **61.5%** |

## Mario Pinto vs. Ryan Spann — Heavyweight
P(Mario Pinto wins) = 0.796  ->  pick: Mario Pinto (80%)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Mario Pinto holds the quality-weighted form edge (hot vs mixed over the last 5).
- research: Style record: Ryan Spann is 57% against strikers in the UFC.
- skill-only research model P(Mario Pinto) = 0.792; vig-free market = 0.735 (gap +0.058). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Mario Pinto by KO 38% / sub 8% / dec 33%; Ryan Spann by KO 9% / sub 5% / dec 6%
- pick outcome: Mario Pinto by KO/TKO, round 1 (method 38%; round given method 57%; exact outcome 21%)
- how it ends: finish 60% (R1 33% / R2 19% / R3 8%) vs. decision 40%
- likeliest endings: Mario Pinto by decision (33%), Mario Pinto by KO/TKO, round 1 (21%), Mario Pinto by KO/TKO, round 2 (11%)
- drivers (log-odds): diff_age +0.20, diff_strike_elo -0.16, diff_td15_l5 +0.10, diff_career_win_pct +0.09, f2_career_streak +0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Mario Pinto by KO/TKO | 21.5% | 11.4% | 4.9% | **37.7%** |
| Mario Pinto by submission | 4.6% | 2.6% | 1.2% | **8.4%** |
| Ryan Spann by KO/TKO | 4.4% | 3.1% | 1.4% | **9.0%** |
| Ryan Spann by submission | 2.5% | 1.9% | 0.9% | **5.4%** |
| decision (either fighter) | — | — | — | **39.5%** |

## Oumar Sy vs. Modestas Bukauskas — Light Heavyweight
P(Oumar Sy wins) = 0.710  ->  pick: Oumar Sy (71%)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Modestas Bukauskas holds the quality-weighted form edge (mixed vs hot over the last 5).
- research: Style record: Oumar Sy is 50% against strikers in the UFC.
- research: Common opponents (1): Modestas Bukauskas's record against them is better.
- skill-only research model P(Oumar Sy) = 0.698; vig-free market = 0.670 (gap +0.029). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Oumar Sy by KO 34% / sub 13% / dec 24%; Modestas Bukauskas by KO 15% / sub 2% / dec 12%
- pick outcome: Oumar Sy by KO/TKO, round 1 (method 34%; round given method 58%; exact outcome 20%)
- how it ends: finish 64% (R1 35% / R2 20% / R3 9%) vs. decision 36%
- likeliest endings: Oumar Sy by decision (24%), Oumar Sy by KO/TKO, round 1 (20%), Modestas Bukauskas by decision (12%)
- drivers (log-odds): diff_style_reach_striker +0.22, diff_strike_elo +0.17, diff_age +0.11, diff_td15_l5 +0.10, diff_career_win_pct +0.10

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Oumar Sy by KO/TKO | 19.8% | 10.3% | 4.1% | **34.2%** |
| Oumar Sy by submission | 7.3% | 4.1% | 1.7% | **13.0%** |
| Modestas Bukauskas by KO/TKO | 7.4% | 5.1% | 2.6% | **15.0%** |
| Modestas Bukauskas by submission | 0.9% | 0.7% | 0.4% | **2.0%** |
| decision (either fighter) | — | — | — | **35.7%** |

## Nathaniel Wood vs. Pavel Andrusca — Featherweight
P(Nathaniel Wood wins) = 0.650  ->  pick: Nathaniel Wood (65%)
- CAUTION: no UFC history for Pavel Andrusca (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 8-0-0.
- context: f2 flagged short notice — confidence dampened
- research: Last fights: Nathaniel Wood won last time out.
- skill-only research model P(Nathaniel Wood) = 0.657; vig-free market = 0.719 (gap -0.062). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Nathaniel Wood by KO 21% / sub 11% / dec 33%; Pavel Andrusca by KO 19% / sub 3% / dec 12%
- pick outcome: Nathaniel Wood by decision (33%)
- how it ends: finish 55% (R1 34% / R2 14% / R3 6%) vs. decision 45%
- likeliest endings: Nathaniel Wood by decision (33%), Nathaniel Wood by KO/TKO, round 1 (13%), Pavel Andrusca by KO/TKO, round 1 (13%)
- drivers (log-odds): diff_strike_elo +0.41, diff_pre_ufc_finish_loss_rate -0.32, diff_height_cm -0.29, f2_reach_cm +0.26, f1_reach_cm +0.22

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Nathaniel Wood by KO/TKO | 12.8% | 5.7% | 2.5% | **21.1%** |
| Nathaniel Wood by submission | 6.4% | 3.1% | 1.4% | **10.9%** |
| Pavel Andrusca by KO/TKO | 12.8% | 4.8% | 1.9% | **19.5%** |
| Pavel Andrusca by submission | 2.1% | 0.9% | 0.4% | **3.4%** |
| decision (either fighter) | — | — | — | **45.2%** |

## Fabia Sintes vs. Michael Aljarouj — Flyweight
P(Fabia Sintes wins) = 0.478  ->  no call (52% lean Michael Aljarouj)
- CAUTION: no UFC history for Fabia Sintes (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 11-3-0.
- CAUTION: no UFC history for Michael Aljarouj (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 13-3-0.
- skill-only research model P(Fabia Sintes) = 0.496; vig-free market = 0.474 (gap +0.022). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Fabia Sintes by KO 12% / sub 15% / dec 21%; Michael Aljarouj by KO 22% / sub 9% / dec 22%
- pick outcome: Michael Aljarouj by decision (22%)
- how it ends: finish 57% (R1 29% / R2 18% / R3 10%) vs. decision 43%
- likeliest endings: Michael Aljarouj by decision (22%), Fabia Sintes by decision (21%), Michael Aljarouj by KO/TKO, round 1 (12%)
- drivers (log-odds): diff_age -0.10, diff_career_win_pct -0.07, diff_career_fights_24m +0.03, f1_career_streak +0.03, f2_career_layoff_days +0.02

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Fabia Sintes by KO/TKO | 6.0% | 3.7% | 2.1% | **11.8%** |
| Fabia Sintes by submission | 7.4% | 4.9% | 2.8% | **15.1%** |
| Michael Aljarouj by KO/TKO | 11.6% | 6.5% | 3.5% | **21.7%** |
| Michael Aljarouj by submission | 4.4% | 2.7% | 1.5% | **8.6%** |
| decision (either fighter) | — | — | — | **42.9%** |

## Nora Cornolle vs. Klaudia Sygula — Women's Bantamweight
P(Nora Cornolle wins) = 0.483  ->  no call (52% lean Klaudia Sygula)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Klaudia Sygula is the volume striker (7.3 vs 2.8 SLpM).
- research: Form: Klaudia Sygula holds the quality-weighted form edge (mixed vs hot over the last 5).
- research: Style record: Nora Cornolle is 50% against strikers in the UFC.
- research: Common opponents (1): Nora Cornolle's record against them is better.
- skill-only research model P(Nora Cornolle) = 0.480; vig-free market = 0.490 (gap -0.010). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Nora Cornolle by KO 10% / sub 8% / dec 31%; Klaudia Sygula by KO 6% / sub 7% / dec 39%
- pick outcome: Klaudia Sygula by decision (39%)
- how it ends: finish 31% (R1 15% / R2 10% / R3 6%) vs. decision 69%
- likeliest endings: Klaudia Sygula by decision (39%), Nora Cornolle by decision (31%), Nora Cornolle by KO/TKO, round 1 (5%)
- drivers (log-odds): diff_age -0.40, diff_strike_elo +0.18, diff_age_past_prime -0.08, diff_career_win_pct -0.08, diff_elo -0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Nora Cornolle by KO/TKO | 5.2% | 3.0% | 1.6% | **9.8%** |
| Nora Cornolle by submission | 4.0% | 2.5% | 1.3% | **7.9%** |
| Klaudia Sygula by KO/TKO | 2.5% | 1.8% | 1.2% | **5.6%** |
| Klaudia Sygula by submission | 3.2% | 2.4% | 1.7% | **7.3%** |
| decision (either fighter) | — | — | — | **69.4%** |

## Luis Felipe Dias vs. Matthieu Duclos — Middleweight
P(Luis Felipe Dias wins) = 0.526  ->  no call (53% lean Luis Felipe Dias)
- CAUTION: no UFC history for Matthieu Duclos (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 10-3-0.
- research: Last fights: Luis Felipe Dias won last time out.
- skill-only research model P(Luis Felipe Dias) = 0.579; vig-free market = 0.490 (gap +0.090). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Luis Felipe Dias by KO 30% / sub 10% / dec 13%; Matthieu Duclos by KO 25% / sub 4% / dec 19%
- pick outcome: Luis Felipe Dias by KO/TKO, round 1 (method 30%; round given method 59%; exact outcome 17%)
- how it ends: finish 68% (R1 39% / R2 20% / R3 9%) vs. decision 32%
- likeliest endings: Matthieu Duclos by decision (19%), Luis Felipe Dias by KO/TKO, round 1 (17%), Matthieu Duclos by KO/TKO, round 1 (14%)
- drivers (log-odds): f1_reach_cm -0.31, diff_height_cm +0.29, f2_reach_cm -0.28, diff_strike_elo +0.21, diff_career_win_pct +0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Luis Felipe Dias by KO/TKO | 17.4% | 8.6% | 3.7% | **29.7%** |
| Luis Felipe Dias by submission | 5.4% | 2.8% | 1.2% | **9.5%** |
| Matthieu Duclos by KO/TKO | 13.9% | 7.5% | 3.7% | **25.0%** |
| Matthieu Duclos by submission | 2.0% | 1.2% | 0.6% | **3.8%** |
| decision (either fighter) | — | — | — | **32.0%** |

## Delphine Benouaich vs. Sofia Montenegro — Women's Strawweight
P(Delphine Benouaich wins) = 0.513  ->  no call (51% lean Delphine Benouaich)
- CAUTION: no UFC history for Delphine Benouaich (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 7-2-0.
- CAUTION: no UFC history for Sofia Montenegro (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 6-2-0.
- skill-only research model P(Delphine Benouaich) = 0.410; vig-free market = 0.568 (gap -0.158). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Delphine Benouaich by KO 18% / sub 9% / dec 25%; Sofia Montenegro by KO 13% / sub 9% / dec 26%
- pick outcome: Delphine Benouaich by decision (25%)
- how it ends: finish 49% (R1 26% / R2 15% / R3 8%) vs. decision 51%
- likeliest endings: Sofia Montenegro by decision (26%), Delphine Benouaich by decision (25%), Delphine Benouaich by KO/TKO, round 1 (10%)
- drivers (log-odds): f1_reach_cm -0.40, f2_reach_cm -0.34, diff_height_cm +0.31, diff_age -0.12, diff_style_reach_striker -0.07

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Delphine Benouaich by KO/TKO | 9.7% | 5.4% | 2.7% | **17.7%** |
| Delphine Benouaich by submission | 4.6% | 2.7% | 1.4% | **8.7%** |
| Sofia Montenegro by KO/TKO | 7.1% | 4.0% | 2.1% | **13.2%** |
| Sofia Montenegro by submission | 4.7% | 2.8% | 1.5% | **9.1%** |
| decision (either fighter) | — | — | — | **51.2%** |

---
*Simulation/educational project. No betting advice. The market knows more than this model.*