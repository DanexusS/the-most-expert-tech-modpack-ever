ServerEvents.recipes(event => {

    event.shaped(
            Item.of('allthemodium:alloy_pick'),
            [
                    'AAA',
                    ' B ',
                    ' B '
            ],
            {
                    A: 'kubejs:allthemodium_alloy',
                    B: 'allthemodium:allthemodium_rod'
            }
    )
});
