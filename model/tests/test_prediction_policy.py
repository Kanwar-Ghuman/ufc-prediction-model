"""End-to-end policy regression: market/context cannot alter skill mode."""

import numpy as np
import pandas as pd
import yaml

from octagon import predict
from octagon.features import regional
from octagon.models import calibration
from octagon.scraping import context
from tests.test_finish_round import _finish_features
from tests.test_gbm import FAST_PARAMS


def test_skill_mode_ignores_odds_rankings_and_sentiment(tmp_path, monkeypatch):
    history = _finish_features(60)
    upcoming = history.iloc[-1:].copy()
    upcoming["label"] = np.nan
    upcoming["date"] = "2020-04-01"
    upcoming["fight_id"] = -1
    frame = pd.concat([history, upcoming], ignore_index=True)
    monkeypatch.setattr(predict, "load_bouts", lambda conn: [])
    monkeypatch.setattr(predict, "load_tott", lambda conn: {})
    monkeypatch.setattr(regional, "load_regional", lambda conn: {})
    monkeypatch.setattr(predict, "build_feature_rows", lambda *a, **kw: frame.to_dict("records"))

    def forbidden(*args, **kwargs):
        raise AssertionError("Skill-only mode must not call a market or context adjuster")

    monkeypatch.setattr(predict, "apply_market_layer", forbidden)
    monkeypatch.setattr(predict, "apply_ranking_nudge", forbidden)
    monkeypatch.setattr(context, "soft_adjust_p_f1", forbidden)
    monkeypatch.setattr(context, "load_context", lambda path: {"fighters": {"sentiment": 1}})
    artifact = {"seed": 42, "params": FAST_PARAMS, "weight_lr": 0.5,
                "iso": calibration.fit_isotonic(np.array([0, 1]), np.array([0., 1.]))}
    cfg = {"seed": 42, "prediction": {"mode": "skill_only", "call_all": True}}
    path = tmp_path / "card.yaml"
    path.write_text(yaml.safe_dump({"date": "2020-04-01", "fights": [{
        "fighter1": "F0", "fighter2": "F1", "ranking": [1, 100]}]}))
    frame.loc[60, ["f1_odds", "f2_odds"]] = [1.1, 9.0]
    first = predict.card_predictions(None, path, artifact, cfg)
    frame.loc[60, ["f1_odds", "f2_odds"]] = [9.0, 1.1]
    second = predict.card_predictions(None, path, artifact, cfg)
    np.testing.assert_allclose(first.win_prob, second.win_prob, atol=1e-12)
    np.testing.assert_allclose(first.win_prob, first.skill_prob, atol=1e-12)
    assert first.market_prob[0] != second.market_prob[0]
    assert first.call_all and first.prediction_mode == "skill_only"
    frozen = predict.predictions_frame(first)
    assert frozen.call_all.all()
    assert frozen.prediction_mode.eq("skill_only").all()
    assert {"p_lr", "p_gbm"} <= set(frozen.columns)


def test_verified_tarin_profile_alias_recovers_age_without_overwriting():
    import sqlite3
    from octagon.features.build import load_tott

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE fighters(uid, name, height_cm, reach_cm, stance, dob)")
    conn.execute("CREATE TABLE fights(fighter1, fighter2)")
    conn.execute("INSERT INTO fighters VALUES ('tarin', 'Regina Malpica Rivera', NULL, NULL, NULL, '2004-10-19')")
    assert load_tott(conn)["Regina Tarin"]["dob"] == "2004-10-19"
    conn.execute("INSERT INTO fighters VALUES ('tarin2', 'Regina Tarin', 170, 168, 'Orthodox', '2004-10-19')")
    assert load_tott(conn)["Regina Tarin"]["height_cm"] == 170
    conn.close()


def test_profiles_resolve_punctuation_and_verified_silva_uid():
    import sqlite3
    from octagon.features.build import load_tott

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE fighters(uid, name, height_cm, reach_cm, stance, dob)")
    conn.execute("CREATE TABLE fights(fighter1, fighter2)")
    conn.executemany("INSERT INTO fighters VALUES (?, ?, NULL, NULL, NULL, ?)", [
        ("waldo", "Waldo Cortes-Acosta", "1991-10-03"),
        ("older-silva", "Jean Silva", "1977-10-08"),
        ("52ef95b5860fb28c", "Jean Silva", "1996-12-27"),
    ])
    conn.execute("INSERT INTO fights VALUES ('Waldo Cortes Acosta', 'Jean Silva')")
    profiles = load_tott(conn)
    assert profiles["Waldo Cortes Acosta"]["dob"] == "1991-10-03"
    assert profiles["Jean Silva"]["dob"] == "1996-12-27"
    conn.close()
