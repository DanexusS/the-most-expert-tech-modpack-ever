const EXPERT_COMPONENTS = [
  // Early foundation: three independent opening disciplines.
  ['field_engineering_kit', 'minecraft:item/compass', 'uncommon'],
  ['power_regulation_unit', 'minecraft:item/redstone', 'uncommon'],
  ['materials_analysis_matrix', 'minecraft:item/quartz', 'uncommon'],

  // Persistent intermediate engineering standards. These make the main chain
  // multi-step without relying on meaningless bulk ingot costs.
  ['structural_lattice', 'minecraft:item/iron_bars', 'uncommon'],
  ['kinetic_regulator', 'minecraft:item/repeater', 'rare'],
  ['electrical_bus', 'minecraft:item/lightning_rod', 'rare'],
  ['calibrated_substrate', 'minecraft:item/comparator', 'rare'],
  ['signal_backplane', 'minecraft:item/echo_shard', 'rare'],
  ['pressure_manifold', 'minecraft:item/copper_block', 'rare'],
  ['chemical_reactor_core', 'minecraft:item/ender_eye', 'rare'],
  ['bio_process_controller', 'minecraft:item/slime_ball', 'rare'],
  ['quantum_bus', 'minecraft:item/amethyst_shard', 'rare'],
  ['resonant_power_cell', 'minecraft:item/nether_star', 'rare'],
  ['antimatter_regulator', 'minecraft:item/dragon_breath', 'epic'],
  ['dimensional_resonator', 'minecraft:item/recovery_compass', 'epic'],
  ['draconic_lattice', 'minecraft:item/dragon_breath', 'epic'],
  ['emc_containment_core', 'minecraft:item/echo_shard', 'epic'],
  ['cosmic_assembly_matrix', 'minecraft:item/netherite_block', 'epic'],
  ['cosmic_synthesis_core', 'minecraft:item/end_crystal', 'epic'],
  ['creative_convergence_matrix', 'minecraft:item/knowledge_book', 'epic'],

  // Macro-stage milestones.
  ['kinetic_interface', 'minecraft:item/piston', 'rare'],
  ['mechanical_core', 'minecraft:item/clock', 'rare'],
  ['industrial_frame', 'minecraft:item/iron_ingot', 'rare'],
  ['precision_circuit', 'minecraft:item/comparator', 'rare'],
  ['chemical_processor', 'minecraft:item/ender_eye', 'rare'],
  ['bioindustrial_matrix', 'minecraft:item/slime_ball', 'rare'],
  ['quantum_logic', 'minecraft:item/amethyst_shard', 'rare'],
  ['resonant_core', 'minecraft:item/nether_star', 'rare'],
  ['draconic_processor', 'minecraft:item/dragon_breath', 'rare'],
  ['transmutation_matrix', 'minecraft:item/echo_shard', 'rare'],
  ['cosmic_catalyst', 'minecraft:item/netherite_ingot', 'epic']
]

const DIVINE_PROGRESSION_SEALS = [
  ['divine_seal', 'divinerpg:item/divine_shards'],
  ['eden_seal', 'divinerpg:item/eden_heart'],
  ['wildwood_seal', 'divinerpg:item/wildwood_heart'],
  ['apalachia_seal', 'divinerpg:item/apalachia_heart'],
  ['skythern_seal', 'divinerpg:item/skythern_heart'],
  ['mortum_seal', 'divinerpg:item/mortum_heart'],
  ['vethea_seal', 'divinerpg:item/clean_pearls'],
  ['wreck_seal', 'divinerpg:item/arksiane_lump'],
  ['lunar_seal', 'divinerpg:item/everbright']
]

StartupEvents.registry('item', event => {
  EXPERT_COMPONENTS.forEach(component => {
    event.create(component[0])
      .texture(component[1])
      .unstackable()
      .rarity(component[2])
      .containerItem(`kubejs:${component[0]}`)
  })

  DIVINE_PROGRESSION_SEALS.forEach(seal => {
    event.create(seal[0])
      .texture(seal[1])
      .unstackable()
      .rarity('epic')
      .containerItem(`kubejs:${seal[0]}`)
  })
})
