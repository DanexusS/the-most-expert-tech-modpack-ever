from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from generate_stage_project_matrix import (
    CHAPTER_ID,
    CHAPTER_PATH,
    CONTRACT_PATH,
    LANG_DIR,
    LESSONS,
    stable_id,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "STAGE_PROJECT_MATRIX_QUALITY_REPORT.md"
KEY_RE = re.compile(r"(?m)^\t([A-Za-z0-9_.-]+):")


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
    raise RuntimeError(f"Unclosed delimiter at {start}")


def quest_blocks(text: str) -> dict[str, str]:
    marker = text.find("quests:")
    if marker < 0:
        raise RuntimeError("Project matrix has no quests list")
    list_start = text.find("[", marker)
    list_end = matching_delimiter(text, list_start, "[", "]")
    blocks: dict[str, str] = {}
    cursor = list_start + 1
    while cursor < list_end:
        start = text.find("{", cursor, list_end)
        if start < 0:
            break
        end = matching_delimiter(text, start, "{", "}")
        block = text[start : end + 1]
        match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
        if not match:
            raise RuntimeError(f"Top-level quest block at offset {start} has no ID")
        quest_id = match.group(1)
        if quest_id in blocks:
            raise RuntimeError(f"Duplicate top-level quest ID {quest_id}")
        blocks[quest_id] = block
        cursor = end + 1
    return blocks


def parse_localization(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    matches = list(KEY_RE.finditer(text))
    values: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else text.rfind("}")
        values[match.group(1)] = text[start:end].strip()
    return values


def visible_length(raw: str) -> int:
    return len(" ".join(re.findall(r'"((?:\\.|[^"\\])*)"', raw)))


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    stages = contract["stages"]
    chapter = CHAPTER_PATH.read_text(encoding="utf-8")
    en = parse_localization(LANG_DIR / "en_us.snbt")
    ru = parse_localization(LANG_DIR / "ru_ru.snbt")
    failures: list[str] = []
    rows: list[tuple[int, str, int, int, int, str]] = []

    expected: list[tuple[dict, dict, str, str]] = []
    previous_id = ""
    for stage in stages:
        for lesson in LESSONS:
            quest_id = stable_id(f"v1_stage_project:{stage['id']}:{lesson['slug']}")
            expected.append((stage, lesson, quest_id, previous_id))
            previous_id = quest_id

    try:
        blocks = quest_blocks(chapter)
    except RuntimeError as error:
        blocks = {}
        failures.append(str(error))

    expected_ids = {quest_id for _, _, quest_id, _ in expected}
    extra_ids = sorted(set(blocks) - expected_ids)
    missing_ids = sorted(expected_ids - set(blocks))
    if len(stages) != 18:
        failures.append(f"Expected 18 stages, found {len(stages)}")
    if len(expected) != 180:
        failures.append(f"Expected contract to define 180 quests, found {len(expected)}")
    if len(blocks) != 180:
        failures.append(f"Expected 180 top-level quest blocks, found {len(blocks)}")
    if extra_ids:
        failures.append("Unexpected project quest IDs: " + ", ".join(extra_ids))
    if missing_ids:
        failures.append("Missing project quest IDs: " + ", ".join(missing_ids))
    if f'id: "{CHAPTER_ID}"' not in chapter:
        failures.append("Chapter ID does not match the v1 project matrix contract")

    for stage, lesson, quest_id, previous_id in expected:
        block = blocks.get(quest_id, "")
        status = "PASS"
        if not block:
            rows.append((int(stage["index"]), lesson["slug"], 0, 0, 0, "FAIL"))
            continue

        dependencies = set(re.findall(r'"([0-9A-F]{16})"', re.search(r'dependencies:\s*\[(.*?)\]', block, re.S).group(1))) if "dependencies:" in block else set()
        required_dependencies = set() if not previous_id else {previous_id}
        if not required_dependencies.issubset(dependencies):
            failures.append(
                f"{quest_id}: missing required previous quest dependency {previous_id or 'none'}"
            )
            status = "FAIL"

        task_types = re.findall(r'(?m)^\s*type:\s*"([a-z0-9_]+)"', block)
        expected_item_tasks = 1 if lesson.get("milestone_task") else 0
        if task_types.count("checkmark") != 1 or task_types.count("item") != expected_item_tasks:
            failures.append(
                f"{quest_id}: expected one checkmark and {expected_item_tasks} item tasks, found {task_types}"
            )
            status = "FAIL"
        if "rewards:" in block:
            failures.append(f"{quest_id}: project quest contains rewards")
            status = "FAIL"
        if lesson.get("milestone_task") and f'id: "{stage["milestone"]}"' not in block:
            failures.append(f"{quest_id}: final stage quest does not require {stage['milestone']}")
            status = "FAIL"

        title_key = f"quest.{quest_id}.title"
        desc_key = f"quest.{quest_id}.quest_desc"
        en_length = visible_length(en.get(desc_key, ""))
        ru_length = visible_length(ru.get(desc_key, ""))
        if title_key not in en or title_key not in ru:
            failures.append(f"{quest_id}: missing bilingual title")
            status = "FAIL"
        if en_length < 170 or ru_length < 170:
            failures.append(
                f"{quest_id}: project explanation too short (EN {en_length}, RU {ru_length}; minimum 170)"
            )
            status = "FAIL"
        rows.append((int(stage["index"]), lesson["slug"], len(task_types), en_length, ru_length, status))

    lines = [
        "# Stage Project Matrix Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "The project matrix is the practical main route: ten ordered engineering checks for each of eighteen progression stages. Validation is based on stable quest IDs, not physical SNBT block order.",
        "",
        "## Summary",
        "",
        f"- Progression stages: **{len(stages)}**",
        f"- Expected project quests: **{len(expected)}**",
        f"- Parsed project quests: **{len(blocks)}**",
        f"- Final milestone acceptance quests: **{sum(bool(lesson.get('milestone_task')) for _, lesson, _, _ in expected)}**",
        f"- Reward-bearing project quests: **{sum('rewards:' in block for block in blocks.values())}**",
        f"- Failures: **{len(failures)}**",
        "",
        "| Stage | Check | Tasks | EN description | RU description | Status |",
        "|---:|---|---:|---:|---:|---|",
    ]
    for stage_index, slug, tasks, en_length, ru_length, status in rows:
        lines.append(f"| {stage_index} | `{slug}` | {tasks} | {en_length} | {ru_length} | {status} |")
    lines.append("")
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"stage_project_matrix: {'PASS' if not failures else 'FAIL'}")
    print(f"stages: {len(stages)}")
    print(f"quests: {len(blocks)}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
