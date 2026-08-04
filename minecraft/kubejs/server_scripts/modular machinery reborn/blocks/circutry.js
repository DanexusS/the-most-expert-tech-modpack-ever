ServerEvents.recipes(event => {

    event.shaped(
            Item.of('modular_machinery_reborn:casing_circuitry'),
            [
                    'AAA',
                    'ABA',
                    'AAA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'ufo:dimensional_processor'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:casing_vent'),
            [
                    'ABA',
                    'BAB',
                    'ABA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'mekanismgenerators:turbine_vent'
            }
    )
});
