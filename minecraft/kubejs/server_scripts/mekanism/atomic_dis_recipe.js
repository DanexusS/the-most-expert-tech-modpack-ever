ServerEvents.recipes(event => {
  event.remove({ output: 'mekanism:atomic_disassembler' })

    event.shaped(
            Item.of('mekanism:atomic_disassembler'),
            [
                    'ABA',
                    'ACA',
                    ' D '
            ],
            {
                    C: 'mekanism:alloy_atomic',
                    D: 'advancednetherite:netherite_diamond_ingot',
                    B: 'mekanism:basic_induction_cell',
                    A: 'allthemodium:allthemodium_ingot'
            }
    )
});
