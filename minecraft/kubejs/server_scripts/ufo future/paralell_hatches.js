ServerEvents.recipes(event => {

    event.shaped(
            Item.of('modular_machinery_reborn:parallel_hatch_advanced'),
            [
                    'ABC',
                    'BDB',
                    'CBA'
            ],
            {
                    B: 'modular_machinery_reborn:casing_plain',
                    A: 'mekanism_extras:absolute_control_circuit',
                    C: 'ufo:phase_shift_component_matrix',
                    D: 'modular_machinery_reborn:parallel_hatch_medium'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:parallel_hatch_ultimate'),
            [
                    'ABA',
                    'CDC',
                    'ABA'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'minformax:ultimate_ingot',
                    C: 'oritech:machine_core_7',
                    D: 'modular_machinery_reborn:parallel_hatch_advanced'
            }
    )
    event.shaped(
            Item.of('modular_machinery_reborn:parallel_hatch_max'),
            [
                    'ABC',
                    'DED',
                    'CBA'
            ],
            {
                    C: 'modern_industrialization:quantum_machine_casing',
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'mekanism_extras:supreme_control_circuit',
                    E: 'modular_machinery_reborn:parallel_hatch_ultimate',
                    D: 'ufo:quantum_hyper_mechanical_casing'
            }
    )
});
