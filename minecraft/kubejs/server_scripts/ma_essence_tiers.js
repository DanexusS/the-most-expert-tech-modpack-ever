ServerEvents.recipes(event => {
  const MysticalAgricultureAPI = Java.loadClass('com.blakebr0.mysticalagriculture.api.MysticalAgricultureAPI')
  const CRYSTAL_NS = 'matc'
  const CUSTOM_NAMESPACE = 'kubejs:'
  var customTierContentAvailable = true

  function usesCustomRegistry() {
    for (var argumentIndex = 0; argumentIndex < arguments.length; argumentIndex++) {
      var argumentValue = arguments[argumentIndex]

      if (typeof argumentValue === 'string' && argumentValue.indexOf(CUSTOM_NAMESPACE) === 0) {
        return true
      }
    }

    return false
  }

  function runRecipeStep(description, dependsOnCustomTierContent, action) {
    if (dependsOnCustomTierContent && !customTierContentAvailable) {
      return
    }

    try {
      action()
    } catch (error) {
      if (!dependsOnCustomTierContent) {
        throw error
      }

      customTierContentAvailable = false
      console.warn(
        '[MAEssenceTiers] Custom KubeJS items are not registered in the current game session yet. ' +
          'Skipping custom MA recipes for now; restart the whole game to load startup_scripts. ' +
          'First failed step: ' +
          description +
          ' (' +
          error +
          ')'
      )
    }
  }

  function buildStandardSeedOutputId(cropId) {
    return 'mysticalagriculture:' + cropId.split(':')[1] + '_seeds'
  }

  function buildStandardSeedInfusionIngredients(cropId) {
    const ingredients = []

    for (let ingredientIndex = 0; ingredientIndex < 4; ingredientIndex++) {
      ingredients.push({
        type: 'mysticalagriculture:crop_component',
        component: 'material',
        crop: cropId
      })
      ingredients.push({
        type: 'mysticalagriculture:crop_component',
        component: 'essence',
        crop: cropId
      })
    }

    return ingredients
  }

  const crystalRecipes = [
    {
      output: 'kubejs:insanium_crystal',
      essence: 'mysticalagradditions:insanium_essence',
      catalyst: `${CRYSTAL_NS}:supremium_crystal`
    },
    {
      output: 'kubejs:dimyanit_crystal',
      essence: 'kubejs:dimyanit_essence',
      catalyst: 'kubejs:insanium_crystal'
    },
    {
      output: 'kubejs:eduardit_crystal',
      essence: 'kubejs:eduardit_essence',
      catalyst: 'kubejs:dimyanit_crystal'
    },
    {
      output: 'kubejs:dannexit_crystal',
      essence: 'kubejs:dannexit_essence',
      catalyst: 'kubejs:eduardit_crystal'
    },
    {
      output: 'kubejs:emkoviy_crystal',
      essence: 'kubejs:emkoviy_essence',
      catalyst: 'kubejs:dannexit_crystal'
    },
    {
      output: 'kubejs:rakuniy_crystal',
      essence: 'kubejs:rakuniy_essence',
      catalyst: 'kubejs:emkoviy_crystal'
    }
  ]

  const tierUpRecipes = [
    {
      lowerEssence: 'mysticalagriculture:inferium_essence',
      lowerBlock: 'mysticalagriculture:inferium_block',
      crystal: `${CRYSTAL_NS}:inferium_crystal`,
      higherEssence: 'mysticalagriculture:prudentium_essence'
    },
    {
      lowerEssence: 'mysticalagriculture:prudentium_essence',
      lowerBlock: 'mysticalagriculture:prudentium_block',
      crystal: `${CRYSTAL_NS}:prudentium_crystal`,
      higherEssence: 'mysticalagriculture:tertium_essence'
    },
    {
      lowerEssence: 'mysticalagriculture:tertium_essence',
      lowerBlock: 'mysticalagriculture:tertium_block',
      crystal: `${CRYSTAL_NS}:tertium_crystal`,
      higherEssence: 'mysticalagriculture:imperium_essence'
    },
    {
      lowerEssence: 'mysticalagriculture:imperium_essence',
      lowerBlock: 'mysticalagriculture:imperium_block',
      crystal: `${CRYSTAL_NS}:imperium_crystal`,
      higherEssence: 'mysticalagriculture:supremium_essence'
    },
    {
      lowerEssence: 'mysticalagriculture:supremium_essence',
      lowerBlock: 'mysticalagriculture:supremium_block',
      crystal: `${CRYSTAL_NS}:supremium_crystal`,
      higherEssence: 'mysticalagradditions:insanium_essence'
    },
    {
      lowerEssence: 'mysticalagradditions:insanium_essence',
      lowerBlock: 'mysticalagradditions:insanium_block',
      crystal: 'kubejs:insanium_crystal',
      higherEssence: 'kubejs:dimyanit_essence'
    },
    {
      lowerEssence: 'kubejs:dimyanit_essence',
      lowerBlock: 'kubejs:dimyanit_block',
      crystal: 'kubejs:dimyanit_crystal',
      higherEssence: 'kubejs:eduardit_essence'
    },
    {
      lowerEssence: 'kubejs:eduardit_essence',
      lowerBlock: 'kubejs:eduardit_block',
      crystal: 'kubejs:eduardit_crystal',
      higherEssence: 'kubejs:dannexit_essence'
    },
    {
      lowerEssence: 'kubejs:dannexit_essence',
      lowerBlock: 'kubejs:dannexit_block',
      crystal: 'kubejs:dannexit_crystal',
      higherEssence: 'kubejs:emkoviy_essence'
    },
    {
      lowerEssence: 'kubejs:emkoviy_essence',
      lowerBlock: 'kubejs:emkoviy_block',
      crystal: 'kubejs:emkoviy_crystal',
      higherEssence: 'kubejs:rakuniy_essence'
    },
    {
      lowerEssence: 'kubejs:rakuniy_essence',
      lowerBlock: 'kubejs:rakuniy_block',
      crystal: 'kubejs:rakuniy_crystal',
      higherEssence: 'kubejs:kodeksit_essence'
    }
  ]

  const sameTierBlocks = [
    {
      essence: 'mysticalagriculture:inferium_essence',
      block: 'mysticalagriculture:inferium_block'
    },
    {
      essence: 'mysticalagriculture:prudentium_essence',
      block: 'mysticalagriculture:prudentium_block'
    },
    {
      essence: 'mysticalagriculture:tertium_essence',
      block: 'mysticalagriculture:tertium_block'
    },
    {
      essence: 'mysticalagriculture:imperium_essence',
      block: 'mysticalagriculture:imperium_block'
    },
    {
      essence: 'mysticalagriculture:supremium_essence',
      block: 'mysticalagriculture:supremium_block'
    },
    {
      essence: 'mysticalagradditions:insanium_essence',
      block: 'mysticalagradditions:insanium_block'
    },
    {
      essence: 'kubejs:dimyanit_essence',
      block: 'kubejs:dimyanit_block'
    },
    {
      essence: 'kubejs:eduardit_essence',
      block: 'kubejs:eduardit_block'
    },
    {
      essence: 'kubejs:dannexit_essence',
      block: 'kubejs:dannexit_block'
    },
    {
      essence: 'kubejs:emkoviy_essence',
      block: 'kubejs:emkoviy_block'
    },
    {
      essence: 'kubejs:rakuniy_essence',
      block: 'kubejs:rakuniy_block'
    },
    {
      essence: 'kubejs:kodeksit_essence',
      block: 'kubejs:kodeksit_block'
    }
  ]

  crystalRecipes.forEach(recipe => {
    const recipeId = `kubejs:${recipe.output.split(':')[1]}_crafting`
    const dependsOnCustomTierContent = usesCustomRegistry(
      recipe.output,
      recipe.essence,
      recipe.catalyst
    )

    runRecipeStep(`crystal recipe ${recipeId}`, dependsOnCustomTierContent, () => {
      event.remove({ output: recipe.output })

      event.shaped(recipe.output, [
        'PEP',
        'EGE',
        'PEP'
      ], {
        P: recipe.essence,
        E: 'mysticalagriculture:prosperity_shard',
        G: recipe.catalyst
      }).id(recipeId)
    })
  })

  tierUpRecipes.forEach(recipe => {
    const outputName = recipe.higherEssence.split(':')[1]
    const lowerBlockName = recipe.lowerBlock.split(':')[1]
    const recipeId = `kubejs:${outputName}_from_8_${lowerBlockName}_and_crystal`
    const dependsOnCustomTierContent = usesCustomRegistry(
      recipe.lowerEssence,
      recipe.lowerBlock,
      recipe.crystal,
      recipe.higherEssence
    )

    runRecipeStep(`tier-up recipe ${recipeId}`, dependsOnCustomTierContent, () => {
      event.remove({ output: recipe.higherEssence })
      event.remove({
        input: recipe.higherEssence,
        output: recipe.lowerEssence
      })

      event.shaped(recipe.higherEssence, [
        'BBB',
        'BCB',
        'BBB'
      ], {
        B: recipe.lowerBlock,
        C: recipe.crystal
      }).id(recipeId)
    })
  })

  sameTierBlocks.forEach(recipe => {
    const blockName = recipe.block.split(':')[1]
    const toBlockRecipeId = `kubejs:${blockName}_from_9_same_tier_essence`
    const toEssenceRecipeId = `kubejs:${blockName}_to_9_same_tier_essence`
    const dependsOnCustomTierContent = usesCustomRegistry(recipe.essence, recipe.block)

    runRecipeStep(`same-tier block recipe ${toBlockRecipeId}`, dependsOnCustomTierContent, () => {
      event.remove({ output: recipe.block })
      event.remove({
        input: recipe.block,
        output: recipe.essence
      })

      event.shaped(recipe.block, [
        'EEE',
        'EEE',
        'EEE'
      ], {
        E: recipe.essence
      }).id(toBlockRecipeId)

      event.shapeless(Item.of(recipe.essence, 9), [
        recipe.block
      ]).id(toEssenceRecipeId)
    })
  })

  runRecipeStep(
    'creative essence infusion recipe',
    true,
    () => {
      event.remove({ output: 'mysticalagradditions:creative_essence' })

      event.custom({
        type: 'mysticalagriculture:infusion',
        input: {
          item: 'avaritia:neutron'
        },
        ingredients: Array(8).fill({
          item: 'kubejs:kodeksit_block'
        }),
        result: {
          id: 'mysticalagradditions:creative_essence',
          count: 1
        }
      }).id('kubejs:creative_essence_from_neutron_and_kodeksit_blocks')
    }
  )

  const cropRegistry = MysticalAgricultureAPI.getCropRegistry()
  const crops = cropRegistry.getCrops()
  let generatedSeedRecipeCount = 0
  var cropIndex
  var registeredCrop
  var cropId
  var tierId
  var recipeConfig
  var seedOutputId
  var recipeId
  var dependsOnCustomTierContent

  for (cropIndex = 0; cropIndex < crops.size(); cropIndex++) {
    registeredCrop = crops.get(cropIndex)
    cropId = String(registeredCrop.getId())
    tierId = String(registeredCrop.getTier().getId())
    recipeConfig = registeredCrop.getRecipeConfig()

    if (!registeredCrop.isEnabled()) {
      continue
    }

    if (!recipeConfig.isSeedInfusionRecipeEnabled()) {
      continue
    }

    if (cropId === 'mysticalagriculture:inferium') {
      continue
    }

    if (tierId === 'mysticalagriculture:elemental') {
      continue
    }

    seedOutputId = buildStandardSeedOutputId(cropId)
    recipeId = 'kubejs:ma_seed_infusion/' + cropId.replace(':', '/')
    dependsOnCustomTierContent = tierId.indexOf('mysticalcustomization:') === 0

    runRecipeStep(`seed infusion recipe ${recipeId}`, dependsOnCustomTierContent, () => {
      event.remove({ output: seedOutputId })

      event.custom({
        'neoforge:conditions': [
          {
            type: 'mysticalagriculture:crop_enabled',
            crop: cropId
          },
          {
            type: 'mysticalagriculture:crop_has_material',
            crop: cropId
          }
        ],
        type: 'mysticalagriculture:infusion',
        input: {
          item: 'mysticalagriculture:prosperity_seed_base'
        },
        ingredients: buildStandardSeedInfusionIngredients(cropId),
        result: {
          id: seedOutputId,
          count: 1
        }
      }).id(recipeId)

      generatedSeedRecipeCount++
    })
  }

  console.info(
    '[MAEssenceTiers] Generated ' +
      generatedSeedRecipeCount +
      ' prosperity-seed infusion recipes for Mystical Agriculture crops.'
  )
})
