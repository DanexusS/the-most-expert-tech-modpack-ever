ServerEvents.recipes(event => {
  event.remove({ output: 'mekanism:jetpack' })
  event.shaped('mekanism:jetpack', [
    'SMS',
    'BUB',
    ' D '
  ], {
    M: 'mekanism:ultimate_control_circuit',
    U: 'mekanism:ultimate_chemical_tank',
    B: '#c:ingots/tin',
    D: 'immersiveengineering:plate_duroplast',
    S: '#c:ingots/steel'
  })

  event.remove({ output: 'oritech:jetpack' })
  event.shaped('oritech:jetpack', [
    ' M ',
    'BBB',
    'SDS'
  ], {
    M: 'immersiveengineering:ersatz_leather',
    B: '#c:ingots/steel',
    D: 'enderio:redstone_alloy_block',
    S: 'immersiveengineering:plate_duroplast'
  })
})