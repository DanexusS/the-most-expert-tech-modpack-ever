from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
REPORT_PATH = ROOT / "docs" / "QUEST_QUALITY_REPORT.md"
CORE_CHAPTERS = {"expert_progression", "engineering_foundations_guide"}
KEY_RE = re.compile(r"(?m)^\t([A-Za-z0-9_.-]+):")


@dataclass
class QuestMetric:
    quest_id: str
    task_count: int
    task_types: set[str]
    dependency_count: int
    maximum_item_count: int
    en_title: bool
    ru_title: bool
    en_desc_length: int
    ru_desc_length: int
    score: int


@dataclass
class ChapterMetric:
    filename: str
    chapter_id: str
    quests: list[QuestMetric]

    @property
    def average_score(self) -> float:
        return sum(quest.score for quest in self.quests) / max(1, len(self.quests))


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
    raise RuntimeError(f"Unclosed delimiter {opening!r} at offset {start}")


def extract_array(text: str, marker: str) -> str:
    marker_index = text.find(marker)
    if marker_index < 0:
        return ""
    start = text.find("[", marker_index)
    if start < 0:
        return ""
    end = matching_delimiter(text, start, "[", "]")
    return text[start + 1 : end]


def top_level_objects(array_body: str) -> list[str]:
    objects: list[str] = []
    index = 0
    while index < len(array_body):
        start = array_body.find("{", index)
        if start < 0:
            break
        end = matching_delimiter(array_body, start, "{", "}")
        objects.append(array_body[start : end + 1])
        index = end + 1
    return objects


def parse_localization(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    matches = list(KEY_RE.finditer(text))
    values: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else text.rfind("}")
        values[match.group(1)] = text[start:end].strip()
    return values


def text_length(raw: str) -> int:
    # Count visible localized content, ignoring SNBT punctuation and formatting.
    return len(" ".join(re.findall(r'"((?:\\.|[^"\\])*)"', raw)))


def score_quest(
    quest_id: str,
    task_count: int,
    dependency_count: int,
    maximum_item_count: int,
    en: dict[str, str],
    ru: dict[str, str],
) -> tuple[int, bool, bool, int, int]:
    title_key = f"quest.{quest_id}.title"
    desc_key = f"quest.{quest_id}.quest_desc"
    en_title = title_key in en
    ru_title = title_key in ru
    en_desc_length = text_length(en.get(desc_key, ""))
    ru_desc_length = text_length(ru.get(desc_key, ""))

    score = 0
    score += 10 if en_title else 0
    score += 10 if ru_title else 0
    score += 15 if en_desc_length > 0 else 0
    score += 15 if ru_desc_length > 0 else 0
    score += 10 if en_desc_length >= 80 else 0
    score += 10 if ru_desc_length >= 80 else 0
    score += 10 if dependency_count > 0 else 5
    score += 10 if task_count > 0 else 0
    score += 10 if maximum_item_count <= 64 else 0
    return score, en_title, ru_title, en_desc_length, ru_desc_length


def parse_chapter(path: Path, en: dict[str, str], ru: dict[str, str]) -> ChapterMetric:
    text = path.read_text(encoding="utf-8")
    filename_match = re.search(r'(?m)^\s*filename:\s*"([^"]+)"', text)
    chapter_id_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', text)
    filename = filename_match.group(1) if filename_match else path.stem
    chapter_id = chapter_id_match.group(1) if chapter_id_match else "UNKNOWN"
    quest_body = extract_array(text, "quests:")
    metrics: list[QuestMetric] = []

    for block in top_level_objects(quest_body):
        quest_id_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
        if not quest_id_match:
            continue
        quest_id = quest_id_match.group(1)
        tasks_body = extract_array(block, "tasks:")
        task_objects = top_level_objects(tasks_body)
        task_types = set(re.findall(r'(?m)^\s*type:\s*"([a-z0-9_]+)"', tasks_body))
        item_counts = [int(value) for value in re.findall(r'\bcount:\s*([0-9]+)', tasks_body)]
        dependencies_body = extract_array(block, "dependencies:")
        dependency_count = len(re.findall(r'"[0-9A-F]{16}"', dependencies_body))
        maximum_item_count = max(item_counts, default=1)
        score, en_title, ru_title, en_desc_length, ru_desc_length = score_quest(
            quest_id,
            len(task_objects),
            dependency_count,
            maximum_item_count,
            en,
            ru,
        )
        metrics.append(
            QuestMetric(
                quest_id=quest_id,
                task_count=len(task_objects),
                task_types=task_types,
                dependency_count=dependency_count,
                maximum_item_count=maximum_item_count,
                en_title=en_title,
                ru_title=ru_title,
                en_desc_length=en_desc_length,
                ru_desc_length=ru_desc_length,
                score=score,
            )
        )
    return ChapterMetric(filename=filename, chapter_id=chapter_id, quests=metrics)


def chapter_counts(chapter: ChapterMetric) -> dict[str, int]:
    return {
        "quests": len(chapter.quests),
        "roots": sum(quest.dependency_count == 0 for quest in chapter.quests),
        "single_item": sum(quest.task_count == 1 and quest.task_types == {"item"} for quest in chapter.quests),
        "checkmark_only": sum(quest.task_count == 1 and quest.task_types == {"checkmark"} for quest in chapter.quests),
        "large_counts": sum(quest.maximum_item_count > 64 for quest in chapter.quests),
        "missing_en_desc": sum(quest.en_desc_length == 0 for quest in chapter.quests),
        "missing_ru_desc": sum(quest.ru_desc_length == 0 for quest in chapter.quests),
    }


def core_failures(chapters: list[ChapterMetric]) -> list[str]:
    failures: list[str] = []
    by_name = {chapter.filename: chapter for chapter in chapters}
    for name in sorted(CORE_CHAPTERS):
        chapter = by_name.get(name)
        if chapter is None:
            failures.append(f"Missing core chapter: {name}")
            continue
        if chapter.average_score < 85.0:
            failures.append(f"{name}: average quality score {chapter.average_score:.1f} < 85")
        for quest in chapter.quests:
            if not quest.en_title or not quest.ru_title:
                failures.append(f"{name}/{quest.quest_id}: missing bilingual title")
            if quest.en_desc_length < 80 or quest.ru_desc_length < 80:
                failures.append(f"{name}/{quest.quest_id}: description shorter than 80 characters")
            if quest.maximum_item_count > 64:
                failures.append(f"{name}/{quest.quest_id}: item count exceeds 64")
            if name == "expert_progression" and quest.dependency_count > 0 and quest.task_count < 2:
                failures.append(f"{name}/{quest.quest_id}: legacy milestone lacks acceptance task")
    return failures


def render_report(chapters: list[ChapterMetric], failures: list[str]) -> str:
    all_quests = [quest for chapter in chapters for quest in chapter.quests]
    total = len(all_quests)
    single_item = sum(quest.task_count == 1 and quest.task_types == {"item"} for quest in all_quests)
    checkmark_only = sum(quest.task_count == 1 and quest.task_types == {"checkmark"} for quest in all_quests)
    large_counts = sum(quest.maximum_item_count > 64 for quest in all_quests)
    bilingual_desc = sum(quest.en_desc_length > 0 and quest.ru_desc_length > 0 for quest in all_quests)

    lines = [
        "# Quest Quality Report",
        "",
        "Generated by `tools/quest_quality_audit.py`. Scores are triage metrics, not a claim that a quest is fun in actual play.",
        "",
        "## Global metrics",
        "",
        f"- Chapters: **{len(chapters)}**",
        f"- Quests parsed: **{total}**",
        f"- Bilingual quest descriptions: **{bilingual_desc} / {total}**",
        f"- Single item-only quests: **{single_item}**",
        f"- Checkmark-only quests: **{checkmark_only}**",
        f"- Quests requesting more than 64 items in one task: **{large_counts}**",
        "",
        "## Chapter ranking",
        "",
        "Lower-scoring chapters are the next candidates for manual redesign and translation.",
        "",
        "| Chapter | Quests | Avg score | Item-only | Checkmark-only | >64 count | Missing EN desc | Missing RU desc |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for chapter in sorted(chapters, key=lambda item: (item.average_score, item.filename)):
        counts = chapter_counts(chapter)
        lines.append(
            f"| `{chapter.filename}` | {counts['quests']} | {chapter.average_score:.1f} | "
            f"{counts['single_item']} | {counts['checkmark_only']} | {counts['large_counts']} | "
            f"{counts['missing_en_desc']} | {counts['missing_ru_desc']} |"
        )

    lines.extend(["", "## Core release gates", ""])
    if failures:
        lines.append("**FAIL**")
        lines.extend(f"- {failure}" for failure in failures)
    else:
        lines.append("**PASS** — core expert chapters meet the current static quality gates.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    en = parse_localization(LANG_DIR / "en_us.snbt")
    ru = parse_localization(LANG_DIR / "ru_ru.snbt")
    chapters = [parse_chapter(path, en, ru) for path in sorted(CHAPTER_DIR.glob("*.snbt"))]
    failures = core_failures(chapters)
    REPORT_PATH.write_text(render_report(chapters, failures), encoding="utf-8", newline="\n")

    print(f"quest_quality: {'FAIL' if failures else 'PASS'}")
    print(f"chapters: {len(chapters)}")
    print(f"quests: {sum(len(chapter.quests) for chapter in chapters)}")
    print(f"core_failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
