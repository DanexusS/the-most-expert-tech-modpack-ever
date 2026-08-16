# Strategic Recipe Fairness Report

**PASS**

This gate evaluates the final shaped recipe for each staged output. It expands reusable assemblies recursively, so cross-mod provenance and prior-stage convergence are measured through the complete dependency tree rather than by counting only direct KubeJS ingredients. Runtime throughput and player testing remain separate gates.

| Stage | Output | Milestone | Direct ingredients | Direct NS | Provenance NS | Slots | Direct prior | Transitive prior | Authoritative | Status |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | `kubejs:field_engineering_kit` | yes | 5 | 3 | 2 | 9 | 0 | 0 | yes | PASS |
| 1 | `kubejs:materials_analysis_matrix` | no | 5 | 2 | 2 | 9 | 0 | 0 | yes | PASS |
| 1 | `kubejs:power_regulation_unit` | no | 4 | 3 | 3 | 9 | 0 | 0 | yes | PASS |
| 2 | `immersiveengineering:blastbrick_reinforced` | no | 4 | 3 | 3 | 9 | 0 | 1 | yes | PASS |
| 2 | `kubejs:structural_lattice` | yes | 4 | 2 | 2 | 9 | 1 | 1 | yes | PASS |
| 2 | `modern_industrialization:bronze_boiler` | no | 4 | 3 | 3 | 9 | 0 | 1 | yes | PASS |
| 3 | `kubejs:electrical_bus` | no | 4 | 2 | 4 | 9 | 1 | 1 | yes | PASS |
| 3 | `kubejs:mechanical_core` | yes | 5 | 2 | 4 | 9 | 1 | 3 | yes | PASS |
| 3 | `modern_industrialization:basic_machine_hull` | no | 5 | 2 | 4 | 9 | 0 | 1 | yes | PASS |
| 4 | `create:precision_mechanism` | no | 6 | 3 | 5 | 9 | 0 | 6 | yes | PASS |
| 4 | `kubejs:kinetic_interface` | yes | 5 | 2 | 5 | 9 | 1 | 6 | yes | PASS |
| 4 | `kubejs:kinetic_regulator` | no | 5 | 2 | 5 | 9 | 2 | 6 | yes | PASS |
| 5 | `kubejs:calibrated_substrate` | no | 5 | 3 | 3 | 9 | 1 | 1 | yes | PASS |
| 5 | `kubejs:industrial_frame` | yes | 6 | 3 | 6 | 9 | 2 | 10 | yes | PASS |
| 6 | `ae2:drive` | no | 5 | 2 | 5 | 9 | 0 | 4 | yes | PASS |
| 6 | `ae2:inscriber` | no | 5 | 4 | 6 | 9 | 1 | 11 | yes | PASS |
| 6 | `kubejs:signal_backplane` | yes | 5 | 3 | 5 | 9 | 1 | 4 | yes | PASS |
| 7 | `kubejs:precision_circuit` | yes | 5 | 2 | 9 | 9 | 1 | 14 | yes | PASS |
| 7 | `kubejs:pressure_manifold` | no | 5 | 3 | 7 | 9 | 1 | 13 | yes | PASS |
| 7 | `mekanism:steel_casing` | no | 5 | 3 | 7 | 9 | 1 | 13 | yes | PASS |
| 8 | `industrialforegoing:machine_frame_advanced` | no | 5 | 3 | 8 | 9 | 1 | 13 | yes | PASS |
| 8 | `kubejs:chemical_processor` | yes | 5 | 2 | 10 | 9 | 0 | 18 | yes | PASS |
| 8 | `kubejs:chemical_reactor_core` | no | 5 | 2 | 9 | 9 | 1 | 18 | yes | PASS |
| 9 | `kubejs:bio_process_controller` | no | 6 | 2 | 12 | 9 | 2 | 22 | yes | PASS |
| 9 | `kubejs:bioindustrial_matrix` | yes | 5 | 3 | 12 | 9 | 2 | 22 | yes | PASS |
| 9 | `mysticalagriculture:infusion_altar` | no | 4 | 3 | 11 | 9 | 1 | 22 | yes | PASS |
| 10 | `ae2:controller` | no | 4 | 2 | 12 | 9 | 0 | 25 | yes | PASS |
| 10 | `ae2:quantum_ring` | no | 5 | 3 | 12 | 9 | 1 | 25 | yes | PASS |
| 10 | `kubejs:quantum_bus` | no | 6 | 1 | 12 | 9 | 2 | 25 | yes | PASS |
| 10 | `kubejs:quantum_logic` | yes | 4 | 2 | 12 | 9 | 1 | 25 | yes | PASS |
| 11 | `kubejs:resonant_core` | yes | 5 | 3 | 14 | 9 | 1 | 28 | yes | PASS |
| 11 | `kubejs:resonant_power_cell` | no | 5 | 2 | 14 | 9 | 1 | 28 | yes | PASS |
| 11 | `mekanism:induction_casing` | no | 5 | 3 | 12 | 9 | 1 | 28 | yes | PASS |
| 11 | `powah:reactor_nitro` | no | 5 | 2 | 14 | 9 | 0 | 28 | yes | PASS |
| 12 | `kubejs:antimatter_regulator` | yes | 5 | 2 | 14 | 9 | 0 | 32 | yes | PASS |
| 12 | `mekanism:sps_casing` | no | 4 | 2 | 14 | 9 | 1 | 32 | yes | PASS |
| 13 | `kubejs:dimensional_resonator` | yes | 6 | 1 | 15 | 9 | 3 | 37 | yes | PASS |
| 14 | `draconicevolution:awakened_core` | no | 4 | 3 | 16 | 9 | 0 | 38 | yes | PASS |
| 14 | `draconicevolution:wyvern_core` | no | 4 | 3 | 15 | 9 | 2 | 38 | yes | PASS |
| 14 | `kubejs:draconic_lattice` | no | 4 | 2 | 15 | 9 | 1 | 38 | yes | PASS |
| 14 | `kubejs:draconic_processor` | yes | 6 | 2 | 16 | 9 | 0 | 38 | yes | PASS |
| 15 | `kubejs:emc_containment_core` | no | 5 | 3 | 17 | 9 | 1 | 42 | yes | PASS |
| 15 | `kubejs:transmutation_matrix` | yes | 6 | 2 | 17 | 9 | 1 | 42 | yes | PASS |
| 15 | `projecte:philosophers_stone` | no | 5 | 4 | 16 | 9 | 2 | 42 | yes | PASS |
| 15 | `projecte:transmutation_table` | no | 4 | 3 | 17 | 9 | 0 | 42 | yes | PASS |
| 16 | `avaritia:extreme_crafting_table` | no | 5 | 2 | 18 | 9 | 1 | 46 | yes | PASS |
| 16 | `extendedcrafting:ultimate_table` | no | 5 | 3 | 16 | 9 | 2 | 42 | yes | PASS |
| 16 | `kubejs:cosmic_assembly_matrix` | no | 5 | 4 | 18 | 9 | 2 | 46 | yes | PASS |
| 16 | `kubejs:cosmic_catalyst` | yes | 7 | 3 | 18 | 9 | 2 | 46 | yes | PASS |
| 17 | `avaritia:infinity_ingot` | no | 7 | 4 | 18 | 9 | 6 | 50 | yes | PASS |
| 17 | `kubejs:cosmic_synthesis_core` | yes | 5 | 1 | 18 | 9 | 2 | 50 | yes | PASS |
| 18 | `kubejs:creative_convergence_matrix` | yes | 7 | 1 | 18 | 9 | 4 | 53 | yes | PASS |

## Aggregate

- Parsed shaped strategic outputs: **52**
- Milestones with shaped recipes: **18 / 18**
- Authoritative strategic recipes: **52 / 52**
- Failures: **0**
