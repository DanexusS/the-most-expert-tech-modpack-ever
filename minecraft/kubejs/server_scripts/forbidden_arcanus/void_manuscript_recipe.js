ServerEvents.recipes(event => {
  event.recipes.forbidden_arcanus.ritual(
    RitualResults.ofCreateItemResult(Item.of("fragmentumneoforge:manuscriptvoid")), 
    "allthearcanistgear:unobtainium_spell_book"
  )
  .addInput("cognition:nightmare_bottle", 1)
  .addInput("ars_nouveau:wilden_tribute", 1)
  .addInput("forbidden_arcanus:corrupt_soul", 1)
  .addInput("projectexpansion:fading_matter", 1)
  .addInput("mysticalagradditions:creative_essence", 1)
  .addInput("irons_spellbooks:eldritch_manuscript", 1)
  .addInput("cataclysm:abyssal_sacrifice", 1)
  .addInput("bhc:soul_heart_crystal", 1)
  .essences(20000, 1000, 100000, 7500)
  .tier(5)
  .matchTierExact(false) 
  .enhancers("forbidden_arcanus:artisan_relic", "forbidden_arcanus:crescent_moon")
  .magicCircles("forbidden_arcanus:upgrade_tier");
});
