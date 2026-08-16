from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
KEY_RE = re.compile(r"(?m)^\t([A-Za-z0-9_.-]+):")


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


def quest_spans(text: str) -> list[tuple[int, int]]:
    marker = text.find("quests:")
    if marker < 0:
        raise RuntimeError("Chapter has no quests list")
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


def remove_rewards(block: str) -> tuple[str, bool]:
    match = re.search(r"(?m)^\s*rewards:\s*", block)
    if not match:
        return block, False
    value_start = match.end()
    while value_start < len(block) and block[value_start].isspace():
        value_start += 1
    if value_start >= len(block) or block[value_start] not in "[{":
        raise RuntimeError("Unexpected rewards value")
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


def acceptance_id(namespace: str, quest_id: str) -> str:
    return hashlib.sha256(f"{namespace}:{quest_id}".encode()).hexdigest()[:16].upper()


def add_acceptance_task(block: str, quest_id: str, namespace: str) -> tuple[str, bool]:
    _, list_end, body = extract_array(block, "tasks:")
    if re.search(r'(?m)^\s*type:\s*"checkmark"', body):
        return block, False
    task_id = acceptance_id(namespace, quest_id)
    insertion = (
        "\n\t\t\t{\n"
        f"\t\t\t\tid: \"{task_id}\"\n"
        "\t\t\t\ttype: \"checkmark\"\n"
        "\t\t\t}\n\t\t\t"
    )
    return block[:list_end] + insertion + block[list_end:], True


def quest_identity(block: str) -> tuple[str, list[str]]:
    quest_match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not quest_match:
        raise RuntimeError("Quest without a valid ID")
    _, _, tasks_body = extract_array(block, "tasks:")
    direct = re.findall(r'id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', tasks_body)
    tagged = re.findall(r'item_tag\(([a-z0-9_.-]+:[a-z0-9_./-]+)\)', tasks_body)
    items = list(dict.fromkeys(tagged + direct))
    if tagged:
        items = [item for item in items if item != "ftbfiltersystem:smart_filter"]
    return quest_match.group(1), items


def human_name(item_id: str) -> str:
    return item_id.split(":", 1)[1].replace("_", " ").replace("/", " ").title()


def select_category(policy: dict, item_id: str | None) -> dict:
    if item_id is None:
        return policy["checkpoint"]
    namespace, path = item_id.split(":", 1)
    if namespace != policy["primary_namespace"]:
        return policy["cross_mod"]
    for category in policy["categories"]:
        if any(token in path for token in category["tokens"]):
            return category
    return policy["default"]


def localized_content(policy: dict, items: list[str], quest_id: str) -> dict[str, tuple[str, list[str]]]:
    if items:
        display = " / ".join(human_name(item) for item in items[:4])
        category = select_category(policy, items[0])
    else:
        display = f"{policy['checkpoint_name']} {quest_id[-4:]}"
        category = select_category(policy, None)

    en_desc = [
        policy["description_en"].format(display=display, role=category["role_en"]),
        policy["acceptance_en"].format(focus=category["focus_en"]),
    ]
    ru_desc = [
        policy["description_ru"].format(display=display, role=category["role_ru"]),
        policy["acceptance_ru"].format(focus=category["focus_ru"]),
    ]
    return {
        "en_us": (f"{display} — {policy['title_suffix_en']}", en_desc),
        "ru_ru": (f"{display} — {policy['title_suffix_ru']}", ru_desc),
    }


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


def load_policy(path: Path) -> dict:
    policy = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "chapter_filename", "chapter_id", "chapter_title_en", "chapter_title_ru",
        "report_filename", "expected_quests", "primary_namespace", "acceptance_namespace",
        "checkpoint_name", "title_suffix_en", "title_suffix_ru", "description_en",
        "description_ru", "acceptance_en", "acceptance_ru", "categories", "default",
        "cross_mod", "checkpoint",
    }
    missing = sorted(required - set(policy))
    if missing:
        raise RuntimeError(f"Policy {path} missing fields: {', '.join(missing)}")
    return policy


def upgrade(policy: dict) -> None:
    chapter_path = ROOT / "config" / "ftbquests" / "quests" / "chapters" / f"{policy['chapter_filename']}.snbt"
    text = chapter_path.read_text(encoding="utf-8")
    spans = quest_spans(text)
    replacements: list[tuple[int, int, str]] = []
    localization: dict[str, dict[str, str | list[str]]] = {"en_us": {}, "ru_ru": {}}
    rewards_removed = 0
    tasks_added = 0

    for start, end in spans:
        block = text[start:end]
        quest_id, items = quest_identity(block)
        block, removed = remove_rewards(block)
        rewards_removed += int(removed)
        block, added = add_acceptance_task(block, quest_id, policy["acceptance_namespace"])
        tasks_added += int(added)
        replacements.append((start, end, block))
        content = localized_content(policy, items, quest_id)
        for locale, (title, desc) in content.items():
            localization[locale][f"quest.{quest_id}.title"] = title
            localization[locale][f"quest.{quest_id}.quest_desc"] = desc

    for start, end, block in reversed(replacements):
        text = text[:start] + block + text[end:]
    chapter_path.write_text(text, encoding="utf-8", newline="\n")

    for locale, entries in localization.items():
        path = LANG_DIR / f"{locale}.snbt"
        language = path.read_text(encoding="utf-8")
        for key, value in entries.items():
            language = upsert(language, key, value)
        language = upsert(
            language,
            f"chapter.{policy['chapter_id']}.title",
            policy["chapter_title_en"] if locale == "en_us" else policy["chapter_title_ru"],
        )
        path.write_text(language, encoding="utf-8", newline="\n")

    print(f"catalog: {policy['chapter_filename']}")
    print(f"quests: {len(spans)}")
    print(f"rewards_removed: {rewards_removed}")
    print(f"acceptance_tasks_added: {tasks_added}")


def parse_localization(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    matches = list(KEY_RE.finditer(text))
    values: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else text.rfind("}")
        values[match.group(1)] = text[start:end].strip()
    return values


def visible_length(raw: str) -> int:
    return len(" ".join(re.findall(r'"((?:\\.|[^"\\])*)"', raw)))


def task_types(block: str) -> list[str]:
    _, _, body = extract_array(block, "tasks:")
    return re.findall(r'(?m)^\s*type:\s*"([a-z0-9_]+)"', body)


def gate(policy: dict) -> int:
    chapter_path = ROOT / "config" / "ftbquests" / "quests" / "chapters" / f"{policy['chapter_filename']}.snbt"
    report_path = ROOT / "docs" / policy["report_filename"]
    chapter = chapter_path.read_text(encoding="utf-8")
    en = parse_localization(LANG_DIR / "en_us.snbt")
    ru = parse_localization(LANG_DIR / "ru_ru.snbt")
    failures: list[str] = []
    rows: list[tuple[str, str, int, int, int, bool, str]] = []
    spans = quest_spans(chapter)
    expected = int(policy["expected_quests"])
    minimum = int(policy.get("minimum_description", 180))
    if len(spans) != expected:
        failures.append(f"Expected {expected} quests, found {len(spans)}")

    for start, end in spans:
        block = chapter[start:end]
        quest_id, items = quest_identity(block)
        types = task_types(block)
        no_rewards = "rewards:" not in block
        desc_key = f"quest.{quest_id}.quest_desc"
        title_key = f"quest.{quest_id}.title"
        en_length = visible_length(en.get(desc_key, ""))
        ru_length = visible_length(ru.get(desc_key, ""))
        label = ", ".join(items[:4]) if items else f"checkpoint:{quest_id}"
        status = "PASS"
        if types.count("checkmark") < 1:
            failures.append(f"{label}: no practical acceptance task")
            status = "FAIL"
        if not no_rewards:
            failures.append(f"{label}: quest reward remains")
            status = "FAIL"
        if title_key not in en or title_key not in ru:
            failures.append(f"{label}: missing bilingual title")
            status = "FAIL"
        if en_length < minimum or ru_length < minimum:
            failures.append(f"{label}: description too short (EN {en_length}, RU {ru_length})")
            status = "FAIL"
        rows.append((label, quest_id, len(types), en_length, ru_length, no_rewards, status))

    lines = [
        f"# {policy['report_title']}",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        policy["report_intro"],
        "",
        "| Gate | Quest | Tasks | EN description | RU description | No rewards | Status |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for label, quest_id, tasks, en_length, ru_length, no_rewards, status in rows:
        lines.append(
            f"| `{label}` | `{quest_id}` | {tasks} | {en_length} | {ru_length} | "
            f"{'yes' if no_rewards else 'no'} | {status} |"
        )
    lines.extend([
        "",
        "## Aggregate",
        "",
        f"- Quests: **{len(rows)}**",
        f"- Reward-free: **{sum(row[5] for row in rows)}**",
        f"- Fully bilingual: **{sum(row[3] >= minimum and row[4] >= minimum for row in rows)}**",
        f"- Failures: **{len(failures)}**",
        "",
    ])
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"catalog_quality: {'PASS' if not failures else 'FAIL'}")
    print(f"chapter: {policy['chapter_filename']}")
    print(f"quests: {len(rows)}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("upgrade", "gate"))
    parser.add_argument("policy", type=Path)
    args = parser.parse_args()
    policy_path = args.policy if args.policy.is_absolute() else ROOT / args.policy
    policy = load_policy(policy_path)
    if args.mode == "upgrade":
        upgrade(policy)
        return 0
    return gate(policy)


if __name__ == "__main__":
    sys.exit(main())
