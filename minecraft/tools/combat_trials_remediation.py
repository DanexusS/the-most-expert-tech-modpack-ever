from __future__ import annotations

import argparse
import re
import sys

import catalog_upgrade_common as common
from catalog_upgrade_batch import merge_entries
from snbt_field_parser import quest_spans

ROOT = common.ROOT
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "combat_trials.snbt"
REPORT_PATH = ROOT / "docs" / "COMBAT_TRIALS_QUALITY_REPORT.md"
CHAPTER_ID = "6EA0FB427B985A5D"
EXPECTED_QUESTS = 108
MINIMUM_DESCRIPTION = 220


def quest_id(block: str) -> str:
    match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not match:
        raise RuntimeError("Quest without a valid ID")
    return match.group(1)


def humanize(value: str) -> str:
    return value.split(":", 1)[-1].replace("_", " ").replace("/", " ").title()


def entity_and_count(block: str) -> tuple[str | None, int]:
    entity_match = re.search(r'(?m)^\s*entity:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', block)
    if not entity_match:
        return None, 0
    entity = entity_match.group(1)
    value_match = re.search(r"(?m)^\s*value:\s*([0-9]+)L?", block)
    return entity, int(value_match.group(1)) if value_match else 1


def trial_profile(entity: str | None, count: int, block: str) -> tuple[str, str, str, str]:
    if entity is None:
        return (
            "combat-readiness and arena-planning checkpoint",
            "контрольная точка боевой готовности и планирования арены",
            "loadout baseline, armor and resistance coverage, healing and escape reserve, arena boundaries, protected storage, defeat recovery and explicit criteria for beginning the next trial",
            "базовое снаряжение, покрытие брони и сопротивлений, запас лечения и отхода, границы арены, защищённое хранение, восстановление после поражения и явные критерии начала следующего испытания",
        )
    if count <= 1 or 'shape: "octagon"' in block:
        return (
            "single boss or first-victory combat trial",
            "одиночное боссовое испытание или проверка первой победы",
            "summoning or location route, arena containment, attack and resistance profile, phase changes, add control, retreat threshold, first-kill evidence, unique-drop custody and recovery after defeat without automated replacement of the initial victory",
            "маршрут призыва или поиска, изоляцию арены, профиль атак и сопротивлений, смену фаз, контроль прислужников, порог отступления, доказательство первой победы, хранение уникального лута и восстановление после поражения без автоматической замены первой победы",
        )
    if count <= 5:
        return (
            "elite group or repeated high-threat combat trial",
            "испытание элитной группы или повторяемой высокой угрозы",
            "spawn source and count, target priority, terrain control, crowd-control resistance, damage and healing budget, kill-count verification, drop buffer, interrupted-wave recovery and prevention of a trapped farm satisfying the trial unattended",
            "источник и число противников, приоритет целей, контроль местности, сопротивление контролю толпы, бюджет урона и лечения, проверку числа побед, буфер лута, восстановление прерванной волны и запрет выполнения испытания без участия через ловушечную ферму",
        )
    return (
        "mass-wave combat endurance trial",
        "массовое испытание боевой выносливости волной",
        "required count and spawn source, arena capacity, sustained damage and healing rate, crowd-control plan, entity cap and lag budget, retreat or reset condition, drop cleanup and proof that automation or forced spawning does not replace active completion",
        "требуемое число и источник спавна, вместимость арены, устойчивую скорость урона и лечения, план контроля толпы, лимит сущностей и лаг-бюджет, условие отступления или сброса, очистку лута и доказательство, что автоматизация или принудительный спавн не заменяют активное выполнение",
    )


def localized_content(block: str) -> dict[str, tuple[str, list[str]]]:
    qid = quest_id(block)
    entity, count = entity_and_count(block)
    display = humanize(entity) if entity else f"Combat Readiness {qid[-4:]}"
    role_en, role_ru, focus_en, focus_ru = trial_profile(entity, count, block)
    count_en = f" Required verified count: {count}." if entity and count > 1 else ""
    count_ru = f" Требуемое подтверждённое количество: {count}." if entity and count > 1 else ""
    return {
        "en_us": (
            f"{display} — Combat Trial Acceptance",
            [
                f"{display} is a {role_en}. The objective is prepared, active and recoverable combat—not raw kill repetition, an unattended farm or an XP reward.{count_en}",
                f"Acceptance: verify {focus_en}; document the loadout and arena before engagement, complete the required active encounter, reconcile ordinary and unique drops, record one failure or retreat response and confirm that summons, traps, duplication, quest rewards and automated simulation cannot satisfy first-victory or boss permissions.",
            ],
        ),
        "ru_ru": (
            f"{display} — приёмка боевого испытания",
            [
                f"{display} — {role_ru}. Целью является подготовленный, активный и восстанавливаемый бой, а не простое повторение убийств, автономная ферма или награда опытом.{count_ru}",
                f"Приёмка: проверьте {focus_ru}; задокументируйте снаряжение и арену до боя, активно завершите требуемую встречу, сверьте обычный и уникальный лут, зафиксируйте одну реакцию на поражение или отступление и исключите выполнение допусков первой победы или босса через призывные обходы, ловушки, копирование, награды и автоматическую симуляцию.",
            ],
        ),
    }


def upgrade() -> None:
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
        block, added = common.add_acceptance_task(block, qid, "combat_trial_acceptance")
        tasks_added += int(added)
        replacements.append((start, end, block))
        for locale, (title, desc) in localized_content(block).items():
            localization[locale][f"quest.{qid}.title"] = title
            localization[locale][f"quest.{qid}.quest_desc"] = desc

    for start, end, block in reversed(replacements):
        text = text[:start] + block + text[end:]
    CHAPTER_PATH.write_text(text, encoding="utf-8", newline="\n")

    localization["en_us"][f"chapter.{CHAPTER_ID}.title"] = "Combat Trials — Active Encounters and Recovery"
    localization["ru_ru"][f"chapter.{CHAPTER_ID}.title"] = "Боевые испытания — активные встречи и восстановление"
    for locale, entries in localization.items():
        path = common.LANG_DIR / f"{locale}.snbt"
        original = path.read_text(encoding="utf-8")
        merged = merge_entries(original, entries)
        if merged != original:
            path.write_text(merged, encoding="utf-8", newline="\n")

    print("catalog: combat_trials")
    print(f"quests: {len(spans)}")
    print(f"rewards_removed: {rewards_removed}")
    print(f"acceptance_tasks_added: {tasks_added}")


def gate() -> int:
    chapter = CHAPTER_PATH.read_text(encoding="utf-8")
    en = common.parse_localization(common.LANG_DIR / "en_us.snbt")
    ru = common.parse_localization(common.LANG_DIR / "ru_ru.snbt")
    spans = quest_spans(chapter)
    failures: list[str] = []
    rows: list[tuple[str, int, str, int, int, bool, str]] = []

    if len(spans) != EXPECTED_QUESTS:
        failures.append(f"Expected {EXPECTED_QUESTS} quests, found {len(spans)}")

    for start, end in spans:
        block = chapter[start:end]
        qid = quest_id(block)
        entity, count = entity_and_count(block)
        label = entity or f"checkpoint:{qid}"
        types = common.task_types(block)
        en_len = common.visible_length(en.get(f"quest.{qid}.quest_desc", ""))
        ru_len = common.visible_length(ru.get(f"quest.{qid}.quest_desc", ""))
        no_rewards = "rewards:" not in block
        status = "PASS"
        if "checkmark" not in types:
            failures.append(f"{label}: no practical acceptance task")
            status = "FAIL"
        if not no_rewards:
            failures.append(f"{label}: reward remains")
            status = "FAIL"
        if en_len < MINIMUM_DESCRIPTION or ru_len < MINIMUM_DESCRIPTION:
            failures.append(f"{label}: description too short (EN {en_len}, RU {ru_len})")
            status = "FAIL"
        rows.append((label, count, qid, en_len, ru_len, no_rewards, status))

    lines = [
        "# Combat Trials Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "Every combat trial requires entity- and count-aware RU/EN preparation, active-completion acceptance, recovery planning and no XP, item, random or loot rewards.",
        "",
        "| Entity/checkpoint | Count | Quest | EN description | RU description | No rewards | Status |",
        "|---|---:|---|---:|---:|---|---|",
    ]
    for label, count, qid, en_len, ru_len, no_rewards, status in rows:
        lines.append(f"| `{label}` | {count} | `{qid}` | {en_len} | {ru_len} | {'yes' if no_rewards else 'no'} | {status} |")
    lines.extend([
        "",
        "## Aggregate",
        "",
        f"- Quests: **{len(rows)}**",
        f"- Reward-free: **{sum(row[5] for row in rows)}**",
        f"- Fully bilingual: **{sum(row[3] >= MINIMUM_DESCRIPTION and row[4] >= MINIMUM_DESCRIPTION for row in rows)}**",
        f"- Failures: **{len(failures)}**",
        "",
    ])
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"combat_trials_quality: {'PASS' if not failures else 'FAIL'}")
    print(f"quests: {len(rows)}")
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
