from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI

from packages.veyra_core.ingestion import load_case
from packages.veyra_core.reconstruction import build_decision_pack
from packages.veyra_core.serialization import to_jsonable

app = FastAPI(
    title="Veyra Reference API",
    description="Read-only operational evidence reconstruction for readiness reviews.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/reviews/sample")
def sample_review() -> dict:
    seed_path = Path(__file__).resolve().parents[2] / "seeds" / "aceco_like_case.json"
    events, request = load_case(seed_path)
    pack = build_decision_pack(events, request)
    return to_jsonable(pack)


@app.post("/reviews/from-seed")
def review_from_seed(payload: dict) -> dict:
    events = []
    from packages.veyra_core.ingestion import canonical_event_from_dict, review_request_from_dict

    for item in payload["events"]:
        events.append(canonical_event_from_dict(item))
    request = review_request_from_dict(payload["review_request"])
    return to_jsonable(build_decision_pack(events, request))

