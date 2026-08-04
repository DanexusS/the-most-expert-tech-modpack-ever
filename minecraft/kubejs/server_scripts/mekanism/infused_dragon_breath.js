ServerEvents.recipes(event => {
    event.custom({
        type: "mekanism:metallurgic_infusing",
        chemical_input: {
            amount: 200,
            tag: "mekanism_extras:shining"
        },
        item_input: {
            count: 1,
            item: "minecraft:dragon_breath"
        },
        output: {
            count: 1,
            id: "apothic_enchanting:infused_breath"
        },
        per_tick_usage: false
    })
})
