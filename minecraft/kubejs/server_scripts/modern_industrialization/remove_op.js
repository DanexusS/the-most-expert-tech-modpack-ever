ServerEvents.recipes(event => {
  let itensRemover = [
    'modern_industrialization:quantum_sword',
    'modern_industrialization:quantum_helmet',
    'modern_industrialization:quantum_chestplate',
    'modern_industrialization:quantum_leggings',
    'modern_industrialization:quantum_boots',
    'extended_industrialization:nano_quantum_saber',
    'extended_industrialization:nano_quantum_helmet',
    'extended_industrialization:nano_quantum_chestplate',
    'extended_industrialization:nano_quantum_leggings',
    'extended_industrialization:nano_quantum_boots'
  ]

  itensRemover.forEach(item => {
    event.remove({ output: item })
  })
})
