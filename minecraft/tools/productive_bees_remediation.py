from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import catalog_upgrade_common as common
from snbt_field_parser import extract_array, quest_spans

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "productive_bees.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
REPORT_PATH = ROOT / "docs" / "PRODUCTIVE_BEES_CATALOG_QUALITY_REPORT.md"
CHAPTER_ID = "26E6ED94168A05C4"
EXPECTED_QUESTS = 204
ACCEPTANCE_NAMESPACE = "productive_bees_catalog_acceptance"
QUEST_ID_RE = re.compile(r'(?m)^\s*id:\s*"([0-9A-F]{16})"')
BEE_TYPE_RE = re.compile(r'"productivebees:bee_type"\s*:\s*"productivebees:([a-z0-9_./-]+)"')
DIRECT_ITEM_RE = re.compile(r'\bid:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"')


def human(value: str) -> str:
    return value.replace("_", " ").replace("/", " ").title()


def quest_id(block: str) -> str:
    match = QUEST_ID_RE.search(block)
    if match is None:
        raise RuntimeError("Productive Bees quest without a valid ID")
    return match.group(1)


def task_context(block: str) -> tuple[str, str | None, list[str]]:
    _, _, tasks = extract_array(block, "tasks:")
    bee_match = BEE_TYPE_RE.search(tasks)
    bee_type = bee_match.group(1) if bee_match else None
    items = [
        item
        for item in DIRECT_ITEM_RE.findall(tasks)
        if item != "ftbfiltersystem:smart_filter"
    ]
    primary = items[0] if items else "productivebees:field_checkpoint"
    return primary, bee_type, items


def category(item_id: str, bee_type: str | None) -> tuple[str, str, str, str]:
    path = item_id.split(":", 1)[-1]
    if bee_type is not None:
        return (
            "resource bee, comb or bee-specific production proof",
            "ресурсная пчела, соты или доказательство производства конкретного вида",
            "the legal first source of the bee, required flower or block condition, hive occupancy, comb yield, processing output, genetics or breeding ancestry and prohibition of using simulation before first acquisition",
            "честный первый источник пчелы, требуемый цветок или блок, заполнение улья, выход сот, результат переработки, генетику или происхождение разведения и запрет симуляции до первого получения",
        )
    if any(token in path for token in ("hive", "apiary", "expansion_box")):
        return (
            "hive, apiary or colony-capacity component",
            "компонент улья, пасеки или вместимости колонии",
            "valid multiblock or hive structure, bee and flower capacity, weather and day-cycle behaviour, output access, expansion limits and recovery after moving or breaking one occupied hive",
            "валидную структуру пасеки или улья, вместимость пчёл и цветов, погоду и цикл дня, доступ к выходу, пределы расширения и восстановление после переноса или разрушения занятого улья",
        )
    if any(token in path for token in ("cage", "treat", "bottle", "nest", "feeder", "feeding_slab")):
        return (
            "bee handling, feeding, capture or breeding component",
            "компонент обращения с пчёлами, кормления, поимки или разведения",
            "safe capture and release, consumed feed, breeding pair and result, nest or feeding condition, duplicate handling and a recovery plan that does not delete a rare parent bee",
            "безопасную поимку и выпуск, расход корма, пару и результат разведения, условие гнезда или кормления, обработку дублей и восстановление без потери редкой родительской пчелы",
        )
    if any(token in path for token in ("centrifuge", "bottler", "powered", "processor")):
        return (
            "comb-processing or product-extraction machine",
            "машина переработки сот или извлечения продукта",
            "legal comb input, exact product and byproduct yield, power or container demand, side configuration, finite output buffers and clean shutdown when bottles or storage are unavailable",
            "честный вход сот, точный выход продукта и побочных материалов, спрос энергии или контейнеров, настройку сторон, конечные выходные буферы и чистую остановку при отсутствии бутылок или хранения",
        )
    if any(token in path for token in ("upgrade", "simulator", "productivity", "speed", "babee", "filter")):
        return (
            "apiary upgrade, simulation or production-control component",
            "улучшение пасеки, симуляции или управления производством",
            "upgrade slot and compatibility, measured before-and-after rate, energy or environmental tradeoff, protected-output blacklist, idle behaviour and removal without losing bees or stored combs",
            "слот и совместимость улучшения, измеренную скорость до и после, энергетический или природный компромисс, чёрный список защищённых выходов, простой и удаление без потери пчёл или накопленных сот",
        )
    if any(token in path for token in ("gene", "squashed", "breeding", "incubator")):
        return (
            "bee genetics, incubation or trait-selection component",
            "компонент генетики, инкубации или отбора признаков пчёл",
            "sample provenance, selected trait, probability or batch count, rejected samples, parent protection, repeatability and prevention of copying protected or impossible traits",
            "происхождение образца, выбранный признак, вероятность или размер партии, отклонённые образцы, защиту родителей, повторяемость и запрет копирования защищённых или невозможных признаков",
        )
    return (
        "specialized Productive Bees production component",
        "специализированный производственный компонент Productive Bees",
        "its exact hive, breeding, processing, genetics or logistics role, legal source, representative operating cycle, finite buffer and recovery after one bee or machine becomes unavailable",
        "его точную роль в улье, разведении, переработке, генетике или логистике, честный источник, типовой рабочий цикл, конечный буфер и восстановление после потери одной пчелы или машины",
    )


def localized(block: str, qid: str) -> dict[str, tuple[str, list[str]]]:
    item_id, bee_type, items = task_context(block)
    role_en, role_ru, focus_en, focus_ru = category(item_id, bee_type)
    if bee_type:
        subject_en = f"{human(bee_type)} Bee Production"
        subject_ru = f"Производство пчелы: {human(bee_type)}"
    elif items:
        subject_en = human(item_id.split(":", 1)[-1])
        subject_ru = human(item_id.split(":", 1)[-1])
    else:
        subject_en = f"Apiary Checkpoint {qid[-4:]}"
        subject_ru = f"Контроль пасеки {qid[-4:]}"

    en = [
        f"{subject_en} is a {role_en} in the Productive Bees route. The objective is a healthy, supplied and recoverable production cell—not collecting a comb or receiving a bee from a quest reward.",
        f"Acceptance: verify {focus_en}; run or observe a representative production cycle, record hive occupancy, environmental condition, comb rate, processing output and overflow, then test one interruption without losing a rare bee.",
    ]
    ru = [
        f"{subject_ru} — {role_ru} ветви Productive Bees. Целью является здоровая, снабжаемая и восстанавливаемая производственная ячейка, а не коллекционирование сот или получение пчелы из квестовой награды.",
        f"Приёмка: проверьте {focus_ru}; выполните или наблюдайте типовой производственный цикл, запишите заполнение улья, условия среды, скорость сот, выход переработки и переполнение, затем испытайте одно прерывание без потери редкой пчелы.",
    ]
    return {
        "en_us": (f"{subject_en} — Apiary Acceptance", en),
        "ru_ru": (f"{subject_ru} — приёмка пасеки", ru),
    }


def upgrade() -> None:
    common.extract_array = extract_array
    text = CHAPTER_PATH.read_text(encoding="utf-8")
    spans = quest_spans(text)
    replacements: list[tuple[int, int, str]] = []
    localization: dict[str, dict[str, str | list[str]]] = {"en_us": {}, "ru_ru": {}}
    rewards_removed = 0
    tasks_added = 0

    for start, end in spans:
        block = text[start:end]
        qid = quest_id(block)
        block, removed = common.remove_rewards(block)
        rewards_removed += int(removed)
        block, added = common.add_acceptance_task(block, qid, ACCEPTANCE_NAMESPACE)
        tasks_added += int(added)
        replacements.append((start, end, block))
        for locale, (title, desc) in localized(block, qid).items():
            localization[locale][f"quest.{qid}.title"] = title
            localization[locale][f"quest.{qid}.quest_desc"] = desc

    for start, end, block in reversed(replacements):
        text = text[:start] + block + text[end:]
    CHAPTER_PATH.write_text(text, encoding="utf-8", newline="\n")

    for locale, entries in localization.items():
        path = LANG_DIR / f"{locale}.snbt"
        language = path.read_text(encoding="utf-8")
        language = common.upsert(
            language,
            f"chapter.{CHAPTER_ID}.title",
            "Productive Bees — Sustainable Apiary Engineering"
            if locale == "en_us"
            else "Productive Bees — устойчивая инженерия пасеки",
        )
        for key, value in entries.items():
            language = common.upsert(language, key, value)
        path.write_text(language, encoding="utf-8", newline="\n")

    print(f"productive_bees_quests: {len(spans)}")
    print(f"productive_bees_rewards_removed: {rewards_removed}")
    print(f"productive_bees_acceptance_tasks_added: {tasks_added}")


def gate() -> int:
    common.extract_array = extract_array
    chapter = CHAPTER_PATH.read_text(encoding="utf-8")
    spans = quest_spans(chapter)
    en = common.parse_localization(LANG_DIR / "en_us.snbt")
    ru = common.parse_localization(LANG_DIR / "ru_ru.snbt")
    failures: list[str] = []
    bilingual = 0
    with_check = 0

    if len(spans) != EXPECTED_QUESTS:
        failures.append(f"Expected {EXPECTED_QUESTS} Productive Bees quests, found {len(spans)}")

    for start, end in spans:
        block = chapter[start:end]
        qid = quest_id(block)
        if "rewards:" in block:
            failures.append(f"{qid}: rewards remain")
        types = common.task_types(block)
        if types.count("checkmark") >= 1:
            with_check += 1
        else:
            failures.append(f"{qid}: practical acceptance check missing")
        desc_key = f"quest.{qid}.quest_desc"
        title_key = f"quest.{qid}.title"
        en_len = common.visible_length(en.get(desc_key, ""))
        ru_len = common.visible_length(ru.get(desc_key, ""))
        if title_key in en and title_key in ru and en_len >= 220 and ru_len >= 220:
            bilingual += 1
        else:
            failures.append(f"{qid}: incomplete RU/EN guidance (EN {en_len}, RU {ru_len})")

    lines = [
        "# Productive Bees Catalogue Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "Every bee, comb, hive, genetics, upgrade and processing quest must describe a recoverable apiary production cell and contain a practical acceptance check without material, XP or random rewards.",
        "",
        f"- Quests: **{len(spans)} / {EXPECTED_QUESTS}**",
        f"- Practical acceptance tasks: **{with_check} / {len(spans)}**",
        f"- Full RU/EN guidance: **{bilingual} / {len(spans)}**",
        f"- Failures: **{len(failures)}**",
        "",
    ]
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"productive_bees_catalog: {'PASS' if not failures else 'FAIL'}")
    print(f"quests: {len(spans)}")
    print(f"failures: {len(failures)}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("upgrade", "gate"))
    args = parser.parse_args()
    if args.mode == "upgrade":
        upgrade()
        return 0
    return gate()


if __name__ == "__main__":
    sys.exit(main())
