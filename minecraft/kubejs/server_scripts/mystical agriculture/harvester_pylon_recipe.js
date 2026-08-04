ServerEvents.recipes(event => {
  event.remove({ output: 'pylons:harvester_pylon' })
  event.shaped('pylons:harvester_pylon', [
    'RRR',
    'BHB',
    'III'
  ], {
    I: 'allthecompressed:blackstone_2x',
    B: 'enderio:dark_steel_bars',
    H: 'allthecompressed:hay_block_1x',
    R: 'actuallyadditions:ethetic_white_slab'
  })
})
