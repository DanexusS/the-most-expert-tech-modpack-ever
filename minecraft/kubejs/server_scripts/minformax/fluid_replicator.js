ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:fluid_replicator' })
    event.shaped(
            Item.of('minformax:fluid_replicator'),
            [
                    'ABA',
                    'CDC',
                    'ABA'
            ],
            {
                    D: 'advanced_ae:printed_quantum_processor',
                    A: 'actuallyadditions:enori_crystal_block',
                    C: 'mekanism:ultimate_fluid_tank',
                    B: 'alltheores:silver_block'
            }
    )
});
