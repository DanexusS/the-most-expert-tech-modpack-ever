ServerEvents.recipes(event => {
  event.remove({ output: 'justdynathings:ticker' })
  event.remove({ output: 'extendedae_plus:entity_speed_card[custom_data={"EAS:mult":2b}]' })
  event.remove({ output: 'extendedae_plus:entity_speed_card[custom_data={"EAS:mult":4b}]' })
  event.remove({ output: 'extendedae_plus:entity_speed_card[custom_data={"EAS:mult":8b}]' })
  event.remove({ output: 'extendedae_plus:entity_speed_card[custom_data={"EAS:mult":16b}]' })
});
