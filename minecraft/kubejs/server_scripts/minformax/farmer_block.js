ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:farmer' })
  event.shaped('minformax:farmer', [
    'RBR',
    'BMB',
    'RBR'
  ], {
    M: 'allthemodium:allthemodium_hoe',
    B: 'powah:nitro_crystal_block',
    R: 'minformax:quantum_ingot'
  })
})
