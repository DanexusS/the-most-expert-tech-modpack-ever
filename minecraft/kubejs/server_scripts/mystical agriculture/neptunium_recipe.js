ServerEvents.recipes(event => {

    event.shaped(
            Item.of('aquaculture:neptunium_ingot'),
            [
                    'AAA',
                    'A A',
                    'AAA'
            ],
            {
                    A: 'mysticalagriculture:neptunium_essence'
            }
    )
});
