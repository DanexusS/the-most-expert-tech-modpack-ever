StartupEvents.registry('item', event => {
    event.create('sturdy_bottle')
        .displayName('Sturdy Bottle')
        .maxStackSize(64)
        .rarity('rare')
        .fireResistant()
        .tooltip('Seems strong enough')
})
