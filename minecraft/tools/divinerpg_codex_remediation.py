from __future__ import annotations

import argparse
import re
import sys

import catalog_upgrade_common as common
from catalog_upgrade_batch import merge_entries
from divinerpg_stage_seal_remediation import localized_content
from snbt_field_parser import quest_spans

ROOT = common.ROOT
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "divinerpg_codex.snbt"
REPORT_PATH = ROOT / "docs" / "DIVINERPG_CODEX_QUALITY_REPORT.md"
CHAPTER_ID = "7833368934691BD9"
EXPECTED_QUESTS = 89
MINIMUM_DESCRIPTION = 215


def quest_id(block: str) -> str:
    match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not match:
        raise RuntimeError("Quest without a valid ID")
    return match.group(1)


def upgrade() -> None:
    text = CHAPTER_PATH.read_text(encoding="utf-8")
    spans = quest_spans(text)
    replacements: list[tuple[int, int, str]] = []
    localization: dict[str, dict[str, str | list[str]]] = {"en_us": {}, "ru_ru": {}}
    rewards_removed = 0
    tasks_added = 0

    for start, end in spans:
        block = text[start:end]
        qid = quest_id(block)
        block, removed = common.remove_rewards(block)
        rewards_removed += int(removed)
        block, added = common.add_acceptance_task(block, qid, "divinerpg_codex_acceptance")
        tasks_added += int(added)
        replacements.append((start, end, block))
        content = localized_content(block, [])
        for locale, (title, desc) in content.items():
            localization[locale][f"quest.{qid}.title"] = title.replace(
                "DivineRPG Acceptance",
                "DivineRPG Codex Acceptance",
            ) if locale == "en_us" else title.replace(
                "приёмка DivineRPG",
                "приёмка кодекса DivineRPG",
            )
            localization[locale][f"quest.{qid}.quest_desc"] = desc

    for start, end, block in reversed(replacements):
        text = text[:start] + block + text[end:]
    CHAPTER_PATH.write_text(text, encoding="utf-8", newline="\n")

    localization["en_us"][f"chapter.{CHAPTER_ID}.title"] = "DivineRPG Codex — Dimensions, Bosses and Materials"
    localization["ru_ru"][f"chapter.{CHAPTER_ID}.title"] = "Кодекс DivineRPG — измерения, боссы и материалы"
    for locale, entries in localization.items():
        path = common.LANG_DIR / f"{locale}.snbt"
        original = path.read_text(encoding="utf-8")
        merged = merge_entries(original, entries)
        if merged != original:
            path.write_text(merged, encoding="utf-8", newline="\n")

    print("catalog: divinerpg_codex")
    print(f"quests: {len(spans)}")
    print(f"rewards_removed: {rewards_removed}")
    print(f"acceptance_tasks_added: {tasks_added}")


def gate() -> int:
    chapter = CHAPTER_PATH.read_text(encoding="utf-8")
    en = common.parse_localization(common.LANG_DIR / "en_us.snbt")
    ru = common.parse_localization(common.LANG_DIR / "ru_ru.snbt")
    spans = quest_spans(chapter)
    failures: list[str] = []
    rows: list[tuple[str, str, int, int, bool, str]] = []

    if len(spans) != EXPECTED_QUESTS:
        failures.append(f"Expected {EXPECTED_QUESTS} quests, found {len(spans)}")

    for start, end in spans:
        block = chapter[start:end]
        qid = quest_id(block)
        types = common.task_types(block)
        entity_match = re.search(r'(?m)^\s*entity:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', block)
        _, items = common.quest_identity(block)
        label = entity_match.group(1) if entity_match else (items[0] if items else f"checkpoint:{qid}")
        en_len = common.visible_length(en.get(f"quest.{qid}.quest_desc", ""))
        ru_len = common.visible_length(ru.get(f"quest.{qid}.quest_desc", ""))
        no_rewards = "rewards:" not in block
        status = "PASS"

        if "checkmark" not in types:
            failures.append(f"{label}: no practical acceptance task")
            status = "FAIL"
        if not no_rewards:
            failures.append(f"{label}: reward remains")
            status = "FAIL"
        if en_len < MINIMUM_DESCRIPTION or ru_len < MINIMUM_DESCRIPTION:
            failures.append(f"{label}: description too short (EN {en_len}, RU {ru_len})")
            status = "FAIL"
        rows.append((label, qid, en_len, ru_len, no_rewards, status))

    lines = [
        "# DivineRPG Codex Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "Every codex node requires task-aware RU/EN guidance, practical acceptance and no XP or material rewards. The codex remains supplementary and does not issue stage seals.",
        "",
        "| Subject | Quest | EN description | RU description | No rewards | Status |",
        "|---|---|---:|---:|---|---|",
    ]
    for label, qid, en_len, ru_len, no_rewards, status in rows:
        lines.append(f"| `{label}` | `{qid}` | {en_len} | {ru_len} | {'yes' if no_rewards else 'no'} | {status} |")
    lines.extend([
        "",
        "## Aggregate",
        "",
        f"- Quests: **{len(rows)}**",
        f"- Reward-free: **{sum(row[4] for row in rows)}**",
        f"- Fully bilingual: **{sum(row[2] >= MINIMUM_DESCRIPTION and row[3] >= MINIMUM_DESCRIPTION for row in rows)}**",
        f"- Failures: **{len(failures)}**",
        "",
    ])
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"divinerpg_codex_quality: {'PASS' if not failures else 'FAIL'}")
    print(f"quests: {len(rows)}")
    print(f"failures: {len(failures)}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("upgrade", "gate"))
    args = parser.parse_args()
    if args.mode == "upgrade":
        upgrade()
        return 0
    return gate()


if __name__ == "__main__":
    sys.exit(main())
