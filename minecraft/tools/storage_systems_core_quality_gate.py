from __future__ import annotations

import re
import sys
from pathlib import Path

from upgrade_storage_systems_core import CHAPTER_PATH, FOCUS_ITEMS, quest_for_item

ROOT = Path(__file__).resolve().parents[1]
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
REPORT_PATH = ROOT / "docs" / "STORAGE_SYSTEMS_CORE_QUALITY_REPORT.md"


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


def task_count(block: str) -> int:
    marker = block.find("tasks:")
    if marker < 0:
        return 0
    start = block.find("[", marker)
    end = matching_delimiter(block, start, "[", "]")
    return len(re.findall(r'(?m)^\s*type:\s*"[a-z0-9_]+"', block[start:end]))


def localization_value(text: str, key: str) -> str:
    pattern = re.compile(rf"(?ms)^\t{re.escape(key)}:.*?(?=^\t[A-Za-z0-9_.-]+:|^\}}\s*$)")
    match = pattern.search(text)
    return match.group(0) if match else ""


def visible_length(raw: str) -> int:
    return len(" ".join(re.findall(r'"((?:\\.|[^"\\])*)"', raw)))


def main() -> int:
    chapter = CHAPTER_PATH.read_text(encoding="utf-8")
    en = (LANG_DIR / "en_us.snbt").read_text(encoding="utf-8")
    ru = (LANG_DIR / "ru_ru.snbt").read_text(encoding="utf-8")
    failures: list[str] = []
    rows: list[tuple[str, str, int, int, int, str]] = []

    for item_id in FOCUS_ITEMS:
        quest_id, start, end = quest_for_item(chapter, item_id)
        block = chapter[start : end + 1]
        tasks = task_count(block)
        en_title = localization_value(en, f"quest.{quest_id}.title")
        ru_title = localization_value(ru, f"quest.{quest_id}.title")
        en_length = visible_length(localization_value(en, f"quest.{quest_id}.quest_desc"))
        ru_length = visible_length(localization_value(ru, f"quest.{quest_id}.quest_desc"))
        status = "PASS"
        if tasks < 2:
            failures.append(f"{item_id}: expected item task plus acceptance task")
            status = "FAIL"
        if not en_title or not ru_title:
            failures.append(f"{item_id}: missing bilingual title")
            status = "FAIL"
        if en_length < 180 or ru_length < 180:
            failures.append(f"{item_id}: operational explanation shorter than 180 characters")
            status = "FAIL"
        rows.append((item_id, quest_id, tasks, en_length, ru_length, status))

    lines = [
        "# Storage Systems Core Quality Report",
        "",
        "This report covers the redesigned portable and stationary storage route in the legacy storage catalogue.",
        "",
        "| Item gate | Quest | Tasks | EN description | RU description | Status |",
        "|---|---|---:|---:|---:|---|",
    ]
    for item_id, quest_id, tasks, en_length, ru_length, status in rows:
        lines.append(f"| `{item_id}` | `{quest_id}` | {tasks} | {en_length} | {ru_length} | {status} |")
    lines.extend(["", "## Result", ""])
    if failures:
        lines.append("**FAIL**")
        lines.extend(f"- {failure}" for failure in failures)
    else:
        lines.append("**PASS** — selected storage quests require practical acceptance and include bilingual failure-oriented guidance.")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"storage_systems_core_quality: {'FAIL' if failures else 'PASS'}")
    print(f"focus_quests: {len(rows)}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
