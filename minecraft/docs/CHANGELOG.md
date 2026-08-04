# Changelog

## v0.2.0

- Added 365 quests in four new chapters.
- Added 116 kill tasks across seven reinforced combat mods.
- Added detailed Russian progression explanations and English fallback localization.
- Added optional automation benchmarks and line-audit checkmarks.
- Reduced reward philosophy to symbolic XP only.

# Журнал изменений

## v0.1.2

- Усилено здоровье враждебных существ из Cataclysm, Mowzie's Mobs, Mutant Monsters, Earth Mobs, DivineRPG, Twilight Forest и Ice and Fire.
- Добавлены отдельные коэффициенты для обычных противников и боссов/крупных элит.
- Cataclysm: ×4 / ×6; Mowzie's Mobs: ×3,75 / ×5; DivineRPG: ×3,75 / ×5; Twilight Forest: ×3,5 / ×5; Ice and Fire: ×3,75 / ×5,5.
- Mutant Monsters усилены до ×4, враждебные Earth Mobs — до ×3,5.
- Пассивная фауна Earth Mobs, Twilight Forest и Ice and Fire исключена из массового усиления.
- Старый постоянный модификатор теперь заменяется, а не блокирует обновление коэффициента; процент текущего здоровья сохраняется.

## v0.1.1

- Исправлен `client_scripts/expert_tooltips.js`: событие `ItemEvents.tooltip` заменено на `ItemEvents.modifyTooltips` для KubeJS 2101.7.2.
- Подтверждена загрузка 17/17 startup-скриптов без ошибок.
- Уточнена фактическая версия DivineRPG из игрового лога.
- Добавлен отчёт первой runtime-проверки.


## KubeJS

### Удалено или заменено

- Удалены разрозненные скрипты `born_in_chaos_health.js` и `divinerpg_non_boss_health.js`.
- Удалён исходный `boss_progression.js`, не согласованный с целевой маршрутной сеткой и содержавший ссылки на необязательные моды и иной порядок прогрессии.
- Удалены демонстрационные `main.js`.
- Удалены два небезопасных datapack-рецепта Mystical Agriculture, которые конфликтовали с новой системой.

### Добавлено

- `startup_scripts/expert_components.js` — 10 компонентов и 9 печатей прогрессии.
- `server_scripts/expert_recipes.js` — межмодовая цепочка и стратегические замены рецептов.
- `server_scripts/combat_scaling.js` — единый масштабатор здоровья.
- `client_scripts/expert_tooltips.js` — русские подсказки компонентов и печатей.
- Обновлён `assets/boss_checklist/bosses.json`: 38 боссов, включая 23 босса DivineRPG; удалены ссылки на отсутствующие аддоны.

### Сохранено

- Пользовательская система эссенций и кристаллов: dimyanit, eduardit, dannexit, emkoviy, rakuniy и kodeksit.
- Скрипт уровней эссенций Mystical Agriculture.

## FTB Quests

- Добавлена глава `divinerpg.snbt`: 20 квестов.
- Добавлена глава `expert_progression.snbt`: 11 квестов.
- Связаны DivineRPG и технологические этапы через многоразовые печати.
- Изменены зависимости в главах:
  - Mekanism Part 1;
  - Industrial Foregoing;
  - Applied Energistics 2;
  - Powah;
  - Draconic Evolution;
  - ProjectE;
  - Avaritia;
  - Mystical Agriculture;
  - Main Questline Part 1.
- Исправлены битые ссылки в `tfmg_electricity.snbt` и `tfmg_steel.snbt`.
- Расширены `en_us.snbt` и `ru_ru.snbt`.

## Не выполнено автоматически

- Не удалены моды.
- Не добавлен JAR DivineRPG.
- Не выполнен запуск Minecraft и профильный тест TPS/памяти.
- Не переведены вручную все тексты всех старых квестов; полностью переведена новая прогрессия и актуализированы изменённые критические узлы.
