from __future__ import annotations

from typing import Any


CANONICAL_EVENT_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Veyra Canonical Operational Event",
    "type": "object",
    "required": ["event_id", "source", "event_type", "occurred_at", "asset", "summary"],
    "properties": {
        "event_id": {"type": "string"},
        "source": {
            "type": "object",
            "required": ["system", "record_id"],
            "properties": {
                "system": {"type": "string"},
                "record_id": {"type": "string"},
                "ingested_at": {"type": "string", "format": "date-time"},
            },
        },
        "event_type": {"type": "string"},
        "occurred_at": {"type": "string", "format": "date-time"},
        "asset": {
            "type": "object",
            "required": ["asset_id"],
            "properties": {
                "asset_id": {"type": "string"},
                "asset_type": {"type": "string"},
                "subsystem": {"type": ["string", "null"]},
            },
        },
        "anchors": {"type": "object"},
        "severity": {"type": "string"},
        "summary": {"type": "string"},
        "measurements": {"type": "object"},
        "evidence_role": {
            "enum": ["for_proceeding", "against_proceeding", "missing", "context", "unknown"]
        },
        "raw_ref": {"type": ["string", "null"]},
    },
}


def validate_event_shape(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in CANONICAL_EVENT_SCHEMA["required"]:
        if field not in payload:
            errors.append(f"missing required field: {field}")
    source = payload.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
    else:
        for field in ("system", "record_id"):
            if field not in source:
                errors.append(f"source missing required field: {field}")
    asset = payload.get("asset")
    if not isinstance(asset, dict):
        errors.append("asset must be an object")
    elif "asset_id" not in asset:
        errors.append("asset missing required field: asset_id")
    return errors

