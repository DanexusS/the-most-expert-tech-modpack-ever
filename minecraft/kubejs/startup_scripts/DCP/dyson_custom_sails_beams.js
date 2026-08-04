StartupEvents.registry('item', event => {


  event.create("insanium_solar_sail_package")
    .displayName("Insanium Solar Sail Package")
    .tooltip("Dyson Sphere Component")
    .component(
      "dysoncubeproject:sphere_component_solar_sail",
      Java.cast("java.lang.Integer", 64)
    )

  event.create("insanium_beam_package")
    .displayName("Insanium Beam Package")
    .tooltip("Dyson Sphere Component")
    .component(
      "dysoncubeproject:sphere_component_beam",
      Java.cast("java.lang.Integer", 16)
    )


  event.create("neutronium_solar_sail_package")
    .displayName("Neutronium Solar Sail Package")
    .tooltip("Dyson Sphere Component")
    .component(
      "dysoncubeproject:sphere_component_solar_sail",
      Java.cast("java.lang.Integer", 128)
    )

  event.create("neutronium_beam_package")
    .displayName("Neutronium Beam Package")
    .tooltip("Dyson Sphere Component")
    .component(
      "dysoncubeproject:sphere_component_beam",
      Java.cast("java.lang.Integer", 32)
    )

})
