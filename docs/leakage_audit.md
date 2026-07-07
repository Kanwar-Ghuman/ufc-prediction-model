# Data leakage audit checklist (PRD section 6)

Every box must stay checked before any model result is trusted. Each item
names its enforcement mechanism — a unit test (runs in `uv run pytest`) or an
artifact check (runs in `uv run python -m octagon audit` against the real
feature table). Re-run both after ANY change to the data or feature code.

- [x] **No feature uses stats from the fight being predicted.**
  Per-fight stats enter only as historical rolling aggregates (`_l3`/`_l5`
  windows), built from each fighter's history *before* the current fight is
  appended (`build_feature_rows` order of operations).
  Enforced by: `audit: no current-fight or snapshot columns leaked in`
  (column scan) + `test_debut_fighter_has_no_history` (a debut has nothing).

- [x] **Rolling features verified by independent recomputation.**
  Enforced by: `audit: records match independent SQL recomputation`
  (random fighters' records recomputed via raw SQL that shares no code with
  the builder), `audit: publicly-known records reproduce` (McGregor 10-3
  into UFC 264, Khabib 12-0 into UFC 254, Adesanya 12-1 into UFC 281), and
  `test_history_arithmetic_by_hand` (hand-computed rolling rates).

- [x] **Records/Elo computed strictly from fights dated before the target
  fight.** Enforced by: `test_point_in_time_by_truncation` (deleting future
  fights must not change any earlier fight's features) and
  `test_run_history_returns_pre_fight_ratings` (Elo features are the
  ratings *entering* the fight).

- [x] **Chronological train/valid/test split, never random.**
  train ≤ 2021-12-31, valid 2022–2023, test 2024+ (config.yaml `splits`).
  Enforced by: `audit: chronological split boundaries hold`.

- [x] **Symmetry: the model must be invariant to fighter ordering.**
  Dataset construction applies a seeded coin-flip corner swap per fight
  (f1/f2 exchanged, differentials negated, label flipped) so ordering
  can't be learned. The reference logistic regression is antisymmetric by
  architecture (differentials only, zero-imputed, uncentered scaling, no
  intercept). Enforced by:
  `test_swap_corners_is_an_involution_and_antisymmetric`,
  `audit: differentials antisymmetric on real rows`, and the model-level
  `test_model_symmetry_predict_ab_equals_one_minus_predict_ba`
  (holds to 1e-12). Any M4+ model must add itself to that test.

- [x] **No duplicate fights across splits; rematches audited.**
  fight_ids are unique (one row per fight); the audit counts rematch pairs
  spanning train and later splits (35 pairs, reported, kept — excluding
  rematches would misrepresent the real prediction task).

- [x] **Scalers/encoders/imputers fit on train only.**
  No preprocessing is baked into the feature table (raw values + NaN).
  All preprocessing lives inside sklearn Pipelines
  (`octagon.models.logistic.make_pipeline`), fit exclusively inside
  `fit()`/`walk_forward_predict()` on strictly-earlier fights.
  Enforced by: `test_walk_forward_only_predicts_inside_windows`.

## Known data caveats (not leakage, but honesty)

- Odds are betmma.tips **best-available-line** odds: median overround ~1.01,
  24% of fights below 1.0. Fine for vig-free market probabilities (we
  normalize), but the M6 backtest must disclose that betting simulated at
  best-available prices inflates ROI relative to any single book.
- Fights reference fighters by name; 7 names are shared by two fighters.
  Their tale-of-the-tape features are set to unknown rather than guessed
  (`load_tott`), and their rolling histories may mix two people — accepted,
  documented noise (<0.2% of fights).
- Fighter records are **UFC-only** (ufcstats has no pre-UFC fights), so
  "wins entering" undercounts full MMA careers, especially for debutants.
  Consistent across all fighters, so differentials stay meaningful.
