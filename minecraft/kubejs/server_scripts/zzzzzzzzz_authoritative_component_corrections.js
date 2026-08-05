// Final authoritative replacements for reusable late-game components.
// These definitions load after every legacy and correction layer so no easier
// parallel recipe can survive for the Draconic, EMC or cosmic assemblies.

var AuthorityCorrectionLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var AuthorityCorrectionRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
var AUTHORITY_CORRECTION_CACHE = Object.create(null)

function authorityCorrectionExists(itemId) {
  if (Object.prototype.hasOwnProperty.call(AUTHORITY_CORRECTION_CACHE, itemId)) {
    return AUTHORITY_CORRECTION_CACHE[itemId]
  }
  var exists = false
  try {
    exists = AuthorityCorrectionRegistries.ITEM.containsKey(
      AuthorityCorrectionLocation.parse(itemId)
    )
  } catch (error) {
    exists = false
  }
  AUTHORITY_CORRECTION_CACHE[itemId] = exists
  return exists
}

function authorityCorrectionRegister(event, definition) {
  var required = [definition.output].concat(Object.keys(definition.key).map(function(symbol) {
    return definition.key[symbol]
  }))
  for (var index = 0; index < required.length; index++) {
    if (!authorityCorrectionExists(required[index])) {
      console.warn('[AuthorityCorrections] Kept previous path for ' + definition.output +
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
      id: 'kubejs:authority_correction/draconic_lattice',
      output: 'kubejs:draconic_lattice',
      authoritative: true,
      pattern: ['AWA', 'RWR', 'AHA'],
      key: {
        A: 'draconicevolution:awakened_draconium_ingot',
        W: 'draconicevolution:wyvern_core',
        R: 'kubejs:resonant_core',
        H: 'kubejs:vethea_seal'
      }
    },
    {
      id: 'kubejs:authority_correction/emc_containment_core',
      output: 'kubejs:emc_containment_core',
      authoritative: true,
      pattern: ['DUD', 'PCP', 'DWD'],
      key: {
        D: 'projecte:dark_matter',
        U: 'extendedcrafting:ultimate_singularity',
        P: 'kubejs:draconic_processor',
        C: 'extendedcrafting:ultimate_catalyst',
        W: 'kubejs:wreck_seal'
      }
    },
    {
      id: 'kubejs:authority_correction/cosmic_assembly_matrix',
      output: 'kubejs:cosmic_assembly_matrix',
      authoritative: true,
      pattern: ['CMC', 'ATA', 'CLC'],
      key: {
        C: 'avaritia:crystal_matrix_ingot',
        M: 'draconicevolution:awakened_core',
        A: 'extendedcrafting:ultimate_catalyst',
        T: 'kubejs:transmutation_matrix',
        L: 'kubejs:lunar_seal'
      }
    }
  ]

  var registered = 0
  definitions.forEach(function(definition) {
    registered += authorityCorrectionRegister(event, definition) ? 1 : 0
  })
})
