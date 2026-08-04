ServerEvents.recipes(event => {
  event.remove({ output: 'quarryplus:mover' })
    event.shaped(
            Item.of('quarryplus:adv_quarry'),
            [
                    'ABA',
                    'CDC',
                    'EBE'
            ],
            {
                    B: 'avaritia:neutron_gear',
                    D: 'modern_industrialization:electric_quarry',
                    A: 'allthecompressed:iron_block_4x',
                    E: 'quarryplus:chunk_marker',
                    C: 'justdirethings:eclipsealloy_pickaxe'
            }
    )
});
