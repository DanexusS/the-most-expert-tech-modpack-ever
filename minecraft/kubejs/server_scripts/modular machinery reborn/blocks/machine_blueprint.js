ServerEvents.recipes(event => {

    event.shaped(
            Item.of('modular_machinery_reborn:blueprint'),
            [
                    'ABA',
                    'BCB',
                    'ABA'
            ],
            {
                    B: 'createaddition:diamond_grit_sandpaper',
                    C: 'modular_machinery_reborn:modularium',
                    A: 'silentgear:blueprint_paper'
            }
    )
});
