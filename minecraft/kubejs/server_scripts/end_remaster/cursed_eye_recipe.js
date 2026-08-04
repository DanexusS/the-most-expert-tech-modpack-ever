ServerEvents.recipes(event => {

    event.shaped(
            Item.of('endrem:cursed_eye'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    C: 'minecraft:golden_apple',
                    D: 'minecraft:ender_eye',
                    E: 'ars_nouveau:bastion_pod',
                    B: 'minecraft:end_crystal',
                    A: 'minecraft:crying_obsidian'
            }
    )
});
