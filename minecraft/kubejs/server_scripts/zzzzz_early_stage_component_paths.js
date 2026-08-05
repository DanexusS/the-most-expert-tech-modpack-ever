// Authoritative multi-step recipe paths for the first four progression stages.
// These recipes replace direct milestone crafts with consumable assemblies and
// reusable engineering standards. Difficulty comes from building several small
// production lines, not from multiplying raw ingot counts or waiting manually.

var EarlyPathLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var EarlyPathRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
var EARLY_PATH_CACHE = Object.create(null)

function earlyPathExists(itemId) {
  if (Object.prototype.hasOwnProperty.call(EARLY_PATH_CACHE, itemId)) {
    return EARLY_PATH_CACHE[itemId]
  }
  var exists = false
  try {
    exists = EarlyPathRegistries.ITEM.containsKey(EarlyPathLocation.parse(itemId))
  } catch (error) {
    exists = false
  }
  EARLY_PATH_CACHE[itemId] = exists
  return exists
}

function earlyPathRegister(event, definition) {
  var required = [definition.output].concat(Object.keys(definition.key).map(function(symbol) {
    return definition.key[symbol]
  }))
  for (var index = 0; index < required.length; index++) {
    if (!earlyPathExists(required[index])) {
      console.warn('[EarlyStagePaths] Kept previous path for ' + definition.output +
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
    // Stage 1 — Field Foundations
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:early_path/survey_lens',
      output: 'kubejs:survey_lens',
      authoritative: true,
      pattern: ['GQG', 'CAC', 'GQG'],
      key: {
        G: 'minecraft:glass_pane',
        Q: 'minecraft:quartz',
        C: 'minecraft:copper_ingot',
        A: 'minecraft:amethyst_shard'
      }
    },
    {
      id: 'kubejs:early_path/insulated_wiring_bundle',
      output: 'kubejs:insulated_wiring_bundle',
      authoritative: true,
      pattern: ['CRC', 'RPR', 'CRC'],
      key: {
        C: 'minecraft:copper_ingot',
        R: 'minecraft:redstone',
        P: 'minecraft:paper'
      }
    },
    {
      id: 'kubejs:early_path/field_tool_frame',
      output: 'kubejs:field_tool_frame',
      authoritative: true,
      pattern: ['ILI', 'LCL', 'IHI'],
      key: {
        I: 'immersiveengineering:component_iron',
        L: 'minecraft:leather',
        C: 'minecraft:copper_ingot',
        H: 'minecraft:iron_ingot'
      }
    },
    {
      id: 'kubejs:early_path/manual_control_board',
      output: 'kubejs:manual_control_board',
      authoritative: true,
      pattern: ['QRQ', 'CBC', 'QRQ'],
      key: {
        Q: 'minecraft:quartz',
        R: 'minecraft:redstone',
        C: 'minecraft:comparator',
        B: 'actuallyadditions:black_quartz'
      }
    },
    {
      id: 'kubejs:early_path/materials_analysis_matrix',
      output: 'kubejs:materials_analysis_matrix',
      authoritative: true,
      pattern: ['LSL', 'BCB', 'LQL'],
      key: {
        L: 'kubejs:survey_lens',
        S: 'minecraft:spyglass',
        B: 'kubejs:manual_control_board',
        C: 'minecraft:copper_ingot',
        Q: 'minecraft:quartz'
      }
    },
    {
      id: 'kubejs:early_path/power_regulation_unit',
      output: 'kubejs:power_regulation_unit',
      authoritative: true,
      pattern: ['WBW', 'CMC', 'WBW'],
      key: {
        W: 'kubejs:insulated_wiring_bundle',
        B: 'kubejs:manual_control_board',
        C: 'minecraft:copper_ingot',
        M: 'modern_industrialization:motor'
      }
    },
    {
      id: 'kubejs:early_path/field_engineering_kit',
      output: 'kubejs:field_engineering_kit',
      authoritative: true,
      pattern: ['FTF', 'WLW', 'FIF'],
      key: {
        F: 'kubejs:field_tool_frame',
        T: 'kubejs:survey_lens',
        W: 'kubejs:insulated_wiring_bundle',
        L: 'minecraft:leather',
        I: 'immersiveengineering:component_iron'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 2 — Steam and Metallurgy
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:early_path/refractory_binder',
      output: 'kubejs:refractory_binder',
      authoritative: true,
      pattern: ['CBC', 'BGB', 'CBC'],
      key: {
        C: 'minecraft:clay_ball',
        B: 'minecraft:brick',
        G: 'minecraft:gravel'
      }
    },
    {
      id: 'kubejs:early_path/steam_valve_assembly',
      output: 'kubejs:steam_valve_assembly',
      authoritative: true,
      pattern: ['CBC', 'VFV', 'CBC'],
      key: {
        C: 'minecraft:copper_ingot',
        B: 'modern_industrialization:bronze_ingot',
        V: 'minecraft:iron_bars',
        F: 'kubejs:field_engineering_kit'
      }
    },
    {
      id: 'kubejs:early_path/metallurgical_bracing',
      output: 'kubejs:metallurgical_bracing',
      authoritative: true,
      pattern: ['ICI', 'BFB', 'ICI'],
      key: {
        I: 'immersiveengineering:component_iron',
        C: 'minecraft:copper_ingot',
        B: 'minecraft:iron_bars',
        F: 'kubejs:field_engineering_kit'
      }
    },
    {
      id: 'kubejs:early_path/structural_lattice',
      output: 'kubejs:structural_lattice',
      authoritative: true,
      pattern: ['BMB', 'GFG', 'BMB'],
      key: {
        B: 'kubejs:metallurgical_bracing',
        M: 'minecraft:iron_bars',
        G: 'minecraft:glass',
        F: 'kubejs:field_engineering_kit'
      }
    },
    {
      id: 'kubejs:early_path/bronze_boiler',
      output: 'modern_industrialization:bronze_boiler',
      authoritative: true,
      pattern: ['BVB', 'LFL', 'BVB'],
      key: {
        B: 'modern_industrialization:bronze_ingot',
        V: 'kubejs:steam_valve_assembly',
        L: 'kubejs:structural_lattice',
        F: 'minecraft:furnace'
      }
    },
    {
      id: 'kubejs:early_path/reinforced_blastbrick',
      output: 'immersiveengineering:blastbrick_reinforced',
      authoritative: true,
      pattern: ['SBS', 'RLR', 'SBS'],
      key: {
        S: 'modern_industrialization:steel_plate',
        B: 'immersiveengineering:blastbrick',
        R: 'kubejs:refractory_binder',
        L: 'kubejs:structural_lattice'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 3 — Regulated Electricity
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:early_path/low_voltage_busbar',
      output: 'kubejs:low_voltage_busbar',
      authoritative: true,
      pattern: ['CEC', 'WPW', 'CEC'],
      key: {
        C: 'minecraft:copper_ingot',
        E: 'immersiveengineering:component_electronic',
        W: 'kubejs:insulated_wiring_bundle',
        P: 'kubejs:power_regulation_unit'
      }
    },
    {
      id: 'kubejs:early_path/circuit_protection_module',
      output: 'kubejs:circuit_protection_module',
      authoritative: true,
      pattern: ['QRQ', 'CBC', 'QEQ'],
      key: {
        Q: 'minecraft:quartz',
        R: 'minecraft:redstone',
        C: 'minecraft:comparator',
        B: 'kubejs:manual_control_board',
        E: 'immersiveengineering:component_electronic'
      }
    },
    {
      id: 'kubejs:early_path/reserve_switchgear',
      output: 'kubejs:reserve_switchgear',
      authoritative: true,
      pattern: ['IBI', 'PCP', 'IBI'],
      key: {
        I: 'minecraft:iron_ingot',
        B: 'kubejs:low_voltage_busbar',
        P: 'kubejs:circuit_protection_module',
        C: 'minecraft:copper_block'
      }
    },
    {
      id: 'kubejs:early_path/electrical_bus',
      output: 'kubejs:electrical_bus',
      authoritative: true,
      pattern: ['BLB', 'PCP', 'BLB'],
      key: {
        B: 'kubejs:low_voltage_busbar',
        L: 'immersiveengineering:component_electronic',
        P: 'kubejs:circuit_protection_module',
        C: 'kubejs:power_regulation_unit'
      }
    },
    {
      id: 'kubejs:early_path/basic_machine_hull',
      output: 'modern_industrialization:basic_machine_hull',
      authoritative: true,
      pattern: ['SRS', 'EBE', 'SMS'],
      key: {
        S: 'modern_industrialization:steel_plate',
        R: 'kubejs:reserve_switchgear',
        E: 'modern_industrialization:electronic_circuit',
        B: 'kubejs:electrical_bus',
        M: 'modern_industrialization:motor'
      }
    },
    {
      id: 'kubejs:early_path/mechanical_core',
      output: 'kubejs:mechanical_core',
      authoritative: true,
      pattern: ['RLR', 'EBE', 'RMR'],
      key: {
        R: 'kubejs:reserve_switchgear',
        L: 'kubejs:structural_lattice',
        E: 'kubejs:electrical_bus',
        B: 'modern_industrialization:basic_machine_hull',
        M: 'modern_industrialization:motor'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 4 — Kinetic Automation
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:early_path/stress_sensor',
      output: 'kubejs:stress_sensor',
      authoritative: true,
      pattern: ['RCR', 'GMG', 'RCR'],
      key: {
        R: 'minecraft:repeater',
        C: 'minecraft:comparator',
        G: 'create:cogwheel',
        M: 'kubejs:mechanical_core'
      }
    },
    {
      id: 'kubejs:early_path/gearbox_alignment_frame',
      output: 'kubejs:gearbox_alignment_frame',
      authoritative: true,
      pattern: ['AGA', 'BIB', 'AGA'],
      key: {
        A: 'create:andesite_alloy',
        G: 'create:large_cogwheel',
        B: 'kubejs:metallurgical_bracing',
        I: 'minecraft:iron_bars'
      }
    },
    {
      id: 'kubejs:early_path/sequencing_cam',
      output: 'kubejs:sequencing_cam',
      authoritative: true,
      pattern: ['ETE', 'GCG', 'ESE'],
      key: {
        E: 'minecraft:iron_nugget',
        T: 'create:electron_tube',
        G: 'create:golden_sheet',
        C: 'kubejs:manual_control_board',
        S: 'kubejs:stress_sensor'
      }
    },
    {
      id: 'kubejs:early_path/kinetic_regulator',
      output: 'kubejs:kinetic_regulator',
      authoritative: true,
      pattern: ['SGS', 'RMR', 'SFS'],
      key: {
        S: 'kubejs:stress_sensor',
        G: 'create:gearshift',
        R: 'kubejs:gearbox_alignment_frame',
        M: 'kubejs:mechanical_core',
        F: 'kubejs:field_engineering_kit'
      }
    },
    {
      id: 'kubejs:early_path/precision_mechanism',
      output: 'create:precision_mechanism',
      authoritative: true,
      pattern: ['GCG', 'TRT', 'NEN'],
      key: {
        G: 'create:golden_sheet',
        C: 'kubejs:sequencing_cam',
        T: 'create:electron_tube',
        R: 'kubejs:kinetic_regulator',
        N: 'minecraft:iron_nugget',
        E: 'create:large_cogwheel'
      }
    },
    {
      id: 'kubejs:early_path/kinetic_interface',
      output: 'kubejs:kinetic_interface',
      authoritative: true,
      pattern: ['ARA', 'PMP', 'AIA'],
      key: {
        A: 'create:andesite_alloy',
        R: 'kubejs:gearbox_alignment_frame',
        P: 'create:precision_mechanism',
        M: 'kubejs:mechanical_core',
        I: 'kubejs:kinetic_regulator'
      }
    }
  ]

  var registered = 0
  definitions.forEach(function(definition) {
    registered += earlyPathRegister(event, definition) ? 1 : 0
  })
  console.info('[EarlyStagePaths] Registered ' + registered + '/' + definitions.length +
    ' fair multi-step stage recipes.')
})
