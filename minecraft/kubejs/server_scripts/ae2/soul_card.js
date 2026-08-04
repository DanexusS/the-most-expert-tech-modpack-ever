ServerEvents.recipes(event => {
  event.remove({ output: 'mesoulcard:soul_card' })
    event.shaped(
            Item.of('mesoulcard:soul_card'),
            [
                    'ABA',
                    'CDE',
                    'AFA'
            ],
            {
                    C: 'industrialforegoingsouls:soul_surge',
                    F: 'appliedsoul:soul_storage_cell_256k',
                    B: 'industrialforegoingsouls:soul_network_pipe',
                    D: 'advanced_ae:quantum_upgrade_base',
                    E: 'appliedsoul:ender_star',
                    A: 'allthecompressed:iron_block_2x'
            }
    )
});
