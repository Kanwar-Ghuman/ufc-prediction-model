# Evaluation report — valid split

Generated 2026-07-07 01:15 UTC. Fights dated (2021-12-31, 2023-12-31]. Walk-forward windows: 2022-01-01->2022-06-30, 2022-07-01->2022-12-31, 2023-01-01->2023-06-30, 2023-07-01->2023-12-16

| model | n | accuracy | log loss | Brier | ROC AUC | ECE | note |
|---|---|---|---|---|---|---|---|
| coin flip | 1010 | 0.5000 | 0.6931 | 0.2500 | 0.5000 | 0.0208 |  |
| better record | 1010 | 0.5713 | 10.4166 | 0.4015 | 0.5794 | 0.3762 |  |
| higher Elo | 1010 | 0.5564 | 0.6806 | 0.2437 | 0.5908 | 0.0313 |  |
| market (vig-free favorite) | 697 | 0.6793 | 0.6035 | 0.2084 | 0.7344 | 0.0475 | priced fights only |
| logistic regression (walk-forward) | 1010 | 0.5970 | 0.6503 | 0.2300 | 0.6518 | 0.0537 |  |
| GBM (walk-forward, tuned) | 1010 | 0.5931 | 0.6548 | 0.2316 | 0.6534 | 0.0357 |  |
| GBM + isotonic (fit on train-era OOS) | 1010 | 0.6035 | 0.6552 | 0.2315 | 0.6536 | 0.0327 |  |
| LR+GBM blend (w=0.25, tuned on train-era OOS) | 1010 | 0.6020 | 0.6515 | 0.2301 | 0.6587 | 0.0375 |  |
| logistic regression (priced subset) | 697 | 0.6055 | 0.6458 | 0.2278 | 0.6633 | 0.0401 | same fights as market row |
| GBM + isotonic (priced subset) | 697 | 0.6112 | 0.6519 | 0.2297 | 0.6622 | 0.0335 | same fights as market row |
| LR+GBM blend (priced subset) | 697 | 0.6069 | 0.6477 | 0.2281 | 0.6685 | 0.0365 | same fights as market row |

Reading guide: 'better record' is a picking rule (0/0.5/1 outputs) — its log loss is meaningless by design; compare models on log loss / Brier / ECE against the market row, on accuracy against all rows.

![reliability diagram](reliability_valid.png)

## Logistic regression — largest standardized coefficients

Positive means: the bigger fighter1's edge in this differential, the likelier fighter1 wins (per the model).

| feature | coefficient |
|---|---|
| diff_elo | +0.334 |
| diff_age | -0.293 |
| diff_td15_l5 | +0.258 |
| diff_sapm_l5 | -0.234 |
| diff_dec_win_rate | -0.207 |
| diff_td15_l3 | -0.182 |
| diff_fights_12m | +0.163 |
| diff_opp_elo_l5 | +0.135 |
| diff_avg_fight_min | +0.127 |
| diff_losses | +0.126 |
| diff_ko_win_rate | -0.114 |
| diff_slpm_l5 | +0.111 |
| diff_sapm_l3 | +0.110 |
| diff_sig_acc_l3 | +0.104 |
| diff_n_fights | -0.102 |

---
*Honest context: 'always pick the favorite' wins ~65% of priced fights and the vig-free market's log loss is ~0.62. Beating the record/Elo baselines is expected; approaching the market is the actual fight.*