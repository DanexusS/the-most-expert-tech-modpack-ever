var ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var BuiltInRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')

function expertItemExists(itemId) {
  try {
    return BuiltInRegistries.ITEM.containsKey(ResourceLocation.parse(itemId))
  } catch (error) {
    return false
  }
}

function expertAllItemsExist(items) {
  for (var index = 0; index < items.length; index++) {
    if (!expertItemExists(items[index])) {
      return false
    }
  }
  return true
}

function registerExpertShaped(event, definition) {
  var ingredientIds = Object.keys(definition.key).map(function(symbol) {
    return definition.key[symbol]
  })
  var required = [definition.output].concat(ingredientIds)

  if (!expertAllItemsExist(required)) {
    console.warn('[ExpertRecipes] Skipped ' + definition.id + ': one or more item IDs are unavailable.')
    return
  }

  if (definition.replace === true) {
    event.remove({ output: definition.output })
  }

  event.shaped(definition.output, definition.pattern, definition.key).id(definition.id)
}

ServerEvents.recipes(function(event) {
  var recipes = [
    {
      id: 'kubejs:expert/mechanical_core',
      output: 'kubejs:mechanical_core',
      pattern: ['ICI', 'MPM', 'IQI'],
      key: {
        I: 'immersiveengineering:component_iron',
        C: 'create:andesite_alloy',
        M: 'modern_industrialization:motor',
        P: 'create:precision_mechanism',
        Q: 'actuallyadditions:black_quartz'
      }
    },
    {
      id: 'kubejs:expert/industrial_frame',
      output: 'kubejs:industrial_frame',
      pattern: ['SDS', 'CMC', 'SPS'],
      key: {
        S: 'immersiveengineering:component_steel',
        D: 'kubejs:divine_seal',
        C: 'pneumaticcraft:ingot_iron_compressed',
        M: 'kubejs:mechanical_core',
        P: 'modern_industrialization:basic_machine_hull'
      }
    },
    {
      id: 'kubejs:expert/precision_circuit',
      output: 'kubejs:precision_circuit',
      pattern: ['LEL', 'CIC', 'LHL'],
      key: {
        L: 'ae2:logic_processor',
        E: 'modern_industrialization:electronic_circuit',
        C: 'mekanism:basic_control_circuit',
        I: 'kubejs:industrial_frame',
        H: 'kubejs:eden_seal'
      }
    },
    {
      id: 'kubejs:expert/chemical_processor',
      output: 'kubejs:chemical_processor',
      pattern: ['PAP', 'CIC', 'PWP'],
      key: {
        P: 'pneumaticcraft:printed_circuit_board',
        A: 'immersiveengineering:component_electronic_adv',
        C: 'mekanism:advanced_control_circuit',
        I: 'kubejs:precision_circuit',
        W: 'kubejs:wildwood_seal'
      }
    },
    {
      id: 'kubejs:expert/bioindustrial_matrix',
      output: 'kubejs:bioindustrial_matrix',
      pattern: ['SAS', 'FCF', 'SHS'],
      key: {
        S: 'mysticalagriculture:supremium_essence',
        A: 'industrialforegoing:machine_frame_advanced',
        F: 'industrialforegoing:plastic',
        C: 'kubejs:chemical_processor',
        H: 'kubejs:apalachia_seal'
      }
    },
    {
      id: 'kubejs:expert/quantum_logic',
      output: 'kubejs:quantum_logic',
      pattern: ['EDE', 'BQB', 'EHE'],
      key: {
        E: 'ae2:engineering_processor',
        D: 'modern_industrialization:digital_circuit',
        B: 'mekanism:elite_control_circuit',
        Q: 'kubejs:bioindustrial_matrix',
        H: 'kubejs:skythern_seal'
      }
    },
    {
      id: 'kubejs:expert/resonant_core',
      output: 'kubejs:resonant_core',
      pattern: ['NUN', 'DQD', 'NMN'],
      key: {
        N: 'powah:crystal_nitro',
        U: 'mekanism:ultimate_control_circuit',
        D: 'draconicevolution:draconium_core',
        Q: 'kubejs:quantum_logic',
        M: 'kubejs:mortum_seal'
      }
    },
    {
      id: 'kubejs:expert/draconic_processor',
      output: 'kubejs:draconic_processor',
      pattern: ['UWU', 'RCR', 'UHU'],
      key: {
        U: 'extendedcrafting:ultimate_component',
        W: 'draconicevolution:wyvern_core',
        R: 'draconicevolution:awakened_draconium_ingot',
        C: 'kubejs:resonant_core',
        H: 'kubejs:vethea_seal'
      }
    },
    {
      id: 'kubejs:expert/transmutation_matrix',
      output: 'kubejs:transmutation_matrix',
      pattern: ['DUD', 'PCP', 'DTD'],
      key: {
        D: 'projecte:dark_matter',
        U: 'extendedcrafting:ultimate_singularity',
        P: 'projecte:philosophers_stone',
        C: 'kubejs:draconic_processor',
        T: 'kubejs:wreck_seal'
      }
    },
    {
      id: 'kubejs:expert/cosmic_catalyst',
      output: 'kubejs:cosmic_catalyst',
      pattern: ['AMA', 'CTC', 'ALA'],
      key: {
        A: 'avaritia:crystal_matrix_ingot',
        M: 'draconicevolution:awakened_core',
        C: 'extendedcrafting:ultimate_catalyst',
        T: 'kubejs:transmutation_matrix',
        L: 'kubejs:lunar_seal'
      }
    },

    // Key progression recipes. Only these strategic machines are replaced;
    // decorative and routine components remain untouched.
    {
      id: 'kubejs:expert/mekanism_steel_casing',
      output: 'mekanism:steel_casing',
      replace: true,
      pattern: ['SIS', 'ICI', 'SIS'],
      key: {
        S: 'immersiveengineering:ingot_steel',
        I: 'modern_industrialization:steel_ingot',
        C: 'kubejs:industrial_frame'
      }
    },
    {
      id: 'kubejs:expert/industrial_foregoing_advanced_frame',
      output: 'industrialforegoing:machine_frame_advanced',
      replace: true,
      pattern: ['PDP', 'FIF', 'PMP'],
      key: {
        P: 'industrialforegoing:plastic',
        D: 'minecraft:diamond',
        F: 'industrialforegoing:machine_frame_simple',
        I: 'kubejs:industrial_frame',
        M: 'mekanism:advanced_control_circuit'
      }
    },
    {
      id: 'kubejs:expert/ae2_controller',
      output: 'ae2:controller',
      replace: true,
      pattern: ['SFS', 'LQL', 'SFS'],
      key: {
        S: 'ae2:smooth_sky_stone_block',
        F: 'ae2:fluix_crystal',
        L: 'ae2:engineering_processor',
        Q: 'kubejs:quantum_logic'
      }
    },
    {
      id: 'kubejs:expert/powah_nitro_reactor',
      output: 'powah:reactor_nitro',
      replace: true,
      pattern: ['NCN', 'RER', 'NQN'],
      key: {
        N: 'powah:crystal_nitro',
        C: 'powah:capacitor_nitro',
        R: 'powah:reactor_spirited',
        E: 'kubejs:resonant_core',
        Q: 'mekanism:ultimate_control_circuit'
      }
    },
    {
      id: 'kubejs:expert/draconic_wyvern_core',
      output: 'draconicevolution:wyvern_core',
      replace: true,
      pattern: ['DED', 'ERE', 'DED'],
      key: {
        D: 'draconicevolution:draconium_ingot',
        E: 'minecraft:ender_eye',
        R: 'kubejs:resonant_core'
      }
    },
    {
      id: 'kubejs:expert/projecte_philosophers_stone',
      output: 'projecte:philosophers_stone',
      replace: true,
      pattern: ['AUA', 'NPN', 'ATA'],
      key: {
        A: 'draconicevolution:awakened_draconium_ingot',
        U: 'extendedcrafting:ultimate_component',
        N: 'minecraft:nether_star',
        P: 'kubejs:draconic_processor',
        T: 'divinerpg:dungeon_tokens'
      }
    },
    {
      id: 'kubejs:expert/avaritia_extreme_crafting_table',
      output: 'avaritia:extreme_crafting_table',
      replace: true,
      pattern: ['CMC', 'MTM', 'CMC'],
      key: {
        C: 'avaritia:crystal_matrix_ingot',
        M: 'avaritia:double_compressed_crafting_table',
        T: 'kubejs:cosmic_catalyst'
      }
    },
    {
      id: 'kubejs:expert/mystical_agriculture_infusion_altar',
      output: 'mysticalagriculture:infusion_altar',
      replace: true,
      pattern: ['PSP', 'FIF', 'SSS'],
      key: {
        P: 'mysticalagriculture:prosperity_shard',
        S: 'minecraft:stone',
        F: 'immersiveengineering:component_iron',
        I: 'kubejs:industrial_frame'
      }
    }
  ]

  recipes.forEach(function(recipe) {
    registerExpertShaped(event, recipe)
  })

  console.info('[ExpertRecipes] Cross-mod expert progression recipes registered.')
})
