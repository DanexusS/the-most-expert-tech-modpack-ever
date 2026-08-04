ServerEvents.recipes(event => {
  event.custom({
    "type": "iceandfire:dragonforge",
    "dragonType": "lightning",
    "cookTime": 2000,
    "input": { "item": "kubejs:heated_dragon_blood" },
    "blood": { "item": "iceandfire:lightning_dragon_blood" },
    "result": { "id": "kubejs:electrified_dragon_blood" }
  })
})
