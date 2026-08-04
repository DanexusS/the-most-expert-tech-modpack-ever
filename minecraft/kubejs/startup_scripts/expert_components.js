const EXPERT_COMPONENTS = [
  // Early foundation. These components deliberately represent separate paths:
  // field engineering, basic power control and material analysis.
  ['field_engineering_kit', 'minecraft:item/compass', 'uncommon'],
  ['power_regulation_unit', 'minecraft:item/redstone', 'uncommon'],
  ['materials_analysis_matrix', 'minecraft:item/quartz', 'uncommon'],
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
      .rarity(component[2])
  })

  DIVINE_PROGRESSION_SEALS.forEach(seal => {
    event.create(seal[0])
      .texture(seal[1])
      .unstackable()
      .rarity('epic')
      .containerItem(`kubejs:${seal[0]}`)
  })
})
