ServerEvents.recipes(event => {
  const time = 140
  const machine_id = "mmr:catalyst_forge"

  event.remove('avaritia:infinity_catalyst')


  event.recipes.modular_machinery_reborn.machine_recipe(machine_id, time)
    .requireItem("industrialforegoing:machine_frame_supreme", 10, 10)
    .requireItem("apothic_enchanting:draconic_endshelf", 30, 10)
    .requireItem("avaritia:diamond_lattice_block", 50, 10)
    .requireItem("avaritia:star_fuel_block", 70, 10)
    .requireItem("draconicevolution:awakened_draconium_block", 90, 10)
    .requireItem("justdirethings:eclipsealloy_block", 110, 10)
    .requireItem("allthecompressed:antimatter_block_1x", 130, 10)
    .requireItem("avaritia:endest_pearl", 150, 10)
    .requireItem("bigreactors:insanite_block", 170, 10)
    .requireItem("mysticalagradditions:creative_essence", 190, 10)
    .requireItem("extendedcrafting:the_ultimate_ingot", 210, 10)

    .requireItem("modern_industrialization:processing_unit", 10, 30)
    .requireItem("extendedcrafting:ultimate_singularity", 30, 30)
    .requireItem("enderio:vibrant_capacitor_bank", 50, 30)
    .requireItem("megacells:cell_component_256m", 70, 30)
    .requireItem("avaritia:neutron_pile", 90, 30)
    .requireItem("avaritia:neutron_nugget", 110, 30)
    .requireItem("avaritia:neutron_ingot", 130, 30)
    .requireItem("avaritia:neutron_gear", 150, 30)
    .requireItem("avaritia:neutron", 170, 30)
    .requireItem("avaritia:diamond_lattice", 190, 30)
    .requireItem("avaritia:crystal_matrix_ingot", 210, 30)

    .requireItem("avaritia:star_fuel", 10, 50)
    .requireItem("avaritia:refined_coal", 30, 50)
    .requireItem("avaritia:refined_coal_block", 50, 50)
    .requireItem("avaritia:cosmic_meatballs", 70, 50)
    .requireItem("avaritia:ultimate_stew", 90, 50)

    .requireEnergy(1000000000, 10, 70)
    .requireFluid("20000x modern_industrialization:cryofluid", 110, 50)

    .produceItem("avaritia:infinity_catalyst", 260, 30)

    .width(290)
    .height(150)
     .progressData(
      ProgressData.create()
        .x(230)
        .y(30)
     )
})
