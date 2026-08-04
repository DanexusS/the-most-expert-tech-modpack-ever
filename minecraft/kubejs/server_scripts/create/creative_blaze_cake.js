ServerEvents.recipes(event => {

    event.shaped(
            Item.of('create:creative_blaze_cake'),
            [
                    'ABA',
                    'CDC',
                    'EBE'
            ],
            {
                    B: 'mysticalagradditions:creative_essence',
                    C: 'create:precision_mechanism',
                    D: 'create:blaze_cake_base',
                    E: 'allthemodium:soul_lava_bucket',
                    A: 'create:blaze_cake'
            }
    )
});
