ServerEvents.recipes(event => {
  event.remove({ output: 'justdirethings:time_wand' })
    event.shaped(
            Item.of('justdirethings:time_wand'),
            [
                    ' AB',
                    ' CA',
                    'C  '
            ],
            {
                    B: 'justdirethings:time_crystal',
                    C: 'avaritia:neutron_ingot',
                    A: 'mysticalagriculture:awakened_supremium_ingot'
            }
    )
});
