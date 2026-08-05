# Review API

## Create Review

```http
POST /reviews
Content-Type: application/json
```

```json
{
  "decision": "Should Line A Conveyor return to service after rev_218?",
  "asset_id": "line-a-conveyor",
  "review_window": {
    "from": "2026-08-05T08:30:00Z",
    "to": "2026-08-05T10:00:00Z"
  },
  "required_evidence": [
    "runtime_telemetry",
    "deployment_record",
    "maintenance_record",
    "inspection_record"
  ]
}
```

## Response

```json
{
  "review_id": "revw_001",
  "status": "not_ready",
  "confidence": "medium",
  "evidence_for": [],
  "evidence_against": [],
  "missing_evidence": [],
  "related_cases": [],
  "suggested_next_action": "Run inspection before return-to-service.",
  "citations": []
}
```

## Human Decision

```http
POST /reviews/{review_id}/decision
```

```json
{
  "decision": "ready_for_limited_test",
  "rationale": "Inspection completed and variance cleared.",
  "owner": "reliability-engineer"
}
```

