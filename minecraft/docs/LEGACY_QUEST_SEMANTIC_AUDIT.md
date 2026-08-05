# Legacy Quest Semantic Audit

This report analyses non-generated legacy chapters for obsolete catalogue structure, missing operational guidance, malformed quest objects, empty tasks, rewards, excessive item counts and duplicate descriptions. It is a remediation queue, not proof that every surviving quest is fun in play.

## Summary

- Legacy chapters analysed: **57**
- Legacy quests and malformed objects analysed: **3324**
- Malformed quest objects: **0**
- Chapters requiring rewrite: **13**
- Chapters requiring review: **5**
- Empty chapters requiring a keep/remove decision: **0**
- Duplicate description groups: **64**

## Chapter remediation queue

| Chapter | Objects | Risk score | High risk | Malformed | Item-only | Missing guidance | Rewards | Classification |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `create_crafts__additions` | 27 | 273 | 27 | 0 | 27 | 27 | 27 | REWRITE_REQUIRED |
| `dl_stellaris` | 29 | 270 | 29 | 0 | 21 | 29 | 29 | REWRITE_REQUIRED |
| `heart_of_the_void` | 26 | 270 | 26 | 0 | 26 | 26 | 25 | REWRITE_REQUIRED |
| `package_mod` | 27 | 265 | 27 | 0 | 25 | 27 | 27 | REWRITE_REQUIRED |
| `create_connected` | 26 | 258 | 26 | 0 | 25 | 26 | 25 | REWRITE_REQUIRED |
| `when_dungeons_arise` | 31 | 248 | 31 | 0 | 0 | 31 | 31 | REWRITE_REQUIRED |
| `minimum_for_maximummfm` | 25 | 240 | 24 | 0 | 18 | 25 | 24 | REWRITE_REQUIRED |
| `apotheosis_2` | 22 | 213 | 22 | 0 | 18 | 22 | 22 | REWRITE_REQUIRED |
| `creative_items` | 19 | 192 | 19 | 0 | 18 | 19 | 19 | REWRITE_REQUIRED |
| `divinerpg` | 20 | 140 | 16 | 0 | 0 | 16 | 20 | REWRITE_REQUIRED |
| `Gadgets` | 15 | 136 | 15 | 0 | 8 | 15 | 15 | REWRITE_REQUIRED |
| `dyson_cube_project` | 12 | 115 | 12 | 0 | 11 | 12 | 11 | REWRITE_REQUIRED |
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
| `draconic_evolution` | 111 | 3 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `mekanism_part_1` | 78 | 3 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `projecte` | 29 | 3 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `rftools` | 81 | 3 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `ender_io` | 67 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `industrial_foregoing` | 74 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `occultism` | 34 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `tfmg_electricity` | 44 | 2 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `allthemodium` | 31 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `cataclysm` | 79 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `create_stuff_n_additions` | 36 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `extended_crafting` | 43 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `extreme_reactors` | 30 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `hostile_neural_networks` | 51 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `immersive_engineering` | 46 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `other_storage_systems` | 104 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `powah` | 74 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `woot` | 58 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |

## Highest-risk individual quests and objects

| Chapter | Quest/Object ID | Score | Flags |
|---|---|---:|---|
| `create_connected` | `2ADDA74C73C08DB2` | 12 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, DUPLICATE_DESCRIPTION |
| `create_connected` | `30D6BFA1A3B6B205` | 12 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, DUPLICATE_DESCRIPTION |
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
| `create_crafts__additions` | `43E4EE94BB396A7C` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `create_crafts__additions` | `4FCCEB8B6A6AA643` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `create_crafts__additions` | `7B6E46D719CFB570` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `creative_items` | `087144F5252E5FF5` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `creative_items` | `7C31E7904E8DD77C` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg` | `1086BBFA8FB8AA80` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `2685BED005B7CE85` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `divinerpg_codex` | `3A0EB475437F4169` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `dl_stellaris` | `128AF83728356D60` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `flux_networks` | `439C6C61A5263D31` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `heart_of_the_void` | `030E814BD568A97F` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `heart_of_the_void` | `0EF4982211D87606` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `heart_of_the_void` | `152ED772C41FD63A` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `heart_of_the_void` | `24B5D2FC32F32D0D` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `heart_of_the_void` | `30C7F7955B71A428` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `heart_of_the_void` | `3D82F9E035BE899E` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `heart_of_the_void` | `41612BEABB489AB2` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `heart_of_the_void` | `571695B26E4EA017` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `heart_of_the_void` | `5E5995EFD532081C` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `heart_of_the_void` | `66CB86E03D47D430` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `heart_of_the_void` | `6EEEAA630E7F7E91` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `heart_of_the_void` | `79D9840E56157DCB` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `minimum_for_maximummfm` | `1F87798C942B893F` | 11 | CHECKMARK_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `minimum_for_maximummfm` | `232F28C7B5A9F4DD` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
| `package_mod` | `54832AACF9BC8B54` | 11 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD, ROOT_OR_ORPHAN |
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
| `create_connected` | `00654F576522DDCA` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `1A61ABEC34369F47` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `1D197B1919452187` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `1E01AC22D5903AD1` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `261ABBDC3DABD8B3` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `2AF85A5EE9A8CCBA` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `2F6B432512FA2A65` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `35F24F6E403AADA1` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `4A47E558AD90EB64` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `4EC20D5D0EEC1DF7` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `4EC499B88FBFA01C` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `54589F10802DFE16` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `63B4B83F528E6AD6` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `63E8F78EEA3063F7` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `6832CFEAFA7922E8` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `69816C16E81355E8` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `6B7188472F6ED6AF` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `6B8966D7EA9BB5FB` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `6DE8ACA4F08C420E` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `6FE2FE40C2F60183` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `7AA7094E591A373B` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `7EB1BE897B2B8C1A` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_connected` | `7F5D32DA7E8D094F` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `00ACD837E30165B3` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `0354DB37FD2030EE` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `0488989FD7F5AF42` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `0834527ED1C0E83B` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `0B8148DAF5CC9DF1` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `0C8F501F6BDFFB92` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `113E1D3C37C63088` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `17709C4D6222244B` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `1F36CF5D11E08839` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `215D766150B54B17` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `22AC3C79141AB3FC` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `36760F31374EB61E` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
| `create_crafts__additions` | `39124F73B82400F4` | 10 | ITEM_ONLY, NO_OPERATIONAL_GUIDANCE, HAS_REWARD |
