ServerEvents.recipes(event => {

    event.shaped(
            Item.of('powah:player_aerial_pearl'),
            [
                    'ABC',
                    'DED',
                    'CFA'
            ],
            {
                    A: 'ae2additions:me_wireless_transceiver',
                    C: 'alltheores:enderium_block',
                    F: 'appflux:insulating_resin',
                    E: 'powah:aerial_pearl',
                    B: 'create:precision_mechanism',
                    D: 'mysticalagradditions:insanium_essence'
            }
    )
});
