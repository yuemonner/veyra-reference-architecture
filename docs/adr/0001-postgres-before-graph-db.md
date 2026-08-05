# ADR 0001: PostgreSQL Before Graph Database

## Status

Accepted

## Decision

Use PostgreSQL-style relational tables and JSONB fields for the first reference implementation. Model graph relationships explicitly in a `relationships` table.

## Rationale

The first technical risk is context reconstruction, not graph database performance. A relational model is easier to inspect, test, deploy and explain to technical collaborators.

## Consequences

- Faster reference implementation
- Clear migration path to graph storage later
- Relationship semantics remain explicit
- Advanced graph traversal is out of scope for v0.1

