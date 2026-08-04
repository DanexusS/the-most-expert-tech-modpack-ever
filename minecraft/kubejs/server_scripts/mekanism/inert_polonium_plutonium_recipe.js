ServerEvents.recipes(event => {

    event.shaped(
            Item.of('kubejs:weak_polonium'),
            [
                    'AAA',
                    'ABA',
                    'AAA'
            ],
            {
                    B: 'mekanism:hdpe_pellet',
                    A: 'mysticalagriculture:polonium_essence'
            }
    )
    event.shaped(
            Item.of('kubejs:weak_plutonium'),
            [
                    'AAA',
                    'ABA',
                    'AAA'
            ],
            {
                    A: 'mysticalagriculture:plutonium_essence',
                    B: 'mekanism:hdpe_pellet'
            }
    )
});
