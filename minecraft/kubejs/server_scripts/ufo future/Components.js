ServerEvents.recipes(event => {
  event.remove({ id: 'ufo:dma/component/phase_shift' })
  event.remove({ id: 'ufo:universal/qmf/bulk/component/phase_shift' })
  event.remove({ id: 'ufo:dma/component/hyper_dense_component_matrix' })
  event.remove({ id: 'ufo:universal/qmf/bulk/component/hyper_dense_component_matrix' })
  event.remove({ id: 'ufo:universal/qmf/tesseract_component_matrix_batch' })
  event.remove({ id: 'ufo:universal/qmf/event_horizon_component_matrix_batch' })
  event.remove({ id: 'ufo:universal/qmf/cosmic_string_component_matrix_batch' })
  event.custom({
    type: 'ufo:dimensional_assembly',
    item_inputs: [
      {ingredient: { item: 'ufo:dimensional_processor' }, amount: 8},
      {ingredient: { item: 'ae2:cell_component_256k' }, amount: 64},
      {ingredient: { item: 'ae2:quartz_vibrant_glass' }, amount: 8},
      {ingredient: { item: 'minecraft:nether_star' }, amount: 8},
    ],
    fluid_inputs: [
      {ingredient: { fluid: 'ufo:source_liquid_starlight_fluid' }, amount: 1000}
    ],
    item_outputs: [
      { '#': 1, '#t': 'ae2:i', id: 'ufo:phase_shift_component_matrix' }
    ],
    fluid_outputs: [],
    energy: 1200000,
    time: 600
  }).id('kubejs:custom_phase_shift')

  event.custom({
    type: 'ufo:dimensional_assembly',
    item_inputs: [
      {ingredient: { item: 'ufo:phase_shift_component_matrix' }, amount: 6},
      {ingredient: { item: 'ufo:white_dwarf_matter' }, amount: 8},
      {ingredient: { item: 'ufo:dimensional_processor' }, amount: 4}
    ],
    fluid_inputs: [
      {ingredient: { fluid: 'ufo:source_primordial_matter_fluid' }, amount: 2000}
    ],
    item_outputs: [
      { '#': 1, '#t': 'ae2:i', id: 'ufo:hyper_dense_component_matrix' }
    ],
    fluid_outputs: [],
    energy: 4000000,
    time: 1200
  }).id('kubejs:custom_hyper_dense')

  event.custom({
    type: 'ufo:universal_multiblock',
    machine: 'qmf',
    recipe_name: 'kubejs/qmf/tesseract_component_matrix',
    item_inputs: [
      {ingredient: { item: 'ufo:hyper_dense_component_matrix' }, amount: 6},
      {ingredient: { item: 'ufo:neutron_star_matter' }, amount: 32},
      {ingredient: { item: 'ufo:dimensional_processor' }, amount: 128}
    ],
    fluid_inputs: [
      {fluid: { id: 'ufo:source_spatial_fluid', amount: 1 }, amount: 32000}
    ],
    item_output: {
      id: 'ufo:tesseract_component_matrix',
      count: 1
    },
    energy: 240000000,
    time: 2400,
    required_tier: 1
  }).id('kubejs:qmf_tesseract_component_matrix')

  event.custom({
    type: 'ufo:universal_multiblock',
    machine: 'qmf',
    recipe_name: 'kubejs/qmf/event_horizon_component_matrix',
    item_inputs: [
      {ingredient: { item: 'ufo:tesseract_component_matrix' }, amount: 6},
      {ingredient: { item: 'ufo:pulsar_matter' }, amount: 32},
      {ingredient: { item: 'ufo:dimensional_processor' }, amount: 256},
      {ingredient: { item: 'ufo:quantum_anomaly' }, amount: 32}
    ],
    fluid_inputs: [
      {fluid: { id: 'ufo:source_spatial_fluid', amount: 1 }, amount: 64000}
    ],
    item_output: {
      id: 'ufo:event_horizon_component_matrix',
      count: 1
    },
    energy: 480000000,
    time: 4800,
    required_tier: 2
  }).id('kubejs:qmf_event_horizon_component_matrix')

  event.custom({
    type: 'ufo:universal_multiblock',
    machine: 'qmf',
    recipe_name: 'kubejs/qmf/cosmic_string_component_matrix',
    item_inputs: [
      {ingredient: { item: 'ufo:event_horizon_component_matrix' }, amount: 6},
      {ingredient: { item: 'ufo:dark_matter' }, amount: 16},
      {ingredient: { item: 'ufo:charged_enriched_neutronium_sphere' }, amount: 16},
      {ingredient: { item: 'ufo:dimensional_processor' }, amount: 512}
    ],
    fluid_inputs: [
      {fluid: { id: 'ufo:transcending_matter', amount: 1 }, amount: 128000}
    ],
    item_output: {
      id: 'ufo:cosmic_string_component_matrix',
      count: 1
    },
    energy: 1200000000,
    time: 19200,
    required_tier: 2
  }).id('kubejs:qmf_cosmic_string_component_matrix')
})
