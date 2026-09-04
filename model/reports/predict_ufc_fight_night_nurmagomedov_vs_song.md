# UFC Fight Night: Nurmagomedov vs. Song — 2026-08-29

Point-in-time predictions from 8690 historical fights. Educational output — NOT betting advice; the backtest shows this model does not beat the market.

## Umar Nurmagomedov vs. Song Yadong — Bantamweight
P(Umar Nurmagomedov wins) = 0.833  ->  pick: Umar Nurmagomedov (83%)
- context: YouTube lean -0.22 (n=7) noted but not applied — skill already decisive (0.79)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Umar Nurmagomedov holds the quality-weighted form edge (hot vs mixed over the last 5).
- research: Style record: Umar Nurmagomedov is 83% against strikers in the UFC.
- research: Common opponents (2): Umar Nurmagomedov's record against them is better.
- skill-only research model P(Umar Nurmagomedov) = 0.791; vig-free market = 0.827 (gap -0.037). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Umar Nurmagomedov by KO 15% / sub 12% / dec 57%; Song Yadong by KO 5% / sub 1% / dec 10%
- how it ends: finish 33% (R1 11% / R2 10% / R3 6% / R4 3% / R5 3%) vs. decision 67%
- likeliest endings: Umar Nurmagomedov by decision (57%), Song Yadong by decision (10%), Umar Nurmagomedov by KO/TKO, round 1 (5%)
- drivers (log-odds): diff_strike_elo +0.22, diff_age -0.11, diff_elo +0.10, f1_pre_ufc_win_pct +0.10, diff_grapple_elo +0.08

| ending | R1 | R2 | R3 | R4 | R5 | any round |
|---|---|---|---|---|---|---|
| Umar Nurmagomedov by KO/TKO | 5.1% | 4.3% | 2.6% | 1.5% | 1.5% | **15.0%** |
| Umar Nurmagomedov by submission | 3.5% | 3.4% | 2.3% | 1.3% | 1.1% | **11.6%** |
| Song Yadong by KO/TKO | 1.8% | 1.6% | 1.0% | 0.5% | 0.5% | **5.4%** |
| Song Yadong by submission | 0.4% | 0.4% | 0.3% | 0.1% | 0.1% | **1.3%** |
| decision (either fighter) | — | — | — | — | — | **66.7%** |

## Yan Xiaonan vs. Denise Gomes — Women's Strawweight
P(Yan Xiaonan wins) = 0.447  ->  no call (55% lean Denise Gomes)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Denise Gomes holds the quality-weighted form edge (mixed vs hot over the last 5).
- research: Style record: Yan Xiaonan is 82% against strikers in the UFC.
- research: Common opponents (2): Yan Xiaonan's record against them is better.
- skill-only research model P(Yan Xiaonan) = 0.370; vig-free market = 0.576 (gap -0.206). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Yan Xiaonan by KO 7% / sub 4% / dec 34%; Denise Gomes by KO 9% / sub 5% / dec 42%
- how it ends: finish 24% (R1 12% / R2 8% / R3 5%) vs. decision 76%
- likeliest endings: Denise Gomes by decision (42%), Yan Xiaonan by decision (34%), Denise Gomes by KO/TKO, round 1 (4%)
- drivers (log-odds): diff_age -0.42, diff_strike_elo +0.18, diff_opp_elo_l5 +0.13, f1_pre_ufc_win_pct +0.11, f2_pre_ufc_win_pct +0.10

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Yan Xiaonan by KO/TKO | 3.1% | 2.2% | 1.4% | **6.7%** |
| Yan Xiaonan by submission | 1.8% | 1.4% | 0.9% | **4.2%** |
| Denise Gomes by KO/TKO | 4.5% | 2.9% | 1.7% | **9.0%** |
| Denise Gomes by submission | 2.2% | 1.5% | 0.9% | **4.6%** |
| decision (either fighter) | — | — | — | **75.5%** |

## Aoriqileng vs. Kai Asakura — Bantamweight
P(Aoriqileng wins) = 0.206  ->  pick: Kai Asakura (79%)
- research: Style: both profile as strikers — a same-look fight.
- research: Last fights: Aoriqileng lost last time out; Kai Asakura won last time out.
- research: Style record: Aoriqileng is 57% against strikers in the UFC.
- skill-only research model P(Aoriqileng) = 0.332; vig-free market = 0.212 (gap +0.120). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Aoriqileng by KO 7% / sub 4% / dec 9%; Kai Asakura by KO 30% / sub 6% / dec 43%
- how it ends: finish 48% (R1 27% / R2 15% / R3 6%) vs. decision 52%
- likeliest endings: Kai Asakura by decision (43%), Kai Asakura by KO/TKO, round 1 (18%), Aoriqileng by decision (9%)
- drivers (log-odds): diff_strike_elo -0.16, diff_opp_elo_l5 -0.11, f1_pre_ufc_win_pct -0.06, diff_age -0.06, diff_sig_acc_l5 +0.04

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Aoriqileng by KO/TKO | 4.2% | 2.3% | 0.9% | **7.4%** |
| Aoriqileng by submission | 2.1% | 1.2% | 0.5% | **3.8%** |
| Kai Asakura by KO/TKO | 17.5% | 9.1% | 3.7% | **30.2%** |
| Kai Asakura by submission | 3.6% | 2.0% | 0.8% | **6.4%** |
| decision (either fighter) | — | — | — | **52.1%** |

## Sumudaerji vs. Alex Perez — Flyweight
P(Sumudaerji wins) = 0.665  ->  pick: Sumudaerji (66%)
- context: YouTube lean -1.00 (n=5) noted but not applied — skill already decisive (0.64)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Sumudaerji holds the quality-weighted form edge (mixed vs mixed over the last 5).
- research: Style record: Sumudaerji is 60% against strikers in the UFC.
- research: Rematch: 1 previous meeting 91 days ago.
- research: Common opponents (1): Alex Perez's record against them is better.
- skill-only research model P(Sumudaerji) = 0.636; vig-free market = 0.663 (gap -0.026). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Sumudaerji by KO 29% / sub 8% / dec 30%; Alex Perez by KO 6% / sub 8% / dec 19%
- how it ends: finish 51% (R1 27% / R2 17% / R3 8%) vs. decision 49%
- likeliest endings: Sumudaerji by decision (30%), Alex Perez by decision (19%), Sumudaerji by KO/TKO, round 1 (16%)
- drivers (log-odds): diff_style_reach_striker +0.29, diff_age +0.19, diff_strike_elo +0.13, diff_opp_elo_l5 -0.11, diff_grapple_elo -0.09

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Sumudaerji by KO/TKO | 15.7% | 9.2% | 4.0% | **28.9%** |
| Sumudaerji by submission | 4.1% | 2.6% | 1.2% | **7.9%** |
| Alex Perez by KO/TKO | 3.3% | 2.0% | 0.9% | **6.3%** |
| Alex Perez by submission | 4.3% | 2.8% | 1.3% | **8.4%** |
| decision (either fighter) | — | — | — | **48.6%** |

## Liu Ce vs. Levi Rodrigues — Light Heavyweight
P(Liu Ce wins) = 0.572  ->  no call (57% lean Liu Ce)
- CAUTION: no UFC history for Liu Ce (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 3-1-0.
- CAUTION: no UFC history for Levi Rodrigues (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 5-1-0.
- context: f2 flagged late replacement — confidence dampened
- skill-only research model P(Liu Ce) = 0.498; vig-free market = 0.609 (gap -0.111). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Liu Ce by KO 25% / sub 13% / dec 19%; Levi Rodrigues by KO 19% / sub 10% / dec 14%
- how it ends: finish 67% (R1 40% / R2 19% / R3 9%) vs. decision 33%
- likeliest endings: Liu Ce by decision (19%), Liu Ce by KO/TKO, round 1 (15%), Levi Rodrigues by decision (14%)
- drivers (log-odds): f1_pre_ufc_win_pct -0.14, f2_pre_ufc_win_pct -0.09, f1_sub_end_rate_l5 -0.02, f1_sig_def_l5 -0.02, f2_sig_acc_l3 -0.01

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Liu Ce by KO/TKO | 14.9% | 6.9% | 3.1% | **25.0%** |
| Liu Ce by submission | 7.8% | 3.9% | 1.8% | **13.4%** |
| Levi Rodrigues by KO/TKO | 11.2% | 5.2% | 2.4% | **18.8%** |
| Levi Rodrigues by submission | 5.8% | 2.9% | 1.3% | **10.0%** |
| decision (either fighter) | — | — | — | **32.8%** |

## Bilal Hasan vs. Nilson Rojas — Flyweight
P(Bilal Hasan wins) = 0.500  ->  no call (50% lean Bilal Hasan)
- CAUTION: no UFC history for Bilal Hasan (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 8-0-0.
- CAUTION: no UFC history for Nilson Rojas (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 9-0-0.
- context: market-trap guard: skill=0.51 but market=0.85 on a debut bout — abstaining
- skill-only research model P(Bilal Hasan) = 0.509; vig-free market = 0.853 (gap -0.344). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Bilal Hasan by KO 16% / sub 14% / dec 20%; Nilson Rojas by KO 16% / sub 14% / dec 20%
- how it ends: finish 60% (R1 32% / R2 18% / R3 10%) vs. decision 40%
- likeliest endings: Nilson Rojas by decision (20%), Bilal Hasan by decision (20%), Bilal Hasan by KO/TKO, round 1 (9%)
- drivers (log-odds): f1_reach_cm -0.06, f2_pre_ufc_fights +0.03, diff_age +0.03, f2_reach_cm -0.02, f2_age -0.01

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Bilal Hasan by KO/TKO | 9.0% | 4.9% | 2.5% | **16.5%** |
| Bilal Hasan by submission | 7.3% | 4.3% | 2.2% | **13.8%** |
| Nilson Rojas by KO/TKO | 8.4% | 4.8% | 2.7% | **15.9%** |
| Nilson Rojas by submission | 7.1% | 4.4% | 2.4% | **13.9%** |
| decision (either fighter) | — | — | — | **39.9%** |

## Namsrai Batbayar vs. Andre Lima — Flyweight
P(Namsrai Batbayar wins) = 0.273  ->  pick: Andre Lima (73%)
- CAUTION: no UFC history for Namsrai Batbayar (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 10-1-0.
- research: Last fights: Andre Lima lost last time out.
- skill-only research model P(Namsrai Batbayar) = 0.397; vig-free market = 0.298 (gap +0.098). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Namsrai Batbayar by KO 4% / sub 6% / dec 17%; Andre Lima by KO 15% / sub 17% / dec 41%
- how it ends: finish 42% (R1 21% / R2 14% / R3 8%) vs. decision 58%
- likeliest endings: Andre Lima by decision (41%), Namsrai Batbayar by decision (17%), Andre Lima by submission, round 1 (8%)
- drivers (log-odds): diff_strike_elo -0.18, diff_elo -0.12, diff_age +0.12, f1_pre_ufc_win_pct +0.04, f1_sub_end_rate_l5 +0.04

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Namsrai Batbayar by KO/TKO | 2.5% | 1.3% | 0.6% | **4.4%** |
| Namsrai Batbayar by submission | 3.2% | 1.9% | 0.9% | **6.0%** |
| Andre Lima by KO/TKO | 7.5% | 4.9% | 2.8% | **15.2%** |
| Andre Lima by submission | 7.9% | 5.6% | 3.2% | **16.6%** |
| decision (either fighter) | — | — | — | **57.9%** |

## Rei Tsuruya vs. Kevin Borjas — Flyweight
P(Rei Tsuruya wins) = 0.865  ->  pick: Rei Tsuruya (86%)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Rei Tsuruya holds the quality-weighted form edge (hot vs mixed over the last 5).
- research: Style record: Rei Tsuruya is 67% against strikers in the UFC.
- research: Common opponents: 1 shared names on the record.
- skill-only research model P(Rei Tsuruya) = 0.725; vig-free market = 0.858 (gap -0.132). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Rei Tsuruya by KO 14% / sub 25% / dec 48%; Kevin Borjas by KO 4% / sub 2% / dec 8%
- how it ends: finish 44% (R1 22% / R2 15% / R3 7%) vs. decision 56%
- likeliest endings: Rei Tsuruya by decision (48%), Rei Tsuruya by submission, round 1 (13%), Rei Tsuruya by submission, round 2 (8%)
- drivers (log-odds): diff_strike_elo +0.25, diff_age +0.19, diff_elo +0.12, diff_quality_win_rate -0.08, diff_td15_l5 +0.08

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Rei Tsuruya by KO/TKO | 7.3% | 4.5% | 2.2% | **14.0%** |
| Rei Tsuruya by submission | 12.6% | 8.3% | 4.1% | **24.9%** |
| Kevin Borjas by KO/TKO | 1.6% | 1.3% | 0.7% | **3.6%** |
| Kevin Borjas by submission | 0.8% | 0.7% | 0.4% | **1.8%** |
| decision (either fighter) | — | — | — | **55.7%** |

## Xiao Long vs. Francesco Nuzzi — Bantamweight
P(Xiao Long wins) = 0.615  ->  pick: Xiao Long (61%)
- CAUTION: no UFC history for Francesco Nuzzi (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 11-2-0.
- research: Last fights: Xiao Long lost last time out.
- skill-only research model P(Xiao Long) = 0.538; vig-free market = 0.603 (gap -0.066). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Xiao Long by KO 21% / sub 8% / dec 33%; Francesco Nuzzi by KO 15% / sub 6% / dec 17%
- how it ends: finish 50% (R1 26% / R2 15% / R3 8%) vs. decision 50%
- likeliest endings: Xiao Long by decision (33%), Francesco Nuzzi by decision (17%), Xiao Long by KO/TKO, round 1 (11%)
- drivers (log-odds): f2_reach_cm +0.38, f1_reach_cm +0.36, diff_height_cm -0.31, f1_height_cm -0.17, diff_strike_elo +0.14

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Xiao Long by KO/TKO | 10.8% | 6.4% | 3.6% | **20.8%** |
| Xiao Long by submission | 4.0% | 2.5% | 1.4% | **7.9%** |
| Francesco Nuzzi by KO/TKO | 8.2% | 4.5% | 2.4% | **15.1%** |
| Francesco Nuzzi by submission | 3.3% | 2.0% | 1.1% | **6.3%** |
| decision (either fighter) | — | — | — | **49.9%** |

## Jack Jenkins vs. Sean Woodson — Featherweight
P(Jack Jenkins wins) = 0.348  ->  pick: Sean Woodson (65%)
- research: Style: both profile as strikers — a same-look fight.
- research: Form: Sean Woodson holds the quality-weighted form edge (mixed vs hot over the last 5).
- research: Style record: Jack Jenkins is 60% against strikers in the UFC.
- skill-only research model P(Jack Jenkins) = 0.303; vig-free market = 0.434 (gap -0.131). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Jack Jenkins by KO 11% / sub 3% / dec 21%; Sean Woodson by KO 19% / sub 9% / dec 37%
- how it ends: finish 41% (R1 20% / R2 14% / R3 7%) vs. decision 59%
- likeliest endings: Sean Woodson by decision (37%), Jack Jenkins by decision (21%), Sean Woodson by KO/TKO, round 1 (9%)
- drivers (log-odds): diff_style_reach_striker -0.26, diff_strike_elo -0.17, diff_height_cm +0.13, diff_elo -0.10, diff_reach_cm -0.10

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Jack Jenkins by KO/TKO | 5.9% | 3.3% | 1.6% | **10.9%** |
| Jack Jenkins by submission | 1.4% | 0.8% | 0.4% | **2.6%** |
| Sean Woodson by KO/TKO | 9.2% | 6.4% | 3.6% | **19.2%** |
| Sean Woodson by submission | 3.9% | 2.9% | 1.7% | **8.5%** |
| decision (either fighter) | — | — | — | **58.7%** |

## Lawrence Lui vs. Hector de Sousa Santiago — Bantamweight
P(Lawrence Lui wins) = 0.777  ->  pick: Lawrence Lui (78%)
- CAUTION: no UFC history for Hector de Sousa Santiago (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 6-1-0.
- research: Last fights: Lawrence Lui won last time out.
- skill-only research model P(Lawrence Lui) = 0.675; vig-free market = 0.738 (gap -0.064). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Lawrence Lui by KO 18% / sub 21% / dec 39%; Hector de Sousa Santiago by KO 6% / sub 5% / dec 12%
- how it ends: finish 50% (R1 27% / R2 15% / R3 8%) vs. decision 50%
- likeliest endings: Lawrence Lui by decision (39%), Hector de Sousa Santiago by decision (12%), Lawrence Lui by submission, round 1 (11%)
- drivers (log-odds): f2_reach_cm +0.38, f1_reach_cm +0.29, diff_height_cm -0.25, diff_age +0.21, diff_elo +0.11

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Lawrence Lui by KO/TKO | 10.1% | 5.4% | 2.7% | **18.2%** |
| Lawrence Lui by submission | 11.2% | 6.5% | 3.2% | **20.9%** |
| Hector de Sousa Santiago by KO/TKO | 3.0% | 1.7% | 0.9% | **5.6%** |
| Hector de Sousa Santiago by submission | 2.6% | 1.5% | 0.9% | **4.9%** |
| decision (either fighter) | — | — | — | **50.3%** |

## Xiong Jingnan vs. Julia Polastri — Women's Strawweight
P(Xiong Jingnan wins) = 0.258  ->  pick: Julia Polastri (74%)
- research: Style: both profile as strikers — a same-look fight.
- research: Pace: Julia Polastri is the volume striker (6.2 vs 4.5 SLpM).
- research: Form: Julia Polastri holds the quality-weighted form edge (cold vs mixed over the last 5).
- research: Style record: Julia Polastri is 40% against strikers in the UFC.
- skill-only research model P(Xiong Jingnan) = 0.218; vig-free market = 0.333 (gap -0.115). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Xiong Jingnan by KO 6% / sub 3% / dec 17%; Julia Polastri by KO 18% / sub 7% / dec 50%
- how it ends: finish 33% (R1 17% / R2 10% / R3 6%) vs. decision 67%
- likeliest endings: Julia Polastri by decision (50%), Xiong Jingnan by decision (17%), Julia Polastri by KO/TKO, round 1 (9%)
- drivers (log-odds): diff_age -0.35, f1_reach_cm -0.30, f2_reach_cm -0.30, diff_height_cm +0.28, diff_strike_elo -0.26

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Xiong Jingnan by KO/TKO | 3.4% | 1.7% | 0.8% | **5.9%** |
| Xiong Jingnan by submission | 1.5% | 0.8% | 0.4% | **2.7%** |
| Julia Polastri by KO/TKO | 8.6% | 5.7% | 3.5% | **17.8%** |
| Julia Polastri by submission | 3.1% | 2.2% | 1.4% | **6.7%** |
| decision (either fighter) | — | — | — | **66.9%** |

## Ding Meng vs. Cameron Nelson — Welterweight
P(Ding Meng wins) = 0.525  ->  no call (52% lean Ding Meng)
- CAUTION: no UFC history for Cameron Nelson (debut or misspelled name?) — prediction is weak. Pro record outside the UFC: 7-1-0.
- research: Last fights: Ding Meng lost last time out.
- skill-only research model P(Ding Meng) = 0.343; vig-free market = 0.566 (gap -0.223). Shipped number mixes both; deeper UFC history weights the research model more.
- method: Ding Meng by KO 16% / sub 6% / dec 30%; Cameron Nelson by KO 20% / sub 8% / dec 19%
- how it ends: finish 51% (R1 28% / R2 15% / R3 8%) vs. decision 49%
- likeliest endings: Ding Meng by decision (30%), Cameron Nelson by decision (19%), Cameron Nelson by KO/TKO, round 1 (11%)
- drivers (log-odds): f2_reach_cm +0.45, f1_reach_cm +0.43, diff_height_cm -0.28, diff_age -0.18, f1_height_cm -0.17

| ending | R1 | R2 | R3 | any round |
|---|---|---|---|---|
| Ding Meng by KO/TKO | 8.8% | 4.8% | 2.6% | **16.2%** |
| Ding Meng by submission | 3.3% | 2.0% | 1.1% | **6.4%** |
| Cameron Nelson by KO/TKO | 11.4% | 5.8% | 2.9% | **20.0%** |
| Cameron Nelson by submission | 4.5% | 2.5% | 1.2% | **8.2%** |
| decision (either fighter) | — | — | — | **49.1%** |

---
*Simulation/educational project. No betting advice. The market knows more than this model.*