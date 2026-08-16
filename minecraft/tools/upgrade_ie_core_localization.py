from __future__ import annotations

import json
import re
from pathlib import Path

from upgrade_ie_core import CHAPTER_PATH, quest_for_item

ROOT = Path(__file__).resolve().parents[1]
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"

CONTENT: dict[str, dict[str, tuple[str, list[str]]]] = {
    "en_us": {
        "immersiveengineering:hammer": (
            "Engineer's Hammer — Multiblock Control",
            [
                "The hammer forms and services Immersive Engineering multiblocks; it is not merely a crafting ingredient.",
                "Acceptance: keep a spare outside the production area, leave safe access to formation faces, and document how each critical multiblock is rebuilt after failure."
            ],
        ),
        "immersiveengineering:voltmeter": (
            "Voltmeter — Measure Before Connecting",
            [
                "Voltage tier, transfer limits and stored energy must be checked before unfamiliar machines share a network.",
                "Acceptance: measure source and buffer state, label the line tier, and preserve at least 25% normal transfer headroom before adding another consumer."
            ],
        ),
        "immersiveengineering:cokebrick": (
            "Coke Oven — Two-Product Process",
            [
                "The coke oven produces both coke and creosote; either blocked output can stop the entire process.",
                "Acceptance: form the complete oven, route creosote into controlled storage, provide solid-output space, and complete three batches without manual clearing."
            ],
        ),
        "immersiveengineering:blastbrick": (
            "Blast Furnace — Steel Baseline",
            [
                "Steel becomes an infrastructure material and must be produced in planned batches rather than only when a recipe blocks progress.",
                "Acceptance: provide coke input, slag handling and storage for at least one stack of steel output; the furnace must run three cycles unattended."
            ],
        ),
        "immersiveengineering:blastbrick_reinforced": (
            "Reinforced Blast Furnace — Continuous Steel",
            [
                "The reinforced furnace converts steel production from a manual milestone into an automatable industrial line.",
                "Acceptance: automate input and both outputs, prevent slag backpressure, provide maintenance access, and demonstrate a sixteen-ingot batch without intervention."
            ],
        ),
        "immersiveengineering:blastfurnace_preheater": (
            "Preheaters — Throughput With Power Cost",
            [
                "Preheaters accelerate the reinforced furnace but add continuous electrical demand and another failure point.",
                "Acceptance: install the intended pair, measure demand under load, keep 25% network headroom, and verify that loss of power does not deadlock material routing."
            ],
        ),
        "immersiveengineering:craftingtable": (
            "Engineer's Crafting Table — Dedicated Assembly",
            [
                "A dedicated assembly station keeps recurring engineering parts visible and prevents critical tools from disappearing into general storage.",
                "Acceptance: stock standard fasteners and plates, reserve tool slots, and label the table for IE components rather than treating it as another miscellaneous bench."
            ],
        ),
        "immersiveengineering:workbench": (
            "Engineer's Workbench — Upgrade Discipline",
            [
                "The workbench handles specialized equipment and upgrades whose ingredients should be controlled separately from bulk factory inputs.",
                "Acceptance: provide dedicated blueprint and component storage, retain rollback parts, and record the intended loadout before consuming rare upgrades."
            ],
        ),
        "immersiveengineering:component_steel": (
            "Iron and Steel Components — Batch Inventory",
            [
                "Mechanical components are repeated machine inputs and become a hidden bottleneck when crafted only at the final assembly step.",
                "Acceptance: maintain labelled buffers for iron and steel components, target at least sixteen of each, and expose the slowest plate or rod process for scaling."
            ],
        ),
        "immersiveengineering:fluid_pipe": (
            "Fluid Pipes — Directed Material Flow",
            [
                "A connected pipe network is not automatically a controlled network; unintended connections can mix products or drain buffers.",
                "Acceptance: label source and destination, use deliberate extraction points, provide shutoff access, and verify that a full destination cannot block an unrelated process."
            ],
        ),
        "immersiveengineering:fluid_pump": (
            "Fluid Pump — Bounded Transfer",
            [
                "The pump defines active fluid movement and must be sized around buffer capacity rather than maximum theoretical speed.",
                "Acceptance: power it through a protected line, prevent dry or wrong-fluid transfer, add a controllable stop condition, and test recovery after the destination fills."
            ],
        ),
        "immersiveengineering:cloche": (
            "Garden Cloche — Sustainable Input Contract",
            [
                "The cloche is useful only when water, power, soil and output handling form a stable contract with downstream machines.",
                "Acceptance: run three harvest cycles unattended, stop safely on full storage, keep seed recovery independent, and document the actual output rate used by consumers."
            ],
        ),
    },
    "ru_ru": {
        "immersiveengineering:hammer": (
            "Инженерный молот — управление мультиблоками",
            [
                "Молот формирует и обслуживает мультиблоки Immersive Engineering, а не просто участвует в рецептах.",
                "Приёмка: запасной молот хранится вне производства, к точкам формирования есть безопасный доступ, порядок восстановления критических мультиблоков задокументирован."
            ],
        ),
        "immersiveengineering:voltmeter": (
            "Вольтметр — измерить до подключения",
            [
                "Уровень напряжения, предел передачи и запас энергии нужно проверять до подключения незнакомой машины.",
                "Приёмка: измерены источник и буфер, линия подписана по уровню, перед добавлением потребителя остаётся минимум 25% штатного запаса передачи."
            ],
        ),
        "immersiveengineering:cokebrick": (
            "Коксовая печь — процесс с двумя продуктами",
            [
                "Коксовая печь одновременно производит кокс и креозот; заполнение любого выхода останавливает процесс.",
                "Приёмка: печь сформирована полностью, креозот направлен в управляемое хранилище, твёрдый выход не переполняется, три партии проходят без ручной очистки."
            ],
        ),
        "immersiveengineering:blastbrick": (
            "Доменная печь — базовый стандарт стали",
            [
                "Сталь становится инфраструктурным материалом и должна выпускаться партиями, а не только при блокировке очередного рецепта.",
                "Приёмка: обеспечены кокс, обработка шлака и место минимум под стак стали; три цикла проходят без вмешательства."
            ],
        ),
        "immersiveengineering:blastbrick_reinforced": (
            "Усиленная доменная печь — непрерывная сталь",
            [
                "Усиленная печь превращает ручной этап получения стали в автоматизируемую промышленную линию.",
                "Приёмка: вход и оба выхода автоматизированы, шлак не создаёт обратного давления, есть доступ для ремонта, партия из шестнадцати слитков проходит без вмешательства."
            ],
        ),
        "immersiveengineering:blastfurnace_preheater": (
            "Преднагреватели — выпуск с ценой энергии",
            [
                "Преднагреватели ускоряют усиленную печь, но добавляют постоянное энергопотребление и новую точку отказа.",
                "Приёмка: установлена нужная пара, нагрузка измерена, остаётся 25% запаса сети, потеря питания не блокирует маршрутизацию материалов."
            ],
        ),
        "immersiveengineering:craftingtable": (
            "Инженерный верстак — выделенная сборка",
            [
                "Выделенный верстак делает повторяющиеся детали видимыми и не даёт критическим инструментам потеряться в общем складе.",
                "Приёмка: стандартный крепёж и пластины запасены, места инструментов зарезервированы, верстак подписан для IE, а не используется как случайное хранилище."
            ],
        ),
        "immersiveengineering:workbench": (
            "Инженерная мастерская — дисциплина улучшений",
            [
                "Мастерская работает со специализированным оборудованием и улучшениями, которые нельзя смешивать с массовыми входами фабрики.",
                "Приёмка: чертежи и компоненты хранятся отдельно, сохранены детали для отката, целевая конфигурация записана до расходования редких улучшений."
            ],
        ),
        "immersiveengineering:component_steel": (
            "Железные и стальные компоненты — пакетный запас",
            [
                "Механические компоненты постоянно расходуются на машины и незаметно становятся узким местом при поштучном крафте.",
                "Приёмка: подписаны буферы железных и стальных деталей, целевой запас — минимум шестнадцать каждого вида, медленная операция пластин или стержней видна для масштабирования."
            ],
        ),
        "immersiveengineering:fluid_pipe": (
            "Жидкостные трубы — направленный поток",
            [
                "Соединённая трубная сеть не обязательно является управляемой: случайные связи смешивают продукты и опустошают буферы.",
                "Приёмка: источник и назначение подписаны, точки извлечения заданы намеренно, доступно отключение, полный приёмник не блокирует посторонний процесс."
            ],
        ),
        "immersiveengineering:fluid_pump": (
            "Жидкостный насос — ограниченная передача",
            [
                "Насос задаёт активное движение жидкости и должен соответствовать ёмкости буферов, а не максимальной теоретической скорости.",
                "Приёмка: питание защищено, исключена перекачка неверной жидкости или всухую, есть условие остановки, восстановление после заполнения приёмника проверено."
            ],
        ),
        "immersiveengineering:cloche": (
            "Садовая клош — устойчивый контракт снабжения",
            [
                "Клош полезен только тогда, когда вода, энергия, почва и вывод образуют стабильную систему с потребителями.",
                "Приёмка: три урожайных цикла проходят без вмешательства, полное хранилище безопасно останавливает линию, семена восстанавливаются отдельно, фактический выпуск записан."
            ],
        ),
    },
}


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
    changed_any = False
    for locale, content in CONTENT.items():
        path = LANG_DIR / f"{locale}.snbt"
        text = path.read_text(encoding="utf-8")
        changed = False
        for item_id, (title, description) in content.items():
            quest_id, _, _ = quest_for_item(chapter, item_id)
            text, title_changed = upsert(text, f"quest.{quest_id}.title", title)
            text, desc_changed = upsert(text, f"quest.{quest_id}.quest_desc", description)
            changed = changed or title_changed or desc_changed
        if changed:
            path.write_text(text, encoding="utf-8", newline="\n")
            print(f"{locale}: upgraded {len(content)} IE core quests")
        else:
            print(f"{locale}: IE core localization already upgraded")
        changed_any = changed_any or changed
    print("IE core localization changed" if changed_any else "IE core localization unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
