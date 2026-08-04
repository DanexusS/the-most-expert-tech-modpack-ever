ServerEvents.recipes(event => {

    event.shaped(
            Item.of('endrem:old_eye'),
            [
                    'ABA',
                    'CDE',
                    'AFA'
            ],
            {
                    A: 'allthecompressed:sand_2x',
                    E: 'minecraft:dead_bush',
                    B: 'create:cuckoo_clock',
                    D: 'minecraft:ender_eye',
                    C: 'minecraft:cactus',
                    F: 'minecraft:bone'
            }
    )
});
