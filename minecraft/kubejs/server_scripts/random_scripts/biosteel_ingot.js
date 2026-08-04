ServerEvents.recipes(event => {
    event.smelting('oritech:biosteel_ingot', 'oritech:biosteel_dust')
        .xp(0.7)
        .cookingTime(200); 

    event.blasting('oritech:biosteel_ingot', 'oritech:biosteel_dust')
        .xp(0.7)
        .cookingTime(100); 
});