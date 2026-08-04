ServerEvents.recipes(event => {
    event.shaped(
            Item.of('stellaris:mercury_solerium_ore', 2),
            [
                    'AAA',
                    'CBC',
                    'AAA'
            ],
            {
                    A: 'stellaris:mercury_stone',
                    C: 'projectexpansion:yellow_matter',
                    B: 'avaritia:blaze_cube_block'
            }
    )
});
