ServerEvents.recipes(event => {
  event.remove({ output: 'justdynathings:paradox_mixer' })
    event.shaped(
            Item.of('justdynathings:paradox_mixer'),
            [
                    'ABA',
                    'BCB',
                    'ABA'
            ],
            {
                    B: 'justdirethings:eclipsealloy_ingot',
                    C: 'modern_industrialization:electric_mixer',
                    A: 'justdirethings:portal_fluid_bucket'
            }
    )
});
