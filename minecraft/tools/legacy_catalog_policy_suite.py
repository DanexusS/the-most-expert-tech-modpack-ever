from __future__ import annotations

from pathlib import Path

import catalog_upgrade_common as common
from catalog_upgrade_batch import merge_entries
from catalog_upgrade_multinamespace import select_category
from snbt_field_parser import extract_array, quest_spans


def upgrade_policies(policy_paths: list[str]) -> int:
    common.select_category = select_category
    common.extract_array = extract_array
    common.quest_spans = quest_spans

    localization: dict[str, dict[str, str | list[str]]] = {
        "en_us": {},
        "ru_ru": {},
    }
    total_quests = 0
    total_rewards_removed = 0
    total_tasks_added = 0

    for policy_name in policy_paths:
        policy_path = Path(policy_name)
        if not policy_path.is_absolute():
            policy_path = common.ROOT / policy_path
        policy = common.load_policy(policy_path)
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

        localization["en_us"][f"chapter.{policy['chapter_id']}.title"] = policy[
            "chapter_title_en"
        ]
        localization["ru_ru"][f"chapter.{policy['chapter_id']}.title"] = policy[
            "chapter_title_ru"
        ]
        total_quests += len(spans)
        total_rewards_removed += rewards_removed
        total_tasks_added += tasks_added
        print(
            f"catalog: {policy['chapter_filename']} quests={len(spans)} "
            f"rewards_removed={rewards_removed} acceptance_tasks_added={tasks_added}"
        )

    for locale, entries in localization.items():
        path = common.LANG_DIR / f"{locale}.snbt"
        original = path.read_text(encoding="utf-8")
        merged = merge_entries(original, entries)
        if merged != original:
            path.write_text(merged, encoding="utf-8", newline="\n")
        print(f"{locale}_manifest_localization_entries: {len(entries)}")

    print(f"manifest_policy_quests: {total_quests}")
    print(f"manifest_reward_fields_removed: {total_rewards_removed}")
    print(f"manifest_acceptance_tasks_added: {total_tasks_added}")
    return 0


def gate_policies(policy_paths: list[str]) -> int:
    common.select_category = select_category
    common.extract_array = extract_array
    common.quest_spans = quest_spans
    result = 0
    for policy_name in policy_paths:
        policy_path = Path(policy_name)
        if not policy_path.is_absolute():
            policy_path = common.ROOT / policy_path
        policy = common.load_policy(policy_path)
        result = max(result, common.gate(policy))
    return result
