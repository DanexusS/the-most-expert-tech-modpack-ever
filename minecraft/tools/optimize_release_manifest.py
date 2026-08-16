from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "flame" / "manifest.json"

# Euphoria Patches is an add-on for Complementary Shaders. The release instance
# currently ships no compatible Complementary shader pack; runtime evidence from
# 2026-08-16 showed the patcher emitting repeated errors and starting a folder
# watcher while doing no useful work. Keep this exclusion exact and fail if the
# project is silently changed to a different file so the decision is reviewed.
EXCLUSIONS = {
    915902: {
        "file_id": 8177588,
        "name": "Euphoria Patches",
        "reason": "required Complementary shader is not shipped by the pack",
    }
}


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    files = manifest.get("files")
    if not isinstance(files, list):
        raise RuntimeError("CurseForge manifest has no files array")

    kept: list[dict] = []
    removed: list[tuple[int, int]] = []
    for entry in files:
        project_id = int(entry.get("projectID", -1))
        exclusion = EXCLUSIONS.get(project_id)
        if exclusion is None:
            kept.append(entry)
            continue

        file_id = int(entry.get("fileID", -1))
        expected_file_id = int(exclusion["file_id"])
        if file_id != expected_file_id:
            raise RuntimeError(
                f"Excluded project {project_id} changed fileID: {file_id} != {expected_file_id}; review required"
            )
        removed.append((project_id, file_id))

    if len(kept) == len(files):
        print("release_manifest_exclusions_removed: 0")
        print(f"release_manifest_projects: {len(files)}")
        return 0

    manifest["files"] = kept
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"release_manifest_exclusions_removed: {len(removed)}")
    for project_id, file_id in removed:
        print(f"removed_project: {project_id}/{file_id}")
    print(f"release_manifest_projects: {len(kept)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
