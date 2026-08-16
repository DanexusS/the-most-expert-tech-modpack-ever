from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "applied_energistics_2.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"

FOCUS_ITEMS = (
    "ae2:charger",
    "ae2:inscriber",
    "ae2:energy_acceptor",
    "ae2:drive",
    "ae2:controller",
    "ae2:molecular_assembler",
    "ae2:storage_bus",
    "ae2:import_bus",
    "ae2:export_bus",
    "ae2:quantum_ring",
)

CONTENT: dict[str, dict[str, tuple[str, list[str]]]] = {
    "en_us": {
        "ae2:charger": (
            "Charger — Controlled Certus Intake",
            [
                "The Charger is the first powered AE2 process and establishes how external energy enters a dedicated digital-workshop line.",
                "Acceptance: provide buffered power, automate input and output without mixing charged and uncharged crystals, and stop intake when the destination is full."
            ],
        ),
        "ae2:inscriber": (
            "Inscriber — Processor Production Cell",
            [
                "Processors are recurring infrastructure components; one shared unfiltered Inscriber becomes a permanent bottleneck and can trap the wrong press.",
                "Acceptance: isolate press recipes, automate silicon and printed circuits, return reusable presses, and complete sixteen mixed processors without inventory correction."
            ],
        ),
        "ae2:energy_acceptor": (
            "Energy Acceptor — Network Power Boundary",
            [
                "The Energy Acceptor separates external FE infrastructure from the AE network and makes power loss diagnosable instead of invisible.",
                "Acceptance: add an external buffer, label the feed, verify the network survives one normal crafting job after generation stops, and prevent unrelated consumers from draining the reserve."
            ],
        ),
        "ae2:drive": (
            "ME Drive — Storage Policy",
            [
                "A Drive is useful only with a policy for cell sizes, item types, partitioning and overflow; random cells hide capacity problems until production stops.",
                "Acceptance: separate bulk and rare items, reserve one expansion slot, expose remaining bytes and types, and route overflow without deleting or endlessly recirculating items."
            ],
        ),
        "ae2:controller": (
            "ME Controller — Channel Architecture",
            [
                "The Controller unlocks dense channel distribution, but a larger network is not automatically a better designed network.",
                "Acceptance: document channel use per face, keep a maintenance path, isolate at least one subnet, and demonstrate that one disconnected cable cannot disable storage and autocrafting together."
            ],
        ),
        "ae2:molecular_assembler": (
            "Molecular Assembler — Safe Autocrafting",
            [
                "Assemblers convert patterns into production and can deadlock when ingredients, outputs or reusable tools share uncontrolled paths.",
                "Acceptance: complete eight crafts from request to storage, prevent circular patterns, return container items, and expose a visible stalled-craft diagnostic path."
            ],
        ),
        "ae2:storage_bus": (
            "Storage Bus — External Inventory Contract",
            [
                "A Storage Bus can expose drawers, vaults and machines as network storage, but priorities and recursive access must be planned explicitly.",
                "Acceptance: assign priorities, prevent the same inventory from being exposed twice, reserve space for machine output, and verify extraction uses the intended source first."
            ],
        ),
        "ae2:import_bus": (
            "Import Bus — Bounded Extraction",
            [
                "Import Buses move items into the network and can silently consume every output slot or saturate storage when filtering is omitted.",
                "Acceptance: filter the source, limit acceleration to actual demand, preserve machine maintenance slots, and stop cleanly when the target storage policy rejects an item."
            ],
        ),
        "ae2:export_bus": (
            "Export Bus — Controlled Stocking",
            [
                "Export Buses should maintain a defined stock or machine input, not create uncontrolled loops through interfaces and external inventories.",
                "Acceptance: set exact filters, cap stock with level control where appropriate, prevent re-import of the same item, and verify missing materials produce a visible shortage instead of a silent loop."
            ],
        ),
        "ae2:quantum_ring": (
            "Quantum Ring — Cross-Dimensional Reliability",
            [
                "Quantum links are late infrastructure because they combine large energy demand, paired singularities and failure across dimensions or unloaded areas.",
                "Acceptance: label both endpoints, provide independent power reserve, test shutdown and reconnection, and ensure loss of the link cannot strand the only copy of critical recovery equipment."
            ],
        ),
    },
    "ru_ru": {
        "ae2:charger": (
            "Зарядник — управляемый поток церта",
            [
                "Зарядник является первым энергозависимым процессом AE2 и задаёт способ подключения отдельной цифровой мастерской к внешней сети.",
                "Приёмка: питание имеет буфер, вход и выход автоматизированы без смешивания заряженных и обычных кристаллов, подача останавливается при заполнении назначения."
            ],
        ),
        "ae2:inscriber": (
            "Высекатель — ячейка производства процессоров",
            [
                "Процессоры постоянно расходуются на инфраструктуру; один общий высекатель без фильтров становится постоянным узким местом и удерживает неверный пресс.",
                "Приёмка: рецепты прессов изолированы, кремний и печатные схемы автоматизированы, многоразовые прессы возвращаются, шестнадцать смешанных процессоров создаются без коррекции инвентаря."
            ],
        ),
        "ae2:energy_acceptor": (
            "Приёмщик энергии — граница питания сети",
            [
                "Приёмщик отделяет внешнюю FE-инфраструктуру от сети AE и позволяет диагностировать потерю питания вместо скрытого отключения устройств.",
                "Приёмка: установлен внешний буфер, линия подписана, сеть завершает один обычный автокрафт после остановки генерации, посторонние потребители не расходуют резерв."
            ],
        ),
        "ae2:drive": (
            "МЭ-накопитель — политика хранения",
            [
                "Накопитель полезен только при политике размеров ячеек, типов, разметки и переполнения; случайный набор ячеек скрывает проблему до остановки производства.",
                "Приёмка: массовые и редкие предметы разделены, оставлен слот расширения, видны байты и типы, переполнение обрабатывается без удаления и бесконечной циркуляции."
            ],
        ),
        "ae2:controller": (
            "МЭ-контроллер — архитектура каналов",
            [
                "Контроллер открывает плотное распределение каналов, но большой размер сети сам по себе не означает правильную архитектуру.",
                "Приёмка: каналы по граням документированы, сохранён доступ для обслуживания, выделена хотя бы одна подсеть, отключение одного кабеля не лишает одновременно хранения и автокрафта."
            ],
        ),
        "ae2:molecular_assembler": (
            "Молекулярный сборщик — безопасный автокрафт",
            [
                "Сборщики превращают шаблоны в производство и могут зависнуть, когда входы, выходы и многоразовые инструменты используют неконтролируемые маршруты.",
                "Приёмка: восемь заказов проходят от запроса до хранения, циклические шаблоны исключены, контейнеры возвращаются, зависший крафт имеет видимый путь диагностики."
            ],
        ),
        "ae2:storage_bus": (
            "Шина хранения — контракт внешнего инвентаря",
            [
                "Шина открывает ящики, хранилища и машины для сети, но приоритеты и рекурсивный доступ должны проектироваться явно.",
                "Приёмка: приоритеты назначены, один инвентарь не подключён дважды, оставлено место для выхода машин, извлечение сначала использует запланированный источник."
            ],
        ),
        "ae2:import_bus": (
            "Шина импорта — ограниченное извлечение",
            [
                "Шины импорта переносят предметы в сеть и без фильтров незаметно опустошают служебные слоты либо заполняют всё хранилище.",
                "Приёмка: источник фильтруется, ускорение соответствует спросу, служебные слоты машин сохранены, линия чисто останавливается, если политика хранения отклоняет предмет."
            ],
        ),
        "ae2:export_bus": (
            "Шина экспорта — контролируемое снабжение",
            [
                "Шина экспорта должна поддерживать заданный запас или вход машины, а не создавать цикл через интерфейсы и внешние инвентари.",
                "Приёмка: фильтры точны, запас при необходимости ограничен уровнем, повторный импорт того же предмета исключён, нехватка материала отображается как понятный дефицит."
            ],
        ),
        "ae2:quantum_ring": (
            "Квантовое кольцо — надёжность между измерениями",
            [
                "Квантовая связь является поздней инфраструктурой из-за высокого энергопотребления, связанных сингулярностей и отказов между измерениями или незагруженными областями.",
                "Приёмка: обе стороны подписаны, имеют независимый резерв, проверены отключение и восстановление, потеря связи не оставляет единственное аварийное оборудование на другой стороне."
            ],
        ),
    },
}


def matching_delimiter(text: str, start: int, opening: str, closing: str) -> int:
    depth = 0
    in_string = False
    escaped = False
    quote = ""
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                in_string = False
            continue
        if char in "'\"":
            in_string = True
            quote = char
        elif char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return index
    raise RuntimeError(f"Unclosed delimiter {opening!r} at offset {start}")


def quest_for_item(text: str, item_id: str) -> tuple[str, int, int]:
    item_index = text.find(f'id: "{item_id}"')
    if item_index < 0:
        raise RuntimeError(f"AE2 focus item not found in chapter: {item_id}")
    object_start = text.rfind("\n\t\t{", 0, item_index)
    if object_start < 0:
        raise RuntimeError(f"AE2 quest object start not found for {item_id}")
    object_start += 1
    object_end = matching_delimiter(text, object_start, "{", "}")
    block = text[object_start : object_end + 1]
    quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not quest_match:
        raise RuntimeError(f"AE2 quest ID not found for {item_id}")
    return quest_match.group(1), object_start, object_end


def acceptance_id(quest_id: str) -> str:
    return hashlib.sha256(f"ae2_acceptance:{quest_id}".encode()).hexdigest()[:16].upper()


def add_checkmark(text: str, item_id: str) -> tuple[str, bool, str]:
    quest_id, object_start, object_end = quest_for_item(text, item_id)
    task_id = acceptance_id(quest_id)
    if f'id: "{task_id}"' in text:
        return text, False, quest_id
    block = text[object_start : object_end + 1]
    tasks_marker = block.find("tasks:")
    if tasks_marker < 0:
        raise RuntimeError(f"AE2 quest has no task list: {quest_id}")
    list_start = block.find("[", tasks_marker)
    list_end = matching_delimiter(block, list_start, "[", "]")
    insertion = (
        "\n\t\t\t{\n"
        f"\t\t\t\tid: \"{task_id}\"\n"
        "\t\t\t\ttype: \"checkmark\"\n"
        "\t\t\t}\n\t\t\t"
    )
    global_list_end = object_start + list_end
    return text[:global_list_end] + insertion + text[global_list_end:], True, quest_id


def render(value: str | list[str]) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def upsert(text: str, key: str, value: str | list[str]) -> tuple[str, bool]:
    rendered = f"\t{key}: {render(value)}\n"
    pattern = re.compile(rf"(?ms)^\t{re.escape(key)}:.*?(?=^\t[A-Za-z0-9_.-]+:|^\}}\s*$)")
    updated, count = pattern.subn(rendered, text, count=1)
    if count:
        return updated, updated != text
    closing = text.rfind("}")
    if closing < 0 or text[closing + 1 :].strip():
        raise RuntimeError("Localization file has an unexpected ending")
    return text[:closing].rstrip() + "\n" + rendered + "}\n", True


def main() -> int:
    chapter = CHAPTER_PATH.read_text(encoding="utf-8")
    changed_tasks = 0
    quest_ids: dict[str, str] = {}
    for item_id in FOCUS_ITEMS:
        chapter, added, quest_id = add_checkmark(chapter, item_id)
        changed_tasks += int(added)
        quest_ids[item_id] = quest_id
        print(f"{item_id} -> {quest_id}")
    if changed_tasks:
        CHAPTER_PATH.write_text(chapter, encoding="utf-8", newline="\n")

    changed_localization = False
    for locale, content in CONTENT.items():
        path = LANG_DIR / f"{locale}.snbt"
        text = path.read_text(encoding="utf-8")
        changed = False
        for item_id, (title, description) in content.items():
            quest_id = quest_ids[item_id]
            text, title_changed = upsert(text, f"quest.{quest_id}.title", title)
            text, desc_changed = upsert(text, f"quest.{quest_id}.quest_desc", description)
            changed = changed or title_changed or desc_changed
        if changed:
            path.write_text(text, encoding="utf-8", newline="\n")
        changed_localization = changed_localization or changed
        print(f"{locale}: {'updated' if changed else 'unchanged'}")

    print(f"AE2 core acceptance tasks added: {changed_tasks}")
    print("AE2 core localization changed" if changed_localization else "AE2 core localization unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
