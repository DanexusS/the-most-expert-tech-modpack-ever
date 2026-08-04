ServerEvents.recipes(event => {

    event.shaped(
            Item.of('modular_machinery_reborn:fluidinputhatch_normal'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    C: 'modular_machinery_reborn:fluidinputhatch_small',
                    B: 'modular_machinery_reborn:modularium',
                    D: 'mekanism:basic_fluid_tank'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:fluidinputhatch_reinforced'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'modular_machinery_reborn:modularium',
                    C: 'modular_machinery_reborn:fluidinputhatch_normal',
                    D: 'modern_industrialization:iron_tank'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:fluidinputhatch_big'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'modular_machinery_reborn:modularium',
                    D: 'modern_industrialization:bronze_tank',
                    C: 'modular_machinery_reborn:fluidinputhatch_reinforced'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:fluidinputhatch_huge'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'modular_machinery_reborn:modularium',
                    C: 'modular_machinery_reborn:fluidinputhatch_big',
                    D: 'modern_industrialization:steel_tank'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:fluidinputhatch_ludicrous'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'modular_machinery_reborn:modularium',
                    D: 'mekanism:advanced_fluid_tank',
                    C: 'modular_machinery_reborn:fluidinputhatch_huge'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:fluidinputhatch_vacuum'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'modular_machinery_reborn:modularium',
                    C: 'modular_machinery_reborn:fluidinputhatch_ludicrous',
                    D: 'mekanism:elite_fluid_tank'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:experienceinputhatch_vacuum'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    B: 'productivebees:configurable_honeycomb',
                    D: 'mysticalagriculture:experience_seeds',
                    A: 'create:experience_block',
                    C: 'modern_industrialization:large_tank_hatch'
            }
    )
});
