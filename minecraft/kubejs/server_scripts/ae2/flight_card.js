ServerEvents.recipes(event => {
  event.remove({ output: 'advanced_ae:flight_card' })
  event.shaped('advanced_ae:flight_card', [
    'RER',
    'CMC',
    'RBR'
  ], {
    M: 'advanced_ae:quantum_upgrade_base',
    E: 'dimensionalpocketsii:dimensional_elytraplate',
    B: 'reliquary:angelic_feather',
    C: 'reliquary:phoenix_down',
    R: 'advanced_ae:quantum_alloy_plate'
  })
})
