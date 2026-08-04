// Unified hostile-mob scaling for Minecraft 1.21.1 / NeoForge.
// Uses a permanent ADD_MULTIPLIED_BASE modifier so Apotheosis and other
// attribute systems remain compatible. Existing v0.1.x modifiers are
// replaced in place, preserving the entity's current health percentage.

var ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var BuiltInRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
var Attributes = Java.loadClass('net.minecraft.world.entity.ai.attributes.Attributes')
var AttributeModifier = Java.loadClass('net.minecraft.world.entity.ai.attributes.AttributeModifier')

var HEALTH_MODIFIER_ID = ResourceLocation.parse('kubejs:expert_health_scale')

// Regular hostile mobs from the requested combat-heavy mods.
var NAMESPACE_MULTIPLIERS = Object.freeze({
  cataclysm: 4.0,
  mowziesmobs: 3.75,
  mutantmonsters: 4.0,
  earthmobsmod: 3.5,
  divinerpg: 3.75,
  twilightforest: 3.5,
  iceandfire: 3.75,
  born_in_chaos_v1: 2.5
})

// Bosses and large elite creatures receive a separate tier.
var BOSS_NAMESPACE_MULTIPLIERS = Object.freeze({
  cataclysm: 6.0,
  mowziesmobs: 5.0,
  divinerpg: 5.0,
  twilightforest: 5.0,
  iceandfire: 5.5,
  minecraft: 2.5
})

var BOSS_IDS = Object.freeze({
  'minecraft:elder_guardian': true,
  'minecraft:wither': true,
  'minecraft:ender_dragon': true,

  // Mowzie's Mobs
  'mowziesmobs:ferrous_wroughtnaut': true,
  'mowziesmobs:umvuthi': true,
  'mowziesmobs:frostmaw': true,
  'mowziesmobs:sculptor': true,

  // DivineRPG
  'divinerpg:ancient_entity': true,
  'divinerpg:the_watcher': true,
  'divinerpg:king_of_scorchers': true,
  'divinerpg:kitra': true,
  'divinerpg:ayeraco': true,
  'divinerpg:sunstorm': true,
  'divinerpg:termasect': true,
  'divinerpg:eternal_archer': true,
  'divinerpg:experienced_cori': true,
  'divinerpg:parasecta': true,
  'divinerpg:dramix': true,
  'divinerpg:soul_fiend': true,
  'divinerpg:twilight_demon': true,
  'divinerpg:vamacheron': true,
  'divinerpg:densos': true,
  'divinerpg:reyvor': true,
  'divinerpg:karot': true,
  'divinerpg:hive_queen': true,
  'divinerpg:quadro': true,
  'divinerpg:karos': true,
  'divinerpg:raglok': true,
  'divinerpg:wreck': true,
  'divinerpg:lady_luna': true,

  // L_Ender's Cataclysm
  'cataclysm:netherite_monstrosity': true,
  'cataclysm:ender_guardian': true,
  'cataclysm:the_harbinger': true,
  'cataclysm:ancient_remnant': true,
  'cataclysm:the_leviathan': true,
  'cataclysm:scylla': true,
  'cataclysm:maledictus': true,
  'cataclysm:ignis': true,

  // Twilight Forest progression bosses
  'twilightforest:naga': true,
  'twilightforest:lich': true,
  'twilightforest:minoshroom': true,
  'twilightforest:hydra': true,
  'twilightforest:knight_phantom': true,
  'twilightforest:ur_ghast': true,
  'twilightforest:alpha_yeti': true,
  'twilightforest:snow_queen': true,

  // Ice and Fire major threats. Explicit IDs also cover creatures whose
  // spawn category is not MONSTER, such as dragons and sea serpents.
  'iceandfire:fire_dragon': true,
  'iceandfire:ice_dragon': true,
  'iceandfire:lightning_dragon': true,
  'iceandfire:hydra': true,
  'iceandfire:cyclops': true,
  'iceandfire:gorgon': true,
  'iceandfire:sea_serpent': true,
  'iceandfire:death_worm': true,
  'iceandfire:troll': true,
  'iceandfire:cockatrice': true,
  'iceandfire:stymphalian_bird': true,
  'iceandfire:dread_lich': true,
  'iceandfire:dread_knight': true
})

function namespaceOf(entityId) {
  var separator = entityId.indexOf(':')
  return separator < 0 ? 'minecraft' : entityId.substring(0, separator)
}

function isMonsterCategory(entityId) {
  try {
    var location = ResourceLocation.parse(entityId)
    if (!BuiltInRegistries.ENTITY_TYPE.containsKey(location)) {
      return false
    }

    var entityType = BuiltInRegistries.ENTITY_TYPE.get(location)
    return entityType != null && String(entityType.getCategory()) === 'monster'
  } catch (error) {
    console.warn('[CombatScaling] Failed category lookup for ' + entityId + ': ' + error)
    return false
  }
}

function multiplierFor(entityId) {
  var namespace = namespaceOf(entityId)

  if (BOSS_IDS[entityId] === true) {
    return BOSS_NAMESPACE_MULTIPLIERS[namespace] || 2.5
  }

  // Do not buff passive fauna from Earth Mobs, Twilight Forest or Ice and Fire.
  if (!isMonsterCategory(entityId)) {
    return 1.0
  }

  return NAMESPACE_MULTIPLIERS[namespace] || 2.25
}

function applyHealthMultiplier(entity, multiplier) {
  if (multiplier <= 1.0) {
    return
  }

  var attribute = entity.getAttribute(Attributes.MAX_HEALTH)
  if (attribute == null) {
    return
  }

  var oldMaxHealth = entity.getMaxHealth()
  var oldHealth = entity.getHealth()
  var healthRatio = oldMaxHealth > 0 ? oldHealth / oldMaxHealth : 1.0

  // Replace the previous v0.1.x value instead of stacking on top of it.
  if (attribute.getModifier(HEALTH_MODIFIER_ID) != null) {
    attribute.removeModifier(HEALTH_MODIFIER_ID)
  }

  attribute.addPermanentModifier(
    new AttributeModifier(
      HEALTH_MODIFIER_ID,
      multiplier - 1.0,
      AttributeModifier.Operation.ADD_MULTIPLIED_BASE
    )
  )

  var newMaxHealth = entity.getMaxHealth()
  entity.setHealth(Math.max(1.0, Math.min(newMaxHealth, newMaxHealth * healthRatio)))
}

EntityEvents.spawned(function(event) {
  var entity = event.entity

  if (!entity || !entity.isLiving()) {
    return
  }

  var entityId = String(BuiltInRegistries.ENTITY_TYPE.getKey(entity.getType()))
  applyHealthMultiplier(entity, multiplierFor(entityId))
})

console.info('[CombatScaling] Enhanced combat-mod health scaling v0.1.2 loaded.')
