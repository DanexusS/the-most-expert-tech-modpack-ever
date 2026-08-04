// Final material gate for the first Infinity Ingot.
// The recipe consumes late production materials while using reusable standards
// for proof of infrastructure. It is intentionally a convergence recipe, not a
// request for thousands of ordinary ingots or hours of manual crafting.

var InfinityPathResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var InfinityPathRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')

function infinityPathExists(itemId) {
  try {
    return InfinityPathRegistries.ITEM.containsKey(InfinityPathResourceLocation.parse(itemId))
  } catch (error) {
    return false
  }
}

ServerEvents.recipes(function(event) {
  var output = 'avaritia:infinity_ingot'
  var key = {
    I: 'avaritia:infinity_catalyst',
    C: 'kubejs:cosmic_catalyst',
    M: 'kubejs:cosmic_assembly_matrix',
    A: 'kubejs:antimatter_regulator',
    P: 'mekanism:pellet_antimatter',
    D: 'draconicevolution:awakened_core',
    L: 'kubejs:lunar_seal'
  }
  var required = [output].concat(Object.keys(key).map(function(symbol) { return key[symbol] }))
  for (var index = 0; index < required.length; index++) {
    if (!infinityPathExists(required[index])) {
      console.warn('[InfinityPath] Kept original Infinity Ingot recipe: unavailable item ' + required[index])
      return
    }
  }

  event.remove({ output: output })
  event.shaped(output, ['ICI', 'PMP', 'DLD'], key).id('kubejs:v1_path/infinity_ingot')
  console.info('[InfinityPath] Registered fair cross-mod Infinity Ingot convergence recipe.')
})
