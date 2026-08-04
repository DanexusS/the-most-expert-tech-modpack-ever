ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:heliodor_ingot' })
    event.shaped(
            Item.of('minformax:heliodor_ingot'),
            [
                    'ABA',
                    'BCB',
                    'ABA'
            ],
            {
                    C: 'minformax:frozen_core',
                    B: 'minformax:amanita_ingot',
                    A: 'allthecompressed:gold_block_2x'
            }
    )
});
