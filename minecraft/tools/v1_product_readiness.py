from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "V1_PRODUCT_READINESS.md"
EVIDENCE_PATH = ROOT / "config" / "v1_runtime_evidence.json"

REPORTS = {
    "Theoretical balance": ROOT / "docs" / "THEORETICAL_BALANCE_REPORT.md",
    "Quest quality": ROOT / "docs" / "QUEST_QUALITY_REPORT.md",
    "Curated manuals": ROOT / "docs" / "ALL_MANUAL_QUALITY_REPORT.md",
    "Progression contract": ROOT / "docs" / "PROGRESSION_CONTRACT_REPORT.md",
    "Recipe dependency graph": ROOT / "docs" / "RECIPE_DEPENDENCY_REPORT.md",
    "Bypass closure": ROOT / "docs" / "BYPASS_AUDIT_REPORT.md",
    "Selected gameplay guide coverage": ROOT / "docs" / "MOD_GUIDE_COVERAGE_REPORT.md",
    "Create route": ROOT / "docs" / "CREATE_CORE_QUALITY_REPORT.md",
    "Immersive Engineering route": ROOT / "docs" / "IE_CORE_QUALITY_REPORT.md",
    "Modern Industrialization route": ROOT / "docs" / "MI_CORE_QUALITY_REPORT.md",
    "Applied Energistics 2 route": ROOT / "docs" / "AE2_CORE_QUALITY_REPORT.md",
    "Mekanism route": ROOT / "docs" / "MEKANISM_CORE_QUALITY_REPORT.md",
    "Simply Swords catalogue": ROOT / "docs" / "SIMPLY_SWORDS_QUALITY_REPORT.md",
    "Powah catalogue": ROOT / "docs" / "POWAH_QUALITY_REPORT.md",
}

MINIMUM_RUNTIME_GATES = {
    "clean_client_start",
    "new_world_create_save_reopen",
    "kubejs_milestone_items_exist",
    "strategic_recipes_verified",
    "representative_quest_tasks_complete",
    "language_switch_verified",
    "second_clean_restart_and_world_reopen",
}


def report_pass(path: Path) -> bool:
    return path.is_file() and "**PASS**" in path.read_text(encoding="utf-8")


def integer(text: str, pattern: str) -> int:
    match = re.search(pattern, text)
    return int(match.group(1).replace(",", "")) if match else 0


def quest_metrics() -> dict[str, int | float]:
    text = (ROOT / "docs" / "QUEST_QUALITY_REPORT.md").read_text(encoding="utf-8")
    quests = integer(text, r"Quests parsed:\s*\*\*([0-9,]+)\*\*")
    bilingual = integer(text, r"Bilingual quest descriptions:\s*\*\*([0-9,]+)")
    item_only = integer(text, r"Single item-only quests:\s*\*\*([0-9,]+)\*\*")
    return {
        "quests": quests,
        "bilingual": bilingual,
        "item_only": item_only,
        "item_only_ratio": item_only / max(1, quests),
    }


def guide_metrics() -> dict[str, int]:
    text = (ROOT / "docs" / "MOD_GUIDE_COVERAGE_REPORT.md").read_text(encoding="utf-8")
    return {
        "manifest": integer(text, r"Manifest projects:\s*\*\*([0-9,]+)\*\*"),
        "tracked": integer(text, r"Tracked gameplay/progression projects:\s*\*\*([0-9,]+)\*\*"),
        "not_selected": integer(text, r"Manifest projects not selected for individual guides:\s*\*\*([0-9,]+)\*\*"),
        "missing_review": integer(text, r"Tracked guides not reviewed:\s*\*\*([0-9,]+)\*\*"),
        "reviewed": integer(text, r"Reviewed tracked guides:\s*\*\*([0-9,]+)\*\*"),
        "complete": integer(text, r"Complete tracked guides:\s*\*\*([0-9,]+)\*\*"),
        "blockers": integer(text, r"Coverage blockers:\s*\*\*([0-9,]+)\*\*"),
    }


def main() -> int:
    status = {name: report_pass(path) for name, path in REPORTS.items()}
    quests = quest_metrics()
    guides = guide_metrics()
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    runtime = {name: bool(evidence.get("gates", {}).get(name, False)) for name in MINIMUM_RUNTIME_GATES}

    quest_volume = 5000 <= quests["quests"] <= 6000
    full_bilingual = quests["quests"] > 0 and quests["bilingual"] == quests["quests"]
    quest_structure = quests["item_only_ratio"] <= 0.30
    guide_complete = guides["tracked"] > 0 and guides["missing_review"] == 0 and guides["blockers"] == 0
    static_complete = all(status.values()) and quest_volume and full_bilingual and quest_structure and guide_complete
    runtime_complete = all(runtime.values())

    if static_complete and runtime_complete:
        classification = "V1"
    elif static_complete:
        classification = "V1 CANDIDATE — MINIMUM RUNTIME EVIDENCE REQUIRED"
    elif all(status.values()):
        classification = "STATIC FOUNDATION PASS — PRODUCT INCOMPLETE"
    else:
        classification = "DEVELOPMENT — STATIC GATES INCOMPLETE"

    lines = [
        "# v1 Product Readiness",
        "",
        f"## Classification: **{classification}**",
        "",
        "## Static reports",
        "",
        "| Gate | Status |",
        "|---|---|",
    ]
    for name, passed in status.items():
        lines.append(f"| {name} | {'PASS' if passed else 'IN PROGRESS / FAIL'} |")

    lines.extend([
        "",
        "## Quest product specification",
        "",
        "| Requirement | Current | Status |",
        "|---|---:|---|",
        f"| Total quests | {quests['quests']} / 5,000–6,000 | {'PASS' if quest_volume else 'IN PROGRESS'} |",
        f"| RU/EN descriptions | {quests['bilingual']} / {quests['quests']} | {'PASS' if full_bilingual else 'IN PROGRESS'} |",
        f"| Single item-only ratio | {quests['item_only_ratio']:.1%} / ≤30% | {'PASS' if quest_structure else 'IN PROGRESS'} |",
        "",
        "## Selected gameplay guide specification",
        "",
        "| Metric | Current |",
        "|---|---:|",
        f"| Manifest inventory projects | {guides['manifest']} |",
        f"| Tracked gameplay/progression projects | {guides['tracked']} |",
        f"| Projects not requiring individual guides | {guides['not_selected']} |",
        f"| Tracked guides awaiting review | {guides['missing_review']} |",
        f"| Reviewed tracked guides | {guides['reviewed']} |",
        f"| Complete tracked guides | {guides['complete']} |",
        f"| Coverage status | {'PASS' if guide_complete else 'IN PROGRESS'} |",
        "",
        "## Minimum runtime evidence",
        "",
        "| Gate | Status |",
        "|---|---|",
    ])
    for name in sorted(runtime):
        lines.append(f"| `{name}` | {'VERIFIED' if runtime[name] else 'UNVERIFIED'} |")

    lines.extend([
        "",
        "## Release rule",
        "",
        "The label `v1` is prohibited until all static reports pass, the quest book contains 5,000–6,000 fully bilingual quests, item-only quests are at most 30%, every selected meaningful gameplay/progression mod has a reviewed guide, and the minimum runtime evidence is verified. Unselected libraries, APIs, renderers, compatibility layers and optimization projects do not require individual guide chapters.",
        "",
    ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"v1_product_classification: {classification}")
    print(f"static_reports: {sum(status.values())}/{len(status)}")
    print(f"quests: {quests['quests']}")
    print(f"bilingual: {quests['bilingual']}")
    print(f"item_only_ratio: {quests['item_only_ratio']:.4f}")
    print(f"tracked_guide_coverage: {guides['tracked'] - guides['missing_review']}/{guides['tracked']}")
    print(f"manifest_projects_not_selected: {guides['not_selected']}")
    print(f"minimum_runtime: {sum(runtime.values())}/{len(runtime)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
