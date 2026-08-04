ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:memory_shard' })
    event.shaped(
            Item.of('minformax:memory_shard'),
            [
                    ' BA',
                    'BDB',
                    'AB '
            ],
            {
                    A: 'allthecompressed:signalum_block_4x',
                    D: 'enderio:weather_crystal',
                    B: 'allthecompressed:redstone_block_4x'
            }
    )
});
