from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "other_storage_systems.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"

FOCUS_ITEMS = (
    "sophisticatedbackpacks:backpack",
    "sophisticatedbackpacks:netherite_backpack",
    "sophisticatedbackpacks:pickup_upgrade",
    "sophisticatedbackpacks:filter_upgrade",
    "sophisticatedbackpacks:compacting_upgrade",
    "sophisticatedbackpacks:void_upgrade",
    "sophisticatedstorage:barrel",
    "sophisticatedstorage:diamond_barrel",
    "sophisticatedstorage:pickup_upgrade",
    "sophisticatedstorage:filter_upgrade",
    "sophisticatedstorage:compacting_upgrade",
    "sophisticatedstorage:advanced_void_upgrade",
)

CONTENT: dict[str, dict[str, tuple[str, list[str]]]] = {
    "en_us": {
        "sophisticatedbackpacks:backpack": (
            "Backpack — Portable Buffer Contract",
            [
                "A backpack reduces travel and sorting interruptions, but it must not become an unplanned warehouse containing the only copy of tools, quest evidence and progression components.",
                "Acceptance: reserve recovery slots, separate protected items from routine loot, define a filtered unload point and complete one expedition without manually sorting the entire inventory."
            ],
        ),
        "sophisticatedbackpacks:netherite_backpack": (
            "Netherite Backpack — Concentrated Risk Review",
            [
                "Maximum portable capacity concentrates several production batches and valuable equipment into one object, so loss planning matters more than nominal slot count.",
                "Acceptance: keep replacement transport and tools at base, record irreplaceable contents, test death recovery and prove that losing the backpack cannot erase the only progression path."
            ],
        ),
        "sophisticatedbackpacks:pickup_upgrade": (
            "Pickup Upgrade — Controlled Collection",
            [
                "Automatic pickup is a routing rule. Without a narrow policy it fills storage with debris, competes with machine collectors and captures items intended for another player or process.",
                "Acceptance: use an allowlist, test overflow, disable competing magnets and verify that protected, component-bearing and stage-gated items are rejected safely."
            ],
        ),
        "sophisticatedbackpacks:filter_upgrade": (
            "Backpack Filter — Exact Matching Policy",
            [
                "Tag and item filters can include modded variants, filled containers or equipment states that should follow different routes even when their base identity appears similar.",
                "Acceptance: document allow/deny behavior, test unknown items and component-sensitive stacks, and maintain a visible quarantine for anything that does not match an approved category."
            ],
        ),
        "sophisticatedbackpacks:compacting_upgrade": (
            "Backpack Compacting — Reversible Conversions Only",
            [
                "Automatic compacting may select irreversible or cross-mod recipes, consume working stock needed by machines or create a reverse-conversion loop with another storage system.",
                "Acceptance: allow only reviewed reversible conversions, preserve production minimums and verify exact item counts before and after a full compact/decompact cycle."
            ],
        ),
        "sophisticatedbackpacks:void_upgrade": (
            "Backpack Void Upgrade — Destructive Boundary",
            [
                "A void upgrade is safe only for explicitly overproduced low-value items. Broad filters can silently destroy rare drops, reusable containers and quest evidence.",
                "Acceptance: place visible overflow before deletion, use a strict allowlist, retain a diagnostic sample and prove that unknown or protected items can never reach the destructive stage."
            ],
        ),
        "sophisticatedstorage:barrel": (
            "Barrel — Bulk Storage Role",
            [
                "A barrel should have one documented role such as bulk raw material, machine input buffer or finished-product reserve rather than becoming an unlabeled catch-all.",
                "Acceptance: define minimum and maximum stock, label the destination, stop producers near capacity and demonstrate safe behavior when insertion continues into a full container."
            ],
        ),
        "sophisticatedstorage:diamond_barrel": (
            "Diamond Barrel — High-Capacity Migration",
            [
                "A higher tier concentrates more production value in one block and increases the impact of configuration errors, explosions or unsafe movement of loaded storage.",
                "Acceptance: stop inputs, snapshot counts and filters, migrate under controlled conditions, verify totals and maintain a separate reserve for irreplaceable strategic materials."
            ],
        ),
        "sophisticatedstorage:pickup_upgrade": (
            "Storage Pickup Upgrade — Area Ownership",
            [
                "Stationary collection must not compete with player magnets, nearby machines or another team area, because ownership conflicts produce unpredictable routing and apparent losses.",
                "Acceptance: establish one collector per area, test range and multiplayer ownership, provide overflow and prove that items intended for calibrated machine inputs remain untouched."
            ],
        ),
        "sophisticatedstorage:filter_upgrade": (
            "Storage Filter — Exclusive Destinations",
            [
                "When several containers accept the same item, routing depends on hidden priority and available capacity. Overlapping filters make storage behavior difficult to diagnose.",
                "Acceptance: use mutually exclusive rules, define destination priority, test marked samples and route unmatched items to a finite visible quarantine instead of a generic fallback."
            ],
        ),
        "sophisticatedstorage:compacting_upgrade": (
            "Storage Compacting — Conversion Ownership",
            [
                "Warehouse compacting can compete with machine recipes or another decompacting system, creating loops that waste energy and hide the real stock available to production.",
                "Acceptance: assign one owner to each conversion, disable reverse paths elsewhere, preserve emergency stock and audit item and energy totals across a complete cycle."
            ],
        ),
        "sophisticatedstorage:advanced_void_upgrade": (
            "Advanced Void Upgrade — Fail-Closed Overflow",
            [
                "High-throughput deletion can erase thousands of items before a filter mistake is noticed, so its default and restart states must be demonstrably safe.",
                "Acceptance: require an allowlisted excess item, alarm on unexpected volume, make deletion independently switchable and verify fail-closed behavior after chunk reload and full restart."
            ],
        ),
    },
    "ru_ru": {
        "sophisticatedbackpacks:backpack": (
            "Рюкзак — контракт переносного буфера",
            [
                "Рюкзак уменьшает число поездок и ручной сортировки, но не должен становиться случайным складом с единственным экземпляром инструментов, доказательств и этапных компонентов.",
                "Приёмка: зарезервируйте восстановление, отделите защищённое от обычного лута, создайте фильтрованную разгрузку и завершите поход без сортировки всего инвентаря вручную."
            ],
        ),
        "sophisticatedbackpacks:netherite_backpack": (
            "Незеритовый рюкзак — проверка концентрированного риска",
            [
                "Максимальная переносная ёмкость концентрирует несколько партий и ценное снаряжение в одном предмете, поэтому план потери важнее номинального числа слотов.",
                "Приёмка: храните замену транспорта и инструментов на базе, отмечайте невосполнимое, проверьте возврат после смерти и исключите потерю единственного пути прогрессии."
            ],
        ),
        "sophisticatedbackpacks:pickup_upgrade": (
            "Улучшение подбора — управляемый сбор",
            [
                "Автоподбор является правилом маршрутизации. Без узкой политики он заполняет мусором, конфликтует со сборщиками машин и забирает предметы другого игрока или процесса.",
                "Приёмка: используйте белый список, проверьте переполнение, отключите конкурирующие магниты и безопасно отклоняйте защищённые, компонентные и этапные предметы."
            ],
        ),
        "sophisticatedbackpacks:filter_upgrade": (
            "Фильтр рюкзака — политика точного совпадения",
            [
                "Фильтры по тегам и предметам могут включать модовые варианты, заполненные контейнеры или состояния снаряжения, которым требуются разные маршруты.",
                "Приёмка: зафиксируйте белый или чёрный список, проверьте неизвестные и компонентные предметы и направляйте всё нераспознанное в видимый карантин."
            ],
        ),
        "sophisticatedbackpacks:compacting_upgrade": (
            "Сжатие в рюкзаке — только обратимые преобразования",
            [
                "Автосжатие может выбрать необратимый или межмодовый рецепт, забрать рабочий запас машин или создать цикл с другим разборщиком хранения.",
                "Приёмка: разрешите только проверенные обратимые преобразования, сохраните производственный минимум и сверяйте количество до и после полного цикла."
            ],
        ),
        "sophisticatedbackpacks:void_upgrade": (
            "Удаляющее улучшение рюкзака — разрушительная граница",
            [
                "Удаление безопасно только для явно избыточных дешёвых предметов. Широкий фильтр незаметно уничтожит редкий лут, многоразовую тару и доказательства квестов.",
                "Приёмка: поставьте видимое переполнение перед удалением, используйте строгий белый список, сохраняйте образец и не допускайте неизвестное или защищённое."
            ],
        ),
        "sophisticatedstorage:barrel": (
            "Бочка — роль массового хранения",
            [
                "Бочка должна иметь одну документированную роль: массовое сырьё, входной буфер машины или резерв готового продукта, а не быть неподписанным общим контейнером.",
                "Приёмка: задайте минимум и максимум, подпишите назначение, останавливайте производство возле ёмкости и проверьте продолжение ввода в полный контейнер."
            ],
        ),
        "sophisticatedstorage:diamond_barrel": (
            "Алмазная бочка — перенос большой ёмкости",
            [
                "Высокий уровень концентрирует больше стоимости в одном блоке и усиливает последствия ошибки настройки, взрыва или небезопасного перемещения заполненного склада.",
                "Приёмка: остановите входы, снимите количество и фильтры, выполните контролируемый перенос, сверяйте итог и держите отдельный резерв стратегических материалов."
            ],
        ),
        "sophisticatedstorage:pickup_upgrade": (
            "Складской подбор — владение областью",
            [
                "Стационарный сбор не должен конфликтовать с магнитами игрока, соседними машинами или другой командной зоной, иначе маршрут и причины потерь непредсказуемы.",
                "Приёмка: оставьте один сборщик на область, проверьте радиус и владельца, добавьте переполнение и не забирайте предметы точных входов машин."
            ],
        ),
        "sophisticatedstorage:filter_upgrade": (
            "Складской фильтр — взаимоисключающие назначения",
            [
                "Если несколько контейнеров принимают один предмет, маршрут зависит от скрытого приоритета и свободной ёмкости. Пересекающиеся фильтры затрудняют диагностику.",
                "Приёмка: используйте взаимоисключающие правила, задайте приоритет, проверяйте отмеченные образцы и отправляйте неизвестное в конечный видимый карантин."
            ],
        ),
        "sophisticatedstorage:compacting_upgrade": (
            "Складское сжатие — владелец преобразования",
            [
                "Сжатие на складе может конкурировать с рецептами машин или другим разборщиком, создавая цикл, который расходует энергию и скрывает настоящий запас.",
                "Приёмка: назначьте одного владельца преобразования, отключите обратные пути, сохраните аварийный запас и проверьте предметы и энергию за полный цикл."
            ],
        ),
        "sophisticatedstorage:advanced_void_upgrade": (
            "Улучшенное удаление — безопасное закрытие при отказе",
            [
                "Высокоскоростное удаление способно уничтожить тысячи предметов до обнаружения ошибки фильтра, поэтому его состояние после отказа и запуска должно быть безопасным.",
                "Приёмка: удаляйте только разрешённый избыток, сигнализируйте неожиданный объём, добавьте отдельный выключатель и проверьте закрытие после загрузки чанка и перезапуска."
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
    quests_marker = text.find("quests:")
    item_index = text.find(f'id: "{item_id}"', quests_marker)
    if item_index < 0:
        raise RuntimeError(f"Storage focus item not found in chapter: {item_id}")
    object_start = text.rfind("\n\t\t{", 0, item_index)
    if object_start < 0:
        raise RuntimeError(f"Storage quest object start not found for {item_id}")
    object_start += 1
    object_end = matching_delimiter(text, object_start, "{", "}")
    block = text[object_start : object_end + 1]
    quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not quest_match:
        raise RuntimeError(f"Storage quest ID not found for {item_id}")
    return quest_match.group(1), object_start, object_end


def acceptance_id(quest_id: str) -> str:
    return hashlib.sha256(f"storage_acceptance:{quest_id}".encode()).hexdigest()[:16].upper()


def add_checkmark(text: str, item_id: str) -> tuple[str, bool, str]:
    quest_id, object_start, object_end = quest_for_item(text, item_id)
    task_id = acceptance_id(quest_id)
    if f'id: "{task_id}"' in text:
        return text, False, quest_id
    block = text[object_start : object_end + 1]
    tasks_marker = block.find("tasks:")
    if tasks_marker < 0:
        raise RuntimeError(f"Storage quest has no task list: {quest_id}")
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

    print(f"Storage acceptance tasks added: {changed_tasks}")
    print("Storage localization changed" if changed_localization else "Storage localization unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
