# Performance Configuration Quality Report

**PASS**

This static safeguard verifies low-risk configuration, bounded questbook growth and script budgets before runtime profiling. It does not replace TPS, heap and restart measurements.

| Check | Current | Status |
|---|---|---|
| FTB Quests detection delay | `40.0` | PASS |
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
| Workflow optimization quests | `90/90` | PASS |
| Depth optimization quests | `180/180` | PASS |
| Mandatory quests per stage | `min=121, max=121` | PASS |
| Total questbook size | `5640/6000` | PASS |
| KubeJS JavaScript files | `205/220` | PASS |
| Event subscriptions | `197/220` | PASS |
| Explicit console calls | `30/35` | PASS |

## Runtime measurements still required

- startup and world-open time;
- 30-minute server TPS/MSPT soak with representative factories;
- heap growth and post-GC stability;
- entity and block-entity counts in loaded production chunks;
- repeated-log rate during normal operation;
- clean restart and world reopen after the soak.
