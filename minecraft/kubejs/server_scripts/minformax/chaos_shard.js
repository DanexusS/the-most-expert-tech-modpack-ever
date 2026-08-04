ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:chaos_shard' })
    event.shaped(
            Item.of('minformax:chaos_shard'),
            [
                    ' BA',
                    'BDB',
                    'AB '
            ],
            {
                    A: 'allthecompressed:black_concrete_5x',
                    D: 'allthecompressed:netherite_block_5x',
                    B: 'allthecompressed:nitro_crystal_block_4x'
            }
    )
});
