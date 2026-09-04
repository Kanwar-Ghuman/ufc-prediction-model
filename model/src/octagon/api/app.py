"""Read-only FastAPI over files the CLI already wrote."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from octagon.api import findings

SPLIT_HELP = "Split to read: 'valid' (2022-2023) or 'test' (2024+)."


def create_app(allow_origins: list[str] | None = None) -> FastAPI:
    app = FastAPI(
        title="Octagon API",
        version="0.1.0",
        description="Read-only evaluation results and card predictions.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins or ["http://localhost:3000",
                                        "http://127.0.0.1:3000"],
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    def _check_split(split: str) -> str:
        if split not in findings.SPLITS:
            raise HTTPException(404, f"Unknown split '{split}'. {SPLIT_HELP}")
        return split

    @app.get("/api/health", tags=["meta"])
    def health() -> dict:
        return {"status": "ok", "trained": findings.artifact() is not None}

    @app.get("/api/overview", tags=["findings"])
    def overview() -> dict:
        """Dataset size, split boundaries and what tuning chose."""
        return findings.overview()

    @app.get("/api/metrics/{split}", tags=["findings"])
    def metrics(split: str) -> dict:
        """Log loss, Brier, accuracy, AUC and ECE per model, plus baselines."""
        result = findings.split_metrics(_check_split(split))
        if not result["available"]:
            raise HTTPException(
                404, f"No predictions for '{split}'. Run `octagon evaluate "
                     f"--split {split}` first.")
        return result

    @app.get("/api/calibration/{split}", tags=["findings"])
    def calibration(split: str, bins: int = 10, min_count: int = 20) -> dict:
        """Reliability curve: predicted probability vs. observed win rate."""
        result = findings.calibration(_check_split(split), n_bins=bins,
                                      min_count=min_count)
        if not result["available"]:
            raise HTTPException(404, f"No predictions for '{split}'.")
        return result

    @app.get("/api/cards", tags=["cards"])
    def cards() -> list[dict]:
        """Every card with frozen predictions, newest first."""
        return findings.list_cards()

    @app.get("/api/next-card", tags=["cards"])
    def next_card() -> dict:
        """The card the homepage leads with: the next one, else the last one."""
        slug = findings.next_card_slug()
        result = findings.card_detail(slug) if slug else None
        if result is None:
            raise HTTPException(
                404, "No card predictions yet. Run `octagon fetch-card` then "
                     "`octagon predict --card cards/<file>.yaml`.")
        result["scorecard"] = findings.card_scorecard(slug)
        return result

    @app.get("/api/portraits/{file_name}", tags=["cards"])
    def portrait(file_name: str) -> FileResponse:
        """A fighter portrait from the local media cache.

        Served from disk rather than hotlinked from ufc.com: the page then
        works offline and doesn't put a request on someone else's CDN every
        time somebody scrolls a card.
        """
        path = findings.portrait_path(file_name)
        if path is None:
            raise HTTPException(404, f"No portrait '{file_name}'. Run "
                                     "`octagon fetch-media --card <yaml>`.")
        return FileResponse(path, headers={"Cache-Control": "public, max-age=86400"})

    @app.get("/api/cards/{slug}", tags=["cards"])
    def card(slug: str) -> dict:
        """Frozen predictions for one card: win, method and round grids."""
        result = findings.card_detail(slug)
        if result is None:
            raise HTTPException(404, f"No frozen predictions for card '{slug}'.")
        return result

    @app.get("/api/cards/{slug}/scorecard", tags=["cards"])
    def scorecard(slug: str) -> dict:
        """How that card actually went, graded against the frozen numbers."""
        result = findings.card_scorecard(slug)
        if result is None:
            raise HTTPException(
                404, f"No results on record for card '{slug}' yet — the source "
                     "CSVs lag a live event by a day or two.")
        return result

    return app


app = create_app()
