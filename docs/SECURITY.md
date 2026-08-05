# Security Model

## Trust Boundary

Veyra should be deployed as close as possible to the customer's operational environment.

Default deployment:

- read-only connectors
- customer-owned raw data
- Veyra stores structured metadata and references
- no machine control path
- no write access to deployment systems

## Primary Threats

| Threat | Control |
| --- | --- |
| Raw data exposure | Store references, not raw continuous streams |
| Connector over-permissioning | Read-only scoped tokens |
| Hallucinated decision rationale | AI output must cite included events |
| Hidden causality claims | Use correlation language unless causality is explicit |
| Tampered source records | Source hash and ingestion timestamp |
| Insider misuse | Review audit log and owner attribution |
| Cross-customer leakage | Tenant isolation and no shared raw records |

## Non-Control Path

The reference architecture never executes operational actions. It supports human review.

