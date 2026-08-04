ServerEvents.recipes(event => {
  event.remove({ output: 'mysticalagriculture:infusion_altar' })

    event.shaped(
            Item.of('mysticalagriculture:infusion_altar'),
            [
                    'ABA',
                    'BCB',
                    'CCC'
            ],
            {
                    A: 'cataclysm:ignitium_ingot',
                    C: 'pneumaticcraft:compressed_stone',
                    B: 'minecraft:red_wool'
            }
    )
});
