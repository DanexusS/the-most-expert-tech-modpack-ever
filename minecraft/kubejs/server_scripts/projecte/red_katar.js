ServerEvents.recipes(event => {
  event.remove({ output: 'projecte:rm_katar' })
  event.remove({ output: 'quarryplus:remove_bedrock_module' })
    event.shaped(
            Item.of('projecte:rm_katar'),
            [
                    'ABC',
                    'DEF',
                    'FFF'
            ],
            {
                    A: 'projecte:rm_shears',
                    B: 'projecte:rm_axe',
                    D: 'projecte:rm_hoe',
                    C: 'projecte:rm_sword',
                    E: 'draconicevolution:small_chaos_frag',
                    F: 'projecte:red_matter'
            }
    )
});
