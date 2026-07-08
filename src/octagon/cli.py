"""Command-line interface: python -m octagon <command>.

Commands land milestone by milestone; unimplemented ones say so honestly
instead of pretending.
"""

import argparse
import re
from pathlib import Path

from octagon.config import load_config, resolve_path


def cmd_init_db(args: argparse.Namespace, cfg: dict) -> None:
    from octagon.db.schema import connect, init_db

    db_path = resolve_path(cfg["data"]["db_path"])
    init_db(connect(db_path))
    print(f"Initialized schema in {db_path}")


GRECO_FILES = ["ufc_event_details.csv", "ufc_fight_results.csv", "ufc_fight_stats.csv",
               "ufc_fighter_details.csv", "ufc_fighter_tott.csv", "ufc_fight_details.csv"]
GRECO_RAW_URL = "https://raw.githubusercontent.com/Greco1899/scrape_ufc_stats/main/"


def cmd_refresh_data(args: argparse.Namespace, cfg: dict) -> None:
    """Re-download the Greco CSVs (our update path — ufcstats itself is
    bot-walled), then rebuild the DB and feature table and re-run the audit."""
    import requests

    greco_dir = resolve_path(cfg["data"]["greco_dir"])
    greco_dir.mkdir(parents=True, exist_ok=True)
    for name in GRECO_FILES:
        resp = requests.get(GRECO_RAW_URL + name, timeout=120)
        resp.raise_for_status()
        (greco_dir / name).write_bytes(resp.content)
        print(f"  downloaded {name} ({len(resp.content) // 1024} KB)")

    cmd_build_db(args, cfg)
    cmd_build_features(args, cfg)
    print("\nRe-running the leakage audit on the fresh build:")
    cmd_audit(args, cfg)
    print("\nIf the audit passed, re-run `octagon train` so the artifact "
          "(params/calibration/blend) reflects the new data.")


def cmd_build_db(args: argparse.Namespace, cfg: dict) -> None:
    from octagon.db.build import build_db

    db_path = resolve_path(cfg["data"]["db_path"])
    counts = build_db(
        db_path,
        greco_dir=resolve_path(cfg["data"]["greco_dir"]),
        bootstrap_dir=resolve_path(cfg["data"]["bootstrap_dir"]),
    )
    print(f"Rebuilt {db_path} from raw sources:")
    for table, n in counts.items():
        print(f"  {table:>18}: {n}")


def cmd_build_features(args: argparse.Namespace, cfg: dict) -> None:
    from octagon.db.schema import connect
    from octagon.features.build import build_features

    conn = connect(resolve_path(cfg["data"]["db_path"]))
    df = build_features(conn, elo_k=cfg["elo"]["k_factor"], seed=cfg["seed"])
    out = resolve_path(cfg["data"]["processed_dir"]) / "features.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)

    with_odds = df["f1_odds"].notna().sum()
    print(f"Wrote {out}: {len(df)} fights x {len(df.columns)} columns")
    print(f"  label balance: {df['label'].mean():.3f} (should sit near 0.5 after corner swaps)")
    print(f"  swapped: {df['swapped'].mean():.3f}")
    print(f"  fights with odds: {with_odds}")
    print(f"  date range: {df['date'].min()} -> {df['date'].max()}")


def cmd_train(args: argparse.Namespace, cfg: dict) -> None:
    """Tune the GBM with walk-forward CV inside the train era, calibrate on
    train-era out-of-sample predictions, save the whole artifact."""
    import joblib
    import pandas as pd

    from octagon.eval import metrics
    from octagon.eval.report import semiannual_windows
    from octagon.models import calibration, ensemble, gbm, logistic

    df = pd.read_parquet(resolve_path(cfg["data"]["processed_dir"]) / "features.parquet")
    train_end = cfg["splits"]["train_end"]
    seed = cfg["seed"]
    include_raw = cfg["model"]["include_raw"]
    n_seeds = cfg["model"]["n_seeds"]
    windows = semiannual_windows("2016-12-31", train_end)

    print(f"Tuning LightGBM: {args.trials} Optuna trials x {len(windows)} "
          f"walk-forward folds (2017 -> {train_end}) ...")
    params, cv_loss = gbm.tune(df, windows, n_trials=args.trials, seed=seed,
                               include_raw=include_raw)
    print(f"  best walk-forward CV log loss: {cv_loss:.4f}")
    print(f"  params: {params}")

    # Out-of-sample train-era predictions -> the calibrator's training data.
    oos = gbm.walk_forward_predict(df, windows, params, seed=seed,
                                   include_raw=include_raw, n_seeds=n_seeds)
    mask = oos.notna()
    y_oos = df.loc[mask, "label"].to_numpy(dtype=float)
    p_oos = oos[mask].to_numpy()
    iso = calibration.fit_isotonic(y_oos, p_oos)
    p_cal = calibration.apply(iso, p_oos)
    print(f"  train-era OOS ({mask.sum()} fights): "
          f"log loss {metrics.log_loss(y_oos, p_oos):.4f} -> "
          f"{metrics.log_loss(y_oos, p_cal):.4f} calibrated, "
          f"ECE {metrics.ece(y_oos, p_oos):.4f} -> {metrics.ece(y_oos, p_cal):.4f}")

    # Phase C blend: LR weight chosen on the same train-era OOS predictions.
    lr_oos = logistic.walk_forward_predict(df, windows)[mask].to_numpy()
    weight_lr = ensemble.tune_weight(y_oos, lr_oos, p_cal)
    p_blend = ensemble.blend(lr_oos, p_cal, weight_lr)
    print(f"  blend weight (LR share): {weight_lr:.2f}; train-era OOS log loss "
          f"{metrics.log_loss(y_oos, p_blend):.4f}")

    # Market-aware stack (PRD 5.6): fit on the priced subset of the same OOS.
    from octagon.models import baselines, market

    priced = mask & df["f1_odds"].notna() & df["f2_odds"].notna()
    p_mkt = baselines.market(df[priced])
    idx = mask[mask].index.get_indexer(priced[priced].index)
    stack_a, stack_b = market.fit_stack(
        df.loc[priced, "label"].to_numpy(dtype=float), p_mkt, p_blend[idx])
    print(f"  market stack (a=market, b=skill): a={stack_a:.3f}, b={stack_b:.3f} "
          f"on {int(priced.sum())} priced OOS fights")

    artifacts = resolve_path("artifacts")
    artifacts.mkdir(exist_ok=True)
    metrics.reliability_diagram(
        {"GBM raw": (y_oos, p_oos), "GBM + isotonic": (y_oos, p_cal)},
        artifacts / "calibration_train_oos.png")
    final_model = gbm.fit(df[df["date"] <= train_end], params, seed=seed,
                          include_raw=include_raw, n_seeds=n_seeds)
    joblib.dump({
        "params": params,
        "cv_log_loss": cv_loss,
        "iso": iso,
        "model": final_model,
        # SHAP needs a single tree model; explanations use the first member.
        "shap_model": final_model.members[0] if hasattr(final_model, "members")
                      else final_model,
        "include_raw": include_raw,
        "n_seeds": n_seeds,
        "weight_lr": weight_lr,
        "market_stack": (stack_a, stack_b),
        "feature_list": list(gbm.feature_frame(df, include_raw=include_raw).columns),
        "splits": dict(cfg["splits"]),
        "seed": seed,
        "n_trials": args.trials,
    }, artifacts / "gbm.joblib")
    print("Saved artifacts/gbm.joblib + calibration_train_oos.png")


def cmd_evaluate(args: argparse.Namespace, cfg: dict) -> None:
    import pandas as pd

    from octagon.eval.report import evaluate_split

    if args.split == "test":
        print("=" * 70)
        print("WARNING: evaluating on the TEST split (2024+). This is the final")
        print("holdout — do this once, at the end, and report what you get.")
        print("Repeated peeking turns test into a second validation set.")
        print("=" * 70)

    df = pd.read_parquet(resolve_path(cfg["data"]["processed_dir"]) / "features.parquet")
    reports_dir = resolve_path("reports")
    md = evaluate_split(df, cfg["splits"]["train_end"], cfg["splits"]["valid_end"],
                        args.split, reports_dir)
    out = reports_dir / f"evaluation_{args.split}.md"
    out.write_text(md, encoding="utf-8")
    print(md)
    print(f"\nWrote {out}")


def cmd_fetch_card(args: argparse.Namespace, cfg: dict) -> None:
    """Build a card YAML for the next UFC event from Wikipedia."""
    import yaml

    from octagon.scraping.wikipedia import card_yaml, fight_card, next_event

    if args.event:
        page = event_name = args.event
        iso_date = args.date or raise_missing_date()
    else:
        page, event_name, iso_date = next_event()
    bouts = fight_card(page)
    if not bouts:
        raise SystemExit(f"No announced bouts parsed from Wikipedia page '{page}'.")

    card = card_yaml(event_name, iso_date, bouts)
    out = Path(args.out) if args.out else resolve_path("cards") / (
        re.sub(r"[^a-z0-9]+", "_", event_name.lower()).strip("_") + ".yaml")
    out.parent.mkdir(exist_ok=True)
    out.write_text(yaml.safe_dump(card, sort_keys=False, allow_unicode=True),
                   encoding="utf-8")
    print(f"{event_name} — {iso_date}: {len(bouts)} bouts")
    for b in bouts:
        print(f"  {b['weight_class']}: {b['fighter1']} vs. {b['fighter2']}"
              + ("  [title]" if b["title_fight"] else ""))
    print(f"\nWrote {out}")
    print("Review the names (Wikipedia spellings can differ from ufcstats), "
          "optionally add decimal odds, then run:")
    print(f"  uv run python -m octagon predict --card {out}")


def raise_missing_date():
    raise SystemExit("--date YYYY-MM-DD is required when --event is given")


def cmd_predict(args: argparse.Namespace, cfg: dict) -> None:
    """Predict an upcoming card described by a YAML file."""
    import joblib

    from octagon.db.schema import connect
    from octagon.predict import predict_card

    artifact_path = resolve_path("artifacts/gbm.joblib")
    if not artifact_path.exists():
        raise SystemExit("No artifacts/gbm.joblib — run `octagon train` first.")
    card_path = Path(args.card)
    if not card_path.exists():
        raise SystemExit(f"Card file not found: {card_path} "
                         "(see cards/example_card.yaml for the format)")

    conn = connect(resolve_path(cfg["data"]["db_path"]))
    md = predict_card(conn, card_path, joblib.load(artifact_path), cfg)
    out = resolve_path("reports") / f"predict_{card_path.stem}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(md)
    print(f"\nWrote {out}")


def cmd_backtest(args: argparse.Namespace, cfg: dict) -> None:
    """Paper-trading simulation over the priced validation era."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd

    from octagon.betting.backtest import DISCLAIMER, equity_curve, run_backtest, summarize

    preds_path = resolve_path("reports/predictions_valid.parquet")
    if not preds_path.exists():
        raise SystemExit("No predictions found — run `octagon evaluate` first.")
    preds = pd.read_parquet(preds_path)
    if "p_blend" not in preds.columns:
        raise SystemExit("Predictions lack the blend — run `octagon train`, then `octagon evaluate`.")

    kelly_fraction = cfg["betting"]["kelly_fraction"]
    lines = [
        "# Paper-trading backtest — validation era (2022-2023)",
        "",
        f"**{DISCLAIMER}**",
        "",
        "Model: LR+GBM blend, walk-forward (each fight predicted by a model "
        "trained only on earlier fights). Odds: betmma best-available closing "
        "lines — a REAL bettor at one book gets worse prices than this. "
        "True CLV is not computable without opening odds; 'edge vs close' "
        "is the model's disagreement with the closing line, not captured value.",
        "",
        "| staking | edge >= | bets | staked | P&L (u) | ROI | 95% CI | hit rate | max DD (u) | avg odds |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    curves = {}
    for staking in ["flat", "kelly"]:
        for threshold in [0.02, 0.05, 0.08]:
            bets = run_backtest(preds, "p_blend", staking, threshold,
                                kelly_fraction=kelly_fraction)
            s = summarize(bets, seed=cfg["seed"])
            if s["n_bets"] == 0:
                lines.append(f"| {staking} | {threshold:.2f} | 0 | - | - | - | - | - | - | - |")
                continue
            lo, hi = s["roi_ci95"]
            lines.append(
                f"| {staking} | {threshold:.2f} | {s['n_bets']} | {s['total_staked']:.0f} "
                f"| {s['total_pnl_units']:+.1f} | {s['roi']:+.1%} | [{lo:+.1%}, {hi:+.1%}] "
                f"| {s['hit_rate']:.1%} | {s['max_drawdown_units']:.1f} | {s['avg_odds']:.2f} |")
            if staking == "flat":
                curves[f"flat, edge>={threshold:.2f}"] = equity_curve(bets)

    fig, ax = plt.subplots(figsize=(10, 5))
    for name, (dates, equity) in curves.items():
        ax.plot(pd.to_datetime(dates), equity, label=name)
    ax.axhline(0, color="k", linewidth=1)
    ax.set_ylabel("cumulative P&L (units, flat 1u stakes)")
    ax.set_title("Paper-trading equity curves — SIMULATION, not advice")
    ax.legend()
    fig.tight_layout()
    reports_dir = resolve_path("reports")
    fig.savefig(reports_dir / "backtest_equity.png", dpi=120)

    lines += [
        "",
        "![equity curves](backtest_equity.png)",
        "",
        "## How to read this",
        "- A 95% CI containing 0 means the result is indistinguishable from luck.",
        "- The M5 error analysis showed the market wins ~61% of disagreements "
        "with this model, so losses here are the expected outcome, not a bug.",
        "- Higher edge thresholds bet less often on bigger disagreements — "
        "which are exactly the fights where the model is most likely wrong.",
    ]
    out = reports_dir / "backtest_valid.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:20]))
    print(f"\nWrote {out} and reports/backtest_equity.png")


def cmd_explain(args: argparse.Namespace, cfg: dict) -> None:
    """SHAP explanations from the trained GBM artifact."""
    import joblib
    import pandas as pd

    from octagon.eval import explain
    from octagon.models import calibration, gbm

    artifact_path = resolve_path("artifacts/gbm.joblib")
    if not artifact_path.exists():
        raise SystemExit("No artifacts/gbm.joblib — run `octagon train` first.")
    artifact = joblib.load(artifact_path)
    df = pd.read_parquet(resolve_path(cfg["data"]["processed_dir"]) / "features.parquet")
    reports_dir = resolve_path("reports")
    reports_dir.mkdir(exist_ok=True)

    if args.fight_id is None:
        # Global view over the validation era (fights the final model never saw).
        valid = df[(df["date"] > cfg["splits"]["train_end"])
                   & (df["date"] <= cfg["splits"]["valid_end"])]
        shap_model = artifact.get("shap_model", artifact["model"])
        raw_flag = artifact.get("include_raw", False)
        importance = explain.global_importance(shap_model, valid, raw_flag)
        out = reports_dir / "shap_summary.png"
        explain.summary_plot(shap_model, valid, out, raw_flag)
        print(f"Global SHAP importance on {len(valid)} validation fights "
              f"(mean |log-odds contribution|):\n")
        for name, value in importance.head(15).items():
            print(f"  {value:.4f}  {name}")
        print(f"\nWrote {out}")
        return

    contributions = explain.explain_fight(
        artifact.get("shap_model", artifact["model"]), df, args.fight_id,
        artifact.get("include_raw", False))
    row = df[df["fight_id"] == args.fight_id]
    p_raw = gbm.predict_sym(artifact["model"], row,
                            include_raw=artifact.get("include_raw", False))
    p_cal = calibration.apply(artifact["iso"], p_raw)[0]
    print(explain.render_fight_text(df, args.fight_id, contributions, p_cal))
    out = reports_dir / f"shap_fight_{args.fight_id}.png"
    explain.waterfall_plot(contributions, out)
    print(f"\nWrote {out}")


def cmd_audit(args: argparse.Namespace, cfg: dict) -> None:
    import pandas as pd

    from octagon.db.schema import connect
    from octagon.eval.audit import run_audit

    conn = connect(resolve_path(cfg["data"]["db_path"]))
    df = pd.read_parquet(resolve_path(cfg["data"]["processed_dir"]) / "features.parquet")
    checks = run_audit(conn, df,
                       train_end=cfg["splits"]["train_end"],
                       valid_end=cfg["splits"]["valid_end"])
    failed = 0
    for name, passed, detail in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}\n         {detail}")
        failed += not passed
    if failed:
        raise SystemExit(f"\n{failed} audit check(s) FAILED — do not trust any model "
                         "trained on this feature table until this is resolved.")
    print(f"\nAll {len(checks)} leakage audit checks passed.")


def cmd_scrape_events(args: argparse.Namespace, cfg: dict) -> None:
    """Fetch the events index (+ the N most recent event pages) into the cache.

    M1 scope: prove fetch/cache/parse work end to end. Merging scraped fights
    into the DB (deduplicating against bootstrap rows) is an M2 task.
    """
    from octagon.scraping.fetch import BotChallengeError, fetch
    from octagon.scraping.ufcstats import COMPLETED_EVENTS_URL, parse_event_page, parse_events_index

    cache_dir = resolve_path(cfg["data"]["html_cache_dir"])
    rate = cfg["scraping"]["rate_limit_seconds"]

    try:
        html = fetch(COMPLETED_EVENTS_URL, cache_dir, rate, force=args.refresh)
    except BotChallengeError as exc:
        raise SystemExit(
            f"{exc}\nufcstats.com is behind an anti-bot wall; we don't bypass those.\n"
            "Data refresh path: the Greco1899/scrape_ufc_stats CSVs (see README)."
        )
    events = parse_events_index(html)
    if not events:
        raise SystemExit("Fetched the events index but parsed 0 events — "
                         "the page markup may have changed; inspect the cached HTML.")
    print(f"Events index: {len(events)} completed events "
          f"({events[-1]['date']} -> {events[0]['date']})")

    for event in events[: args.limit]:
        page = fetch(event["url"], cache_dir, rate)
        fights = parse_event_page(page)
        print(f"  {event['date']}  {event['name']}: {len(fights)} fights parsed")


def main() -> None:
    parser = argparse.ArgumentParser(prog="octagon", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db", help="create the SQLite schema").set_defaults(func=cmd_init_db)

    p = sub.add_parser("build-db", help="rebuild data/ufc.db from the raw CSV sources")
    p.set_defaults(func=cmd_build_db)

    p = sub.add_parser("refresh-data",
                       help="re-download Greco CSVs, rebuild DB + features, re-audit")
    p.set_defaults(func=cmd_refresh_data)

    p = sub.add_parser("scrape-events", help="fetch ufcstats events into the HTML cache")
    p.add_argument("--limit", type=int, default=3, help="event pages to fetch (default 3)")
    p.add_argument("--refresh", action="store_true", help="re-download the events index")
    p.set_defaults(func=cmd_scrape_events)

    p = sub.add_parser("build-features",
                       help="build the point-in-time feature table (parquet)")
    p.set_defaults(func=cmd_build_features)

    p = sub.add_parser("audit", help="run the data leakage audit (PRD section 6)")
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("evaluate", help="baselines + models metrics report")
    p.add_argument("--split", choices=["valid", "test"], default="valid",
                   help="which era to score (default: valid; test is the final holdout)")
    p.set_defaults(func=cmd_evaluate)

    p = sub.add_parser("train", help="tune + calibrate the GBM, save artifact")
    p.add_argument("--trials", type=int, default=40, help="Optuna trials (default 40)")
    p.set_defaults(func=cmd_train)

    p = sub.add_parser("explain", help="SHAP: global summary, or one fight")
    p.add_argument("--fight-id", type=int, default=None,
                   help="explain a single fight (default: global summary)")
    p.set_defaults(func=cmd_explain)

    p = sub.add_parser("backtest", help="paper-trading simulation (educational)")
    p.set_defaults(func=cmd_backtest)

    p = sub.add_parser("fetch-card",
                       help="build a card YAML for the next UFC event (Wikipedia)")
    p.add_argument("--event", help="Wikipedia page title (default: next event)")
    p.add_argument("--date", help="ISO date, required with --event")
    p.add_argument("--out", help="output YAML path (default: cards/<event>.yaml)")
    p.set_defaults(func=cmd_fetch_card)

    p = sub.add_parser("predict", help="predict an upcoming card from a YAML file")
    p.add_argument("--card", required=True,
                   help="path to a card YAML (see cards/example_card.yaml)")
    p.set_defaults(func=cmd_predict)

    args = parser.parse_args()
    args.func(args, load_config())


if __name__ == "__main__":
    main()
