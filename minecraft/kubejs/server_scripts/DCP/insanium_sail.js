ServerEvents.recipes(event => {

    event.shaped(
            Item.of('kubejs:insanium_solar_sail_package'),
            [
                    'ABA',
                    'CDC',
                    'ABA'
            ],
            {
                    B: 'mysticalagradditions:insanium_ingot_block',
                    A: 'mysticalagradditions:insanium_block',
                    C: 'mysticalagradditions:insanium_gemstone_block',
                    D: 'dysoncubeproject:solar_sail_package'
            }
    )
    event.shaped(
            Item.of('kubejs:insanium_beam_package'),
            [
                    'ABA',
                    'CDC',
                    'ABA'
            ],
            {
                    D: 'dysoncubeproject:beam_package',
                    C: 'mysticalagradditions:insanium_ingot_block',
                    A: 'mysticalagradditions:insanium_block',
                    B: 'mysticalagradditions:insanium_gemstone_block'
            }
    )
});
