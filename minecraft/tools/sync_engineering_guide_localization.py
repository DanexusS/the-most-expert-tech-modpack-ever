from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"

ENTRIES = {
    "en_us": {
        "chapter.5E684E5FDC0912E2.title": '"Engineering Foundations — Practical Guide"',
        "quest.2A0768299BEC7CCC.title": '"Three Foundations, One Industry"',
        "quest.2A0768299BEC7CCC.quest_desc": '["This chapter explains the redesigned opening of the expert progression.", "Field engineering, power regulation and materials analysis can be developed in parallel. Create becomes a specialized automation branch after the common mechanical foundation."]',
        "quest.436B911E8482D562.title": '"Field Engineering"',
        "quest.436B911E8482D562.quest_desc": '["The field kit represents reliable hand fabrication: structural components, copper conductors and protected observation surfaces.", "Keep a small reserve. It is a foundation component, not disposable filler."]',
        "quest.D9BFE27ABA2A8E46.title": '"Regulate Before You Scale"',
        "quest.D9BFE27ABA2A8E46.quest_desc": '["A motor is useful only when its energy and motion can be controlled.", "This branch joins redstone logic, conductive materials and a Modern Industrialization motor without requiring Create machinery first."]',
        "quest.B5B36564426EF7E8.title": '"Measure the Material"',
        "quest.B5B36564426EF7E8.quest_desc": '["Quartz, a comparator and redstone form the first analytical layer of the pack.", "The matrix represents measurement and classification. Later circuits assume that materials have already been tested instead of guessed."]',
        "quest.605660875B4C79AF.title": '"Convergence: Mechanical Core"',
        "quest.605660875B4C79AF.quest_desc": '["The three opening branches meet here.", "The mechanical core is the first shared industrial standard: structural reliability, regulated motion and measured materials in one reusable component."]',
        "quest.3ED4D6DED8602830.title": '"Create Enters the Factory"',
        "quest.3ED4D6DED8602830.quest_desc": '["Create is now an engineering specialization rather than the compulsory first step.", "The kinetic interface connects andesite mechanics to the common core and prepares machines for the industrial frame."]',
        "quest.20D0E8E84656635C.title": '"Stress Capacity"',
        "quest.20D0E8E84656635C.quest_desc": '["Create networks fail when total stress impact exceeds available stress capacity.", "Read the network before expanding it. Add generation or split the network instead of hiding an overloaded design behind extra shafts."]',
        "quest.D0D83BE590660FF8.title": '"Speed Is Not Free"',
        "quest.D0D83BE590660FF8.quest_desc": '["Rotational speed changes throughput, but faster machines usually demand more stress.", "Measure RPM and stress together. A stable slower line is more useful than a fast line that stops under load."]',
        "quest.B6A47F9FF2C532F8.title": '"Ratios and Transmission"',
        "quest.B6A47F9FF2C532F8.quest_desc": '["Small and large cogwheels change rotational speed when meshed correctly.", "Design ratios around the slowest process, then use clutches, gearshifts or separate branches to prevent one machine from destabilizing the entire factory."]',
        "quest.C1766C57141D1D5A.title": '"Coke Oven Discipline"',
        "quest.C1766C57141D1D5A.quest_desc": '["Build the complete Immersive Engineering coke-oven shell and verify the multiblock before loading bulk fuel.", "Coke and creosote are both products. Plan storage for the liquid instead of allowing a full output tank to stop production."]',
        "quest.E771260B5C787ACA.title": '"Use Every Drop of Creosote"',
        "quest.E771260B5C787ACA.quest_desc": '["Treated wood is an early infrastructure material, not decoration only.", "Convert creosote into planned batches and keep a buffer for wiring, scaffolding and machines. Oversized uncontrolled tanks only postpone a blockage."]',
        "quest.C36CEA6924CE2E77.title": '"Motor as a Standard Component"',
        "quest.C36CEA6924CE2E77.quest_desc": '["Modern Industrialization motors connect electrical industry to mechanical work.", "Treat motors as stocked components. Producing them one at a time will become a bottleneck as machine hulls and cross-mod parts begin consuming them."]',
        "quest.B4F20A0C67EF1200.title": '"Power Networks Need Limits"',
        "quest.B4F20A0C67EF1200.quest_desc": '["Do not connect unfamiliar machines to the largest available network without checking their tier and demand.", "Separate generation, buffering and consumers. Label lines and leave capacity for startup spikes and later automation."]',
        "quest.984E0159892B0E76.title": '"Automation Readiness Check"',
        "quest.984E0159892B0E76.quest_desc": '["Before advancing, verify that each branch can be repeated without manual emergency work.", "Provide buffered inputs, controlled outputs, overflow handling, maintenance access and a visible indication of stalled production."]',
        "quest.F8CB87B3063D8541.title": '"Industrial Frame"',
        "quest.F8CB87B3063D8541.quest_desc": '["The industrial frame proves that the three foundations and the Create interface are functioning together.", "It gates strategic machines because it represents an integrated factory standard, not because it is merely expensive metal."]',
        "quest.515835E1E6E7125D.title": '"Foundation Review"',
        "quest.515835E1E6E7125D.quest_desc": '["You should now be able to explain stress, speed, material analysis, motor production and creosote handling without relying on trial and error.", "Document your layouts and bottlenecks. The next stages will multiply throughput and make undocumented improvisation expensive."]',
    },
    "ru_ru": {
        "chapter.5E684E5FDC0912E2.title": '"Основы инженерии — практическое руководство"',
        "quest.2A0768299BEC7CCC.title": '"Три основы одной промышленности"',
        "quest.2A0768299BEC7CCC.quest_desc": '["Эта глава объясняет переработанное начало экспертной прогрессии.", "Полевая инженерия, регулирование энергии и анализ материалов развиваются параллельно. Create становится отдельной ветвью автоматизации после общей механической основы."]',
        "quest.436B911E8482D562.title": '"Полевая инженерия"',
        "quest.436B911E8482D562.quest_desc": '["Полевой комплект означает надёжное ручное изготовление: прочные компоненты, медные проводники и защищённые поверхности наблюдения.", "Храните небольшой запас. Это базовый компонент, а не одноразовый наполнитель рецепта."]',
        "quest.D9BFE27ABA2A8E46.title": '"Сначала регулирование, потом масштаб"',
        "quest.D9BFE27ABA2A8E46.quest_desc": '["Мотор полезен только тогда, когда его питание и движение можно контролировать.", "Эта ветвь объединяет редстоун-логику, проводящие материалы и мотор Modern Industrialization без обязательных механизмов Create."]',
        "quest.B5B36564426EF7E8.title": '"Измерьте материал"',
        "quest.B5B36564426EF7E8.quest_desc": '["Кварц, компаратор и редстоун образуют первый аналитический уровень сборки.", "Матрица отвечает за измерение и классификацию. Поздние схемы предполагают, что материалы уже проверены, а не выбраны наугад."]',
        "quest.605660875B4C79AF.title": '"Схождение: механическое ядро"',
        "quest.605660875B4C79AF.quest_desc": '["Здесь сходятся три стартовые ветви.", "Механическое ядро — первый общий промышленный стандарт: надёжная конструкция, регулируемое движение и измеренные материалы в одном повторяемом компоненте."]',
        "quest.3ED4D6DED8602830.title": '"Create входит в фабрику"',
        "quest.3ED4D6DED8602830.quest_desc": '["Create теперь является инженерной специализацией, а не обязательным первым шагом.", "Кинетический интерфейс соединяет андезитовую механику с общим ядром и готовит машины к промышленной раме."]',
        "quest.20D0E8E84656635C.title": '"Нагрузочная способность"',
        "quest.20D0E8E84656635C.quest_desc": '["Сети Create останавливаются, когда суммарная нагрузка превышает доступную нагрузочную способность.", "Проверяйте сеть до расширения. Увеличивайте генерацию или разделяйте линии, а не маскируйте перегрузку дополнительными валами."]',
        "quest.D0D83BE590660FF8.title": '"Скорость не бесплатна"',
        "quest.D0D83BE590660FF8.quest_desc": '["Скорость вращения меняет производительность, но ускоренные машины обычно требуют больше нагрузочной способности.", "Измеряйте обороты и нагрузку вместе. Стабильная медленная линия полезнее быстрой линии, которая останавливается под нагрузкой."]',
        "quest.B6A47F9FF2C532F8.title": '"Передаточные отношения"',
        "quest.B6A47F9FF2C532F8.quest_desc": '["Малые и большие шестерни при правильном соединении изменяют скорость вращения.", "Проектируйте отношения под самый медленный процесс, затем используйте муфты, коробки передач или отдельные ветви, чтобы одна машина не останавливала всю фабрику."]',
        "quest.C1766C57141D1D5A.title": '"Дисциплина коксовой печи"',
        "quest.C1766C57141D1D5A.quest_desc": '["Постройте полный корпус коксовой печи Immersive Engineering и проверьте мультиблок до массовой загрузки топлива.", "Кокс и креозот являются продуктами. Заранее подготовьте хранилище жидкости, иначе заполненный выход остановит производство."]',
        "quest.E771260B5C787ACA.title": '"Используйте весь креозот"',
        "quest.E771260B5C787ACA.quest_desc": '["Обработанная древесина — ранний инфраструктурный материал, а не только декор.", "Перерабатывайте креозот плановыми партиями и держите запас для проводки, конструкций и машин. Огромный бесконтрольный резервуар лишь откладывает засорение линии."]',
        "quest.C36CEA6924CE2E77.title": '"Мотор как стандартный компонент"',
        "quest.C36CEA6924CE2E77.quest_desc": '["Моторы Modern Industrialization связывают электрическую промышленность с механической работой.", "Производите моторы серийно. Изготовление по одному станет узким местом, когда корпуса машин и межмодовые компоненты начнут массово их потреблять."]',
        "quest.B4F20A0C67EF1200.title": '"Энергосетям нужны пределы"',
        "quest.B4F20A0C67EF1200.quest_desc": '["Не подключайте незнакомые машины к крупнейшей доступной сети без проверки их уровня и потребления.", "Разделяйте генерацию, буфер и потребителей. Подписывайте линии и оставляйте запас для пусковых нагрузок и будущей автоматизации."]',
        "quest.984E0159892B0E76.title": '"Проверка готовности к автоматизации"',
        "quest.984E0159892B0E76.quest_desc": '["Перед переходом дальше убедитесь, что каждую ветвь можно повторять без ручного устранения аварий.", "Нужны буферизованные входы, контролируемые выходы, защита от переполнения, доступ для обслуживания и видимый признак остановки производства."]',
        "quest.F8CB87B3063D8541.title": '"Промышленная рама"',
        "quest.F8CB87B3063D8541.quest_desc": '["Промышленная рама доказывает, что три основы и интерфейс Create работают совместно.", "Она ограничивает стратегические машины, потому что представляет единый фабричный стандарт, а не просто дорогой набор металлов."]',
        "quest.515835E1E6E7125D.title": '"Проверка инженерной основы"',
        "quest.515835E1E6E7125D.quest_desc": '["Теперь вы должны уметь объяснить нагрузку, скорость, анализ материалов, производство моторов и обращение с креозотом без перебора случайных решений.", "Документируйте схемы и узкие места. Следующие этапы увеличат объёмы, и незаписанная импровизация станет слишком дорогой."]',
    },
}


def format_block(entries: dict[str, str]) -> str:
    return "\n".join(f"\t{key}: {value}" for key, value in entries.items())


def synchronize(locale: str, entries: dict[str, str]) -> bool:
    path = LANG_DIR / f"{locale}.snbt"
    if not path.is_file():
        raise FileNotFoundError(f"Missing FTB Quests localization file: {path}")

    text = path.read_text(encoding="utf-8")
    present = {key for key in entries if f"{key}:" in text}
    if present == set(entries):
        print(f"{locale}: engineering guide localization already synchronized")
        return False
    if present:
        missing = sorted(set(entries) - present)
        raise RuntimeError(
            f"{locale}: partial engineering guide localization; missing keys: {missing}"
        )

    closing = text.rfind("}")
    if closing < 0 or text[closing + 1 :].strip():
        raise RuntimeError(f"{locale}: localization file has an unexpected ending")

    updated = f"{text[:closing].rstrip()}\n{format_block(entries)}\n}}\n"
    path.write_text(updated, encoding="utf-8", newline="\n")
    print(f"{locale}: added {len(entries)} engineering guide localization keys")
    return True


def main() -> int:
    changed = False
    for locale, entries in ENTRIES.items():
        changed = synchronize(locale, entries) or changed
    print("Engineering guide synchronized" if changed else "Engineering guide unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
