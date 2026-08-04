ServerEvents.recipes(event => {

    event.shaped(
            Item.of('endrem:magical_eye'),
            [
                    'ABA',
                    'CDC',
                    'ECE'
            ],
            {
                    B: 'minecraft:totem_of_undying',
                    D: 'minecraft:ender_eye',
                    E: 'ars_nouveau:conjuration_essence',
                    A: 'mahoutsukai:powdered_diamond',
                    C: '#c:gems/sapphire'
            }
    )
});
