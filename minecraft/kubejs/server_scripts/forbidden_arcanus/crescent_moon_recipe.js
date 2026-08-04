ServerEvents.recipes(event => {
  event.recipes.forbidden_arcanus.ritual(
    RitualResults.ofCreateItemResult(Item.of("forbidden_arcanus:crescent_moon")), 
    "forbidden_arcanus:quantum_core"
  )
  .addInput("astral_dimension:moonstone", 1)
  .addInput("stellaris:moon_globe", 1)
  .addInput("stellaris:polished_moon_stone", 1)
  .addInput("ars_nouveau:ritual_moonfall", 1)
  .addInput("astral_dimension:moonstone", 1)
  .addInput("astral_dimension:moonstone", 1)
  .addInput("astral_dimension:moonstone", 1)
  .addInput("astral_dimension:moonstone", 1)
  .essences(2000, 100, 5000, 1500)
  .tier(4)
  .matchTierExact(false) 
  .enhancers("forbidden_arcanus:elementarium")
  .magicCircles("forbidden_arcanus:upgrade_tier");
});
