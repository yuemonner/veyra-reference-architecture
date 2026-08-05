# Veyra Reference Architecture

Veyra is a reference architecture for reconstructing operational evidence behind high-consequence decisions in Physical AI and intelligent industrial systems.

This repository is intentionally not a polished SaaS demo. It is a founder-grade technical package: domain model, schemas, storage design, APIs, threat model, ADRs, seed data, tests and a runnable reference implementation.

## Core Question

When an autonomous or connected physical system behaves unexpectedly, teams need to answer:

> What changed, what happened, what evidence is missing, and is this system ready for what comes next?

Veyra turns fragmented operational history into a Decision Evidence Pack for workflows such as:

- deployment readiness
- robot incident review
- return-to-service review
- mission readiness
- operational review
- equipment financing readiness

## What This Reference Proves

1. Different source systems can map into a canonical operational event model.
2. Explicit identifiers and time windows can reconstruct a bounded operational case.
3. Missing and conflicting evidence can be represented directly rather than hidden.
4. Human interventions and outcomes can become part of long-term operational memory.
5. AI can summarize selected evidence without reading raw enterprise systems or taking action.

## What This Reference Does Not Claim

- It does not control machines.
- It does not replace fleet management, observability or robotics data tooling.
- It does not make autonomous decisions.
- It does not prove universal ontology across every robot or industrial asset.
- It does not claim production-grade OT security approval.

## Repository Map

```text
apps/
  api/                    FastAPI wrapper around the reference engine
  workspace/              Static workspace mock for technical walkthroughs
docs/
  ARCHITECTURE.md         System context, components and workflows
  DOMAIN_MODEL.md         Canonical entities and relationships
  EVENT_SCHEMA.md         Canonical operational event JSON schema
  API.md                  Review API contract
  STORAGE.md              PostgreSQL-first storage design
  AI_BOUNDARY.md          AI scope, prompt contract and failure modes
  SECURITY.md             Threat model and deployment controls
  NON_GOALS.md            Explicit boundaries
  TESTING.md              Test strategy and adversarial fixtures
  adr/                    Architecture Decision Records
packages/
  veyra_core/             Runnable reference engine
seeds/
  aceco_like_case.json    Synthetic connected equipment case
tests/
  test_reconstruction.py  Core workflow tests
```

## Quick Start

```bash
python -m packages.veyra_core.cli seeds/aceco_like_case.json
```

Run tests:

```bash
python -m pytest tests
```

Run API:

```bash
uvicorn apps.api.main:app --reload
```

Open the workspace mock:

```text
apps/workspace/index.html
```

## The Product Boundary

Veyra is a read-only evidence reconstruction layer.

```text
Operational systems
  telemetry, logs, deployments, tickets, maintenance records, operator notes
        |
        v
Canonical event model
        |
        v
Explicit relationship rules
        |
        v
Operational case reconstruction
        |
        v
Decision Evidence Pack
        |
        v
Human readiness review
```

The system outputs evidence. The customer owns the final decision.

