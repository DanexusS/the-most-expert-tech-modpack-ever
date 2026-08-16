from __future__ import annotations

import re
import sys
from pathlib import Path

from upgrade_mystical_agriculture_catalog import (
    CHAPTER_PATH,
    LANG_DIR,
    acceptance_id,
    extract_array,
    quest_identity,
    quest_spans,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "MYSTICAL_AGRICULTURE_QUALITY_REPORT.md"
KEY_RE = re.compile(r"(?m)^\t([A-Za-z0-9_.-]+):")


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


def task_types(block: str) -> list[str]:
    _, _, body = extract_array(block, "tasks:")
    return re.findall(r'(?m)^\s*type:\s*"([a-z0-9_]+)"', body)


def main() -> int:
    chapter = CHAPTER_PATH.read_text(encoding="utf-8")
    en = parse_localization(LANG_DIR / "en_us.snbt")
    ru = parse_localization(LANG_DIR / "ru_ru.snbt")
    failures: list[str] = []
    rows: list[tuple[str, str, int, int, int, bool, str]] = []

    spans = quest_spans(chapter)
    if len(spans) != 141:
        failures.append(f"Expected 141 Mystical Agriculture quests, found {len(spans)}")

    for start, end in spans:
        block = chapter[start:end]
        quest_id, items = quest_identity(block)
        types = task_types(block)
        expected_acceptance = acceptance_id(quest_id)
        has_acceptance = f'id: "{expected_acceptance}"' in block
        no_rewards = "rewards:" not in block
        title_key = f"quest.{quest_id}.title"
        desc_key = f"quest.{quest_id}.quest_desc"
        en_length = visible_length(en.get(desc_key, ""))
        ru_length = visible_length(ru.get(desc_key, ""))
        label = ", ".join(items) if items else f"quest {quest_id}"
        status = "PASS"

        if len(types) < 2 or not has_acceptance:
            failures.append(
                f"{label}: expected original task(s) plus authored acceptance task, found {types}"
            )
            status = "FAIL"
        if not no_rewards:
            failures.append(f"{label}: material, random or XP reward remains")
            status = "FAIL"
        if title_key not in en or title_key not in ru:
            failures.append(f"{label}: missing bilingual title")
            status = "FAIL"
        if en_length < 180 or ru_length < 180:
            failures.append(
                f"{label}: description too short (EN {en_length}, RU {ru_length}; minimum 180)"
            )
            status = "FAIL"

        rows.append((label, quest_id, len(types), en_length, ru_length, no_rewards, status))

    lines = [
        "# Mystical Agriculture Catalogue Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "The legacy crop catalogue must validate a legal renewable-production system and must not distribute seeds, essence, souls or other progression materials as quest rewards.",
        "",
        "| Item or system | Quest | Tasks | EN description | RU description | No rewards | Status |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for label, quest_id, tasks, en_length, ru_length, no_rewards, status in rows:
        lines.append(
            f"| `{label}` | `{quest_id}` | {tasks} | {en_length} | {ru_length} | "
            f"{'yes' if no_rewards else 'no'} | {status} |"
        )
    lines.extend([
        "",
        "## Aggregate",
        "",
        f"- Mystical Agriculture quests: **{len(rows)}**",
        f"- Reward-free quests: **{sum(row[5] for row in rows)}**",
        f"- Fully bilingual quests: **{sum(row[3] >= 180 and row[4] >= 180 for row in rows)}**",
        f"- Failures: **{len(failures)}**",
        "",
    ])
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"mystical_agriculture_quality: {'PASS' if not failures else 'FAIL'}")
    print(f"quests: {len(rows)}")
    print(f"reward_free: {sum(row[5] for row in rows)}")
    print(f"bilingual: {sum(row[3] >= 180 and row[4] >= 180 for row in rows)}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
