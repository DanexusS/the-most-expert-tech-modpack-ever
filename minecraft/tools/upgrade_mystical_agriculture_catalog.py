from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "mystical_ag.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"

TIERS = (
    "inferium",
    "prudentium",
    "tertium",
    "imperium",
    "supremium",
    "awakened_supremium",
    "insanium",
)
TIER_RU = {
    "inferium": "инфериумный",
    "prudentium": "пруденциальный",
    "tertium": "тертиумный",
    "imperium": "империумный",
    "supremium": "супремиумный",
    "awakened_supremium": "пробуждённый супремиумный",
    "insanium": "инсаниумный",
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
        raise RuntimeError("Mystical Agriculture chapter has no quests list")
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
        raise RuntimeError("Unexpected Mystical Agriculture rewards value")
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


def quest_identity(block: str) -> tuple[str, list[str]]:
    quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not quest_match:
        raise RuntimeError("Mystical Agriculture quest without a valid ID")
    _, _, tasks_body = extract_array(block, "tasks:")
    items = list(dict.fromkeys(re.findall(r'id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', tasks_body)))
    if not items:
        icon_match = re.search(r'icon:\s*\{[^{}]*id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', block)
        if icon_match:
            items = [icon_match.group(1)]
    return quest_match.group(1), items


def acceptance_id(quest_id: str) -> str:
    return hashlib.sha256(f"mystical_agriculture_acceptance:{quest_id}".encode()).hexdigest()[:16].upper()


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


def human_name(item_id: str) -> str:
    return item_id.split(":", 1)[1].replace("_", " ").title()


def tier(path: str) -> tuple[str, str]:
    for value in reversed(TIERS):
        if path == value or path.startswith(value + "_") or path.endswith("_" + value) or ("_" + value + "_") in path:
            return value.replace("_", " ").title(), TIER_RU[value]
    return "Untiered", "внеуровневый"


def category(item_id: str) -> tuple[str, str, str, str]:
    namespace, path = item_id.split(":", 1)
    tier_en, tier_ru = tier(path)
    if namespace not in {"mysticalagriculture", "mysticalagradditions"}:
        return (
            "cross-mod crop or integration requirement",
            "межмодовое требование культуры или интеграции",
            "the original encounter or machine path, the declared stage and whether agriculture is allowed only after first legitimate acquisition",
            "исходный бой или машинный путь, заявленный этап и разрешение сельского производства только после первого честного получения",
        )

    categories = [
        (("infusion_altar", "infusion_pedestal"), "infusion structure component", "компонент инфузионной структуры", "the complete altar layout, pedestal count, recipe isolation and reusable catalyst handling", "полную схему алтаря, число пьедесталов, изоляцию рецепта и возврат многоразового катализатора"),
        (("seeds",), "resource-crop seed", "семя ресурсной культуры", "the legal first source of the represented material, seed crafting cost, farmland tier, harvest yield and automation boundary", "разрешённый первый источник представленного материала, стоимость семени, уровень почвы, выход урожая и границу автоматизации"),
        (("essence",), "tier or resource essence", "уровневая или ресурсная эссенция", "upgrade and downgrade direction, infusion-crystal durability, batch ratios and prevention of recursive conversion or EMC loops", "направление повышения и понижения, прочность инфузионного кристалла, размер партии и запрет рекурсивных преобразований или EMC-циклов"),
        (("farmland",), "crop-tier farmland", "почва уровня культуры", "hydration, crop-tier compatibility, harvest area, replacement stock and the effect of acceleration on server load", "увлажнение, совместимость уровня культуры, площадь сбора, запас замены и влияние ускорения на нагрузку сервера"),
        (("soul_jar", "soulium", "soul_dagger"), "soul acquisition component", "компонент получения душ", "which creatures may fill the soul resource, first-kill legitimacy, storage capacity and exclusion from Woot, neural simulation and generic spawners", "какие существа дают ресурс души, честность первой победы, ёмкость хранения и исключение из Woot, нейросимуляции и обычных спавнеров"),
        (("reprocessor",), f"{tier_en} seed reprocessor", f"{tier_ru} переработчик семян", "seed recovery yield, energy and time cost, output buffering and prevention of a seed-to-essence positive feedback loop", "выход переработки семян, стоимость энергии и времени, буфер результата и запрет положительного цикла семена-эссенция"),
        (("growth_accelerator",), f"{tier_en} growth accelerator", f"{tier_ru} ускоритель роста", "vertical stacking, effective range, diminishing benefit, chunk activity and a measured limit for accelerated crop density", "вертикальное складывание, радиус, убывающую пользу, активность чанка и измеренный предел плотности ускоренных культур"),
        (("watering_can",), f"{tier_en} watering tool", f"{tier_ru} инструмент полива", "manual learning use, area of effect, automation restrictions and the point at which the task must move to bounded infrastructure", "ручное обучающее применение, площадь действия, ограничения автоматизации и момент перехода к ограниченной инфраструктуре"),
        (("furnace",), f"{tier_en} processing furnace", f"{tier_ru} производственная печь", "real throughput, fuel or energy supply, input and output buffering and whether the tier duplicates an earlier machine without a useful role", "реальную пропускную способность, подачу топлива или энергии, входные и выходные буферы и отсутствие бессмысленного дублирования ранней машины"),
        (("harvester", "machine_frame"), "crop automation machine", "машина автоматизации культур", "harvest footprint, replant behavior, seed retention, overflow shutdown and compatibility with protected or stage-gated crops", "площадь сбора, повторную посадку, сохранение семян, остановку при переполнении и совместимость с защищёнными или этапными культурами"),
        (("infusion_crystal",), "reusable infusion catalyst", "многоразовый инфузионный катализатор", "durability, return behavior, recipe ownership and emergency replacement without handing out free tier progression", "прочность, возврат, владельца рецепта и аварийную замену без бесплатного продвижения уровня"),
        (("armor", "helmet", "chestplate", "leggings", "boots", "sword", "pickaxe", "axe", "shovel", "hoe", "bow", "crossbow", "shield", "staff", "scythe"), f"{tier_en} equipment", f"{tier_ru} экипировка", "capability unlocks, augment slots, repair path, replacement cost and whether flight, area mining or damage exceeds the declared stage", "открываемые возможности, слоты улучшений, ремонт, стоимость замены и соответствие полёта, массовой добычи или урона заявленному этапу"),
        (("augment",), "equipment augment", "улучшение экипировки", "slot compatibility, mutually exclusive effects, stage-changing capability and safe removal or replacement", "совместимость слота, взаимоисключающие эффекты, изменение возможностей этапа и безопасное снятие или замену"),
        (("creative",), "creative-class agriculture component", "творческий сельскохозяйственный компонент", "all prior convergence requirements, non-renewable permission evidence and complete exclusion from ordinary crops, rewards, EMC and simulation", "все предыдущие требования схождения, невозобновляемое доказательство допуска и полное исключение из обычных культур, наград, EMC и симуляции"),
    ]
    for tokens, en_role, ru_role, en_focus, ru_focus in categories:
        if any(token in path for token in tokens):
            return en_role, ru_role, en_focus, ru_focus
    return (
        f"{tier_en} Mystical Agriculture component",
        f"{tier_ru} компонент Mystical Agriculture",
        "its actual production role, legal first acquisition, sustained input and output rates and every renewable-resource bypass it could introduce",
        "его производственную роль, честное первое получение, устойчивые входные и выходные скорости и каждый возможный обход через возобновляемые ресурсы",
    )


def localized_content(items: list[str], quest_id: str) -> dict[str, tuple[str, list[str]]]:
    primary = items[0] if items else "mysticalagriculture:prosperity_shard"
    if len(items) > 1:
        display = " / ".join(human_name(item) for item in items[:3])
        if len(items) > 3:
            display += " / System"
        role_en = "linked agriculture system"
        role_ru = "связанная сельскохозяйственная система"
        focus_en = "component ratios, shared catalysts, legal crop tiers, output ownership and unattended completion without duplicating seeds or essences"
        focus_ru = "соотношения компонентов, общие катализаторы, разрешённые уровни культур, владельца выхода и автономное завершение без дублирования семян или эссенций"
    else:
        display = human_name(primary)
        role_en, role_ru, focus_en, focus_ru = category(primary)

    en_desc = [
        f"{display} is a {role_en}. In an expert progression pack, renewable production is permitted only after the represented resource, creature or capability has been obtained through its legitimate stage path.",
        f"Acceptance: verify {focus_en}; process or harvest a representative batch with bounded automation, record yield and reserve, and prove that quest rewards, EMC, trades, loot, simulated mobs or alternate seed recipes cannot unlock or multiply this resource early."
    ]
    ru_desc = [
        f"{display} — {role_ru}. В экспертной прогрессии возобновляемое производство разрешается только после честного получения представленного ресурса, существа или возможности на соответствующем этапе.",
        f"Приёмка: проверьте {focus_ru}; обработайте или соберите типовую партию ограниченной автоматикой, запишите выход и резерв и исключите раннее открытие или умножение через награды, EMC, торговлю, лут, симуляцию мобов и альтернативные семена."
    ]
    return {
        "en_us": (f"{display} — Renewable Production Acceptance", en_desc),
        "ru_ru": (f"{display} — приёмка возобновляемого производства", ru_desc),
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

        content = localized_content(items, quest_id)
        for locale, (title, desc) in content.items():
            localization[locale][f"quest.{quest_id}.title"] = title
            localization[locale][f"quest.{quest_id}.quest_desc"] = desc

    for start, end, block in reversed(replacements):
        text = text[:start] + block + text[end:]
    CHAPTER_PATH.write_text(text, encoding="utf-8", newline="\n")

    for locale, entries in localization.items():
        path = LANG_DIR / f"{locale}.snbt"
        lang = path.read_text(encoding="utf-8")
        for key, value in entries.items():
            lang = upsert(lang, key, value)
        path.write_text(lang, encoding="utf-8", newline="\n")

    print(f"mystical_agriculture_quests: {len(spans)}")
    print(f"reward_fields_removed: {reward_removals}")
    print(f"acceptance_tasks_added: {task_additions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
