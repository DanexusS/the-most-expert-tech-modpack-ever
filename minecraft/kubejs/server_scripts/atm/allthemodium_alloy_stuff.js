ServerEvents.recipes(event => {

  // Sword
  event.shaped(
    'allthemodium:alloy_sword',
    [
      ' M ',
      ' M ',
      ' S '
    ],
    {
      M: 'kubejs:allthemodium_alloy',
      S: 'allthemodium:allthemodium_rod'
    }
  )

  // Pickaxe
  event.shaped(
    'allthemodium:alloy_pick',
    [
      'MMM',
      ' S ',
      ' S '
    ],
    {
      M: 'kubejs:allthemodium_alloy',
      S: 'allthemodium:allthemodium_rod'
    }
  )

  // Axe
  event.shaped(
    'allthemodium:alloy_axe',
    [
      'MM ',
      'MS ',
      ' S '
    ],
    {
      M: 'kubejs:allthemodium_alloy',
      S: 'allthemodium:allthemodium_rod'
    }
  )

  // Shovel
  event.shaped(
    'allthemodium:alloy_shovel',
    [
      ' M ',
      ' S ',
      ' S '
    ],
    {
      M: 'kubejs:allthemodium_alloy',
      S: 'allthemodium:allthemodium_rod'
    }
  )

  // Trident (custom, mas estilo vanilla)
  event.shaped(
    'allthemodium:alloy_trident',
    [
      ' M ',
      'MMM',
      ' S '
    ],
    {
      M: 'kubejs:allthemodium_alloy',
      S: 'allthemodium:allthemodium_rod'
    }
  )

})
