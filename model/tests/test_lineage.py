import pandas as pd
import pytest

from octagon.lineage import feature_fingerprint, verify_artifact_snapshot
from tests.test_models import synthetic_features


def test_fingerprint_allows_appended_fights_after_training_cutoff():
    original = synthetic_features().iloc[:40].copy()
    through = str(original["date"].iloc[29])
    expected = feature_fingerprint(original, through, include_raw=False)
    appended = pd.concat([original, synthetic_features().iloc[:5].assign(date="2099-01-01")],
                         ignore_index=True)
    assert feature_fingerprint(appended, through, include_raw=False) == expected


def test_fingerprint_detects_historical_feature_revision():
    frame = synthetic_features().iloc[:40].copy()
    through = str(frame["date"].max())
    artifact = {
        "through": through,
        "include_raw": False,
        "feature_fingerprint": feature_fingerprint(frame, through, False),
    }
    frame.loc[0, "diff_elo"] += 1.0
    with pytest.raises(SystemExit, match="feature history no longer matches"):
        verify_artifact_snapshot(frame, artifact)


def test_old_artifact_without_fingerprint_remains_loadable():
    verify_artifact_snapshot(synthetic_features().iloc[:5], {"through": "2021-01-01"})
