from __future__ import annotations

import re
from pathlib import Path

from simulation_catalog_common import acceptance_id, extract_array, quest_identity, quest_spans

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


def run_quality_gate(
    chapter_path: Path,
    lang_dir: Path,
    report_path: Path,
    report_title: str,
    chapter_name: str,
    acceptance_namespace: str,
    expected_count: int,
    minimum_description: int = 180,
) -> tuple[list[str], int]:
    chapter = chapter_path.read_text(encoding="utf-8")
    en = parse_localization(lang_dir / "en_us.snbt")
    ru = parse_localization(lang_dir / "ru_ru.snbt")
    failures: list[str] = []
    rows: list[tuple[str, str, int, int, int, bool, str]] = []

    spans = quest_spans(chapter, chapter_name)
    if len(spans) != expected_count:
        failures.append(f"Expected {expected_count} {chapter_name} quests, found {len(spans)}")

    for start, end in spans:
        block = chapter[start:end]
        quest_id, resources = quest_identity(block)
        types = task_types(block)
        authored_id = acceptance_id(acceptance_namespace, quest_id)
        has_acceptance = f'id: "{authored_id}"' in block
        no_rewards = "rewards:" not in block
        title_key = f"quest.{quest_id}.title"
        desc_key = f"quest.{quest_id}.quest_desc"
        en_length = visible_length(en.get(desc_key, ""))
        ru_length = visible_length(ru.get(desc_key, ""))
        label = ", ".join(resources[:4]) if resources else f"checkpoint:{quest_id}"
        status = "PASS"

        if len(types) < 2 or not has_acceptance:
            failures.append(f"{label}: original task plus authored acceptance required; found {types}")
            status = "FAIL"
        if not no_rewards:
            failures.append(f"{label}: random, material or XP quest reward remains")
            status = "FAIL"
        if title_key not in en or title_key not in ru:
            failures.append(f"{label}: missing bilingual title")
            status = "FAIL"
        if en_length < minimum_description or ru_length < minimum_description:
            failures.append(
                f"{label}: description too short (EN {en_length}, RU {ru_length}; minimum {minimum_description})"
            )
            status = "FAIL"

        rows.append((label, quest_id, len(types), en_length, ru_length, no_rewards, status))

    lines = [
        f"# {report_title}",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        f"Every {chapter_name} catalogue node must validate a bounded, stage-legal simulation system and must not distribute progression materials as quest rewards.",
        "",
        "| Gate | Quest | Tasks | EN description | RU description | No rewards | Status |",
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
        f"- Quests: **{len(rows)}**",
        f"- Reward-free quests: **{sum(row[5] for row in rows)}**",
        f"- Fully bilingual quests: **{sum(row[3] >= minimum_description and row[4] >= minimum_description for row in rows)}**",
        f"- Failures: **{len(failures)}**",
        "",
    ])
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    return failures, len(rows)
