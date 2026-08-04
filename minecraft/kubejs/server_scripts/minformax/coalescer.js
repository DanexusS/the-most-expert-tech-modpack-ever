ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:ore_coalescer' })
  event.shaped('minformax:ore_coalescer', [
    'RBR',
    'BMB',
    'RBR'
  ], {
    M: 'advancednetherite:netherite_diamond_block',
    B: 'mekanism:elite_control_circuit',
    R: 'allthecompressed:iron_block_2x'
  })
})
