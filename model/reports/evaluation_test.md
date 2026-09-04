# Evaluation report — test split

Generated 2026-09-01 22:08 UTC. Fights dated (2023-12-31, 9999-12-31]. Walk-forward windows: 2024-01-01->2024-06-30, 2024-07-01->2024-12-31, 2025-01-01->2025-06-30, 2025-07-01->2025-12-31, 2026-01-01->2026-06-30, 2026-07-01->2026-08-22

| model | n | accuracy | log loss | Brier | ROC AUC | ECE | note |
|---|---|---|---|---|---|---|---|
| coin flip | 1373 | 0.5000 | 0.6931 | 0.2500 | 0.5000 | 0.0025 |  |
| better record | 1373 | 0.5885 | 9.8985 | 0.3835 | 0.5984 | 0.3591 |  |
| higher Elo | 1373 | 0.5645 | 0.6787 | 0.2429 | 0.5979 | 0.0321 |  |
| market (vig-free favorite) | - | - | - | - | - | - | no fights to score (priced fights only) |
| logistic regression (walk-forward) | 1373 | 0.6591 | 0.6269 | 0.2185 | 0.7069 | 0.0265 |  |
| GBM (walk-forward, tuned) | 1373 | 0.6548 | 0.6311 | 0.2202 | 0.7029 | 0.0331 |  |
| GBM + isotonic (fit on train-era OOS) | 1373 | 0.6566 | 0.6298 | 0.2196 | 0.7035 | 0.0344 |  |
| LR+GBM blend (w=0.15, tuned on train-era OOS) | 1373 | 0.6599 | 0.6273 | 0.2185 | 0.7087 | 0.0350 |  |

Reading guide: 'better record' is a picking rule (0/0.5/1 outputs) — its log loss is meaningless by design; compare models on log loss / Brier / ECE against the market row, on accuracy against all rows.

![reliability diagram](reliability_test.png)

## Logistic regression — largest standardized coefficients

Positive means: the bigger fighter1's edge in this differential, the likelier fighter1 wins (per the model).

| feature | coefficient |
|---|---|
| diff_ko_end_rate_l5 | -0.475 |
| diff_dec_end_rate_l5 | -0.473 |
| diff_career_wins | +0.443 |
| diff_losses | +0.392 |
| diff_career_n_fights | -0.387 |
| diff_avg_fight_min | +0.376 |
| diff_style_age_wrestle | +0.353 |
| diff_sub_end_rate_l5 | -0.347 |
| diff_elo | +0.295 |
| diff_wins | -0.272 |
| diff_ko_win_rate | +0.268 |
| diff_sub_win_rate | +0.229 |
| diff_avg_end_round | -0.207 |
| diff_sapm_l5 | -0.205 |
| diff_td15_l5 | +0.204 |

## How the fight ends (method + round)

Both models are walk-forward and scored only where they apply: the method model on every decisive fight, the round model on finishes only (a decision has no round to predict). The method model answers how the winner wins (KO / submission / decision); fight-level KO/sub/dec is that split averaged across corners, which is what the scorecard grades. The round model answers a conditional question — given that this fighter finished by this method, which round? — so its opponent is the historical round split for the same method and the same fight length.

| method of victory (how the winner wins) | n | log loss | winner's method | fight KO/sub/dec |
|---|---|---|---|---|
| method model, shrunk (production, 75% model) | 1371 | 0.9189 | 56.3% | 51.5% |
| method model, unshrunk | 1371 | 0.9156 | 55.9% | 50.8% |
| base rate (division x scheduled rounds, recent era) | 1371 | 0.9950 | 52.1% | 45.5% |

| round of finish (1-5) | n | log loss | exact round | within 1 round |
|---|---|---|---|---|
| round model, shrunk (production, 50% model) | 684 | 1.0344 | 51.2% | 81.4% |
| round model, unshrunk | 684 | 1.0356 | 51.2% | 82.0% |
| base rate (method x scheduled rounds) | 684 | 1.0458 | 51.3% | 81.7% |

Uninformed reference: guessing uniformly over 3 methods costs 1.0986; over the 3 rounds of a standard fight, 1.0986. Read both tables with the base-rate row as the bar. Finish timing is close to a coin flip weighted by 'earlier is likelier', which is why the production model is shrunk toward that base rate rather than trusted outright.

---
Favorite baseline is ~65% accuracy / ~0.62 log loss on priced fights.