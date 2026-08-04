from pathlib import Path
import collections
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []

for path in (ROOT / "kubejs").rglob("*.js"):
    result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
    if result.returncode:
        ERRORS.append(f"JS: {path}: {result.stderr.strip()}")

for path in (ROOT / "kubejs").rglob("*.json"):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        ERRORS.append(f"JSON: {path}: {exc}")

pairs = {"}": "{", "]": "["}
def balanced(text):
    stack = []
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
            if not stack or stack[-1][0] != pairs[char]:
                return False
            stack.pop()
    return not in_string and not stack

for path in (ROOT / "config" / "ftbquests").rglob("*.snbt"):
    if not balanced(path.read_text(encoding="utf-8")):
        ERRORS.append(f"SNBT balance: {path}")

chapter_dir = ROOT / "config" / "ftbquests" / "quests" / "chapters"
all_ids = []
dependencies = []
for path in chapter_dir.glob("*.snbt"):
    text = path.read_text(encoding="utf-8")
    all_ids.extend(re.findall(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', text))
    for block in re.findall(r'dependencies:\s*\[([^\]]*)\]', text, re.S):
        dependencies.extend(re.findall(r'"([0-9A-F]{16})"', block))

counter = collections.Counter(all_ids)
duplicates = [key for key, value in counter.items() if value > 1]
missing = sorted(set(dependencies) - set(counter))
if duplicates:
    ERRORS.append(f"Duplicate IDs: {duplicates}")
if missing:
    ERRORS.append(f"Missing dependencies: {missing}")

print("PASS" if not ERRORS else "FAIL")
print(f"IDs: {len(all_ids)} / unique: {len(counter)}")
print(f"Dependencies: {len(dependencies)} / missing: {len(missing)}")
for error in ERRORS:
    print(error)
sys.exit(1 if ERRORS else 0)
