# Data leakage checklist

Re-run `uv run pytest` and `uv run python -m octagon audit` after any change
to data loading or feature code.

- [x] **No feature uses stats from the fight being predicted.**
  Per-fight stats enter only as historical rolling aggregates, taken from
  each fighter's history before the current fight is appended.
  `audit: no current-fight or snapshot columns leaked in`,
  `test_debut_fighter_has_no_history`.

- [x] **Rolling features match an independent recomputation.**
  `audit: records match independent SQL recomputation`,
  `audit: publicly-known records reproduce`,
  `test_history_arithmetic_by_hand`.

- [x] **Records and Elo use only fights dated before the target.**
  `test_point_in_time_by_truncation`,
  `test_point_in_time_truncation_includes_regional`,
  `test_run_history_returns_pre_fight_ratings`.
  Elo K is chosen with `select_k` on dates ≤ `train_end`
  (`test_select_k_ignores_labels_after_train_end`).

- [x] **Chronological train / valid / test split.**
  Train through 2021-12-31, valid 2022–2023, test 2024+ (`config.yaml`).
  `audit: chronological split boundaries hold`.

- [x] **Predictions are invariant to fighter order.**
  Dataset construction applies a seeded corner swap. Logistic regression is
  antisymmetric by architecture. Enforced by
  `test_swap_corners_is_an_involution_and_antisymmetric`,
  `audit: differentials antisymmetric on real rows`, and
  `test_model_symmetry_predict_ab_equals_one_minus_predict_ba` (1e-12).
  Every model is added to that test (see `test_debut.py`, `test_gbm.py`).

- [x] **Research features (form, rematch, common opponents, style) are
  pre-fight only.**
  `test_research_features_survive_truncation`,
  `test_rematch_sees_only_the_previous_meeting`.

- [x] **Regional / pre-UFC features are pre-fight only.**
  `regional_snapshot` filters Sherdog rows to `date < on_date`.
  `test_regional_features_use_only_pre_debut_fights`,
  `test_regional_elo_ignores_fights_on_or_after_the_snapshot_date`.
  UFC bouts on Sherdog are dropped by organization name, not by debut date —
  a debut-date cutoff would erase regional history for fighters who have not
  yet fought in the UFC.

- [x] **No duplicate fights across splits.**
  Pairwise disjoint `fight_id`s plus date monotonicity. Rematches that
  span splits are counted and kept.

- [x] **Scalers / imputers fit on earlier fights only.**
  Preprocessing lives inside sklearn pipelines inside walk-forward folds.
  `test_walk_forward_only_predicts_inside_windows`.

## Data caveats

- Odds are betmma.tips best-available line (median overround ~1.01). Fine
  for vig-free market probabilities; simulated ROI is kinder than a single
  book.
- Seven fighter names are shared by two people. Tale-of-the-tape is left
  unknown; rolling history may mix them (<0.2% of fights).
- Core rolling stats are UFC-only. `pre_ufc_*` columns fill in Sherdog /
  Wikipedia where a page was found; missing pages stay NaN.
- Regional records are whatever Sherdog had when last scraped. A later
  correction to a 2015 record is invisible on a 2015-dated training row.
- Sherdog name search takes the first match. Common names can resolve to
  the wrong person. Cards should be resolved via `--event-url`.
