from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "industrial_foregoing.snbt"
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
        raise RuntimeError("Industrial Foregoing chapter has no quests list")
    list_start = text.find("[", marker)
    list_end = matching_delimiter(text, list_start, "[", "]")
    spans: list[tuple[int, int]] = []
    cursor = list_start + 1
    while cursor < list_end:
        start = text.find("{", cursor, list_end)
        if start < 0:
            break
        end = matching_delimiter(text, start, "{", "}")
        spans.append((start, end + 1))
        cursor = end + 1
    return spans


def remove_rewards(block: str) -> tuple[str, bool]:
    match = re.search(r"(?m)^\s*rewards:\s*", block)
    if not match:
        return block, False
    value_start = match.end()
    while value_start < len(block) and block[value_start].isspace():
        value_start += 1
    if value_start >= len(block) or block[value_start] not in "[{":
        raise RuntimeError("Unexpected Industrial Foregoing rewards value")
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
    return hashlib.sha256(f"industrial_foregoing_acceptance:{quest_id}".encode()).hexdigest()[:16].upper()


def add_acceptance_task(block: str, quest_id: str) -> tuple[str, bool]:
    _, list_end, body = extract_array(block, "tasks:")
    if re.search(r'(?m)^\s*type:\s*"checkmark"', body):
        return block, False
    task_id = acceptance_id(quest_id)
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
        raise RuntimeError("Industrial Foregoing quest without a valid ID")
    _, _, tasks_body = extract_array(block, "tasks:")
    items = list(dict.fromkeys(re.findall(r'id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', tasks_body)))
    return quest_match.group(1), items


def human_name(item_id: str) -> str:
    return item_id.split(":", 1)[1].replace("_", " ").title()


def category(item_id: str) -> tuple[str, str, str, str]:
    namespace, path = item_id.split(":", 1)
    if namespace != "industrialforegoing":
        return (
            "cross-mod integration checkpoint",
            "межмодовая контрольная точка",
            "the supplying mod's stage, conversion direction and the absence of a cheaper substitute",
            "этап исходного мода, направление преобразования и отсутствие более дешёвой замены",
        )
    groups = [
        (("machine_frame",), "machine-frame tier", "уровень корпуса машины", "frame ancestry, previous-tier consumption and authoritative recipe replacement", "происхождение корпуса, расход предыдущего уровня и замену исходного рецепта"),
        (("fluid_extractor", "latex", "dryrubber", "plastic"), "latex and plastic production step", "этап производства латекса и пластика", "wood feed, latex rate, water supply, rubber conversion and plastic buffer", "подачу древесины, скорость латекса, воду, переработку резины и буфер пластика"),
        (("plant_sower", "plant_gatherer", "plant_fertilizer", "hydroponic"), "crop automation machine", "машина автоматизации растений", "working area, seed return, fertilizer demand, harvest routing and overflow", "рабочую область, возврат семян, расход удобрения, маршрут урожая и переполнение"),
        (("animal_", "sewer", "sewage_composter", "spores_recreator"), "animal or biological processing machine", "машина животной или биологической переработки", "entity limits, breeding inputs, waste handling, welfare spacing and output separation", "лимиты существ, входы разведения, отходы, безопасное размещение и разделение выходов"),
        (("mob_slaughter", "mob_duplicator", "mob_crusher"), "mob-processing machine", "машина переработки мобов", "spawn ownership, essence or fluid cost, blacklist policy and unique-drop exclusion", "владение спавном, стоимость эссенции или жидкости, чёрные списки и запрет уникального дропа"),
        (("laser_drill", "ore_laser", "fluid_laser"), "laser resource acquisition system", "лазерная система добычи ресурсов", "lens weighting, dimension rules, power cost, output table and stage-sensitive blacklist", "веса линз, правила измерений, энергозатраты, таблицу выходов и этапный чёрный список"),
        (("black_hole",), "high-capacity storage component", "компонент высокоёмкого хранения", "capacity, controller routing, extraction priority and recovery after controller loss", "ёмкость, маршрутизацию контроллера, приоритет извлечения и восстановление после его потери"),
        (("enchantment_", "potion_", "essence"), "experience or enchantment processor", "переработчик опыта или зачарований", "XP ownership, fluid conversion, enchantment extraction, invalid-input quarantine and duplication prevention", "владение опытом, преобразование жидкости, извлечение чар, карантин ошибок и защиту от копирования"),
        (("infinity_",), "Infinity-tier capability item", "предмет возможностей уровня Infinity", "charging tiers, special ability, effective mining or combat power, repair and all early acquisition paths", "уровни зарядки, особую способность, реальную силу добычи или боя, ремонт и все ранние пути получения"),
        (("material_stonework", "washing_factory", "fermentation_station"), "multi-recipe processing factory", "многорецептная производственная машина", "recipe locking, shared-input contamination, byproducts, energy demand and full-output shutdown", "фиксацию рецепта, смешивание общих входов, побочные продукты, энергию и остановку при полном выходе"),
        (("fluid_placer", "fluid_collector", "water_condensator"), "fluid logistics machine", "машина жидкостной логистики", "source rules, tank reserve, chunk boundaries, overflow and unintended world-fluid duplication", "правила источников, резерв ёмкостей, границы чанков, переполнение и исключение дублирования жидкости мира"),
        (("block_breaker", "block_placer"), "world interaction machine", "машина взаимодействия с миром", "area ownership, tool or block supply, protected blocks, unloaded chunks and item collection", "владение областью, подачу инструмента или блоков, защиту блоков, выгрузку чанков и сбор предметов"),
        (("biofuel", "bioreactor", "mycelial"), "renewable power or fuel system", "возобновляемая топливная или энергетическая система", "input diversity, fuel rate, generator demand, renewable boundaries and net energy balance", "разнообразие входов, скорость топлива, спрос генератора, границы возобновляемости и чистый энергобаланс"),
        (("marine_fisher", "resourceful_furnace"), "continuous production machine", "машина непрерывного производства", "input legality, loot or recipe table, sustained throughput, byproducts and output saturation", "законность входов, таблицу лута или рецептов, устойчивую скорость, побочные продукты и насыщение выхода"),
    ]
    for tokens, en_role, ru_role, en_focus, ru_focus in groups:
        if any(token in path for token in tokens):
            return en_role, ru_role, en_focus, ru_focus
    return (
        "Industrial Foregoing production component",
        "производственный компонент Industrial Foregoing",
        "its exact work area, input contract, power or fluid demand, output routing and safe shutdown",
        "точную рабочую область, контракт входов, расход энергии или жидкости, маршрут выхода и безопасную остановку",
    )


def localized_content(items: list[str], quest_id: str) -> dict[str, tuple[str, list[str]]]:
    if items:
        display = " / ".join(human_name(item) for item in items[:4])
        primary = items[0]
        role_en, role_ru, focus_en, focus_ru = category(primary)
    else:
        display = f"Factory Checkpoint {quest_id[-4:]}"
        role_en = "factory planning checkpoint"
        role_ru = "контрольная точка планирования фабрики"
        focus_en = "documented inputs, outputs, ownership, failure state and restart procedure"
        focus_ru = "задокументированные входы, выходы, владение, состояние отказа и процедуру перезапуска"

    en_desc = [
        f"{display} is a {role_en}. Owning the block or item is not completion: the corresponding process must operate as part of a controlled factory rather than as an isolated manual machine.",
        f"Acceptance: verify {focus_en}; complete a representative unattended batch, record rate and reserves, and prove that random rewards, mob simulation, loot, trades, EMC or alternate recipes cannot grant the capability before its declared stage."
    ]
    ru_desc = [
        f"{display} — {role_ru}. Владение блоком или предметом не завершает этап: соответствующий процесс должен работать как часть управляемой фабрики, а не отдельная ручная машина.",
        f"Приёмка: проверьте {focus_ru}; выполните типовую автономную партию, запишите скорость и резервы и исключите раннее получение возможности случайными наградами, симуляцией мобов, лутом, торговлей, EMC или альтернативным рецептом."
    ]
    return {
        "en_us": (f"{display} — Production Acceptance", en_desc),
        "ru_ru": (f"{display} — производственная приёмка", ru_desc),
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
    rewards_removed = 0
    tasks_added = 0

    for start, end in spans:
        block = text[start:end]
        quest_id, items = quest_identity(block)
        block, removed = remove_rewards(block)
        rewards_removed += int(removed)
        block, added = add_acceptance_task(block, quest_id)
        tasks_added += int(added)
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
        language = path.read_text(encoding="utf-8")
        for key, value in entries.items():
            language = upsert(language, key, value)
        language = upsert(
            language,
            "chapter.6873833ABE2267AE.title",
            "Industrial Foregoing — Controlled Factory Systems"
            if locale == "en_us"
            else "Industrial Foregoing — управляемые фабричные системы",
        )
        path.write_text(language, encoding="utf-8", newline="\n")

    print(f"industrial_foregoing_quests: {len(spans)}")
    print(f"reward_fields_removed: {rewards_removed}")
    print(f"acceptance_tasks_added: {tasks_added}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
