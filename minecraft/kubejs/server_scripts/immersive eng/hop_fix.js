ServerEvents.recipes(event => {
  event.smelting('immersiveengineering:ingot_hop_graphite', 'immersiveengineering:dust_hop_graphite')
    .xp(0.7)
    .id('kubejs:smelting_hop_graphite');
      event.blasting('immersiveengineering:ingot_hop_graphite', 'immersiveengineering:dust_hop_graphite')
    .xp(0.7)
    .id('kubejs:blasting_hop_graphite');
});
