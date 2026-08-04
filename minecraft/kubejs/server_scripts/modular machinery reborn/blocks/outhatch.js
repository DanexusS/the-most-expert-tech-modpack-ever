ServerEvents.recipes(event => {

    event.shaped(
            Item.of('modular_machinery_reborn:outputbus_normal'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'minecraft:hopper',
                    C: 'modular_machinery_reborn:modularium',
                    D: 'modular_machinery_reborn:outputbus_small',
                    E: 'minecraft:chest'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:outputbus_reinforced'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'minecraft:hopper',
                    C: 'modular_machinery_reborn:modularium',
                    D: 'modular_machinery_reborn:outputbus_normal',
                    E: 'draconicevolution:draconium_chest'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:outputbus_big'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'minecraft:hopper',
                    C: 'modular_machinery_reborn:modularium',
                    E: 'projecte:alchemical_chest',
                    D: 'modular_machinery_reborn:outputbus_reinforced'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:outputbus_huge'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'minecraft:hopper',
                    C: 'modular_machinery_reborn:modularium',
                    D: 'modular_machinery_reborn:outputbus_big',
                    E: 'mekanism:personal_chest'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:outputbus_ludicrous'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'minecraft:hopper',
                    C: 'modular_machinery_reborn:modularium',
                    D: 'modular_machinery_reborn:outputbus_huge',
                    E: 'avaritia:compressed_chest'
            }
    )
});
