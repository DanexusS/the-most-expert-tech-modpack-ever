ServerEvents.recipes(event => {
  event.remove({ output: 'ae2:controller' })
  event.shaped('ae2:controller', [
    'RBR',
    'BMB',
    'RBR'
  ], {
    M: 'mekanism:ultimate_control_circuit',
    B: 'extendedae:entro_ingot',
    R: 'megacells:sky_steel_block'
  })
})
