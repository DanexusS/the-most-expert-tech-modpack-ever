ServerEvents.recipes(event => {

    event.shaped(
            Item.of('endrem:cryptic_eye'),
            [
                    'ABA',
                    'CDE',
                    'AFA'
            ],
            {
                    C: 'occultism:large_candle',
                    E: 'minecraft:enchanting_table',
                    B: 'apothic_enchanting:geode_shelf',
                    D: 'minecraft:ender_eye',
                    F: 'create_enchantment_industry:enchanting_template',
                    A: 'minecraft:experience_bottle'
            }
    )
});
