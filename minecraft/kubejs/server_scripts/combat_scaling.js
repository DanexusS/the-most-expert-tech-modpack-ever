// Unified hostile-mob scaling for Minecraft 1.21.1 / NeoForge.
// The profile changes health, attack damage, armor and knockback resistance.
// Permanent modifiers are replaced by stable IDs, so repeated spawn hooks or
// pack updates do not stack the same expert bonus multiple times.

var ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var BuiltInRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
var Attributes = Java.loadClass('net.minecraft.world.entity.ai.attributes.Attributes')
var AttributeModifier = Java.loadClass('net.minecraft.world.entity.ai.attributes.AttributeModifier')
var IdentityHashMap = Java.loadClass('java.util.IdentityHashMap')

var MODIFIER_IDS = Object.freeze({
  health: ResourceLocation.parse('kubejs:expert_health_scale'),
  damage: ResourceLocation.parse('kubejs:expert_damage_scale'),
  armor: ResourceLocation.parse('kubejs:expert_armor_bonus'),
  knockback: ResourceLocation.parse('kubejs:expert_knockback_resistance')
})

var DEFAULT_HOSTILE_PROFILE = Object.freeze({
  health: 2.25,
  damage: 1.20,
  armor: 1.0,
  knockback: 0.05
})

var DEFAULT_BOSS_PROFILE = Object.freeze({
  health: 3.0,
  damage: 1.50,
  armor: 5.0,
  knockback: 0.20
})

// Regular hostile creatures. The values are intentionally below boss values:
// common encounters become dangerous without turning every cave into a boss.
var NAMESPACE_PROFILES = Object.freeze({
  cataclysm: Object.freeze({ health: 4.0, damage: 1.55, armor: 5.0, knockback: 0.15 }),
  mowziesmobs: Object.freeze({ health: 3.75, damage: 1.50, armor: 4.0, knockback: 0.15 }),
  mutantmonsters: Object.freeze({ health: 4.0, damage: 1.65, armor: 5.0, knockback: 0.20 }),
  earthmobsmod: Object.freeze({ health: 3.5, damage: 1.45, armor: 3.0, knockback: 0.10 }),
  divinerpg: Object.freeze({ health: 3.75, damage: 1.55, armor: 4.0, knockback: 0.15 }),
  twilightforest: Object.freeze({ health: 3.5, damage: 1.45, armor: 4.0, knockback: 0.10 }),
  iceandfire: Object.freeze({ health: 3.75, damage: 1.60, armor: 5.0, knockback: 0.15 }),
  born_in_chaos_v1: Object.freeze({ health: 2.75, damage: 1.40, armor: 3.0, knockback: 0.10 })
})

var BOSS_NAMESPACE_PROFILES = Object.freeze({
  cataclysm: Object.freeze({ health: 5.0, damage: 1.75, armor: 8.0, knockback: 0.35 }),
  mowziesmobs: Object.freeze({ health: 4.5, damage: 1.65, armor: 6.0, knockback: 0.30 }),
  divinerpg: Object.freeze({ health: 4.5, damage: 1.70, armor: 6.0, knockback: 0.30 }),
  twilightforest: Object.freeze({ health: 4.5, damage: 1.60, armor: 6.0, knockback: 0.30 }),
  iceandfire: Object.freeze({ health: 5.0, damage: 1.75, armor: 7.0, knockback: 0.35 }),
  minecraft: Object.freeze({ health: 2.5, damage: 1.45, armor: 4.0, knockback: 0.20 })
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

// Entity categories and profiles are stable after registries finish loading.
// The string cache prevents repeated profile resolution by ID. The identity
// cache additionally removes the registry-key lookup from every repeated spawn
// of the same EntityType singleton, which matters in large farms and during
// world population.
var PROFILE_CACHE = Object.create(null)
var TYPE_PROFILE_CACHE = new IdentityHashMap()

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

function resolveProfile(entityId) {
  var namespace = namespaceOf(entityId)

  if (BOSS_IDS[entityId] === true) {
    return BOSS_NAMESPACE_PROFILES[namespace] || DEFAULT_BOSS_PROFILE
  }

  // Passive fauna from exploration mods must not inherit namespace bonuses.
  if (!isMonsterCategory(entityId)) {
    return null
  }

  return NAMESPACE_PROFILES[namespace] || DEFAULT_HOSTILE_PROFILE
}

function profileFor(entityId) {
  if (Object.prototype.hasOwnProperty.call(PROFILE_CACHE, entityId)) {
    return PROFILE_CACHE[entityId] || null
  }

  var profile = resolveProfile(entityId)
  PROFILE_CACHE[entityId] = profile || false
  return profile
}

function profileForType(entityType) {
  if (TYPE_PROFILE_CACHE.containsKey(entityType)) {
    return TYPE_PROFILE_CACHE.get(entityType) || null
  }

  var entityId = String(BuiltInRegistries.ENTITY_TYPE.getKey(entityType))
  var profile = profileFor(entityId)
  TYPE_PROFILE_CACHE.put(entityType, profile || false)
  return profile
}

function replaceModifier(entity, attributeType, modifierId, amount, operation) {
  var attribute = entity.getAttribute(attributeType)
  if (attribute == null) {
    return
  }

  if (attribute.getModifier(modifierId) != null) {
    attribute.removeModifier(modifierId)
  }

  if (amount === 0) {
    return
  }

  attribute.addPermanentModifier(new AttributeModifier(modifierId, amount, operation))
}

function applyProfile(entity, profile) {
  if (profile == null) {
    return
  }

  var oldMaxHealth = entity.getMaxHealth()
  var oldHealth = entity.getHealth()
  var healthRatio = oldMaxHealth > 0 ? oldHealth / oldMaxHealth : 1.0

  replaceModifier(
    entity,
    Attributes.MAX_HEALTH,
    MODIFIER_IDS.health,
    Math.max(0.0, profile.health - 1.0),
    AttributeModifier.Operation.ADD_MULTIPLIED_BASE
  )
  replaceModifier(
    entity,
    Attributes.ATTACK_DAMAGE,
    MODIFIER_IDS.damage,
    Math.max(0.0, profile.damage - 1.0),
    AttributeModifier.Operation.ADD_MULTIPLIED_BASE
  )
  replaceModifier(
    entity,
    Attributes.ARMOR,
    MODIFIER_IDS.armor,
    Math.max(0.0, profile.armor),
    AttributeModifier.Operation.ADD_VALUE
  )
  replaceModifier(
    entity,
    Attributes.KNOCKBACK_RESISTANCE,
    MODIFIER_IDS.knockback,
    Math.max(0.0, Math.min(0.50, profile.knockback)),
    AttributeModifier.Operation.ADD_VALUE
  )

  var newMaxHealth = entity.getMaxHealth()
  entity.setHealth(Math.max(1.0, Math.min(newMaxHealth, newMaxHealth * healthRatio)))
}

EntityEvents.spawned(function(event) {
  var entity = event.entity

  if (!entity || !entity.isLiving()) {
    return
  }

  applyProfile(entity, profileForType(entity.getType()))
})
