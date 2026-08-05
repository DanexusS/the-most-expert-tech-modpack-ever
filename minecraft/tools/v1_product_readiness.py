from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REPORT_PATH = DOCS / "V1_PRODUCT_READINESS.md"
EVIDENCE_PATH = ROOT / "config" / "v1_runtime_evidence.json"

BASE_REPORTS = {
    "Theoretical balance": DOCS / "THEORETICAL_BALANCE_REPORT.md",
    "Progression contract": DOCS / "PROGRESSION_CONTRACT_REPORT.md",
    "Recipe dependency graph": DOCS / "RECIPE_DEPENDENCY_REPORT.md",
    "Bypass closure": DOCS / "BYPASS_AUDIT_REPORT.md",
    "Selected gameplay guide coverage": DOCS / "MOD_GUIDE_COVERAGE_REPORT.md",
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

FINAL_PERFORMANCE_GATES = {
    "startup_and_world_load_regression_below_10_percent",
    "thirty_minute_soak_tps_gate",
    "heap_stability_gate",
    "log_rate_gate",
}


def report_label(path: Path) -> str:
    return path.stem.replace("_QUALITY_REPORT", "").replace("_", " ").title()


def report_registry() -> dict[str, Path]:
    reports = dict(BASE_REPORTS)
    for path in sorted(DOCS.glob("*_QUALITY_REPORT.md")):
        reports[report_label(path)] = path
    return reports


def report_pass(path: Path) -> bool:
    return path.is_file() and "**PASS**" in path.read_text(encoding="utf-8")


def integer(text: str, pattern: str) -> int:
    match = re.search(pattern, text)
    return int(match.group(1).replace(",", "")) if match else 0


def quest_metrics() -> dict[str, int | float]:
    text = (DOCS / "QUEST_QUALITY_REPORT.md").read_text(encoding="utf-8")
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
    text = (DOCS / "MOD_GUIDE_COVERAGE_REPORT.md").read_text(encoding="utf-8")
    return {
        "manifest": integer(text, r"Manifest projects:\s*\*\*([0-9,]+)\*\*"),
        "tracked": integer(text, r"Tracked gameplay/progression projects:\s*\*\*([0-9,]+)\*\*"),
        "not_selected": integer(text, r"Manifest projects not selected for individual guides:\s*\*\*([0-9,]+)\*\*"),
        "missing_review": integer(text, r"Tracked guides not reviewed:\s*\*\*([0-9,]+)\*\*"),
        "reviewed": integer(text, r"Reviewed tracked guides:\s*\*\*([0-9,]+)\*\*"),
        "complete": integer(text, r"Complete tracked guides:\s*\*\*([0-9,]+)\*\*"),
        "blockers": integer(text, r"Coverage blockers:\s*\*\*([0-9,]+)\*\*"),
    }


def runtime_gate_verified(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return isinstance(value, dict) and value.get("verified") is True


def main() -> int:
    reports = report_registry()
    status = {name: report_pass(path) for name, path in reports.items()}
    quests = quest_metrics()
    guides = guide_metrics()
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    gate_records = evidence.get("gates", {})
    minimum_runtime = {
        name: runtime_gate_verified(gate_records.get(name, False))
        for name in MINIMUM_RUNTIME_GATES
    }
    final_performance = {
        name: runtime_gate_verified(gate_records.get(name, False))
        for name in FINAL_PERFORMANCE_GATES
    }

    quest_volume = 5000 <= quests["quests"] <= 6000
    full_bilingual = quests["quests"] > 0 and quests["bilingual"] == quests["quests"]
    quest_structure = quests["item_only_ratio"] <= 0.30
    guide_complete = (
        guides["tracked"] > 0
        and guides["missing_review"] == 0
        and guides["blockers"] == 0
    )
    static_complete = (
        all(status.values())
        and quest_volume
        and full_bilingual
        and quest_structure
        and guide_complete
    )
    minimum_runtime_complete = all(minimum_runtime.values())
    final_performance_complete = all(final_performance.values())

    if static_complete and minimum_runtime_complete and final_performance_complete:
        classification = "V1"
    elif static_complete and minimum_runtime_complete:
        classification = "V1 CANDIDATE — PERFORMANCE EVIDENCE REQUIRED"
    elif static_complete:
        classification = "V1 CANDIDATE — MINIMUM RUNTIME EVIDENCE REQUIRED"
    elif all(status.values()):
        classification = "STATIC FOUNDATION PASS — PRODUCT INCOMPLETE"
    else:
        classification = "DEVELOPMENT — STATIC GATES INCOMPLETE"

    remaining_volume = max(0, 5000 - quests["quests"])
    remaining_bilingual = max(0, quests["quests"] - quests["bilingual"])
    lines = [
        "# v1 Product Readiness",
        "",
        f"## Classification: **{classification}**",
        "",
        "Every `*_QUALITY_REPORT.md` file is automatically release-gated. Adding a redesigned chapter or performance safeguard therefore adds a mandatory static check without editing this classifier.",
        "",
        "## Static reports",
        "",
        "| Gate | Status |",
        "|---|---|",
    ]
    for name, passed in sorted(status.items()):
        lines.append(f"| {name} | {'PASS' if passed else 'IN PROGRESS / FAIL'} |")

    lines.extend(
        [
            "",
            "## Quest product specification",
            "",
            "| Requirement | Current | Status |",
            "|---|---:|---|",
            f"| Total quests | {quests['quests']} / 5,000–6,000 | {'PASS' if quest_volume else 'IN PROGRESS'} |",
            f"| RU/EN descriptions | {quests['bilingual']} / {quests['quests']} | {'PASS' if full_bilingual else 'IN PROGRESS'} |",
            f"| Single item-only ratio | {quests['item_only_ratio']:.1%} / ≤30% | {'PASS' if quest_structure else 'IN PROGRESS'} |",
            f"| Remaining to 5,000 quests | {remaining_volume} | {'PASS' if remaining_volume == 0 else 'IN PROGRESS'} |",
            f"| Remaining without full RU/EN | {remaining_bilingual} | {'PASS' if remaining_bilingual == 0 else 'IN PROGRESS'} |",
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
            "## Minimum functional runtime evidence",
            "",
            "| Gate | Status |",
            "|---|---|",
        ]
    )
    for name in sorted(minimum_runtime):
        lines.append(f"| `{name}` | {'VERIFIED' if minimum_runtime[name] else 'UNVERIFIED'} |")

    lines.extend(
        [
            "",
            "## Final release performance evidence",
            "",
            "| Gate | Status |",
            "|---|---|",
        ]
    )
    for name in sorted(final_performance):
        lines.append(f"| `{name}` | {'VERIFIED' if final_performance[name] else 'UNVERIFIED'} |")

    lines.extend(
        [
            "",
            "## Release rule",
            "",
            "The label `v1` is prohibited until all static reports pass, the quest product specification is complete, all seven functional runtime gates are verified, and the four final performance gates pass measured startup/world-load, representative soak, heap-stability and repeated-log thresholds. Unselected libraries, APIs, renderers, compatibility layers and optimization projects do not require individual guide chapters.",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"v1_product_classification: {classification}")
    print(f"static_reports: {sum(status.values())}/{len(status)}")
    print(
        f"quality_reports_discovered: "
        f"{sum(path.name.endswith('_QUALITY_REPORT.md') for path in reports.values())}"
    )
    print(f"quests: {quests['quests']}")
    print(f"bilingual: {quests['bilingual']}")
    print(f"remaining_to_5000: {remaining_volume}")
    print(f"remaining_without_full_bilingual: {remaining_bilingual}")
    print(f"item_only_ratio: {quests['item_only_ratio']:.4f}")
    print(
        f"tracked_guide_coverage: "
        f"{guides['tracked'] - guides['missing_review']}/{guides['tracked']}"
    )
    print(f"manifest_projects_not_selected: {guides['not_selected']}")
    print(
        f"minimum_runtime: {sum(minimum_runtime.values())}/{len(minimum_runtime)}"
    )
    print(
        f"final_performance: {sum(final_performance.values())}/{len(final_performance)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
