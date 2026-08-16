from __future__ import annotations

import collections
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []
METRICS: dict[str, int] = collections.defaultdict(int)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def require_directory(path: Path) -> None:
    if not path.is_dir():
        ERRORS.append(f"Missing required directory: {relative(path)}")


def check_javascript() -> None:
    scripts = sorted((ROOT / "kubejs").rglob("*.js"))
    METRICS["javascript_files"] = len(scripts)
    node = shutil.which("node")
    if scripts and node is None:
        ERRORS.append("Node.js is required to validate KubeJS scripts")
        return

    for path in scripts:
        result = subprocess.run(
            [node, "--check", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            ERRORS.append(f"JS syntax: {relative(path)}: {result.stderr.strip()}")


def check_json() -> None:
    paths = sorted((ROOT / "kubejs").rglob("*.json"))
    METRICS["kubejs_json_files"] = len(paths)
    for path in paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            ERRORS.append(f"JSON: {relative(path)}: {exc}")


PAIRS = {"}": "{", "]": "["}


def balanced(text: str) -> bool:
    stack: list[tuple[str, int]] = []
    in_string = False
    escaped = False
    for index, char in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char in "{[":
            stack.append((char, index))
        elif char in "}]":
            if not stack or stack[-1][0] != PAIRS[char]:
                return False
            stack.pop()

    return not in_string and not stack


def check_snbt_balance() -> None:
    paths = sorted((ROOT / "config" / "ftbquests").rglob("*.snbt"))
    METRICS["snbt_files"] = len(paths)
    for path in paths:
        if not balanced(path.read_text(encoding="utf-8")):
            ERRORS.append(f"SNBT balance: {relative(path)}")


def check_quest_graph() -> None:
    chapter_dir = ROOT / "config" / "ftbquests" / "quests" / "chapters"
    chapter_paths = sorted(chapter_dir.glob("*.snbt"))
    METRICS["quest_chapters"] = len(chapter_paths)

    all_ids: list[str] = []
    dependencies: list[str] = []

    for path in chapter_paths:
        text = path.read_text(encoding="utf-8")
        all_ids.extend(re.findall(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', text))
        for block in re.findall(r'dependencies:\s*\[([^\]]*)\]', text, re.S):
            dependencies.extend(re.findall(r'"([0-9A-F]{16})"', block))

    counter = collections.Counter(all_ids)
    duplicates = sorted(key for key, value in counter.items() if value > 1)
    missing = sorted(set(dependencies) - set(counter))

    METRICS["ftb_object_ids"] = len(all_ids)
    METRICS["unique_ftb_object_ids"] = len(counter)
    METRICS["quest_dependencies"] = len(dependencies)
    METRICS["missing_dependencies"] = len(missing)

    if duplicates:
        ERRORS.append(f"Duplicate FTB object IDs: {duplicates}")
    if missing:
        ERRORS.append(f"Missing quest dependencies: {missing}")


LANG_KEY_RE = re.compile(r'^\s*([A-Za-z0-9_.-]+):')


def parse_lang_keys(path: Path) -> tuple[list[str], set[str]]:
    ordered: list[str] = []
    if not path.is_file():
        ERRORS.append(f"Missing localization file: {relative(path)}")
        return ordered, set()

    for line in path.read_text(encoding="utf-8").splitlines():
        match = LANG_KEY_RE.match(line)
        if match:
            ordered.append(match.group(1))

    duplicates = sorted(key for key, count in collections.Counter(ordered).items() if count > 1)
    if duplicates:
        ERRORS.append(f"Duplicate localization keys in {relative(path)}: {duplicates}")
    return ordered, set(ordered)


def check_localizations() -> None:
    lang_dir = ROOT / "config" / "ftbquests" / "quests" / "lang"
    en_ordered, en_keys = parse_lang_keys(lang_dir / "en_us.snbt")
    ru_ordered, ru_keys = parse_lang_keys(lang_dir / "ru_ru.snbt")

    METRICS["en_us_keys"] = len(en_ordered)
    METRICS["ru_ru_keys"] = len(ru_ordered)
    METRICS["missing_in_en_us"] = len(ru_keys - en_keys)
    METRICS["missing_in_ru_ru"] = len(en_keys - ru_keys)

    if ru_keys - en_keys:
        WARNINGS.append(f"Localization keys missing in en_us: {len(ru_keys - en_keys)}")
    if en_keys - ru_keys:
        WARNINGS.append(f"Localization keys missing in ru_ru: {len(en_keys - ru_keys)}")


RECIPE_ID_RE = re.compile(r"\.id\(\s*['\"]([^'\"]+)['\"]\s*\)")


def check_kubejs_recipe_ids() -> None:
    ids: list[str] = []
    for path in sorted((ROOT / "kubejs" / "server_scripts").rglob("*.js")):
        ids.extend(RECIPE_ID_RE.findall(path.read_text(encoding="utf-8")))

    duplicates = sorted(key for key, count in collections.Counter(ids).items() if count > 1)
    METRICS["explicit_recipe_ids"] = len(ids)
    METRICS["duplicate_recipe_ids"] = len(duplicates)
    if duplicates:
        ERRORS.append(f"Duplicate explicit KubeJS recipe IDs: {duplicates}")


def check_repository_hygiene() -> None:
    generated = [
        ROOT / "command_history.txt",
        ROOT / "logs",
        ROOT / "crash-reports",
        ROOT / "saves",
    ]
    present = [relative(path) for path in generated if path.exists()]
    METRICS["tracked_runtime_artifacts"] = len(present)
    if present:
        WARNINGS.append("Runtime artifacts present in source tree: " + ", ".join(present))


def main() -> int:
    for required in (
        ROOT / "config" / "ftbquests" / "quests",
        ROOT / "kubejs" / "server_scripts",
        ROOT / "kubejs" / "startup_scripts",
    ):
        require_directory(required)

    check_javascript()
    check_json()
    check_snbt_balance()
    check_quest_graph()
    check_localizations()
    check_kubejs_recipe_ids()
    check_repository_hygiene()

    print("PASS" if not ERRORS else "FAIL")
    for key in sorted(METRICS):
        print(f"{key}: {METRICS[key]}")
    for warning in WARNINGS:
        print(f"WARNING: {warning}")
    for error in ERRORS:
        print(f"ERROR: {error}")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
