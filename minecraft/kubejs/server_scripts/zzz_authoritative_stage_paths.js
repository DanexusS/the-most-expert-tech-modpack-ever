// Additional authoritative paths for progression outputs that previously kept
// an early vanilla/mod recipe. This layer is loaded after all other expert
// recipe scripts. Missing IDs preserve the original recipe and emit a warning.

var V1PathResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var V1PathRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
var V1_PATH_CACHE = Object.create(null)

function v1PathItemExists(itemId) {
  if (Object.prototype.hasOwnProperty.call(V1_PATH_CACHE, itemId)) {
    return V1_PATH_CACHE[itemId]
  }
  var exists = false
  try {
    exists = V1PathRegistries.ITEM.containsKey(V1PathResourceLocation.parse(itemId))
  } catch (error) {
    exists = false
  }
  V1_PATH_CACHE[itemId] = exists
  return exists
}

function v1PathRegister(event, definition) {
  var required = [definition.output].concat(Object.keys(definition.key).map(function(symbol) {
    return definition.key[symbol]
  }))
  for (var index = 0; index < required.length; index++) {
    if (!v1PathItemExists(required[index])) {
      console.warn('[AuthoritativeStagePaths] Kept original ' + definition.output +
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
    // The structural standard must be craftable before powered bronze plate
    // production; otherwise the bronze boiler and lattice form a cycle.
    {
      id: 'kubejs:v1_path/structural_lattice',
      output: 'kubejs:structural_lattice',
      authoritative: true,
      pattern: ['IBI', 'GFG', 'IBI'],
      key: {
        I: 'immersiveengineering:component_iron',
        B: 'minecraft:iron_bars',
        G: 'minecraft:glass',
        F: 'kubejs:field_engineering_kit'
      }
    },
    // Correct the early calibrated substrate so it does not depend on an AE2
    // processor that itself requires the gated Inscriber.
    {
      id: 'kubejs:v1_path/calibrated_substrate',
      output: 'kubejs:calibrated_substrate',
      authoritative: true,
      pattern: ['QGQ', 'EAE', 'QRQ'],
      key: {
        Q: 'minecraft:quartz',
        G: 'minecraft:gold_ingot',
        E: 'modern_industrialization:electronic_circuit',
        A: 'kubejs:materials_analysis_matrix',
        R: 'minecraft:comparator'
      }
    },
    {
      id: 'kubejs:v1_path/ae2_inscriber',
      output: 'ae2:inscriber',
      authoritative: true,
      pattern: ['PCP', 'EME', 'PBP'],
      key: {
        P: 'minecraft:sticky_piston',
        C: 'kubejs:calibrated_substrate',
        E: 'immersiveengineering:component_electronic',
        M: 'modern_industrialization:motor',
        B: 'kubejs:electrical_bus'
      }
    },
    {
      id: 'kubejs:v1_path/ae2_drive',
      output: 'ae2:drive',
      authoritative: true,
      pattern: ['QEQ', 'BSB', 'QCQ'],
      key: {
        Q: 'ae2:quartz_glass',
        E: 'ae2:engineering_processor',
        B: 'kubejs:signal_backplane',
        S: 'ae2:fluix_glass_cable',
        C: 'kubejs:calibrated_substrate'
      }
    },
    {
      id: 'kubejs:v1_path/create_precision_mechanism',
      output: 'create:precision_mechanism',
      authoritative: true,
      pattern: ['GCG', 'TRT', 'NEN'],
      key: {
        G: 'create:golden_sheet',
        C: 'create:cogwheel',
        T: 'create:electron_tube',
        R: 'kubejs:kinetic_regulator',
        N: 'minecraft:iron_nugget',
        E: 'create:large_cogwheel'
      }
    },
    {
      id: 'kubejs:v1_path/ie_reinforced_blastbrick',
      output: 'immersiveengineering:blastbrick_reinforced',
      authoritative: true,
      pattern: ['SBS', 'BLB', 'SBS'],
      key: {
        S: 'modern_industrialization:steel_plate',
        B: 'immersiveengineering:blastbrick',
        L: 'kubejs:structural_lattice'
      }
    },
    {
      id: 'kubejs:v1_path/mi_bronze_boiler',
      output: 'modern_industrialization:bronze_boiler',
      authoritative: true,
      pattern: ['BCB', 'LFL', 'BKB'],
      key: {
        B: 'modern_industrialization:bronze_ingot',
        C: 'minecraft:copper_ingot',
        L: 'kubejs:structural_lattice',
        F: 'minecraft:furnace',
        K: 'kubejs:field_engineering_kit'
      }
    },
    {
      id: 'kubejs:v1_path/mi_basic_machine_hull',
      output: 'modern_industrialization:basic_machine_hull',
      authoritative: true,
      pattern: ['SLS', 'EBE', 'SMS'],
      key: {
        S: 'modern_industrialization:steel_plate',
        L: 'kubejs:structural_lattice',
        E: 'modern_industrialization:electronic_circuit',
        B: 'kubejs:electrical_bus',
        M: 'modern_industrialization:motor'
      }
    }
  ]

  var registered = 0
  definitions.forEach(function(definition) {
    registered += v1PathRegister(event, definition) ? 1 : 0
  })
  console.info('[AuthoritativeStagePaths] Registered ' + registered +
    '/' + definitions.length + ' corrected progression paths.')
})
