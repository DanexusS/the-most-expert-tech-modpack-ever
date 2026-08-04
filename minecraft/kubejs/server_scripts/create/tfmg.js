ServerEvents.recipes(event => {

  // N-Type Semiconductor
  event.recipes.createMixing(
    'tfmg:n_semiconductor',
    [
      'immersiveengineering:dust_sulfur',
      'oritech:silicon'
    ]
  ).superheated()

  // P-Type Semiconductor
  event.recipes.createMixing(
    'tfmg:p_semiconductor',
    [
      'immersiveengineering:ingot_aluminum',
      'oritech:silicon'
    ]
  ).superheated()

})
