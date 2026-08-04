ServerEvents.recipes(event => {

    event.shaped(
            Item.of('kubejs:neutronium_solar_sail_package'),
            [
                    'ABA',
                    'CDC',
                    'ABA'
            ],
            {
                    C: 'avaritia:neutron_ingot',
                    B: 'avaritia:neutron_gear',
                    D: 'dysoncubeproject:solar_sail_package',
                    A: 'avaritia:neutron'
            }
    )
    event.shaped(
            Item.of('kubejs:neutronium_beam_package'),
            [
                    'ABA',
                    'CDC',
                    'ABA'
            ],
            {
                    D: 'dysoncubeproject:beam_package',
                    B: 'avaritia:neutron_ingot',
                    C: 'avaritia:neutron_gear',
                    A: 'avaritia:neutron'
            }
    )
    event.shapeless(
            Item.of('ae2:silicon', 6),
            [
                    'mysticalagriculture:silicon_essence',
                    'mysticalagriculture:silicon_essence',
                    'mysticalagriculture:silicon_essence'
            ]
    )
    event.shapeless(
            Item.of('oritech:still_oil_bucket'),
            [
                    'pneumaticcraft:oil_bucket'
            ]
    )
});
