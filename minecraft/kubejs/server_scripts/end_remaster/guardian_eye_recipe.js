ServerEvents.recipes(event => {

    event.shaped(
            Item.of('endrem:guardian_eye'),
            [
                    'ABC',
                    'DED',
                    'CFA'
            ],
            {
                    A: 'minecraft:prismarine_crystals',
                    C: 'minecraft:prismarine_shard',
                    D: 'mysticalagriculture:prismarine_agglomeratio',
                    E: 'minecraft:ender_eye',
                    B: 'minecraft:chicken',
                    F: 'minecraft:sea_pickle'
            }
    )
});
