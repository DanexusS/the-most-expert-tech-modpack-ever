ServerEvents.recipes(event => {

    event.shaped(
            Item.of('fragmentumneoforge:elixirof_life'),
            [
                    'ABC',
                    'DEF',
                    'GHI'
            ],
            {
                    C: 'iceandfire:dragonsteel_ice_ingot',
                    H: 'allthecompressed:cinnabar_block_6x',
                    E: 'kubejs:mixed_dragon_blood',
                    I: 'minecraft:enchanted_book[stored_enchantments={levels:{"apothic_enchanting:life_mending":3}}]',
                    F: 'mysticalagradditions:insanium_apple',
                    A: 'iceandfire:dragonsteel_fire_ingot',
                    B: 'iceandfire:dragonsteel_lightning_ingot',
                    D: 'allthemodium:allthemodium_apple',
                    G: 'irons_spellbooks:scroll[irons_spellbooks:spell_container={data:[{id:"irons_spellbooks:blessing_of_life",index:0,level:10,locked:1b}],maxSpells:1,mustEquip:0b,spellWheel:0b}]'
            }
    )
});
