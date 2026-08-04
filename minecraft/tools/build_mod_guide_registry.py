from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parent
MANIFEST_PATH = REPOSITORY_ROOT / "flame" / "manifest.json"
REGISTRY_PATH = ROOT / "config" / "mod_guide_registry.json"
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"


def load_existing() -> dict[int, dict]:
    if not REGISTRY_PATH.is_file():
        return {}
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {int(entry["project_id"]): entry for entry in data.get("projects", [])}


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    existing = load_existing()
    chapter_files = sorted(path.stem for path in CHAPTER_DIR.glob("*.snbt"))
    projects: list[dict] = []

    for file_entry in manifest.get("files", []):
        project_id = int(file_entry["projectID"])
        current = dict(existing.get(project_id, {}))
        current.setdefault("project_id", project_id)
        current["file_id"] = int(file_entry["fileID"])
        current["required"] = bool(file_entry.get("required", True))
        current.setdefault("name", "")
        current.setdefault("mod_id", "")
        current.setdefault("classification", "unclassified")
        current.setdefault("guide_tier", "unassigned")
        current.setdefault("quest_target", 0)
        current.setdefault("chapter", "")
        current.setdefault("guide_status", "missing")
        current.setdefault("notes", "")
        projects.append(current)

    projects.sort(key=lambda entry: entry["project_id"])
    output = {
        "schema_version": 1,
        "manifest_name": manifest.get("name", ""),
        "manifest_version": manifest.get("version", ""),
        "minecraft_version": manifest.get("minecraft", {}).get("version", ""),
        "classification_values": [
            "core_progression",
            "major_gameplay",
            "minor_gameplay",
            "worldgen_or_adventure",
            "quality_of_life",
            "optimization",
            "library_or_api",
            "compatibility",
            "server_or_admin",
            "unclassified"
        ],
        "guide_tier_values": ["core", "major", "minor", "reference", "none", "unassigned"],
        "guide_status_values": ["missing", "planned", "draft", "reviewed", "complete", "not_applicable"],
        "chapter_files_snapshot": chapter_files,
        "projects": projects
    }
    rendered = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
    previous = REGISTRY_PATH.read_text(encoding="utf-8") if REGISTRY_PATH.is_file() else ""
    if previous == rendered:
        print(f"Mod guide registry unchanged: {len(projects)} projects")
        return 0
    REGISTRY_PATH.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"Mod guide registry updated: {len(projects)} projects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
