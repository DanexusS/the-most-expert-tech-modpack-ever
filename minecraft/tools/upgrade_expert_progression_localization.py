from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"

ENTRIES: dict[str, dict[str, str | list[str]]] = {
    "en_us": {
        "chapter.301DF0A89B0E6061.title": "Expert Progression — Operating Standard",
        "quest.1B663F652AEF7395.title": "Read Before Building",
        "quest.1B663F652AEF7395.quest_desc": [
            "This chapter is the mandatory technical spine of the pack, not a shopping list.",
            "Each milestone requires its component and a manual acceptance check. Confirm only when the component can be reproduced without emergency hand-crafting.",
            "Static calculations provide pre-release limits; measured in-world behavior overrides every theoretical estimate."
        ],
        "quest.A17E4D09B8C2F101.title": "Field Engineering Kit",
        "quest.A17E4D09B8C2F101.quest_desc": [
            "Build the first reliable structural and conductive kit from Immersive Engineering materials, copper and protected glass.",
            "Acceptance: inputs are labelled, no boss drop is consumed, and enough ordinary material remains for at least four additional kits.",
            "This branch establishes manual fabrication before automated machinery is allowed to hide poor preparation."
        ],
        "quest.B29F510AC7D3E202.title": "Power Regulation Unit",
        "quest.B29F510AC7D3E202.quest_desc": [
            "Combine redstone control, conductive materials and a Modern Industrialization motor.",
            "Acceptance: the motor supply is repeatable, the energy path is protected, and buffers cover at least three normal crafting cycles.",
            "Power distribution and motion control are independent engineering problems; neither requires Create as the first machine."
        ],
        "quest.C3A0621BD8E4F303.title": "Materials Analysis Matrix",
        "quest.C3A0621BD8E4F303.quest_desc": [
            "Prepare the analytical layer from quartz, redstone, glass and comparator logic.",
            "Acceptance: quartz and redstone inputs can support four repeated crafts and the output has dedicated storage.",
            "Later circuits assume that materials are measured and classified instead of guessed."
        ],
        "quest.5E5CFA388D9EC683.title": "Mechanical Core — Convergence Test",
        "quest.5E5CFA388D9EC683.quest_desc": [
            "Join field engineering, regulated power and material analysis into the first common industrial component.",
            "Acceptance: all three branches can supply another four cores without dismantling machines or borrowing protected progression items.",
            "A core is complete only when its production route is documented and repeatable."
        ],
        "quest.D4B1732CE9F50404.title": "Industrial Kinetic Interface",
        "quest.D4B1732CE9F50404.quest_desc": [
            "Create enters the factory here as a specialized mechanical automation system.",
            "Acceptance: the kinetic network remains below 75% of available stress during the intended workload and can be isolated with a clutch or equivalent control.",
            "Do not compensate for an unstable design by adding shafts blindly; measure stress and speed together."
        ],
        "quest.16838B1A7CA4BE89.title": "Industrial Frame — Repeatability Gate",
        "quest.16838B1A7CA4BE89.quest_desc": [
            "The frame proves that structural parts, motors and kinetic automation operate as one production standard.",
            "Acceptance: produce or provision a batch of four, automate normal inputs and outputs, and prevent full by-product storage from deadlocking the line.",
            "Strategic machines use this frame because it represents integrated infrastructure, not merely expensive metal."
        ],
        "quest.31E4D1B55CA6546E.title": "Precision Circuit — Controlled Electronics",
        "quest.31E4D1B55CA6546E.quest_desc": [
            "Unify early AE2, Modern Industrialization and Mekanism electronics into a common precision standard.",
            "Acceptance: maintain processor materials for eight circuits, separate intermediate storage, and expose the slowest step for later scaling.",
            "A circuit line that requires manual rescue every craft has not passed this gate."
        ],
        "quest.33D42DC311D2F9BE.title": "Chemical Processor — Closed Material Flow",
        "quest.33D42DC311D2F9BE.quest_desc": [
            "Connect controlled electronics to chemical processing and pressure-dependent infrastructure.",
            "Acceptance: complete three consecutive cycles while every fluid, gas and solid by-product has a valid destination; buffer at least two cycles of critical inputs.",
            "Any unhandled secondary output is treated as a production failure."
        ],
        "quest.0D54023AEE59ED08.title": "Bioindustrial Matrix — Sustainable Throughput",
        "quest.0D54023AEE59ED08.quest_desc": [
            "Industrial Foregoing and managed biological production begin at this milestone.",
            "Acceptance: run three complete production batches without manual refilling, overflow deletion or moving machines between cycles.",
            "Resource generation must be controllable, stoppable and bounded by the previous chemical stage."
        ],
        "quest.4377C3797509D983.title": "Quantum Logic — Network Capacity Gate",
        "quest.4377C3797509D983.quest_desc": [
            "Build the logic standard for AE2 controllers, quantum links and late digital infrastructure.",
            "Acceptance: channels, power and storage retain at least 25% free capacity under normal factory load, and critical subnetworks have labelled isolation points.",
            "A larger network is not a better network when one cable failure stops the entire base."
        ],
        "quest.3EE8E42D0138A34A.title": "Resonant Core — Energy Stability Gate",
        "quest.3EE8E42D0138A34A.quest_desc": [
            "Unify Nitro Powah, high-tier Mekanism control and the entry requirements for Draconic Evolution.",
            "Acceptance: stored energy covers two complete high-tier production cycles after generation stops, and the network survives simultaneous machine startup.",
            "Peak demand, not average demand, determines whether this stage is stable."
        ],
        "quest.742C709923A5AB9B.title": "Draconic Processor — Hazard Control",
        "quest.742C709923A5AB9B.quest_desc": [
            "Awakened infrastructure begins only after the resonant energy stage is stable.",
            "Acceptance: hazardous machines have physical separation, remote shutdown, recovery access and replacement materials outside the hazard zone.",
            "Raw output does not compensate for an installation that destroys its own control system."
        ],
        "quest.6B91727E7931BD65.title": "Transmutation Matrix — Controlled EMC",
        "quest.6B91727E7931BD65.quest_desc": [
            "ProjectE is introduced as a governed conversion system, not permission to erase the progression graph.",
            "Acceptance: seal-locked and non-EMC items stay outside automated conversion, import and export are separated, and excluded materials are documented.",
            "Transmutation may remove repetition; it must not remove technological prerequisites."
        ],
        "quest.0D199D42E619C8CF.title": "Cosmic Catalyst — Final Integration Review",
        "quest.0D199D42E619C8CF.quest_desc": [
            "The catalyst joins Avaritia-scale crafting with every preceding industrial standard.",
            "Acceptance: the factory can reproduce all prerequisite components, critical patterns and control items from stored or renewable inputs after a controlled shutdown.",
            "Keep independent backups of progression seals, digital patterns and recovery equipment before calling the endgame infrastructure complete."
        ]
    },
    "ru_ru": {
        "chapter.301DF0A89B0E6061.title": "Экспертная прогрессия — производственный стандарт",
        "quest.1B663F652AEF7395.title": "Прочитать перед строительством",
        "quest.1B663F652AEF7395.quest_desc": [
            "Эта глава — обязательный технологический каркас сборки, а не список покупок.",
            "Каждый этап требует компонент и ручную приёмку. Подтверждайте её только тогда, когда компонент можно повторно произвести без аварийного ручного крафта.",
            "Статические расчёты задают предварительные пределы; измерения внутри мира всегда имеют больший приоритет."
        ],
        "quest.A17E4D09B8C2F101.title": "Комплект полевого инженера",
        "quest.A17E4D09B8C2F101.quest_desc": [
            "Соберите первую надёжную конструкционную и проводящую основу из материалов Immersive Engineering, меди и защищённого стекла.",
            "Приёмка: входы подписаны, боссовый дроп не расходуется, обычных материалов достаточно минимум ещё на четыре комплекта.",
            "Эта ветвь закрепляет ручное производство до того, как автоматизация начнёт скрывать плохую подготовку."
        ],
        "quest.B29F510AC7D3E202.title": "Блок регулирования энергии",
        "quest.B29F510AC7D3E202.quest_desc": [
            "Объедините редстоун-управление, проводящие материалы и мотор Modern Industrialization.",
            "Приёмка: моторы производятся повторяемо, энерголиния защищена, буферы покрывают минимум три обычных цикла крафта.",
            "Распределение энергии и управление движением — разные инженерные задачи; ни одна из них не требует начинать с Create."
        ],
        "quest.C3A0621BD8E4F303.title": "Матрица анализа материалов",
        "quest.C3A0621BD8E4F303.quest_desc": [
            "Подготовьте аналитический слой из кварца, редстоуна, стекла и логики компаратора.",
            "Приёмка: запас кварца и редстоуна выдерживает четыре повторных крафта, для результата выделено отдельное хранилище.",
            "Поздние схемы предполагают, что материалы измерены и классифицированы, а не выбраны наугад."
        ],
        "quest.5E5CFA388D9EC683.title": "Механическое ядро — проверка схождения",
        "quest.5E5CFA388D9EC683.quest_desc": [
            "Объедините полевую инженерию, регулируемую энергию и анализ материалов в первый общий промышленный компонент.",
            "Приёмка: все три ветви способны обеспечить ещё четыре ядра без демонтажа машин и заимствования защищённых предметов прогрессии.",
            "Ядро считается завершённым только при документированном и повторяемом маршруте производства."
        ],
        "quest.D4B1732CE9F50404.title": "Кинетический промышленный интерфейс",
        "quest.D4B1732CE9F50404.quest_desc": [
            "Create входит в фабрику как специализированная система механической автоматизации.",
            "Приёмка: при штатной нагрузке сеть использует не более 75% доступной мощности напряжения и отключается муфтой или равноценным устройством.",
            "Не скрывайте нестабильную схему лишними валами: измеряйте скорость и нагрузку одновременно."
        ],
        "quest.16838B1A7CA4BE89.title": "Промышленная рама — допуск повторяемости",
        "quest.16838B1A7CA4BE89.quest_desc": [
            "Рама подтверждает, что конструкции, моторы и кинетическая автоматизация работают как единый стандарт.",
            "Приёмка: произведена или обеспечена партия из четырёх рам, обычные входы и выходы автоматизированы, заполнение побочного выхода не блокирует линию.",
            "Стратегические машины используют эту раму как признак готовой инфраструктуры, а не просто дорогого металла."
        ],
        "quest.31E4D1B55CA6546E.title": "Прецизионная схема — управляемая электроника",
        "quest.31E4D1B55CA6546E.quest_desc": [
            "Объедините раннюю электронику AE2, Modern Industrialization и Mekanism в общий стандарт точности.",
            "Приёмка: поддерживается запас процессорных материалов на восемь схем, промежуточные детали хранятся отдельно, самое медленное звено явно обозначено.",
            "Линия, которую приходится вручную спасать при каждом крафте, этот этап не прошла."
        ],
        "quest.33D42DC311D2F9BE.title": "Химический процессор — замкнутый поток материалов",
        "quest.33D42DC311D2F9BE.quest_desc": [
            "Свяжите управляемую электронику с химическими процессами и инфраструктурой давления.",
            "Приёмка: выполнены три последовательных цикла, у каждой жидкости, газа и твёрдого побочного продукта есть назначение, критические входы запасены минимум на два цикла.",
            "Любой необработанный вторичный выход считается отказом производства."
        ],
        "quest.0D54023AEE59ED08.title": "Биоиндустриальная матрица — устойчивый выпуск",
        "quest.0D54023AEE59ED08.quest_desc": [
            "На этом этапе начинаются Industrial Foregoing и управляемое биологическое производство.",
            "Приёмка: три полные партии проходят без ручной дозаправки, удаления переполнения и перестановки машин между циклами.",
            "Генерация ресурсов должна быть управляемой, отключаемой и ограниченной предыдущим химическим этапом."
        ],
        "quest.4377C3797509D983.title": "Квантовая логика — допуск ёмкости сети",
        "quest.4377C3797509D983.quest_desc": [
            "Создайте логический стандарт для контроллеров AE2, квантовых связей и поздней цифровой инфраструктуры.",
            "Приёмка: каналы, энергия и хранилище сохраняют минимум 25% свободной ёмкости при штатной нагрузке, критические подсети имеют подписанные точки отключения.",
            "Большая сеть не является хорошей, если один повреждённый кабель останавливает всю базу."
        ],
        "quest.3EE8E42D0138A34A.title": "Резонансное ядро — допуск стабильности энергии",
        "quest.3EE8E42D0138A34A.quest_desc": [
            "Объедините Nitro Powah, высшее управление Mekanism и входные требования Draconic Evolution.",
            "Приёмка: накопленной энергии хватает на два полных высокоуровневых производственных цикла после остановки генерации, сеть выдерживает одновременный запуск машин.",
            "Стабильность этапа определяется пиковой, а не средней нагрузкой."
        ],
        "quest.742C709923A5AB9B.title": "Драконический процессор — контроль опасности",
        "quest.742C709923A5AB9B.quest_desc": [
            "Пробуждённая инфраструктура начинается только после стабилизации резонансной энергетики.",
            "Приёмка: опасные машины физически отделены, имеют удалённое отключение, доступ для восстановления и запасные материалы вне опасной зоны.",
            "Высокий выпуск не оправдывает установку, уничтожающую собственную систему управления."
        ],
        "quest.6B91727E7931BD65.title": "Матрица трансмутации — контролируемый EMC",
        "quest.6B91727E7931BD65.quest_desc": [
            "ProjectE вводится как регулируемая система преобразования, а не разрешение стереть граф прогрессии.",
            "Приёмка: предметы с печатями и без EMC исключены из автоматического преобразования, импорт отделён от экспорта, список исключений задокументирован.",
            "Трансмутация может убрать повторение, но не технологические требования."
        ],
        "quest.0D199D42E619C8CF.title": "Космический катализатор — итоговая приёмка",
        "quest.0D199D42E619C8CF.quest_desc": [
            "Катализатор объединяет крафты масштаба Avaritia со всеми предыдущими промышленными стандартами.",
            "Приёмка: после контролируемой остановки фабрика способна воспроизвести все компоненты, шаблоны и управляющие предметы из запасённых или возобновляемых входов.",
            "До признания эндгейма завершённым храните независимые копии печатей прогрессии, цифровых шаблонов и аварийного оборудования."
        ]
    }
}

KEY_RE = re.compile(r"(?m)^\t([A-Za-z0-9_.-]+):")


def render(value: str | list[str]) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def upsert(text: str, key: str, value: str | list[str]) -> tuple[str, bool]:
    rendered = f"\t{key}: {render(value)}\n"
    pattern = re.compile(
        rf"(?ms)^\t{re.escape(key)}:.*?(?=^\t[A-Za-z0-9_.-]+:|^\}}\s*$)"
    )
    updated, count = pattern.subn(rendered, text, count=1)
    if count:
        return updated, updated != text

    closing = text.rfind("}")
    if closing < 0 or text[closing + 1 :].strip():
        raise RuntimeError("Localization file has an unexpected ending")
    return text[:closing].rstrip() + "\n" + rendered + "}\n", True


def synchronize(locale: str, entries: dict[str, str | list[str]]) -> bool:
    path = LANG_DIR / f"{locale}.snbt"
    text = path.read_text(encoding="utf-8")
    changed = False
    for key, value in entries.items():
        text, entry_changed = upsert(text, key, value)
        changed = changed or entry_changed
    if changed:
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"{locale}: upgraded {len(entries)} expert progression localization entries")
    else:
        print(f"{locale}: expert progression localization already upgraded")
    return changed


def main() -> int:
    changed = False
    for locale, entries in ENTRIES.items():
        changed = synchronize(locale, entries) or changed
    print("Expert progression localization changed" if changed else "Expert progression localization unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
