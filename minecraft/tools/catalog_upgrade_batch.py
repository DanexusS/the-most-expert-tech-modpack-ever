from __future__ import annotations

import argparse
import sys
from pathlib import Path

import catalog_upgrade_common as common
from catalog_upgrade_multinamespace import select_category
from snbt_field_parser import extract_array, quest_spans


def merge_entries(text: str, entries: dict[str, str | list[str]]) -> str:
    matches = list(common.KEY_RE.finditer(text))
    closing = text.rfind("}")
    if closing < 0:
        raise RuntimeError("Localization file has no closing brace")

    rendered = {
        key: f"\t{key}: {common.render(value)}\n"
        for key, value in entries.items()
    }
    remaining = dict(rendered)

    if not matches:
        insertion = "".join(remaining[key] for key in sorted(remaining))
        return text[:closing].rstrip() + "\n" + insertion + text[closing:]

    parts = [text[: matches[0].start()]]
    for index, match in enumerate(matches):
        key = match.group(1)
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else closing
        replacement = remaining.pop(key, None)
        parts.append(replacement if replacement is not None else text[start:end])

    if remaining:
        if parts and not parts[-1].endswith("\n"):
            parts.append("\n")
        parts.extend(remaining[key] for key in sorted(remaining))
    parts.append(text[closing:])
    return "".join(parts)


def upgrade(policy: dict) -> None:
    chapter_path = (
        common.ROOT
        / "config"
        / "ftbquests"
        / "quests"
        / "chapters"
        / f"{policy['chapter_filename']}.snbt"
    )
    text = chapter_path.read_text(encoding="utf-8")
    spans = quest_spans(text)
    replacements: list[tuple[int, int, str]] = []
    localization: dict[str, dict[str, str | list[str]]] = {
        "en_us": {},
        "ru_ru": {},
    }
    rewards_removed = 0
    tasks_added = 0

    for start, end in spans:
        block = text[start:end]
        quest_id, items = common.quest_identity(block)
        block, removed = common.remove_rewards(block)
        rewards_removed += int(removed)
        block, added = common.add_acceptance_task(
            block,
            quest_id,
            policy["acceptance_namespace"],
        )
        tasks_added += int(added)
        replacements.append((start, end, block))

        content = common.localized_content(policy, items, quest_id)
        for locale, (title, desc) in content.items():
            localization[locale][f"quest.{quest_id}.title"] = title
            localization[locale][f"quest.{quest_id}.quest_desc"] = desc

    for start, end, block in reversed(replacements):
        text = text[:start] + block + text[end:]
    chapter_path.write_text(text, encoding="utf-8", newline="\n")

    for locale, entries in localization.items():
        entries[f"chapter.{policy['chapter_id']}.title"] = (
            policy["chapter_title_en"]
            if locale == "en_us"
            else policy["chapter_title_ru"]
        )
        path = common.LANG_DIR / f"{locale}.snbt"
        language = path.read_text(encoding="utf-8")
        merged = merge_entries(language, entries)
        if merged != language:
            path.write_text(merged, encoding="utf-8", newline="\n")

    print(f"catalog: {policy['chapter_filename']}")
    print(f"quests: {len(spans)}")
    print(f"rewards_removed: {rewards_removed}")
    print(f"acceptance_tasks_added: {tasks_added}")
    print(f"localization_entries_batched: {sum(len(v) for v in localization.values())}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("upgrade", "gate"))
    parser.add_argument("policy", type=Path)
    args = parser.parse_args()

    policy_path = (
        args.policy
        if args.policy.is_absolute()
        else common.ROOT / args.policy
    )
    policy = common.load_policy(policy_path)
    common.select_category = select_category
    common.extract_array = extract_array
    common.quest_spans = quest_spans

    if args.mode == "upgrade":
        upgrade(policy)
        return 0
    return common.gate(policy)


if __name__ == "__main__":
    sys.exit(main())
