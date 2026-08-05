from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import AssetRef, CanonicalEvent, EvidenceRole, ReviewRequest, SourceRef
from .schema import validate_event_shape


def parse_dt(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def canonical_event_from_dict(payload: dict[str, Any]) -> CanonicalEvent:
    errors = validate_event_shape(payload)
    if errors:
        raise ValueError(f"invalid event {payload.get('event_id', '<unknown>')}: {', '.join(errors)}")
    source = payload["source"]
    asset = payload["asset"]
    return CanonicalEvent(
        event_id=payload["event_id"],
        source=SourceRef(
            system=source["system"],
            record_id=source["record_id"],
            ingested_at=parse_dt(source.get("ingested_at")) if source.get("ingested_at") else None,
        ),
        event_type=payload["event_type"],
        occurred_at=parse_dt(payload["occurred_at"]),
        asset=AssetRef(
            asset_id=asset["asset_id"],
            asset_type=asset.get("asset_type", "unknown"),
            subsystem=asset.get("subsystem"),
        ),
        summary=payload["summary"],
        anchors=payload.get("anchors", {}),
        severity=payload.get("severity", "info"),
        evidence_role=EvidenceRole(payload.get("evidence_role", EvidenceRole.UNKNOWN.value)),
        measurements=payload.get("measurements", {}),
        raw_ref=payload.get("raw_ref"),
    )


def review_request_from_dict(payload: dict[str, Any]) -> ReviewRequest:
    return ReviewRequest(
        review_id=payload["review_id"],
        question=payload["question"],
        asset_id=payload["asset_id"],
        requested_at=parse_dt(payload["requested_at"]),
        window_start=parse_dt(payload["window_start"]),
        window_end=parse_dt(payload["window_end"]),
        required_evidence=payload.get("required_evidence", []),
        anchors=payload.get("anchors", {}),
    )


def load_case(path: str | Path) -> tuple[list[CanonicalEvent], ReviewRequest]:
    data = json.loads(Path(path).read_text())
    events = [canonical_event_from_dict(item) for item in data["events"]]
    request = review_request_from_dict(data["review_request"])
    return events, request

