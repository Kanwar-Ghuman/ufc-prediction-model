"""Project config from config.yaml."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def project_root() -> Path:
    """Repo root = two levels above this file (src/octagon/config.py)."""
    return Path(__file__).resolve().parents[2]


def load_dotenv(path: Path | None = None) -> None:
    """Load KEY=VALUE pairs from model/.env into os.environ (setdefault).

    Secrets (YouTube, Odds API, …) live here and are gitignored. Existing
    environment variables always win — so CI / shells can override.
    """
    path = path or (project_root() / ".env")
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def env_secret(cfg: dict, key_name: str) -> str | None:
    """Read an API key named in config (e.g. scraping.youtube_api_key_env)."""
    load_dotenv()
    env_var = (cfg.get("scraping") or {}).get(key_name)
    if not env_var:
        return None
    value = os.environ.get(env_var, "").strip()
    return value or None


def load_config(path: Path | None = None) -> dict[str, Any]:
    """Read config.yaml (from the repo root by default) into a dict."""
    load_dotenv()
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
