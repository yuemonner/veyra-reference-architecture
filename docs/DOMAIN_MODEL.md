# Domain Model

## Core Entities

### Asset

A physical or logical system under operational review.

Examples:

- AMR-07
- Line A Conveyor
- Solar Node 017
- Robot Fleet North

### Source Record

An immutable record imported from an external system.

Examples:

- telemetry event
- deployment webhook
- maintenance ticket
- operator intervention note
- inspection report

### Canonical Event

A normalized event representing a meaningful operational change, checkpoint or outcome.

### Relationship

An explicit or suggested link between events, assets, deployments, tickets and reviews.

### Operational Case

A bounded reconstruction around one decision under review.

### Decision Evidence Pack

The product output. It summarizes:

- decision under review
- last validated state
- what changed
- evidence for proceeding
- evidence against proceeding
- missing evidence
- related prior cases
- readiness status
- suggested next action

### Human Decision

The action selected by an accountable person:

- ready
- ready for limited test
- hold
- rollback
- dispatch
- inspect
- request evidence

### Outcome

What happened after the decision. Outcomes are the beginning of operational memory.

## Relationship Types

```text
same_asset
same_subsystem
caused_by_explicit_reference
occurred_after
within_review_window
references_deployment
references_ticket
references_intervention
resolved_by
similar_signature
missing_required_evidence
```

## Confidence

Veyra separates relationship confidence from decision confidence.

```text
deterministic  explicit ID match
strong         asset + deployment + narrow time window
medium         asset + subsystem + event signature
weak           text similarity or broad time window
unknown        missing anchor
```

