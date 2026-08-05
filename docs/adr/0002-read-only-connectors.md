# ADR 0002: Read-Only Connectors

## Status

Accepted

## Decision

All connectors are read-only in v0.1.

## Rationale

The product is an evidence layer, not a control plane. Read-only connectors reduce operational risk and make design partner pilots easier to approve.

## Consequences

- No deployment execution
- No robot control
- No ticket mutation by default
- Human review remains accountable

