"""Style archetypes and clash features from L5 rates."""


def style_scores(snap: dict) -> dict[str, float]:
    """0-1 archetype scores from a fighter_snapshot-like dict."""
    def g(key: str, default: float = 0.0) -> float:
        value = snap.get(key)
        return float(value) if value is not None else default

    striker = min(1.0, 0.35 * g("slpm_l5") + 0.35 * g("head_share_l5")
                  + 0.30 * g("kd15_l5") * 3)
    wrestler = min(1.0, 0.45 * g("td15_l5") + 0.35 * g("td_acc_l5")
                   + 0.20 * g("ctrl_pct_l5"))
    grappler = min(1.0, 0.40 * g("ground_share_l5") + 0.40 * g("sub15_l5") * 2
                   + 0.20 * g("sub_win_rate"))
    pressure = min(1.0, 0.40 * g("clinch_share_l5") + 0.35 * g("ctrl_pct_l5")
                   + 0.25 * min(1.0, g("slpm_l5") / 6.0))
    return {"striker": striker, "wrestler": wrestler,
            "grappler": grappler, "pressure": pressure}


def _primary(scores: dict[str, float]) -> str:
    return max(scores, key=scores.get)


def style_matchup(f1: dict, f2: dict) -> dict[str, float | None]:
    """How styles clash — antisymmetric diffs for the feature table."""
    def observed(snap: dict, key: str, default: float) -> float:
        value = snap.get(key)
        return default if value is None else float(value)

    a, b = style_scores(f1), style_scores(f2)
    wrestle_vs_strike = (
        a["wrestler"] * (1.0 - observed(f2, "td_def_l5", 0.5))
        - b["wrestler"] * (1.0 - observed(f1, "td_def_l5", 0.5)))
    strike_vs_wrestle = (
        a["striker"] * max(0.0, 1.0 - b["wrestler"])
        - b["striker"] * max(0.0, 1.0 - a["wrestler"]))
    grapple_vs_strike = (
        a["grappler"] * observed(f2, "ground_absorbed_share_l5", 0.3)
        - b["grappler"] * observed(f1, "ground_absorbed_share_l5", 0.3))

    def minus(x, y):
        return (x - y) if x is not None and y is not None else None

    r1, r2 = f1.get("reach_cm"), f2.get("reach_cm")
    reach_striker = (
        ((r1 - r2) * a["striker"] - (r2 - r1) * b["striker"])
        if r1 is not None and r2 is not None else None)

    age1, age2 = f1.get("age"), f2.get("age")
    # Wrestling ages worse than striking; the older wrestler is the one hurt.
    age_wrestle = (
        -(age1 * a["wrestler"] - age2 * b["wrestler"])
        if age1 is not None and age2 is not None else None)

    am, bm = f1.get("avg_fight_min"), f2.get("avg_fight_min")
    af, bf = f1.get("finish_involvement"), f2.get("finish_involvement")
    cardio_fade = (
        (af * (bm / 15.0) - bf * (am / 15.0))
        if None not in (am, bm, af, bf) else None)

    s1, s2 = f1.get("southpaw"), f2.get("southpaw")
    southpaw_striker = (
        (s1 - s2) * (a["striker"] + b["striker"]) / 2.0
        if s1 is not None and s2 is not None else None)

    rec1 = f1.get(f"vs_{_primary(b)}_win_pct")
    rec2 = f2.get(f"vs_{_primary(a)}_win_pct")
    style_record = minus(rec1, rec2)

    return {
        "style_wrestle_strike": wrestle_vs_strike,
        "style_strike_wrestle": strike_vs_wrestle,
        "style_grapple_strike": grapple_vs_strike,
        "style_pressure_gap": a["pressure"] - b["pressure"],
        "style_striker_gap": a["striker"] - b["striker"],
        "style_wrestler_gap": a["wrestler"] - b["wrestler"],
        "style_grappler_gap": a["grappler"] - b["grappler"],
        "style_reach_striker": reach_striker,
        "style_age_wrestle": age_wrestle,
        "style_cardio_fade": cardio_fade,
        "style_southpaw_striker": southpaw_striker,
        "style_record": style_record,
    }
