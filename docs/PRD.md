# PRD: UFC Fight Outcome Prediction Model ("Octagon Oracle")

## 1. Overview

Build an end-to-end machine learning pipeline that predicts the winner of UFC fights with **well-calibrated probabilities**, evaluated honestly against real-world baselines, plus a **paper-trading backtest module** that simulates betting strategies against historical odds (no real money — simulation and analysis only).

This is also a learning project. Code should be readable, well-commented, and built in phases so the owner (an ML beginner) can understand every step. Prefer clarity over cleverness.

### 1.1 Honest context (read this first, Claude Code)

- The realistic ceiling for UFC prediction accuracy is roughly **60–68%** on properly held-out future fights. Published claims of 70–80% almost always suffer from data leakage or bad splits.
- **"Always pick the betting favorite" already wins ~63–66%** of fights. Raw accuracy is therefore a misleading metric. The real goals are: (a) beat naive baselines, (b) produce calibrated probabilities (measured by log loss / Brier score), and (c) understand *why* the model predicts what it does.
- The betting market (closing odds) is a very strong predictor. Beating it consistently is extremely hard. The betting module exists to *teach* expected value, Kelly sizing, and backtesting — success is defined as a rigorous simulation, not profit.

## 2. Goals & success metrics

| Goal | Metric | Target |
|---|---|---|
| Beat coin flip | Accuracy on time-based holdout | > 60% |
| Beat naive baseline | Accuracy vs. "always pick favorite" | ≥ favorite baseline |
| Calibrated probabilities | Log loss on holdout | < 0.66 (favorite baseline ≈ 0.63–0.65) |
| Calibration quality | Expected Calibration Error (ECE) | < 0.05, with reliability diagram |
| Discrimination | ROC AUC | > 0.65 |
| No leakage | Leakage audit checklist (Section 6) passes | 100% |
| Explainability | SHAP summary + per-fight explanation | Working for every prediction |
| Betting sim | Backtest report vs. historical closing odds | Report generated with ROI, drawdown, CLV |

## 3. Non-goals

- No real-money betting integration, no sportsbook APIs for placing bets, no financial advice output.
- No round-by-round or method-of-victory prediction in v1 (stretch goal for v2).
- No deep learning in v1 (gradient boosting wins on tabular data; a small neural net is a v2 experiment).
- No live/in-fight prediction.

## 4. Data sources

### 4.1 Primary: ufcstats.com (scraped)
- Fight results, per-fight statistics (significant strikes, takedowns, control time, knockdowns, submission attempts), fighter tale-of-the-tape (height, reach, stance, DOB), event dates, weight classes, method of victory.
- Build our own scraper (requests + BeautifulSoup, polite rate limiting ~1 req/sec, cache raw HTML to `data/raw/html/` so re-parsing never re-scrapes).
- Reference implementations to study (do not blindly copy): `Greco1899/scrape_ufc_stats` on GitHub.

### 4.2 Bootstrap datasets (to start modeling on day 1 while scraper is built)
- Kaggle: "Ultimate UFC Dataset" (mdabbert) — includes historical betting odds.
- Kaggle: "UFC Complete Dataset (All events 1996–2024)" (maksbasher).
- GitHub: `jansen88/ufc-data` — match history + fighter stats + ~9 years of historical odds (from betmma.tips).

### 4.3 Odds data
- Historical closing odds from the datasets above (odds coverage realistically starts ~2013–2014).
- Optional live odds for upcoming events: The Odds API (free tier) — used only for making predictions on upcoming cards and computing model-vs-market disagreement.

### 4.4 Storage
- Raw scrapes → `data/raw/` (immutable). Cleaned tables → `data/processed/` as Parquet. A single SQLite DB `data/ufc.db` with tables: `events`, `fights`, `fight_stats`, `fighters`, `odds`.

## 5. Feature engineering (the heart of the project)

All features must be computed **point-in-time**: for a fight on date D, use only information available *before* D.

### 5.1 Static / physical
- Age at fight time (and age difference — consistently a top predictor in the literature)
- Height, reach, reach differential, stance matchup (orthodox vs southpaw etc.)
- Weight class, gender, title fight flag, number of rounds scheduled

### 5.2 Career & form (rolling, pre-fight only)
- Record entering the fight: wins, losses, win %, current win/loss streak
- Rolling averages over last 3 and last 5 fights: significant strikes landed/absorbed per minute, striking accuracy, striking defense, takedowns landed/attempted per 15 min, takedown accuracy and defense, control time %, knockdowns per fight
- Finish rates: KO/TKO rate, submission rate, decision rate (both winning and losing by each method)
- Durability: times KO'd, times submitted (recency-weighted)
- Layoff: days since last fight; fights in last 12/24 months
- Total octagon time; average fight length; late-round (R3+) finish rate as a cardio proxy
- Short-notice fight flag if derivable

### 5.3 Opponent-adjusted skill
- **Elo rating** per fighter, updated after each fight (K tuned by validation; optional margin-of-victory adjustment for finishes). Elo difference is a feature.
- Optional v2: Glicko-2 or TrueSkill; strength-of-schedule (mean opponent Elo over last 5).

### 5.4 Matchup differentials
- For every paired stat, include the **difference** (fighter A minus fighter B). Literature shows differentials carry most of the signal.

### 5.5 Symmetry requirement (critical)
The model must be invariant to fighter ordering. UFCStats lists winners first / red corner conventions leak the label. Mitigation:
- Randomly swap fighter A/B (and negate differentials, flip label) during dataset construction, OR train on both orderings, OR enforce an antisymmetric architecture (predict from differentials only).
- Unit test: `predict(A, B) ≈ 1 − predict(B, A)` for a sample of fights.

### 5.6 Odds features — handle with care
Train **two model variants**:
1. **Skill model** (no odds features) — the "pure" model, used for learning and SHAP analysis.
2. **Market-aware model** (includes opening/closing odds implied probability) — shows how much the market knows; used for the betting sim's "edge vs. market" analysis. Never claim the market-aware model's accuracy as "our model beat the odds."

## 6. Data leakage audit (must pass before any model is trusted)

- [ ] No feature uses stats from the fight being predicted (per-fight stats are outputs, not inputs — only their *historical rolling aggregates* are inputs).
- [ ] All rolling features verified via spot checks: recompute 10 random fighters' features by hand from raw data.
- [ ] Fighter records/Elo computed strictly from fights dated before the target fight.
- [ ] Train/validation/test split is **chronological** (e.g., train ≤ 2021, validate 2022–2023, test 2024+). Never random-split fights.
- [ ] Symmetry test from 5.5 passes.
- [ ] No duplicate fights across splits; rematches audited.
- [ ] Scaler/encoder/imputer fit on train only (use sklearn Pipelines).

## 7. Modeling plan (phased)

### Phase A — Baselines
1. Coin flip; always pick fighter with better record; always pick betting favorite (where odds exist); always pick higher Elo.
2. **Logistic regression** on differentials (interpretable, calibrated by nature). This is the reference model.

### Phase B — Gradient boosting
3. XGBoost / LightGBM / CatBoost with early stopping; hyperparameter search via Optuna using **walk-forward (expanding window) time-series CV**, not k-fold.
4. Probability calibration on validation data (isotonic or Platt); verify with reliability diagrams.

### Phase C — Ensemble & analysis
5. Simple weighted/stacked ensemble of Phase A–B models (logistic regression meta-learner).
6. SHAP feature importance (global + per-fight waterfall plots). Prune to top ~40–50 features if it helps validation log loss.
7. Error analysis notebook: where does the model fail? (Upsets, debuting fighters with no history, short-notice fights, weight-class changes.) Define a "low-confidence / abstain" band (e.g., 45–55%).

### Phase D — Betting simulation (paper only)
8. Convert American/decimal odds → implied probability; **remove the vig** (normalize the overround) to get fair market probabilities.
9. Expected value per bet: `EV = p_model × payout − (1 − p_model)`. Flag bets where model probability exceeds vig-free market probability by a threshold (e.g., ≥ 4–5 edge points).
10. Staking strategies to simulate: flat stake, fractional Kelly (¼ Kelly cap), EV-threshold filter.
11. Walk-forward backtest on the test years: report ROI, total units, max drawdown, hit rate, closing line value (CLV), number of bets, and bootstrap confidence intervals on ROI. **Print a prominent disclaimer that this is a simulation, past results don't predict future returns, and this tool does not constitute betting advice.**

### Phase E — Prediction on upcoming cards
12. CLI command: `python -m octagon predict --event next` → scrape/fetch the upcoming card, build point-in-time features, output each fight's probabilities, SHAP explanation, model-vs-market gap, and confidence band. Output a clean markdown/HTML report.

## 8. Architecture & repo layout

```
ufc-predictor/
├── data/                  # raw/, processed/, ufc.db (gitignored)
├── src/octagon/
│   ├── scraping/          # ufcstats scraper + HTML cache
│   ├── db/                # schema, loaders
│   ├── features/          # point-in-time feature builders, Elo
│   ├── models/            # baselines, gbm, ensemble, calibration
│   ├── eval/              # metrics, calibration plots, error analysis
│   ├── betting/           # odds utils, EV, Kelly, backtester
│   └── cli.py             # scrape / build-features / train / evaluate / backtest / predict
├── notebooks/             # 01_eda, 02_features, 03_models, 04_errors, 05_backtest
├── tests/                 # pytest: leakage tests, symmetry test, Elo tests, odds-math tests
├── reports/               # generated evaluation + backtest reports
├── pyproject.toml         # python 3.11+, pandas, scikit-learn, xgboost, lightgbm,
│                          # catboost, optuna, shap, beautifulsoup4, requests, matplotlib
└── README.md
```

Engineering requirements:
- Type hints, docstrings explaining the *why* (this is a learning codebase).
- `pytest` suite; the leakage/symmetry tests are non-negotiable and run in CI.
- Deterministic seeds; config in a single `config.yaml`; log all experiment metrics to a simple CSV or MLflow.
- Every training run saves: model artifact, feature list, split dates, metrics, calibration plot.

## 9. Milestones

1. **M1 — Data**: bootstrap Kaggle data loaded into SQLite; EDA notebook; scraper working with cache.
2. **M2 — Features**: point-in-time feature table built; leakage audit checklist passing; Elo implemented and unit-tested.
3. **M3 — Baselines**: all baselines + logistic regression evaluated with walk-forward splits; metrics report generated.
4. **M4 — GBM + calibration**: tuned boosted model beats logistic regression on log loss; reliability diagram acceptable.
5. **M5 — Explainability & errors**: SHAP reports; error-analysis notebook; abstain band defined.
6. **M6 — Backtest**: paper-trading backtest report with ROI/drawdown/CLV and disclaimers.
7. **M7 — Predict CLI**: upcoming-card predictions with explanations; polished README with honest results.

## 10. Acceptance criteria

- All Section 2 metrics reported on a **chronological test set the model never touched**, side-by-side with all baselines.
- Leakage checklist committed to the repo and every box verified.
- README states results honestly, including where the model loses to the closing line.
- Betting module clearly labeled simulation/educational; no real-money functionality anywhere.
