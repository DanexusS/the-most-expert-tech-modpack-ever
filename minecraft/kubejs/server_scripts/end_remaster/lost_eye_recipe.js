ServerEvents.recipes(event => {

    event.shaped(
            Item.of('endrem:lost_eye'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    E: 'minecraft:nether_wart',
                    A: 'minecraft:redstone_block',
                    C: 'ars_nouveau:fire_essence',
                    D: 'minecraft:ender_eye',
                    B: 'minecraft:fermented_spider_eye'
            }
    )
});
