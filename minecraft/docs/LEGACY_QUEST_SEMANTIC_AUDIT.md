# Legacy Quest Semantic Audit

This report analyses non-generated legacy chapters for obsolete catalogue structure, missing operational guidance, malformed quest objects, empty tasks, rewards, excessive item counts and duplicate descriptions. It is a remediation queue, not proof that every surviving quest is fun in play.

## Summary

- Legacy chapters analysed: **57**
- Legacy quests and malformed objects analysed: **3324**
- Malformed quest objects: **0**
- Chapters requiring rewrite: **6**
- Chapters requiring review: **5**
- Empty chapters requiring a keep/remove decision: **0**
- Duplicate description groups: **63**

## Chapter remediation queue

| Chapter | Objects | Risk score | High risk | Malformed | Item-only | Missing guidance | Rewards | Classification |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `when_dungeons_arise` | 31 | 248 | 31 | 0 | 0 | 31 | 31 | REWRITE_REQUIRED |
| `minimum_for_maximummfm` | 25 | 240 | 24 | 0 | 18 | 25 | 24 | REWRITE_REQUIRED |
| `apotheosis_2` | 22 | 213 | 22 | 0 | 18 | 22 | 22 | REWRITE_REQUIRED |
| `divinerpg` | 20 | 140 | 16 | 0 | 0 | 16 | 20 | REWRITE_REQUIRED |
| `Gadgets` | 15 | 136 | 15 | 0 | 8 | 15 | 15 | REWRITE_REQUIRED |
| `flux_networks` | 10 | 101 | 10 | 0 | 10 | 10 | 10 | REWRITE_REQUIRED |
| `divinerpg_codex` | 89 | 431 | 36 | 0 | 31 | 50 | 9 | REVIEW_REQUIRED |
| `automation_challenges` | 72 | 350 | 33 | 0 | 36 | 33 | 12 | REVIEW_REQUIRED |
| `combat_trials` | 108 | 343 | 9 | 0 | 0 | 60 | 7 | REVIEW_REQUIRED |
| `engineering_foundations_guide` | 16 | 34 | 0 | 0 | 10 | 0 | 1 | REVIEW_REQUIRED |
| `expert_progression` | 15 | 34 | 0 | 0 | 0 | 0 | 11 | REVIEW_REQUIRED |
| `productive_bees` | 204 | 167 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `simply_swords_2` | 52 | 52 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `engineering_handbook` | 96 | 50 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `amateur_archaeologist` | 43 | 43 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `tips_and_tricks` | 32 | 32 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `ars_nouveau` | 94 | 18 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `applied_energistics_2` | 135 | 13 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `heart_of_the_void` | 26 | 13 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `Modern Industrialization` | 105 | 11 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `minecolonies` | 65 | 11 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `apotheosis` | 43 | 10 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `mekanism_part_2` | 102 | 9 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `ufo_future` | 65 | 8 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
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
| `creative_items` | 19 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `ender_io` | 67 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `industrial_foregoing` | 74 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
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
| `hostile_neural_networks` | 51 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `immersive_engineering` | 46 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `other_storage_systems` | 104 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `package_mod` | 27 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `powah` | 74 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `woot` | 58 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |

## Highest-risk individual quests and objects

| Chapter | Quest/Object ID | Score | Flags |
|---|---|---:|---|
| `Gadgets` | `2A2E1C7C34C9A4AA` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `Gadgets` | `2B29DDBADF11195E` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `Gadgets` | `40F1315207ADEB80` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `Gadgets` | `4F00BE972EFE7FBE` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `Gadgets` | `5855D8361A2C6623` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `Gadgets` | `6DDA86A3B4C0ACC1` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `Gadgets` | `6EEAF4D9F3BF6414` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `apotheosis_2` | `7C3968AF39557751` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `automation_challenges` | `51DFDEAC05124ED6` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `automation_challenges` | `69529ABB3E76DC19` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `automation_challenges` | `6A569C5B3D593EEA` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg` | `1086BBFA8FB8AA80` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `2685BED005B7CE85` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `3A0EB475437F4169` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `flux_networks` | `439C6C61A5263D31` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `minimum_for_maximummfm` | `1F87798C942B893F` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `minimum_for_maximummfm` | `232F28C7B5A9F4DD` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `Gadgets` | `68107A111627BD77` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `00588B2FDB99874D` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `0D6D45DBA64E612D` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `0E02CE4469FCA4C9` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `0F89BFD4A3F63A48` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `167E1474644C9908` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `186593EBCE3FE8D8` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `1AD87CB3226ED224` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `30EB438C66324213` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `340BCA3B946CB5CF` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `3E2A411FF5B4B0E7` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `40096ED0B04C3EC5` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `42D7C8CD8E6F5CD7` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `4D07B0A4A2E77CDA` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `528111F34C96380C` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `5A0DDE4265A2A8B4` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `6A497B063CF32A5C` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `6F71FD826C29C31A` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `7A9AE63998BB41FF` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `automation_challenges` | `67E156F68E42F5A6` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `automation_challenges` | `6ADF14F9875DBF13` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `combat_trials` | `21B514DDD0177F9A` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `combat_trials` | `24B11C0EBB23F75A` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `combat_trials` | `28FE5C4EF2C287CA` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `combat_trials` | `6D2A03C2AF9E2BE3` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `combat_trials` | `6D743B95130671AE` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `divinerpg_codex` | `0EA838E3062775AB` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `divinerpg_codex` | `14F3BA3DDC607758` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `flux_networks` | `1651E315517369BD` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `flux_networks` | `1B60491EDE73447B` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `flux_networks` | `1C214DD51C58BE4D` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `flux_networks` | `486457F40D2A1D29` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `flux_networks` | `4CC229C23E5AC155` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `flux_networks` | `6886DFF567919753` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `flux_networks` | `6E9B60CCAE55E387` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `flux_networks` | `7AA18B409FB698D2` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `flux_networks` | `7AEAF2E101B5D652` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `0DCFCBCFB363C921` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `0E9F3510205FE096` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `119CB7DC2A3AD8B6` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `132F18F4FDF51813` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `1A904F5D656789D6` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `203600FDAB9A148A` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `305C778D5538E46F` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `30CB226DAA54E6EA` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `38D14675BA200B0E` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `45D20904723662F8` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `4ED870EA84A78E94` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `506E8A76D87A55B9` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `520FCDA696573BAA` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `556488ADD6C1576A` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `62C126C97A94CBE5` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `692AAD0BCCBCB657` | 10 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `6C74E5CD21611F2E` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `75777D3DF45D6651` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `7947F1F725619F60` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `minimum_for_maximummfm` | `7A9DF67899445C99` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `apotheosis_2` | `310969B8FE0A94DE` | 8 | NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
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
| `divinerpg` | `0C0E383A6F559E02` | 8 | NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg` | `1672F109D4C0E42B` | 8 | NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg` | `29C46C9F9B029F54` | 8 | NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg` | `4A53992AD167FA2E` | 8 | NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg` | `4EFA24AD3B679AFE` | 8 | NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg` | `594DF7E33BAEFF34` | 8 | NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg` | `59B95F948B6B9578` | 8 | NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
