ServerEvents.recipes(event => {
    event.remove('gag:time_sand_pouch')
    event.shaped(
            Item.of('gag:time_sand_pouch'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    C: 'extendedae:entro_crystal',
                    D: 'sophisticatedbackpacks:diamond_backpack',
                    E: 'apotheosis:uncommon_material',
                    B: 'minecraft:clock',
                    A: 'tempad:time_steel'
            }
    )
});
