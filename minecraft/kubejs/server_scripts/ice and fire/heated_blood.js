ServerEvents.recipes(event => {
  event.custom({
    "type": "iceandfire:dragonforge",
    "dragonType": "fire",
    "cookTime": 2000,
    "input": { "item": "kubejs:sturdy_bottle" },
    "blood": { "item": "iceandfire:fire_dragon_blood" },
    "result": { "id": "kubejs:heated_dragon_blood" }
  })
})
