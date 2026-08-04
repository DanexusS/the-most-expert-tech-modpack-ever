from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "config" / "mod_guide_registry.json"
REPORT_PATH = ROOT / "docs" / "MOD_GUIDE_COVERAGE_REPORT.md"

USER_FACING = {
    "core_progression",
    "major_gameplay",
    "minor_gameplay",
    "worldgen_or_adventure",
    "quality_of_life",
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
    unclassified = [entry for entry in projects if entry.get("classification") == "unclassified"]
    user_facing = [entry for entry in projects if entry.get("classification") in USER_FACING]
    missing_user_guides = [
        entry for entry in user_facing
        if entry.get("guide_status") not in {"reviewed", "complete"}
    ]
    target_failures: list[dict] = []
    for entry in projects:
        tier = entry.get("guide_tier", "unassigned")
        minimum = MIN_TARGETS.get(tier, 0)
        if int(entry.get("quest_target", 0)) < minimum:
            target_failures.append(entry)
        if entry.get("classification") in USER_FACING and not entry.get("chapter"):
            target_failures.append(entry)

    quest_target = sum(int(entry.get("quest_target", 0)) for entry in projects)
    complete_count = sum(entry.get("guide_status") == "complete" for entry in projects)
    reviewed_count = sum(entry.get("guide_status") == "reviewed" for entry in projects)
    return {
        "total_projects": len(projects),
        "classifications": classifications,
        "statuses": statuses,
        "unclassified": unclassified,
        "user_facing": user_facing,
        "missing_user_guides": missing_user_guides,
        "target_failures": target_failures,
        "quest_target": quest_target,
        "complete_count": complete_count,
        "reviewed_count": reviewed_count,
    }


def project_label(entry: dict) -> str:
    name = entry.get("name") or entry.get("mod_id") or f"CurseForge project {entry['project_id']}"
    return f"{name} (`{entry['project_id']}`)"


def render(result: dict) -> str:
    blocking = bool(
        result["unclassified"]
        or result["missing_user_guides"]
        or result["target_failures"]
        or not 5000 <= result["quest_target"] <= 6000
    )
    lines = [
        "# Mod Guide Coverage Report",
        "",
        f"**{'IN PROGRESS' if blocking else 'PASS'}**",
        "",
        "The registry is sourced from the pack manifest. Every manifest project must be classified before v1; every user-facing project must have a reviewed or complete guide.",
        "",
        "## Summary",
        "",
        f"- Manifest projects: **{result['total_projects']}**",
        f"- User-facing projects: **{len(result['user_facing'])}**",
        f"- Unclassified projects: **{len(result['unclassified'])}**",
        f"- User-facing guides not reviewed: **{len(result['missing_user_guides'])}**",
        f"- Reviewed guides: **{result['reviewed_count']}**",
        f"- Complete guides: **{result['complete_count']}**",
        f"- Registry quest target: **{result['quest_target']}**",
        "",
        "## Classification totals",
        "",
    ]
    for key, value in sorted(result["classifications"].items()):
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Guide status totals", ""])
    for key, value in sorted(result["statuses"].items()):
        lines.append(f"- `{key}`: {value}")

    if result["unclassified"]:
        lines.extend(["", "## Next projects requiring classification", ""])
        for entry in result["unclassified"][:100]:
            lines.append(f"- {project_label(entry)}; file `{entry['file_id']}`")
        if len(result["unclassified"]) > 100:
            lines.append(f"- ...and {len(result['unclassified']) - 100} more")

    if result["missing_user_guides"]:
        lines.extend(["", "## User-facing guides not yet reviewed", ""])
        for entry in result["missing_user_guides"][:100]:
            lines.append(
                f"- {project_label(entry)}: tier `{entry.get('guide_tier')}`, "
                f"status `{entry.get('guide_status')}`, target {entry.get('quest_target')}"
            )
        if len(result["missing_user_guides"]) > 100:
            lines.append(f"- ...and {len(result['missing_user_guides']) - 100} more")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    result = audit(load_registry())
    REPORT_PATH.write_text(render(result), encoding="utf-8", newline="\n")
    blocking = bool(
        result["unclassified"]
        or result["missing_user_guides"]
        or result["target_failures"]
        or not 5000 <= result["quest_target"] <= 6000
    )
    print(f"mod_guide_coverage: {'IN PROGRESS' if blocking else 'PASS'}")
    print(f"projects: {result['total_projects']}")
    print(f"unclassified: {len(result['unclassified'])}")
    print(f"user_facing_missing: {len(result['missing_user_guides'])}")
    print(f"registry_quest_target: {result['quest_target']}")
    return 1 if args.strict and blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
