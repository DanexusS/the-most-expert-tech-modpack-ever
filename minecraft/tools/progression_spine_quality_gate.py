from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from generate_progression_spine import (
    CHAPTER_PATH,
    CONTRACT_PATH,
    FILENAME,
    LANG_DIR,
    LESSON_TYPES,
)
from manual_generator_common import stable_id
from quest_quality_audit import extract_array, parse_localization, text_length, top_level_objects

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "PROGRESSION_SPINE_QUALITY_REPORT.md"


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    chapter = CHAPTER_PATH.read_text(encoding="utf-8")
    en = parse_localization(LANG_DIR / "en_us.snbt")
    ru = parse_localization(LANG_DIR / "ru_ru.snbt")
    quest_blocks = top_level_objects(extract_array(chapter, "quests:"))
    by_id: dict[str, str] = {}
    failures: list[str] = []

    for block in quest_blocks:
        match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
        if not match:
            failures.append("Quest block without a valid ID")
            continue
        quest_id = match.group(1)
        if quest_id in by_id:
            failures.append(f"Duplicate quest ID {quest_id}")
        by_id[quest_id] = block

    expected_quests = sum(len(stage["substages"]) * len(LESSON_TYPES) for stage in contract["stages"])
    if len(quest_blocks) != expected_quests:
        failures.append(f"Expected {expected_quests} progression-spine quests, found {len(quest_blocks)}")

    dependency_total = 0
    bilingual = 0
    long_descriptions = 0
    reward_free = 0
    milestone_checks = 0
    previous_id = ""
    rows: list[tuple[int, str, str, str, str]] = []

    for stage in contract["stages"]:
        stage_status = "PASS"
        stage_quest_count = 0
        stage_bilingual = 0
        final_id = ""
        for sub_index, substage in enumerate(stage["substages"]):
            for lesson, _, _ in LESSON_TYPES:
                quest_id = stable_id(f"{FILENAME}:{stage['id']}:{substage}:{lesson}")
                final_id = quest_id
                stage_quest_count += 1
                block = by_id.get(quest_id)
                if block is None:
                    failures.append(f"Missing {stage['id']} / {substage} / {lesson}: {quest_id}")
                    stage_status = "FAIL"
                    continue

                dependencies = re.findall(r'"([0-9A-F]{16})"', extract_array(block, "dependencies:"))
                dependency_total += len(dependencies)
                if previous_id:
                    if dependencies != [previous_id]:
                        failures.append(
                            f"{quest_id}: expected dependency {previous_id}, found {dependencies}"
                        )
                        stage_status = "FAIL"
                elif dependencies:
                    failures.append(f"First quest {quest_id} must not have dependencies")
                    stage_status = "FAIL"

                if "rewards:" in block:
                    failures.append(f"{quest_id}: progression-spine quests may not have rewards")
                    stage_status = "FAIL"
                else:
                    reward_free += 1

                tasks = top_level_objects(extract_array(block, "tasks:"))
                task_types = re.findall(r'(?m)^\s*type:\s*"([a-z0-9_]+)"', extract_array(block, "tasks:"))
                if "checkmark" not in task_types:
                    failures.append(f"{quest_id}: missing acceptance checkmark")
                    stage_status = "FAIL"

                is_stage_final = sub_index == len(stage["substages"]) - 1 and lesson == "acceptance"
                milestone_mentions = sum(stage["milestone"] in task for task in tasks)
                if is_stage_final:
                    if "item" not in task_types or milestone_mentions != 1:
                        failures.append(
                            f"{quest_id}: final stage acceptance must require {stage['milestone']} exactly once"
                        )
                        stage_status = "FAIL"
                    else:
                        milestone_checks += 1
                elif milestone_mentions:
                    failures.append(
                        f"{quest_id}: milestone item must be required only by final stage acceptance"
                    )
                    stage_status = "FAIL"

                title_key = f"quest.{quest_id}.title"
                desc_key = f"quest.{quest_id}.quest_desc"
                en_length = text_length(en.get(desc_key, ""))
                ru_length = text_length(ru.get(desc_key, ""))
                if title_key in en and title_key in ru and en_length > 0 and ru_length > 0:
                    bilingual += 1
                    stage_bilingual += 1
                else:
                    failures.append(f"{quest_id}: missing bilingual title or description")
                    stage_status = "FAIL"
                if en_length >= 180 and ru_length >= 180:
                    long_descriptions += 1
                else:
                    failures.append(
                        f"{quest_id}: description too short (EN {en_length}, RU {ru_length}; minimum 180)"
                    )
                    stage_status = "FAIL"

                previous_id = quest_id

        rows.append(
            (
                int(stage["index"]),
                stage["title_en"],
                str(stage_quest_count),
                str(stage_bilingual),
                stage_status,
            )
        )

    if dependency_total != max(0, expected_quests - 1):
        failures.append(
            f"Expected {expected_quests - 1} dependency edges, found {dependency_total}"
        )
    if milestone_checks != len(contract["stages"]):
        failures.append(
            f"Expected {len(contract['stages'])} final milestone checks, found {milestone_checks}"
        )

    lines = [
        "# Progression Spine Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "The progression spine converts the 18-stage contract and 72 mandatory substages into a single dependency path. Every substage contains system theory, infrastructure construction and production acceptance.",
        "",
        "| Stage | Title | Quests | Bilingual | Status |",
        "|---:|---|---:|---:|---|",
    ]
    for index, title, quests, stage_bilingual, status in rows:
        lines.append(f"| {index} | {title} | {quests} | {stage_bilingual} | {status} |")
    lines.extend([
        "",
        "## Aggregate",
        "",
        f"- Stages: **{len(contract['stages'])}**",
        f"- Substages: **{sum(len(stage['substages']) for stage in contract['stages'])}**",
        f"- Quests: **{len(quest_blocks)}**",
        f"- Dependency edges: **{dependency_total}**",
        f"- Reward-free quests: **{reward_free}**",
        f"- Fully bilingual quests: **{bilingual}**",
        f"- Descriptions at least 180 characters in both languages: **{long_descriptions}**",
        f"- Final milestone item checks: **{milestone_checks}**",
        f"- Failures: **{len(failures)}**",
        "",
    ])
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"progression_spine_quality: {'PASS' if not failures else 'FAIL'}")
    print(f"quests: {len(quest_blocks)}")
    print(f"dependencies: {dependency_total}")
    print(f"bilingual: {bilingual}")
    print(f"milestone_checks: {milestone_checks}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
