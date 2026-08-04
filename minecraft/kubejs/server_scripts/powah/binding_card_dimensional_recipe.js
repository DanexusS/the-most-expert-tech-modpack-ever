ServerEvents.recipes(event => {

    event.shaped(
            Item.of('powah:binding_card_dim'),
            [
                    'ABC',
                    'BDB',
                    'CBA'
            ],
            {
                    C: 'ae2additions:me_wireless_transceiver',
                    A: 'alltheores:enderium_block',
                    B: 'appflux:insulating_resin',
                    D: 'powah:blank_card'
            }
    )
});
