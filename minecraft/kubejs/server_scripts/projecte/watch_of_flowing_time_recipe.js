ServerEvents.recipes(event => {
  event.remove({ output: 'projecte:watch_of_flowing_time' })
  event.shaped('projecte:watch_of_flowing_time', [
    'ABA',
    'CDC',
    'EFE'
  ], {
    A: 'draconicevolution:chaos_shard',
    B: 'mekanism_extras:qio_drive_singularity',
    C: 'draconicevolution:chaotic_core',
    D: 'minecraft:clock',
    E: 'justdirethings:time_crystal',
    F: 'projectexpansion:gargantuan_star_omega'
  })
})
