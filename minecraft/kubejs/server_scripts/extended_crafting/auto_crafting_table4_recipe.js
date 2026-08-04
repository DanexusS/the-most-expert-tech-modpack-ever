ServerEvents.recipes(event => {
  event.remove({ output: 'extendedcrafting:ultimate_auto_table' })
  event.shaped('extendedcrafting:ultimate_auto_table', [
    'CSC',
    'EBE',
    'CHC'
  ], {
    C: 'extendedcrafting:black_iron_ingot',
    E: 'extendedcrafting:enhanced_redstone_component',
    B: 'extendedcrafting:ultimate_table',
    S: 'extendedcrafting:crystaltine_component',
    H: 'avaritia:endest_pearl'
  })
})
