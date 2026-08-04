ServerEvents.recipes(event => {

    event.shaped(
            Item.of('forbidden_arcanus:corrupted_arcane_crystal'),
            [
                    'AAA',
                    'ABA',
                    'AAA'
            ],
            {
                    B: 'draconicevolution:medium_chaos_frag',
                    A: 'forbidden_arcanus:arcane_crystal'
            }
    )
});
