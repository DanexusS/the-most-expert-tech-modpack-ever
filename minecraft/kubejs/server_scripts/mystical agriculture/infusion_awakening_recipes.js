ServerEvents.recipes(event => {
    event.remove({ output: 'mysticalautomation:awakening_altarnator' })
    event.remove({ output: 'mysticalautomation:infusion_altarnator' })
    event.shaped(
            Item.of('mysticalautomation:awakening_altarnator'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    B: 'mysticalagriculture:awakening_altar',
                    E: 'mysticalagriculture:awakened_supremium_block',
                    A: 'advancednetherite:netherite_iron_ingot',
                    D: 'mysticalagriculture:machine_frame',
                    C: 'mysticalagriculture:soulium_ingot'
            }
    )
    event.shaped(
            Item.of('mysticalautomation:infusion_altarnator'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    B: 'mysticalagriculture:infusion_altar',
                    E: 'mysticalagradditions:insanium_block',
                    A: 'advancednetherite:netherite_iron_ingot',
                    D: 'mysticalagriculture:machine_frame',
                    C: 'mysticalagriculture:soulium_ingot'
            }
    )
});
