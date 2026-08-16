from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
REPORT_PATH = ROOT / "docs" / "ALL_MANUAL_QUALITY_REPORT.md"
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
    raise RuntimeError(f"Unclosed delimiter {opening!r} at {start}")


def extract_array(text: str, marker: str) -> str:
    marker_index = text.find(marker)
    if marker_index < 0:
        return ""
    start = text.find("[", marker_index)
    if start < 0:
        return ""
    end = matching_delimiter(text, start, "[", "]")
    return text[start + 1 : end]


def top_level_objects(body: str) -> list[str]:
    result: list[str] = []
    index = 0
    while index < len(body):
        start = body.find("{", index)
        if start < 0:
            break
        end = matching_delimiter(body, start, "{", "}")
        result.append(body[start : end + 1])
        index = end + 1
    return result


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
    en = parse_localization(LANG_DIR / "en_us.snbt")
    ru = parse_localization(LANG_DIR / "ru_ru.snbt")
    paths = sorted(CHAPTER_DIR.glob("core_technology_manual_*.snbt"))
    failures: list[str] = []
    rows: list[tuple[str, int, int, int, int, int, str]] = []
    global_ids: set[str] = set()

    if not paths:
        failures.append("No curated manual chapters found")

    for path in paths:
        filename = path.stem
        suffix = filename.rsplit("_", 1)[-1]
        expected = 60 if suffix == "1" else 50
        text = path.read_text(encoding="utf-8")
        quest_objects = top_level_objects(extract_array(text, "quests:"))
        quest_ids: list[str] = []
        dependency_ids: list[str] = []
        roots = 0
        bilingual = 0
        minimum_description = 10**9
        status = "PASS"

        if len(quest_objects) != expected:
            failures.append(f"{filename}: expected {expected} quests, found {len(quest_objects)}")
            status = "FAIL"

        for block in quest_objects:
            quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
            if not quest_match:
                failures.append(f"{filename}: quest without valid ID")
                status = "FAIL"
                continue
            quest_id = quest_match.group(1)
            quest_ids.append(quest_id)
            if quest_id in global_ids:
                failures.append(f"{filename}: duplicate quest ID {quest_id}")
                status = "FAIL"
            global_ids.add(quest_id)

            dependencies = re.findall(r'"([0-9A-F]{16})"', extract_array(block, "dependencies:"))
            dependency_ids.extend(dependencies)
            if not dependencies:
                roots += 1
            elif len(dependencies) != 1:
                failures.append(f"{filename}/{quest_id}: expected one module-chain dependency")
                status = "FAIL"

            task_body = extract_array(block, "tasks:")
            tasks = top_level_objects(task_body)
            task_types = re.findall(r'(?m)^\s*type:\s*"([a-z0-9_]+)"', task_body)
            if len(tasks) != 1 or task_types != ["checkmark"]:
                failures.append(f"{filename}/{quest_id}: expected one checkmark task")
                status = "FAIL"
            if "rewards:" in block:
                failures.append(f"{filename}/{quest_id}: curated lesson must not contain rewards")
                status = "FAIL"

            title_key = f"quest.{quest_id}.title"
            desc_key = f"quest.{quest_id}.quest_desc"
            en_length = visible_length(en.get(desc_key, ""))
            ru_length = visible_length(ru.get(desc_key, ""))
            minimum_description = min(minimum_description, en_length, ru_length)
            if title_key in en and title_key in ru and en_length >= 140 and ru_length >= 140:
                bilingual += 1
            else:
                failures.append(f"{filename}/{quest_id}: incomplete RU/EN explanation")
                status = "FAIL"

        missing = sorted(set(dependency_ids) - set(quest_ids))
        if missing:
            failures.append(f"{filename}: missing dependency targets {missing}")
            status = "FAIL"
        if roots != 5:
            failures.append(f"{filename}: expected five module roots, found {roots}")
            status = "FAIL"
        rows.append(
            (
                filename,
                len(quest_objects),
                roots,
                len(dependency_ids),
                bilingual,
                0 if minimum_description == 10**9 else minimum_description,
                status,
            )
        )

    lines = [
        "# All Curated Manuals Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "| Manual | Quests | Module roots | Dependencies | Bilingual | Min description | Status |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row[0]}` | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} |"
        )
    lines.extend([
        "",
        "## Aggregate",
        "",
        f"- Manual chapters: **{len(rows)}**",
        f"- Verified lessons: **{sum(row[1] for row in rows)}**",
        f"- Fully bilingual lessons: **{sum(row[4] for row in rows)}**",
        f"- Failures: **{len(failures)}**",
        "",
    ])
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"all_manual_quality: {'PASS' if not failures else 'FAIL'}")
    print(f"manuals: {len(rows)}")
    print(f"lessons: {sum(row[1] for row in rows)}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
