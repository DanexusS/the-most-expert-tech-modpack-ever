# Legacy Quest Semantic Audit

This report analyses non-generated legacy chapters for obsolete catalogue structure, missing operational guidance, malformed quest objects, empty tasks, rewards, excessive item counts and duplicate descriptions. It is a remediation queue, not proof that every surviving quest is fun in play.

## Summary

- Legacy chapters analysed: **57**
- Legacy quests and malformed objects analysed: **3324**
- Malformed quest objects: **0**
- Chapters requiring rewrite: **0**
- Chapters requiring review: **6**
- Empty chapters requiring a keep/remove decision: **0**
- Duplicate description groups: **63**

## Chapter remediation queue

| Chapter | Objects | Risk score | High risk | Malformed | Item-only | Missing guidance | Rewards | Classification |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `divinerpg_codex` | 89 | 431 | 36 | 0 | 31 | 50 | 9 | REVIEW_REQUIRED |
| `automation_challenges` | 72 | 350 | 33 | 0 | 36 | 33 | 12 | REVIEW_REQUIRED |
| `combat_trials` | 108 | 343 | 9 | 0 | 0 | 60 | 7 | REVIEW_REQUIRED |
| `divinerpg` | 20 | 40 | 0 | 0 | 0 | 0 | 9 | REVIEW_REQUIRED |
| `engineering_foundations_guide` | 16 | 34 | 0 | 0 | 10 | 0 | 1 | REVIEW_REQUIRED |
| `expert_progression` | 15 | 34 | 0 | 0 | 0 | 0 | 11 | REVIEW_REQUIRED |
| `productive_bees` | 204 | 167 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `simply_swords_2` | 52 | 52 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `engineering_handbook` | 96 | 50 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `amateur_archaeologist` | 43 | 43 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `tips_and_tricks` | 32 | 32 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `when_dungeons_arise` | 31 | 31 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `ars_nouveau` | 94 | 18 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `applied_energistics_2` | 135 | 13 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `heart_of_the_void` | 26 | 13 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `Modern Industrialization` | 105 | 11 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `minecolonies` | 65 | 11 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `apotheosis` | 43 | 10 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `mekanism_part_2` | 102 | 9 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `ufo_future` | 65 | 8 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `Gadgets` | 15 | 7 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `mainquestline_part_1` | 74 | 7 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `pneumaticcraft` | 72 | 6 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `avaritia` | 75 | 5 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `ice_and_fire` | 88 | 5 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `mob_grinding` | 25 | 5 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `create` | 80 | 4 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `mystical_ag` | 141 | 4 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `tfmg_chemistry` | 35 | 4 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `tfmg_steel` | 39 | 4 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `create_crafts__additions` | 27 | 3 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `draconic_evolution` | 111 | 3 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `mekanism_part_1` | 78 | 3 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `projecte` | 29 | 3 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `rftools` | 81 | 3 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `apotheosis_2` | 22 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `creative_items` | 19 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `ender_io` | 67 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `industrial_foregoing` | 74 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `minimum_for_maximummfm` | 25 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `occultism` | 34 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `tfmg_electricity` | 44 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `allthemodium` | 31 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `cataclysm` | 79 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `create_connected` | 26 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `create_stuff_n_additions` | 36 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `dl_stellaris` | 29 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `dyson_cube_project` | 12 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `extended_crafting` | 43 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `extreme_reactors` | 30 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `flux_networks` | 10 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `hostile_neural_networks` | 51 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `immersive_engineering` | 46 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `other_storage_systems` | 104 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `package_mod` | 27 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `powah` | 74 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `woot` | 58 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |

## Highest-risk individual quests and objects

| Chapter | Quest/Object ID | Score | Flags |
|---|---|---:|---|
| `automation_challenges` | `51DFDEAC05124ED6` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `automation_challenges` | `69529ABB3E76DC19` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `automation_challenges` | `6A569C5B3D593EEA` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `2685BED005B7CE85` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `3A0EB475437F4169` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `automation_challenges` | `67E156F68E42F5A6` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `automation_challenges` | `6ADF14F9875DBF13` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `combat_trials` | `21B514DDD0177F9A` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `combat_trials` | `24B11C0EBB23F75A` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `combat_trials` | `28FE5C4EF2C287CA` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `combat_trials` | `6D2A03C2AF9E2BE3` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `combat_trials` | `6D743B95130671AE` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `divinerpg_codex` | `0EA838E3062775AB` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `divinerpg_codex` | `14F3BA3DDC607758` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `automation_challenges` | `116F7A57C35817E2` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `23E955FEEA77B312` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `53DC65EC2650F714` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `562CD705335D967C` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `5BDB48BA178720B1` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `5C7231CEC5177C96` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `5FB60258AA48A05F` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `61008A6AE19135D7` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `6FA491BD8659A13A` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `75245F0AF0A38625` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `7B7D6EC785C52176` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `7B7FE280AAC658C8` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `7B8C4499FFD8BB66` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `7BF5A7A538541CA5` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `combat_trials` | `01BDBF0EC1D48575` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `combat_trials` | `3690C0E169587826` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `combat_trials` | `65977110985192B3` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `combat_trials` | `7D676A0E2BDEEBC1` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `03C3D0E11A66121E` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `095DFBD0FC7BCAB9` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `22779650B288A2E7` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `25A6D01989407798` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `32D0D348540D5C09` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `3BB3721762FF799E` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `49FB62F58FD49B36` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `4ADDD5B2CBCBDFD9` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `51F940142726DDE9` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `53166EDE38132E5E` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `54D82E5A7F19F63E` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `6B449EE59BFDF1E4` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `778ADA651A07C2E9` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `781B29DA8F223B28` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `7991C47143A83D44` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `7B1592C870BEF347` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `7C25D3A05DCC3ED7` | 8 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `7E57B202158CDC14` | 8 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, ROOT_OR_ORPHAN |
| `automation_challenges` | `05833BA19A0C4441` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `0BBD1E65BFD11D57` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `1E0211C004E3DB08` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `3A0BF535867D9EF0` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `414BEEAF35C79C6C` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `51E179750AF9E0B6` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `5571B40704061357` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `5619B4AAA3C19DD2` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `57A3C95848A95B48` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `64E50825984A8C6B` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `6D7EAC3B8443B1A9` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `6E66934654A45A2E` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `72D97C73861B281E` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `75EDF3D53E9C19F4` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `09486B5A26C30CCE` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `1755262DEC041F4C` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `1B39848B5566E29B` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `1D969EC020DA4CAE` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `299857CAB7827052` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `2C9299F91E4D470A` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `2E8B6F014AAFA620` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `364938D6E7D2B21C` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `3F0B16D944884C9E` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `4B6048557F00AE5A` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `4E287D900820B4FD` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `58703D5D4A2D6256` | 7 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `5FD61F33E25B54E4` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `divinerpg_codex` | `6DBBB488515EC3A3` | 7 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE |
| `automation_challenges` | `0309031C02F40F48` | 6 | ITEM_ONLY, ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `1F95DE2B8AEAADB6` | 6 | ITEM_ONLY, ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `245F4D37B9D6BDEA` | 6 | ITEM_ONLY, ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `3F34DC9EE4EFF09E` | 6 | ITEM_ONLY, ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `603FEA2B63EBD29A` | 6 | CHECKMARK_ONLY, HAS_REWARD, ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `7739E5F65499CE9F` | 6 | ITEM_ONLY, ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `7FA8EB0C90B3F72B` | 6 | CHECKMARK_ONLY, HAS_REWARD, ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `divinerpg_codex` | `1A692A5E03C485B2` | 6 | CHECKMARK_ONLY, HAS_REWARD, ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `divinerpg_codex` | `1DCFEFBFB79866D9` | 6 | CHECKMARK_ONLY, HAS_REWARD, ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `divinerpg_codex` | `59FE01FC8C79654C` | 6 | CHECKMARK_ONLY, HAS_REWARD, ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `Modern Industrialization` | `1CC910880728D896` | 5 | EXCESSIVE_ITEM_COUNT |
| `Modern Industrialization` | `3761B64135EA94C0` | 5 | EXCESSIVE_ITEM_COUNT |
| `automation_challenges` | `0BEADBE8FAA1A907` | 5 | ITEM_ONLY, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `11076A09529A4BEA` | 5 | ITEM_ONLY, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `23B13127579104CF` | 5 | CHECKMARK_ONLY, HAS_REWARD, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `23E2F2528AB7A0BB` | 5 | ITEM_ONLY, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `25170E9E2A0EEF15` | 5 | ITEM_ONLY, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `3A3E58D0B6EA38BB` | 5 | ITEM_ONLY, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `3A9F6E8659F5B2D6` | 5 | CHECKMARK_ONLY, HAS_REWARD, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `3AC4E2186DC04ED6` | 5 | CHECKMARK_ONLY, HAS_REWARD, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `459266EB73384474` | 5 | CHECKMARK_ONLY, HAS_REWARD, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `473B9CFA8C6E18CC` | 5 | CHECKMARK_ONLY, HAS_REWARD, DUPLICATE_DESCRIPTION |
