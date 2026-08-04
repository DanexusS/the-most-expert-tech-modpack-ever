ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:linker' })
    event.shaped(
            Item.of('minformax:linker'),
            [
                    'AB ',
                    'CD ',
                    'DD '
            ],
            {
                    A: 'modern_industrialization:plutonium_battery',
                    B: 'enderio:wireless_charger_antenna_advanced',
                    C: 'oritech:super_ai_chip',
                    D: 'minecraft:bedrock'
            }
    )
});
