# Storage Model

PostgreSQL is the primary storage target. JSONB is used for source payloads and measurements. Graph structure is represented with ordinary relational tables until graph queries become a proven bottleneck.

## Tables

```sql
CREATE TABLE source_records (
  id TEXT PRIMARY KEY,
  source_system TEXT NOT NULL,
  source_record_id TEXT NOT NULL,
  ingested_at TIMESTAMPTZ NOT NULL,
  payload JSONB NOT NULL
);

CREATE TABLE canonical_events (
  id TEXT PRIMARY KEY,
  source_record_id TEXT REFERENCES source_records(id),
  event_type TEXT NOT NULL,
  occurred_at TIMESTAMPTZ NOT NULL,
  asset_id TEXT NOT NULL,
  asset_type TEXT,
  subsystem TEXT,
  severity TEXT,
  summary TEXT NOT NULL,
  anchors JSONB NOT NULL DEFAULT '{}',
  measurements JSONB NOT NULL DEFAULT '{}',
  evidence_role TEXT NOT NULL DEFAULT 'context'
);

CREATE TABLE relationships (
  id TEXT PRIMARY KEY,
  source_entity_type TEXT NOT NULL,
  source_entity_id TEXT NOT NULL,
  relation_type TEXT NOT NULL,
  target_entity_type TEXT NOT NULL,
  target_entity_id TEXT NOT NULL,
  evidence_source_id TEXT,
  confidence TEXT NOT NULL,
  review_status TEXT NOT NULL DEFAULT 'unreviewed'
);

CREATE TABLE reviews (
  id TEXT PRIMARY KEY,
  decision TEXT NOT NULL,
  asset_id TEXT NOT NULL,
  window_start TIMESTAMPTZ NOT NULL,
  window_end TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL,
  confidence TEXT NOT NULL,
  pack JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE human_decisions (
  id TEXT PRIMARY KEY,
  review_id TEXT REFERENCES reviews(id),
  decision TEXT NOT NULL,
  rationale TEXT,
  owner TEXT,
  decided_at TIMESTAMPTZ NOT NULL
);
```

