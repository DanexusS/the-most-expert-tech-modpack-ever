ServerEvents.recipes(event => {
  event.recipes.actuallyadditions.empowering(
    Item.of("kubejs:capacitor_cover"), 
    Item.of("appflux:insulating_resin"), 
    [
      Item.of("immersiveengineering:graphite_electrode"),
      Item.of("modern_industrialization:blastproof_alloy_large_plate"),
      Item.of("immersiveengineering:graphite_electrode"),
      Item.of("modern_industrialization:sodium_hydroxide_bucket")
    ], 
    250000,
    100 
  );
  });