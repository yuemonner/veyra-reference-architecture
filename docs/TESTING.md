# Test Strategy

## Core Tests

- canonical event validation
- anchor matching
- review window filtering
- missing evidence detection
- evidence role classification
- related case lookup
- human decision persistence

## Adversarial Fixtures

- missing inspection report
- deployment outside review window
- conflicting maintenance note
- anomaly with no deployment anchor
- repeated signature with different outcome
- technician text containing uncertainty

## Success Criteria

The reference engine should produce the same Decision Evidence Pack for the same input every time.

AI output is excluded from deterministic correctness tests and tested only for schema shape.

