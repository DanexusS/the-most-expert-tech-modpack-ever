# v1 Product Readiness

## Classification: **DEVELOPMENT — STATIC GATES INCOMPLETE**

## Static reports

| Gate | Status |
|---|---|
| Theoretical balance | PASS |
| Quest quality | PASS |
| Curated manuals | PASS |
| Progression contract | PASS |
| Recipe dependency graph | PASS |
| Bypass closure | PASS |
| Selected gameplay guide coverage | IN PROGRESS / FAIL |
| Create route | PASS |
| Immersive Engineering route | PASS |
| Modern Industrialization route | PASS |
| Applied Energistics 2 route | PASS |
| Mekanism route | PASS |

## Quest product specification

| Requirement | Current | Status |
|---|---:|---|
| Total quests | 3318 / 5,000–6,000 | IN PROGRESS |
| RU/EN descriptions | 632 / 3318 | IN PROGRESS |
| Single item-only ratio | 67.4% / ≤30% | IN PROGRESS |

## Selected gameplay guide specification

| Metric | Current |
|---|---:|
| Manifest inventory projects | 501 |
| Tracked gameplay/progression projects | 13 |
| Projects not requiring individual guides | 488 |
| Tracked guides awaiting review | 13 |
| Reviewed tracked guides | 0 |
| Complete tracked guides | 0 |
| Coverage status | IN PROGRESS |

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

## Release rule

The label `v1` is prohibited until all static reports pass, the quest book contains 5,000–6,000 fully bilingual quests, item-only quests are at most 30%, every selected meaningful gameplay/progression mod has a reviewed guide, and the minimum runtime evidence is verified. Unselected libraries, APIs, renderers, compatibility layers and optimization projects do not require individual guide chapters.
