// Authoritative multi-step recipe paths for progression stages 13–18.
// Each milestone consumes the output of several independent production branches
// so the quest DAG and the real crafting graph describe the same factory.

var LatePathLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var LatePathRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
var LATE_PATH_CACHE = Object.create(null)

function latePathExists(itemId) {
  if (Object.prototype.hasOwnProperty.call(LATE_PATH_CACHE, itemId)) {
    return LATE_PATH_CACHE[itemId]
  }
  var exists = false
  try {
    exists = LatePathRegistries.ITEM.containsKey(LatePathLocation.parse(itemId))
  } catch (error) {
    exists = false
  }
  LATE_PATH_CACHE[itemId] = exists
  return exists
}

function latePathRegister(event, definition) {
  var required = [definition.output].concat(Object.keys(definition.key).map(function(symbol) {
    return definition.key[symbol]
  }))
  for (var index = 0; index < required.length; index++) {
    if (!latePathExists(required[index])) {
      console.warn('[LateStagePaths] Kept previous path for ' + definition.output +
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
    // Stage 13 — Dimensional Materials
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:late_path/expedition_supply_frame',
      output: 'kubejs:expedition_supply_frame',
      authoritative: true,
      pattern: ['SRS', 'QFQ', 'SAS'],
      key: {
        S: 'minecraft:shulker_box',
        R: 'kubejs:resonant_core',
        Q: 'kubejs:quantum_logic',
        F: 'kubejs:antimatter_regulator',
        A: 'kubejs:skythern_seal'
      }
    },
    {
      id: 'kubejs:late_path/trophy_assay_module',
      output: 'kubejs:trophy_assay_module',
      authoritative: true,
      pattern: ['DMD', 'RAR', 'DTD'],
      key: {
        D: 'divinerpg:dungeon_tokens',
        M: 'kubejs:materials_analysis_matrix',
        R: 'minecraft:recovery_compass',
        A: 'kubejs:mortum_seal',
        T: 'minecraft:tinted_glass'
      }
    },
    {
      id: 'kubejs:late_path/dimensional_cargo_anchor',
      output: 'kubejs:dimensional_cargo_anchor',
      authoritative: true,
      pattern: ['EAE', 'QLQ', 'EFE'],
      key: {
        E: 'minecraft:ender_eye',
        A: 'kubejs:antimatter_regulator',
        Q: 'ae2:quantum_ring',
        L: 'minecraft:lodestone',
        F: 'kubejs:expedition_supply_frame'
      }
    },
    {
      id: 'kubejs:late_path/dimensional_resonator',
      output: 'kubejs:dimensional_resonator',
      authoritative: true,
      pattern: ['FAT', 'RCR', 'FDF'],
      key: {
        F: 'kubejs:expedition_supply_frame',
        A: 'kubejs:trophy_assay_module',
        T: 'kubejs:dimensional_cargo_anchor',
        R: 'kubejs:resonant_core',
        C: 'kubejs:antimatter_regulator',
        D: 'kubejs:divine_seal'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 14 — Draconic Engineering
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:late_path/injector_alignment_core',
      output: 'kubejs:injector_alignment_core',
      authoritative: true,
      pattern: ['WUW', 'RDR', 'WUW'],
      key: {
        W: 'draconicevolution:wyvern_core',
        U: 'extendedcrafting:ultimate_component',
        R: 'kubejs:dimensional_resonator',
        D: 'draconicevolution:draconium_core'
      }
    },
    {
      id: 'kubejs:late_path/awakened_containment_shell',
      output: 'kubejs:awakened_containment_shell',
      authoritative: true,
      pattern: ['AOA', 'RDR', 'AOA'],
      key: {
        A: 'draconicevolution:awakened_draconium_ingot',
        O: 'minecraft:crying_obsidian',
        R: 'kubejs:dimensional_resonator',
        D: 'draconicevolution:wyvern_core'
      }
    },
    {
      id: 'kubejs:late_path/draconic_energy_coupler',
      output: 'kubejs:draconic_energy_coupler',
      authoritative: true,
      pattern: ['DUD', 'RCR', 'DUD'],
      key: {
        D: 'draconicevolution:draconium_core',
        U: 'mekanism:ultimate_control_circuit',
        R: 'kubejs:resonant_core',
        C: 'kubejs:dimensional_resonator'
      }
    },
    {
      id: 'kubejs:late_path/draconic_processor',
      output: 'kubejs:draconic_processor',
      authoritative: true,
      pattern: ['IAC', 'RLR', 'IHC'],
      key: {
        I: 'kubejs:injector_alignment_core',
        A: 'kubejs:awakened_containment_shell',
        C: 'kubejs:draconic_energy_coupler',
        R: 'draconicevolution:awakened_draconium_ingot',
        L: 'kubejs:draconic_lattice',
        H: 'kubejs:vethea_seal'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 15 — Contained Transmutation
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:late_path/emc_accounting_ledger',
      output: 'kubejs:emc_accounting_ledger',
      authoritative: true,
      pattern: ['DBD', 'PMP', 'DBD'],
      key: {
        D: 'projecte:dark_matter',
        B: 'minecraft:book',
        P: 'projecte:philosophers_stone',
        M: 'kubejs:materials_analysis_matrix'
      }
    },
    {
      id: 'kubejs:late_path/matter_compression_frame',
      output: 'kubejs:matter_compression_frame',
      authoritative: true,
      pattern: ['DUD', 'APA', 'DUD'],
      key: {
        D: 'projecte:dark_matter_block',
        U: 'extendedcrafting:ultimate_component',
        A: 'kubejs:awakened_containment_shell',
        P: 'kubejs:draconic_processor'
      }
    },
    {
      id: 'kubejs:late_path/transmutation_safety_lock',
      output: 'kubejs:transmutation_safety_lock',
      authoritative: true,
      pattern: ['TCT', 'PWP', 'TCT'],
      key: {
        T: 'minecraft:tripwire_hook',
        C: 'extendedcrafting:ultimate_catalyst',
        P: 'projecte:transmutation_table',
        W: 'kubejs:wreck_seal'
      }
    },
    {
      id: 'kubejs:late_path/transmutation_matrix',
      output: 'kubejs:transmutation_matrix',
      authoritative: true,
      pattern: ['LCF', 'PDP', 'LSF'],
      key: {
        L: 'kubejs:emc_accounting_ledger',
        C: 'kubejs:matter_compression_frame',
        F: 'kubejs:transmutation_safety_lock',
        P: 'kubejs:draconic_processor',
        D: 'projecte:dark_matter',
        S: 'kubejs:wreck_seal'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 16 — Extreme Fabrication
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:late_path/singularity_routing_lattice',
      output: 'kubejs:singularity_routing_lattice',
      authoritative: true,
      pattern: ['USU', 'QTQ', 'USU'],
      key: {
        U: 'extendedcrafting:ultimate_singularity',
        S: 'kubejs:quantum_bus',
        Q: 'ae2:quantum_ring',
        T: 'kubejs:transmutation_matrix'
      }
    },
    {
      id: 'kubejs:late_path/ultimate_pattern_frame',
      output: 'kubejs:ultimate_pattern_frame',
      authoritative: true,
      pattern: ['UEU', 'TXT', 'UEU'],
      key: {
        U: 'extendedcrafting:ultimate_component',
        E: 'extendedcrafting:ultimate_table',
        T: 'kubejs:transmutation_matrix',
        X: 'avaritia:extreme_crafting_table'
      }
    },
    {
      id: 'kubejs:late_path/bulk_material_manifold',
      output: 'kubejs:bulk_material_manifold',
      authoritative: true,
      pattern: ['CMC', 'QTQ', 'CMC'],
      key: {
        C: 'avaritia:crystal_matrix_ingot',
        M: 'projecte:dark_matter_block',
        Q: 'kubejs:quantum_bus',
        T: 'kubejs:transmutation_matrix'
      }
    },
    {
      id: 'kubejs:late_path/cosmic_catalyst',
      output: 'kubejs:cosmic_catalyst',
      authoritative: true,
      pattern: ['SRP', 'MTM', 'BLB'],
      key: {
        S: 'kubejs:singularity_routing_lattice',
        R: 'kubejs:ultimate_pattern_frame',
        P: 'kubejs:bulk_material_manifold',
        M: 'draconicevolution:awakened_core',
        T: 'kubejs:transmutation_matrix',
        B: 'kubejs:lunar_seal',
        L: 'extendedcrafting:ultimate_catalyst'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 17 — Cosmic Synthesis
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:late_path/stellar_sample_chamber',
      output: 'kubejs:stellar_sample_chamber',
      authoritative: true,
      pattern: ['TST', 'DCD', 'TNT'],
      key: {
        T: 'minecraft:tinted_glass',
        S: 'kubejs:dimensional_resonator',
        D: 'kubejs:cosmic_catalyst',
        C: 'minecraft:end_crystal',
        N: 'minecraft:nether_star'
      }
    },
    {
      id: 'kubejs:late_path/infinity_alloy_crucible',
      output: 'kubejs:infinity_alloy_crucible',
      authoritative: true,
      pattern: ['IAI', 'CLC', 'IAI'],
      key: {
        I: 'avaritia:infinity_ingot',
        A: 'draconicevolution:awakened_core',
        C: 'kubejs:cosmic_catalyst',
        L: 'minecraft:lava_bucket'
      }
    },
    {
      id: 'kubejs:late_path/cosmic_energy_coupler',
      output: 'kubejs:cosmic_energy_coupler',
      authoritative: true,
      pattern: ['BRB', 'DCD', 'BQB'],
      key: {
        B: 'minecraft:beacon',
        R: 'kubejs:resonant_core',
        D: 'kubejs:draconic_processor',
        C: 'kubejs:cosmic_catalyst',
        Q: 'kubejs:quantum_logic'
      }
    },
    {
      id: 'kubejs:late_path/cosmic_synthesis_core',
      output: 'kubejs:cosmic_synthesis_core',
      authoritative: true,
      pattern: ['SCI', 'LCL', 'SEC'],
      key: {
        S: 'kubejs:stellar_sample_chamber',
        C: 'kubejs:cosmic_energy_coupler',
        I: 'kubejs:infinity_alloy_crucible',
        L: 'kubejs:lunar_seal',
        E: 'kubejs:cosmic_catalyst'
      }
    },

    // ---------------------------------------------------------------------
    // Stage 18 — Creative Convergence
    // ---------------------------------------------------------------------
    {
      id: 'kubejs:late_path/creative_subsystem_key',
      output: 'kubejs:creative_subsystem_key',
      authoritative: true,
      pattern: ['QAK', 'CSC', 'QAK'],
      key: {
        Q: 'kubejs:quantum_logic',
        A: 'kubejs:antimatter_regulator',
        K: 'minecraft:knowledge_book',
        C: 'kubejs:cosmic_synthesis_core',
        S: 'kubejs:cosmic_assembly_matrix'
      }
    },
    {
      id: 'kubejs:late_path/infinite_logistics_frame',
      output: 'kubejs:infinite_logistics_frame',
      authoritative: true,
      pattern: ['AQA', 'ECE', 'AQA'],
      key: {
        A: 'ae2:controller',
        Q: 'ae2:quantum_ring',
        E: 'minecraft:ender_chest',
        C: 'kubejs:cosmic_assembly_matrix'
      }
    },
    {
      id: 'kubejs:late_path/completion_audit_seal',
      output: 'kubejs:completion_audit_seal',
      authoritative: true,
      pattern: ['KSK', 'RTR', 'KFK'],
      key: {
        K: 'kubejs:creative_subsystem_key',
        S: 'kubejs:cosmic_synthesis_core',
        R: 'minecraft:recovery_compass',
        T: 'kubejs:transmutation_matrix',
        F: 'kubejs:infinite_logistics_frame'
      }
    },
    {
      id: 'kubejs:late_path/creative_convergence_matrix',
      output: 'kubejs:creative_convergence_matrix',
      authoritative: true,
      pattern: ['KFA', 'SXS', 'KLC'],
      key: {
        K: 'kubejs:creative_subsystem_key',
        F: 'kubejs:infinite_logistics_frame',
        A: 'kubejs:completion_audit_seal',
        S: 'kubejs:cosmic_synthesis_core',
        X: 'kubejs:cosmic_assembly_matrix',
        L: 'kubejs:transmutation_matrix',
        C: 'kubejs:antimatter_regulator'
      }
    }
  ]

  var registered = 0
  definitions.forEach(function(definition) {
    registered += latePathRegister(event, definition) ? 1 : 0
  })
})
