# v1 Readiness

## Classification: **STATIC CANDIDATE — PRODUCT INCOMPLETE**

Core static checks pass, but the 5–6k quest target, guide coverage, progression contract or bypass closure is incomplete.

## Foundation evidence

| Gate | Status |
|---|---|
| Theoretical balance | PASS |
| Core quest quality | PASS |
| Create core route | PASS |
| Immersive Engineering core route | PASS |
| Modern Industrialization core route | PASS |
| Applied Energistics 2 core route | PASS |

## Product evidence

| Gate | Status |
|---|---|
| Progression contract | PASS |
| Bypass closure | IN PROGRESS / FAIL |
| All-mod guide coverage | IN PROGRESS / FAIL |
| Quest volume 5,000–6,000 | IN PROGRESS (2958) |
| Item-only ratio ≤30% | IN PROGRESS (75.6%) |

## Minimum runtime evidence

| Gate | Status |
|---|---|
| `clean_client_start` | UNVERIFIED |
| `kubejs_milestone_items_exist` | UNVERIFIED |
| `language_switch_verified` | UNVERIFIED |
| `new_world_create_save_reopen` | UNVERIFIED |
| `representative_quest_tasks_complete` | UNVERIFIED |
| `second_clean_restart_and_world_reopen` | UNVERIFIED |
| `strategic_recipes_verified` | UNVERIFIED |

## Optional measurements

These improve tuning but do not block v1 under the current product specification.

| Gate | Status |
|---|---|
| `scaled_namespaces_sampled` | UNVERIFIED |
| `combat_samples_within_targets` | UNVERIFIED |
| `startup_and_world_load_regression_below_10_percent` | UNVERIFIED |
| `thirty_minute_soak_tps_gate` | UNVERIFIED |
| `heap_stability_gate` | UNVERIFIED |
| `log_rate_gate` | UNVERIFIED |

## Rule

The label `v1` is prohibited until the product specification, progression contract, bypass audit, all-mod guide coverage and minimum runtime gates pass together.
