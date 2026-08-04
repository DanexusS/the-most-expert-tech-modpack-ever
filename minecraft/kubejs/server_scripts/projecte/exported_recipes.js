ServerEvents.recipes(event => {
  event.remove({ output: 'projecte:condenser_mk1' })
    event.shaped(
            Item.of('projecte:condenser_mk1'),
            [
                    'ABA',
                    'BCB',
                    'ADA'
            ],
            {
                    D: 'projecte:dark_matter',
                    B: 'minecraft:diamond',
                    C: 'projecte:alchemical_chest',
                    A: 'minecraft:obsidian'
            }
    )
});
