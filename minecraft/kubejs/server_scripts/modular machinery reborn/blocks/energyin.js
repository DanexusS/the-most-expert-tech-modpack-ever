ServerEvents.recipes(event => {

    event.shaped(
            Item.of('modular_machinery_reborn:energyinputhatch_normal'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    D: 'powah:energy_cell_basic',
                    B: 'modular_machinery_reborn:modularium',
                    C: 'modular_machinery_reborn:energyinputhatch_small'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:energyinputhatch_reinforced'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'modular_machinery_reborn:modularium',
                    C: 'modular_machinery_reborn:energyinputhatch_normal',
                    D: 'powah:energy_cell_hardened'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:energyinputhatch_big'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'modular_machinery_reborn:modularium',
                    D: 'powah:energy_cell_blazing',
                    C: 'modular_machinery_reborn:energyinputhatch_reinforced'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:energyinputhatch_huge'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'modular_machinery_reborn:modularium',
                    C: 'modular_machinery_reborn:energyinputhatch_big',
                    D: 'powah:energy_cell_niotic'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:energyinputhatch_ludicrous'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'modular_machinery_reborn:modularium',
                    D: 'powah:energy_cell_spirited',
                    C: 'modular_machinery_reborn:energyinputhatch_huge'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:energyinputhatch_ultimate'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    D: 'powah:energy_cell_nitro',
                    B: 'modular_machinery_reborn:modularium',
                    C: 'modular_machinery_reborn:energyinputhatch_ludicrous'
            }
    )
});
