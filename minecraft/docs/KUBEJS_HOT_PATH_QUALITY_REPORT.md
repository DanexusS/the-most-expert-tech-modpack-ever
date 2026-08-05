# KubeJS Hot Path Quality Report

**PASS**

This static gate scans frequent KubeJS handlers and startup scripts. It rejects synchronous file I/O, full registry scans and console output in tick/spawn/hurt paths, and requires diagnostic startup writes to be explicitly enabled.

## Budgets

| Category | Current | Maximum | Status |
|---|---:|---:|---|
| tick subscriptions | 0 | 4 | PASS |
| spawn subscriptions | 1 | 4 | PASS |
| hurt subscriptions | 0 | 4 | PASS |
| Guarded startup file writers | 1 | diagnostic only | PASS |
| Unguarded startup file writers | 0 | 0 | PASS |
| Combat EntityType identity cache | present | required | PASS |

## High-frequency handlers

| File | Handler | Category | Status |
|---|---|---|---|
| `kubejs/server_scripts/combat_scaling.js` | `EntityEvents.spawned` | spawn | PASS |

## Aggregate

- High-frequency subscriptions: **1**
- Guarded startup file writers: **1**
- Unguarded startup file writers: **0**
- Failures: **0**
