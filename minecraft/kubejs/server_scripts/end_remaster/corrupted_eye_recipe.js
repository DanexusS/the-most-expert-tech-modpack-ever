ServerEvents.recipes(event => {

    event.shaped(
            Item.of('endrem:corrupted_eye'),
            [
                    'ABA',
                    'CDC',
                    'ABA'
            ],
            {
                    B: 'forbidden_arcanus:corrupti_dust',
                    D: 'minecraft:ender_eye',
                    C: 'actuallyadditions:empowered_void_crystal',
                    A: 'forbidden_arcanus:arcane_polished_darkstone'
            }
    )
});
