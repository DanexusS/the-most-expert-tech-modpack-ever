from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"

ENTRIES: dict[str, dict[str, str | list[str]]] = {
    "en_us": {
        "chapter.5C3FF9D1ECAC4860.title": "Create — Kinetic Engineering",
        "quest.4BB13C80196FD034.title": "Andesite: Structural Baseline",
        "quest.4BB13C80196FD034.quest_desc": [
            "Andesite begins the Create chapter, but one block is not a supply chain.",
            "Acceptance: identify a renewable or well-stocked source, reserve material for at least sixteen casings, and keep progression components separate from decorative use."
        ],
        "quest.0E5FC39E6C71A872.title": "Shafts: Controlled Power Paths",
        "quest.0E5FC39E6C71A872.quest_desc": [
            "Shafts transmit rotation; they do not create capacity and they do not solve overloads.",
            "Acceptance: build a labelled test line, verify rotation direction, and leave physical access for later clutches, gearboxes and maintenance."
        ],
        "quest.4B976C143EDA4317.title": "Andesite Casing: Batch Standard",
        "quest.4B976C143EDA4317.quest_desc": [
            "Casings are a recurring machine input and should not be crafted one at a time.",
            "Acceptance: provision a batch of sixteen, separate stripped-log processing from alloy storage, and keep enough reserve to rebuild one failed machine line."
        ],
        "quest.1837076B0EA3C11A.title": "Belts: Observable Logistics",
        "quest.1837076B0EA3C11A.quest_desc": [
            "Belts move items visibly and are useful for diagnosing throughput, spacing and blocked outputs.",
            "Acceptance: demonstrate automatic insertion and extraction, prevent item accumulation at the endpoint, and keep the belt reachable for filters and tunnels."
        ],
        "quest.4266BF7FCE3B4330.title": "Cogwheels: Ratio Demonstration",
        "quest.4266BF7FCE3B4330.quest_desc": [
            "Small and large cogwheels change speed and direction when meshed in different arrangements.",
            "Acceptance: build one speed-up and one speed-down example, observe the direction change, and record which machine branch must remain slowest."
        ],
        "quest.4C7CD3858A2BE870.title": "Mechanical Press: Continuous Output",
        "quest.4C7CD3858A2BE870.quest_desc": [
            "The press is the first serious proof that kinetic processing can replace repetitive crafting.",
            "Acceptance: process sixteen plates without manual item placement, extract every result automatically, and stop the input when output storage is full."
        ],
        "quest.1D00D782B8F0B6D6.title": "Mechanical Mixer: Basin Discipline",
        "quest.1D00D782B8F0B6D6.quest_desc": [
            "Mixer lines fail when recipes share uncontrolled inputs or when the basin cannot export the result.",
            "Acceptance: use filtered inputs, provide automatic extraction, isolate heated recipes, and complete three consecutive batches without touching the basin."
        ],
        "quest.732D1A96512F2BFD.title": "Steam Engine: Capacity Before Speed",
        "quest.732D1A96512F2BFD.quest_desc": [
            "Steam generation is an infrastructure project: heat, water, engines and stress capacity must remain stable together.",
            "Acceptance: water is continuous, heat can be shut down safely, and the intended factory load uses no more than 75% of available stress capacity."
        ],
        "quest.19754AE8C11A6317.title": "Deployer: Controlled Interaction",
        "quest.19754AE8C11A6317.quest_desc": [
            "Deployers automate player-like interaction and can consume the wrong item when their supply is not filtered.",
            "Acceptance: lock the held item, recover incomplete workpieces, stop on missing input, and keep wrench access without entering the moving assembly."
        ],
        "quest.0EE2E9EB6DC01E34.title": "Precision Mechanism: Sequenced Assembly",
        "quest.0EE2E9EB6DC01E34.quest_desc": [
            "Precision mechanisms are a repeatable manufacturing process, not a manual milestone tax.",
            "Acceptance: automate every sequence step, loop incomplete items correctly, isolate junk output, and complete a batch of sixteen without manual reinsertion."
        ],
        "quest.61348E2551E8AD6C.title": "Rotation Speed Controller: Governed RPM",
        "quest.61348E2551E8AD6C.quest_desc": [
            "A speed controller changes throughput but cannot create stress capacity.",
            "Acceptance: keep at least 25% stress reserve at the chosen RPM, place high-speed machines on a controlled branch, and verify safe restart after shutdown."
        ],
        "quest.197AB0E07A40512F.title": "Water Wheels: Stable Generation",
        "quest.197AB0E07A40512F.quest_desc": [
            "Water wheels provide predictable early capacity when flow direction and placement are correct.",
            "Acceptance: compare standard and large wheels, measure the resulting network, and choose a layout that stays below 75% load during normal processing."
        ],
        "quest.51CCB7ACFD7B45F1.title": "Brass Casing: Heated Production Gate",
        "quest.51CCB7ACFD7B45F1.quest_desc": [
            "Brass infrastructure marks the transition from andesite machinery to controlled heated production.",
            "Acceptance: blaze-burner fuel is managed safely, zinc and copper inputs are buffered, and a batch of sixteen casings can be repeated without moving the mixer."
        ]
    },
    "ru_ru": {
        "chapter.5C3FF9D1ECAC4860.title": "Create — кинетическая инженерия",
        "quest.4BB13C80196FD034.title": "Андезит: конструкционная основа",
        "quest.4BB13C80196FD034.quest_desc": [
            "Андезит открывает главу Create, но один блок ещё не является снабжением.",
            "Приёмка: найден возобновляемый или крупный запас, отложен материал минимум на шестнадцать корпусов, компоненты прогрессии не расходуются на декор."
        ],
        "quest.0E5FC39E6C71A872.title": "Валы: управляемые линии мощности",
        "quest.0E5FC39E6C71A872.quest_desc": [
            "Валы передают вращение, но не создают мощность и не исправляют перегрузку.",
            "Приёмка: собрана подписанная тестовая линия, проверено направление вращения, оставлен доступ для муфт, редукторов и обслуживания."
        ],
        "quest.4B976C143EDA4317.title": "Андезитовый корпус: пакетный стандарт",
        "quest.4B976C143EDA4317.quest_desc": [
            "Корпуса постоянно расходуются на машины, поэтому крафт по одному быстро становится узким местом.",
            "Приёмка: подготовлена партия из шестнадцати, обработка брёвен отделена от хранения сплава, есть резерв на восстановление одной линии."
        ],
        "quest.1837076B0EA3C11A.title": "Ремни: наблюдаемая логистика",
        "quest.1837076B0EA3C11A.quest_desc": [
            "Ремни наглядно показывают пропускную способность, интервалы между предметами и заблокированные выходы.",
            "Приёмка: ввод и вывод автоматизированы, на конце не копятся предметы, линия доступна для фильтров и тоннелей."
        ],
        "quest.4266BF7FCE3B4330.title": "Шестерни: демонстрация передаточного отношения",
        "quest.4266BF7FCE3B4330.quest_desc": [
            "Малые и большие шестерни меняют скорость и направление в зависимости от соединения.",
            "Приёмка: собраны примеры ускорения и замедления, проверена смена направления, отмечена ветвь, которая должна оставаться самой медленной."
        ],
        "quest.4C7CD3858A2BE870.title": "Механический пресс: непрерывный выпуск",
        "quest.4C7CD3858A2BE870.quest_desc": [
            "Пресс впервые доказывает, что кинетическая обработка заменяет повторяющийся ручной крафт.",
            "Приёмка: шестнадцать пластин обработаны без ручной подачи, результат выгружается автоматически, вход останавливается при полном выходе."
        ],
        "quest.1D00D782B8F0B6D6.title": "Механический миксер: дисциплина бассейна",
        "quest.1D00D782B8F0B6D6.quest_desc": [
            "Линии миксера ломаются из-за смешивания неконтролируемых входов и невозможности выгрузить результат.",
            "Приёмка: входы фильтруются, выход автоматизирован, нагреваемые рецепты изолированы, три партии проходят без касания бассейна."
        ],
        "quest.732D1A96512F2BFD.title": "Паровой двигатель: мощность до скорости",
        "quest.732D1A96512F2BFD.quest_desc": [
            "Паровая генерация требует одновременно стабильных воды, нагрева, двигателей и запаса нагрузочной мощности.",
            "Приёмка: вода непрерывна, нагрев безопасно отключается, штатная фабрика использует не более 75% доступной мощности напряжения."
        ],
        "quest.19754AE8C11A6317.title": "Развёртыватель: контролируемое взаимодействие",
        "quest.19754AE8C11A6317.quest_desc": [
            "Развёртыватель имитирует действия игрока и расходует неверные предметы при отсутствии фильтрации.",
            "Приёмка: удерживаемый предмет зафиксирован, незавершённые заготовки возвращаются, линия останавливается без входа, доступ ключом остаётся безопасным."
        ],
        "quest.0EE2E9EB6DC01E34.title": "Точный механизм: последовательная сборка",
        "quest.0EE2E9EB6DC01E34.quest_desc": [
            "Точные механизмы должны быть повторяемым производством, а не ручной платой за этап.",
            "Приёмка: автоматизированы все шаги, незавершённые детали правильно зациклены, брак отделён, партия из шестнадцати сделана без ручной подачи."
        ],
        "quest.61348E2551E8AD6C.title": "Регулятор скорости вращения: управляемые обороты",
        "quest.61348E2551E8AD6C.quest_desc": [
            "Регулятор повышает производительность, но не создаёт нагрузочную мощность.",
            "Приёмка: при выбранных оборотах остаётся минимум 25% резерва, скоростные машины выделены в управляемую ветвь, перезапуск после остановки безопасен."
        ],
        "quest.197AB0E07A40512F.title": "Водяные колёса: стабильная генерация",
        "quest.197AB0E07A40512F.quest_desc": [
            "Водяные колёса дают предсказуемую раннюю мощность при правильном потоке и размещении.",
            "Приёмка: сравнены обычное и большое колесо, сеть измерена, штатная нагрузка выбранной схемы остаётся ниже 75%."
        ],
        "quest.51CCB7ACFD7B45F1.title": "Латунный корпус: допуск нагретого производства",
        "quest.51CCB7ACFD7B45F1.quest_desc": [
            "Латунная инфраструктура переводит фабрику от андезитовых машин к управляемому нагретому производству.",
            "Приёмка: топливо горелки контролируется безопасно, цинк и медь буферизованы, партия из шестнадцати корпусов повторяется без перестройки миксера."
        ]
    }
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


def synchronize(locale: str, entries: dict[str, str | list[str]]) -> bool:
    path = LANG_DIR / f"{locale}.snbt"
    text = path.read_text(encoding="utf-8")
    changed = False
    for key, value in entries.items():
        text, entry_changed = upsert(text, key, value)
        changed = changed or entry_changed
    if changed:
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"{locale}: upgraded {len(entries)} Create core localization entries")
    else:
        print(f"{locale}: Create core localization already upgraded")
    return changed


def main() -> int:
    changed = False
    for locale, entries in ENTRIES.items():
        changed = synchronize(locale, entries) or changed
    print("Create core localization changed" if changed else "Create core localization unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
