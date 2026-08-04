ServerEvents.recipes(event => {
    event.remove({ output: 'minformax:pandora_box' })
    event.shaped(
            Item.of('minformax:pandora_box'),
            [
                    'ABA',
                    'CDC',
                    'ABA'
            ],
            {
                    A: 'justdirethings:coalblock_t3',
                    D: 'minformax:frozen_core',
                    B: 'projectexpansion:fading_matter_block',
                    C: 'mekanism_extras:infinite_induction_provider'
            }
    )
});
