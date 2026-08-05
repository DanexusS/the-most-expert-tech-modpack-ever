// Authoritative multi-step recipe paths for progression stages 9–12.
// The recipes force controlled resource production, digital logistics, energy
// infrastructure and antimatter engineering to converge through real branch
// components instead of one isolated expensive craft.

var AdvancedPathLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var AdvancedPathRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
var ADVANCED_PATH_CACHE = Object.create(null)

function advancedPathExists(itemId) {
  if (Object.prototype.hasOwnProperty.call(ADVANCED_PATH_CACHE, itemId)) {
    return ADVANCED_PATH_CACHE[itemId]
  }
  var exists = false
  try {
    exists = AdvancedPathRegistries.ITEM.containsKey(AdvancedPathLocation.parse(itemId))
  } catch (error) {
    exists = false
  }
  ADVANCED_PATH_CACHE[itemId] = exists
  return exists
}

function advancedPathRegister(event, definition) {
  var required = [definition.output].concat(Object.keys(definition.key).map(function(symbol) {
    return definition.key[symbol]
  }))
  for (var index = 0; index < required.length; index++) {
    if (!advancedPathExists(required[index])) {
      console.warn('[AdvancedStagePaths] Kept previous path for ' + definition.output +
        ': unavailable item ' + required[index])
      return false
    }
  }
  event.remove({ output: definition.output })
  event.shaped(definition.output, definition.pattern, definition.key).id(definition.id)
  return true
}

ServerEvents.recipes(function(event) {
  var definitions = [
    // ---------------------------------------------------------------------
    // Stage 9 — Controlled Resource Production
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:advanced_path/culture_support_matrix',
      output: 'kubejs:culture_support_matrix',
      authoritative: true,
      pattern: ['SPS', 'FCF', 'SAS'],
      key: {
        S: 'mysticalagriculture:supremium_essence',
        P: 'industrialforegoing:plastic',
        F: 'industrialforegoing:machine_frame_advanced',
        C: 'kubejs:chemical_processor',
        A: 'kubejs:apalachia_seal'
      }
    },
    {
      id: 'kubejs:advanced_path/simulation_data_coupler',
      output: 'kubejs:simulation_data_coupler',
      authoritative: true,
      pattern: ['BEB', 'SPS', 'BCB'],
      key: {
        B: 'hostilenetworks:blank_data_model',
        E: 'ae2:engineering_processor',
        S: 'kubejs:signal_backplane',
        P: 'kubejs:precision_circuit',
        C: 'mekanism:elite_control_circuit'
      }
    },
    {
      id: 'kubejs:advanced_path/renewable_harvest_controller',
      output: 'kubejs:renewable_harvest_controller',
      authoritative: true,
      pattern: ['SPS', 'FCF', 'SAS'],
      key: {
        S: 'mysticalagriculture:supremium_essence',
        P: 'industrialforegoing:plastic',
        F: 'industrialforegoing:machine_frame_advanced',
        C: 'kubejs:process_control_board',
        A: 'mekanism:advanced_control_circuit'
      }
    },
    {
      id: 'kubejs:advanced_path/infusion_altar',
      output: 'mysticalagriculture:infusion_altar',
      authoritative: true,
      pattern: ['PSP', 'MCM', 'SSS'],
      key: {
        P: 'mysticalagriculture:prosperity_shard',
        S: 'minecraft:stone',
        M: 'kubejs:culture_support_matrix',
        C: 'kubejs:chemical_processor'
      }
    },
    {
      id: 'kubejs:advanced_path/sim_chamber',
      output: 'hostilenetworks:sim_chamber',
      authoritative: true,
      pattern: ['PBP', 'CSC', 'PMP'],
      key: {
        P: 'hostilenetworks:prediction_matrix',
        B: 'hostilenetworks:blank_data_model',
        C: 'kubejs:simulation_data_coupler',
        S: 'kubejs:signal_backplane',
        M: 'kubejs:chemical_processor'
      }
    },
    {
      id: 'kubejs:advanced_path/plant_gatherer',
      output: 'industrialforegoing:plant_gatherer',
      authoritative: true,
      pattern: ['PFP', 'HCH', 'PAP'],
      key: {
        P: 'industrialforegoing:plastic',
        F: 'industrialforegoing:machine_frame_advanced',
        H: 'kubejs:renewable_harvest_controller',
        C: 'kubejs:chemical_processor',
        A: 'mekanism:advanced_control_circuit'
      }
    },
    {
      id: 'kubejs:advanced_path/bio_process_controller',
      output: 'kubejs:bio_process_controller',
      authoritative: true,
      pattern: ['CSC', 'HPR', 'CAC'],
      key: {
        C: 'kubejs:culture_support_matrix',
        S: 'kubejs:simulation_data_coupler',
        H: 'kubejs:renewable_harvest_controller',
        P: 'kubejs:chemical_processor',
        R: 'industrialforegoing:machine_frame_advanced',
        A: 'kubejs:apalachia_seal'
      }
    },
    {
      id: 'kubejs:advanced_path/bioindustrial_matrix',
      output: 'kubejs:bioindustrial_matrix',
      authoritative: true,
      pattern: ['SBS', 'FCF', 'SAS'],
      key: {
        S: 'mysticalagriculture:supremium_essence',
        B: 'kubejs:bio_process_controller',
        F: 'industrialforegoing:machine_frame_advanced',
        C: 'kubejs:chemical_processor',
        A: 'kubejs:apalachia_seal'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 10 — Applied Logistics
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:advanced_path/controller_channel_frame',
      output: 'kubejs:controller_channel_frame',
      authoritative: true,
      pattern: ['SES', 'BQB', 'SES'],
      key: {
        S: 'ae2:smooth_sky_stone_block',
        E: 'ae2:engineering_processor',
        B: 'kubejs:signal_backplane',
        Q: 'kubejs:bioindustrial_matrix'
      }
    },
    {
      id: 'kubejs:advanced_path/crafting_cpu_scheduler',
      output: 'kubejs:crafting_cpu_scheduler',
      authoritative: true,
      pattern: ['CPC', 'DBD', 'CQC'],
      key: {
        C: 'ae2:calculation_processor',
        P: 'ae2:engineering_processor',
        D: 'modern_industrialization:digital_circuit',
        B: 'kubejs:signal_backplane',
        Q: 'kubejs:bioindustrial_matrix'
      }
    },
    {
      id: 'kubejs:advanced_path/quantum_link_stabilizer',
      output: 'kubejs:quantum_link_stabilizer',
      authoritative: true,
      pattern: ['FEF', 'BQB', 'FIF'],
      key: {
        F: 'ae2:fluix_crystal',
        E: 'ae2:engineering_processor',
        B: 'kubejs:bioindustrial_matrix',
        Q: 'kubejs:signal_backplane',
        I: 'minecraft:ender_eye'
      }
    },
    {
      id: 'kubejs:advanced_path/ae2_controller',
      output: 'ae2:controller',
      authoritative: true,
      pattern: ['SFS', 'ECE', 'SFS'],
      key: {
        S: 'ae2:smooth_sky_stone_block',
        F: 'ae2:fluix_crystal',
        E: 'ae2:engineering_processor',
        C: 'kubejs:controller_channel_frame'
      }
    },
    {
      id: 'kubejs:advanced_path/ae2_crafting_unit',
      output: 'ae2:crafting_unit',
      authoritative: true,
      pattern: ['QCQ', 'PSP', 'QCQ'],
      key: {
        Q: 'ae2:quartz_glass',
        C: 'ae2:calculation_processor',
        P: 'kubejs:crafting_cpu_scheduler',
        S: 'kubejs:signal_backplane'
      }
    },
    {
      id: 'kubejs:advanced_path/ae2_quantum_ring',
      output: 'ae2:quantum_ring',
      authoritative: true,
      pattern: ['FEF', 'SBS', 'FIF'],
      key: {
        F: 'ae2:fluix_crystal',
        E: 'ae2:engineering_processor',
        S: 'kubejs:quantum_link_stabilizer',
        B: 'kubejs:bioindustrial_matrix',
        I: 'minecraft:ender_eye'
      }
    },
    {
      id: 'kubejs:advanced_path/quantum_bus',
      output: 'kubejs:quantum_bus',
      authoritative: true,
      pattern: ['CFC', 'SBQ', 'CHC'],
      key: {
        C: 'kubejs:controller_channel_frame',
        F: 'kubejs:crafting_cpu_scheduler',
        S: 'kubejs:quantum_link_stabilizer',
        B: 'kubejs:signal_backplane',
        Q: 'kubejs:bioindustrial_matrix',
        H: 'kubejs:skythern_seal'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 11 — Resonant Energy
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:advanced_path/nitro_regulation_array',
      output: 'kubejs:nitro_regulation_array',
      authoritative: true,
      pattern: ['NCN', 'UQU', 'NCN'],
      key: {
        N: 'powah:crystal_nitro',
        C: 'powah:capacitor_nitro',
        U: 'mekanism:ultimate_control_circuit',
        Q: 'kubejs:quantum_logic'
      }
    },
    {
      id: 'kubejs:advanced_path/induction_transfer_manifold',
      output: 'kubejs:induction_transfer_manifold',
      authoritative: true,
      pattern: ['OEO', 'BQB', 'OEO'],
      key: {
        O: 'mekanism:ingot_refined_obsidian',
        E: 'mekanism:elite_control_circuit',
        B: 'kubejs:quantum_bus',
        Q: 'ae2:engineering_processor'
      }
    },
    {
      id: 'kubejs:advanced_path/resonant_distribution_frame',
      output: 'kubejs:resonant_distribution_frame',
      authoritative: true,
      pattern: ['DND', 'MQM', 'DID'],
      key: {
        D: 'draconicevolution:draconium_core',
        N: 'kubejs:nitro_regulation_array',
        M: 'kubejs:induction_transfer_manifold',
        Q: 'kubejs:quantum_logic',
        I: 'mekanism:ultimate_control_circuit'
      }
    },
    {
      id: 'kubejs:advanced_path/energizing_rod_nitro',
      output: 'powah:energizing_rod_nitro',
      authoritative: true,
      pattern: ['NCN', 'RAR', 'NUN'],
      key: {
        N: 'powah:crystal_nitro',
        C: 'powah:capacitor_nitro',
        R: 'powah:energizing_rod_niotic',
        A: 'kubejs:nitro_regulation_array',
        U: 'mekanism:ultimate_control_circuit'
      }
    },
    {
      id: 'kubejs:advanced_path/induction_casing',
      output: 'mekanism:induction_casing',
      authoritative: true,
      pattern: ['OCO', 'MIM', 'OEO'],
      key: {
        O: 'mekanism:ingot_refined_obsidian',
        C: 'mekanism:elite_control_circuit',
        M: 'kubejs:induction_transfer_manifold',
        I: 'ae2:engineering_processor',
        E: 'kubejs:quantum_logic'
      }
    },
    {
      id: 'kubejs:advanced_path/resonant_power_cell',
      output: 'kubejs:resonant_power_cell',
      authoritative: true,
      pattern: ['NIN', 'RQR', 'NUN'],
      key: {
        N: 'kubejs:nitro_regulation_array',
        I: 'kubejs:induction_transfer_manifold',
        R: 'kubejs:resonant_distribution_frame',
        Q: 'kubejs:quantum_logic',
        U: 'mekanism:ultimate_control_circuit'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 12 — Nuclear and Antimatter Engineering
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:advanced_path/radiation_interlock_module',
      output: 'kubejs:radiation_interlock_module',
      authoritative: true,
      pattern: ['PUP', 'IRI', 'PUP'],
      key: {
        P: 'mekanism:pellet_polonium',
        U: 'mekanism:ultimate_control_circuit',
        I: 'mekanism:induction_casing',
        R: 'kubejs:resonant_core'
      }
    },
    {
      id: 'kubejs:advanced_path/sps_pulse_controller',
      output: 'kubejs:sps_pulse_controller',
      authoritative: true,
      pattern: ['NUN', 'RQR', 'NIN'],
      key: {
        N: 'minecraft:nether_star',
        U: 'mekanism:ultimate_control_circuit',
        R: 'kubejs:resonant_power_cell',
        Q: 'kubejs:quantum_logic',
        I: 'mekanism:induction_casing'
      }
    },
    {
      id: 'kubejs:advanced_path/antimatter_containment_cell',
      output: 'kubejs:antimatter_containment_cell',
      authoritative: true,
      pattern: ['ONO', 'PRP', 'ONO'],
      key: {
        O: 'mekanism:ingot_refined_obsidian',
        N: 'minecraft:netherite_ingot',
        P: 'mekanism:pellet_polonium',
        R: 'kubejs:resonant_core'
      }
    },
    {
      id: 'kubejs:advanced_path/sps_casing',
      output: 'mekanism:sps_casing',
      authoritative: true,
      pattern: ['PUP', 'IRI', 'PUP'],
      key: {
        P: 'mekanism:pellet_polonium',
        U: 'mekanism:ultimate_control_circuit',
        I: 'mekanism:induction_casing',
        R: 'kubejs:radiation_interlock_module'
      }
    },
    {
      id: 'kubejs:advanced_path/supercharged_coil',
      output: 'mekanism:supercharged_coil',
      authoritative: true,
      pattern: ['UCU', 'PIP', 'URU'],
      key: {
        U: 'mekanism:ultimate_control_circuit',
        C: 'kubejs:sps_pulse_controller',
        P: 'kubejs:resonant_power_cell',
        I: 'mekanism:induction_casing',
        R: 'kubejs:resonant_core'
      }
    },
    {
      id: 'kubejs:advanced_path/antimatter_regulator',
      output: 'kubejs:antimatter_regulator',
      authoritative: true,
      pattern: ['RPR', 'SAC', 'RPR'],
      key: {
        R: 'kubejs:radiation_interlock_module',
        P: 'kubejs:sps_pulse_controller',
        S: 'mekanism:sps_casing',
        A: 'mekanism:pellet_antimatter',
        C: 'kubejs:antimatter_containment_cell'
      }
    }
  ]

  var registered = 0
  definitions.forEach(function(definition) {
    registered += advancedPathRegister(event, definition) ? 1 : 0
  })
  console.info('[AdvancedStagePaths] Registered ' + registered + '/' + definitions.length +
    ' staged resource, logistics, energy and antimatter recipes.')
})
