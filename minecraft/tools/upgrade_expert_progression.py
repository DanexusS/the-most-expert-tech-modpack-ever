from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "expert_progression.snbt"

# Each legacy progression node already verifies its milestone item. The second
# task turns it into an explicit acceptance checkpoint: the localized text tells
# the player what must be repeatable, buffered or documented before confirming.
CHECKMARK_TASKS = {
    "A17E4D09B8C2F101": "A17E4D09B8C2F1A2",
    "B29F510AC7D3E202": "B29F510AC7D3E2B3",
    "C3A0621BD8E4F303": "C3A0621BD8E4F3C4",
    "5E5CFA388D9EC683": "5E5CFA388D9EC6D5",
    "D4B1732CE9F50404": "D4B1732CE9F504E6",
    "16838B1A7CA4BE89": "16838B1A7CA4BEF7",
    "31E4D1B55CA6546E": "31E4D1B55CA654A8",
    "33D42DC311D2F9BE": "33D42DC311D2F9B9",
    "0D54023AEE59ED08": "0D54023AEE59EDA0",
    "4377C3797509D983": "4377C3797509D9B1",
    "3EE8E42D0138A34A": "3EE8E42D0138A3C2",
    "742C709923A5AB9B": "742C709923A5ABD3",
    "6B91727E7931BD65": "6B91727E7931BDE4",
    "0D199D42E619C8CF": "0D199D42E619C8F5",
}


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


def add_checkmark(text: str, quest_id: str, task_id: str) -> tuple[str, bool]:
    if f'id: "{task_id}"' in text:
        return text, False

    marker = f'\n\t\t\tid: "{quest_id}"'
    marker_index = text.find(marker)
    if marker_index < 0:
        raise RuntimeError(f"Quest not found in expert progression: {quest_id}")

    object_start = text.rfind("\n\t\t{", 0, marker_index)
    if object_start < 0:
        raise RuntimeError(f"Quest object start not found: {quest_id}")
    object_start += 1
    object_end = matching_delimiter(text, object_start, "{", "}")
    block = text[object_start : object_end + 1]

    tasks_marker = block.find("tasks:")
    if tasks_marker < 0:
        raise RuntimeError(f"Quest has no task list: {quest_id}")
    list_start = block.find("[", tasks_marker)
    list_end = matching_delimiter(block, list_start, "[", "]")

    insertion = (
        "\n\t\t\t{\n"
        f"\t\t\t\tid: \"{task_id}\"\n"
        "\t\t\t\ttype: \"checkmark\"\n"
        "\t\t\t}\n\t\t\t"
    )
    global_list_end = object_start + list_end
    return text[:global_list_end] + insertion + text[global_list_end:], True


def main() -> int:
    text = CHAPTER_PATH.read_text(encoding="utf-8")
    changed = 0
    for quest_id, task_id in CHECKMARK_TASKS.items():
        text, added = add_checkmark(text, quest_id, task_id)
        changed += int(added)

    if changed:
        CHAPTER_PATH.write_text(text, encoding="utf-8", newline="\n")
        print(f"Upgraded legacy expert progression tasks: {changed}")
    else:
        print("Legacy expert progression tasks already upgraded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
