ServerEvents.recipes(event => {
  event.remove({ output: 'projecte:repair_talisman' })
  event.shaped('projecte:repair_talisman', [
    'ABC',
    'DEF',
    'CBA'
  ], {
    A: 'projecte:high_covalence_dust',
    B: 'projecte:medium_covalence_dust',
    C: 'projecte:low_covalence_dust',
    D: 'enderio:skeletal_contractor',
    E: 'extendedcrafting:luminessence',
    F: 'tempad:time_steel'
  })
})
