ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:index_inscriber' })
    event.shaped(
            Item.of('minformax:index_inscriber'),
            [
                    'ABA',
                    'CDC',
                    'BEB'
            ],
            {
                    B: 'silentgear:azure_silver_ingot',
                    A: 'minecraft:blaze_rod',
                    D: 'minecraft:crying_obsidian',
                    C: 'avaritia:double_compressed_crafting_table',
                    E: 'allthecompressed:iron_block_1x'
            }
    )
});
