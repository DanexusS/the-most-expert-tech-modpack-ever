ServerEvents.recipes(event => {

    event.shaped(
            Item.of('create:refined_radiance_casing'),
            [
                    'AAA',
                    'ABA',
                    'AAA'
            ],
            {
                    B: 'create:shadow_steel_casing',
                    A: 'mekanism_extras:alloy_spectrum'
            }
    )
});
