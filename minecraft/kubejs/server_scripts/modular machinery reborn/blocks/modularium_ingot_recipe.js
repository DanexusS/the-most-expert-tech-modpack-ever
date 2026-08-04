ServerEvents.recipes(event => {
event.remove({ output: 'modular_machinery_reborn:modularium' })
    event.shaped(
            Item.of('modular_machinery_reborn:modularium'),
            [
                    'ABA',
                    'CDC',
                    'DED'
            ],
            {
                    C: 'mysticalagradditions:insanium_ingot',
                    E: '#c:dusts/bronze',
                    D: 'draconicevolution:awakened_draconium_dust',
                    B: 'bigreactors:insanite_ingot',
                    A: 'allthemodium:unobtainium_ingot'
            }
    )
});
