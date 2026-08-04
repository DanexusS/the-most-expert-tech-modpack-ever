recipes.remove(<item:ironjetpacks:jetpack>.withJsonComponent(<componenttype:ironjetpacks:jetpack_id>, "ironjetpacks:wood"));
craftingTable.addShaped("ironjetpacks_wood_jetpack_vanilla",
    <item:ironjetpacks:jetpack>.withJsonComponent(<componenttype:ironjetpacks:jetpack_id>, "ironjetpacks:wood"),
    [
        [ <item:draconicevolution:draconium_ingot>, <item:ironjetpacks:capacitor>.withJsonComponent(<componenttype:ironjetpacks:jetpack_id>, "ironjetpacks:wood"), <item:draconicevolution:draconium_ingot> ],
        [ <item:megacells:sky_bronze_ingot>, <item:ironjetpacks:strap>, <item:megacells:sky_bronze_ingot> ],
        [ <item:ironjetpacks:thruster>.withJsonComponent(<componenttype:ironjetpacks:jetpack_id>, "ironjetpacks:wood"), <item:mekanism:ultimate_control_circuit>, <item:ironjetpacks:thruster>.withJsonComponent(<componenttype:ironjetpacks:jetpack_id>, "ironjetpacks:wood") ]
    ]
);

