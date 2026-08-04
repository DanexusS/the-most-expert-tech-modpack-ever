# v1 Readiness

## Classification: **STATIC CANDIDATE — NOT V1**

Static and theoretical gates pass, but runtime evidence is incomplete.

## Static and theoretical evidence

| Gate | Status |
|---|---|
| Theoretical balance | PASS |
| Quest quality | PASS |
| Create core route | PASS |
| Immersive Engineering core route | PASS |
| Modern Industrialization core route | PASS |

## Runtime evidence

| Gate | Status |
|---|---|
| `clean_client_start` | UNVERIFIED |
| `new_world_create_save_reopen` | UNVERIFIED |
| `kubejs_milestone_items_exist` | UNVERIFIED |
| `strategic_recipes_verified` | UNVERIFIED |
| `scaled_namespaces_sampled` | UNVERIFIED |
| `representative_quest_tasks_complete` | UNVERIFIED |
| `language_switch_verified` | UNVERIFIED |
| `combat_samples_within_targets` | UNVERIFIED |
| `startup_and_world_load_regression_below_10_percent` | UNVERIFIED |
| `thirty_minute_soak_tps_gate` | UNVERIFIED |
| `heap_stability_gate` | UNVERIFIED |
| `log_rate_gate` | UNVERIFIED |
| `second_clean_restart_and_world_reopen` | UNVERIFIED |

## Recorded measurements

| Measurement | Value |
|---|---:|
| `baseline_startup_seconds_median` | not measured |
| `candidate_startup_seconds_median` | not measured |
| `baseline_world_load_seconds_median` | not measured |
| `candidate_world_load_seconds_median` | not measured |
| `soak_tps_p05` | not measured |
| `heap_after_first_cycle_mib` | not measured |
| `heap_after_second_cycle_mib` | not measured |
| `maximum_repeated_log_lines_per_minute` | not measured |

## Rule

The label `v1` is prohibited while any runtime gate is unverified. Theoretical calculations may tune test targets but cannot set runtime evidence to verified.
