const CUSTOM_MA_ESSENCES = [
  {
    id: 'dimyanit_essence',
    name: 'Эссенция Димьянита',
    texture: 'mysticalagradditions:item/essence/nether_star_essence'
  },
  {
    id: 'eduardit_essence',
    name: 'Эссенция Эдуардита',
    texture: 'mysticalagradditions:item/essence/dragon_egg_essence'
  },
  {
    id: 'dannexit_essence',
    name: 'Эссенция Даннексита',
    texture: 'mysticalagradditions:item/essence/gaia_spirit_essence'
  },
  {
    id: 'emkoviy_essence',
    name: 'Эссенция Емковия',
    texture: 'mysticalagradditions:item/essence/awakened_draconium_essence'
  },
  {
    id: 'rakuniy_essence',
    name: 'Эссенция Ракуния',
    texture: 'mysticalagradditions:item/essence/neutronium_essence'
  },
  {
    id: 'kodeksit_essence',
    name: 'Эссенция Кодэксита',
    texture: 'mysticalagradditions:item/essence/nitro_crystal_essence'
  }
]

const CUSTOM_MA_BLOCKS = [
  {
    id: 'dimyanit_block',
    name: 'Блок эссенции Димьянита',
    texture: 'mysticalagriculture:block/inferium_block'
  },
  {
    id: 'eduardit_block',
    name: 'Блок эссенции Эдуардита',
    texture: 'mysticalagriculture:block/prudentium_block'
  },
  {
    id: 'dannexit_block',
    name: 'Блок эссенции Даннексита',
    texture: 'mysticalagriculture:block/tertium_block'
  },
  {
    id: 'emkoviy_block',
    name: 'Блок эссенции Емковия',
    texture: 'mysticalagriculture:block/imperium_block'
  },
  {
    id: 'rakuniy_block',
    name: 'Блок эссенции Ракуния',
    texture: 'mysticalagriculture:block/supremium_block'
  },
  {
    id: 'kodeksit_block',
    name: 'Блок эссенции Кодэксита',
    texture: 'mysticalagradditions:block/insanium_block'
  }
]

const CUSTOM_MA_CRYSTALS = [
  {
    id: 'insanium_crystal',
    name: 'Кристалл Инсаниума',
    durability: 8192
  },
  {
    id: 'dimyanit_crystal',
    name: 'Кристалл Димьянита',
    durability: 16384
  },
  {
    id: 'eduardit_crystal',
    name: 'Кристалл Эдуардита',
    durability: 32768
  },
  {
    id: 'dannexit_crystal',
    name: 'Кристалл Даннексита',
    durability: 65536
  },
  {
    id: 'emkoviy_crystal',
    name: 'Кристалл Емковия',
    durability: 131072
  },
  {
    id: 'rakuniy_crystal',
    name: 'Кристалл Ракуния',
    durability: 262144
  }
]

StartupEvents.registry('item', event => {
  CUSTOM_MA_ESSENCES.forEach(essence => {
    event.create(essence.id)
      .displayName(essence.name)
      .texture(essence.texture)
  })

  CUSTOM_MA_CRYSTALS.forEach(crystal => {
    event.create(crystal.id)
      .displayName(crystal.name)
      .texture('mysticalagriculture:item/infusion_crystal')
      .unstackable()
      .maxDamage(crystal.durability)
      .containerItem(`kubejs:${crystal.id}`)
  })
})

StartupEvents.registry('block', event => {
  CUSTOM_MA_BLOCKS.forEach(block => {
    event.create(block.id)
      .displayName(block.name)
      .hardness(5)
      .resistance(6)
      .texture(block.texture)
  })
})
