const EXPERT_COMPONENTS = [
  // Early foundation. These components deliberately represent separate paths:
  // field engineering, basic power control and material analysis.
  ['field_engineering_kit', 'Комплект полевого инженера', 'minecraft:item/compass', 'uncommon'],
  ['power_regulation_unit', 'Блок регулирования энергии', 'minecraft:item/redstone', 'uncommon'],
  ['materials_analysis_matrix', 'Матрица анализа материалов', 'minecraft:item/quartz', 'uncommon'],
  ['kinetic_interface', 'Кинетический промышленный интерфейс', 'minecraft:item/piston', 'rare'],

  ['mechanical_core', 'Механическое ядро', 'minecraft:item/clock', 'rare'],
  ['industrial_frame', 'Промышленная рама', 'minecraft:item/iron_ingot', 'rare'],
  ['precision_circuit', 'Прецизионная схема', 'minecraft:item/comparator', 'rare'],
  ['chemical_processor', 'Химический процессор', 'minecraft:item/ender_eye', 'rare'],
  ['bioindustrial_matrix', 'Биоиндустриальная матрица', 'minecraft:item/slime_ball', 'rare'],
  ['quantum_logic', 'Квантовая логическая матрица', 'minecraft:item/amethyst_shard', 'rare'],
  ['resonant_core', 'Резонансное энергетическое ядро', 'minecraft:item/nether_star', 'rare'],
  ['draconic_processor', 'Драконический процессор', 'minecraft:item/dragon_breath', 'rare'],
  ['transmutation_matrix', 'Матрица трансмутации', 'minecraft:item/echo_shard', 'rare'],
  ['cosmic_catalyst', 'Космический катализатор', 'minecraft:item/netherite_ingot', 'epic']
]

const DIVINE_PROGRESSION_SEALS = [
  ['divine_seal', 'Печать Божественного порога', 'divinerpg:item/divine_shards'],
  ['eden_seal', 'Печать Эдема', 'divinerpg:item/eden_heart'],
  ['wildwood_seal', 'Печать Дикого леса', 'divinerpg:item/wildwood_heart'],
  ['apalachia_seal', 'Печать Апалачии', 'divinerpg:item/apalachia_heart'],
  ['skythern_seal', 'Печать Скайтерна', 'divinerpg:item/skythern_heart'],
  ['mortum_seal', 'Печать Мортума', 'divinerpg:item/mortum_heart'],
  ['vethea_seal', 'Печать Ветеи', 'divinerpg:item/clean_pearls'],
  ['wreck_seal', 'Печать Рэка', 'divinerpg:item/arksiane_lump'],
  ['lunar_seal', 'Печать Леди Луны', 'divinerpg:item/everbright']
]

StartupEvents.registry('item', event => {
  EXPERT_COMPONENTS.forEach(component => {
    event.create(component[0])
      .displayName(component[1])
      .texture(component[2])
      .rarity(component[3])
  })

  DIVINE_PROGRESSION_SEALS.forEach(seal => {
    event.create(seal[0])
      .displayName(seal[1])
      .texture(seal[2])
      .unstackable()
      .rarity('epic')
      .containerItem(`kubejs:${seal[0]}`)
  })
})
