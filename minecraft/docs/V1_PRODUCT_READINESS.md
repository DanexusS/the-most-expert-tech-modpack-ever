# v1 Product Readiness

## Classification: **STATIC FOUNDATION PASS — PRODUCT INCOMPLETE**

Every `*_QUALITY_REPORT.md` file is automatically release-gated. Adding a redesigned chapter therefore adds a mandatory v1 check without editing this classifier.

## Static reports

| Gate | Status |
|---|---|
| Ae2 Catalog | PASS |
| Ae2 Core | PASS |
| All Manual | PASS |
| Allthemodium Resource Gate | PASS |
| Amateur Archaeologist Catalog | PASS |
| Apotheosis Catalog | PASS |
| Ars Nouveau Catalog | PASS |
| Avaritia Catalog | PASS |
| Bypass closure | PASS |
| Cataclysm Catalog | PASS |
| Create Catalog | PASS |
| Create Connected Routing | PASS |
| Create Core | PASS |
| Create Crafts Additions Operational | PASS |
| Create Stuff N Additions Catalog | PASS |
| Draconic Evolution Catalog | PASS |
| Ender Io Catalog | PASS |
| Engineering Handbook Catalog | PASS |
| Extended Crafting Catalog | PASS |
| Extreme Reactors Operational | PASS |
| Hostile Neural Networks | PASS |
| Ice And Fire Catalog | PASS |
| Ie Core | PASS |
| Immersive Engineering Catalog | PASS |
| Industrial Foregoing | PASS |
| Mainquestline Part 1 Catalog | PASS |
| Mekanism Core | PASS |
| Mekanism Part 1 Catalog | PASS |
| Mekanism Part 2 Catalog | PASS |
| Mi Core | PASS |
| Minecolonies Catalog | PASS |
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
| Selected gameplay guide coverage | PASS |
| Simply Swords | PASS |
| Stage Chapter Organization | PASS |
| Stage Depth Program | PASS |
| Storage Systems Catalog | PASS |
| Storage Systems Core | PASS |
| Tfmg Chemistry Catalog | PASS |
| Tfmg Electricity Catalog | PASS |
| Tfmg Steel Catalog | PASS |
| Theoretical balance | PASS |
| Tips And Tricks Catalog | PASS |
| Ufo Future Catalog | PASS |
| Woot | PASS |

## Quest product specification

| Requirement | Current | Status |
|---|---:|---|
| Total quests | 5970 / 5,000–6,000 | PASS |
| RU/EN descriptions | 5625 / 5970 | IN PROGRESS |
| Single item-only ratio | 3.5% / ≤30% | PASS |
| Remaining to 5,000 quests | 0 | PASS |
| Remaining without full RU/EN | 345 | IN PROGRESS |

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
