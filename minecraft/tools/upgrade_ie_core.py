from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "immersive_engineering.snbt"

FOCUS_ITEMS = (
    "immersiveengineering:hammer",
    "immersiveengineering:voltmeter",
    "immersiveengineering:cokebrick",
    "immersiveengineering:blastbrick",
    "immersiveengineering:blastbrick_reinforced",
    "immersiveengineering:blastfurnace_preheater",
    "immersiveengineering:craftingtable",
    "immersiveengineering:workbench",
    "immersiveengineering:component_steel",
    "immersiveengineering:fluid_pipe",
    "immersiveengineering:fluid_pump",
    "immersiveengineering:cloche",
)


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


def quest_for_item(text: str, item_id: str) -> tuple[str, int, int]:
    item_index = text.find(f'id: "{item_id}"')
    if item_index < 0:
        raise RuntimeError(f"IE focus item not found in chapter: {item_id}")
    object_start = text.rfind("\n\t\t{", 0, item_index)
    if object_start < 0:
        raise RuntimeError(f"IE quest object start not found for {item_id}")
    object_start += 1
    object_end = matching_delimiter(text, object_start, "{", "}")
    block = text[object_start : object_end + 1]
    quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not quest_match:
        raise RuntimeError(f"IE quest ID not found for {item_id}")
    return quest_match.group(1), object_start, object_end


def acceptance_id(quest_id: str) -> str:
    return hashlib.sha256(f"ie_acceptance:{quest_id}".encode()).hexdigest()[:16].upper()


def add_checkmark(text: str, item_id: str) -> tuple[str, bool, str]:
    quest_id, object_start, object_end = quest_for_item(text, item_id)
    task_id = acceptance_id(quest_id)
    if f'id: "{task_id}"' in text:
        return text, False, quest_id

    block = text[object_start : object_end + 1]
    tasks_marker = block.find("tasks:")
    if tasks_marker < 0:
        raise RuntimeError(f"IE quest has no task list: {quest_id}")
    list_start = block.find("[", tasks_marker)
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
    text = CHAPTER_PATH.read_text(encoding="utf-8")
    changed = 0
    for item_id in FOCUS_ITEMS:
        text, added, quest_id = add_checkmark(text, item_id)
        changed += int(added)
        print(f"{item_id} -> {quest_id}")

    if changed:
        CHAPTER_PATH.write_text(text, encoding="utf-8", newline="\n")
        print(f"IE core acceptance tasks added: {changed}")
    else:
        print("IE core acceptance tasks already present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
