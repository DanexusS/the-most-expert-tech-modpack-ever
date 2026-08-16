# Legacy Quest Semantic Audit

This report analyses non-generated legacy chapters for obsolete catalogue structure, missing operational guidance, malformed quest objects, empty tasks, unauthorized rewards, excessive counts and duplicate descriptions. The nine progression-contract DivineRPG seal rewards are explicitly authorized and are not treated as reward risk.

## Summary

- Legacy chapters analysed: **57**
- Legacy quests and malformed objects analysed: **3324**
- Malformed quest objects: **0**
- Chapters requiring rewrite: **0**
- Chapters requiring review: **0**
- Authorized seal-reward quests: **9**
- Empty chapters requiring a keep/remove decision: **0**
- Duplicate description groups: **66**

## Chapter remediation queue

| Chapter | Objects | Risk score | High risk | Malformed | Item-only | Missing guidance | Unauthorized rewards | Classification |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `productive_bees` | 204 | 167 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `combat_trials` | 108 | 55 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `simply_swords_2` | 52 | 52 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `divinerpg_codex` | 89 | 51 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `engineering_handbook` | 96 | 50 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `amateur_archaeologist` | 43 | 43 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `tips_and_tricks` | 32 | 32 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `when_dungeons_arise` | 31 | 31 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `automation_challenges` | 72 | 29 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `ars_nouveau` | 94 | 18 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `applied_energistics_2` | 135 | 13 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `divinerpg` | 20 | 13 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
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
| `engineering_foundations_guide` | 16 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
| `expert_progression` | 15 | 1 | 0 | 0 | 0 | 0 | 0 | CURRENTLY_ACCEPTABLE |
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
| `Modern Industrialization` | `1CC910880728D896` | 5 | EXCESSIVE_ITEM_COUNT |
| `Modern Industrialization` | `3761B64135EA94C0` | 5 | EXCESSIVE_ITEM_COUNT |
| `mekanism_part_2` | `068728DE3B9B13C3` | 5 | EXCESSIVE_ITEM_COUNT |
| `pneumaticcraft` | `63F6F4EBCEB914B0` | 5 | EXCESSIVE_ITEM_COUNT |
| `ufo_future` | `689F61EF65826A33` | 5 | EXCESSIVE_ITEM_COUNT |
| `ars_nouveau` | `0FF49F7DD4D172CF` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `245F4D37B9D6BDEA` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `51DFDEAC05124ED6` | 3 | CHECKMARK_ONLY, ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `automation_challenges` | `53DC65EC2650F714` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `cataclysm` | `689F32883C4E9502` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `divinerpg` | `179FCE9AB6967729` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `divinerpg` | `29C46C9F9B029F54` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `divinerpg` | `594DF7E33BAEFF34` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `divinerpg` | `59B95F948B6B9578` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `divinerpg` | `66CABAD95C0CCE94` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `divinerpg_codex` | `1A0CD110E701AB7A` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `divinerpg_codex` | `486480EB1C5336A6` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `divinerpg_codex` | `6D1DA8A7822470F3` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `mystical_ag` | `00D11748B75CDABC` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `productive_bees` | `0072C4F028C327CB` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `productive_bees` | `0FB1FC640471363A` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `productive_bees` | `1D995548A159F291` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `productive_bees` | `1EBD5E4410A6DF34` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `productive_bees` | `3D63868AC4393EBC` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `productive_bees` | `40F8A44DF4D8DBD6` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `productive_bees` | `516289A040EE9FDC` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `productive_bees` | `7B40A9DAA119DE59` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `rftools` | `5DAC6A9AFDDCAA33` | 3 | ROOT_OR_ORPHAN, DUPLICATE_DESCRIPTION |
| `Modern Industrialization` | `0FBA78955F7F1335` | 2 | DUPLICATE_DESCRIPTION |
| `Modern Industrialization` | `499BF10C09D3EAFB` | 2 | DUPLICATE_DESCRIPTION |
| `apotheosis` | `353C7440B32F0A5E` | 2 | DUPLICATE_DESCRIPTION |
| `apotheosis` | `4F4B2A6997F25A5A` | 2 | DUPLICATE_DESCRIPTION |
| `apotheosis` | `50EEDDDE129D2742` | 2 | DUPLICATE_DESCRIPTION |
| `apotheosis` | `5B3CC3F66F2C3DE5` | 2 | DUPLICATE_DESCRIPTION |
| `apotheosis` | `62B2C1A24AE245EA` | 2 | DUPLICATE_DESCRIPTION |
| `apotheosis` | `7234CB42AEF6C941` | 2 | DUPLICATE_DESCRIPTION |
| `ars_nouveau` | `3E671B3A7EAE23C1` | 2 | DUPLICATE_DESCRIPTION |
| `automation_challenges` | `3AC4E2186DC04ED6` | 2 | CHECKMARK_ONLY, DUPLICATE_DESCRIPTION |
| `cataclysm` | `18EB86F91CBBCCC6` | 2 | DUPLICATE_DESCRIPTION |
| `combat_trials` | `22730642E4742859` | 2 | DUPLICATE_DESCRIPTION |
| `combat_trials` | `422D0708D2EE996E` | 2 | DUPLICATE_DESCRIPTION |
| `divinerpg` | `069AD068CDFB38A2` | 2 | DUPLICATE_DESCRIPTION |
| `divinerpg` | `1EEE7BB40F110ECE` | 2 | DUPLICATE_DESCRIPTION |
| `divinerpg` | `22D93E849A8ACA9A` | 2 | DUPLICATE_DESCRIPTION |
| `divinerpg` | `70B73B7BD6EB968E` | 2 | DUPLICATE_DESCRIPTION |
| `divinerpg_codex` | `03E368B2B213B9DD` | 2 | DUPLICATE_DESCRIPTION |
| `divinerpg_codex` | `43C23E6262E14CD5` | 2 | DUPLICATE_DESCRIPTION |
| `divinerpg_codex` | `4A29A7BC42F98577` | 2 | DUPLICATE_DESCRIPTION |
| `divinerpg_codex` | `5070A91AE9998E77` | 2 | DUPLICATE_DESCRIPTION |
| `divinerpg_codex` | `5D7347F980DBD322` | 2 | DUPLICATE_DESCRIPTION |
| `divinerpg_codex` | `7C9BDB55153AD394` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `13EDFA9124D60D53` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `1A8A78BB89CBF5E0` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `1E6717073A2504CA` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `274355D740D7D4AF` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `280288D5E3221C1B` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `2CDB914E84D00B66` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `32439CCC802C8041` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `360B4A5D7EAC3024` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `3CCB560EC216F826` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `47379E2C3068985D` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `4D04830CBA2E04AF` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `4D9DF84171B7453A` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `4E09A9C4D7200D2A` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `51A618DFE2B4746A` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `5269E601F5EED47A` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `673E76FE852A39DE` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `70DD78CE9A860AC0` | 2 | DUPLICATE_DESCRIPTION |
| `ender_io` | `7295B4B792EB5103` | 2 | DUPLICATE_DESCRIPTION |
| `extreme_reactors` | `354086C858E10154` | 2 | DUPLICATE_DESCRIPTION |
| `extreme_reactors` | `69642A3618E86DED` | 2 | DUPLICATE_DESCRIPTION |
| `ice_and_fire` | `162B4F19D2E58FB9` | 2 | DUPLICATE_DESCRIPTION |
| `ice_and_fire` | `4D6EE89D977F041D` | 2 | DUPLICATE_DESCRIPTION |
| `ice_and_fire` | `758A3B06BA4240FF` | 2 | DUPLICATE_DESCRIPTION |
| `immersive_engineering` | `07D2F9D6128C2437` | 2 | DUPLICATE_DESCRIPTION |
| `immersive_engineering` | `41F93E64432175D5` | 2 | DUPLICATE_DESCRIPTION |
| `mainquestline_part_1` | `19BAE924E8965920` | 2 | DUPLICATE_DESCRIPTION |
| `mainquestline_part_1` | `2AEBE3F28996A6ED` | 2 | DUPLICATE_DESCRIPTION |
| `mainquestline_part_1` | `2D0F18033AC4A98F` | 2 | DUPLICATE_DESCRIPTION |
| `mainquestline_part_1` | `3B6F1BD64C0C570F` | 2 | DUPLICATE_DESCRIPTION |
| `mainquestline_part_1` | `4869C413646CC4CC` | 2 | DUPLICATE_DESCRIPTION |
| `mainquestline_part_1` | `72E1C19156633391` | 2 | DUPLICATE_DESCRIPTION |
| `mainquestline_part_1` | `7EC01E7DB045DB05` | 2 | DUPLICATE_DESCRIPTION |
| `mekanism_part_2` | `3593D955361B0C6D` | 2 | DUPLICATE_DESCRIPTION |
| `mekanism_part_2` | `54D8B9CB3F98040F` | 2 | DUPLICATE_DESCRIPTION |
| `mystical_ag` | `1CC4F8570A7A99EB` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `040C85189C07D923` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `049409EDCB433E14` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `04F06E6527C76D27` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `06AEB36ACCD29568` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `08D80CA2FC9EDBBE` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `09DFBC68DF6C2885` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `0A0F597296C7EE1E` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `0B1A4E92EE0BBE34` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `0DDFA4CDFAE02260` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `0E83EA92DDC52774` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `0F5CD890270B0D2B` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `11D75E32EA144C1E` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `14179E7A4ED36957` | 2 | DUPLICATE_DESCRIPTION |
| `other_storage_systems` | `151818021756E29F` | 2 | DUPLICATE_DESCRIPTION |
