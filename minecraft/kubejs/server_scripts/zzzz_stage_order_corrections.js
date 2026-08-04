// Corrections for stage-order dependencies found by the recipe graph audit.
// Each output is removed only after every replacement ingredient exists.

var StageOrderLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var StageOrderRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')

function stageOrderExists(itemId) {
  try {
    return StageOrderRegistries.ITEM.containsKey(StageOrderLocation.parse(itemId))
  } catch (error) {
    return false
  }
}

function stageOrderRecipe(event, definition) {
  var required = [definition.output].concat(Object.keys(definition.key).map(function(symbol) {
    return definition.key[symbol]
  }))
  for (var index = 0; index < required.length; index++) {
    if (!stageOrderExists(required[index])) {
      console.warn('[StageOrderCorrections] Kept previous ' + definition.output +
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
      id: 'kubejs:v1_order/industrial_frame',
      output: 'kubejs:industrial_frame',
      pattern: ['LDL', 'KCK', 'LHL'],
      key: {
        L: 'kubejs:structural_lattice',
        D: 'kubejs:divine_seal',
        K: 'kubejs:kinetic_regulator',
        C: 'kubejs:mechanical_core',
        H: 'modern_industrialization:basic_machine_hull'
      }
    },
    {
      id: 'kubejs:v1_order/dimensional_resonator',
      output: 'kubejs:dimensional_resonator',
      pattern: ['SDS', 'MRM', 'SAS'],
      key: {
        S: 'kubejs:skythern_seal',
        D: 'kubejs:divine_seal',
        M: 'kubejs:mortum_seal',
        R: 'kubejs:resonant_core',
        A: 'kubejs:antimatter_regulator'
      }
    }
  ]

  var registered = 0
  definitions.forEach(function(definition) {
    registered += stageOrderRecipe(event, definition) ? 1 : 0
  })
  console.info('[StageOrderCorrections] Registered ' + registered +
    '/' + definitions.length + ' stage-order corrections.')
})
