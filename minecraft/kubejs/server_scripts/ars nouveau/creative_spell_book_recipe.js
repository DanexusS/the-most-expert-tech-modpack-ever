ServerEvents.recipes(event => {

    event.shaped(
            Item.of('ars_nouveau:creative_spell_book'),
            [
                    'ABB',
                    'BCD',
                    'EFG'
            ],
            {
                    F: 'forbidden_arcanus:eternal_stella',
                    C: 'fragmentumneoforge:manuscriptvoid',
                    D: 'projecte:klein_star_omega',
                    G: 'mysticalagradditions:creative_essence',
                    A: 'allthearcanistgear:unobtainium_spell_book',
                    E: 'artifacts:chorus_totem',
                    B: 'avaritia:endest_pearl'
            }
    )
});
