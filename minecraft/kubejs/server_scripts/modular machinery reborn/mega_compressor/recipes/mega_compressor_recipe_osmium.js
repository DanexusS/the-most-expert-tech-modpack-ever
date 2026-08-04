ServerEvents.recipes(event => {
  const time = 240
  const machine_id = "mmr:mega_compressor_controller"

  event.recipes.modular_machinery_reborn.machine_recipe(machine_id, time)
    .requireItem("1111x #c:storage_blocks/osmium", 30, 30)

    .requireEnergy(20000, 5, 30)

    .produceItem('5x avaritia:singularity[avaritia:singularity_id="avaritia:osmium"]', 75, 30)

    .width(150)
    .height(100)
    .progressData(
      ProgressData.create()
        .x(50)
        .y(30)
    )
})
