ServerEvents.recipes(event => {

    event.shaped(
            Item.of('endrem:cold_eye'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    A: 'minecraft:blue_ice',
                    E: 'reliquary:frozen_core',
                    B: 'powah:charged_snowball',
                    D: 'minecraft:ender_eye',
                    C: 'powah:dry_ice'
            }
    )
});
