from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "Modern Industrialization.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"

FOCUS_ITEMS = (
    "modern_industrialization:bronze_boiler",
    "modern_industrialization:bronze_macerator",
    "modern_industrialization:bronze_furnace",
    "modern_industrialization:bronze_compressor",
    "modern_industrialization:bronze_cutting_machine",
    "modern_industrialization:assembler",
    "modern_industrialization:advanced_large_steam_boiler",
)

CONTENT: dict[str, dict[str, tuple[str, list[str]]]] = {
    "en_us": {
        "modern_industrialization:bronze_boiler": (
            "Bronze Boiler — Stable Steam Contract",
            [
                "The first MI machines depend on steam quality, water supply and fuel delivery rather than on the boiler block alone.",
                "Acceptance: water cannot run dry, fuel input can be stopped, steam has a buffer, and the boiler supports three normal machine cycles without manual correction."
            ],
        ),
        "modern_industrialization:bronze_macerator": (
            "Bronze Macerator — Ore Intake Standard",
            [
                "Maceration establishes the first controlled ore-processing route and should not mix every ore into one unbounded output chest.",
                "Acceptance: input is filtered, products are separated or buffered, one stack can process unattended, and a full output stops intake without dropping items."
            ],
        ),
        "modern_industrialization:bronze_furnace": (
            "Bronze Furnace — Continuous Smelting",
            [
                "The furnace becomes useful when it consumes processed material at the same average rate that upstream machines provide it.",
                "Acceptance: complete three batches automatically, preserve fuel or steam reserve, and prevent either input starvation or full output from blocking unrelated machines."
            ],
        ),
        "modern_industrialization:bronze_compressor": (
            "Bronze Compressor — Plate Throughput",
            [
                "Plates are shared by many machine recipes; manual emergency compression creates hidden downtime across the entire factory.",
                "Acceptance: maintain a labelled plate buffer, process sixteen plates unattended, and record the slowest material so capacity can be expanded deliberately."
            ],
        ),
        "modern_industrialization:bronze_cutting_machine": (
            "Bronze Cutting Machine — Component Yield",
            [
                "Cutting converts bulk materials into rods, rings and other recurring parts whose lubricant or secondary inputs must be controlled.",
                "Acceptance: route required fluids safely, separate outputs, complete sixteen component operations, and stop cleanly when any destination is full."
            ],
        ),
        "modern_industrialization:assembler": (
            "Assembler — Recipe Isolation",
            [
                "The assembler is a strategic automation point: uncontrolled shared inputs can produce the wrong item or consume rare components.",
                "Acceptance: lock the intended recipe, dedicate or filter every input, return reusable tools or molds, and complete eight crafts without manual inventory rearrangement."
            ],
        ),
        "modern_industrialization:advanced_large_steam_boiler": (
            "Advanced Large Steam Boiler — Generation Redundancy",
            [
                "Large steam generation must be designed around startup demand, water security and safe shutdown rather than maximum nominal output.",
                "Acceptance: stored steam covers two production cycles after fuel stops, water has an independent reserve, and one generator outage does not strand every critical machine."
            ],
        ),
    },
    "ru_ru": {
        "modern_industrialization:bronze_boiler": (
            "Бронзовый котёл — стабильный контракт пара",
            [
                "Первые машины MI зависят от качества пара, подачи воды и топлива, а не только от наличия блока котла.",
                "Приёмка: вода не заканчивается, топливо можно отключить, пар имеет буфер, котёл обеспечивает три штатных цикла машин без ручной коррекции."
            ],
        ),
        "modern_industrialization:bronze_macerator": (
            "Бронзовый мацератор — стандарт приёма руды",
            [
                "Дробление создаёт первый управляемый маршрут руды и не должно смешивать все продукты в одном бесконечном сундуке.",
                "Приёмка: вход фильтруется, продукты разделены или буферизованы, стак обрабатывается без вмешательства, полный выход останавливает подачу без выброса предметов."
            ],
        ),
        "modern_industrialization:bronze_furnace": (
            "Бронзовая печь — непрерывная выплавка",
            [
                "Печь полезна, когда расходует обработанный материал с той же средней скоростью, с которой его поставляют предыдущие машины.",
                "Приёмка: три партии проходят автоматически, сохранён запас топлива или пара, нехватка входа и полный выход не блокируют посторонние машины."
            ],
        ),
        "modern_industrialization:bronze_compressor": (
            "Бронзовый компрессор — выпуск пластин",
            [
                "Пластины нужны во множестве машин, поэтому аварийное ручное прессование создаёт простой всей фабрики.",
                "Приёмка: поддерживается подписанный буфер пластин, шестнадцать штук обрабатываются без вмешательства, самый медленный материал отмечен для масштабирования."
            ],
        ),
        "modern_industrialization:bronze_cutting_machine": (
            "Бронзовый резак — выход компонентов",
            [
                "Резка превращает массовые материалы в стержни, кольца и другие детали, а смазка и дополнительные входы требуют контроля.",
                "Приёмка: жидкости подаются безопасно, выходы разделены, выполнено шестнадцать операций, линия чисто останавливается при заполнении любого назначения."
            ],
        ),
        "modern_industrialization:assembler": (
            "Сборщик — изоляция рецепта",
            [
                "Сборщик является стратегической точкой автоматизации: общие неконтролируемые входы производят неверный предмет и расходуют редкие детали.",
                "Приёмка: рецепт зафиксирован, каждый вход выделен или фильтруется, многоразовые инструменты возвращаются, восемь крафтов проходят без перестановки инвентаря."
            ],
        ),
        "modern_industrialization:advanced_large_steam_boiler": (
            "Улучшенный большой паровой котёл — резервирование генерации",
            [
                "Крупную паровую генерацию нужно проектировать по пиковому запуску, защите воды и безопасной остановке, а не только по номинальному выпуску.",
                "Приёмка: запас пара покрывает два цикла после остановки топлива, вода имеет независимый резерв, отказ одного генератора не оставляет критические машины без питания."
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
        raise RuntimeError(f"MI focus item not found in chapter: {item_id}")
    object_start = text.rfind("\n\t\t{", 0, item_index)
    if object_start < 0:
        raise RuntimeError(f"MI quest object start not found for {item_id}")
    object_start += 1
    object_end = matching_delimiter(text, object_start, "{", "}")
    block = text[object_start : object_end + 1]
    quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not quest_match:
        raise RuntimeError(f"MI quest ID not found for {item_id}")
    return quest_match.group(1), object_start, object_end


def acceptance_id(quest_id: str) -> str:
    return hashlib.sha256(f"mi_acceptance:{quest_id}".encode()).hexdigest()[:16].upper()


def add_checkmark(text: str, item_id: str) -> tuple[str, bool, str]:
    quest_id, object_start, object_end = quest_for_item(text, item_id)
    task_id = acceptance_id(quest_id)
    if f'id: "{task_id}"' in text:
        return text, False, quest_id
    block = text[object_start : object_end + 1]
    tasks_marker = block.find("tasks:")
    if tasks_marker < 0:
        raise RuntimeError(f"MI quest has no task list: {quest_id}")
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

    print(f"MI core acceptance tasks added: {changed_tasks}")
    print("MI core localization changed" if changed_localization else "MI core localization unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
