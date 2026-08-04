from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "mekanism_part_1.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"

FOCUS_ITEMS = (
    "mekanism:metallurgic_infuser",
    "mekanism:enrichment_chamber",
    "mekanism:crusher",
    "mekanism:electrolytic_separator",
    "mekanism:purification_chamber",
    "mekanism:chemical_injection_chamber",
    "mekanism:chemical_dissolution_chamber",
    "mekanism:chemical_washer",
    "mekanism:chemical_crystallizer",
    "mekanism:pressurized_reaction_chamber",
    "mekanism:digital_miner",
)

CONTENT: dict[str, dict[str, tuple[str, list[str]]]] = {
    "en_us": {
        "mekanism:metallurgic_infuser": (
            "Metallurgic Infuser — Infusion Accounting",
            [
                "The Infuser combines an item stream with a stored infusion type; changing recipes without clearing or separating infusion can contaminate the next batch.",
                "Acceptance: dedicate or positively lock infusion inputs, expose remaining infusion, process sixteen mixed components, and recover safely from a full output without dumping valuable material."
            ],
        ),
        "mekanism:enrichment_chamber": (
            "Enrichment Chamber — Concentrate Buffer",
            [
                "Enrichment improves ore yield and converts secondary materials into concentrated forms used by many later recipes.",
                "Acceptance: separate ore and enrichment-material schedules, maintain a labelled concentrate buffer, process one stack unattended, and prevent scarce enrichment input from feeding a low-priority recipe."
            ],
        ),
        "mekanism:crusher": (
            "Crusher — Controlled Reduction",
            [
                "The Crusher supports ore processing and chemical production, so one uncontrolled shared line can block unrelated recipes with the wrong dust or biofuel product.",
                "Acceptance: filter each input route, separate outputs, complete sixteen operations from two recipe families, and stop intake when either destination cannot accept more material."
            ],
        ),
        "mekanism:electrolytic_separator": (
            "Electrolytic Separator — Gas Balance",
            [
                "Electrolysis creates two gases from one fluid; allowing either gas tank to fill can stop production even when the other gas is urgently needed.",
                "Acceptance: buffer both gases, configure dumping only for a documented surplus, preserve emergency oxygen, and demonstrate continuous operation through one complete upstream batch."
            ],
        ),
        "mekanism:purification_chamber": (
            "Purification Chamber — Threefold Ore Contract",
            [
                "Purification begins the threefold ore route and depends on stable oxygen supply, predictable raw-ore intake and downstream crushing capacity.",
                "Acceptance: process one stack of raw ore, buffer oxygen and clumps, prevent downstream saturation, and calculate whether the whole chain—not this machine alone—meets the target throughput."
            ],
        ),
        "mekanism:chemical_injection_chamber": (
            "Chemical Injection Chamber — Fourfold Chain",
            [
                "Chemical injection adds hydrogen chloride and another processing stage; gas starvation or excess intermediate stock makes the nominal yield irrelevant.",
                "Acceptance: provide monitored hydrogen chloride, isolate shards from clumps, process sixteen ore units end to end, and shut down upstream machines before any intermediate buffer overflows."
            ],
        ),
        "mekanism:chemical_dissolution_chamber": (
            "Chemical Dissolution — Slurry Boundary",
            [
                "Dissolution converts ore into dirty slurry using sulfuric acid and marks the hazardous entrance to the fivefold processing chain.",
                "Acceptance: acid production is separately buffered, dirty slurry has a dedicated route, no chemical is silently dumped, and loss of washing capacity automatically stops ore and acid input."
            ],
        ),
        "mekanism:chemical_washer": (
            "Chemical Washer — Slurry Purity",
            [
                "The Washer converts dirty slurry to clean slurry and can stall the entire fivefold line when water, chemical storage or output capacity is undersized.",
                "Acceptance: guarantee water reserve, separate dirty and clean networks, expose tank fill levels, and process a full dissolution batch without cross-contamination or manual tank clearing."
            ],
        ),
        "mekanism:chemical_crystallizer": (
            "Chemical Crystallizer — Crystal Throughput",
            [
                "Crystallization converts clean slurry into solid crystals; its batch rate determines whether the expensive fivefold chemical infrastructure can actually run continuously.",
                "Acceptance: crystallize one full clean-slurry batch, route crystals by material, prevent mixed outputs, and record the slowest stage across dissolution, washing and crystallization."
            ],
        ),
        "mekanism:pressurized_reaction_chamber": (
            "Pressurized Reaction Chamber — Three-Domain Recipe Control",
            [
                "The PRC combines items, fluids and gases; a recipe can appear idle when any one domain is missing, full or connected to the wrong side.",
                "Acceptance: label every side, buffer all three domains, complete eight cycles unattended, recover secondary outputs, and provide a visible diagnostic for the missing input that stops production."
            ],
        ),
        "mekanism:digital_miner": (
            "Digital Miner — Bounded Extraction Project",
            [
                "The Digital Miner is a strategic resource jump and must be treated as a controlled extraction project rather than an unlimited replacement for every mine.",
                "Acceptance: use explicit tag or item filters, bound radius and height, provide return transport and energy reserve, review replacement-block behavior, and verify the machine cannot extract progression-locked resources."
            ],
        ),
    },
    "ru_ru": {
        "mekanism:metallurgic_infuser": (
            "Металлургический наполнитель — учёт инфузии",
            [
                "Наполнитель объединяет поток предметов с сохранённым типом инфузии; смена рецепта без очистки или разделения загрязняет следующую партию.",
                "Приёмка: инфузия выделена или жёстко зафиксирована фильтрами, остаток виден, шестнадцать смешанных компонентов обработаны, полный выход не заставляет выбрасывать ценный материал."
            ],
        ),
        "mekanism:enrichment_chamber": (
            "Камера обогащения — буфер концентратов",
            [
                "Обогащение повышает выход руды и превращает вторичные материалы в концентраты, необходимые множеству поздних рецептов.",
                "Приёмка: расписания руды и материалов разделены, подписанный буфер поддерживается, стак проходит без вмешательства, дефицитный концентрат не расходуется на низкоприоритетный рецепт."
            ],
        ),
        "mekanism:crusher": (
            "Дробитель — управляемое измельчение",
            [
                "Дробитель используется и в рудной, и в химической цепочке, поэтому общий неконтролируемый вход блокирует процессы неверной пылью или биотопливом.",
                "Приёмка: каждый вход фильтруется, выходы разделены, выполнено шестнадцать операций двух семейств, подача прекращается при заполнении любого назначения."
            ],
        ),
        "mekanism:electrolytic_separator": (
            "Электролитический сепаратор — баланс газов",
            [
                "Электролиз создаёт два газа из одной жидкости; заполнение любого бака останавливает производство даже при срочной необходимости второго газа.",
                "Приёмка: оба газа буферизованы, сброс разрешён только для документированного избытка, аварийный кислород сохранён, установка непрерывно обрабатывает полную входную партию."
            ],
        ),
        "mekanism:purification_chamber": (
            "Камера очистки — контракт тройной руды",
            [
                "Очистка начинает тройную рудную цепочку и зависит от стабильного кислорода, предсказуемой подачи сырья и пропускной способности дробления.",
                "Приёмка: обработан стак сырой руды, кислород и комки имеют буферы, выход не переполняется, рассчитана скорость всей цепочки, а не одной машины."
            ],
        ),
        "mekanism:chemical_injection_chamber": (
            "Камера химической инъекции — четверная цепочка",
            [
                "Химическая инъекция добавляет хлороводород и новый этап; нехватка газа или избыток промежуточных материалов уничтожает пользу номинального выхода.",
                "Приёмка: хлороводород контролируется, осколки отделены от комков, шестнадцать единиц руды проходят весь маршрут, верхние машины останавливаются до переполнения буферов."
            ],
        ),
        "mekanism:chemical_dissolution_chamber": (
            "Камера химического растворения — граница суспензии",
            [
                "Растворение превращает руду в грязную суспензию с серной кислотой и является опасным входом в пятерную обработку.",
                "Приёмка: кислота имеет отдельный буфер, грязная суспензия идёт по выделенной линии, химикаты не сбрасываются, потеря мойки автоматически прекращает подачу руды и кислоты."
            ],
        ),
        "mekanism:chemical_washer": (
            "Химический омыватель — чистота суспензии",
            [
                "Омыватель превращает грязную суспензию в чистую и останавливает всю пятерную линию при недостатке воды, химических баков или выхода.",
                "Приёмка: вода имеет гарантированный резерв, грязная и чистая сети разделены, уровни баков видны, партия проходит без смешивания и ручной очистки ёмкостей."
            ],
        ),
        "mekanism:chemical_crystallizer": (
            "Химический кристаллизатор — выпуск кристаллов",
            [
                "Кристаллизация превращает чистую суспензию в кристаллы; скорость партий определяет, способна ли дорогая пятерная химическая инфраструктура работать непрерывно.",
                "Приёмка: полная партия суспензии кристаллизована, материалы разведены, смешение исключено, отмечен самый медленный этап растворения, мойки и кристаллизации."
            ],
        ),
        "mekanism:pressurized_reaction_chamber": (
            "Камера реакции под давлением — контроль трёх сред",
            [
                "PRC объединяет предметы, жидкости и газы; машина выглядит бездействующей, когда любая среда отсутствует, переполнена или подключена не к той стороне.",
                "Приёмка: все стороны подписаны, три среды буферизованы, восемь циклов проходят без вмешательства, вторичные выходы извлекаются, отсутствующий вход диагностируется явно."
            ],
        ),
        "mekanism:digital_miner": (
            "Цифровой шахтёр — ограниченный добывающий проект",
            [
                "Цифровой шахтёр является резким скачком ресурсов и должен использоваться как управляемый проект, а не бесконечная замена всем шахтам.",
                "Приёмка: фильтры заданы тегами или предметами, радиус и высота ограничены, возврат и энергия обеспечены, замена блоков проверена, закрытые по прогрессии ресурсы не добываются."
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
        raise RuntimeError(f"Mekanism focus item not found in chapter: {item_id}")
    object_start = text.rfind("\n\t\t{", 0, item_index)
    if object_start < 0:
        raise RuntimeError(f"Mekanism quest object start not found for {item_id}")
    object_start += 1
    object_end = matching_delimiter(text, object_start, "{", "}")
    block = text[object_start : object_end + 1]
    quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not quest_match:
        raise RuntimeError(f"Mekanism quest ID not found for {item_id}")
    return quest_match.group(1), object_start, object_end


def acceptance_id(quest_id: str) -> str:
    return hashlib.sha256(f"mekanism_acceptance:{quest_id}".encode()).hexdigest()[:16].upper()


def add_checkmark(text: str, item_id: str) -> tuple[str, bool, str]:
    quest_id, object_start, object_end = quest_for_item(text, item_id)
    task_id = acceptance_id(quest_id)
    if f'id: "{task_id}"' in text:
        return text, False, quest_id
    block = text[object_start : object_end + 1]
    tasks_marker = block.find("tasks:")
    if tasks_marker < 0:
        raise RuntimeError(f"Mekanism quest has no task list: {quest_id}")
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

    print(f"Mekanism core acceptance tasks added: {changed_tasks}")
    print("Mekanism core localization changed" if changed_localization else "Mekanism core localization unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
