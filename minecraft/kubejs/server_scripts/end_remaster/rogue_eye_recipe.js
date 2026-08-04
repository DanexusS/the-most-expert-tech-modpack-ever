ServerEvents.recipes(event => {

    event.shaped(
            Item.of('endrem:rogue_eye'),
            [
                    'ABA',
                    'CDE',
                    'AFA'
            ],
            {
                    A: 'minecraft:emerald_block',
                    D: 'minecraft:ender_eye',
                    F: 'minecraft:slime_ball',
                    C: 'minecraft:melon',
                    E: 'minecraft:cocoa_beans',
                    B: 'minecraft:turtle_scute'
            }
    )
});
