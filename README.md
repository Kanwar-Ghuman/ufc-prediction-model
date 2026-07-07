# Octagon Oracle — UFC Fight Outcome Prediction

[![tests](https://github.com/Kanwar-Ghuman/ufc-prediction-model/actions/workflows/ci.yml/badge.svg)](https://github.com/Kanwar-Ghuman/ufc-prediction-model/actions/workflows/ci.yml)

An educational ML pipeline that predicts UFC fight winners with **calibrated
probabilities**, evaluated honestly against real baselines, plus a
**paper-trading backtest** (simulation only — no real-money betting anywhere,
and nothing here is betting advice).

## Honest context, before any results

- The realistic ceiling for UFC prediction is roughly **60–68%** accuracy on
  properly held-out future fights. Claims of 70–80% almost always mean leakage.
- On our data, **"always pick the betting favorite" wins 65.4%** of fights
  (3,388 fights with closing odds, 2014–2023), and the vig-free market has a
  log loss of **0.617**. Those are the numbers to beat — not a coin flip.
- Raw accuracy is misleading. The goals are: beat naive baselines, produce
  calibrated probabilities (log loss / Brier / ECE), and understand *why* the
  model predicts what it does.

## Quickstart

```bash
uv sync                                     # install everything (macOS: brew install libomp first)
uv run pytest                               # 73 tests: odds math, Elo, features, models, backtest
uv run python -m octagon build-db           # data/ufc.db from the raw CSV sources
uv run python -m octagon build-features     # point-in-time feature table (parquet)
uv run python -m octagon audit              # data leakage audit — must pass
uv run python -m octagon train              # tune GBM (Optuna) + calibrate + blend -> artifacts/
uv run python -m octagon evaluate           # baselines vs. models report (validation)
uv run python -m octagon explain            # SHAP: global summary (or --fight-id N)
uv run python -m octagon backtest           # paper-trading simulation (educational)
uv run python -m octagon predict --card cards/example_card.yaml   # upcoming card
```

Notebooks: `01_eda` (data + the favorite baseline), `02_features` (the
point-in-time table), `03_errors` (error analysis + abstain band).

## Data

| Source | What | Status |
|---|---|---|
| [Greco1899/scrape_ufc_stats](https://github.com/Greco1899/scrape_ufc_stats) CSVs in `data/raw/greco/` | **Canonical**: 774 events, 8,701 fights (1994→2026-05) with per-round stats, 4,496 fighters with stable ufcstats IDs | **loaded** |
| [jansen88/ufc-data](https://github.com/jansen88/ufc-data) CSVs in `data/raw/bootstrap/` | Contributes 3,448 closing odds (2014→2023), matched onto fights by normalized names + date (100% of valid rows matched) | **loaded** |
| Our own ufcstats.com scraper (`src/octagon/scraping/`) | fetch + cache + parsers built | **blocked**: ufcstats.com sits behind a JavaScript proof-of-work bot wall. We don't bypass anti-bot protections; refreshing the Greco CSVs is the update path. |

Everything lands in one SQLite DB, `data/ufc.db` (`events`, `fights`,
`fight_stats`, `fighters`, `odds`), rebuilt from scratch by `build-db` —
no in-place patching, no state that remembers old bugs. `build-features`
then replays all fights chronologically into
`data/processed/features.parquet`: 8,547 decisive fights × 135 point-in-time
columns (career/form/rolling stats, Elo, tale of the tape, differentials).

### Known data traps (handled, fenced, or disclosed)

- **Ordering leaks the label**: sources list winners first (bootstrap ~100%,
  Greco ~63%). Dataset construction applies a seeded coin-flip corner swap;
  the audit verifies antisymmetry on real rows. The model-level symmetry test
  `predict(A,B) ≈ 1 − predict(B,A)` lands with the first model (M3).
- **Odds are best-available-line** (betmma.tips): median overround ~1.01, 24%
  of fights below 1.0. Vig-free normalization handles market probabilities;
  the backtest (M6) must disclose the ROI inflation vs. a single book.
- 54 odds rows in the source are literal `inf` — rejected at load.
- 7 fighter names are shared by two people; their tale-of-the-tape is
  treated as unknown rather than guessed.
- Records are UFC-only (no pre-UFC careers) — consistent for everyone, so
  differentials stay meaningful.

The full checklist lives in [docs/leakage_audit.md](docs/leakage_audit.md),
with each box mapped to the test or audit check that enforces it.

## Roadmap (PRD milestones)

- [x] **M1 — Data**: bootstrap loaded into SQLite; EDA notebook; scraper built
      with cache (live site bot-walled; alternative source identified)
- [x] **M2 — Features**: Greco data ingested (test years 2024+ unlocked);
      point-in-time feature table (8,547 × 135); 6-check leakage audit passing;
      Elo K tuned on validation (K=80)
- [x] **M3 — Baselines**: all baselines + walk-forward logistic regression
      evaluated on validation; report + reliability diagram generated;
      model-level symmetry test passing to machine precision
- [x] **M4 — GBM + calibration**: LightGBM tuned with Optuna over walk-forward
      folds (train era only); isotonic calibration fit on train-era OOS;
      LR+GBM blend (Phase C step 5). Honest verdict: GBM wins accuracy/AUC,
      ties LR on log loss; blend best-in-class on the priced subset
- [x] **M5 — Explainability**: symmetrized SHAP (`octagon explain`, global +
      per-fight waterfalls); error-analysis notebook; abstain band [0.45, 0.55]
      in config. Pruning tested per the PRD: top-25 features gained 0.003 log
      loss — within noise, full set kept. Key finding: when the model disagrees
      with the market it wins only ~39% of the time
- [x] **M6 — Backtest**: paper-trading sim over the priced era (flat /
      quarter-Kelly x edge thresholds) with bootstrap CIs and disclaimers.
      Result: −2% to −6% ROI, every CI contains 0 — the expected honest outcome
- [x] **M7 — Predict CLI**: `octagon predict --card cards/<file>.yaml` —
      point-in-time features, calibrated blend probability, SHAP drivers,
      market gap, abstain band. Final test-set evaluation run once (below)

## Final results — test set (2024 → 2026-05, evaluated once, after all decisions were frozen)

1,230 fights no model or tuning decision ever saw. No betting odds exist for
this era in our data, so the market baseline is absent here (on validation it
scored 67.9% / 0.604 — still the honest benchmark). These numbers were
produced by the v1 pipeline, frozen before evaluation; the v2 additions below
(strength of schedule, method-of-victory) came AFTER this run and were
validated only on 2022–2023 — the test set is spent and does not get re-run
to flatter later work.

| model | accuracy | log loss | Brier | AUC | ECE |
|---|---|---|---|---|---|
| coin flip | 0.500 | 0.693 | 0.250 | 0.500 | — |
| better record (picking rule) | 0.584 | — | — | — | — |
| higher Elo (K=80) | 0.560 | 0.681 | 0.244 | 0.591 | 0.029 |
| logistic regression (walk-forward) | 0.636 | 0.642 | 0.225 | 0.681 | 0.025 |
| GBM + isotonic | 0.625 | 0.643 | 0.226 | 0.680 | 0.034 |
| **LR+GBM blend** | 0.629 | **0.641** | **0.225** | **0.684** | 0.041 |

PRD scorecard on the untouched test set: accuracy > 60% ✓ · log loss < 0.66 ✓
· ECE < 0.05 ✓ · AUC > 0.65 ✓ · leakage audit 100% ✓ · SHAP for every
prediction ✓ · backtest report with disclaimers ✓. The one unmet target —
beating "always pick the favorite" — was measured on validation (61–63% vs
67.9%) and reported as a loss: this model does not beat the market, and the
paper-trading backtest (−2% to −6% ROI, all CIs spanning zero) says the same
thing in units.

## Development results (validation 2022–2023)

| model | n | accuracy | log loss | Brier | AUC | ECE |
|---|---|---|---|---|---|---|
| coin flip | 1010 | 0.500 | 0.693 | 0.250 | 0.500 | — |
| better record (picking rule) | 1010 | 0.571 | — | — | — | — |
| higher Elo (K=80) | 1010 | 0.556 | 0.681 | 0.244 | 0.591 | 0.031 |
| **market (vig-free favorite)** | 697 | **0.679** | **0.604** | 0.208 | 0.734 | 0.048 |
| logistic regression (walk-forward) | 1010 | 0.597 | 0.650 | 0.230 | 0.652 | 0.054 |
| GBM, tuned + isotonic | 1010 | 0.604 | 0.655 | 0.232 | 0.654 | 0.033 |
| LR+GBM blend (w tuned on train-era OOS) | 1010 | 0.602 | 0.652 | 0.230 | 0.659 | 0.038 |
| — same three on the priced subset — | 697 | 0.606 / 0.611 / 0.607 | 0.646 / 0.652 / 0.648 | | 0.663 / 0.662 / **0.669** | |

(Numbers are from the current v2 feature set and re-tune; the pre-v2 run
differed by ±0.005 log loss and ±2pp accuracy on the same fights — a useful
calibration for how much of any single number is noise.)

Read it honestly: every skill model beats every skill baseline and meets the
PRD's calibration targets (log loss < 0.66, ECE < 0.05, AUC > 0.65). The GBM
adds ranking power (+2pp accuracy, best AUC) but NOT better probabilities
than the humble logistic regression — on ~1,000 fights, log-loss differences
of 0.002 are noise. The blend is the best skill model on the priced subset
across all probability metrics, and everything is still clearly behind the
betting market — which is what the literature says should happen.
Full report: `reports/evaluation_valid.md` (regenerate with
`uv run python -m octagon evaluate`; retrain with `uv run python -m octagon
train`).

Fun fact from the coefficients: Elo difference is the strongest single
signal, followed by age difference (younger fighter favored) — both match
the published literature. Some coefficient signs (e.g. `diff_losses`
positive) are collinearity artifacts, not causal claims: with Elo and win%
already in the model, raw loss counts act as an experience proxy.

## v2 additions (beyond the original milestones)

- **`octagon refresh-data`** — re-downloads the Greco CSVs, rebuilds the DB
  and feature table, re-runs the audit. Run it after new UFC events land in
  the source repo, then `octagon train` to refresh the artifact.
- **Strength of schedule** (`opp_elo_l5`: mean opponent Elo over the last 5
  fights) — planned in PRD 5.3, adopted, and honestly a null result on
  validation log loss (LR −0.0002, GBM +0.0008): Elo already prices
  opposition quality. Kept because it's informative in SHAP explanations.
- **Method-of-victory model** (PRD v2 stretch goal): 6-class LightGBM
  ({fighter1, fighter2} × {KO, sub, decision}) with the same
  corner-symmetry guarantees (class permutation under swap, exact by
  construction). Validation, walk-forward: log loss 1.670 vs 1.734 for the
  class-prior baseline; top-1 method accuracy 29.3% vs 24.9%. In
  `octagon predict` its six probabilities are rescaled to agree with the
  calibrated blend's win probability — the blend decides *who*, this model
  only splits the *how*.

## Repo layout

```
src/octagon/
├── scraping/    # polite cached fetching + ufcstats parsers
├── db/          # SQLite schema + bootstrap loader
├── features/    # Elo (built + tested); point-in-time builders land in M2
├── models/      # (M3+) baselines, GBM, ensemble, calibration
├── eval/        # (M3+) metrics, calibration plots, error analysis
├── betting/     # odds math (built + tested); backtester lands in M6
└── cli.py       # python -m octagon <command>
notebooks/       # 01_eda, ... (02–05 land with their milestones)
tests/           # odds math, Elo invariants (incl. point-in-time guard), parsers
```

The leakage rules live in the PRD (section 6) and are enforced by tests —
the point-in-time Elo test and the symmetry test are the ones that keep the
results honest.
