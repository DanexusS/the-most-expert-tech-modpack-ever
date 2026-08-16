from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import generate_early_stage_workflow_expansions as workflow
import generate_stage_depth_program as depth
import generate_stage_project_matrix as matrix
from catalog_upgrade_common import (
    parse_localization,
    quest_identity,
    quest_spans,
    task_types,
    visible_length,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
REPORT_PATH = ROOT / "docs" / "STAGE_DEPTH_PROGRAM_QUALITY_REPORT.md"


def dependencies(block: str) -> list[str]:
    match = re.search(r"(?m)^\s*dependencies:\s*\[([^\]]*)\]", block)
    if match is None:
        return []
    return re.findall(r'"([0-9A-F]{16})"', match.group(1))


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    workflow_profiles = depth.merged_workflow_profiles()
    en = parse_localization(LANG_DIR / "en_us.snbt")
    ru = parse_localization(LANG_DIR / "ru_ru.snbt")
    failures: list[str] = []
    rows: list[tuple[int, str, int, int, int, str]] = []
    total_depth = 0
    total_optimization = 0

    for stage in contract["stages"]:
        stage_id = stage["id"]
        index = int(stage["index"])
        chapter_name = f"main_stage_{index:02d}_{stage_id}"
        path = CHAPTER_DIR / f"{chapter_name}.snbt"
        status = "PASS"
        if not path.is_file():
            failures.append(f"Missing chapter {chapter_name}")
            rows.append((index, stage_id, 0, 0, 0, "FAIL"))
            continue

        text = path.read_text(encoding="utf-8")
        spans = quest_spans(text)
        blocks: dict[str, str] = {}
        for start, end in spans:
            block = text[start:end]
            quest_id, _ = quest_identity(block)
            blocks[quest_id] = block

        if len(spans) != 121:
            failures.append(f"{chapter_name}: expected 121 mandatory quests, found {len(spans)}")
            status = "FAIL"

        expected_ids = depth.depth_quest_ids(stage_id)
        expected_deps = depth.expected_dependencies(
            stage_id, workflow.workflow_final_id(stage_id)
        )
        expected_items = depth.item_expectations(stage, workflow_profiles[stage_id])
        bilingual = 0
        present = 0

        for quest_id in expected_ids:
            block = blocks.get(quest_id)
            if block is None:
                failures.append(f"{chapter_name}: missing depth quest {quest_id}")
                status = "FAIL"
                continue
            present += 1
            total_depth += 1
            if quest_id in {
                depth.depth_id(stage_id, "performance_optimization", phase[0])
                for phase in depth.PHASES
            }:
                total_optimization += 1

            actual_deps = dependencies(block)
            if actual_deps != expected_deps[quest_id]:
                failures.append(
                    f"{chapter_name}/{quest_id}: expected dependencies {expected_deps[quest_id]}, found {actual_deps}"
                )
                status = "FAIL"

            title_key = f"quest.{quest_id}.title"
            desc_key = f"quest.{quest_id}.quest_desc"
            en_len = visible_length(en.get(desc_key, ""))
            ru_len = visible_length(ru.get(desc_key, ""))
            if title_key in en and title_key in ru and en_len >= 220 and ru_len >= 220:
                bilingual += 1
            else:
                failures.append(
                    f"{chapter_name}/{quest_id}: incomplete RU/EN depth text (EN {en_len}, RU {ru_len})"
                )
                status = "FAIL"

            expected_task_items = expected_items.get(quest_id, [])
            types = task_types(block)
            if types.count("item") != len(expected_task_items) or types.count("checkmark") != 1:
                failures.append(
                    f"{chapter_name}/{quest_id}: expected {len(expected_task_items)} item task(s) and one checkmark; found {types}"
                )
                status = "FAIL"
            if len(types) != len(expected_task_items) + 1:
                failures.append(f"{chapter_name}/{quest_id}: unexpected extra tasks {types}")
                status = "FAIL"
            for item_id, count in expected_task_items:
                if item_id not in block or f"count: {count}" not in block:
                    failures.append(
                        f"{chapter_name}/{quest_id}: missing item requirement {count}x {item_id}"
                    )
                    status = "FAIL"
            if "rewards:" in block:
                failures.append(f"{chapter_name}/{quest_id}: rewards are forbidden")
                status = "FAIL"

        matrix_entry = matrix.stable_id(
            f"v1_stage_project:{stage_id}:{matrix.LESSONS[0]['slug']}"
        )
        matrix_block = blocks.get(matrix_entry)
        if matrix_block is None:
            failures.append(f"{chapter_name}: missing stage project matrix entry")
            status = "FAIL"
        elif dependencies(matrix_block) != [depth.depth_final_id(stage_id)]:
            failures.append(
                f"{chapter_name}: final project matrix must depend on {depth.depth_final_id(stage_id)}"
            )
            status = "FAIL"

        rows.append((index, stage_id, present, bilingual, len(spans), status))

    lines = [
        "# Stage Depth Program Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "Every mandatory stage must contain a complete eighty-quest operational depth program in addition to its substage, workflow and certification quests.",
        "",
        "| Stage | ID | Depth quests | Bilingual depth | Total mandatory | Status |",
        "|---:|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row[0]} | `{row[1]}` | {row[2]} | {row[3]} | {row[4]} | {row[5]} |"
        )
    lines.extend(
        [
            "",
            "## Aggregate",
            "",
            f"- Stages at or above 100 mandatory quests: **{sum(row[4] >= 100 for row in rows)} / 18**",
            f"- Mandatory quests per complete stage: **121**",
            f"- Depth-program quests: **{total_depth} / 1440**",
            f"- Dedicated performance-optimization quests: **{total_optimization} / 180**",
            f"- Failures: **{len(failures)}**",
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"stage_depth_program: {'PASS' if not failures else 'FAIL'}")
    print(f"depth_quests: {total_depth}/1440")
    print(f"optimization_depth_quests: {total_optimization}/180")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
