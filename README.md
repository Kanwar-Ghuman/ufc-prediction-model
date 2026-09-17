# UFC Fight Outcome Prediction

Walk-forward pipeline that scores UFC bouts with calibrated win, method, and
round probabilities. Skill models beat record/Elo baselines on a time-based
holdout. They do not beat closing-line odds.

Paper-trading lives in `octagon backtest`

Two packages:

| Path | Role |
|---|---|
| `model/` | Data, features, training, evaluation, CLI, read-only FastAPI |
| `frontend/` | Next.js UI over that API. It does not train or score fights. |

## Results

Test set: 1,373 fights dated 2024 onward. No odds coverage in this era.

| Model | n | Accuracy | Log loss | Brier | AUC | ECE |
|---|---|---|---|---|---|---|
| Coin flip | 1373 | 0.500 | 0.693 | 0.250 | 0.500 | — |
| Better record | 1373 | 0.589 | — | — | — | — |
| Higher Elo | 1373 | 0.565 | 0.679 | 0.243 | 0.598 | 0.032 |
| Logistic regression | 1373 | 0.659 | 0.627 | 0.219 | 0.707 | 0.027 |
| GBM + isotonic | 1373 | 0.657 | 0.630 | 0.220 | 0.704 | 0.034 |
| LR+GBM blend | 1373 | **0.660** | **0.627** | **0.219** | **0.709** | 0.035 |

Validation (2022–2023), where closing odds exist:

| Model | n | Accuracy | Log loss |
|---|---|---|---|
| Market (vig-free favorite) | 697 | **0.679** | **0.604** |
| LR+GBM blend (same fights) | 697 | 0.624 | 0.646 |
| Market-aware stack | 697 | 0.683 | 0.601 |

The stack is the market plus a small residual. The paper-trading backtest
lands around −2% to −6% ROI with CIs that include zero.

Full tables and plots: `model/reports/evaluation_{valid,test}.md`.

## Setup

```bash
cd model
uv sync                          # macOS: brew install libomp first
uv run pytest
uv run python -m octagon build-db       # also restores cached regional histories
uv run python -m octagon build-features
uv run python -m octagon audit
uv run python -m octagon train
uv run python -m octagon evaluate
```

Upcoming card:

```bash
cp .env.example .env             # then fill in ODDS_API_KEY / YOUTUBE_API_KEY
uv run python -m octagon refresh-data
uv run python -m octagon fetch-card
uv run python -m octagon fetch-odds --card cards/<slug>.yaml   # needs ODDS_API_KEY
uv run python -m octagon fetch-media --card cards/<slug>.yaml
uv run python -m octagon fetch-context --card cards/<slug>.yaml --event "UFC …"
uv run python -m octagon predict --card cards/<slug>.yaml
```

Predictions now default to `prediction.mode: skill_only` and
`prediction.call_all: true` in `model/config.yaml`: every fight gets a winner,
including close fights. Odds, ranking nudges and social sentiment cannot move
these probabilities. Reports show the individual LR/GBM votes, recent fights,
and striking/grappling evidence. Low confidence still means low confidence.
Older frozen cards retain their original policy.

September 11 corrections replace the recent-form score with performance
relative to each opponent's pre-fight Elo expectation and preserve genuine
zero defensive rates. On the same 1,010 validation fights, accuracy rose from
60.99% to 61.78%, and log loss fell from 0.64905 to 0.64788. This is a modest
diagnostic improvement, not a new untouched-test result; its paired accuracy
interval includes zero. Details: `model/reports/noche_2026_improvements.md`.

September 17: the scorecard and the evaluation table graded the method call
with a different rule than the card reported — they pooled KO and submission
into "a finish" and resolved that first. Since KO is ~65% of finishes, a
resolved finish nearly always resolved to KO, so the grader called KO on 48%
of test-era fights that ended in KO 33% of the time. All three call sites now
share `method.call_group`, a plain argmax. Test-era method accuracy 51.5% ->
54.7%; a constant "decision" scores 51.8%. Winner probabilities are unchanged.

Or `octagon day-before --card … --event …`. After the event,
`octagon score-card --card …` grades the frozen file, not a refit.

Site:

```bash
cd model && uv run python -m octagon serve      # http://127.0.0.1:8000
cd frontend && npm install && npm run dev       # http://localhost:3000
```

`NEXT_PUBLIC_API_BASE` defaults to `http://127.0.0.1:8000`. See
`frontend/.env.local.example`.

## Data

| Source | Role |
|---|---|
| [Greco1899/scrape_ufc_stats](https://github.com/Greco1899/scrape_ufc_stats) CSVs | Canonical fights, stats, fighters |
| [jansen88/ufc-data](https://github.com/jansen88/ufc-data) | Closing odds 2014–2023 |
| Wikipedia / The Odds API / Sherdog / ufc.com | Cards, live lines, regional records, portraits |

ufcstats.com is behind a JS bot wall; this repo does not bypass it.
`octagon refresh-data` pulls the Greco CSVs instead.

SQLite at `model/data/ufc.db`. Features at
`model/data/processed/features.parquet` (point-in-time only). Corners are
randomly swapped so listing order cannot leak the winner.

Leakage checklist: [model/docs/leakage_audit.md](model/docs/leakage_audit.md).

## Layout

```
model/
├── src/octagon/     # scraping, db, features, models, eval, betting, api, cli
├── notebooks/       # EDA, features, error analysis
├── cards/           # event YAML
├── supplements/     # hand-verified fights missing from the upstream feed
├── reports/         # evaluation markdown, plots, frozen card predictions
└── tests/
frontend/src/
├── app/             # next card, card list, results
├── components/
└── lib/api.ts
```

## License

[MIT](LICENSE).
