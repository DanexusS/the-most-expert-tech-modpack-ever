from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "simply_swords_2.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"


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


def quest_spans(text: str) -> list[tuple[int, int]]:
    marker = text.find("quests:")
    if marker < 0:
        raise RuntimeError("Simply Swords chapter has no quests list")
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


def extract_array(block: str, marker: str) -> tuple[int, int, str]:
    marker_index = block.find(marker)
    if marker_index < 0:
        raise RuntimeError(f"Missing {marker}")
    start = block.find("[", marker_index)
    end = matching_delimiter(block, start, "[", "]")
    return start, end, block[start + 1 : end]


def remove_rewards(block: str) -> tuple[str, bool]:
    match = re.search(r"(?m)^\s*rewards:\s*", block)
    if not match:
        return block, False
    value_start = match.end()
    while value_start < len(block) and block[value_start].isspace():
        value_start += 1
    if value_start >= len(block) or block[value_start] not in "[{":
        raise RuntimeError("Unexpected Simply Swords rewards value")
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
    return hashlib.sha256(f"simply_swords_acceptance:{quest_id}".encode()).hexdigest()[:16].upper()


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


def quest_identity(block: str) -> tuple[str, str]:
    quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not quest_match:
        raise RuntimeError("Simply Swords quest without a valid ID")
    _, _, tasks_body = extract_array(block, "tasks:")
    item_match = re.search(r'id:\s*"(simplyswords:[a-z0-9_./-]+)"', tasks_body)
    if not item_match:
        raise RuntimeError(f"Simply Swords quest {quest_match.group(1)} has no Simply Swords item task")
    return quest_match.group(1), item_match.group(1)


def human_name(item_id: str) -> str:
    return item_id.split(":", 1)[1].replace("_", " ").title()


def role_text(path: str) -> tuple[str, str]:
    if any(token in path for token in ("tablet", "gem", "remnant", "rune")):
        return "progression material", "прогрессионный материал"
    roles = [
        (("claymore", "greathammer", "greataxe"), "heavy weapon", "тяжёлое оружие"),
        (("warglaive", "glaive"), "sweeping reach weapon", "древковое оружие широкого контроля"),
        (("spear",), "long-reach weapon", "оружие большой дальности"),
        (("rapier",), "fast precision weapon", "быстрое точное оружие"),
        (("chakram",), "throwing weapon", "метательное оружие"),
        (("katana", "twinblade"), "high-tempo weapon", "оружие высокого темпа"),
        (("longsword",), "balanced reach weapon", "сбалансированное оружие с дальностью"),
    ]
    for tokens, en, ru in roles:
        if any(token in path for token in tokens):
            return en, ru
    return "unique weapon", "уникальное оружие"


def theme_text(path: str) -> tuple[str, str]:
    themes = [
        (("storm", "thunder", "lightning"), "storm and area-pressure effects", "грозовые эффекты и давление по площади"),
        (("soul", "lich", "watch", "omen"), "soul, execution or sustain effects", "эффекты душ, добивания или поддержания здоровья"),
        (("ember", "hearth", "brimstone", "flame", "fire"), "fire and damage-over-time effects", "огненные эффекты и периодический урон"),
        (("frost", "ice"), "cold and control effects", "эффекты холода и контроля"),
        (("toxic", "venom", "poison"), "poison and attrition effects", "яд и эффекты истощения"),
        (("shadow", "dark", "twisted"), "mobility or debuff-oriented effects", "эффекты движения или ослабления"),
    ]
    for tokens, en, ru in themes:
        if any(token in path for token in tokens):
            return en, ru
    return "its active and passive effects", "его активные и пассивные эффекты"


def localized_content(item_id: str) -> dict[str, tuple[str, list[str]]]:
    path = item_id.split(":", 1)[1]
    name = human_name(item_id)
    role_en, role_ru = role_text(path)
    theme_en, theme_ru = theme_text(path)
    if "material" in role_en:
        en_desc = [
            f"{name} is a {role_en} used by the Simply Swords acquisition or upgrade route. Its rarity must reflect the weapon tier it can unlock rather than becoming a random quest payout.",
            "Acceptance: obtain it from the declared stage-approved source, record whether it is renewable, set loot/EMC/trade policy, and verify that no reward table or generic simulator can duplicate it early."
        ]
        ru_desc = [
            f"{name} — {role_ru} для получения или улучшения оружия Simply Swords. Его редкость должна соответствовать открываемому уровню, а не случайной награде квеста.",
            "Приёмка: получите его из разрешённого источника этапа, зафиксируйте возобновляемость, политику лута/EMC/торговли и отсутствие раннего копирования наградами или симуляцией."
        ]
    else:
        en_desc = [
            f"{name} is a {role_en}. Treat {theme_en} as progression power, not as a cosmetic variant; read the actual tooltip and test the complete attack cycle before comparing raw damage.",
            "Acceptance: obtain the weapon through its approved source, record speed, reach, effect trigger, cooldown, durability and repair path, then prove that quests, trades, loot duplication and mob simulation cannot grant it before its stage."
        ]
        ru_desc = [
            f"{name} — {role_ru}. Считайте {theme_ru} силой прогрессии, а не косметикой; изучите подсказку и полный цикл атаки до сравнения одной цифры урона.",
            "Приёмка: получите оружие разрешённым путём, запишите скорость, дальность, условие эффекта, перезарядку, прочность и ремонт, затем исключите раннее получение наградами, торговлей, копированием лута и симуляцией."
        ]
    return {
        "en_us": (f"{name} — Source and Combat Acceptance", en_desc),
        "ru_ru": (f"{name} — источник и боевая приёмка", ru_desc),
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
        quest_id, item_id = quest_identity(block)
        block, removed = remove_rewards(block)
        reward_removals += int(removed)
        block, added = add_acceptance_task(block, quest_id)
        task_additions += int(added)
        replacements.append((start, end, block))

        content = localized_content(item_id)
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
            "chapter.261F532169C73839.title",
            "Simply Swords — Unique Weapon Catalogue" if locale == "en_us" else "Simply Swords — каталог уникального оружия",
        )
        path.write_text(language, encoding="utf-8", newline="\n")

    print(f"simply_swords_quests: {len(spans)}")
    print(f"random_rewards_removed: {reward_removals}")
    print(f"acceptance_tasks_added: {task_additions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
