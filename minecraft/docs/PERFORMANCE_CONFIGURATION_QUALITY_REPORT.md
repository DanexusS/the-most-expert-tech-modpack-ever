# Performance Configuration Quality Report

**PASS**

This is a static safeguard report. It verifies low-risk configuration and script practices before runtime profiling; it does not replace the required TPS, heap and restart measurements.

| Check | Current | Status |
|---|---|---|
| FTB Quests detection delay | `20.0` | PASS |
| FTB Quests grid scale | `0.5` | PASS |
| FTB Quests verify_on_load | `False` | PASS |
| FTB Quests drop_loot_crates | `False` | PASS |
| CoroUtil useLoggingLog | `False` | PASS |
| CoroUtil useLoggingDebug | `False` | PASS |
| CoroUtil useLoggingError | `True` | PASS |
| Combat scaling — Profile cache | `present` | PASS |
| Combat scaling — Stable modifier IDs | `present` | PASS |
| Combat scaling — Registry guard | `present` | PASS |
| .gitignore /command_history.txt | `present` | PASS |
| .gitignore /ESM/ | `present` | PASS |
| .gitignore /logs/ | `present` | PASS |
| .gitignore /crash-reports/ | `present` | PASS |
| .gitignore /local/ | `present` | PASS |
| .gitignore /saves/ | `present` | PASS |
| Runtime path command_history.txt | `absent` | PASS |
| Runtime path ESM/ | `absent` | PASS |
| Runtime path logs/ | `absent` | PASS |
| Runtime path crash-reports/ | `absent` | PASS |
| Runtime path local/ | `absent` | PASS |
| Runtime path saves/ | `absent` | PASS |
| Measured optimization quests | `60/60` | PASS |

## Script inventory

- KubeJS JavaScript files: **204**
- Event subscriptions found: **196**
- Explicit console calls found: **28**
- Required measured optimization quests: **60**

## Runtime measurements still required

- startup and world-open time;
- 30-minute server TPS/MSPT soak with representative factories;
- heap growth and post-GC stability;
- entity and block-entity counts in loaded production chunks;
- repeated-log rate during normal operation;
- clean restart and world reopen after the soak.
