ItemEvents.modifyTooltips(event => {
  const descriptions = {
    'kubejs:mechanical_core': 'Первый межмодовый узел: Create, Immersive Engineering и Modern Industrialization.',
    'kubejs:industrial_frame': 'Тяжёлая рама для перехода к промышленным машинам.',
    'kubejs:precision_circuit': 'Связывает цифровую обработку, Mekanism и AE2.',
    'kubejs:chemical_processor': 'Общий электронный узел химических и пневматических систем.',
    'kubejs:bioindustrial_matrix': 'Контрольная точка автоматизации биоресурсов и Mystical Agriculture.',
    'kubejs:quantum_logic': 'Поздний вычислительный компонент для AE2 и продвинутой автоматики.',
    'kubejs:resonant_core': 'Энергетический узел нитро-уровня, открываемый после Мортума.',
    'kubejs:draconic_processor': 'Допуск к Draconic Evolution и поздней энергетике.',
    'kubejs:transmutation_matrix': 'Контролирует доступ к ProjectE и не даёт обойти экономику сборки.',
    'kubejs:cosmic_catalyst': 'Финальный допуск к Avaritia и экстремальному ремеслу.'
  }

  Object.keys(descriptions).forEach(itemId => {
    event.add(itemId, Text.gray(descriptions[itemId]))
  })

  const seals = [
    'divine_seal', 'eden_seal', 'wildwood_seal', 'apalachia_seal',
    'skythern_seal', 'mortum_seal', 'vethea_seal', 'wreck_seal', 'lunar_seal'
  ]

  seals.forEach(seal => {
    event.add(`kubejs:${seal}`, Text.lightPurple('Многоразовый ключ прогрессии. Не расходуется при крафте.'))
    event.add(`kubejs:${seal}`, Text.darkGray('Выдаётся за соответствующий этап квестовой линии DivineRPG.'))
  })
})
