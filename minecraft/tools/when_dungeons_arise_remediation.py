from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import catalog_upgrade_common as common
from catalog_upgrade_batch import merge_entries
from snbt_field_parser import quest_spans

ROOT = common.ROOT
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "when_dungeons_arise.snbt"
REPORT_PATH = ROOT / "docs" / "WHEN_DUNGEONS_ARISE_EXPEDITION_QUALITY_REPORT.md"
CHAPTER_ID = "231570DE6A7FCD52"
EXPECTED_QUESTS = 31
MINIMUM_DESCRIPTION = 220


def stable_id(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16].upper()


def quest_id(block: str) -> str:
    match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not match:
        raise RuntimeError("Quest without a valid ID")
    return match.group(1)


def advancement_id(block: str) -> str | None:
    match = re.search(r'(?m)^\s*advancement:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', block)
    return match.group(1) if match else None


def humanize(value: str) -> str:
    path = value.split(":", 1)[-1].rsplit("/", 1)[-1]
    for prefix in ("find_", "locate_", "visit_", "enter_", "kill_"):
        if path.startswith(prefix):
            path = path[len(prefix) :]
            break
    return path.replace("_", " ").replace("-", " ").title()


def focus_for(advancement: str | None) -> tuple[str, str, str, str]:
    path = advancement or "expedition_checkpoint"
    if any(token in path for token in ("ship", "pirate", "naval", "lighthouse")):
        return (
            "maritime ruin or ship expedition",
            "морская экспедиция к руинам или кораблю",
            "approach route, water escape, ranged threats, vertical access, cargo capacity, unique-loot custody and extraction before the structure becomes an uncontrolled farm",
            "маршрут подхода, отход по воде, дальние угрозы, вертикальный доступ, вместимость груза, хранение уникального лута и эвакуацию до превращения структуры в неконтролируемую ферму",
        )
    if any(token in path for token in ("mine", "foundry", "forge", "quarry")):
        return (
            "underground industrial-ruin expedition",
            "подземная экспедиция к промышленным руинам",
            "ventilation and fire risk, blocked corridors, vertical retreat, hostile density, ore-versus-loot classification, protected containers and recovery after a cave-in or failed extraction",
            "вентиляцию и риск огня, заблокированные коридоры, вертикальное отступление, плотность противников, различие руды и лута, защищённые контейнеры и восстановление после обвала либо неудачной эвакуации",
        )
    if any(token in path for token in ("tower", "keep", "castle", "palace", "fort", "monastery", "temple")):
        return (
            "fortified multi-level structure expedition",
            "экспедиция в укреплённую многоуровневую структуру",
            "entry and fallback points, floor-by-floor clearing, ranged and fall hazards, locked or trapped rooms, first-clear evidence, unique chest handling and a controlled exit without bypassing progression doors",
            "точки входа и отхода, зачистку по этажам, дальние угрозы и падения, закрытые или ловушечные комнаты, доказательство первой зачистки, обработку уникальных сундуков и контролируемый выход без обхода прогрессионных дверей",
        )
    if any(token in path for token in ("village", "inn", "market", "house", "settlement")):
        return (
            "inhabited or abandoned settlement expedition",
            "экспедиция в обитаемое или заброшенное поселение",
            "non-hostile entity safety, fire and collateral-damage rules, room search plan, loot ownership, hidden-spawner checks, evacuation route and confirmation that the settlement is not stripped before required encounters are completed",
            "безопасность мирных сущностей, правила огня и побочного ущерба, план осмотра помещений, владение лутом, проверку скрытых спавнеров, маршрут эвакуации и запрет разграбления до завершения обязательных встреч",
        )
    if any(token in path for token in ("arena", "typhon", "ceryneian", "boss", "colosseum")):
        return (
            "named encounter or arena expedition",
            "экспедиция к именованной встрече или арене",
            "arena boundary, boss or elite triggers, first-victory evidence, retreat threshold, add control, unique-drop protection, post-fight cleanup and prevention of automation replacing the initial encounter",
            "границу арены, триггеры босса или элиты, доказательство первой победы, порог отступления, контроль прислужников, защиту уникального лута, очистку после боя и запрет замены первой встречи автоматизацией",
        )
    return (
        "prepared structure-discovery expedition",
        "подготовленная экспедиция по обнаружению структуры",
        "location evidence, approach route, supply and cargo reserve, expected hazards, retreat criteria, first-clear proof, unique-loot custody and post-expedition recovery",
        "доказательство обнаружения, маршрут подхода, запас снабжения и груза, ожидаемые угрозы, критерии отступления, доказательство первой зачистки, хранение уникального лута и восстановление после экспедиции",
    )


def localized_content(qid: str, advancement: str | None) -> dict[str, tuple[str, list[str]]]:
    display = humanize(advancement or f"expedition_{qid[-4:]}")
    role_en, role_ru, focus_en, focus_ru = focus_for(advancement)
    return {
        "en_us": (
            f"{display} — Expedition Acceptance",
            [
                f"{display} is a {role_en} in the When Dungeons Arise branch. Discovery alone is not mastery: the expedition must have a prepared approach, bounded objective, first-clear evidence and a safe extraction plan instead of being subsidized by random loot or experience rewards.",
                f"Acceptance: verify {focus_en}; document equipment and supplies, enter through a legitimate route, complete the representative encounter or search objective, test one retreat or interrupted state, reconcile ordinary and unique loot and confirm that teleportation, structure breaking, rerolls and automated farming cannot replace the first expedition.",
            ],
        ),
        "ru_ru": (
            f"{display} — приёмка экспедиции",
            [
                f"{display} — {role_ru} ветви When Dungeons Arise. Одного обнаружения недостаточно: экспедиция должна иметь подготовленный подход, ограниченную цель, доказательство первой зачистки и безопасный план эвакуации вместо субсидирования случайным лутом или опытом из наград.",
                f"Приёмка: проверьте {focus_ru}; задокументируйте снаряжение и запасы, войдите честным маршрутом, выполните показательную встречу или цель поиска, испытайте одно отступление либо прерывание, сверьте обычный и уникальный лут и исключите замену первой экспедиции телепортацией, разрушением структуры, перероллом и автоматическим фармом.",
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
        advancement = advancement_id(block)
        block, removed = common.remove_rewards(block)
        rewards_removed += int(removed)
        block, added = common.add_acceptance_task(block, qid, "wda_expedition_acceptance")
        tasks_added += int(added)
        replacements.append((start, end, block))
        for locale, (title, desc) in localized_content(qid, advancement).items():
            localization[locale][f"quest.{qid}.title"] = title
            localization[locale][f"quest.{qid}.quest_desc"] = desc

    for start, end, block in reversed(replacements):
        text = text[:start] + block + text[end:]
    CHAPTER_PATH.write_text(text, encoding="utf-8", newline="\n")

    localization["en_us"][f"chapter.{CHAPTER_ID}.title"] = "When Dungeons Arise — Prepared Expeditions"
    localization["ru_ru"][f"chapter.{CHAPTER_ID}.title"] = "When Dungeons Arise — подготовленные экспедиции"
    for locale, entries in localization.items():
        path = common.LANG_DIR / f"{locale}.snbt"
        original = path.read_text(encoding="utf-8")
        merged = merge_entries(original, entries)
        if merged != original:
            path.write_text(merged, encoding="utf-8", newline="\n")

    print("catalog: when_dungeons_arise")
    print(f"quests: {len(spans)}")
    print(f"rewards_removed: {rewards_removed}")
    print(f"acceptance_tasks_added: {tasks_added}")


def gate() -> int:
    chapter = CHAPTER_PATH.read_text(encoding="utf-8")
    en = common.parse_localization(common.LANG_DIR / "en_us.snbt")
    ru = common.parse_localization(common.LANG_DIR / "ru_ru.snbt")
    spans = quest_spans(chapter)
    failures: list[str] = []
    rows: list[tuple[str, str, int, int, bool, str]] = []

    if len(spans) != EXPECTED_QUESTS:
        failures.append(f"Expected {EXPECTED_QUESTS} quests, found {len(spans)}")
    for start, end in spans:
        block = chapter[start:end]
        qid = quest_id(block)
        adv = advancement_id(block) or f"checkpoint:{qid}"
        types = common.task_types(block)
        en_len = common.visible_length(en.get(f"quest.{qid}.quest_desc", ""))
        ru_len = common.visible_length(ru.get(f"quest.{qid}.quest_desc", ""))
        no_rewards = "rewards:" not in block
        status = "PASS"
        if "checkmark" not in types:
            failures.append(f"{adv}: no practical acceptance task")
            status = "FAIL"
        if not no_rewards:
            failures.append(f"{adv}: reward remains")
            status = "FAIL"
        if en_len < MINIMUM_DESCRIPTION or ru_len < MINIMUM_DESCRIPTION:
            failures.append(f"{adv}: description too short (EN {en_len}, RU {ru_len})")
            status = "FAIL"
        rows.append((adv, qid, en_len, ru_len, no_rewards, status))

    lines = [
        "# When Dungeons Arise Expedition Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "Every structure discovery must include practical expedition acceptance, complete RU/EN operational guidance and no XP, item, random or loot rewards.",
        "",
        "| Structure/advancement | Quest | EN description | RU description | No rewards | Status |",
        "|---|---|---:|---:|---|---|",
    ]
    for adv, qid, en_len, ru_len, no_rewards, status in rows:
        lines.append(f"| `{adv}` | `{qid}` | {en_len} | {ru_len} | {'yes' if no_rewards else 'no'} | {status} |")
    lines.extend([
        "",
        "## Aggregate",
        "",
        f"- Quests: **{len(rows)}**",
        f"- Reward-free: **{sum(row[4] for row in rows)}**",
        f"- Fully bilingual: **{sum(row[2] >= MINIMUM_DESCRIPTION and row[3] >= MINIMUM_DESCRIPTION for row in rows)}**",
        f"- Failures: **{len(failures)}**",
        "",
    ])
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"wda_expedition_quality: {'PASS' if not failures else 'FAIL'}")
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
