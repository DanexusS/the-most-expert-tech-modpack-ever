ServerEvents.recipes(event => {
event.remove({ output: 'modular_machinery_reborn:casing_plain' })
    event.shaped(
            Item.of('modular_machinery_reborn:casing_plain', 8),
            [
                    ' A ',
                    'ABA',
                    ' A '
            ],
            {
                    B: 'minecraft:redstone_block',
                    A: 'modular_machinery_reborn:modularium'
            }
    )
});
