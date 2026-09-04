# Evaluation report — valid split

Generated 2026-09-01 22:06 UTC. Fights dated (2021-12-31, 2023-12-31]. Walk-forward windows: 2022-01-01->2022-06-30, 2022-07-01->2022-12-31, 2023-01-01->2023-06-30, 2023-07-01->2023-12-16

| model | n | accuracy | log loss | Brier | ROC AUC | ECE | note |
|---|---|---|---|---|---|---|---|
| coin flip | 1010 | 0.5000 | 0.6931 | 0.2500 | 0.5000 | 0.0208 |  |
| better record | 1010 | 0.5713 | 10.4166 | 0.4015 | 0.5794 | 0.3762 |  |
| higher Elo | 1010 | 0.5564 | 0.6806 | 0.2437 | 0.5908 | 0.0313 |  |
| market (vig-free favorite) | 697 | 0.6793 | 0.6035 | 0.2084 | 0.7344 | 0.0475 | priced fights only |
| logistic regression (walk-forward) | 1010 | 0.6208 | 0.6477 | 0.2284 | 0.6668 | 0.0334 |  |
| GBM (walk-forward, tuned) | 1010 | 0.6020 | 0.6521 | 0.2302 | 0.6616 | 0.0293 |  |
| GBM + isotonic (fit on train-era OOS) | 1010 | 0.6099 | 0.6509 | 0.2296 | 0.6625 | 0.0246 |  |
| LR+GBM blend (w=0.15, tuned on train-era OOS) | 1010 | 0.6149 | 0.6482 | 0.2285 | 0.6677 | 0.0307 |  |
| logistic regression (priced subset) | 697 | 0.6313 | 0.6395 | 0.2245 | 0.6831 | 0.0509 | same fights as market row |
| GBM + isotonic (priced subset) | 697 | 0.6148 | 0.6493 | 0.2287 | 0.6687 | 0.0239 | same fights as market row |
| LR+GBM blend (priced subset) | 697 | 0.6241 | 0.6455 | 0.2271 | 0.6767 | 0.0294 | same fights as market row |
| market-aware stack (a=0.97, b=0.34) | 697 | 0.6829 | 0.6008 | 0.2076 | 0.7344 | 0.0508 | IS the odds + residual skill — never 'beat the odds' |
| shipped (stack + trap) | 1010 | 0.6441 | 0.6206 | 0.2165 | 0.7073 | 0.0341 | predict.py market layer; no YouTube/news. 7 market-trap abstains |
| shipped (stack + trap, priced subset) | 697 | 0.6664 | 0.6055 | 0.2097 | 0.7294 | 0.0443 | same fights as market row |

Reading guide: 'better record' is a picking rule (0/0.5/1 outputs) — its log loss is meaningless by design; compare models on log loss / Brier / ECE against the market row, on accuracy against all rows.

![reliability diagram](reliability_valid.png)

## Logistic regression — largest standardized coefficients

Positive means: the bigger fighter1's edge in this differential, the likelier fighter1 wins (per the model).

| feature | coefficient |
|---|---|
| diff_ko_end_rate_l5 | -0.588 |
| diff_dec_end_rate_l5 | -0.573 |
| diff_career_wins | +0.467 |
| diff_career_n_fights | -0.443 |
| diff_sub_end_rate_l5 | -0.439 |
| diff_avg_fight_min | +0.371 |
| diff_losses | +0.353 |
| diff_style_age_wrestle | +0.313 |
| diff_ko_win_rate | +0.261 |
| diff_elo | +0.248 |
| diff_strike_elo | +0.232 |
| diff_finish_involvement | +0.223 |
| diff_wins | -0.208 |
| diff_age | -0.196 |
| diff_sapm_l5 | -0.183 |

## How the fight ends (method + round)

Both models are walk-forward and scored only where they apply: the method model on every decisive fight, the round model on finishes only (a decision has no round to predict). The method model answers how the winner wins (KO / submission / decision); fight-level KO/sub/dec is that split averaged across corners, which is what the scorecard grades. The round model answers a conditional question — given that this fighter finished by this method, which round? — so its opponent is the historical round split for the same method and the same fight length.

| method of victory (how the winner wins) | n | log loss | winner's method | fight KO/sub/dec |
|---|---|---|---|---|
| method model, shrunk (production, 75% model) | 1008 | 0.9846 | 50.0% | 49.4% |
| method model, unshrunk | 1008 | 0.9952 | 51.0% | 49.9% |
| base rate (division x scheduled rounds, recent era) | 1008 | 1.0300 | 48.5% | 46.0% |

| round of finish (1-5) | n | log loss | exact round | within 1 round |
|---|---|---|---|---|
| round model, shrunk (production, 50% model) | 530 | 1.0446 | 49.1% | 83.8% |
| round model, unshrunk | 530 | 1.0536 | 48.1% | 84.2% |
| base rate (method x scheduled rounds) | 530 | 1.0934 | 49.1% | 83.8% |

Uninformed reference: guessing uniformly over 3 methods costs 1.0986; over the 3 rounds of a standard fight, 1.0986. Read both tables with the base-rate row as the bar. Finish timing is close to a coin flip weighted by 'earlier is likelier', which is why the production model is shrunk toward that base rate rather than trusted outright.

---
Favorite baseline is ~65% accuracy / ~0.62 log loss on priced fights.