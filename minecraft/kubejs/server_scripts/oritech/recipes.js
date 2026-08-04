ServerEvents.recipes(event => {
  // Disable Oritech Enchanting & Catalyst
  event.remove({ id: 'oritech:crafting/catalyst_alt' })
  event.remove({ id: 'oritech:crafting/catalyst' })
  event.remove({ id: 'oritech:crafting/enchanter' })

  // Remove default Oritech oil refinery recipes
  event.remove({ id: 'oritech:refinery/oilalt' })
  event.remove({ id: 'oritech:refinery/oilbase' })

  // Add Crude Oil compatibility for Oritech refinery (without catalyst)
  event.custom({
    "type": "oritech:refinery",
    "fluidInput": {
      "amount": 1000,
      "fluid": "#c:crude_oil"
    },
    "fluidOutputs": [
      {
        "amount": 500,
        "fluid": "oritech:still_heavy_oil"
      },
      {
        "amount": 250,
        "fluid": "oritech:still_naphtha"
      },
      {
        "amount": 250,
        "fluid": "oritech:still_sulfuric_acid"
      }
    ],
    "ingredients": [],
    "results": [],
    "time": 120
  }).id('kubejs:oritech/refinery_oil_compatibility')

  // Add Crude Oil compatibility for Oritech refinery (with clay catalyst beads)
  event.custom({
    "type": "oritech:refinery",
    "fluidInput": {
      "amount": 1000,
      "fluid": "#c:crude_oil"
    },
    "fluidOutputs": [
      {
        "amount": 500,
        "fluid": "oritech:still_diesel"
      },
      {
        "amount": 500,
        "fluid": "oritech:still_naphtha"
      },
      {
        "amount": 500,
        "fluid": "oritech:still_sulfuric_acid"
      }
    ],
    "ingredients": [
      {
        "item": "oritech:clay_catalyst_beads"
      }
    ],
    "results": [],
    "time": 120
  }).id('kubejs:oritech/refinery_oil_compatibility_catalyst')
})
