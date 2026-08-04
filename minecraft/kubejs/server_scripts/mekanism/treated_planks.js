ServerEvents.recipes(event => {
  event.shaped(
    Item.of('tfmg:hardened_planks', 4),
    [
      'PPP',
      'PBP',
      'PPP'
    ],
    {
      P: '#minecraft:planks',
      B: 'tfmg:creosote_bucket'
    }
  )
})
