ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:babylon_key' })
    event.shaped(
            Item.of('minformax:babylon_key'),
            [
                    ' AB',
                    ' CA',
                    'D  '
            ],
            {
                    D: 'minformax:heliodor_ingot',
                    C: 'avaritia:blaze_cube_block',
                    B: 'projecte:watch_of_flowing_time',
                    A: 'allthecompressed:gold_block_5x'
            }
    )
});
