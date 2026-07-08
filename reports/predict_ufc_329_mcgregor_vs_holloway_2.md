# UFC 329: McGregor vs. Holloway 2 — 2026-07-11

Point-in-time predictions from 8547 historical fights. Educational output — NOT betting advice; the backtest shows this model does not beat the market.

Name spellings resolved against ufcstats: Benoît Saint Denis -> Benoit Saint Denis; Adrian Yañez -> Adrian Yanez; César Almeida -> Cesar Almeida

## Conor McGregor vs. Max Holloway — Welterweight
P(Conor McGregor wins) = 0.330  ->  pick: Max Holloway (67%)
- method: Conor McGregor by KO 17% / sub 6% / dec 9%; Max Holloway by KO 34% / sub 6% / dec 27%
- drivers (log-odds): diff_age -0.19, diff_elo -0.17, f1_age -0.10, diff_reach_cm +0.07, diff_ground_absorbed_share_l5 -0.06

## Benoit Saint Denis vs. Paddy Pimblett — Lightweight
P(Benoit Saint Denis wins) = 0.722  ->  pick: Benoit Saint Denis (72%)
- method: Benoit Saint Denis by KO 34% / sub 10% / dec 28%; Paddy Pimblett by KO 11% / sub 5% / dec 12%
- drivers (log-odds): diff_td15_l5 +0.13, diff_age +0.11, diff_elo +0.10, diff_sig_acc_l5 +0.06, diff_td_def_l3 +0.06

## Cory Sandhagen vs. Mario Bautista — Bantamweight
P(Cory Sandhagen wins) = 0.499  ->  NO CALL (abstain band)
- method: Cory Sandhagen by KO 12% / sub 5% / dec 33%; Mario Bautista by KO 9% / sub 6% / dec 36%
- drivers (log-odds): diff_opp_elo_l5 +0.15, diff_age -0.06, f2_td_def_l3 +0.04, diff_slpm_l5 -0.03, diff_elo +0.03

## Brandon Royval vs. Lone'er Kavanagh — Flyweight
P(Brandon Royval wins) = 0.331  ->  pick: Lone'er Kavanagh (67%)
- method: Brandon Royval by KO 8% / sub 8% / dec 18%; Lone'er Kavanagh by KO 24% / sub 8% / dec 35%
- drivers (log-odds): diff_age -0.22, f1_age -0.12, diff_opp_elo_l5 +0.10, diff_sig_def_l5 -0.08, f2_age -0.08

## King Green vs. Terrance McKinney — Lightweight
P(King Green wins) = 0.520  ->  NO CALL (abstain band)
- method: King Green by KO 18% / sub 11% / dec 24%; Terrance McKinney by KO 24% / sub 8% / dec 16%
- drivers (log-odds): diff_age -0.28, diff_sapm_l5 +0.13, f2_age -0.10, f2_sig_def_l3 +0.07, diff_elo +0.07

## Robert Whittaker vs. Nikita Krylov — Light Heavyweight
P(Robert Whittaker wins) = 0.474  ->  NO CALL (abstain band)
- method: Robert Whittaker by KO 12% / sub 6% / dec 29%; Nikita Krylov by KO 19% / sub 7% / dec 27%
- drivers (log-odds): diff_elo +0.15, diff_age -0.13, diff_td15_l5 -0.12, diff_opp_elo_l5 +0.07, diff_td_def_l5 +0.05

## Gable Steveson vs. Elisha Ellison — Heavyweight
P(Gable Steveson wins) = 0.484  ->  NO CALL (abstain band)
- CAUTION: no UFC history for Gable Steveson (debut or misspelled name?) — prediction is weak.
- method: Gable Steveson by KO 28% / sub 7% / dec 13%; Elisha Ellison by KO 24% / sub 11% / dec 17%
- drivers (log-odds): f2_reach_cm -0.50, f1_reach_cm -0.35, diff_height_cm +0.30, f1_height_cm +0.15, diff_age +0.14

## Cody Garbrandt vs. Adrian Yanez — Bantamweight
P(Cody Garbrandt wins) = 0.412  ->  pick: Adrian Yanez (59%)
- method: Cody Garbrandt by KO 8% / sub 4% / dec 29%; Adrian Yanez by KO 18% / sub 7% / dec 33%
- drivers (log-odds): diff_age -0.14, diff_sapm_l5 +0.09, diff_opp_elo_l5 -0.09, f2_sapm_l5 +0.06, diff_sig_acc_l5 +0.05

## Luke Riley vs. Kai Kamaka III — Featherweight
P(Luke Riley wins) = 0.676  ->  pick: Luke Riley (68%)
- method: Luke Riley by KO 24% / sub 11% / dec 32%; Kai Kamaka III by KO 14% / sub 6% / dec 13%
- drivers (log-odds): f1_age +0.18, f2_age +0.14, diff_sapm_l5 +0.09, f2_reach_cm +0.08, diff_elo +0.07

## Tracy Cortez vs. Wang Cong — Women's Flyweight
P(Tracy Cortez wins) = 0.498  ->  NO CALL (abstain band)
- method: Tracy Cortez by KO 8% / sub 10% / dec 32%; Wang Cong by KO 9% / sub 4% / dec 37%
- drivers (log-odds): diff_opp_elo_l5 +0.18, diff_age +0.07, f2_age +0.07, diff_sig_acc_l5 -0.07, diff_elo +0.07

## Damian Pinas vs. Cesar Almeida — Middleweight
P(Damian Pinas wins) = 0.728  ->  pick: Damian Pinas (73%)
- method: Damian Pinas by KO 43% / sub 8% / dec 23%; Cesar Almeida by KO 8% / sub 6% / dec 14%
- drivers (log-odds): diff_age +0.22, f1_age +0.17, f2_age +0.11, diff_reach_cm +0.06, diff_td_def_l5 +0.06

## Ryan Gandra vs. Zachary Reese — Middleweight
P(Ryan Gandra wins) = 0.587  ->  pick: Ryan Gandra (59%)
- CAUTION: no UFC history for Zachary Reese (debut or misspelled name?) — prediction is weak.
- method: Ryan Gandra by KO 24% / sub 11% / dec 23%; Zachary Reese by KO 16% / sub 7% / dec 19%
- drivers (log-odds): f1_sapm_l5 +0.05, f2_sig_def_l5 -0.05, f2_sapm_l5 +0.04, diff_elo +0.03, f1_layoff_days +0.03

## Alessandro Costa vs. Cody Durden — Flyweight
P(Alessandro Costa wins) = 0.667  ->  pick: Alessandro Costa (67%)
- method: Alessandro Costa by KO 21% / sub 8% / dec 38%; Cody Durden by KO 6% / sub 5% / dec 23%
- drivers (log-odds): diff_age +0.14, f1_age +0.10, diff_opp_elo_l5 -0.09, f2_age +0.08, diff_elo +0.08

---
*Simulation/educational project. No betting advice. The market knows more than this model.*