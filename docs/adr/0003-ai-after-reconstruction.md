# ADR 0003: AI After Reconstruction

## Status

Accepted

## Decision

AI receives only reconstructed case evidence, not unbounded raw enterprise data.

## Rationale

The value is evidence reconstruction. AI should summarize and explain bounded evidence, not search through raw operational systems or hallucinate missing context.

## Consequences

- Deterministic core remains testable
- Citations are required
- Missing evidence is preserved
- AI cannot execute operational actions

