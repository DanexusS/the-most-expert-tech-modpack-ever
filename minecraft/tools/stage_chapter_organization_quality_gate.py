from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import generate_early_stage_workflow_expansions as workflow
import generate_progression_spine as spine
import generate_stage_project_matrix as matrix
from catalog_upgrade_common import (
    extract_array,
    parse_localization,
    quest_identity,
    quest_spans,
    task_types,
    visible_length,
)
from manual_generator_common import stable_id

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
REPORT_PATH = ROOT / "docs" / "STAGE_CHAPTER_ORGANIZATION_QUALITY_REPORT.md"
MAIN_GROUP_ID = "F56B9C180F65BF60"
ANNEX_GROUP_ID = "99948FA76BB60233"
ANNEX_SLUGS = (
    "domain_map",
    "recipe_map",
    "alternative_architecture",
    "diagnostic_playbook",
    "capacity_scaling",
    "expert_extension",
)


def dependencies(block: str) -> list[str]:
    try:
        _, _, body = extract_array(block, "dependencies:")
    except RuntimeError:
        return []
    return re.findall(r'"([0-9A-F]{16})"', body)


def spine_ids(stage: dict) -> list[str]:
    return [
        stable_id(f"expert_progression_spine:{stage['id']}:{substage}:{lesson}")
        for substage in stage["substages"]
        for lesson, _, _ in spine.LESSON_TYPES
    ]


def matrix_ids(stage: dict) -> list[str]:
    return [
        matrix.stable_id(f"v1_stage_project:{stage['id']}:{lesson['slug']}")
        for lesson in matrix.LESSONS
    ]


def expected_main_dependencies(stage: dict, previous_final: str) -> dict[str, list[str]]:
    expected: dict[str, list[str]] = {}
    stage_spine = spine_ids(stage)
    for position, quest_id in enumerate(stage_spine):
        if position == 0:
            expected[quest_id] = [previous_final] if previous_final else []
        else:
            expected[quest_id] = [stage_spine[position - 1]]

    stage_workflow = workflow.workflow_quest_ids(stage["id"])
    if stage_workflow:
        expected.update(workflow.expected_dependencies(stage["id"], stage_spine[-1]))
        matrix_entry = workflow.workflow_final_id(stage["id"])
    else:
        matrix_entry = stage_spine[-1]

    stage_matrix = matrix_ids(stage)
    for position, quest_id in enumerate(stage_matrix):
        expected[quest_id] = [matrix_entry] if position == 0 else [stage_matrix[position - 1]]
    return expected


def validate_main_tasks(
    stage: dict,
    quest_id: str,
    block: str,
    stage_matrix: list[str],
    item_expectations: dict[str, list[str]],
    failures: list[str],
    label: str,
) -> bool:
    status = True
    types = task_types(block)
    item_count = types.count("item")
    check_count = types.count("checkmark")

    if quest_id == stage_matrix[-1]:
        if item_count != 1 or check_count != 1 or len(types) != 2:
            failures.append(
                f"{label}/{quest_id}: final certification must have milestone item and checkmark; found {types}"
            )
            status = False
        if stage["milestone"] not in block:
            failures.append(
                f"{label}/{quest_id}: final milestone {stage['milestone']} missing"
            )
            status = False
    elif quest_id in item_expectations:
        expected_items = item_expectations[quest_id]
        if item_count != len(expected_items) or check_count != 1 or len(types) != len(expected_items) + 1:
            failures.append(
                f"{label}/{quest_id}: expected {len(expected_items)} item task(s) plus one checkmark; found {types}"
            )
            status = False
        for item_id in expected_items:
            if item_id not in block:
                failures.append(f"{label}/{quest_id}: required workflow item {item_id} missing")
                status = False
    elif item_count != 0 or check_count != 1 or len(types) != 1:
        failures.append(
            f"{label}/{quest_id}: expected one practical checkmark task; found {types}"
        )
        status = False

    if "rewards:" in block:
        failures.append(f"{label}/{quest_id}: rewards are forbidden")
        status = False
    return status


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    stages = contract["stages"]
    en = parse_localization(LANG_DIR / "en_us.snbt")
    ru = parse_localization(LANG_DIR / "ru_ru.snbt")
    failures: list[str] = []
    rows: list[tuple[int, str, int, int, int, int, str]] = []
    all_main_ids: set[str] = set()
    all_annex_ids: set[str] = set()
    previous_final = ""

    if len(stages) != 18:
        failures.append(f"Expected 18 stages in contract, found {len(stages)}")

    for stage in stages:
        index = int(stage["index"])
        main_name = f"main_stage_{index:02d}_{stage['id']}"
        annex_name = f"stage_annex_{index:02d}_{stage['id']}"
        main_path = CHAPTER_DIR / f"{main_name}.snbt"
        annex_path = CHAPTER_DIR / f"{annex_name}.snbt"
        status = "PASS"

        if not main_path.is_file():
            failures.append(f"Missing main stage chapter {main_name}")
            rows.append((index, stage["id"], 0, 0, 0, 0, "FAIL"))
            continue
        if not annex_path.is_file():
            failures.append(f"Missing stage annex {annex_name}")
            status = "FAIL"

        main_text = main_path.read_text(encoding="utf-8")
        annex_text = annex_path.read_text(encoding="utf-8") if annex_path.is_file() else ""
        if f'group: "{MAIN_GROUP_ID}"' not in main_text:
            failures.append(f"{main_name}: wrong chapter group")
            status = "FAIL"
        if f'group: "{ANNEX_GROUP_ID}"' not in annex_text:
            failures.append(f"{annex_name}: wrong chapter group")
            status = "FAIL"

        main_spans = quest_spans(main_text)
        annex_spans = quest_spans(annex_text) if annex_text else []
        stage_spine = spine_ids(stage)
        stage_workflow = workflow.workflow_quest_ids(stage["id"])
        stage_matrix = matrix_ids(stage)
        expected_order = stage_spine + stage_workflow + stage_matrix
        if len(main_spans) != len(expected_order):
            failures.append(
                f"{main_name}: expected {len(expected_order)} quests, found {len(main_spans)}"
            )
            status = "FAIL"
        if len(annex_spans) != 6:
            failures.append(f"{annex_name}: expected 6 quests, found {len(annex_spans)}")
            status = "FAIL"

        blocks: dict[str, str] = {}
        actual_order: list[str] = []
        for start, end in main_spans:
            block = main_text[start:end]
            quest_id, _ = quest_identity(block)
            if quest_id in blocks or quest_id in all_main_ids or quest_id in all_annex_ids:
                failures.append(f"{main_name}: duplicate quest ID {quest_id}")
                status = "FAIL"
            blocks[quest_id] = block
            actual_order.append(quest_id)
            all_main_ids.add(quest_id)
        if actual_order != expected_order:
            failures.append(f"{main_name}: generated quest order does not match stage workflow contract")
            status = "FAIL"

        expected_deps = expected_main_dependencies(stage, previous_final)
        item_expectations = workflow.expected_item_tasks(stage["id"]) if stage_workflow else {}
        main_bilingual = 0
        for quest_id in expected_order:
            block = blocks.get(quest_id)
            if block is None:
                continue
            if dependencies(block) != expected_deps[quest_id]:
                failures.append(
                    f"{main_name}/{quest_id}: expected dependencies {expected_deps[quest_id]}, found {dependencies(block)}"
                )
                status = "FAIL"

            title_key = f"quest.{quest_id}.title"
            desc_key = f"quest.{quest_id}.quest_desc"
            en_len = visible_length(en.get(desc_key, ""))
            ru_len = visible_length(ru.get(desc_key, ""))
            minimum = 180 if quest_id in stage_workflow else 140
            if title_key in en and title_key in ru and en_len >= minimum and ru_len >= minimum:
                main_bilingual += 1
            else:
                failures.append(
                    f"{main_name}/{quest_id}: incomplete RU/EN content (EN {en_len}, RU {ru_len}; minimum {minimum})"
                )
                status = "FAIL"

            if not validate_main_tasks(
                stage,
                quest_id,
                block,
                stage_matrix,
                item_expectations,
                failures,
                main_name,
            ):
                status = "FAIL"

        annex_bilingual = 0
        annex_ids: list[str] = []
        entry_id = stage_spine[0]
        for position, (start, end) in enumerate(annex_spans):
            block = annex_text[start:end]
            quest_id, _ = quest_identity(block)
            expected_id = stable_id(f"stage_annex:{stage['id']}:{ANNEX_SLUGS[position]}")
            if quest_id != expected_id:
                failures.append(
                    f"{annex_name}: position {position} expected {expected_id}, found {quest_id}"
                )
                status = "FAIL"
            if quest_id in all_main_ids or quest_id in all_annex_ids:
                failures.append(f"{annex_name}: duplicate quest ID {quest_id}")
                status = "FAIL"
            all_annex_ids.add(quest_id)
            annex_ids.append(quest_id)
            expected_dependency = entry_id if position == 0 else annex_ids[position - 1]
            if dependencies(block) != [expected_dependency]:
                failures.append(
                    f"{annex_name}/{quest_id}: expected dependency {expected_dependency}"
                )
                status = "FAIL"
            if "optional: true" not in block:
                failures.append(f"{annex_name}/{quest_id}: annex quest must be optional")
                status = "FAIL"
            if task_types(block) != ["checkmark"]:
                failures.append(f"{annex_name}/{quest_id}: expected one checkmark task")
                status = "FAIL"
            if "rewards:" in block:
                failures.append(f"{annex_name}/{quest_id}: rewards are forbidden")
                status = "FAIL"
            title_key = f"quest.{quest_id}.title"
            desc_key = f"quest.{quest_id}.quest_desc"
            en_len = visible_length(en.get(desc_key, ""))
            ru_len = visible_length(ru.get(desc_key, ""))
            if title_key in en and title_key in ru and en_len >= 220 and ru_len >= 220:
                annex_bilingual += 1
            else:
                failures.append(
                    f"{annex_name}/{quest_id}: incomplete RU/EN content (EN {en_len}, RU {ru_len})"
                )
                status = "FAIL"

        previous_final = stage_matrix[-1]
        rows.append(
            (
                index,
                stage["id"],
                len(main_spans),
                main_bilingual,
                len(annex_spans),
                annex_bilingual,
                status,
            )
        )

    for path in (
        CHAPTER_DIR / "expert_progression_spine.snbt",
        CHAPTER_DIR / "v1_stage_project_matrix.snbt",
    ):
        if path.exists():
            failures.append(f"Legacy monolithic chapter still exists: {path.name}")

    lines = [
        "# Stage Chapter Organization Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "The mandatory route is split into one chapter per stage. Stages 1–4 additionally require branched component production, first-batch proof, automation, measured optimization and recovery before stage certification.",
        "",
        "| Stage | ID | Main quests | Main bilingual | Annex quests | Annex bilingual | Status |",
        "|---:|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row[0]} | `{row[1]}` | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} |"
        )
    lines.extend(
        [
            "",
            "## Aggregate",
            "",
            f"- Main stage chapters: **{sum(row[2] > 0 for row in rows)} / 18**",
            f"- Mandatory stage quests: **{sum(row[2] for row in rows)}**",
            f"- Expanded workflow stages: **{sum(row[1] in workflow.expanded_stage_ids() for row in rows)} / {len(workflow.expanded_stage_ids())}**",
            f"- Required workflow quests: **{sum(len(workflow.workflow_quest_ids(row[1])) for row in rows)}**",
            f"- Optional annex chapters: **{sum(row[4] > 0 for row in rows)} / 18**",
            f"- Optional annex quests: **{sum(row[4] for row in rows)}**",
            f"- Unique organized quest IDs: **{len(all_main_ids) + len(all_annex_ids)}**",
            f"- Failures: **{len(failures)}**",
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"stage_chapter_organization: {'PASS' if not failures else 'FAIL'}")
    print(f"main_chapters: {sum(row[2] > 0 for row in rows)}")
    print(f"main_quests: {sum(row[2] for row in rows)}")
    print(f"expanded_stages: {sum(row[1] in workflow.expanded_stage_ids() for row in rows)}")
    print(f"annex_chapters: {sum(row[4] > 0 for row in rows)}")
    print(f"annex_quests: {sum(row[4] for row in rows)}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
