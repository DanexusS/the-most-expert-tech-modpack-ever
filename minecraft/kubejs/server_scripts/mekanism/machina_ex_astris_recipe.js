ServerEvents.recipes(event => {
    event.custom({
        type: "mekanism:metallurgic_infusing",
        chemical_input: {
            amount: 2000,
            tag: "mekanism_extras:spectrum"
        },
        item_input: {
            count: 1,
            item: "kubejs:multi_quantum_processor"
        },
        output: {
            count: 1,
            id: "fragmentumneoforge:machinaastris"
        },
        per_tick_usage: false
    })
})
