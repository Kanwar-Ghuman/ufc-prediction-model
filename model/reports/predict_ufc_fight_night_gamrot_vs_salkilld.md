# UFC Fight Night: Gamrot vs. Salkilld — 2026-08-08

Point-in-time predictions from 8653 historical fights. Educational output — NOT betting advice; the backtest shows this model does not beat the market.

## Mateusz Gamrot vs. Quillan Salkilld — Lightweight
P(Mateusz Gamrot wins) = 0.407  ->  pick: Quillan Salkilld (59%)
- context: YouTube lean +0.83 (n=8) noted but not applied — skill already decisive (0.40)
- shipped number is the market-aware stack: vig-free market P(Mateusz Gamrot) = 0.438, skill-only model = 0.398 (gap -0.040)
- method: Mateusz Gamrot by KO 16% / sub 8% / dec 16%; Quillan Salkilld by KO 41% / sub 7% / dec 12%
- how it ends: finish 72% (R1 28% / R2 20% / R3 12% / R4 7% / R5 5%) vs. decision 28%
- likeliest endings: Quillan Salkilld by KO/TKO, round 1 (18%), Mateusz Gamrot by decision (16%), Quillan Salkilld by decision (12%)
- drivers (log-odds): diff_age -0.37, diff_opp_elo_l5 +0.12, diff_strike_elo +0.10, f2_age -0.09, f1_age -0.08

| ending | R1 | R2 | R3 | R4 | R5 | any round |
|---|---|---|---|---|---|---|
| Mateusz Gamrot by KO/TKO | 5.5% | 4.7% | 2.9% | 1.6% | 1.5% | **16.2%** |
| Mateusz Gamrot by submission | 2.2% | 2.3% | 1.7% | 1.0% | 0.8% | **8.0%** |
| Quillan Salkilld by KO/TKO | 17.6% | 11.2% | 6.3% | 3.3% | 2.5% | **40.9%** |
| Quillan Salkilld by submission | 2.4% | 1.8% | 1.2% | 0.7% | 0.4% | **6.6%** |
| decision (either fighter) | — | — | — | — | — | **28.4%** |

## Billy Quarantillo vs. Diego Ferreira — Lightweight
P(Billy Quarantillo wins) = 0.313  ->  pick: Diego Ferreira (69%)
- shipped number is the market-aware stack: vig-free market P(Billy Quarantillo) = 0.349, skill-only model = 0.368 (gap +0.019)
- method: Billy Quarantillo by KO 14% / sub 5% / dec 13%; Diego Ferreira by KO 39% / sub 10% / dec 20%
- how it ends: finish 68% (R1 35% / R2 22% / R3 11%) vs. decision 32%
- likeliest endings: Diego Ferreira by KO/TKO, round 1 (21%), Diego Ferreira by decision (20%), Billy Quarantillo by decision (13%)
- drivers (log-odds): diff_age +0.14, diff_elo -0.12, diff_strike_elo -0.11, diff_opp_elo_l5 -0.10, f1_layoff_days -0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Billy Quarantillo by KO/TKO | 7.1% | 4.3% | 2.3% | **13.7%** |
| Billy Quarantillo by submission | 2.5% | 1.7% | 0.9% | **5.1%** |
| Diego Ferreira by KO/TKO | 20.8% | 12.4% | 5.9% | **39.1%** |
| Diego Ferreira by submission | 4.9% | 3.3% | 1.6% | **9.8%** |
| decision (either fighter) | — | — | — | **32.4%** |

## Darren Elkins vs. Yadier del Valle — Featherweight
P(Darren Elkins wins) = 0.215  ->  pick: Yadier del Valle (79%)
- context: YouTube lean -0.50 (n=4) noted but not applied — skill already decisive (0.29)
- shipped number is the market-aware stack: vig-free market P(Darren Elkins) = 0.265, skill-only model = 0.289 (gap +0.025)
- method: Darren Elkins by KO 6% / sub 7% / dec 9%; Yadier del Valle by KO 45% / sub 12% / dec 22%
- how it ends: finish 69% (R1 39% / R2 21% / R3 10%) vs. decision 31%
- likeliest endings: Yadier del Valle by KO/TKO, round 1 (27%), Yadier del Valle by decision (22%), Yadier del Valle by KO/TKO, round 2 (13%)
- drivers (log-odds): diff_age -0.33, diff_strike_elo -0.15, f2_age -0.15, f1_age -0.10, diff_elo +0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Darren Elkins by KO/TKO | 2.7% | 1.9% | 1.1% | **5.7%** |
| Darren Elkins by submission | 3.0% | 2.3% | 1.4% | **6.8%** |
| Yadier del Valle by KO/TKO | 26.6% | 12.8% | 5.5% | **44.9%** |
| Yadier del Valle by submission | 6.7% | 3.5% | 1.5% | **11.7%** |
| decision (either fighter) | — | — | — | **30.9%** |

## Amanda Lemos vs. Alexia Thainara — Women's Strawweight
P(Amanda Lemos wins) = 0.243  ->  pick: Alexia Thainara (76%)
- shipped number is the market-aware stack: vig-free market P(Amanda Lemos) = 0.279, skill-only model = 0.353 (gap +0.074)
- method: Amanda Lemos by KO 6% / sub 3% / dec 15%; Alexia Thainara by KO 11% / sub 17% / dec 48%
- how it ends: finish 37% (R1 19% / R2 12% / R3 6%) vs. decision 63%
- likeliest endings: Alexia Thainara by decision (48%), Amanda Lemos by decision (15%), Alexia Thainara by submission, round 1 (8%)
- drivers (log-odds): diff_age -0.36, diff_opp_elo_l5 +0.15, f1_age -0.14, diff_strike_elo +0.12, f2_age -0.10

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Amanda Lemos by KO/TKO | 3.2% | 2.0% | 1.0% | **6.3%** |
| Amanda Lemos by submission | 1.4% | 1.0% | 0.5% | **2.9%** |
| Alexia Thainara by KO/TKO | 6.1% | 3.7% | 1.7% | **11.5%** |
| Alexia Thainara by submission | 8.5% | 5.5% | 2.5% | **16.5%** |
| decision (either fighter) | — | — | — | **62.8%** |

## Ty Miller vs. Billy Ray Goff — Welterweight
P(Ty Miller wins) = 0.802  ->  pick: Ty Miller (80%)
- shipped number is the market-aware stack: vig-free market P(Ty Miller) = 0.769, skill-only model = 0.660 (gap -0.109)
- method: Ty Miller by KO 46% / sub 13% / dec 21%; Billy Ray Goff by KO 7% / sub 2% / dec 11%
- how it ends: finish 68% (R1 39% / R2 20% / R3 9%) vs. decision 32%
- likeliest endings: Ty Miller by KO/TKO, round 1 (27%), Ty Miller by decision (21%), Ty Miller by KO/TKO, round 2 (13%)
- drivers (log-odds): diff_elo +0.12, diff_age +0.12, diff_reach_cm +0.08, diff_strike_elo -0.07, diff_sapm_l5 -0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Ty Miller by KO/TKO | 27.4% | 12.9% | 5.8% | **46.1%** |
| Ty Miller by submission | 7.4% | 3.9% | 1.8% | **13.0%** |
| Billy Ray Goff by KO/TKO | 3.4% | 2.2% | 1.2% | **6.8%** |
| Billy Ray Goff by submission | 1.2% | 0.8% | 0.4% | **2.4%** |
| decision (either fighter) | — | — | — | **31.6%** |

## Steven Asplund vs. Guilherme Pat — Heavyweight
P(Steven Asplund wins) = 0.578  ->  pick: Steven Asplund (58%)
- context: YouTube lean +1.00 (n=6) nudged p by +0.060 — skill was near a coin flip
- shipped number is the market-aware stack: vig-free market P(Steven Asplund) = 0.500, skill-only model = 0.556 (gap +0.056)
- method: Steven Asplund by KO 34% / sub 7% / dec 17%; Guilherme Pat by KO 25% / sub 6% / dec 12%
- how it ends: finish 71% (R1 42% / R2 20% / R3 9%) vs. decision 29%
- likeliest endings: Steven Asplund by KO/TKO, round 1 (20%), Steven Asplund by decision (17%), Guilherme Pat by KO/TKO, round 1 (15%)
- drivers (log-odds): f2_reach_cm +0.32, f1_reach_cm +0.28, diff_height_cm -0.26, diff_strike_elo +0.16, f1_age +0.15

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Steven Asplund by KO/TKO | 19.9% | 9.2% | 4.4% | **33.5%** |
| Steven Asplund by submission | 4.2% | 2.1% | 1.0% | **7.3%** |
| Guilherme Pat by KO/TKO | 14.9% | 6.8% | 3.0% | **24.7%** |
| Guilherme Pat by submission | 3.2% | 1.6% | 0.7% | **5.5%** |
| decision (either fighter) | — | — | — | **28.9%** |

## Diyar Nurgozhay vs. Bruno Lopes — Light Heavyweight
P(Diyar Nurgozhay wins) = 0.427  ->  pick: Bruno Lopes (57%)
- shipped number is the market-aware stack: vig-free market P(Diyar Nurgozhay) = 0.377, skill-only model = 0.656 (gap +0.279)
- method: Diyar Nurgozhay by KO 33% / sub 2% / dec 8%; Bruno Lopes by KO 20% / sub 19% / dec 18%
- how it ends: finish 74% (R1 40% / R2 23% / R3 11%) vs. decision 26%
- likeliest endings: Diyar Nurgozhay by KO/TKO, round 1 (19%), Bruno Lopes by decision (18%), Bruno Lopes by KO/TKO, round 1 (11%)
- drivers (log-odds): diff_strike_elo +0.22, diff_opp_elo_l5 -0.11, diff_age +0.10, f2_strike_elo +0.06, f2_age +0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Diyar Nurgozhay by KO/TKO | 18.6% | 10.0% | 4.5% | **33.0%** |
| Diyar Nurgozhay by submission | 1.1% | 0.6% | 0.3% | **2.0%** |
| Bruno Lopes by KO/TKO | 10.8% | 6.4% | 3.2% | **20.4%** |
| Bruno Lopes by submission | 9.6% | 6.3% | 3.2% | **19.0%** |
| decision (either fighter) | — | — | — | **25.5%** |

## José Luiz Montanha vs. Louie Sutherland — Heavyweight
P(José Luiz Montanha wins) = 0.369  ->  pick: Louie Sutherland (63%)
- CAUTION: no UFC history for José Luiz Montanha (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 6-1-0.
- shipped number is the market-aware stack: vig-free market P(José Luiz Montanha) = 0.412, skill-only model = 0.359 (gap -0.053)
- method: José Luiz Montanha by KO 25% / sub 5% / dec 7%; Louie Sutherland by KO 31% / sub 17% / dec 14%
- how it ends: finish 79% (R1 50% / R2 20% / R3 8%) vs. decision 21%
- likeliest endings: Louie Sutherland by KO/TKO, round 1 (20%), José Luiz Montanha by KO/TKO, round 1 (16%), Louie Sutherland by decision (14%)
- drivers (log-odds): f1_reach_cm -0.35, diff_height_cm +0.32, f2_reach_cm -0.29, diff_strike_elo +0.18, f2_age -0.15

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| José Luiz Montanha by KO/TKO | 16.4% | 6.3% | 2.6% | **25.3%** |
| José Luiz Montanha by submission | 3.0% | 1.3% | 0.5% | **4.9%** |
| Louie Sutherland by KO/TKO | 20.1% | 7.9% | 3.3% | **31.3%** |
| Louie Sutherland by submission | 10.9% | 4.6% | 1.9% | **17.4%** |
| decision (either fighter) | — | — | — | **21.1%** |

## Manoel Sousa vs. Richie Miranda — Lightweight
P(Manoel Sousa wins) = 0.820  ->  pick: Manoel Sousa (82%)
- CAUTION: no UFC history for Richie Miranda (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 13-1-0.
- shipped number is the market-aware stack: vig-free market P(Manoel Sousa) = 0.801, skill-only model = 0.608 (gap -0.193)
- method: Manoel Sousa by KO 34% / sub 20% / dec 29%; Richie Miranda by KO 6% / sub 3% / dec 8%
- how it ends: finish 63% (R1 35% / R2 19% / R3 9%) vs. decision 37%
- likeliest endings: Manoel Sousa by decision (29%), Manoel Sousa by KO/TKO, round 1 (19%), Manoel Sousa by submission, round 1 (11%)
- drivers (log-odds): f2_reach_cm +0.36, f1_reach_cm +0.32, diff_height_cm -0.31, diff_age +0.14, f1_height_cm -0.13

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Manoel Sousa by KO/TKO | 18.8% | 10.1% | 4.7% | **33.6%** |
| Manoel Sousa by submission | 10.5% | 6.1% | 2.9% | **19.6%** |
| Richie Miranda by KO/TKO | 3.6% | 1.9% | 1.0% | **6.5%** |
| Richie Miranda by submission | 1.7% | 1.0% | 0.5% | **3.2%** |
| decision (either fighter) | — | — | — | **37.2%** |

## Miles Johns vs. Gianni Vazquez — Featherweight
P(Miles Johns wins) = 0.616  ->  pick: Miles Johns (62%)
- shipped number is the market-aware stack: vig-free market P(Miles Johns) = 0.550, skill-only model = 0.705 (gap +0.155)
- method: Miles Johns by KO 24% / sub 6% / dec 31%; Gianni Vazquez by KO 15% / sub 7% / dec 16%
- how it ends: finish 52% (R1 28% / R2 16% / R3 8%) vs. decision 48%
- likeliest endings: Miles Johns by decision (31%), Gianni Vazquez by decision (16%), Miles Johns by KO/TKO, round 1 (13%)
- drivers (log-odds): f1_reach_cm +0.38, f2_reach_cm +0.38, diff_height_cm -0.32, diff_strike_elo +0.13, f1_height_cm -0.13

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Miles Johns by KO/TKO | 12.6% | 7.7% | 3.9% | **24.1%** |
| Miles Johns by submission | 3.0% | 2.0% | 1.0% | **6.0%** |
| Gianni Vazquez by KO/TKO | 8.6% | 4.3% | 1.8% | **14.7%** |
| Gianni Vazquez by submission | 4.1% | 2.2% | 1.0% | **7.3%** |
| decision (either fighter) | — | — | — | **47.9%** |

## Juliana Miller vs. Ravena Oliveira — Women's Flyweight
P(Juliana Miller wins) = 0.632  ->  pick: Juliana Miller (63%)
- shipped number is the market-aware stack: vig-free market P(Juliana Miller) = 0.635, skill-only model = 0.495 (gap -0.140)
- method: Juliana Miller by KO 11% / sub 18% / dec 34%; Ravena Oliveira by KO 6% / sub 3% / dec 28%
- how it ends: finish 39% (R1 19% / R2 13% / R3 7%) vs. decision 61%
- likeliest endings: Juliana Miller by decision (34%), Ravena Oliveira by decision (28%), Juliana Miller by submission, round 1 (8%)
- drivers (log-odds): diff_age -0.11, diff_elo +0.11, diff_opp_elo_l5 -0.10, diff_strike_elo -0.10, diff_grapple_elo +0.06

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Juliana Miller by KO/TKO | 5.7% | 3.8% | 2.0% | **11.4%** |
| Juliana Miller by submission | 8.5% | 6.2% | 3.2% | **17.9%** |
| Ravena Oliveira by KO/TKO | 3.2% | 2.0% | 1.1% | **6.3%** |
| Ravena Oliveira by submission | 1.4% | 1.0% | 0.5% | **2.8%** |
| decision (either fighter) | — | — | — | **61.5%** |

## Giovanna Canuto vs. Carol Foro — Women's Strawweight
P(Giovanna Canuto wins) = 0.322  ->  pick: Carol Foro (68%)
- CAUTION: no UFC history for Giovanna Canuto (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 7-1-0.
- CAUTION: no UFC history for Carol Foro (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 9-1-0.
- context: YouTube lean -0.50 (n=4) noted but not applied — skill already decisive (0.39)
- shipped number is the market-aware stack: vig-free market P(Giovanna Canuto) = 0.354, skill-only model = 0.387 (gap +0.034)
- method: Giovanna Canuto by KO 9% / sub 12% / dec 11%; Carol Foro by KO 27% / sub 21% / dec 20%
- how it ends: finish 69% (R1 40% / R2 20% / R3 9%) vs. decision 31%
- likeliest endings: Carol Foro by decision (20%), Carol Foro by KO/TKO, round 1 (16%), Carol Foro by submission, round 1 (12%)
- drivers (log-odds): f1_reach_cm -0.30, f2_reach_cm -0.28, diff_height_cm +0.25, f1_age -0.16, f2_age -0.15

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Giovanna Canuto by KO/TKO | 5.2% | 2.6% | 1.2% | **8.9%** |
| Giovanna Canuto by submission | 6.8% | 3.6% | 1.6% | **12.0%** |
| Carol Foro by KO/TKO | 15.8% | 7.8% | 3.6% | **27.2%** |
| Carol Foro by submission | 11.7% | 6.2% | 2.9% | **20.9%** |
| decision (either fighter) | — | — | — | **31.1%** |

---
*Simulation/educational project. No betting advice. The market knows more than this model.*