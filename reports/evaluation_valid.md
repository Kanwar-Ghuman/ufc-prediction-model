# Evaluation report — valid split

Generated 2026-07-07 03:39 UTC. Fights dated (2021-12-31, 2023-12-31]. Walk-forward windows: 2022-01-01->2022-06-30, 2022-07-01->2022-12-31, 2023-01-01->2023-06-30, 2023-07-01->2023-12-16

| model | n | accuracy | log loss | Brier | ROC AUC | ECE | note |
|---|---|---|---|---|---|---|---|
| coin flip | 1010 | 0.5000 | 0.6931 | 0.2500 | 0.5000 | 0.0208 |  |
| better record | 1010 | 0.5713 | 10.4166 | 0.4015 | 0.5794 | 0.3762 |  |
| higher Elo | 1010 | 0.5564 | 0.6806 | 0.2437 | 0.5908 | 0.0313 |  |
| market (vig-free favorite) | 697 | 0.6793 | 0.6035 | 0.2084 | 0.7344 | 0.0475 | priced fights only |
| logistic regression (walk-forward) | 1010 | 0.6010 | 0.6509 | 0.2302 | 0.6522 | 0.0464 |  |
| GBM (walk-forward, tuned) | 1010 | 0.5941 | 0.6567 | 0.2326 | 0.6475 | 0.0449 |  |
| GBM + isotonic (fit on train-era OOS) | 1010 | 0.5980 | 0.6585 | 0.2335 | 0.6486 | 0.0396 |  |
| LR+GBM blend (w=0.00, tuned on train-era OOS) | 1010 | 0.5980 | 0.6585 | 0.2335 | 0.6486 | 0.0396 |  |
| logistic regression (priced subset) | 697 | 0.6098 | 0.6466 | 0.2281 | 0.6635 | 0.0320 | same fights as market row |
| GBM + isotonic (priced subset) | 697 | 0.6026 | 0.6523 | 0.2307 | 0.6570 | 0.0426 | same fights as market row |
| LR+GBM blend (priced subset) | 697 | 0.6026 | 0.6523 | 0.2307 | 0.6570 | 0.0426 | same fights as market row |
| market-aware stack (a=1.03, b=0.24) | 697 | 0.6758 | 0.6020 | 0.2082 | 0.7333 | 0.0516 | IS the odds + residual skill — never 'beat the odds' |

Reading guide: 'better record' is a picking rule (0/0.5/1 outputs) — its log loss is meaningless by design; compare models on log loss / Brier / ECE against the market row, on accuracy against all rows.

![reliability diagram](reliability_valid.png)

## Logistic regression — largest standardized coefficients

Positive means: the bigger fighter1's edge in this differential, the likelier fighter1 wins (per the model).

| feature | coefficient |
|---|---|
| diff_elo | +0.331 |
| diff_age | -0.293 |
| diff_td15_l5 | +0.250 |
| diff_sapm_l5 | -0.240 |
| diff_td15_l3 | -0.176 |
| diff_fights_12m | +0.163 |
| diff_dec_win_rate | -0.150 |
| diff_opp_elo_l5 | +0.135 |
| diff_avg_fight_min | +0.128 |
| diff_sapm_l3 | +0.108 |
| diff_fights_24m | +0.102 |
| diff_losses | +0.101 |
| diff_reach_cm | +0.097 |
| diff_td_def_l3 | +0.087 |
| diff_slpm_l5 | +0.087 |

---
*Honest context: 'always pick the favorite' wins ~65% of priced fights and the vig-free market's log loss is ~0.62. Beating the record/Elo baselines is expected; approaching the market is the actual fight.*