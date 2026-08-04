from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "create.snbt"

CHECKMARK_TASKS = {
    "4BB13C80196FD034": "4BB13C80196FD0A1",
    "0E5FC39E6C71A872": "0E5FC39E6C71A8B2",
    "4B976C143EDA4317": "4B976C143EDA43C3",
    "1837076B0EA3C11A": "1837076B0EA3C1D4",
    "4266BF7FCE3B4330": "4266BF7FCE3B43E5",
    "4C7CD3858A2BE870": "4C7CD3858A2BE8F6",
    "1D00D782B8F0B6D6": "1D00D782B8F0B607",
    "732D1A96512F2BFD": "732D1A96512F2B18",
    "19754AE8C11A6317": "19754AE8C11A6329",
    "0EE2E9EB6DC01E34": "0EE2E9EB6DC01E3A",
    "61348E2551E8AD6C": "61348E2551E8ADB4",
    "197AB0E07A40512F": "197AB0E07A4051C5",
    "51CCB7ACFD7B45F1": "51CCB7ACFD7B45D6",
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
        raise RuntimeError(f"Create core quest not found: {quest_id}")

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
        print(f"Create core acceptance tasks added: {changed}")
    else:
        print("Create core acceptance tasks already present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
