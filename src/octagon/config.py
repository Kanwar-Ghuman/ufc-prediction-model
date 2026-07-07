"""Load project configuration from config.yaml.

Why a single YAML file? So every experiment (splits, seeds, Elo K, betting
thresholds) is controlled from one visible place instead of constants
scattered through the code — that makes results reproducible and honest.
"""

from pathlib import Path
from typing import Any

import yaml


def project_root() -> Path:
    """Repo root = two levels above this file (src/octagon/config.py)."""
    return Path(__file__).resolve().parents[2]


def load_config(path: Path | None = None) -> dict[str, Any]:
    """Read config.yaml (from the repo root by default) into a dict."""
    if path is None:
        path = project_root() / "config.yaml"
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def resolve_path(relative: str) -> Path:
    """Turn a config-relative path like 'data/ufc.db' into an absolute one.

    Paths in config.yaml are relative to the repo root so the config stays
    portable across machines.
    """
    return project_root() / relative
