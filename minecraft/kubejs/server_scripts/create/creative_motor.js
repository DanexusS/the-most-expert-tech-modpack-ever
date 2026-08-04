ServerEvents.recipes(event => {

    event.shaped(
            Item.of('create:creative_motor'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    C: 'modern_industrialization:large_motor',
                    B: 'tfmg:electric_motor',
                    E: 'createaddition:electric_motor',
                    D: 'mysticalagradditions:creative_essence',
                    A: 'create:precision_mechanism'
            }
    )
});
