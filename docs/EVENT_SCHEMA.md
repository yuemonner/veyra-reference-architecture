# Canonical Operational Event Schema

The canonical event model borrows the discipline of observability events, but it is organized around operational decisions rather than raw monitoring.

```json
{
  "event_id": "evt_runtime_001",
  "source": {
    "system": "telemetry",
    "record_id": "telemetry-84392",
    "ingested_at": "2026-08-05T09:13:00Z"
  },
  "event_type": "runtime_anomaly",
  "occurred_at": "2026-08-05T09:12:41Z",
  "asset": {
    "asset_id": "line-a-conveyor",
    "asset_type": "industrial_equipment",
    "subsystem": "drive_assembly"
  },
  "anchors": {
    "deployment_id": "rev_218",
    "ticket_id": "OPS-418",
    "mission_id": "sorting_shift_line_a"
  },
  "severity": "review",
  "summary": "Torque variance exceeded expected envelope.",
  "measurements": {
    "torque_variance_pct": 18.4,
    "belt_speed_mps": 0.92,
    "drive_temperature_c": 71
  },
  "evidence_role": "against_proceeding",
  "raw_ref": "s3://customer-bucket/raw/telemetry-84392.json"
}
```

## Required Fields

- `event_id`
- `source.system`
- `source.record_id`
- `event_type`
- `occurred_at`
- `asset.asset_id`
- `summary`

## Event Types

```text
runtime_anomaly
deployment
maintenance
inspection
operator_intervention
test_result
mission_outcome
payment_settlement
readiness_update
human_decision
outcome
```

## Evidence Roles

```text
for_proceeding
against_proceeding
missing
context
unknown
```

