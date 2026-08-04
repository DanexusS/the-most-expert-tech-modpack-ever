ServerEvents.recipes(event => {
    event.custom({
        type: "mekanism:metallurgic_infusing",
        chemical_input: {
            amount: 20000,
            tag: "mekanism:carbon"
        },
        item_input: {
            count: 1,
            item: "justdirethings:gooblock_tier4"
        },
        output: {
            count: 1,
            id: "create:shadow_steel_casing"
        },
        per_tick_usage: false
    })
})
