from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "powah.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"

TIERS = ("starter", "basic", "hardened", "blazing", "niotic", "spirited", "nitro")
TIER_RU = {
    "starter": "стартовый",
    "basic": "базовый",
    "hardened": "укреплённый",
    "blazing": "пылающий",
    "niotic": "ниотический",
    "spirited": "духовный",
    "nitro": "нитро",
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
    raise RuntimeError(f"Unclosed delimiter {opening!r} at {start}")


def extract_array(block: str, marker: str) -> tuple[int, int, str]:
    marker_index = block.find(marker)
    if marker_index < 0:
        raise RuntimeError(f"Missing {marker}")
    start = block.find("[", marker_index)
    if start < 0:
        raise RuntimeError(f"Missing list after {marker}")
    end = matching_delimiter(block, start, "[", "]")
    return start, end, block[start + 1 : end]


def quest_spans(text: str) -> list[tuple[int, int]]:
    marker = text.find("quests:")
    if marker < 0:
        raise RuntimeError("Powah chapter has no quests list")
    list_start = text.find("[", marker)
    list_end = matching_delimiter(text, list_start, "[", "]")
    spans: list[tuple[int, int]] = []
    index = list_start + 1
    while index < list_end:
        start = text.find("{", index, list_end)
        if start < 0:
            break
        end = matching_delimiter(text, start, "{", "}")
        spans.append((start, end + 1))
        index = end + 1
    return spans


def remove_rewards(block: str) -> tuple[str, bool]:
    match = re.search(r"(?m)^\s*rewards:\s*", block)
    if not match:
        return block, False
    value_start = match.end()
    while value_start < len(block) and block[value_start].isspace():
        value_start += 1
    if value_start >= len(block) or block[value_start] not in "[{":
        raise RuntimeError("Unexpected Powah rewards value")
    opening = block[value_start]
    closing = "]" if opening == "[" else "}"
    value_end = matching_delimiter(block, value_start, opening, closing) + 1
    line_start = block.rfind("\n", 0, match.start()) + 1
    line_end = block.find("\n", value_end)
    if line_end < 0:
        line_end = value_end
    else:
        line_end += 1
    return block[:line_start] + block[line_end:], True


def acceptance_id(quest_id: str) -> str:
    return hashlib.sha256(f"powah_acceptance:{quest_id}".encode()).hexdigest()[:16].upper()


def add_acceptance_task(block: str, quest_id: str) -> tuple[str, bool]:
    task_id = acceptance_id(quest_id)
    if f'id: "{task_id}"' in block:
        return block, False
    _, list_end, _ = extract_array(block, "tasks:")
    insertion = (
        "\n\t\t\t{\n"
        f"\t\t\t\tid: \"{task_id}\"\n"
        "\t\t\t\ttype: \"checkmark\"\n"
        "\t\t\t}\n\t\t\t"
    )
    return block[:list_end] + insertion + block[list_end:], True


def quest_identity(block: str) -> tuple[str, list[str]]:
    quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not quest_match:
        raise RuntimeError("Powah quest without a valid ID")
    _, _, tasks_body = extract_array(block, "tasks:")
    items = list(dict.fromkeys(re.findall(r'id:\s*"(powah:[a-z0-9_./-]+)"', tasks_body)))
    if not items:
        raise RuntimeError(f"Powah quest {quest_match.group(1)} has no Powah item task")
    return quest_match.group(1), items


def human_name(item_id: str) -> str:
    return item_id.split(":", 1)[1].replace("_", " ").title()


def tier(path: str) -> tuple[str, str]:
    for value in reversed(TIERS):
        if path == value or path.endswith("_" + value) or ("_" + value + "_") in path:
            return value.title(), TIER_RU[value]
    return "Untiered", "внеуровневый"


def category(path: str) -> tuple[str, str, str, str]:
    tier_en, tier_ru = tier(path)
    categories = [
        (("dielectric",), "dielectric component", "диэлектрический компонент", "material preparation and component stocking", "подготовку материала и запас компонентов"),
        (("capacitor",), "tier capacitor", "уровневый конденсатор", "component tier integrity and energizing inputs", "целостность уровня компонентов и входы энергизации"),
        (("energizing_orb",), "energizing process controller", "контроллер процесса энергизации", "recipe isolation, input buffering and controlled energy delivery", "изоляцию рецепта, буферы входов и управляемую подачу энергии"),
        (("energizing_rod",), "energizing power source", "источник мощности энергизации", "rod count, transfer rate and orb starvation", "число стержней, скорость передачи и нехватку питания сферы"),
        (("reactor",), "multi-input generator", "многокомпонентный генератор", "fuel, coolant, carbon, redstone and output balance", "баланс топлива, охлаждения, углерода, редстоуна и выхода"),
        (("thermo_generator",), "temperature-gradient generator", "термогенератор", "hot-block quality, coolant supply and sustained gradient", "качество горячего блока, подачу охлаждения и устойчивый перепад"),
        (("solar_panel",), "daylight generator", "солнечный генератор", "day-night duty cycle, sky access and storage reserve", "суточный цикл, доступ к небу и резерв хранения"),
        (("magmator",), "fluid-fuel generator", "жидкостный генератор", "lava logistics, tank reserve and safe backpressure", "логистику лавы, резерв ёмкости и безопасное переполнение"),
        (("furnator",), "solid-fuel generator", "твердотопливный генератор", "fuel quality, feed rate and clean shutdown", "качество топлива, скорость подачи и чистую остановку"),
        (("energy_cell",), "stationary energy buffer", "стационарный энергобуфер", "usable capacity, charge rate and emergency reserve", "полезную ёмкость, скорость заряда и аварийный резерв"),
        (("battery",), "portable energy buffer", "переносной энергобуфер", "portable capacity, charging path and tool demand", "переносную ёмкость, путь зарядки и спрос инструментов"),
        (("cable",), "energy distribution cable", "кабель распределения энергии", "throughput, connection topology and bottleneck isolation", "пропускную способность, топологию и изоляцию узких мест"),
        (("ender_gate",), "wireless network endpoint", "беспроводной сетевой узел", "channel ownership, cross-base routing and failure containment", "владение каналом, маршрутизацию между базами и локализацию отказа"),
        (("player_transmitter",), "wireless player charger", "беспроводной зарядник игрока", "range, priority and protection of the main factory reserve", "радиус, приоритет и защиту основного резерва фабрики"),
        (("crystal", "steel_energized", "uraninite"), "energized tier material", "энергизированный уровневый материал", "declared energizing recipe, batch cost and renewable input policy", "заявленный рецепт энергизации, стоимость партии и возобновляемость входов"),
        (("binding_card", "blank_card"), "network configuration item", "предмет настройки сети", "ownership, naming and prevention of accidental cross-network access", "владение, именование и защиту от случайного доступа к другой сети"),
        (("book", "wrench"), "configuration tool", "инструмент настройки", "safe configuration, recovery and documentation of changed state", "безопасную настройку, восстановление и документирование изменений"),
    ]
    for tokens, en_role, ru_role, en_focus, ru_focus in categories:
        if any(token in path for token in tokens):
            return f"{tier_en} {en_role}", f"{tier_ru} {ru_role}", en_focus, ru_focus
    return f"{tier_en} Powah component", f"{tier_ru} компонент Powah", "its actual role, throughput and integration limits", "его фактическую роль, пропускную способность и ограничения интеграции"


def localized_content(items: list[str]) -> dict[str, tuple[str, list[str]]]:
    primary = items[0]
    path = primary.split(":", 1)[1]
    if len(items) > 1:
        display_en = " / ".join(human_name(item) for item in items)
        display_ru = display_en
        role_en = "linked component set"
        role_ru = "связанный набор компонентов"
        focus_en = "batch ratios, shared ingredients and continuous component stocking"
        focus_ru = "соотношения партии, общие ингредиенты и непрерывный запас компонентов"
    else:
        display_en = human_name(primary)
        display_ru = display_en
        role_en, role_ru, focus_en, focus_ru = category(path)

    en_desc = [
        f"{display_en} is a {role_en} in the Powah energy chain. Its tier is meaningful only when the upstream energizing materials and the downstream machine or network can operate at the same sustained rate.",
        f"Acceptance: verify {focus_en}; run a representative load without manual inventory correction, record input/output rate and reserve, and prove that quest rewards, EMC, trades or alternate recipes cannot unlock this tier early."
    ]
    ru_desc = [
        f"{display_ru} — {role_ru} в энергетической цепочке Powah. Уровень имеет смысл только тогда, когда предыдущие материалы энергизации и следующая машина или сеть работают с одинаковой устойчивой скоростью.",
        f"Приёмка: проверьте {focus_ru}; выполните типовую нагрузку без ручной перестановки, запишите вход, выход и резерв и исключите раннее открытие уровня наградами, EMC, торговлей или альтернативным рецептом."
    ]
    return {
        "en_us": (f"{display_en} — Tier and System Acceptance", en_desc),
        "ru_ru": (f"{display_ru} — приёмка уровня и системы", ru_desc),
    }


def render(value: str | list[str]) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def upsert(text: str, key: str, value: str | list[str]) -> str:
    rendered = f"\t{key}: {render(value)}\n"
    pattern = re.compile(rf"(?ms)^\t{re.escape(key)}:.*?(?=^\t[A-Za-z0-9_.-]+:|^\}}\s*$)")
    updated, count = pattern.subn(rendered, text, count=1)
    if count:
        return updated
    closing = text.rfind("}")
    if closing < 0:
        raise RuntimeError("Localization file has no closing brace")
    return text[:closing].rstrip() + "\n" + rendered + "}\n"


def main() -> int:
    text = CHAPTER_PATH.read_text(encoding="utf-8")
    spans = quest_spans(text)
    replacements: list[tuple[int, int, str]] = []
    localization: dict[str, dict[str, str | list[str]]] = {"en_us": {}, "ru_ru": {}}
    reward_removals = 0
    task_additions = 0

    for start, end in spans:
        block = text[start:end]
        quest_id, items = quest_identity(block)
        block, removed = remove_rewards(block)
        reward_removals += int(removed)
        block, added = add_acceptance_task(block, quest_id)
        task_additions += int(added)
        replacements.append((start, end, block))

        content = localized_content(items)
        for locale, (title, desc) in content.items():
            localization[locale][f"quest.{quest_id}.title"] = title
            localization[locale][f"quest.{quest_id}.quest_desc"] = desc

    for start, end, block in reversed(replacements):
        text = text[:start] + block + text[end:]
    CHAPTER_PATH.write_text(text, encoding="utf-8", newline="\n")

    for locale, entries in localization.items():
        path = LANG_DIR / f"{locale}.snbt"
        language = path.read_text(encoding="utf-8")
        for key, value in entries.items():
            language = upsert(language, key, value)
        language = upsert(
            language,
            "chapter.6EADD70261A9CB1A.title",
            "Powah — Tiered Energy Engineering" if locale == "en_us" else "Powah — уровневая энергетическая инженерия",
        )
        path.write_text(language, encoding="utf-8", newline="\n")

    print(f"powah_quests: {len(spans)}")
    print(f"reward_fields_removed: {reward_removals}")
    print(f"acceptance_tasks_added: {task_additions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
