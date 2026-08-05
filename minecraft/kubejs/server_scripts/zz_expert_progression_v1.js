// Authoritative v1 progression recipe layer.
// Loaded after the legacy expert scripts so every listed gated output has one
// final recipe path. Definitions are skipped before removal when an item ID is
// unavailable, preserving compatibility instead of deleting a valid original.

var V1ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var V1Registries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
var V1_ITEM_CACHE = Object.create(null)

function v1ItemExists(itemId) {
  if (Object.prototype.hasOwnProperty.call(V1_ITEM_CACHE, itemId)) {
    return V1_ITEM_CACHE[itemId]
  }

  var exists = false
  try {
    exists = V1Registries.ITEM.containsKey(V1ResourceLocation.parse(itemId))
  } catch (error) {
    exists = false
  }
  V1_ITEM_CACHE[itemId] = exists
  return exists
}

function v1RequiredItems(definition) {
  return [definition.output].concat(Object.keys(definition.key).map(function(symbol) {
    return definition.key[symbol]
  }))
}

function v1RegisterShaped(event, definition) {
  var required = v1RequiredItems(definition)
  for (var index = 0; index < required.length; index++) {
    if (!v1ItemExists(required[index])) {
      console.warn('[ExpertProgressionV1] Kept legacy path for ' + definition.output +
        ': unavailable item ' + required[index])
      return false
    }
  }

  if (definition.authoritative === true) {
    event.remove({ output: definition.output })
  }

  event.shaped(definition.output, definition.pattern, definition.key).id(definition.id)
  return true
}

ServerEvents.recipes(function(event) {
  var definitions = [
    // ---------------------------------------------------------------------
    // Persistent engineering standards. They return after crafting because
    // they represent proven infrastructure and permissions, not consumables.
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:v1/structural_lattice',
      output: 'kubejs:structural_lattice',
      pattern: ['SFS', 'BIB', 'SFS'],
      key: {
        S: 'immersiveengineering:component_steel',
        F: 'kubejs:field_engineering_kit',
        B: 'modern_industrialization:bronze_plate',
        I: 'immersiveengineering:component_iron'
      }
    },
    {
      id: 'kubejs:v1/kinetic_regulator',
      output: 'kubejs:kinetic_regulator',
      pattern: ['GRG', 'MKM', 'GRG'],
      key: {
        G: 'create:gearshift',
        R: 'minecraft:repeater',
        M: 'modern_industrialization:motor',
        K: 'kubejs:kinetic_interface'
      }
    },
    {
      id: 'kubejs:v1/electrical_bus',
      output: 'kubejs:electrical_bus',
      pattern: ['CEC', 'PBP', 'CEC'],
      key: {
        C: 'minecraft:copper_ingot',
        E: 'immersiveengineering:component_electronic',
        P: 'kubejs:power_regulation_unit',
        B: 'modern_industrialization:electronic_circuit'
      }
    },
    {
      id: 'kubejs:v1/calibrated_substrate',
      output: 'kubejs:calibrated_substrate',
      pattern: ['QGQ', 'EAE', 'QRQ'],
      key: {
        Q: 'minecraft:quartz',
        G: 'minecraft:gold_ingot',
        E: 'ae2:logic_processor',
        A: 'kubejs:materials_analysis_matrix',
        R: 'minecraft:comparator'
      }
    },
    {
      id: 'kubejs:v1/signal_backplane',
      output: 'kubejs:signal_backplane',
      pattern: ['FEF', 'CBC', 'FDF'],
      key: {
        F: 'ae2:fluix_crystal',
        E: 'ae2:engineering_processor',
        C: 'kubejs:calibrated_substrate',
        B: 'kubejs:electrical_bus',
        D: 'modern_industrialization:digital_circuit'
      }
    },
    {
      id: 'kubejs:v1/pressure_manifold',
      output: 'kubejs:pressure_manifold',
      pattern: ['CVC', 'PFP', 'CTC'],
      key: {
        C: 'pneumaticcraft:ingot_iron_compressed',
        V: 'pneumaticcraft:pressure_chamber_valve',
        P: 'immersiveengineering:fluid_pipe',
        F: 'kubejs:industrial_frame',
        T: 'pneumaticcraft:pressure_tube'
      }
    },
    {
      id: 'kubejs:v1/chemical_reactor_core',
      output: 'kubejs:chemical_reactor_core',
      pattern: ['PAP', 'CMC', 'PWP'],
      key: {
        P: 'pneumaticcraft:printed_circuit_board',
        A: 'immersiveengineering:component_electronic_adv',
        C: 'kubejs:precision_circuit',
        M: 'mekanism:advanced_control_circuit',
        W: 'kubejs:wildwood_seal'
      }
    },
    {
      id: 'kubejs:v1/bio_process_controller',
      output: 'kubejs:bio_process_controller',
      pattern: ['SPS', 'FCF', 'SHS'],
      key: {
        S: 'mysticalagriculture:supremium_essence',
        P: 'industrialforegoing:plastic',
        F: 'industrialforegoing:machine_frame_advanced',
        C: 'kubejs:chemical_processor',
        H: 'kubejs:apalachia_seal'
      }
    },
    {
      id: 'kubejs:v1/quantum_bus',
      output: 'kubejs:quantum_bus',
      pattern: ['EDE', 'BQB', 'EHE'],
      key: {
        E: 'ae2:engineering_processor',
        D: 'modern_industrialization:digital_circuit',
        B: 'mekanism:elite_control_circuit',
        Q: 'kubejs:signal_backplane',
        H: 'kubejs:skythern_seal'
      }
    },
    {
      id: 'kubejs:v1/resonant_power_cell',
      output: 'kubejs:resonant_power_cell',
      pattern: ['NCN', 'DQD', 'NUN'],
      key: {
        N: 'powah:crystal_nitro',
        C: 'powah:capacitor_nitro',
        D: 'draconicevolution:draconium_core',
        Q: 'kubejs:quantum_logic',
        U: 'mekanism:ultimate_control_circuit'
      }
    },
    {
      id: 'kubejs:v1/antimatter_regulator',
      output: 'kubejs:antimatter_regulator',
      pattern: ['PUP', 'SRS', 'PAP'],
      key: {
        P: 'mekanism:pellet_polonium',
        U: 'mekanism:ultimate_control_circuit',
        S: 'mekanism:sps_casing',
        R: 'kubejs:resonant_core',
        A: 'mekanism:pellet_antimatter'
      }
    },
    {
      id: 'kubejs:v1/dimensional_resonator',
      output: 'kubejs:dimensional_resonator',
      pattern: ['SVS', 'MRM', 'SDS'],
      key: {
        S: 'kubejs:skythern_seal',
        V: 'kubejs:vethea_seal',
        M: 'kubejs:mortum_seal',
        R: 'kubejs:resonant_core',
        D: 'kubejs:divine_seal'
      }
    },
    {
      id: 'kubejs:v1/draconic_lattice',
      output: 'kubejs:draconic_lattice',
      pattern: ['AWA', 'RWR', 'AHA'],
      key: {
        A: 'draconicevolution:awakened_draconium_ingot',
        W: 'draconicevolution:wyvern_core',
        R: 'kubejs:resonant_core',
        H: 'kubejs:vethea_seal'
      }
    },
    {
      id: 'kubejs:v1/emc_containment_core',
      output: 'kubejs:emc_containment_core',
      pattern: ['DUD', 'PCP', 'DWD'],
      key: {
        D: 'projecte:dark_matter',
        U: 'extendedcrafting:ultimate_singularity',
        P: 'kubejs:draconic_processor',
        C: 'extendedcrafting:ultimate_catalyst',
        W: 'kubejs:wreck_seal'
      }
    },
    {
      id: 'kubejs:v1/cosmic_assembly_matrix',
      output: 'kubejs:cosmic_assembly_matrix',
      pattern: ['CMC', 'ATA', 'CLC'],
      key: {
        C: 'avaritia:crystal_matrix_ingot',
        M: 'draconicevolution:awakened_core',
        A: 'extendedcrafting:ultimate_catalyst',
        T: 'kubejs:transmutation_matrix',
        L: 'kubejs:lunar_seal'
      }
    },
    {
      id: 'kubejs:v1/cosmic_synthesis_core',
      output: 'kubejs:cosmic_synthesis_core',
      pattern: ['ILI', 'CLC', 'INI'],
      key: {
        I: 'avaritia:infinity_ingot',
        L: 'kubejs:lunar_seal',
        C: 'kubejs:cosmic_catalyst',
        N: 'minecraft:nether_star'
      }
    },
    {
      id: 'kubejs:v1/creative_convergence_matrix',
      output: 'kubejs:creative_convergence_matrix',
      pattern: ['QAC', 'SXS', 'TRA'],
      key: {
        Q: 'kubejs:quantum_logic',
        A: 'kubejs:antimatter_regulator',
        C: 'kubejs:cosmic_synthesis_core',
        S: 'kubejs:cosmic_assembly_matrix',
        X: 'kubejs:cosmic_catalyst',
        T: 'kubejs:transmutation_matrix',
        R: 'kubejs:resonant_core'
      }
    },

    // ---------------------------------------------------------------------
    // Authoritative macro-stage milestones. Previous standards return to the
    // crafting grid, so repetition rewards infrastructure instead of forcing
    // the player to rebuild the entire chain.
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:v1/mechanical_core',
      output: 'kubejs:mechanical_core',
      authoritative: true,
      pattern: ['LAL', 'EBE', 'LKL'],
      key: {
        L: 'kubejs:structural_lattice',
        A: 'kubejs:materials_analysis_matrix',
        E: 'kubejs:electrical_bus',
        B: 'modern_industrialization:motor',
        K: 'kubejs:field_engineering_kit'
      }
    },
    {
      id: 'kubejs:v1/industrial_frame',
      output: 'kubejs:industrial_frame',
      authoritative: true,
      pattern: ['LKL', 'CMC', 'LPL'],
      key: {
        L: 'kubejs:structural_lattice',
        K: 'kubejs:kinetic_regulator',
        C: 'pneumaticcraft:ingot_iron_compressed',
        M: 'kubejs:mechanical_core',
        P: 'modern_industrialization:basic_machine_hull'
      }
    },
    {
      id: 'kubejs:v1/precision_circuit',
      output: 'kubejs:precision_circuit',
      authoritative: true,
      pattern: ['SCS', 'BIB', 'SHS'],
      key: {
        S: 'kubejs:signal_backplane',
        C: 'mekanism:basic_control_circuit',
        B: 'kubejs:calibrated_substrate',
        I: 'kubejs:industrial_frame',
        H: 'kubejs:eden_seal'
      }
    },
    {
      id: 'kubejs:v1/chemical_processor',
      output: 'kubejs:chemical_processor',
      authoritative: true,
      pattern: ['MRM', 'PCP', 'MHM'],
      key: {
        M: 'kubejs:pressure_manifold',
        R: 'kubejs:chemical_reactor_core',
        P: 'pneumaticcraft:printed_circuit_board',
        C: 'kubejs:precision_circuit',
        H: 'kubejs:wildwood_seal'
      }
    },
    {
      id: 'kubejs:v1/bioindustrial_matrix',
      output: 'kubejs:bioindustrial_matrix',
      authoritative: true,
      pattern: ['SBS', 'FCF', 'SHS'],
      key: {
        S: 'mysticalagriculture:supremium_essence',
        B: 'kubejs:bio_process_controller',
        F: 'industrialforegoing:machine_frame_advanced',
        C: 'kubejs:chemical_processor',
        H: 'kubejs:apalachia_seal'
      }
    },
    {
      id: 'kubejs:v1/quantum_logic',
      output: 'kubejs:quantum_logic',
      authoritative: true,
      pattern: ['EBE', 'BQB', 'EHE'],
      key: {
        E: 'ae2:engineering_processor',
        B: 'kubejs:quantum_bus',
        Q: 'kubejs:bioindustrial_matrix',
        H: 'kubejs:skythern_seal'
      }
    },
    {
      id: 'kubejs:v1/resonant_core',
      output: 'kubejs:resonant_core',
      authoritative: true,
      pattern: ['ICI', 'PQP', 'IMI'],
      key: {
        I: 'mekanism:induction_casing',
        C: 'kubejs:resonant_power_cell',
        P: 'powah:capacitor_nitro',
        Q: 'kubejs:quantum_logic',
        M: 'kubejs:mortum_seal'
      }
    },
    {
      id: 'kubejs:v1/draconic_processor',
      output: 'kubejs:draconic_processor',
      authoritative: true,
      pattern: ['ULU', 'RCR', 'UHU'],
      key: {
        U: 'extendedcrafting:ultimate_component',
        L: 'kubejs:draconic_lattice',
        R: 'draconicevolution:awakened_draconium_ingot',
        C: 'kubejs:resonant_core',
        H: 'kubejs:vethea_seal'
      }
    },
    {
      id: 'kubejs:v1/transmutation_matrix',
      output: 'kubejs:transmutation_matrix',
      authoritative: true,
      pattern: ['DCD', 'PEP', 'DTD'],
      key: {
        D: 'projecte:dark_matter',
        C: 'kubejs:emc_containment_core',
        P: 'kubejs:draconic_processor',
        E: 'extendedcrafting:ultimate_singularity',
        T: 'kubejs:wreck_seal'
      }
    },
    {
      id: 'kubejs:v1/cosmic_catalyst',
      output: 'kubejs:cosmic_catalyst',
      authoritative: true,
      pattern: ['AMA', 'CTC', 'ALA'],
      key: {
        A: 'avaritia:crystal_matrix_ingot',
        M: 'kubejs:cosmic_assembly_matrix',
        C: 'extendedcrafting:ultimate_catalyst',
        T: 'kubejs:transmutation_matrix',
        L: 'kubejs:lunar_seal'
      }
    },

    // Strategic outputs that otherwise create direct tier skips.
    {
      id: 'kubejs:v1/mekanism_steel_casing',
      output: 'mekanism:steel_casing',
      authoritative: true,
      pattern: ['SLS', 'IFI', 'SLS'],
      key: {
        S: 'immersiveengineering:ingot_steel',
        L: 'kubejs:structural_lattice',
        I: 'modern_industrialization:steel_ingot',
        F: 'kubejs:industrial_frame'
      }
    },
    {
      id: 'kubejs:v1/industrial_foregoing_advanced_frame',
      output: 'industrialforegoing:machine_frame_advanced',
      authoritative: true,
      pattern: ['PMP', 'FCF', 'PHP'],
      key: {
        P: 'industrialforegoing:plastic',
        M: 'kubejs:pressure_manifold',
        F: 'industrialforegoing:machine_frame_simple',
        C: 'kubejs:chemical_processor',
        H: 'kubejs:industrial_frame'
      }
    },
    {
      id: 'kubejs:v1/ae2_controller',
      output: 'ae2:controller',
      authoritative: true,
      pattern: ['SBS', 'LQL', 'SCS'],
      key: {
        S: 'ae2:smooth_sky_stone_block',
        B: 'kubejs:quantum_bus',
        L: 'ae2:engineering_processor',
        Q: 'kubejs:quantum_logic',
        C: 'kubejs:signal_backplane'
      }
    },
    {
      id: 'kubejs:v1/powah_nitro_reactor',
      output: 'powah:reactor_nitro',
      authoritative: true,
      pattern: ['NCN', 'RER', 'NQN'],
      key: {
        N: 'powah:crystal_nitro',
        C: 'powah:capacitor_nitro',
        R: 'powah:reactor_spirited',
        E: 'kubejs:resonant_core',
        Q: 'kubejs:resonant_power_cell'
      }
    },
    {
      id: 'kubejs:v1/draconic_wyvern_core',
      output: 'draconicevolution:wyvern_core',
      authoritative: true,
      pattern: ['DED', 'ERE', 'DLD'],
      key: {
        D: 'draconicevolution:draconium_ingot',
        E: 'minecraft:ender_eye',
        R: 'kubejs:resonant_core',
        L: 'kubejs:dimensional_resonator'
      }
    },
    {
      id: 'kubejs:v1/projecte_philosophers_stone',
      output: 'projecte:philosophers_stone',
      authoritative: true,
      pattern: ['AUA', 'NPN', 'ADA'],
      key: {
        A: 'draconicevolution:awakened_draconium_ingot',
        U: 'extendedcrafting:ultimate_component',
        N: 'minecraft:nether_star',
        P: 'kubejs:draconic_processor',
        D: 'kubejs:dimensional_resonator'
      }
    },
    {
      id: 'kubejs:v1/extendedcrafting_ultimate_table',
      output: 'extendedcrafting:ultimate_table',
      authoritative: true,
      pattern: ['UCU', 'LPL', 'UEU'],
      key: {
        U: 'extendedcrafting:ultimate_component',
        C: 'extendedcrafting:ultimate_catalyst',
        L: 'kubejs:draconic_lattice',
        P: 'kubejs:draconic_processor',
        E: 'minecraft:ender_eye'
      }
    },
    {
      id: 'kubejs:v1/avaritia_extreme_crafting_table',
      output: 'avaritia:extreme_crafting_table',
      authoritative: true,
      pattern: ['CMC', 'SXS', 'CTC'],
      key: {
        C: 'avaritia:crystal_matrix_ingot',
        M: 'avaritia:double_compressed_crafting_table',
        S: 'kubejs:cosmic_assembly_matrix',
        X: 'kubejs:cosmic_catalyst',
        T: 'kubejs:transmutation_matrix'
      }
    },
    {
      id: 'kubejs:v1/mystical_agriculture_infusion_altar',
      output: 'mysticalagriculture:infusion_altar',
      authoritative: true,
      pattern: ['PSP', 'FIF', 'SBS'],
      key: {
        P: 'mysticalagriculture:prosperity_shard',
        S: 'minecraft:stone',
        F: 'immersiveengineering:component_iron',
        I: 'kubejs:industrial_frame',
        B: 'kubejs:bio_process_controller'
      }
    }
  ]

  var registered = 0
  definitions.forEach(function(definition) {
    if (v1RegisterShaped(event, definition)) {
      registered++
    }
  })

})
