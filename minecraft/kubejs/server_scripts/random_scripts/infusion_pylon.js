ServerEvents.recipes(event => {
  event.remove('pylons:infusion_pylon')
    event.shaped(
            Item.of('pylons:infusion_pylon'),
            [
                    'AAA',
                    'BCB',
                    'DDD'
            ],
            {
                    B: 'enderio:end_steel_bars',
                    A: 'immersiveengineering:slab_sheetmetal_iron',
                    C: 'minecraft:beacon',
                    D: 'allthecompressed:blackstone_2x'
            }
    )
});
