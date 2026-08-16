# Runtime Performance Quality Report

**PASS**

This gate validates final-release performance evidence against the pack policy. UNVERIFIED rows are structurally valid but continue to block the final v1 label through the readiness classifier.

| Gate | Release target | Evidence status |
|---|---|---|
| Startup and world-load regression | ≤10.0% / ≤10.0% | UNVERIFIED |
| 30-minute representative soak | TPS p05 ≥19.0; MSPT p95 ≤50.0 | UNVERIFIED |
| Post-GC heap stability | growth ≤10.0% | UNVERIFIED |
| Repeated-log rate | ≤30 lines/min | UNVERIFIED |

## Aggregate

- Release performance gates recorded: **4 / 4**
- Release performance gates verified: **0 / 4**
- Invalid claims or threshold failures: **0**
