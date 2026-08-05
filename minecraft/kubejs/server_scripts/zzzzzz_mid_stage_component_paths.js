// Authoritative multi-step recipe paths for progression stages 5–8.
// The intermediate assemblies expose where the real bottleneck is: pressure
// hardware, substrate preparation, digital storage, chemistry or maintenance.

var MidPathLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var MidPathRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
var MID_PATH_CACHE = Object.create(null)

function midPathExists(itemId) {
  if (Object.prototype.hasOwnProperty.call(MID_PATH_CACHE, itemId)) {
    return MID_PATH_CACHE[itemId]
  }
  var exists = false
  try {
    exists = MidPathRegistries.ITEM.containsKey(MidPathLocation.parse(itemId))
  } catch (error) {
    exists = false
  }
  MID_PATH_CACHE[itemId] = exists
  return exists
}

function midPathRegister(event, definition) {
  var required = [definition.output].concat(Object.keys(definition.key).map(function(symbol) {
    return definition.key[symbol]
  }))
  for (var index = 0; index < required.length; index++) {
    if (!midPathExists(required[index])) {
      console.warn('[MidStagePaths] Kept previous path for ' + definition.output +
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
    // Stage 5 — Precision Manufacturing
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:mid_path/pressure_treated_frame',
      output: 'kubejs:pressure_treated_frame',
      authoritative: true,
      pattern: ['CLC', 'KFK', 'CLC'],
      key: {
        C: 'pneumaticcraft:ingot_iron_compressed',
        L: 'kubejs:structural_lattice',
        K: 'kubejs:kinetic_interface',
        F: 'kubejs:field_engineering_kit'
      }
    },
    {
      id: 'kubejs:mid_path/etched_copper_substrate',
      output: 'kubejs:etched_copper_substrate',
      authoritative: true,
      pattern: ['CQC', 'EAE', 'CGC'],
      key: {
        C: 'minecraft:copper_ingot',
        Q: 'minecraft:quartz',
        E: 'modern_industrialization:electronic_circuit',
        A: 'kubejs:materials_analysis_matrix',
        G: 'minecraft:gold_ingot'
      }
    },
    {
      id: 'kubejs:mid_path/assembly_alignment_jig',
      output: 'kubejs:assembly_alignment_jig',
      authoritative: true,
      pattern: ['MBM', 'PFP', 'MCM'],
      key: {
        M: 'kubejs:metallurgical_bracing',
        B: 'minecraft:iron_bars',
        P: 'create:precision_mechanism',
        F: 'kubejs:field_tool_frame',
        C: 'minecraft:comparator'
      }
    },
    {
      id: 'kubejs:mid_path/calibrated_substrate',
      output: 'kubejs:calibrated_substrate',
      authoritative: true,
      pattern: ['ESE', 'MCM', 'ELE'],
      key: {
        E: 'modern_industrialization:electronic_circuit',
        S: 'kubejs:etched_copper_substrate',
        M: 'kubejs:materials_analysis_matrix',
        C: 'minecraft:comparator',
        L: 'kubejs:survey_lens'
      }
    },
    {
      id: 'kubejs:mid_path/industrial_frame',
      output: 'kubejs:industrial_frame',
      authoritative: true,
      pattern: ['PJP', 'HMH', 'RKR'],
      key: {
        P: 'kubejs:pressure_treated_frame',
        J: 'kubejs:assembly_alignment_jig',
        H: 'modern_industrialization:basic_machine_hull',
        M: 'kubejs:mechanical_core',
        R: 'kubejs:kinetic_regulator',
        K: 'kubejs:structural_lattice'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 6 — Digital Storage
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:mid_path/processor_press_frame',
      output: 'kubejs:processor_press_frame',
      authoritative: true,
      pattern: ['PCP', 'FBF', 'PEP'],
      key: {
        P: 'minecraft:sticky_piston',
        C: 'kubejs:calibrated_substrate',
        F: 'kubejs:pressure_treated_frame',
        B: 'kubejs:electrical_bus',
        E: 'immersiveengineering:component_electronic'
      }
    },
    {
      id: 'kubejs:mid_path/storage_cell_backplane',
      output: 'kubejs:storage_cell_backplane',
      authoritative: true,
      pattern: ['QWQ', 'BEB', 'QCQ'],
      key: {
        Q: 'ae2:quartz_glass',
        W: 'kubejs:insulated_wiring_bundle',
        B: 'kubejs:electrical_bus',
        E: 'kubejs:etched_copper_substrate',
        C: 'kubejs:calibrated_substrate'
      }
    },
    {
      id: 'kubejs:mid_path/channel_test_fixture',
      output: 'kubejs:channel_test_fixture',
      authoritative: true,
      pattern: ['FCF', 'BLB', 'FRF'],
      key: {
        F: 'ae2:fluix_glass_cable',
        C: 'minecraft:comparator',
        B: 'kubejs:manual_control_board',
        L: 'kubejs:low_voltage_busbar',
        R: 'minecraft:redstone_torch'
      }
    },
    {
      id: 'kubejs:mid_path/ae2_inscriber',
      output: 'ae2:inscriber',
      authoritative: true,
      pattern: ['PFP', 'EME', 'PBP'],
      key: {
        P: 'minecraft:sticky_piston',
        F: 'kubejs:processor_press_frame',
        E: 'immersiveengineering:component_electronic',
        M: 'modern_industrialization:motor',
        B: 'kubejs:electrical_bus'
      }
    },
    {
      id: 'kubejs:mid_path/ae2_drive',
      output: 'ae2:drive',
      authoritative: true,
      pattern: ['QEQ', 'BSB', 'QTQ'],
      key: {
        Q: 'ae2:quartz_glass',
        E: 'ae2:engineering_processor',
        B: 'kubejs:storage_cell_backplane',
        S: 'ae2:fluix_glass_cable',
        T: 'kubejs:channel_test_fixture'
      }
    },
    {
      id: 'kubejs:mid_path/signal_backplane',
      output: 'kubejs:signal_backplane',
      authoritative: true,
      pattern: ['EDE', 'TBT', 'ECE'],
      key: {
        E: 'ae2:engineering_processor',
        D: 'modern_industrialization:digital_circuit',
        T: 'kubejs:channel_test_fixture',
        B: 'kubejs:storage_cell_backplane',
        C: 'kubejs:calibrated_substrate'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 7 — Process Chemistry
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:mid_path/sealed_reaction_vessel',
      output: 'kubejs:sealed_reaction_vessel',
      authoritative: true,
      pattern: ['CPC', 'FIF', 'CTC'],
      key: {
        C: 'pneumaticcraft:ingot_iron_compressed',
        P: 'immersiveengineering:fluid_pipe',
        F: 'kubejs:pressure_treated_frame',
        I: 'kubejs:industrial_frame',
        T: 'pneumaticcraft:pressure_tube'
      }
    },
    {
      id: 'kubejs:mid_path/gas_distribution_rack',
      output: 'kubejs:gas_distribution_rack',
      authoritative: true,
      pattern: ['TCT', 'BEB', 'TCT'],
      key: {
        T: 'pneumaticcraft:pressure_tube',
        C: 'minecraft:copper_ingot',
        B: 'mekanism:basic_control_circuit',
        E: 'kubejs:electrical_bus'
      }
    },
    {
      id: 'kubejs:mid_path/process_control_board',
      output: 'kubejs:process_control_board',
      authoritative: true,
      pattern: ['PDP', 'ACA', 'PEP'],
      key: {
        P: 'pneumaticcraft:printed_circuit_board',
        D: 'modern_industrialization:digital_circuit',
        A: 'immersiveengineering:component_electronic_adv',
        C: 'kubejs:calibrated_substrate',
        E: 'kubejs:etched_copper_substrate'
      }
    },
    {
      id: 'kubejs:mid_path/pressure_manifold',
      output: 'kubejs:pressure_manifold',
      authoritative: true,
      pattern: ['VRV', 'PIP', 'VGV'],
      key: {
        V: 'kubejs:sealed_reaction_vessel',
        R: 'kubejs:gas_distribution_rack',
        P: 'immersiveengineering:fluid_pipe',
        I: 'kubejs:industrial_frame',
        G: 'pneumaticcraft:pressure_tube'
      }
    },
    {
      id: 'kubejs:mid_path/mekanism_steel_casing',
      output: 'mekanism:steel_casing',
      authoritative: true,
      pattern: ['SRS', 'FIF', 'SBS'],
      key: {
        S: 'modern_industrialization:steel_plate',
        R: 'kubejs:gas_distribution_rack',
        F: 'kubejs:pressure_treated_frame',
        I: 'kubejs:industrial_frame',
        B: 'mekanism:basic_control_circuit'
      }
    },
    {
      id: 'kubejs:mid_path/precision_circuit',
      output: 'kubejs:precision_circuit',
      authoritative: true,
      pattern: ['SPS', 'BIB', 'SHS'],
      key: {
        S: 'kubejs:signal_backplane',
        P: 'kubejs:process_control_board',
        B: 'mekanism:steel_casing',
        I: 'kubejs:industrial_frame',
        H: 'kubejs:eden_seal'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 8 — Industrial Scale
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:mid_path/parallel_machine_bus',
      output: 'kubejs:parallel_machine_bus',
      authoritative: true,
      pattern: ['ESE', 'BCB', 'EPE'],
      key: {
        E: 'kubejs:electrical_bus',
        S: 'kubejs:signal_backplane',
        B: 'kubejs:low_voltage_busbar',
        C: 'kubejs:process_control_board',
        P: 'minecraft:repeater'
      }
    },
    {
      id: 'kubejs:mid_path/fluid_safety_block',
      output: 'kubejs:fluid_safety_block',
      authoritative: true,
      pattern: ['PHP', 'MCM', 'PFP'],
      key: {
        P: 'immersiveengineering:fluid_pipe',
        H: 'minecraft:hopper',
        M: 'kubejs:pressure_manifold',
        C: 'minecraft:comparator',
        F: 'kubejs:field_engineering_kit'
      }
    },
    {
      id: 'kubejs:mid_path/maintenance_access_frame',
      output: 'kubejs:maintenance_access_frame',
      authoritative: true,
      pattern: ['PIP', 'LTL', 'PFP'],
      key: {
        P: 'kubejs:pressure_treated_frame',
        I: 'kubejs:industrial_frame',
        L: 'kubejs:structural_lattice',
        T: 'minecraft:iron_trapdoor',
        F: 'kubejs:field_tool_frame'
      }
    },
    {
      id: 'kubejs:mid_path/chemical_reactor_core',
      output: 'kubejs:chemical_reactor_core',
      authoritative: true,
      pattern: ['PAP', 'RCR', 'PWP'],
      key: {
        P: 'kubejs:process_control_board',
        A: 'immersiveengineering:component_electronic_adv',
        R: 'kubejs:gas_distribution_rack',
        C: 'kubejs:precision_circuit',
        W: 'kubejs:wildwood_seal'
      }
    },
    {
      id: 'kubejs:mid_path/industrial_foregoing_advanced_frame',
      output: 'industrialforegoing:machine_frame_advanced',
      authoritative: true,
      pattern: ['PMP', 'FIF', 'PAP'],
      key: {
        P: 'industrialforegoing:plastic',
        M: 'kubejs:maintenance_access_frame',
        F: 'industrialforegoing:machine_frame_simple',
        I: 'kubejs:industrial_frame',
        A: 'mekanism:advanced_control_circuit'
      }
    },
    {
      id: 'kubejs:mid_path/chemical_processor',
      output: 'kubejs:chemical_processor',
      authoritative: true,
      pattern: ['BSB', 'RCR', 'BHB'],
      key: {
        B: 'kubejs:parallel_machine_bus',
        S: 'kubejs:fluid_safety_block',
        R: 'kubejs:chemical_reactor_core',
        C: 'industrialforegoing:machine_frame_advanced',
        H: 'kubejs:wildwood_seal'
      }
    }
  ]

  var registered = 0
  definitions.forEach(function(definition) {
    registered += midPathRegister(event, definition) ? 1 : 0
  })
  console.info('[MidStagePaths] Registered ' + registered + '/' + definitions.length +
    ' staged manufacturing recipes.')
})
