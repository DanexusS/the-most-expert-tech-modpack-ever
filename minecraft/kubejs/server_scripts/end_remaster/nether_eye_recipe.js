ServerEvents.recipes(event => {
  event.remove({ output: 'endrem:nether_eye' })
  event.shaped('endrem:nether_eye', [
    'NWN',
    'AMA',
    'RBR'
  ], {
    M: 'minecraft:ender_eye',
    A: 'minecraft:lava_bucket',
    B: 'minecraft:netherrack',
    N: 'minecraft:nether_bricks',
    R: 'minecraft:nether_wart_block',
    W: 'minecraft:wither_skeleton_skull'
  })
})
