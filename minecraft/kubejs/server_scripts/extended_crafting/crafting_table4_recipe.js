ServerEvents.recipes(event => {
  event.remove({ output: 'extendedcrafting:ultimate_table' })
  event.shaped('extendedcrafting:ultimate_table', [
    'CUC',
    'EBE',
    'SHS'
  ], {
    C: 'extendedcrafting:ultimate_component',
    E: 'extendedcrafting:elite_table',
    U: 'extendedcrafting:ultimate_catalyst',
    B: 'allthecompressed:emerald_block_1x',
    S: 'extendedcrafting:black_iron_slate',
    H: 'avaritia:endest_pearl'
  })
})
