ServerEvents.recipes(event => {

    event.shaped(
            Item.of('sophisticatedstorage:stack_upgrade_omega_tier', 2),
            [
                    'ABA',
                    'CDC',
                    'ABA'
            ],
            {
                    D: 'sophisticatedstorage:stack_upgrade_tier_5',
                    C: 'allthemodium:unobtainium_ingot',
                    A: 'mysticalagriculture:supremium_ingot',
                    B: 'bigreactors:inanite_ingot'
            }
    )
});
