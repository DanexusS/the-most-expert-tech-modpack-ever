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


def quest_spans(text: str) -> list[tuple[int, int]]:
    marker = text.find("quests:")
    if marker < 0:
        raise RuntimeError("Project matrix has no quests list")
    list_start = text.find("[", marker)
    list_end = matching_delimiter(text, list_start, "[", "]")
    spans: list[tuple[int, int]] = []
    cursor = list_start + 1
    while cursor < list_end:
        start = text.find("{", cursor, list_end)
        if start < 0:
            break
        end = matching_delimiter(text, start, "{", "}")
        spans.append((start, end + 1))
        cursor = end + 1
    return spans


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

    expected_total = len(stages) * len(LESSONS)
    spans = quest_spans(chapter)
    if len(stages) != 18:
        failures.append(f"Expected 18 stages, found {len(stages)}")
    if len(spans) != expected_total:
        failures.append(f"Expected {expected_total} quests, found {len(spans)}")
    if f'id: "{CHAPTER_ID}"' not in chapter:
        failures.append("Chapter ID does not match the v1 project matrix contract")

    expected_ids: list[tuple[dict, dict, str]] = []
    for stage in stages:
        for lesson in LESSONS:
            expected_ids.append((stage, lesson, stable_id(f"v1_stage_project:{stage['id']}:{lesson['slug']}")))

    previous_id = ""
    for position, (stage, lesson, expected_id) in enumerate(expected_ids):
        if position >= len(spans):
            break
        start, end = spans[position]
        block = chapter[start:end]
        quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
        quest_id = quest_match.group(1) if quest_match else ""
        status = "PASS"
        if quest_id != expected_id:
            failures.append(f"Position {position}: expected quest {expected_id}, found {quest_id or 'missing'}")
            status = "FAIL"

        dependencies = re.findall(r'dependencies:\s*\[\s*"([0-9A-F]{16})"\s*\]', block)
        expected_dependencies = [] if not previous_id else [previous_id]
        if dependencies != expected_dependencies:
            failures.append(
                f"{expected_id}: expected dependencies {expected_dependencies}, found {dependencies}"
            )
            status = "FAIL"

        task_types = re.findall(r'(?m)^\s*type:\s*"([a-z0-9_]+)"', block)
        expected_item_tasks = 1 if lesson.get("milestone_task") else 0
        if task_types.count("checkmark") != 1 or task_types.count("item") != expected_item_tasks:
            failures.append(
                f"{expected_id}: expected one checkmark and {expected_item_tasks} item tasks, found {task_types}"
            )
            status = "FAIL"
        if "rewards:" in block:
            failures.append(f"{expected_id}: project quest contains rewards")
            status = "FAIL"

        if lesson.get("milestone_task") and f'id: "{stage["milestone"]}"' not in block:
            failures.append(f"{expected_id}: final stage quest does not require {stage['milestone']}")
            status = "FAIL"

        title_key = f"quest.{expected_id}.title"
        desc_key = f"quest.{expected_id}.quest_desc"
        en_length = visible_length(en.get(desc_key, ""))
        ru_length = visible_length(ru.get(desc_key, ""))
        if title_key not in en or title_key not in ru:
            failures.append(f"{expected_id}: missing bilingual title")
            status = "FAIL"
        if en_length < 190 or ru_length < 190:
            failures.append(
                f"{expected_id}: project explanation too short (EN {en_length}, RU {ru_length})"
            )
            status = "FAIL"

        rows.append((int(stage["index"]), lesson["slug"], len(task_types), en_length, ru_length, status))
        previous_id = expected_id

    lines = [
        "# Stage Project Matrix Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "The project matrix is the practical main route: ten ordered engineering checks for each of eighteen progression stages.",
        "",
        "## Summary",
        "",
        f"- Progression stages: **{len(stages)}**",
        f"- Project quests: **{len(spans)}**",
        f"- Expected linear quests: **{expected_total}**",
        f"- Final milestone acceptance quests: **{sum(bool(lesson.get('milestone_task')) for _, lesson, _ in expected_ids)}**",
        f"- Reward-bearing project quests: **{sum('rewards:' in chapter[start:end] for start, end in spans)}**",
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
    print(f"quests: {len(spans)}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
