ServerEvents.recipes(event => {

    event.shaped(
            Item.of('tfmg:lead_sheet'),
            [
                    'AB ',
                    'B  ',
                    '   '
            ],
            {
                    A: '#alltheores:ore_hammers',
                    B: 'immersiveengineering:ingot_lead'
            }
    )
    event.shaped(
            Item.of('tfmg:nickel_sheet'),
            [
                    'AB ',
                    'B  ',
                    '   '
            ],
            {
                    A: '#alltheores:ore_hammers',
                    B: 'immersiveengineering:ingot_nickel'
            }
    )
});
