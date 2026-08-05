from __future__ import annotations

import json
import re
from pathlib import Path

from manual_generator_common import format_array, stable_id, upsert_localization

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "expert_progression_spine.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
FILENAME = "expert_progression_spine"
CHAPTER_ID = stable_id(f"chapter:{FILENAME}")

STAGE_GUIDANCE = {
    "field_foundations": (
        "recoverable manual work, early material identity and survival safety before automation",
        "восстанавливаемую ручную работу, распознавание ранних материалов и безопасность до автоматизации",
        "manual batch time, spare tools, protected storage and recovery after a simulated loss",
        "время ручной партии, запасные инструменты, защищённое хранение и восстановление после условной потери",
    ),
    "steam_metallurgy": (
        "water-secure steam, coke and creosote handling, repeatable steel and common structural standards",
        "защищённый пар, работу с коксом и креозотом, повторяемую сталь и общие конструкционные стандарты",
        "fuel, water, steam, solid and fluid yields plus clean shutdown under blocked output",
        "расход топлива и воды, выход пара, твёрдых и жидких продуктов и чистую остановку при блокировке",
    ),
    "regulated_electricity": (
        "generation, voltage boundaries, finite reserve and protected distribution across incompatible power systems",
        "генерацию, границы напряжения, конечный резерв и защищённое распределение между несовместимыми энергосистемами",
        "peak demand, transfer limits, reserve duration, overload response and black-start order",
        "пиковый спрос, пределы передачи, длительность резерва, реакцию на перегрузку и порядок холодного запуска",
    ),
    "kinetic_automation": (
        "Create stress budgets, transmission ratios, bounded processing lines and controlled sequenced assembly",
        "бюджеты нагрузки Create, передаточные отношения, ограниченные линии обработки и управляемую последовательную сборку",
        "stress margin, rotational speed, batch yield, byproduct routing and recovery from a stopped sequence",
        "запас нагрузки, скорость вращения, выход партии, маршрут побочных продуктов и восстановление остановленной последовательности",
    ),
    "precision_manufacturing": (
        "compressed materials, stocked recurring components, recipe-locked assembly and formal quality release",
        "сжатые материалы, запас повторяющихся деталей, фиксированную сборку и формальную приёмку качества",
        "component stock levels, repeat batch accuracy, returned tooling, defect quarantine and replacement time",
        "уровни запасов, точность повторной партии, возврат оснастки, карантин брака и время замены",
    ),
    "digital_storage": (
        "certus and processor production, storage-cell limits and channel-aware digital infrastructure",
        "производство церта и процессоров, пределы ячеек и цифровую инфраструктуру с учётом каналов",
        "processor throughput, cell type capacity, migration counts, channel reserve and subnet recovery",
        "скорость процессоров, ёмкость типов ячеек, сверку переноса, резерв каналов и восстановление подсети",
    ),
    "process_chemistry": (
        "infusion, gases, pressure, plastic and useful byproducts with strict material and phase ownership",
        "инфузию, газы, давление, пластик и полезные побочные продукты со строгим владением материалами и фазами",
        "chemical and pressure reserves, conversion ratios, purge time, byproduct capacity and contamination response",
        "резервы химикатов и давления, соотношения преобразования, время продувки, ёмкость побочных продуктов и реакцию на загрязнение",
    ),
    "industrial_scale": (
        "parallel machines, fluid logistics, state-based factory control and recoverable maintenance",
        "параллельные машины, жидкостную логистику, управление по состоянию и восстанавливаемое обслуживание",
        "single-line and parallel throughput, buffer occupancy, stop conditions, bottleneck and repair duration",
        "скорость одной и нескольких линий, заполнение буферов, условия остановки, узкое место и длительность ремонта",
    ),
    "controlled_resources": (
        "biological inputs, legal post-discovery simulation, renewable materials and positive-feedback prevention",
        "биологические входы, честную симуляцию после открытия, возобновляемые материалы и защиту от положительной обратной связи",
        "first-acquisition proof, renewable yield, simulation cost, protected-output blacklist and conservation audit",
        "доказательство первого получения, возобновляемый выход, стоимость симуляции, чёрный список защищённого лута и аудит сохранения",
    ),
    "applied_logistics": (
        "controller-scale AE2 networks, autocrafting, isolated subnets and cross-dimensional transfer",
        "крупные сети AE2, автокрафт, изолированные подсети и межпространственную передачу",
        "channel maps, CPU use, request completion, subnet handoff, remote energy and one-sided link recovery",
        "карты каналов, использование CPU, завершение запроса, передачу подсети, удалённую энергию и восстановление односторонней связи",
    ),
    "resonant_energy": (
        "Nitro generation, mass storage, high-current trunks and explicit late-factory failure modes",
        "нитро-генерацию, массовое хранение, магистрали высокой мощности и явные отказы поздней фабрики",
        "sustained output, storage capacity, provider rate, surge margin, load shedding and generator-loss recovery",
        "устойчивый выход, ёмкость, скорость провайдеров, запас по скачку, сброс нагрузки и восстановление после потери генератора",
    ),
    "nuclear_antimatter": (
        "radiation containment, conservative fission, fusion support and authoritative SPS antimatter production",
        "радиационное сдерживание, консервативное деление, поддержку синтеза и авторитетное производство антиматерии в SPS",
        "burn or injection rate, coolant reserve, waste capacity, SCRAM response, SPS energy and pellet cost",
        "скорость горения или впрыска, резерв охлаждения, ёмкость отходов, аварийную остановку, энергию SPS и стоимость гранулы",
    ),
    "dimensional_materials": (
        "safe expeditions, first-victory permissions, classified trophies and repeatable remote supply chains",
        "безопасные экспедиции, допуски первой победы, классифицированные трофеи и повторяемые удалённые цепочки снабжения",
        "travel reserve, retreat and recovery, boss evidence, ordinary-versus-unique drop policy and cargo reconciliation",
        "резерв поездки, отступление и восстановление, доказательство босса, политику обычного и уникального лута и сверку груза",
    ),
    "draconic_engineering": (
        "draconium processing, Wyvern systems, awakened infrastructure and extreme energy containment",
        "обработку дракония, системы Виверны, пробуждённую инфраструктуру и экстремальное сдерживание энергии",
        "material yield, injector energy, permission return, repair reserve, containment transfer and isolation response",
        "выход материала, энергию инжекторов, возврат допуска, ремонтный резерв, передачу сдерживания и реакцию изоляции",
    ),
    "contained_transmutation": (
        "EMC accounting, matter tiers, late transmutation access and hard automation limits",
        "учёт EMC, уровни материи, поздний доступ к трансмутации и жёсткие ограничения автоматизации",
        "EMC conservation, zero-value gated items, matter production rate, learned-item allowlist and loop detection",
        "сохранение EMC, нулевые закрытые предметы, скорость материи, белый список изученных предметов и обнаружение циклов",
    ),
    "extreme_fabrication": (
        "large-grid crafting, automated singularity supply, convergence components and factory-scale assembly",
        "крупноматричный крафт, автоматическое снабжение сингулярностями, компоненты схождения и сборку фабричного масштаба",
        "exact bulk counts, legal resource sources, previous-tier ancestry, request cycle time and blocked-output recovery",
        "точные массовые количества, честные источники, происхождение от предыдущего уровня, время запроса и восстановление при полном выходе",
    ),
    "cosmic_synthesis": (
        "Infinity materials, stellar resources, cosmic energy and a synchronized final supply chain",
        "материалы Бесконечности, звёздные ресурсы, космическую энергию и синхронизированную финальную цепочку",
        "domain readiness, stellar cargo, cosmic reserve, Infinity batch cost, slowest path and interrupted-cycle recovery",
        "готовность направлений, звёздный груз, космический резерв, стоимость партии Бесконечности, самый медленный путь и восстановление цикла",
    ),
    "creative_convergence": (
        "creative components, limit-removing infrastructure, an integrated mastery project and final release audit",
        "творческие компоненты, снимающую ограничения инфраструктуру, интегрированный проект освоения и финальный релизный аудит",
        "all stage proofs, authoritative creative recipes, safety boundaries, project throughput, controlled failure and release reports",
        "доказательства всех этапов, авторитетные творческие рецепты, границы безопасности, скорость проекта, контролируемый отказ и релизные отчёты",
    ),
}

SUBSTAGE_HINTS = (
    (("safety", "recovery", "maintenance", "failure", "audit"), "failure prevention, safe shutdown and documented recovery", "предотвращение отказов, безопасную остановку и задокументированное восстановление"),
    (("storage", "buffer", "capacity", "stock"), "finite capacity, reserve policy, overflow and verified inventory counts", "конечную ёмкость, резерв, переполнение и проверенные количества"),
    (("logistics", "distribution", "transmission", "supply", "links", "network"), "routing ownership, throughput, priority, isolation and link-loss recovery", "владение маршрутами, пропускную способность, приоритеты, изоляцию и восстановление связи"),
    (("craft", "assembly", "fabrication", "manufacturing", "component"), "recipe ownership, previous-tier ancestry, reusable tools and repeatable batches", "владение рецептом, происхождение от предыдущего уровня, многоразовые инструменты и повторяемые партии"),
    (("resource", "material", "ore", "steel", "bronze", "draconium", "matter", "singularity", "infinity"), "legal first sources, conversion yield, renewable limits and protected-material policy", "честные первые источники, выход преобразования, пределы возобновления и политику защищённых материалов"),
    (("energy", "generation", "voltage", "current", "nuclear", "fusion", "sps"), "sustained power, reserve, transfer limits, protection and restart order", "устойчивую мощность, резерв, пределы передачи, защиту и порядок перезапуска"),
    (("chemical", "gas", "pressure", "plastic", "waste", "byproduct", "coolant"), "phase identity, ratios, containment, byproducts and contamination recovery", "идентичность фаз, соотношения, сдерживание, побочные продукты и восстановление после загрязнения"),
    (("boss", "expedition", "trophy", "dimensional", "stellar"), "first encounter, retreat, permission evidence, unique-drop protection and repeat supply", "первую встречу, отступление, доказательство допуска, защиту уникального лута и повторное снабжение"),
    (("automation", "control", "parallel", "processing", "simulation", "renewable"), "bounded unattended operation, state-based control, throughput and anti-loop checks", "ограниченную автономную работу, управление по состоянию, пропускную способность и защиту от циклов"),
)

LESSON_TYPES = (
    ("concept", "System Contract", "Контракт системы"),
    ("build", "Infrastructure Build", "Построение инфраструктуры"),
    ("acceptance", "Production Acceptance", "Производственная приёмка"),
)


def humanize(value: str) -> str:
    return value.replace("_", " ").title()


def substage_hint(substage: str) -> tuple[str, str]:
    for tokens, en, ru in SUBSTAGE_HINTS:
        if any(token in substage for token in tokens):
            return en, ru
    return (
        "inputs, outputs, constraints, ownership, repeatability and recovery",
        "входы, выходы, ограничения, владение, повторяемость и восстановление",
    )


def task_block(task_id: str, milestone: str | None = None) -> str:
    check_id = stable_id(f"{task_id}:check")
    blocks = [
        "{\n"
        f"\t\t\t\tid: \"{check_id}\"\n"
        "\t\t\t\ttype: \"checkmark\"\n"
        "\t\t\t}"
    ]
    if milestone:
        item_id = stable_id(f"{task_id}:milestone")
        blocks.insert(
            0,
            "{\n"
            f"\t\t\t\tid: \"{item_id}\"\n"
            f"\t\t\t\titem: {{ count: 1, id: \"{milestone}\" }}\n"
            "\t\t\t\ttype: \"item\"\n"
            "\t\t\t}",
        )
    return "[\n\t\t\t" + "\n\t\t\t".join(blocks) + "\n\t\t]"


def descriptions(stage: dict, substage: str, lesson: str) -> tuple[str, list[str], str, list[str]]:
    stage_id = stage["id"]
    title_en = stage["title_en"]
    title_ru = stage["title_ru"]
    sub_en = humanize(substage)
    sub_ru = sub_en
    domains = ", ".join(stage["required_domains"])
    outputs = ", ".join(stage["gated_outputs"])
    focus_en, focus_ru, measure_en, measure_ru = STAGE_GUIDANCE[stage_id]
    hint_en, hint_ru = substage_hint(substage)
    lesson_title = next(row for row in LESSON_TYPES if row[0] == lesson)

    if lesson == "concept":
        en = [
            f"Stage {stage['index']} — {title_en}: {sub_en} defines part of the mandatory route toward {stage['milestone']}. This stage joins {domains} and focuses on {focus_en}.",
            f"Study the system before building it: identify {hint_en}; list legal inputs, controlled outputs and failure boundaries, and explain why the substage belongs before the gated outputs {outputs}."
        ]
        ru = [
            f"Этап {stage['index']} — {title_ru}: {sub_ru} является частью обязательного пути к {stage['milestone']}. Этап связывает {domains} и развивает {focus_ru}.",
            f"Изучите систему до строительства: определите {hint_ru}; перечислите честные входы, управляемые выходы и границы отказа и объясните, почему подэтап должен предшествовать закрытым выходам {outputs}."
        ]
    elif lesson == "build":
        en = [
            f"Build a bounded demonstration of {sub_en} using at least two stage domains from {domains}. Assign every input, output, buffer, reusable component and control signal to an explicit owner.",
            f"The design must address {hint_en}. Prefer repeatable infrastructure over manual repetition, include a visible stop condition and leave enough access to replace one failed component without dismantling unrelated production."
        ]
        ru = [
            f"Постройте ограниченную демонстрацию {sub_ru}, используя минимум два направления этапа из {domains}. Назначьте владельца каждому входу, выходу, буферу, многоразовому компоненту и управляющему сигналу.",
            f"Проект должен учитывать {hint_ru}. Предпочитайте повторяемую инфраструктуру ручному повторению, добавьте видимое условие остановки и доступ для замены одного отказавшего компонента без разбора постороннего производства."
        ]
    else:
        en = [
            f"Accept the {sub_en} installation as a production system, not as a placed-block checklist. Run a representative cycle and record {measure_en}.",
            f"Test full output, missing input and interrupted power or transport; recover without duplication or loss, review rewards, EMC, loot, trade, simulation and alternate recipes, and confirm that progression advances only through the declared milestone {stage['milestone']}."
        ]
        ru = [
            f"Примите установку {sub_ru} как производственную систему, а не как список поставленных блоков. Выполните типовой цикл и запишите {measure_ru}.",
            f"Проверьте полный выход, отсутствующий вход и прерывание питания или транспорта; восстановитесь без копирования и потерь, проверьте награды, EMC, лут, торговлю, симуляцию и альтернативные рецепты и подтвердите продвижение только через {stage['milestone']}."
        ]

    return (
        f"{title_en} — {sub_en}: {lesson_title[1]}",
        en,
        f"{title_ru} — {sub_ru}: {lesson_title[2]}",
        ru,
    )


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    quest_blocks: list[str] = []
    localization: dict[str, dict[str, str]] = {"en_us": {}, "ru_ru": {}}
    localization["en_us"][f"chapter.{CHAPTER_ID}.title"] = json.dumps(
        "Expert Progression Spine — 18 Stages / 72 Substages", ensure_ascii=False
    )
    localization["ru_ru"][f"chapter.{CHAPTER_ID}.title"] = json.dumps(
        "Основная экспертная прогрессия — 18 этапов / 72 подэтапа", ensure_ascii=False
    )

    previous_id = ""
    total = 0
    for stage_offset, stage in enumerate(contract["stages"]):
        column = stage_offset % 6
        row = stage_offset // 6
        for sub_index, substage in enumerate(stage["substages"]):
            for lesson_index, (lesson, _, _) in enumerate(LESSON_TYPES):
                total += 1
                quest_id = stable_id(f"{FILENAME}:{stage['id']}:{substage}:{lesson}")
                task_namespace = f"{FILENAME}:{stage['id']}:{substage}:{lesson}"
                is_stage_final = sub_index == len(stage["substages"]) - 1 and lesson == "acceptance"
                milestone = stage["milestone"] if is_stage_final else None
                dependency = f"\n\t\tdependencies: [\"{previous_id}\"]" if previous_id else ""
                shape = "diamond" if lesson == "acceptance" else "hexagon"
                size = "1.5d" if is_stage_final else "1.0d"
                x = column * 18 + sub_index * 4 + lesson_index * 1.2
                y = row * 18 + sub_index * 3.5
                quest_blocks.append(
                    "\t{\n"
                    f"\t\tid: \"{quest_id}\"{dependency}\n"
                    f"\t\ticon: {{ id: \"{stage['milestone']}\" }}\n"
                    f"\t\tshape: \"{shape}\"\n"
                    f"\t\tsize: {size}\n"
                    f"\t\ttasks: {task_block(task_namespace, milestone)}\n"
                    f"\t\tx: {x:.1f}d\n"
                    f"\t\ty: {y:.1f}d\n"
                    "\t}"
                )
                title_en, desc_en, title_ru, desc_ru = descriptions(stage, substage, lesson)
                localization["en_us"][f"quest.{quest_id}.title"] = json.dumps(title_en, ensure_ascii=False)
                localization["en_us"][f"quest.{quest_id}.quest_desc"] = format_array(desc_en)
                localization["ru_ru"][f"quest.{quest_id}.title"] = json.dumps(title_ru, ensure_ascii=False)
                localization["ru_ru"][f"quest.{quest_id}.quest_desc"] = format_array(desc_ru)
                previous_id = quest_id

    chapter = (
        "{\n"
        "\tdefault_hide_dependency_lines: false\n"
        "\tdefault_quest_shape: \"hexagon\"\n"
        f"\tfilename: \"{FILENAME}\"\n"
        "\tgroup: \"177A10C99EDDA376\"\n"
        "\ticon: { id: \"kubejs:creative_convergence_matrix\" }\n"
        f"\tid: \"{CHAPTER_ID}\"\n"
        "\torder_index: 1\n"
        "\tquest_links: []\n"
        "\tquests: [\n"
        + "\n".join(quest_blocks)
        + "\n\t]\n}\n"
    )
    previous = CHAPTER_PATH.read_text(encoding="utf-8") if CHAPTER_PATH.exists() else ""
    changed = previous != chapter
    if changed:
        CHAPTER_PATH.write_text(chapter, encoding="utf-8", newline="\n")

    for locale, entries in localization.items():
        path = LANG_DIR / f"{locale}.snbt"
        text = path.read_text(encoding="utf-8")
        original = text
        for key, value in entries.items():
            text = upsert_localization(text, key, value)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            changed = True

    print(f"progression_spine_quests: {total}")
    print(f"progression_spine_stages: {len(contract['stages'])}")
    print(f"progression_spine_substages: {sum(len(stage['substages']) for stage in contract['stages'])}")
    print("progression_spine_updated" if changed else "progression_spine_unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
