// Final corrections for two intermediate assemblies that must remain available
// before their stage milestone. This file loads after the main late-stage layer.

var LateCorrectionLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var LateCorrectionRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')

function lateCorrectionExists(itemId) {
  try {
    return LateCorrectionRegistries.ITEM.containsKey(LateCorrectionLocation.parse(itemId))
  } catch (error) {
    return false
  }
}

function lateCorrectionRecipe(event, definition) {
  var required = [definition.output].concat(Object.keys(definition.key).map(function(symbol) {
    return definition.key[symbol]
  }))
  for (var index = 0; index < required.length; index++) {
    if (!lateCorrectionExists(required[index])) {
      console.warn('[LateCycleCorrections] Kept previous path for ' + definition.output +
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
    {
      id: 'kubejs:late_correction/transmutation_safety_lock',
      output: 'kubejs:transmutation_safety_lock',
      pattern: ['TCT', 'PDP', 'TWT'],
      key: {
        T: 'minecraft:tripwire_hook',
        C: 'extendedcrafting:ultimate_catalyst',
        P: 'projecte:philosophers_stone',
        D: 'kubejs:draconic_processor',
        W: 'kubejs:wreck_seal'
      }
    },
    {
      id: 'kubejs:late_correction/ultimate_pattern_frame',
      output: 'kubejs:ultimate_pattern_frame',
      pattern: ['UEU', 'TXT', 'UEU'],
      key: {
        U: 'extendedcrafting:ultimate_component',
        E: 'extendedcrafting:ultimate_table',
        T: 'kubejs:transmutation_matrix',
        X: 'extendedcrafting:elite_table'
      }
    }
  ]

  var registered = 0
  definitions.forEach(function(definition) {
    registered += lateCorrectionRecipe(event, definition) ? 1 : 0
  })
})
