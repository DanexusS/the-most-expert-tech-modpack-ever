ServerEvents.recipes(event => {
    event.custom({
        type: "ufo:stellar_simulation",
        simulation_name: "Data Crystal Synthesis",

        item_inputs: [
            { ingredient: { item: "kubejs:information_disk" }, amount: 5 },
            { ingredient: { item: "ufo:quantum_anomaly" }, amount: 64 },
            { ingredient: { item: "ufo:thermal_resistor_plating" }, amount: 64 },
            { ingredient: { item: "ufo:nuclear_star" }, amount: 64 },
            { ingredient: { item: "ufo:dimensional_catalyst" }, amount: 1 },
            { ingredient: { item: "avaritia:infinity_ingot" }, amount: 64 },
            { ingredient: { item: "modern_industrialization:singularity" }, amount: 64 },
            { ingredient: { item: "projectexpansion:final_star" }, amount: 1 },
            { ingredient: { item: "draconicevolution:reactor_core" }, amount: 64 }
        ],

        fluid_inputs: [
            { ingredient: { fluid: "ufo:transcending_matter" }, amount: 3140000 },
            { ingredient: { fluid: "ufo:raw_star_matter_plasma" }, amount: 2500000 },
            { ingredient: { fluid: "ufo:source_stable_coolant" }, amount: 1600000 }
        ],

        item_outputs: [
            { "#": 1, "#t": "ae2:i", id: "fragmentumneoforge:datacrystal" }
        ],

        fluid_outputs: [],

        energy: 20000000000,
        time: 1728000,
        cooling_level: 3,
        field_tier: 3,
        fuel_fluid: "mekanism:hydrogen",
        fuel_amount: 10000000,
        coolant_fluid: "ufo:source_gelid_cryotheum",
        coolant_amount: 20000000
    })
})