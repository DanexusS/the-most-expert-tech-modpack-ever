// Final convergence corrections for stages 5 and 7. These recipes load after
// the general mid-stage definitions and ensure that every mandatory workflow
// branch contributes a real ingredient to the stage integration item.

var MidConvergenceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var MidConvergenceRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')

function midConvergenceExists(itemId) {
  try {
    return MidConvergenceRegistries.ITEM.containsKey(MidConvergenceLocation.parse(itemId))
  } catch (error) {
    return false
  }
}

function midConvergenceRecipe(event, definition) {
  var required = [definition.output].concat(Object.keys(definition.key).map(function(symbol) {
    return definition.key[symbol]
  }))
  for (var index = 0; index < required.length; index++) {
    if (!midConvergenceExists(required[index])) {
      console.warn('[MidStageConvergence] Kept previous path for ' + definition.output +
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
      id: 'kubejs:mid_convergence/industrial_frame',
      output: 'kubejs:industrial_frame',
      authoritative: true,
      pattern: ['PJP', 'HCH', 'BMB'],
      key: {
        P: 'kubejs:pressure_treated_frame',
        J: 'kubejs:assembly_alignment_jig',
        H: 'modern_industrialization:basic_machine_hull',
        C: 'kubejs:calibrated_substrate',
        B: 'pneumaticcraft:printed_circuit_board',
        M: 'kubejs:mechanical_core'
      }
    },
    {
      id: 'kubejs:mid_convergence/precision_circuit',
      output: 'kubejs:precision_circuit',
      authoritative: true,
      pattern: ['SPS', 'MIM', 'SHS'],
      key: {
        S: 'kubejs:signal_backplane',
        P: 'kubejs:process_control_board',
        M: 'kubejs:pressure_manifold',
        I: 'mekanism:steel_casing',
        H: 'kubejs:eden_seal'
      }
    }
  ]

  var registered = 0
  definitions.forEach(function(definition) {
    registered += midConvergenceRecipe(event, definition) ? 1 : 0
  })
  console.info('[MidStageConvergence] Registered ' + registered +
    '/' + definitions.length + ' branch-complete convergence recipes.')
})
