# v1 Product Readiness

## Classification: **STATIC FOUNDATION PASS — PRODUCT INCOMPLETE**

Every `*_QUALITY_REPORT.md` file is automatically release-gated. Adding a new redesigned chapter therefore adds a mandatory v1 check without editing this classifier.

## Static reports

| Gate | Status |
|---|---|
| Ae2 Core | PASS |
| All Manual | PASS |
| Bypass closure | PASS |
| Create Core | PASS |
| Ie Core | PASS |
| Mekanism Core | PASS |
| Mi Core | PASS |
| Powah | PASS |
| Progression contract | PASS |
| Quest | PASS |
| Recipe dependency graph | PASS |
| Selected gameplay guide coverage | PASS |
| Simply Swords | PASS |
| Storage Systems Core | PASS |
| Theoretical balance | PASS |

## Quest product specification

| Requirement | Current | Status |
|---|---:|---|
| Total quests | 3318 / 5,000–6,000 | IN PROGRESS |
| RU/EN descriptions | 769 / 3318 | IN PROGRESS |
| Single item-only ratio | 63.3% / ≤30% | IN PROGRESS |

## Selected gameplay guide specification

| Metric | Current |
|---|---:|
| Manifest inventory projects | 501 |
| Tracked gameplay/progression projects | 13 |
| Projects not requiring individual guides | 488 |
| Tracked guides awaiting review | 0 |
| Reviewed tracked guides | 13 |
| Complete tracked guides | 0 |
| Coverage status | PASS |

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

The label `v1` is prohibited until every static and chapter quality report passes, the quest book contains 5,000–6,000 fully bilingual quests, item-only quests are at most 30%, every selected meaningful gameplay/progression mod has a reviewed guide, and the minimum runtime evidence is verified. Unselected libraries, APIs, renderers, compatibility layers and optimization projects do not require individual guide chapters.
