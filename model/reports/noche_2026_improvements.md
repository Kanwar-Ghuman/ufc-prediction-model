# Model changes and Noche UFC validation — September 11, 2026

The model now gives a winner for every fight using the skill model alone. Betting odds, ranking nudges, and social sentiment cannot alter the new card probabilities. Close probabilities are still labeled close; selecting a winner does not establish high confidence.

## Measured comparison

The feature corrections were compared on identical historical rows. Each semiannual validation window was predicted from earlier fights only. The isotonic calibration and LR/GBM blend weight were fitted on 2017–2021 out-of-sample predictions, then frozen for 2022–2023. Both runs used the same inherited GBM settings, five seeds, and LR settings (C=0.03, ten-year recency half-life). No odds were inputs.

| 2022–2023 validation, 1,010 fights | Before | Corrected |
|---|---:|---:|
| Winner accuracy | 60.99% | 61.78% |
| Log loss (lower is better) | 0.64905 | 0.64788 |
| Brier score (lower is better) | 0.22907 | 0.22855 |
| AUC | 0.66283 | 0.66485 |
| Calibration error / ECE (lower is better) | 0.02656 | 0.03117 |

There were 22 newly correct calls and 14 newly wrong calls: eight net additional correct calls. A paired bootstrap that resamples event dates (10,000 draws, seed 42) gives a 95% accuracy-gain interval of **−0.39 to +1.98 percentage points**. This includes zero. Calibration error worsened slightly even though log loss and Brier score improved. This is a modest diagnostic gain, not evidence of a large or statistically established improvement.

The validation era was already used in earlier project work; it is not a fresh untouched test. Inherited hyperparameter choices also limit how independently this comparison can be interpreted. No new 2024+ test-set score was used to select these changes. Production calibration through September 5 is a separate fit and must not be described as validation performance.

Reproduction: run `PYTHONPATH=src .venv/bin/python reports/noche_2026_experiment/benchmark.py` from `model/`. The comparison snapshots and previous artifact are kept locally in `model/artifacts/noche_2026_before/` (ignored by Git); JSON results and the two per-fight validation predictions are in `model/reports/noche_2026_experiment/`. The comparison isolates the form/zero-defense changes, before the subsequent card-specific regional-history and Tarin-profile repairs.

## Changes

1. **Corrected opponent-adjusted recent form.** The previous formula multiplied both wins and losses by opponent Elo, penalizing a loss to an elite opponent more than a loss to a weak opponent. The new score is twice the difference between the result and the expected result from both fighters' ratings entering that historical bout. Today's rating cannot rewrite an old expectation. Both last-three and last-five form windows use the correction.
2. **Preserved observed zero defense.** A 0% takedown defense or 0% ground-strike exposure is no longer replaced by a missing-data default in style interactions.
3. **Independent prediction mode.** `prediction.mode: skill_only` bypasses the market, ranking, and sentiment adjustment paths. Odds can be retained for comparison, but do not influence the choice or method probabilities.
4. **A choice for every matchup.** `prediction.call_all: true` persists into frozen predictions and the API. Older files keep their original abstention policy. Low probabilities are not increased to make a choice look safer.
5. **Expanded evidence.** Frozen outputs retain the independent logistic and calibrated GBM votes, recent professional fights, age/reach availability, striking rates, takedowns, defense, control time, opponent strength, and form. The component spread is a sensitivity check, not a statistical confidence interval. SHAP drivers describe one tree member's score and are not causal proof or an exact decomposition of the final blend.
6. **Refreshed histories.** Public Greco/UFCStats data now extends through September 5, yielding 8,717 decisive fights. Regional records for the pictured card were refreshed, including both Rosas and King and Gantt's verified Thomas Gantt profile.
7. **Resolved Tarin's profile alias.** UFC explicitly bills Regina Tarin on the Regina Malpica Rivera profile. The tale-of-the-tape loader now recovers that known profile, including her birth date, when no exact Tarin profile exists. Ambiguous shared names still remain missing rather than being guessed.

The model already used last-three/last-five striking, grappling, finishing history, age, inactivity, opponent Elo, style matchups, rematches, and common opponents. These changes repair inputs and expose the evidence; they do not claim to watch tape or know undisclosed injuries, training-camp quality, or mental state.

## Card and source verification

All 13 pictured matchups match the published card. The main event is five rounds; the others are three. Ige is fighting at bantamweight, Bahamondes at welterweight, and Elliott–Chairez at a 130-pound catchweight. All 26 fighters were reported within their respective limits. [UFC card preview](https://www.ufc.com/news/fight-fight-preview-noche-ufc-phoenix-silva-delgado-2026), [weigh-in results](https://www.mmafighting.com/ufc/509542/noche-ufc-weigh-in-video-silva-vs-delgado).

Delgado's replacement assignment is verified in his pre-fight interview. It is saved as context, without inventing a calibrated numerical penalty. [UFC interview](https://www.ufc.com/news/jose-miguel-delgado-everything-has-built-moment-noche-ufc).

Identity evidence: [Gantt's UFC profile](https://www.ufc.com/athlete/thomas-gantt), [Gantt's Sherdog history](https://www.sherdog.com/fighter/Thomas-Gantt-428202), [Tarin's UFC profile](https://www.ufc.com/athlete/regina-malpica-rivera), [Rosas's history](https://www.sherdog.com/fighter/Jessie-Rosas-338741), [King's history](https://www.sherdog.com/fighter/Sean-King-423706).

## Validation and delivery

The seven database/feature audits passed after the refresh and rebuild. The automated tests cover opponent-strength ordering, point-in-time form, zero defensive rates, exact odds independence, frozen call-all behavior, alias resolution, and the existing model/data contracts. The full suite passed 289 tests. Targeted checks after the final reporting edits are recorded with the card delivery.

The dated card report and parquet are the predictions to grade after the event. Future retraining must not replace those numbers when scoring this card.
