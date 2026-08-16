from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Callable

ContentBuilder = Callable[[str, list[str]], dict[str, tuple[str, list[str]]]]


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


def extract_array(block: str, marker: str) -> tuple[int, int, str]:
    marker_index = block.find(marker)
    if marker_index < 0:
        raise RuntimeError(f"Missing {marker}")
    start = block.find("[", marker_index)
    if start < 0:
        raise RuntimeError(f"Missing list after {marker}")
    end = matching_delimiter(block, start, "[", "]")
    return start, end, block[start + 1 : end]


def quest_spans(text: str, chapter_name: str) -> list[tuple[int, int]]:
    marker = text.find("quests:")
    if marker < 0:
        raise RuntimeError(f"{chapter_name} chapter has no quests list")
    list_start = text.find("[", marker)
    list_end = matching_delimiter(text, list_start, "[", "]")
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


def remove_rewards(block: str, chapter_name: str) -> tuple[str, bool]:
    match = re.search(r"(?m)^\s*rewards:\s*", block)
    if not match:
        return block, False
    value_start = match.end()
    while value_start < len(block) and block[value_start].isspace():
        value_start += 1
    if value_start >= len(block) or block[value_start] not in "[{":
        raise RuntimeError(f"Unexpected {chapter_name} rewards value")
    opening = block[value_start]
    closing = "]" if opening == "[" else "}"
    value_end = matching_delimiter(block, value_start, opening, closing) + 1
    line_start = block.rfind("\n", 0, match.start()) + 1
    line_end = block.find("\n", value_end)
    if line_end < 0:
        line_end = value_end
    else:
        line_end += 1
    return block[:line_start] + block[line_end:], True


def quest_identity(block: str) -> tuple[str, list[str]]:
    quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not quest_match:
        raise RuntimeError("Catalogue quest without a valid ID")
    _, _, tasks_body = extract_array(block, "tasks:")
    resources = list(dict.fromkeys(re.findall(r'"([a-z0-9_.-]+:[a-z0-9_./-]+)"', tasks_body)))
    resources = [
        value for value in resources
        if value not in {"ftbfiltersystem:filter", "hostilenetworks:data_model"}
    ]
    if not resources:
        icon_match = re.search(r'icon:\s*\{(?:(?!\n\s*}).)*?id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', block, re.S)
        if icon_match:
            resources = [icon_match.group(1)]
    return quest_match.group(1), resources


def acceptance_id(namespace: str, quest_id: str) -> str:
    return hashlib.sha256(f"{namespace}_acceptance:{quest_id}".encode()).hexdigest()[:16].upper()


def add_acceptance_task(block: str, namespace: str, quest_id: str) -> tuple[str, bool]:
    task_id = acceptance_id(namespace, quest_id)
    if f'id: "{task_id}"' in block:
        return block, False
    _, list_end, _ = extract_array(block, "tasks:")
    insertion = (
        "\n\t\t\t{\n"
        f"\t\t\t\tid: \"{task_id}\"\n"
        "\t\t\t\ttype: \"checkmark\"\n"
        "\t\t\t}\n\t\t\t"
    )
    return block[:list_end] + insertion + block[list_end:], True


def render(value: str | list[str]) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def upsert(text: str, key: str, value: str | list[str]) -> str:
    rendered = f"\t{key}: {render(value)}\n"
    pattern = re.compile(rf"(?ms)^\t{re.escape(key)}:.*?(?=^\t[A-Za-z0-9_.-]+:|^\}}\s*$)")
    updated, count = pattern.subn(rendered, text, count=1)
    if count:
        return updated
    closing = text.rfind("}")
    if closing < 0:
        raise RuntimeError("Localization file has no closing brace")
    return text[:closing].rstrip() + "\n" + rendered + "}\n"


def upgrade_catalog(
    chapter_path: Path,
    lang_dir: Path,
    chapter_name: str,
    acceptance_namespace: str,
    content_builder: ContentBuilder,
) -> tuple[int, int, int]:
    text = chapter_path.read_text(encoding="utf-8")
    spans = quest_spans(text, chapter_name)
    replacements: list[tuple[int, int, str]] = []
    localization: dict[str, dict[str, str | list[str]]] = {"en_us": {}, "ru_ru": {}}
    rewards_removed = 0
    tasks_added = 0

    for start, end in spans:
        block = text[start:end]
        quest_id, resources = quest_identity(block)
        block, removed = remove_rewards(block, chapter_name)
        rewards_removed += int(removed)
        block, added = add_acceptance_task(block, acceptance_namespace, quest_id)
        tasks_added += int(added)
        replacements.append((start, end, block))

        content = content_builder(quest_id, resources)
        for locale, (title, description) in content.items():
            localization[locale][f"quest.{quest_id}.title"] = title
            localization[locale][f"quest.{quest_id}.quest_desc"] = description

    for start, end, block in reversed(replacements):
        text = text[:start] + block + text[end:]
    chapter_path.write_text(text, encoding="utf-8", newline="\n")

    for locale, entries in localization.items():
        path = lang_dir / f"{locale}.snbt"
        lang = path.read_text(encoding="utf-8")
        for key, value in entries.items():
            lang = upsert(lang, key, value)
        path.write_text(lang, encoding="utf-8", newline="\n")

    return len(spans), rewards_removed, tasks_added
