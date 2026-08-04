ServerEvents.recipes(event => {

    // Mars
    event.shaped(
        Item.of("placeablemaxwell:mars", 1),
        [
            "L L",
            "LWL",
            "GLG"
        ],
        {
            L: "minecraft:light_gray_wool",
            W: "minecraft:white_wool",
            G: "minecraft:gray_wool"
        }
    )

    // Poomba
    event.shaped(
        Item.of("placeablemaxwell:poomba", 1),
        [
            "R R",
            "BRB",
            "BBB"
        ],
        {
            B: "minecraft:black_wool",
            R: "minecraft:brown_wool"
        }
    )

    // Valenok
    event.shaped(
        Item.of("placeablemaxwell:valenok", 1),
        [
            "G G",
            "GWG",
            "WWW"
        ],
        {
            W: "minecraft:white_wool",
            G: "minecraft:orange_wool"
        }
    )

    // Vasilisa
    event.shaped(
        Item.of("placeablemaxwell:vasilisa", 1),
        [
            "G G",
            "GWG",
            "GGG"
        ],
        {
            W: "minecraft:white_wool",
            G: "minecraft:gray_wool"
        }
    )

})
