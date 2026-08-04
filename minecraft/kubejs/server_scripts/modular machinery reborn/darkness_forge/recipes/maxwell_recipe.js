ServerEvents.recipes(event => {
  const time = 36000
  const machine_id = "mmr:darkness_forge"

  event.recipes.modular_machinery_reborn.machine_recipe(machine_id, time)
    .requireItem("minecraft:black_wool", 30, 10)
    .requireItem("avaritia:infinity", 50, 10)
    .requireItem("minecraft:black_wool", 70, 10)

    .requireItem("minecraft:black_wool", 30, 30)
    .requireItem("minecraft:white_wool", 50, 30)
    .requireItem("minecraft:black_wool", 70, 30)

    .requireItem("minecraft:black_wool", 30, 50)
    .requireItem("minecraft:white_wool", 50, 50)
    .requireItem("minecraft:black_wool", 70, 50)

    .requireEnergy(10000000, 50, 70)
    .requireFluid("32000x modern_industrialization:uu_matter", 50, 130)


    .produceItem("placeablemaxwell:maxwell", 135, 30)

    .width(180)
    .height(150)
    .progressData(
      ProgressData.create()
        .x(100)
        .y(30)
    )
})
