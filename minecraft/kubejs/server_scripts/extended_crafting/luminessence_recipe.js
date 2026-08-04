ServerEvents.recipes(event => {
event.remove({ output: 'extendedcrafting:luminessence' })
    event.shaped(
Item.of('extendedcrafting:luminessence'),[
'ABC',
'DED',
'CBA'
], {
E: 'draconicevolution:draconium_dust',
D: 'irons_spellbooks:arcane_essence',
C: 'ae2:fluix_dust',
B: 'advanced_ae:quantum_infused_dust',
A: 'mysticalagradditions:insanium_essence'
})
});
