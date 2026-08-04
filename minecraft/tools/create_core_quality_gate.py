from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "create.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
REPORT_PATH = ROOT / "docs" / "CREATE_CORE_QUALITY_REPORT.md"

FOCUS_QUESTS = {
    "4BB13C80196FD034": "Andesite supply",
    "0E5FC39E6C71A872": "Shaft power path",
    "4B976C143EDA4317": "Andesite casing batch",
    "1837076B0EA3C11A": "Belt logistics",
    "4266BF7FCE3B4330": "Cogwheel ratios",
    "4C7CD3858A2BE870": "Mechanical press",
    "1D00D782B8F0B6D6": "Mechanical mixer",
    "732D1A96512F2BFD": "Steam capacity",
    "19754AE8C11A6317": "Deployer control",
    "0EE2E9EB6DC01E34": "Precision mechanism",
    "61348E2551E8AD6C": "Speed controller",
    "197AB0E07A40512F": "Water-wheel generation",
    "51CCB7ACFD7B45F1": "Brass casing",
}


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


def quest_block(text: str, quest_id: str) -> str:
    marker = f'\n\t\t\tid: "{quest_id}"'
    marker_index = text.find(marker)
    if marker_index < 0:
        raise RuntimeError(f"Create focus quest not found: {quest_id}")
    start = text.rfind("\n\t\t{", 0, marker_index)
    if start < 0:
        raise RuntimeError(f"Create focus quest object start not found: {quest_id}")
    start += 1
    end = matching_delimiter(text, start, "{", "}")
    return text[start : end + 1]


def task_count(block: str) -> int:
    marker = block.find("tasks:")
    if marker < 0:
        return 0
    start = block.find("[", marker)
    end = matching_delimiter(block, start, "[", "]")
    body = block[start + 1 : end]
    count = 0
    depth = 0
    in_string = False
    escaped = False
    quote = ""
    for char in body:
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
        elif char == "{":
            if depth == 0:
                count += 1
            depth += 1
        elif char == "}":
            depth -= 1
    return count


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

    for quest_id, label in FOCUS_QUESTS.items():
        tasks = task_count(quest_block(chapter, quest_id))
        en_title = localization_value(en, f"quest.{quest_id}.title")
        ru_title = localization_value(ru, f"quest.{quest_id}.title")
        en_length = visible_length(localization_value(en, f"quest.{quest_id}.quest_desc"))
        ru_length = visible_length(localization_value(ru, f"quest.{quest_id}.quest_desc"))
        status = "PASS"
        if tasks < 2:
            failures.append(f"{quest_id}: expected item task plus acceptance task")
            status = "FAIL"
        if not en_title or not ru_title:
            failures.append(f"{quest_id}: missing bilingual title")
            status = "FAIL"
        if en_length < 80 or ru_length < 80:
            failures.append(f"{quest_id}: description shorter than 80 characters")
            status = "FAIL"
        rows.append((quest_id, label, tasks, en_length, ru_length, status))

    lines = [
        "# Create Core Quality Report",
        "",
        "This report covers the deliberately redesigned critical route inside the legacy `create` chapter.",
        "",
        "| Quest | Purpose | Tasks | EN description | RU description | Status |",
        "|---|---|---:|---:|---:|---|",
    ]
    for quest_id, label, tasks, en_length, ru_length, status in rows:
        lines.append(f"| `{quest_id}` | {label} | {tasks} | {en_length} | {ru_length} | {status} |")
    lines.extend(["", "## Result", ""])
    if failures:
        lines.append("**FAIL**")
        lines.extend(f"- {failure}" for failure in failures)
    else:
        lines.append("**PASS** — all thirteen Create core-route quests have production acceptance and bilingual guidance.")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"create_core_quality: {'FAIL' if failures else 'PASS'}")
    print(f"focus_quests: {len(rows)}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
