from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


def stable_id(namespace: str) -> str:
    return hashlib.sha256(namespace.encode("utf-8")).hexdigest()[:16].upper()


def format_array(values: list[str]) -> str:
    return "[" + ",".join(json.dumps(value, ensure_ascii=False) for value in values) + "]"


def upsert_localization(text: str, key: str, value: str) -> str:
    rendered = f"\t{key}: {value}\n"
    pattern = re.compile(rf"(?ms)^\t{re.escape(key)}:.*?(?=^\t[A-Za-z0-9_.-]+:|^\}}\s*$)")
    updated, count = pattern.subn(rendered, text, count=1)
    if count:
        return updated
    closing = text.rfind("}")
    if closing < 0:
        raise RuntimeError("Localization file has no closing brace")
    return text[:closing].rstrip() + "\n" + rendered + "}\n"


def generate_manual_data(root: Path, data: dict) -> tuple[int, bool]:
    chapter_dir = root / "config" / "ftbquests" / "quests" / "chapters"
    lang_dir = root / "config" / "ftbquests" / "quests" / "lang"
    chapter_path = chapter_dir / f"{data['filename']}.snbt"
    chapter_id = stable_id(f"chapter:{data['filename']}")
    quest_blocks: list[str] = []
    localization: dict[str, dict[str, str]] = {"en_us": {}, "ru_ru": {}}
    localization["en_us"][f"chapter.{chapter_id}.title"] = json.dumps(data["title_en"], ensure_ascii=False)
    localization["ru_ru"][f"chapter.{chapter_id}.title"] = json.dumps(data["title_ru"], ensure_ascii=False)

    quest_total = 0
    for module_index, module in enumerate(data["modules"]):
        previous_id = ""
        for lesson_index, lesson in enumerate(module["lessons"]):
            quest_total += 1
            quest_id = stable_id(f"{data['filename']}:{module['slug']}:{lesson['slug']}")
            task_id = stable_id(f"{data['filename']}:task:{module['slug']}:{lesson['slug']}")
            dependencies = f"\n\t\t\tdependencies: [\"{previous_id}\"]" if previous_id else ""
            quest_blocks.append(
                "\t\t{" + dependencies + "\n"
                f"\t\t\ticon: {{ id: \"{lesson['icon']}\" }}\n"
                f"\t\t\tid: \"{quest_id}\"\n"
                "\t\t\tshape: \"hexagon\"\n"
                "\t\t\ttasks: [{\n"
                f"\t\t\t\tid: \"{task_id}\"\n"
                "\t\t\t\ttype: \"checkmark\"\n"
                "\t\t\t}]\n"
                f"\t\t\tx: {module_index * float(data.get('module_spacing', 8)):.1f}d\n"
                f"\t\t\ty: {lesson_index * float(data.get('lesson_spacing', 2)):.1f}d\n"
                "\t\t}"
            )
            localization["en_us"][f"quest.{quest_id}.title"] = json.dumps(lesson["title_en"], ensure_ascii=False)
            localization["ru_ru"][f"quest.{quest_id}.title"] = json.dumps(lesson["title_ru"], ensure_ascii=False)
            localization["en_us"][f"quest.{quest_id}.quest_desc"] = format_array(lesson["desc_en"])
            localization["ru_ru"][f"quest.{quest_id}.quest_desc"] = format_array(lesson["desc_ru"])
            previous_id = quest_id

    chapter = (
        "{\n"
        "\tdefault_hide_dependency_lines: false\n"
        "\tdefault_quest_shape: \"hexagon\"\n"
        f"\tfilename: \"{data['filename']}\"\n"
        f"\tgroup: \"{data.get('group', '177A10C99EDDA376')}\"\n"
        f"\ticon: {{ id: \"{data['icon']}\" }}\n"
        f"\tid: \"{chapter_id}\"\n"
        f"\torder_index: {int(data.get('order_index', 5))}\n"
        "\tprogression_mode: \"flexible\"\n"
        "\tquest_links: []\n"
        "\tquests: [\n"
        + "\n".join(quest_blocks)
        + "\n\t]\n}\n"
    )

    previous = chapter_path.read_text(encoding="utf-8") if chapter_path.exists() else ""
    changed = previous != chapter
    if changed:
        chapter_path.write_text(chapter, encoding="utf-8", newline="\n")

    for locale, entries in localization.items():
        path = lang_dir / f"{locale}.snbt"
        text = path.read_text(encoding="utf-8")
        original = text
        for key, value in entries.items():
            text = upsert_localization(text, key, value)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            changed = True

    print(f"{data['filename']}: {quest_total} quests; {'updated' if changed else 'unchanged'}")
    return quest_total, changed


def generate_manual(root: Path, data_path: Path) -> tuple[int, bool]:
    return generate_manual_data(root, json.loads(data_path.read_text(encoding="utf-8")))
