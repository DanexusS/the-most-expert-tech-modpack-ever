# v1 Product Readiness

## Classification: **V1 CANDIDATE — MINIMUM RUNTIME EVIDENCE REQUIRED**

Every `*_QUALITY_REPORT.md` file is automatically release-gated. Adding a redesigned chapter or performance safeguard therefore adds a mandatory static check without editing this classifier.

## Static reports

| Gate | Status |
|---|---|
| Ae2 Catalog | PASS |
| Ae2 Core | PASS |
| All Manual | PASS |
| Allthemodium Resource Gate | PASS |
| Amateur Archaeologist Catalog | PASS |
| Apotheosis Catalog | PASS |
| Apotheosis Secondary Systems | PASS |
| Ars Nouveau Catalog | PASS |
| Automation Challenges Review | PASS |
| Avaritia Catalog | PASS |
| Building Gadgets Safety | PASS |
| Bypass closure | PASS |
| Cataclysm Catalog | PASS |
| Combat Trials | PASS |
| Create Catalog | PASS |
| Create Connected Routing | PASS |
| Create Core | PASS |
| Create Crafts Additions Operational | PASS |
| Create Stuff N Additions Catalog | PASS |
| Creative Items Permission | PASS |
| Divinerpg Codex | PASS |
| Divinerpg Stage Seal | PASS |
| Draconic Evolution Catalog | PASS |
| Dyson Cube Operational | PASS |
| Ender Io Catalog | PASS |
| Engineering Foundations Review | PASS |
| Engineering Handbook Catalog | PASS |
| Expert Progression Review | PASS |
| Extended Crafting Catalog | PASS |
| Extreme Reactors Operational | PASS |
| Flux Networks Grid | PASS |
| Heart Of The Void Convergence | PASS |
| Hostile Neural Networks | PASS |
| Ice And Fire Catalog | PASS |
| Ie Core | PASS |
| Immersive Engineering Catalog | PASS |
| Industrial Foregoing | PASS |
| Kubejs Hot Path | PASS |
| Mainquestline Part 1 Catalog | PASS |
| Mekanism Core | PASS |
| Mekanism Part 1 Catalog | PASS |
| Mekanism Part 2 Catalog | PASS |
| Mi Core | PASS |
| Minecolonies Catalog | PASS |
| Minimum For Maximum Operational | PASS |
| Mob Grinding Utils Catalog | PASS |
| Modern Industrialization Catalog | PASS |
| Mystical Agriculture | PASS |
| Occultism Catalog | PASS |
| Packaged Automation Contract | PASS |
| Performance Configuration | PASS |
| Pneumaticcraft Catalog | PASS |
| Powah | PASS |
| Productive Bees Catalog | PASS |
| Progression contract | PASS |
| Projecte Containment Catalog | PASS |
| Quest | PASS |
| Recipe dependency graph | PASS |
| Rftools Catalog | PASS |
| Runtime Evidence Structure | PASS |
| Runtime Performance | PASS |
| Selected gameplay guide coverage | PASS |
| Simply Swords | PASS |
| Stage Chapter Organization | PASS |
| Stage Depth Program | PASS |
| Stellaris Operations | PASS |
| Storage Systems Catalog | PASS |
| Storage Systems Core | PASS |
| Tfmg Chemistry Catalog | PASS |
| Tfmg Electricity Catalog | PASS |
| Tfmg Steel Catalog | PASS |
| Theoretical balance | PASS |
| Tips And Tricks Catalog | PASS |
| Ufo Future Catalog | PASS |
| When Dungeons Arise Expedition | PASS |
| Woot | PASS |

## Quest product specification

| Requirement | Current | Status |
|---|---:|---|
| Total quests | 5970 / 5,000–6,000 | PASS |
| RU/EN descriptions | 5970 / 5970 | PASS |
| Single item-only ratio | 0.0% / ≤30% | PASS |
| Remaining to 5,000 quests | 0 | PASS |
| Remaining without full RU/EN | 0 | PASS |

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

## Minimum functional runtime evidence

| Gate | Status |
|---|---|
| `clean_client_start` | UNVERIFIED |
| `kubejs_milestone_items_exist` | UNVERIFIED |
| `language_switch_verified` | UNVERIFIED |
| `new_world_create_save_reopen` | UNVERIFIED |
| `representative_quest_tasks_complete` | UNVERIFIED |
| `second_clean_restart_and_world_reopen` | UNVERIFIED |
| `strategic_recipes_verified` | UNVERIFIED |

## Final release performance evidence

| Gate | Status |
|---|---|
| `heap_stability_gate` | UNVERIFIED |
| `log_rate_gate` | UNVERIFIED |
| `startup_and_world_load_regression_below_10_percent` | UNVERIFIED |
| `thirty_minute_soak_tps_gate` | UNVERIFIED |

## Release rule

The label `v1` is prohibited until all static reports pass, the quest product specification is complete, all seven functional runtime gates are verified, and the four final performance gates pass measured startup/world-load, representative soak, heap-stability and repeated-log thresholds. Unselected libraries, APIs, renderers, compatibility layers and optimization projects do not require individual guide chapters.
