ItemEvents.modification(event => {
  event.modify('ufo:white_dwarf_matter', item => {
    item.maxStackSize = 64
  })

  event.modify('ufo:neutron_star_matter', item => {
    item.maxStackSize = 64
  })

  event.modify('ufo:pulsar_matter', item => {
    item.maxStackSize = 64
  })

  event.modify('ufo:dark_matter', item => {
    item.maxStackSize = 64
  })

  event.modify('ufo:quantum_anomaly', item => {
    item.maxStackSize = 64
  })

  event.modify('ufo:nuclear_star', item => {
    item.maxStackSize = 64
  })
})