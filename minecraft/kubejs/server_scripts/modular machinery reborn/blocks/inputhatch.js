ServerEvents.recipes(event => {

    event.shaped(
            Item.of('modular_machinery_reborn:inputbus_normal'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'minecraft:hopper',
                    C: 'modular_machinery_reborn:modularium',
                    D: 'modular_machinery_reborn:inputbus_small',
                    E: 'minecraft:chest'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:inputbus_reinforced'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'minecraft:hopper',
                    C: 'modular_machinery_reborn:modularium',
                    D: 'modular_machinery_reborn:inputbus_normal',
                    E: 'draconicevolution:draconium_chest'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:inputbus_big'),
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
                    D: 'modular_machinery_reborn:inputbus_reinforced'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:inputbus_huge'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'minecraft:hopper',
                    C: 'modular_machinery_reborn:modularium',
                    D: 'modular_machinery_reborn:inputbus_big',
                    E: 'mekanism:personal_chest'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:inputbus_ludicrous'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'minecraft:hopper',
                    C: 'modular_machinery_reborn:modularium',
                    D: 'modular_machinery_reborn:inputbus_huge',
                    E: 'avaritia:compressed_chest'
            }
    )
});
