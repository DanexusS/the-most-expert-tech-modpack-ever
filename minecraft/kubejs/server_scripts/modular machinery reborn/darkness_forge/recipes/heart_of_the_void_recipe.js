ServerEvents.recipes(event => {
  const time = 36000
  const machine_id = "mmr:darkness_forge"

  event.recipes.modular_machinery_reborn.machine_recipe(machine_id, time)
    .requireItem("fragmentumneoforge:ultimatecapacitor", 10, 10)
    .requireItem("fragmentumneoforge:bladeeclipse", 30, 10)
    .requireItem("fragmentumneoforge:creativeamalgamation", 50, 10)
    .requireItem("fragmentumneoforge:elixirof_life", 70, 10)

    .requireItem("fragmentumneoforge:draconicmatrix", 10, 30)
    .requireItem("fragmentumneoforge:manuscriptvoid", 30, 30)
    .requireItem("fragmentumneoforge:machinaastris", 50, 30)
    .requireItem("fragmentumneoforge:auraforgeheart", 70, 30)

    .requireItem("fragmentumneoforge:flos", 10, 50)
    .requireItem("fragmentumneoforge:rocket", 30, 50)
    .requireItem("fragmentumneoforge:datacrystal", 50, 50)
    .requireItem("fragmentumneoforge:coreindustrial", 70, 50)


    .requireEnergy(2000000000, 40, 70)
    .requireFluid("20000x justdirethings:refined_t4_fluid_source", 40, 130)


    .produceItem("fragmentumneoforge:heartofthevoid", 135, 30)

    .width(180)
    .height(150)
    .progressData(
      ProgressData.create()
        .x(100)
        .y(30)
    )
})
