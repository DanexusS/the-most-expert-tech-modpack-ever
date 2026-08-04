ServerEvents.recipes(event => {

    event.shaped(
            Item.of('endrem:black_eye'),
            [
                    'AAA',
                    'ABA',
                    'ACA'
            ],
            {
                    B: 'minecraft:ender_eye',
                    A: 'minecraft:netherite_ingot',
                    C: 'minecraft:oak_chest_boat'
            }
    )
});
