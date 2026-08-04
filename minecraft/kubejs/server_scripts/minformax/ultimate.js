ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:ultimate_speed_upgrade' })
  event.shaped('minformax:ultimate_speed_upgrade', [
    'RBR',
    'BMB',
    'RBR'
  ], {
    M: 'allthecompressed:antimatter_block',
    B: 'mekanism_extras:upgrade_creative',
    R: 'minformax:ultimate_processing_upgrade'
  })
})
