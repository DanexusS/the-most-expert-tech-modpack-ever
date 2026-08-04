StartupEvents.registry('item', event => {
    event.create('information_disk')
        .displayName('Information Disk')
        .maxStackSize(64)
        .rarity('rare')
        .fireResistant()
        .tooltip('Contains approximately 2.5 petabytes')
})
