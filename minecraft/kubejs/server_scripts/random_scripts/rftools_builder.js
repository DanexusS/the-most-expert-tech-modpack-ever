ServerEvents.recipes(event => {
  event.remove({ output: 'rftoolsbuilder:builder' })
    event.shaped(
            Item.of('rftoolsbuilder:builder'),
            [
                    'ABC',
                    'DED',
                    'FDG'
            ],
            {
                    G: 'xycraft_override:polished_blackstone_bricks_light',
                    A: 'xycraft_override:polished_blackstone_bricks_green',
                    B: 'dimensionalpocketsii:dimensional_pearl',
                    D: 'allthemodium:vibranium_nugget',
                    C: 'xycraft_override:polished_blackstone_bricks_red',
                    E: 'rftoolsbase:machine_frame',
                    F: 'xycraft_override:polished_blackstone_bricks_blue'
            }
    )
});
