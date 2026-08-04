ServerEvents.recipes(event => {
  event.remove({ output: 'entangled:block' })

  event.shaped('entangled:block', [
    'SNS',
    'NDN',
    'SNS'
  ], {
    S: 'mysticalagriculture:awakened_supremium_ingot',
    N: 'avaritia:neutron_ingot',
    D: 'avaritia:compressed_chest'
  })
})