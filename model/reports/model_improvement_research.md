# Octagon model improvement report

**Prepared:** 4 September 2026  
**Scope:** winner, method-of-victory, exact-round prediction, data integrity, and tomorrow-card readiness

## Executive conclusion

The highest-value defect was not a shortage of model complexity. A source-format change had turned knockdown, submission-attempt, and reversal counts into strings such as `0.0`; the importer rejected them, leaving only 26 of 17,648 stat rows populated. The repaired database now has 100% coverage for all three fields and produces 373 feature columns instead of the stale 370-column snapshot.

The method architecture itself remains the right one for this amount of data. A direct KO/submission/decision LightGBM was tested and rejected because its chronological training-era log loss was worse (0.9560 versus 0.9516). The production model therefore retains its lower-variance hierarchy—first finish versus decision, then KO versus submission—and shrinks the final probabilities toward recent division/fight-length base rates (20% in the latest production fit).

The visible “always KO” problem also contained a selection bug. The application previously chose the largest individual method-by-round cell. It now chooses the largest *marginal method probability* first and, only for KO or submission, chooses the modal round conditional on that method. Outputs expose all three quantities: method probability, conditional round probability, and exact joint probability.

On the 1,010-fight validation era, the old exact-cell selector produced only 7 submission calls; the corrected hierarchy produces 42, while still letting the calibrated distribution—not a forced quota—decide. It changes 272 calls overall (old DEC/KO/SUB: 929/74/7; new: 731/237/42).

## What changed

1. **Recovered missing fight signals.** The Greco loader now accepts finite, non-negative integral counts written as either `3` or `3.0`, while still rejecting malformed or fractional values.
2. **Added a permanent coverage gate.** `octagon audit` fails if KD, submission-attempt, or reversal database coverage drops below 90%, or if the derived recent KD/submission-rate columns become empty.
3. **Fixed the feature symmetry audit.** Ordinary fighter-level style differences are no longer mistaken for cross-fighter interaction features.
4. **Rebuilt the data snapshot.** The local database, regional records, and feature parquet were replayed point-in-time; all seven audits pass.
5. **Kept the better method architecture.** The direct three-way alternative was benchmarked with the same time folds and rejected.
6. **Made method and round calls coherent.** The selected method is marginalized over rounds; the round is then conditional on that method. Decision outputs have no fabricated round.
7. **Made tomorrow's output explicit.** The API, web card, and Markdown report now show method probability, exact round, conditional round probability, and exact outcome probability.
8. **Added artifact lineage.** A tuned artifact stores a deterministic hash of its fixed historical training prefix. Newly appended fights are allowed, but a parser/feature/history revision now requires rebuilding and retraining rather than silently reusing mismatched calibration.
9. **Removed a stale debut-model path.** If the optional debut specialist ever qualifies, it is refit on current point-in-time history instead of reusing an old fitted estimator.
10. **Corrected model labeling.** Evaluation distinguishes the skill-only blend from the actually shipped market-aware probability.

## Measured results

All choices use chronological data. Architecture selection used semiannual 2017–2021 out-of-sample folds; the fixed 2022–2023 validation era was used for confirmation, not for repeatedly redesigning the split.

| Measurement | Before | Repaired snapshot | Change |
|---|---:|---:|---:|
| Populated KD / SUB.ATT / REV stat rows | 26 / 17,648 | 17,648 / 17,648 | full recovery |
| Feature columns | 370 | 373 | +3 regional-Elo fields |
| Validation method log loss | 0.9846 | 0.9763 | -0.0083 (better) |
| Validation winner-method accuracy | 50.0% | 51.6% | +1.6 points |
| Validation exact-round accuracy | 49.1% | 49.1% | unchanged |
| Validation round within ±1 | 83.8% | 83.8% | unchanged |

The validation-confirmed exact-round setting was intentionally conservative: 50% matchup hazard model and 50% historical method×fight-length rate. The larger production walk-forward pool selected a similar 55%/45% split. The model-only round score remains close to the historical baseline, so a much larger model share would add confidence without demonstrated information.

### Controlled alternatives that were rejected

| Experiment | Selection evidence | Decision |
|---|---|---|
| Direct three-class KO/submission/decision LightGBM | 2017–2021 log loss 0.9560 vs 0.9516 hierarchical | reject |
| Remove raw corner-level features (155 instead of 363 model inputs) | training-era calibrated log loss 0.6523 vs 0.6516 | reject |
| Forty-trial GBM retune | pooled training-era five-seed 0.6555 vs 0.6551; validation skill blend 0.6488 vs 0.6479 | reject |
| Isotonic calibration on both method heads | late training-era improved, but validation worsened 0.9763 -> 0.9869 | reject |
| Low-history/debut specialist | training-era low-history log loss 0.6649 vs 0.6582 main blend | reject |

This rejection log is part of the result. With 6,307 fights in the tuning era, small architectural changes can look attractive on one slice. Shipping only changes that survive a later slice is more valuable than accumulating complexity.

## Why these decisions fit a small dataset

Probability quality matters more than making each label appear equally often. LightGBM explicitly warns that imbalance weighting can improve aggregate classification metrics while producing poor individual class probabilities. That is unacceptable here because the UI and downstream betting analysis consume the probability itself, not only an argmax label. The system therefore reports the naturally rarer submission probability and uses recent base-rate shrinkage rather than forcing class balance. [LightGBM documentation](https://lightgbm.readthedocs.io/en/v3.2.1/Parameters.html)

The calibration map is learned only from walk-forward predictions that were out of sample for their underlying estimator. This follows the requirement that calibration data be independent from model fitting, and it is evaluated with proper probability scores rather than accuracy alone. [scikit-learn calibration guide](https://scikit-learn.org/stable/modules/calibration.html) Boosted trees are especially worth calibrating because their raw scores can be probability-distorted. [Niculescu-Mizil & Caruana, 2005](https://icml.cc/Conferences/2005/proceedings/papers/079_GoodProbabilities_NiculescuMizilCaruana.pdf)

The round head uses discrete hazards—probability of ending in a round given that the fight reached it—which naturally enforces that a three-round bout cannot end in rounds four or five. This is a standard survival-model construction and a better fit than an unconstrained five-class softmax. [Maul, 1994](https://onlinelibrary.wiley.com/doi/abs/10.1002/env.3170050205), [Kvamme & Borgan, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8536596/)

The broader structure agrees with MMA-specific forecasting work that combines result, method, duration, and scheduled rounds while relying more on population priors when fighter histories are thin. [Wåge & Borgan, 2022](https://doi.org/10.1016/j.ijforecast.2022.01.007) Elo/Bradley-Terry features remain valuable because they inject a parsimonious pairwise prior instead of asking a high-dimensional learner to rediscover comparative strength from a few bouts. [Szczecinski & Djebbi, 2017](https://discovery.ucl.ac.uk/id/eprint/1545162/)

## Recommended next data work

The next useful gain is higher-quality coverage, not uncontrolled feature count.

- Refresh Sherdog/regional histories for tomorrow's debutants and low-UFC-history fighters, preserving the existing identity verification and pre-fight date cutoff.
- Add historical weigh-in misses, verified short-notice replacements, stance switches, and injury/layoff context only when the observation timestamp can be frozen before each fight.
- Pursue round-level strike/grappling sequences if a legally reusable historical source becomes available; they can support a joint competing-risk model for KO, submission, and decision timing.
- Benchmark a shared multi-task representation for winner, finish, and KO-versus-submission. Related targets can regularize small samples through inductive transfer, but it should ship only if later chronological folds improve. [Caruana, 1997](https://doi.org/10.1023/A:1007379606734)
- Keep temporal evaluation fixed. Models deployed into a changing population should be assessed on later non-overlapping data, and repeated split adjustment risks selection bias. [Han et al., 2024](https://proceedings.mlr.press/v235/han24b.html), [temporal validation review](https://pmc.ncbi.nlm.nih.gov/articles/PMC10772854/)

## Operating notes for tomorrow's card

The production artifact is now calibrated through the latest available fight (22 August 2026). Its walk-forward calibration pool contains 4,745 fights; the current blend is 35% logistic and 65% calibrated GBM, method probabilities retain 20% recent base-rate shrinkage, and round probabilities retain 45% base-rate shrinkage. These are production-fit settings, not new holdout results.

1. Build or fetch the card YAML and odds.
2. Refresh only genuinely missing fighter/regional records; do not add post-fight information.
3. Run `octagon build-db` (which restores regional histories), `octagon build-features`, and `octagon audit`.
4. If the lineage guard reports a revised training prefix, run `octagon train` before prediction.
5. Run the prediction and freeze its parquet before the event begins.

The generated probability remains educational, not betting advice. On the validation era, the vig-free market is still the stronger benchmark; the system should describe its market-aware output honestly rather than claim to beat the odds.
