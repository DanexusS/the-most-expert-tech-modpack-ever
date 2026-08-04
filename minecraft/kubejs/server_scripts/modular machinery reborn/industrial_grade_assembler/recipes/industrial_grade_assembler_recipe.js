ServerEvents.recipes(event => {
  const time = 36000
  const machine_id = "mmr:industrial_grade_assembler"

  event.recipes.modular_machinery_reborn.machine_recipe(machine_id, time)
    .requireItem("oritech:machine_ultimate_addon", 10, 10)
    .requireItem("createaddition:alternator", 30, 10)
    .requireItem("createaddition:electric_motor", 50, 10)
    .requireItem("actuallyadditions:advanced_coil", 70, 10)
    .requireItem("oritech:particle_collector_block", 90, 10)

    .requireItem("industrialforegoing:machine_frame_supreme", 10, 30)
    .requireItem("create:precision_mechanism", 30, 30)
    .requireItem("create_connected:control_chip", 50, 30)
    .requireItem("immersiveengineering:component_electronic_adv", 70, 30)
    .requireItem("modern_industrialization:analog_circuit", 90, 30)
    .requireItem("cognition:memory_tablet", 110, 30)

    .requireItem("createaddition:capacitor", 10, 50)
    .requireItem("tfmg:p_semiconductor", 30, 50)
    .requireItem("#c:ingots/electrum", 50, 50)
    .requireItem("tfmg:n_semiconductor", 70, 50)
    .requireItem("createdieselgenerators:large_diesel_engine", 90, 50)

    .requireFluid("32000x modern_industrialization:lubricant", 110, 50)
    .requireEnergy(20000, 10, 70)

    .produceItem("fragmentumneoforge:coreindustrial", 160, 30)

    .width(200)
    .height(150)
    .progressData(
      ProgressData.create()
        .x(130)
        .y(30)
    )
})
