ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:speed_upgrade_tier1' })
    event.remove({ output: 'minformax:processing_upgrade_tier1' })
    event.remove({ output: 'minformax:fortune_upgrade_tier1' })
    event.remove({ output: 'minformax:extra_drop_upgrade_tier1' })
    event.shaped(
            Item.of('minformax:speed_upgrade_tier1'),
            [
                    'ABA',
                    'BCB',
                    'ABA'
            ],
            {
                    C: 'forbidden_arcanus:deorum_glass_pane',
                    A: 'minformax:quantum_ingot',
                    B: 'bigreactors:inanite_ingot'
            }
    )
    event.shaped(
            Item.of('minformax:processing_upgrade_tier1'),
            [
                    'ABA',
                    'CDC',
                    'ABA'
            ],
            {
                    D: 'forbidden_arcanus:deorum_glass_pane',
                    C: 'extendedcrafting:redstone_ingot',
                    B: 'avaritia:crystal_matrix_ingot',
                    A: 'minformax:quantum_ingot'
            }
    )
    event.shaped(
            Item.of('minformax:fortune_upgrade_tier1'),
            [
                    'ABA',
                    'CDC',
                    'ABA'
            ],
            {
                    C: 'mekanism:alloy_atomic',
                    D: 'forbidden_arcanus:deorum_glass_pane',
                    B: 'powah:crystal_niotic',
                    A: 'minformax:quantum_ingot'
            }
    )
    event.shaped(
            Item.of('minformax:extra_drop_upgrade_tier1'),
            [
                    'ABA',
                    'BCD',
                    'ADA'
            ],
            {
                    D: 'mekanism:alloy_atomic',
                    C: 'forbidden_arcanus:deorum_glass_pane',
                    A: 'minformax:quantum_ingot',
                    B: 'oritech:overcharged_crystal'
            }
    )
});
