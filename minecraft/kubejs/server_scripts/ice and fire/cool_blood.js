ServerEvents.recipes(event => {
  event.custom({
    "type": "iceandfire:dragonforge",
    "dragonType": "ice",
    "cookTime": 2000,
    "input": { "item": "kubejs:electrified_dragon_blood" },
    "blood": { "item": "iceandfire:ice_dragon_blood" },
    "result": { "id": "kubejs:mixed_dragon_blood" }
  })
})
