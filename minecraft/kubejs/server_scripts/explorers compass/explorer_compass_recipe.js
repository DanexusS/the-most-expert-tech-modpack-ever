ServerEvents.recipes(event => {
  event.remove({ output: 'explorerscompass:explorerscompass' })
    event.shaped(
            Item.of('explorerscompass:explorerscompass'),
            [
                    'ABA',
                    'CDC',
                    'AEA'
            ],
            {
                    A: 'mahoutsukai:powdered_eye',
                    C: 'minecraft:netherite_ingot',
                    E: 'cognition:primordial_assembly',
                    D: 'naturescompass:naturescompass',
                    B: 'minecraft:cobweb'
            }
    )
});
