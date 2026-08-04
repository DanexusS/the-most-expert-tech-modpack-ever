ServerEvents.recipes(event => {
  const materials = [
    'iron', 'gold', 'copper', 'aluminum', 'nickel', 'platinum', 'silver', 'tin', 'uranium', 'zinc',
    'osmium', 'invar', 'electrum', 'bronze', 'steel', 'enderium', 'lumium', 'signalum', 'brass',
    'constantan', 'iridium'
  ]

  materials.forEach(material => {
    event.custom({
      "type": "mekanism:compressing",
      "chemical_input": {
        "amount": 1,
        "chemical": "mekanism:osmium"
      },
      "item_input": {
        "count": 1,
        "tag": `c:ingots/${material}`
      },
      "output": {
        "count": 1,
        "id": `alltheores:${material}_plate`
      },
      "per_tick_usage": true
    }).id(`kubejs:compressing/${material}_plate`)
  })

  event.custom({
    "type": "mekanism:compressing",
    "chemical_input": {
      "amount": 1,
      "chemical": "mekanism:osmium"
    },
    "item_input": {
      "count": 1,
      "tag": "c:gems/diamond"
    },
    "output": {
      "count": 1,
      "id": "alltheores:diamond_plate"
    },
    "per_tick_usage": true
  }).id('kubejs:compressing/diamond_plate')
})
