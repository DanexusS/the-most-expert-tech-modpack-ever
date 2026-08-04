ServerEvents.recipes(event => {
  event.remove({ output: 'projecte:collector_mk1' })

    event.shaped(
            Item.of('projecte:collector_mk1'),
            [
                    'ABA',
                    'ACA',
                    'ADA'
            ],
            {
                    B: 'projecte:red_matter_block',
                    A: 'minecraft:glowstone',
                    C: 'allthecompressed:diamond_block_5x',
                    D: 'minecraft:furnace'
            }
    )
});
