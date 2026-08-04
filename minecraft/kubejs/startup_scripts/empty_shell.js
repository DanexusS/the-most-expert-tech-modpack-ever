StartupEvents.registry('item', event => {
    event.create('sus_shell')
        .displayName('Suspicious Looking Shell')
        .maxStackSize(64)
        .rarity('rare')
        .fireResistant()
        .tooltip('Try giving it some color...')
})
