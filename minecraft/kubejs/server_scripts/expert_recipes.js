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
  for (var i = 0; i < items.length; i++) {
    if (!expertItemExists(items[i])) return false
  }
  return true
}

function expertShaped(event, def) {
  var required = [def.output]
  Object.keys(def.key).forEach(function(k) { required.push(def.key[k]) })
  if (!expertAllItemsExist(required)) {
    console.warn('[ExpertRecipes] skipped ' + def.id + ': unavailable item id')
    return
  }
  if (def.replace) event.remove({ output: def.output })
  event.shaped(def.output, def.pattern, def.key).id(def.id)
}

ServerEvents.recipes(function(event) {
  var recipes = [
    {
      id: 'kubejs:expert/mekanism_steel_casing',
      output: 'mekanism:steel_casing',
      replace: true,
      pattern: ['SPS', 'MCM', 'SPS'],
      key: {
        S: 'immersiveengineering:ingot_steel',
        P: 'create:precision_mechanism',
        M: 'modern_industrialization:steel_ingot',
        C: 'modern_industrialization:basic_machine_hull'
      }
    },
    {
      id: 'kubejs:expert/industrial_foregoing_advanced_frame',
      output: 'industrialforegoing:machine_frame_advanced',
      replace: true,
      pattern: ['PMP', 'FCF', 'PAP'],
      key: {
        P: 'industrialforegoing:plastic',
        M: 'modern_industrialization:motor',
        F: 'industrialforegoing:machine_frame_simple',
        C: 'mekanism:advanced_control_circuit',
        A: 'create:precision_mechanism'
      }
    },
    {
      id: 'kubejs:expert/ae2_controller',
      output: 'ae2:controller',
      replace: true,
      pattern: ['SFS', 'DMD', 'SFS'],
      key: {
        S: 'ae2:smooth_sky_stone_block',
        F: 'ae2:fluix_crystal',
        D: 'modern_industrialization:digital_circuit',
        M: 'mekanism:elite_control_circuit'
      }
    },
    {
      id: 'kubejs:expert/powah_nitro_reactor',
      output: 'powah:reactor_nitro',
      replace: true,
      pattern: ['NCN', 'AEA', 'NUN'],
      key: {
        N: 'powah:crystal_nitro',
        C: 'powah:capacitor_nitro',
        A: 'ae2:engineering_processor',
        E: 'modern_industrialization:energy_input_hatch',
        U: 'mekanism:ultimate_control_circuit'
      }
    },
    {
      id: 'kubejs:expert/draconic_wyvern_core',
      output: 'draconicevolution:wyvern_core',
      replace: true,
      pattern: ['DND', 'URR', 'DND'],
      key: {
        D: 'draconicevolution:draconium_ingot',
        N: 'powah:crystal_nitro',
        U: 'mekanism:ultimate_control_circuit',
        R: 'ae2:engineering_processor'
      }
    },
    {
      id: 'kubejs:expert/projecte_philosophers_stone',
      output: 'projecte:philosophers_stone',
      replace: true,
      pattern: ['AWA', 'NUN', 'AEA'],
      key: {
        A: 'draconicevolution:awakened_draconium_ingot',
        W: 'draconicevolution:wyvern_core',
        N: 'minecraft:nether_star',
        U: 'extendedcrafting:ultimate_component',
        E: 'ae2:engineering_processor'
      }
    },
    {
      id: 'kubejs:expert/avaritia_extreme_crafting_table',
      output: 'avaritia:extreme_crafting_table',
      replace: true,
      pattern: ['CMC', 'PTP', 'CMC'],
      key: {
        C: 'avaritia:crystal_matrix_ingot',
        M: 'avaritia:double_compressed_crafting_table',
        P: 'projecte:dark_matter',
        T: 'projecte:philosophers_stone'
      }
    },
    {
      id: 'kubejs:expert/mystical_agriculture_infusion_altar',
      output: 'mysticalagriculture:infusion_altar',
      replace: true,
      pattern: ['PSP', 'FCF', 'SAS'],
      key: {
        P: 'mysticalagriculture:prosperity_shard',
        S: 'minecraft:stone',
        F: 'immersiveengineering:component_iron',
        C: 'modern_industrialization:motor',
        A: 'create:andesite_alloy'
      }
    }
  ]

  recipes.forEach(function(recipe) { expertShaped(event, recipe) })
})
