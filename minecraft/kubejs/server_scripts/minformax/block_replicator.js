ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:block_replicator' })
    event.shaped(
            Item.of('minformax:block_replicator'),
            [
                    'AAA',
                    'BCB',
                    'AAA'
            ],
            {
                    C: 'advanced_ae:quantum_processor',
                    A: 'allthecompressed:iron_block_1x',
                    B: 'extendedae:assembler_matrix_glass'
            }
    )
});
