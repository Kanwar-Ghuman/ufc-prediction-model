# Example card (hypothetical matchups) — 2026-07-11

Point-in-time predictions from 8547 historical fights. Educational output — NOT betting advice; the backtest shows this model does not beat the market.

## Islam Makhachev vs. Arman Tsarukyan — Lightweight
P(Islam Makhachev wins) = 0.583  ->  pick: Islam Makhachev (58%)
- market (vig-free): P(Islam Makhachev) = 0.663; model - market = -0.080
- market-aware stack: P(Islam Makhachev) = 0.684 (the odds, lightly adjusted — the sharpest number here)
- method: Islam Makhachev by KO 15% / sub 15% / dec 28%; Arman Tsarukyan by KO 26% / sub 4% / dec 12%
- drivers (log-odds): diff_elo +0.47, diff_age -0.21, diff_td15_l5 -0.19, diff_opp_elo_l5 +0.17, diff_slpm_l3 -0.07

## Alexa Grasso vs. Valentina Shevchenko — Women's Flyweight
P(Alexa Grasso wins) = 0.373  ->  pick: Valentina Shevchenko (63%)
- method: Alexa Grasso by KO 11% / sub 8% / dec 19%; Valentina Shevchenko by KO 11% / sub 8% / dec 44%
- drivers (log-odds): diff_elo -0.41, diff_age +0.34, diff_td15_l5 -0.12, diff_opp_elo_l5 +0.11, diff_sig_def_l5 -0.10

## Arnold Allen vs. Melquizael Costa — Featherweight
P(Arnold Allen wins) = 0.627  ->  pick: Arnold Allen (63%)
- method: Arnold Allen by KO 14% / sub 8% / dec 41%; Melquizael Costa by KO 12% / sub 4% / dec 21%
- drivers (log-odds): diff_age -0.23, diff_elo +0.22, diff_opp_elo_l5 +0.22, diff_sig_def_l5 +0.09, diff_td_def_l5 +0.07

---
*Simulation/educational project. No betting advice. The market knows more than this model.*