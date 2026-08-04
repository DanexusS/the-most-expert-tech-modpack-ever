ServerEvents.recipes(event => {

    event.shaped(
            Item.of('modular_machinery_reborn:parallel_hatch_basic'),
            [
                    'ABA',
                    'DEC',
                    'FGF'
            ],
            {
                    A: 'modular_machinery_reborn:casing_plain',
                    B: 'advanced_ae:quantum_core',
                    C: 'oritech:processing_unit',
                    D: 'modern_industrialization:analog_circuit',
                    E: 'ae2:controller',
                    F: 'modern_industrialization:electronic_circuit_board',
                    G: 'mekanism_extras:supreme_control_circuit'
            }      
    )
  })