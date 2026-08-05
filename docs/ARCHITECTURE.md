# Architecture

## System Context

```mermaid
flowchart LR
  A["Robots / industrial equipment"] --> T["Telemetry systems"]
  B["Deployment tools"] --> D["GitHub / CI / release records"]
  C["Field operations"] --> M["Maintenance / ticket systems"]
  H["Humans"] --> O["Operator notes / interventions"]

  T --> V["Veyra read-only connectors"]
  D --> V
  M --> V
  O --> V

  V --> E["Canonical event model"]
  E --> R["Relationship engine"]
  R --> C1["Operational case"]
  C1 --> P["Decision Evidence Pack"]
  P --> U["Human readiness review"]
```

Veyra runs beside existing operational systems. It does not sit in the machine control path.

## Component Architecture

```mermaid
flowchart TB
  subgraph Sources
    S1["machine events JSON / webhook"]
    S2["deployment records"]
    S3["maintenance records"]
    S4["operator intervention notes"]
  end

  subgraph Core
    N["Normalizer"]
    V["Schema validator"]
    R["Relationship resolver"]
    B["Case builder"]
    M["Missing evidence detector"]
    A["Bounded AI summarizer"]
  end

  subgraph Storage
    DB["PostgreSQL"]
    OBJ["Object storage"]
  end

  subgraph Product
    API["Review API"]
    UI["Readiness review workspace"]
  end

  Sources --> N --> V --> DB
  DB --> R --> B --> M --> A --> API --> UI
  DB --> OBJ
```

## Return-To-Service Sequence

```mermaid
sequenceDiagram
  participant Machine
  participant Telemetry
  participant Deployments
  participant Maintenance
  participant Veyra
  participant Engineer

  Machine->>Telemetry: anomaly emitted
  Deployments->>Veyra: release rev_218 record
  Maintenance->>Veyra: recent bearing replacement
  Telemetry->>Veyra: normalized runtime anomaly
  Engineer->>Veyra: request readiness review
  Veyra->>Veyra: reconstruct case by asset, time window and anchors
  Veyra->>Veyra: classify evidence for / against / missing
  Veyra->>Engineer: Decision Evidence Pack
  Engineer->>Veyra: approve limited test / hold / request evidence
  Veyra->>Veyra: store decision and outcome as memory
```

## Design Principles

1. Read-only by default.
2. Explicit relationships before inferred relationships.
3. Missing evidence is first-class.
4. AI summarizes only selected evidence.
5. Human decisions and outcomes become operational memory.
6. Storage stays boring until graph queries prove necessary.

