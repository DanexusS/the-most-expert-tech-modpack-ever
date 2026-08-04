ServerEvents.recipes(event => {
  event.remove({ output: 'mysticalagriculture:infusion_pedestal' })

    event.shaped(
            Item.of('mysticalagriculture:infusion_pedestal'),
            [
                    'ABA',
                    ' C ',
                    ' C '
            ],
            {
                    A: 'modern_industrialization:gold_double_ingot',
                    C: 'pneumaticcraft:compressed_stone',
                    B: 'minecraft:red_wool'
            }
    )
});
