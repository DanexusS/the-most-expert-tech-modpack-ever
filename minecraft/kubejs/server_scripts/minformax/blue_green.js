ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:amanita_ingot' })
    event.remove({ output: 'minformax:yinmin_ingot' })
    event.shaped(
            Item.of('minformax:amanita_ingot'),
            [
                    'ABA',
                    'BCB',
                    'ABA'
            ],
            {
                    B: 'minformax:yinmin_ingot',
                    C: 'minformax:frozen_crystal',
                    A: 'allthecompressed:emerald_block_2x'
            }
    )
    event.shaped(
            Item.of('minformax:yinmin_ingot'),
            [
                    'ABA',
                    'BCB',
                    'ABA'
            ],
            {
                    C: 'minformax:frozen_crystal',
                    A: 'allthecompressed:lapis_block_2x',
                    B: 'minformax:quantum_ingot'
            }
    )
});
