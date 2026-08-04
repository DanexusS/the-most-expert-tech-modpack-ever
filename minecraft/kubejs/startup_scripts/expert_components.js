const EXPERT_COMPONENTS = [
  ['mechanical_core', 'Механическое ядро', 'minecraft:item/clock'],
  ['industrial_frame', 'Промышленная рама', 'minecraft:item/iron_ingot'],
  ['precision_circuit', 'Прецизионная схема', 'minecraft:item/comparator'],
  ['chemical_processor', 'Химический процессор', 'minecraft:item/ender_eye'],
  ['bioindustrial_matrix', 'Биоиндустриальная матрица', 'minecraft:item/slime_ball'],
  ['quantum_logic', 'Квантовая логическая матрица', 'minecraft:item/amethyst_shard'],
  ['resonant_core', 'Резонансное энергетическое ядро', 'minecraft:item/nether_star'],
  ['draconic_processor', 'Драконический процессор', 'minecraft:item/dragon_breath'],
  ['transmutation_matrix', 'Матрица трансмутации', 'minecraft:item/echo_shard'],
  ['cosmic_catalyst', 'Космический катализатор', 'minecraft:item/netherite_ingot']
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
      .rarity(component[0] === 'cosmic_catalyst' ? 'epic' : 'rare')
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
