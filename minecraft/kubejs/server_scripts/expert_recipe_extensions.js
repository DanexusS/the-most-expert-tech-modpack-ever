var ExpertExtensionResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var ExpertExtensionRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')

var EXPERT_EXTENSION_ITEM_CACHE = Object.create(null)

function expertExtensionItemExists(itemId) {
  if (Object.prototype.hasOwnProperty.call(EXPERT_EXTENSION_ITEM_CACHE, itemId)) {
    return EXPERT_EXTENSION_ITEM_CACHE[itemId]
  }

  var exists = false
  try {
    exists = ExpertExtensionRegistries.ITEM.containsKey(
      ExpertExtensionResourceLocation.parse(itemId)
    )
  } catch (error) {
    exists = false
  }

  EXPERT_EXTENSION_ITEM_CACHE[itemId] = exists
  return exists
}

function expertExtensionAllItemsExist(items) {
  for (var index = 0; index < items.length; index++) {
    if (!expertExtensionItemExists(items[index])) {
      return false
    }
  }
  return true
}

function registerExpertExtensionRecipe(event, definition) {
  var ingredients = Object.keys(definition.key).map(function(symbol) {
    return definition.key[symbol]
  })
  var required = [definition.output].concat(ingredients)

  if (!expertExtensionAllItemsExist(required)) {
    console.warn('[ExpertRecipeExtensions] Skipped ' + definition.id + ': unavailable item ID.')
    return
  }

  event.remove({ output: definition.output })
  event.shaped(definition.output, definition.pattern, definition.key).id(definition.id)
}

ServerEvents.recipes(function(event) {
  var recipes = [
    // Large-scale energy storage becomes part of the digital/quantum stage.
    {
      id: 'kubejs:expert_extension/mekanism_induction_casing',
      output: 'mekanism:induction_casing',
      authoritative: true,
      pattern: ['SCS', 'PQP', 'SCS'],
      key: {
        S: 'mekanism:ingot_refined_obsidian',
        C: 'mekanism:elite_control_circuit',
        P: 'ae2:engineering_processor',
        Q: 'kubejs:quantum_logic'
      }
    },

    // Cross-dimensional AE2 networking is no longer unlocked by AE2 alone.
    {
      id: 'kubejs:expert_extension/ae2_quantum_ring',
      output: 'ae2:quantum_ring',
      authoritative: true,
      pattern: ['FEF', 'QIQ', 'FEF'],
      key: {
        F: 'ae2:fluix_crystal',
        E: 'ae2:engineering_processor',
        Q: 'kubejs:quantum_logic',
        I: 'minecraft:ender_eye'
      }
    },

    // Nitro energizing requires the common resonant energy milestone.
    {
      id: 'kubejs:expert_extension/powah_energizing_rod_nitro',
      output: 'powah:energizing_rod_nitro',
      authoritative: true,
      pattern: ['NCN', 'RER', 'NQN'],
      key: {
        N: 'powah:crystal_nitro',
        C: 'powah:capacitor_nitro',
        R: 'powah:energizing_rod_niotic',
        E: 'kubejs:resonant_core',
        Q: 'mekanism:ultimate_control_circuit'
      }
    },

    // Supreme resource processing is tied to the bioindustrial milestone.
    {
      id: 'kubejs:expert_extension/industrial_foregoing_supreme_frame',
      output: 'industrialforegoing:machine_frame_supreme',
      authoritative: true,
      pattern: ['NUN', 'ABA', 'NUN'],
      key: {
        N: 'minecraft:netherite_ingot',
        U: 'mekanism:ultimate_control_circuit',
        A: 'industrialforegoing:machine_frame_advanced',
        B: 'kubejs:bioindustrial_matrix'
      }
    },

    // Antimatter production is a late energy-and-chemistry project.
    {
      id: 'kubejs:expert_extension/mekanism_sps_casing',
      output: 'mekanism:sps_casing',
      authoritative: true,
      pattern: ['PUP', 'IRI', 'PUP'],
      key: {
        P: 'mekanism:pellet_polonium',
        U: 'mekanism:ultimate_control_circuit',
        I: 'mekanism:induction_casing',
        R: 'kubejs:resonant_core'
      }
    },

    // Awakened infrastructure must follow the dedicated draconic processor.
    {
      id: 'kubejs:expert_extension/draconic_awakened_core',
      output: 'draconicevolution:awakened_core',
      authoritative: true,
      pattern: ['AWA', 'PWP', 'ANA'],
      key: {
        A: 'draconicevolution:awakened_draconium_ingot',
        W: 'draconicevolution:wyvern_core',
        P: 'kubejs:draconic_processor',
        N: 'minecraft:nether_star'
      }
    },

    // The highest Extended Crafting table joins the draconic production era.
    {
      id: 'kubejs:expert_extension/extendedcrafting_ultimate_table',
      output: 'extendedcrafting:ultimate_table',
      authoritative: true,
      pattern: ['UCU', 'TPT', 'UEU'],
      key: {
        U: 'extendedcrafting:ultimate_component',
        C: 'extendedcrafting:ultimate_catalyst',
        T: 'extendedcrafting:elite_table',
        P: 'kubejs:draconic_processor',
        E: 'minecraft:ender_eye'
      }
    },

    // EMC automation follows the reusable transmutation milestone.
    {
      id: 'kubejs:expert_extension/projecte_transmutation_table',
      output: 'projecte:transmutation_table',
      authoritative: true,
      pattern: ['DOD', 'PMP', 'DOD'],
      key: {
        D: 'projecte:dark_matter_block',
        O: 'minecraft:obsidian',
        P: 'projecte:philosophers_stone',
        M: 'kubejs:transmutation_matrix'
      }
    }
  ]

  recipes.forEach(function(recipe) {
    registerExpertExtensionRecipe(event, recipe)
  })

  console.info('[ExpertRecipeExtensions] Registered strategic midgame and endgame gates.')
})
