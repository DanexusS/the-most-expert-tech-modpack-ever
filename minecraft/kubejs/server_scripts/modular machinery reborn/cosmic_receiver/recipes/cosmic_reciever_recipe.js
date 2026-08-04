ServerEvents.recipes(event => {
  const time = 80000
  const machine_id = "mmr:cosmic_reciever"

  event.recipes.modular_machinery_reborn.machine_recipe(machine_id, time)
    .requireItem("tfmg:n_semiconductor", 10, 10)
    .requireItem("irons_spellbooks:arcane_ingot", 30, 10)
    .requireItem("advanced_ae:quantum_alloy_block", 50, 10)
    .requireItem("projectexpansion:magnum_star_omega", 70, 10)
    .requireItem("ars_nouveau:abjuration_essence", 90, 10)
    .requireItem("extended_industrialization:tesla_interdimensional_upgrade", 110, 10)
    .requireItem("forbidden_arcanus:dark_matter", 130, 10)
    .requireItem("pneumaticcraft:creative_compressed_iron_block", 150, 10)
    .requireItem("mekanism_extras:infinite_control_circuit", 170, 10)
    .requireItem("modern_industrialization:ultradense_metal_ball", 190, 10)
    .requireItem("mekanism:ultimate_control_circuit", 210, 10)

    .requireItem("ars_nouveau:source_gem_block", 10, 30)
    .requireItem("occultism:dragonyst_dust", 30, 30)
    .requireItem("enderio:weather_crystal", 50, 30)
    .requireItem("allthecompressed:antimatter_block_5x", 70, 30)
    .requireItem("modern_industrialization:singularity", 90, 30)
    .requireItem('extendedcrafting:singularity[extendedcrafting:singularity_id="extendedcrafting:draconium"]', 110, 30)
    .requireItem("cognition:mending_neurogel_blob", 130, 30)
    .requireItem("draconicevolution:draconium_block", 150, 30)
    .requireItem("kubejs:sus_shell", 170, 30)
    .requireItem("allthemodium:unobtainium_block", 190, 30)
    .requireItem("industrialforegoing:pink_slime_block", 210, 30)

    .requireItem("bhc:soul_heart_crystal", 10, 50)
    .requireItem("projectexpansion:pink_matter", 30, 50)
    .requireItem("industrialforegoing:pink_slime_bucket", 50, 50)
    .requireItem("projectexpansion:magenta_matter", 70, 50)
    .requireItem("mysticalagriculture:dye_agglomeratio", 90, 50)
    .requireItem("occultism:chalk_rainbow", 110, 50)
    .requireItem("ironfurnaces:rainbow_core", 130, 50)
    .requireItem("cognition:primordial_assembly", 150, 50)
    .requireItem("cognition:transforming_focus", 170, 50)
    .requireItem("mysticalagradditions:creative_essence", 190, 50)

    .requireEnergy(20000,10,90)

    .requireFluid("10000x mekanismgenerators:fusion_fuel",10,70)

    .produceItem("fragmentumneoforge:creativeamalgamation", 260, 30)

    .width(290)
    .height(150)
     .progressData(
      ProgressData.create()
        .x(230)
        .y(30)
    )
})
