from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from catalog_upgrade_common import (
    extract_array,
    parse_localization,
    quest_spans,
    task_types,
    visible_length,
)

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
REPORT_PATH = ROOT / "docs" / "LEGACY_QUEST_SEMANTIC_AUDIT.md"
QUEUE_PATH = ROOT / "config" / "legacy_quest_remediation_queue.json"
GENERATED_PREFIXES = (
    "main_stage_",
    "stage_annex_",
    "core_technology_manual_",
)
QUEST_ID_RE = re.compile(r'(?m)^\s*id:\s*"([0-9A-F]{16})"')


def chapter_filename(text: str, fallback: str) -> str:
    match = re.search(r'(?m)^\s*filename:\s*"([^"]+)"', text)
    return match.group(1) if match else fallback


def dependency_count(block: str) -> int:
    try:
        _, _, body = extract_array(block, "dependencies:")
    except RuntimeError:
        return 0
    return len(re.findall(r'"[0-9A-F]{16}"', body))


def normalized_description(raw: str) -> str:
    text = " ".join(re.findall(r'"((?:\\.|[^"\\])*)"', raw)).lower()
    return re.sub(r"\s+", " ", text).strip()


def safe_task_types(block: str) -> list[str]:
    try:
        return task_types(block)
    except RuntimeError:
        return []


def main() -> int:
    en = parse_localization(LANG_DIR / "en_us.snbt")
    ru = parse_localization(LANG_DIR / "ru_ru.snbt")
    chapter_rows: list[dict] = []
    quest_rows: list[dict] = []
    description_owners: dict[str, list[tuple[str, str]]] = defaultdict(list)
    malformed_total = 0

    for path in sorted(CHAPTER_DIR.glob("*.snbt")):
        text = path.read_text(encoding="utf-8")
        filename = chapter_filename(text, path.stem)
        if filename.startswith(GENERATED_PREFIXES):
            continue
        spans = quest_spans(text)
        chapter_quests: list[dict] = []

        for object_index, (start, end) in enumerate(spans):
            block = text[start:end]
            quest_match = QUEST_ID_RE.search(block)
            if quest_match is None:
                malformed_total += 1
                row = {
                    "chapter": filename,
                    "quest_id": f"MALFORMED_OBJECT_{object_index:03d}",
                    "risk_score": 12,
                    "flags": ["MALFORMED_QUEST_OBJECT", "NO_TASKS", "NO_OPERATIONAL_GUIDANCE"],
                    "task_types": safe_task_types(block),
                    "en_description_length": 0,
                    "ru_description_length": 0,
                    "maximum_item_count": 1,
                }
                chapter_quests.append(row)
                quest_rows.append(row)
                continue

            quest_id = quest_match.group(1)
            types = safe_task_types(block)
            title_key = f"quest.{quest_id}.title"
            desc_key = f"quest.{quest_id}.quest_desc"
            en_len = visible_length(en.get(desc_key, ""))
            ru_len = visible_length(ru.get(desc_key, ""))
            item_counts = [int(value) for value in re.findall(r"\bcount:\s*([0-9]+)", block)]
            maximum_count = max(item_counts, default=1)
            flags: list[str] = []

            if not types:
                flags.append("NO_TASKS")
            if types == ["item"]:
                flags.append("ITEM_ONLY")
            if types == ["checkmark"]:
                flags.append("CHECKMARK_ONLY")
            if en_len < 80 or ru_len < 80:
                flags.append("NO_OPERATIONAL_GUIDANCE")
            if "rewards:" in block:
                flags.append("HAS_REWARD")
            if maximum_count > 64:
                flags.append("EXCESSIVE_ITEM_COUNT")
            if dependency_count(block) == 0:
                flags.append("ROOT_OR_ORPHAN")

            score = 0
            score += 6 if "NO_TASKS" in flags else 0
            score += 4 if "NO_OPERATIONAL_GUIDANCE" in flags else 0
            score += 3 if "ITEM_ONLY" in flags else 0
            score += 3 if "CHECKMARK_ONLY" in flags and "NO_OPERATIONAL_GUIDANCE" in flags else 0
            score += 3 if "HAS_REWARD" in flags else 0
            score += 5 if "EXCESSIVE_ITEM_COUNT" in flags else 0
            score += 1 if "ROOT_OR_ORPHAN" in flags else 0

            row = {
                "chapter": filename,
                "quest_id": quest_id,
                "risk_score": score,
                "flags": flags,
                "task_types": types,
                "en_description_length": en_len,
                "ru_description_length": ru_len,
                "maximum_item_count": maximum_count,
            }
            chapter_quests.append(row)
            quest_rows.append(row)

            normalized = normalized_description(en.get(desc_key, ""))
            if len(normalized) >= 80:
                description_owners[normalized].append((filename, quest_id))

        counts = Counter(flag for row in chapter_quests for flag in row["flags"])
        high_risk = sum(row["risk_score"] >= 7 for row in chapter_quests)
        risk_total = sum(row["risk_score"] for row in chapter_quests)
        quest_count = len(chapter_quests)
        high_ratio = high_risk / max(1, quest_count)
        guidance_ratio = counts["NO_OPERATIONAL_GUIDANCE"] / max(1, quest_count)
        item_ratio = counts["ITEM_ONLY"] / max(1, quest_count)

        if quest_count == 0:
            classification = "EMPTY_REVIEW"
        elif counts["MALFORMED_QUEST_OBJECT"] > 0:
            classification = "REWRITE_REQUIRED"
        elif high_ratio >= 0.5 or guidance_ratio >= 0.6:
            classification = "REWRITE_REQUIRED"
        elif high_ratio >= 0.2 or item_ratio >= 0.4 or counts["HAS_REWARD"] > 0:
            classification = "REVIEW_REQUIRED"
        else:
            classification = "CURRENTLY_ACCEPTABLE"

        chapter_rows.append(
            {
                "chapter": filename,
                "quests": quest_count,
                "risk_score": risk_total,
                "high_risk_quests": high_risk,
                "classification": classification,
                "flags": dict(counts),
            }
        )

    duplicate_groups = [owners for owners in description_owners.values() if len(owners) > 1]
    duplicate_lookup: set[tuple[str, str]] = {
        owner for owners in duplicate_groups for owner in owners
    }
    for row in quest_rows:
        if (row["chapter"], row["quest_id"]) in duplicate_lookup:
            row["flags"].append("DUPLICATE_DESCRIPTION")
            row["risk_score"] += 2

    chapter_rows.sort(
        key=lambda row: (
            row["classification"] != "REWRITE_REQUIRED",
            row["classification"] != "REVIEW_REQUIRED",
            -row["risk_score"],
            row["chapter"],
        )
    )
    quest_rows.sort(key=lambda row: (-row["risk_score"], row["chapter"], row["quest_id"]))

    queue = {
        "schema_version": 2,
        "generated_exclusions": list(GENERATED_PREFIXES),
        "summary": {
            "legacy_chapters": len(chapter_rows),
            "legacy_quests": len(quest_rows),
            "malformed_quest_objects": malformed_total,
            "rewrite_required_chapters": sum(
                row["classification"] == "REWRITE_REQUIRED" for row in chapter_rows
            ),
            "review_required_chapters": sum(
                row["classification"] == "REVIEW_REQUIRED" for row in chapter_rows
            ),
            "duplicate_description_groups": len(duplicate_groups),
        },
        "chapters": chapter_rows,
        "highest_risk_quests": quest_rows[:250],
    }
    QUEUE_PATH.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    lines = [
        "# Legacy Quest Semantic Audit",
        "",
        "This report analyses non-generated legacy chapters for obsolete catalogue structure, missing operational guidance, malformed quest objects, empty tasks, rewards, excessive item counts and duplicate descriptions. It is a remediation queue, not proof that every surviving quest is fun in play.",
        "",
        "## Summary",
        "",
        f"- Legacy chapters analysed: **{len(chapter_rows)}**",
        f"- Legacy quests and malformed objects analysed: **{len(quest_rows)}**",
        f"- Malformed quest objects: **{malformed_total}**",
        f"- Chapters requiring rewrite: **{sum(row['classification'] == 'REWRITE_REQUIRED' for row in chapter_rows)}**",
        f"- Chapters requiring review: **{sum(row['classification'] == 'REVIEW_REQUIRED' for row in chapter_rows)}**",
        f"- Empty chapters requiring a keep/remove decision: **{sum(row['classification'] == 'EMPTY_REVIEW' for row in chapter_rows)}**",
        f"- Duplicate description groups: **{len(duplicate_groups)}**",
        "",
        "## Chapter remediation queue",
        "",
        "| Chapter | Objects | Risk score | High risk | Malformed | Item-only | Missing guidance | Rewards | Classification |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in chapter_rows:
        flags = row["flags"]
        lines.append(
            f"| `{row['chapter']}` | {row['quests']} | {row['risk_score']} | {row['high_risk_quests']} | {flags.get('MALFORMED_QUEST_OBJECT', 0)} | {flags.get('ITEM_ONLY', 0)} | {flags.get('NO_OPERATIONAL_GUIDANCE', 0)} | {flags.get('HAS_REWARD', 0)} | {row['classification']} |"
        )

    lines.extend(
        [
            "",
            "## Highest-risk individual quests and objects",
            "",
            "| Chapter | Quest/Object ID | Score | Flags |",
            "|---|---|---:|---|",
        ]
    )
    for row in quest_rows[:100]:
        lines.append(
            f"| `{row['chapter']}` | `{row['quest_id']}` | {row['risk_score']} | {', '.join(row['flags']) or 'none'} |"
        )
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"legacy_chapters: {len(chapter_rows)}")
    print(f"legacy_objects: {len(quest_rows)}")
    print(f"malformed_quest_objects: {malformed_total}")
    print(
        "rewrite_required: "
        + str(sum(row["classification"] == "REWRITE_REQUIRED" for row in chapter_rows))
    )
    print(f"duplicate_description_groups: {len(duplicate_groups)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
