from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
POLICY_PATH = ROOT / "config" / "expert_bypass_policy.json"
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"

ITEM_ID_RE = re.compile(r'(?m)^\s*id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"')


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


def top_level_object_spans(text: str, start: int, end: int) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    index = start
    while index < end:
        opening = text.find("{", index, end)
        if opening < 0:
            break
        closing = matching_delimiter(text, opening, "{", "}")
        if closing > end:
            raise RuntimeError("Reward object extends beyond reward array")
        spans.append((opening, closing + 1))
        index = closing + 1
    return spans


def reward_arrays(text: str) -> list[tuple[int, int]]:
    arrays: list[tuple[int, int]] = []
    offset = 0
    while True:
        marker = text.find("rewards:", offset)
        if marker < 0:
            break
        start = text.find("[", marker)
        if start < 0:
            break
        end = matching_delimiter(text, start, "[", "]")
        arrays.append((start, end))
        offset = end + 1
    return arrays


def reward_item_id(block: str) -> str | None:
    marker = block.find("item:")
    if marker < 0:
        return None
    item_start = block.find("{", marker)
    if item_start < 0:
        return None
    item_end = matching_delimiter(block, item_start, "{", "}")
    match = ITEM_ID_RE.search(block[item_start : item_end + 1])
    return match.group(1) if match else None


def remove_from_chapter(path: Path, forbidden: set[str]) -> tuple[int, list[str]]:
    text = path.read_text(encoding="utf-8")
    removals: list[tuple[int, int, str]] = []

    for array_start, array_end in reward_arrays(text):
        for object_start, object_end in top_level_object_spans(text, array_start + 1, array_end):
            item_id = reward_item_id(text[object_start:object_end])
            if item_id in forbidden:
                # Remove indentation immediately before the object but preserve
                # the line containing the opening square bracket.
                start = object_start
                while start > array_start + 1 and text[start - 1] in " \t":
                    start -= 1
                if start > array_start + 1 and text[start - 1] == "\n":
                    start -= 1
                removals.append((start, object_end, item_id))

    if not removals:
        return 0, []

    removed_items: list[str] = []
    for start, end, item_id in sorted(removals, reverse=True):
        text = text[:start] + text[end:]
        removed_items.append(item_id)

    path.write_text(text, encoding="utf-8", newline="\n")
    return len(removals), sorted(removed_items)


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    gated = {
        item
        for stage in contract.get("stages", [])
        for item in stage.get("gated_outputs", [])
    }
    allowlist = set(policy.get("quest_reward_allowlist", []))
    forbidden = gated - allowlist

    total = 0
    for path in sorted(CHAPTER_DIR.glob("*.snbt")):
        count, items = remove_from_chapter(path, forbidden)
        if count:
            total += count
            print(f"{path.name}: removed {count} gated rewards: {', '.join(items)}")

    print(f"Removed gated quest reward objects: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
