from __future__ import annotations

from upgrade_storage_systems_core import (
    CHAPTER_PATH,
    CONTENT,
    FOCUS_ITEMS,
    LANG_DIR,
    acceptance_id,
    matching_delimiter,
    upsert,
)


def quest_spans(text: str) -> list[tuple[int, int]]:
    marker = text.find("quests:")
    if marker < 0:
        raise RuntimeError("Storage chapter has no quests list")
    list_start = text.find("[", marker)
    if list_start < 0:
        raise RuntimeError("Storage chapter quests list is malformed")
    list_end = matching_delimiter(text, list_start, "[", "]")

    spans: list[tuple[int, int]] = []
    cursor = list_start + 1
    while cursor < list_end:
        start = text.find("{", cursor, list_end)
        if start < 0:
            break
        end = matching_delimiter(text, start, "{", "}")
        spans.append((start, end))
        cursor = end + 1
    return spans


def quest_for_item(text: str, item_id: str) -> tuple[str, int, int]:
    target = f'id: "{item_id}"'
    for object_start, object_end in quest_spans(text):
        block = text[object_start : object_end + 1]
        tasks_marker = block.find("tasks:")
        if tasks_marker < 0:
            continue
        list_start = block.find("[", tasks_marker)
        if list_start < 0:
            continue
        list_end = matching_delimiter(block, list_start, "[", "]")
        tasks_body = block[list_start : list_end + 1]
        if target not in tasks_body:
            continue

        import re

        quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
        if not quest_match:
            raise RuntimeError(f"Storage quest ID not found for {item_id}")
        return quest_match.group(1), object_start, object_end

    raise RuntimeError(f"Storage focus item not found in quest tasks: {item_id}")


def add_checkmark(text: str, item_id: str) -> tuple[str, bool, str]:
    quest_id, object_start, object_end = quest_for_item(text, item_id)
    task_id = acceptance_id(quest_id)
    block = text[object_start : object_end + 1]
    if f'id: "{task_id}"' in block:
        return text, False, quest_id

    tasks_marker = block.find("tasks:")
    if tasks_marker < 0:
        raise RuntimeError(f"Storage quest has no task list: {quest_id}")
    list_start = block.find("[", tasks_marker)
    if list_start < 0:
        raise RuntimeError(f"Storage quest task list is malformed: {quest_id}")
    list_end = matching_delimiter(block, list_start, "[", "]")
    insertion = (
        "\n\t\t\t{\n"
        f"\t\t\t\tid: \"{task_id}\"\n"
        "\t\t\t\ttype: \"checkmark\"\n"
        "\t\t\t}\n\t\t\t"
    )
    global_list_end = object_start + list_end
    return text[:global_list_end] + insertion + text[global_list_end:], True, quest_id


def main() -> int:
    chapter = CHAPTER_PATH.read_text(encoding="utf-8")
    changed_tasks = 0
    quest_ids: dict[str, str] = {}

    for item_id in FOCUS_ITEMS:
        chapter, added, quest_id = add_checkmark(chapter, item_id)
        changed_tasks += int(added)
        quest_ids[item_id] = quest_id
        print(f"{item_id} -> {quest_id}")

    if changed_tasks:
        CHAPTER_PATH.write_text(chapter, encoding="utf-8", newline="\n")

    changed_localization = False
    for locale, content in CONTENT.items():
        path = LANG_DIR / f"{locale}.snbt"
        text = path.read_text(encoding="utf-8")
        changed = False
        for item_id, (title, description) in content.items():
            quest_id = quest_ids[item_id]
            text, title_changed = upsert(text, f"quest.{quest_id}.title", title)
            text, desc_changed = upsert(text, f"quest.{quest_id}.quest_desc", description)
            changed = changed or title_changed or desc_changed
        if changed:
            path.write_text(text, encoding="utf-8", newline="\n")
        changed_localization = changed_localization or changed
        print(f"{locale}: {'updated' if changed else 'unchanged'}")

    print(f"Storage acceptance tasks added: {changed_tasks}")
    print("Storage localization changed" if changed_localization else "Storage localization unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
