from __future__ import annotations

import re


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
    raise RuntimeError(f"Unclosed delimiter {opening!r} at {start}")


def field_marker(text: str, marker: str) -> re.Match[str]:
    field = marker[:-1] if marker.endswith(":") else marker
    match = re.search(rf"(?m)^\s*{re.escape(field)}\s*:\s*", text)
    if match is None:
        raise RuntimeError(f"Missing field {field}:")
    return match


def extract_array(text: str, marker: str) -> tuple[int, int, str]:
    match = field_marker(text, marker)
    start = text.find("[", match.end())
    if start < 0:
        raise RuntimeError(f"Missing list after {marker}")
    end = matching_delimiter(text, start, "[", "]")
    return start, end, text[start + 1 : end]


def quest_spans(text: str) -> list[tuple[int, int]]:
    list_start, list_end, _ = extract_array(text, "quests:")
    spans: list[tuple[int, int]] = []
    cursor = list_start + 1
    while cursor < list_end:
        start = text.find("{", cursor, list_end)
        if start < 0:
            break
        end = matching_delimiter(text, start, "{", "}")
        spans.append((start, end + 1))
        cursor = end + 1
    return spans
