ServerEvents.recipes(event => {
  event.remove({ id: 'allthemodium:teleport_pad' })

  event.shaped('allthemodium:teleport_pad', [
    'UNU',
    'NPN',
    'UNU'
  ], {
    U: '#c:nuggets/unobtainium',
    N: '#c:nuggets/allthemodium',
    P: 'minecraft:ender_pearl'
  }).id('kubejs:allthemodium/teleport_pad')
})
