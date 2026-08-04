ServerEvents.recipes(event => {

    event.shaped(
            Item.of('forbidden_arcanus:xpetrified_orb'),
            [
                    'AAA',
                    'ABA',
                    'AAA'
            ],
            {
                    B: 'minecraft:stone',
                    A: 'mysticalagriculture:experience_essence'
            }
    )
});
