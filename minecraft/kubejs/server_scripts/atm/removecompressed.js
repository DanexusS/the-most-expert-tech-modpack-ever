ProjectEEvents.setEMC(event => {
    Ingredient.of('@allthecompressed').stacks.forEach(stack => {
        event.setEMC(stack.id, 0)
    })
})
