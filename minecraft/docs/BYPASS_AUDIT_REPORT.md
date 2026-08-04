# Bypass Audit Report

**IN PROGRESS**

This report tracks known static acquisition paths. A PASS means the source tree contains an explicit policy and authoritative recipe evidence; it does not claim that every third-party runtime mechanic has already been tested.

## Summary

- Gated outputs: **58**
- Outputs with recipe declarations: **51**
- Outputs with explicit recipe removal evidence: **3**
- Unauthorized quest reward outputs: **2**
- Unallowlisted data/loot mentions: **0**
- Outputs without recipe declaration: **7**
- Non-KubeJS outputs without removal evidence: **17**
- Late outputs missing EMC policy: **4**
- Stage 12+ outputs missing simulation policy: **15**

## Unauthorized quest rewards

- `avaritia:infinity_ingot`: config/ftbquests/quests/chapters/avaritia.snbt, config/ftbquests/quests/chapters/creative_items.snbt
- `modern_industrialization:basic_machine_hull`: config/ftbquests/quests/chapters/Modern Industrialization.snbt

## Outputs without an authoritative recipe declaration

- `avaritia:infinity_ingot`
- `kubejs:lunar_seal`
- `kubejs:mortum_seal`
- `kubejs:skythern_seal`
- `kubejs:vethea_seal`
- `mekanism:pellet_antimatter`
- `pneumaticcraft:printed_circuit_board`

## Non-KubeJS outputs without removal evidence

- `ae2:drive`
- `ae2:inscriber`
- `ae2:quantum_ring`
- `avaritia:extreme_crafting_table`
- `create:precision_mechanism`
- `draconicevolution:awakened_core`
- `draconicevolution:wyvern_core`
- `immersiveengineering:blastbrick_reinforced`
- `industrialforegoing:machine_frame_advanced`
- `mekanism:induction_casing`
- `mekanism:sps_casing`
- `mekanism:steel_casing`
- `modern_industrialization:basic_machine_hull`
- `modern_industrialization:bronze_boiler`
- `powah:reactor_nitro`
- `projecte:philosophers_stone`
- `projecte:transmutation_table`

## EMC policy gaps

- `kubejs:lunar_seal`
- `kubejs:mortum_seal`
- `kubejs:skythern_seal`
- `kubejs:vethea_seal`

## Resource simulation policy gaps

- `draconicevolution:wyvern_core`
- `kubejs:antimatter_regulator`
- `kubejs:cosmic_assembly_matrix`
- `kubejs:cosmic_catalyst`
- `kubejs:cosmic_synthesis_core`
- `kubejs:dimensional_resonator`
- `kubejs:draconic_lattice`
- `kubejs:draconic_processor`
- `kubejs:emc_containment_core`
- `kubejs:lunar_seal`
- `kubejs:mortum_seal`
- `kubejs:skythern_seal`
- `kubejs:transmutation_matrix`
- `kubejs:vethea_seal`
- `mekanism:sps_casing`

## Trade policy coverage

The following non-KubeJS late outputs already have an explicit trade blacklist entry:

- `ae2:controller`
- `avaritia:infinity_ingot`
- `mekanism:sps_casing`
- `projecte:philosophers_stone`
