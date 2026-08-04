ServerEvents.recipes(event => {

    event.shaped(
            Item.of('stellaris:moon_globe'),
            [
                    'AA ',
                    'AB ',
                    'AA '
            ],
            {
                    B: 'stellaris:moon_stone',
                    A: 'stellaris:desh_ingot'
            }
    )
});
