from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "config" / "mod_guide_registry.json"
REPORT_PATH = ROOT / "docs" / "MOD_GUIDE_COVERAGE_REPORT.md"

# Only projects explicitly selected as having meaningful player-facing content
# or progression impact are release-gated. Manifest libraries, APIs, renderers,
# compatibility layers and minor service mods do not need individual chapters.
TRACKED_GAMEPLAY = {
    "core_progression",
    "major_gameplay",
    "minor_gameplay",
    "worldgen_or_adventure",
}

MIN_TARGETS = {
    "core": 35,
    "major": 15,
    "minor": 4,
    "reference": 1,
    "none": 0,
    "unassigned": 0,
}


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def audit(registry: dict) -> dict:
    projects = registry.get("projects", [])
    classifications = Counter(entry.get("classification", "unclassified") for entry in projects)
    statuses = Counter(entry.get("guide_status", "missing") for entry in projects)
    tracked = [entry for entry in projects if entry.get("classification") in TRACKED_GAMEPLAY]
    not_selected = [entry for entry in projects if entry not in tracked]
    missing_guides = [
        entry for entry in tracked
        if entry.get("guide_status") not in {"reviewed", "complete"}
    ]

    target_failures: list[dict] = []
    for entry in tracked:
        tier = entry.get("guide_tier", "unassigned")
        minimum = MIN_TARGETS.get(tier, 0)
        if int(entry.get("quest_target", 0)) < minimum or not entry.get("chapter"):
            target_failures.append(entry)

    return {
        "total_projects": len(projects),
        "classifications": classifications,
        "statuses": statuses,
        "tracked": tracked,
        "not_selected": not_selected,
        "missing_guides": missing_guides,
        "target_failures": target_failures,
        "quest_target": sum(int(entry.get("quest_target", 0)) for entry in tracked),
        "complete_count": sum(entry.get("guide_status") == "complete" for entry in tracked),
        "reviewed_count": sum(entry.get("guide_status") == "reviewed" for entry in tracked),
    }


def project_label(entry: dict) -> str:
    name = entry.get("name") or entry.get("mod_id") or f"CurseForge project {entry['project_id']}"
    return f"{name} (`{entry['project_id']}`)"


def is_blocking(result: dict) -> bool:
    return bool(result["missing_guides"] or result["target_failures"] or not result["tracked"])


def render(result: dict) -> str:
    blocking = is_blocking(result)
    lines = [
        "# Gameplay Guide Coverage Report",
        "",
        f"**{'IN PROGRESS' if blocking else 'PASS'}**",
        "",
        "The manifest is an inventory, not a requirement for 501 separate quest chapters. v1 gates only explicitly selected mods with meaningful gameplay, progression, world-generation or adventure content. Libraries, APIs, renderers, compatibility layers, optimizers and minor service mods are non-blocking unless they materially affect progression.",
        "",
        "## Summary",
        "",
        f"- Manifest projects: **{result['total_projects']}**",
        f"- Tracked gameplay/progression projects: **{len(result['tracked'])}**",
        f"- Manifest projects not selected for individual guides: **{len(result['not_selected'])}**",
        f"- Tracked guides not reviewed: **{len(result['missing_guides'])}**",
        f"- Reviewed tracked guides: **{result['reviewed_count']}**",
        f"- Complete tracked guides: **{result['complete_count']}**",
        f"- Tracked guide quest target: **{result['quest_target']}**",
        f"- Coverage blockers: **{len(result['missing_guides']) + len(result['target_failures'])}**",
        "",
        "## Tracked classification totals",
        "",
    ]
    tracked_counts = Counter(entry.get("classification", "unclassified") for entry in result["tracked"])
    for key, value in sorted(tracked_counts.items()):
        lines.append(f"- `{key}`: {value}")

    if result["missing_guides"]:
        lines.extend(["", "## Tracked guides requiring review", ""])
        for entry in result["missing_guides"]:
            lines.append(
                f"- {project_label(entry)}: tier `{entry.get('guide_tier')}`, "
                f"status `{entry.get('guide_status')}`, target {entry.get('quest_target')}, "
                f"chapter `{entry.get('chapter')}`"
            )

    if result["target_failures"]:
        lines.extend(["", "## Invalid tracked guide plans", ""])
        for entry in result["target_failures"]:
            lines.append(
                f"- {project_label(entry)}: tier `{entry.get('guide_tier')}`, "
                f"target {entry.get('quest_target')}, chapter `{entry.get('chapter')}`"
            )

    lines.extend([
        "",
        "## Non-blocking manifest remainder",
        "",
        "Projects outside the tracked set do not require individual quest chapters. They are reviewed only when they expose recipes, loot, resource generation, combat power or another progression bypass.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    result = audit(load_registry())
    REPORT_PATH.write_text(render(result), encoding="utf-8", newline="\n")
    blocking = is_blocking(result)
    print(f"gameplay_guide_coverage: {'IN PROGRESS' if blocking else 'PASS'}")
    print(f"manifest_projects: {result['total_projects']}")
    print(f"tracked_projects: {len(result['tracked'])}")
    print(f"not_selected: {len(result['not_selected'])}")
    print(f"tracked_guides_missing_review: {len(result['missing_guides'])}")
    print(f"tracked_quest_target: {result['quest_target']}")
    return 1 if args.strict and blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
