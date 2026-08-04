ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:compressing_upgrade' })
    event.remove({ output: 'minformax:frozen_crystal' })
    event.shaped(
            Item.of('minformax:compressing_upgrade'),
            [
                    'ABC',
                    'BDB',
                    'EBF'
            ],
            {
                    A: 'avaritia:densest_neutron_compressor',
                    B: 'avaritia:end_crafting_table',
                    E: 'extendedcrafting:compressor',
                    C: 'pneumaticcraft:electrostatic_compressor',
                    D: 'extendedcrafting:crafting_core',
                    F: 'modern_industrialization:electric_compressor'
            }
    )
    event.shaped(
            Item.of('minformax:frozen_crystal'),
            [
                    ' AB',
                    'ACA',
                    'BA '
            ],
            {
                    C: 'irons_spellbooks:ice_upgrade_orb',
                    A: 'silentgear:azure_electrum_ingot',
                    B: 'allthecompressed:blue_ice_3x'
            }
    )
});
