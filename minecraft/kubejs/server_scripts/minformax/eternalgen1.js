ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:eternal_generator' })

    event.shaped(
            Item.of('minformax:eternal_generator'),
            [
                    'ABA',
                    'BCB',
                    'ABA'
            ],
            {
                    B: 'minecraft:ancient_debris',
                    A: 'allthecompressed:platinum_block_5x',
                    C: 'irons_spellbooks:mithril_scrap'
            }
    )
});
