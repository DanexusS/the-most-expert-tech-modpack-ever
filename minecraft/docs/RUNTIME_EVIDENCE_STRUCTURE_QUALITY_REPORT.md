# Runtime Evidence Structure Quality Report

**PASS**

This gate validates the evidence schema and rejects unsupported runtime claims. A structurally valid file may still contain only UNVERIFIED gates; that is expected until an actual client or server run is recorded.

| Gate | Verified | Coverage | Evidence refs | Structure |
|---|---|---:|---:|---|
| `clean_client_start` | no | 0/1 | 0 | PASS |
| `combat_samples_within_targets` | no | 0/4 | 0 | PASS |
| `heap_stability_gate` | no | 0/2 | 0 | PASS |
| `kubejs_milestone_items_exist` | no | 0/18 | 0 | PASS |
| `language_switch_verified` | no | 0/2 | 0 | PASS |
| `log_rate_gate` | no | 0/1 | 0 | PASS |
| `new_world_create_save_reopen` | no | 0/1 | 0 | PASS |
| `representative_quest_tasks_complete` | no | 0/3 | 0 | PASS |
| `scaled_namespaces_sampled` | no | 0/4 | 0 | PASS |
| `second_clean_restart_and_world_reopen` | no | 0/1 | 0 | PASS |
| `startup_and_world_load_regression_below_10_percent` | no | 0/1 | 0 | PASS |
| `strategic_recipes_verified` | no | 0/18 | 0 | PASS |
| `thirty_minute_soak_tps_gate` | no | 0/30 | 0 | PASS |

## Aggregate

- Gates recorded: **13**
- Mandatory gates recorded: **7 / 7**
- Mandatory gates verified: **0 / 7**
- Structural or claim failures: **0**
