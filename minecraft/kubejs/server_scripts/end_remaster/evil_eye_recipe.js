ServerEvents.recipes(event => {

    event.shaped(
            Item.of('endrem:evil_eye'),
            [
                    'ABA',
                    'CDE',
                    'ABA'
            ],
            {
                    C: 'minecraft:rabbit_foot',
                    B: '#c:ingots/silver',
                    D: 'minecraft:ender_eye',
                    A: 'minecraft:amethyst_block',
                    E: 'minecraft:potion'
            }
    )
});
