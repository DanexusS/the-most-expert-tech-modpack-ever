ServerEvents.recipes(event => {
    event.remove({ output: 'limlog:insertion_node' })
    event.remove({ output: 'limlog:extraction_node' })
    event.shaped(
            Item.of('limlog:insertion_node'),
            [
                    'ABA',
                    'CDC',
                    'BBB'
            ],
            {
                    D: 'modern_industrialization:silicon_battery',
                    C: 'powah:battery_nitro',
                    A: 'advancednetherite:netherite_iron_ingot',
                    B: 'modern_industrialization:stainless_steel_large_plate'
            }
    )
    
    event.shaped(
            Item.of('limlog:extraction_node'),
            [
                    'ABA',
                    'CDC',
                    'BBB'
            ],
            {
                    D: 'modern_industrialization:silicon_battery',
                    C: 'powah:battery_nitro',
                    A: 'immersiveengineering:ingot_hop_graphite',
                    B: 'modern_industrialization:stainless_steel_large_plate'
            }
    )
});
