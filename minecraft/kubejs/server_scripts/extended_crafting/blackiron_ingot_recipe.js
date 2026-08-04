ServerEvents.recipes(event => {
  event.remove({ output: 'extendedcrafting:black_iron_ingot' })
  event.shaped('extendedcrafting:black_iron_ingot', [
    'RBN',
    'BMB',
    'NBR'
  ], {
    M: 'minecraft:iron_ingot',
    B: 'enderio:vibrant_alloy_ingot',
    N: 'mekanism:ingot_refined_obsidian',
    R: 'minecraft:netherite_ingot'
  })
})
