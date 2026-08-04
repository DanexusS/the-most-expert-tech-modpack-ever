ServerEvents.recipes(event => {

    event.shaped(
            Item.of('pipez:infinity_upgrade'),
            [
                    'ABA',
                    'CDE',
                    'FFF'
            ],
            {
                    B: 'mekanism:pellet_antimatter',
                    A: 'pipez:universal_pipe',
                    E: 'modern_industrialization:stainless_steel_machine_casing_pipe',
                    F: 'pipez:ultimate_upgrade',
                    C: 'modern_industrialization:titanium_machine_casing_pipe',
                    D: 'mysticalagradditions:creative_essence'
            }
    )
});
