from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "config" / "v1_runtime_evidence.json"
REPORT_PATH = ROOT / "docs" / "V1_READINESS.md"

FOUNDATION_REPORTS = {
    "Theoretical balance": ROOT / "docs" / "THEORETICAL_BALANCE_REPORT.md",
    "Core quest quality": ROOT / "docs" / "QUEST_QUALITY_REPORT.md",
    "Create core route": ROOT / "docs" / "CREATE_CORE_QUALITY_REPORT.md",
    "Immersive Engineering core route": ROOT / "docs" / "IE_CORE_QUALITY_REPORT.md",
    "Modern Industrialization core route": ROOT / "docs" / "MI_CORE_QUALITY_REPORT.md",
}

PRODUCT_REPORTS = {
    "Progression contract": ROOT / "docs" / "PROGRESSION_CONTRACT_REPORT.md",
    "Bypass closure": ROOT / "docs" / "BYPASS_AUDIT_REPORT.md",
    "All-mod guide coverage": ROOT / "docs" / "MOD_GUIDE_COVERAGE_REPORT.md",
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


def report_passed(path: Path) -> bool:
    return path.exists() and "**PASS**" in path.read_text(encoding="utf-8")


def quest_product_metrics() -> dict[str, int | float]:
    path = ROOT / "docs" / "QUEST_QUALITY_REPORT.md"
    if not path.exists():
        return {"quests": 0, "bilingual": 0, "item_only": 0, "item_only_ratio": 1.0}
    text = path.read_text(encoding="utf-8")

    def value(pattern: str) -> int:
        match = re.search(pattern, text)
        return int(match.group(1)) if match else 0

    quests = value(r"Quests parsed:\s*\*\*([0-9]+)\*\*")
    bilingual = value(r"Bilingual quest descriptions:\s*\*\*([0-9]+)")
    item_only = value(r"Single item-only quests:\s*\*\*([0-9]+)\*\*")
    return {
        "quests": quests,
        "bilingual": bilingual,
        "item_only": item_only,
        "item_only_ratio": item_only / max(1, quests),
    }


def main() -> int:
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    foundation_status = {name: report_passed(path) for name, path in FOUNDATION_REPORTS.items()}
    product_status = {name: report_passed(path) for name, path in PRODUCT_REPORTS.items()}
    runtime_gates = {name: bool(value) for name, value in evidence["gates"].items()}
    required_runtime = {name: runtime_gates.get(name, False) for name in MINIMUM_RUNTIME_GATES}
    quest_metrics = quest_product_metrics()

    foundation_complete = all(foundation_status.values())
    product_reports_complete = all(product_status.values())
    quest_volume_complete = 5000 <= quest_metrics["quests"] <= 6000
    quest_structure_complete = quest_metrics["item_only_ratio"] <= 0.30
    product_complete = product_reports_complete and quest_volume_complete and quest_structure_complete
    runtime_complete = all(required_runtime.values())

    if foundation_complete and product_complete and runtime_complete:
        classification = "V1"
        decision = "Product, structural, anti-bypass and minimum runtime requirements pass."
    elif foundation_complete and product_complete:
        classification = "V1 CANDIDATE"
        decision = "The product specification passes; minimum runtime evidence remains incomplete."
    elif foundation_complete:
        classification = "STATIC CANDIDATE — PRODUCT INCOMPLETE"
        decision = "Core static checks pass, but the 5–6k quest target, guide coverage, progression contract or bypass closure is incomplete."
    else:
        classification = "DEVELOPMENT — NOT V1"
        decision = "One or more foundation reports do not pass or do not exist."

    quest_volume_status = "PASS" if quest_volume_complete else f"IN PROGRESS ({quest_metrics['quests']})"
    item_only_status = (
        "PASS" if quest_structure_complete
        else f"IN PROGRESS ({quest_metrics['item_only_ratio']:.1%})"
    )

    lines = [
        "# v1 Readiness",
        "",
        f"## Classification: **{classification}**",
        "",
        decision,
        "",
        "## Foundation evidence",
        "",
        "| Gate | Status |",
        "|---|---|",
    ]
    for name, passed in foundation_status.items():
        lines.append(f"| {name} | {'PASS' if passed else 'MISSING / FAIL'} |")

    lines.extend([
        "",
        "## Product evidence",
        "",
        "| Gate | Status |",
        "|---|---|",
    ])
    for name, passed in product_status.items():
        lines.append(f"| {name} | {'PASS' if passed else 'IN PROGRESS / FAIL'} |")
    lines.extend([
        f"| Quest volume 5,000–6,000 | {quest_volume_status} |",
        f"| Item-only ratio ≤30% | {item_only_status} |",
        "",
        "## Minimum runtime evidence",
        "",
        "| Gate | Status |",
        "|---|---|",
    ])
    for name in sorted(MINIMUM_RUNTIME_GATES):
        lines.append(f"| `{name}` | {'VERIFIED' if required_runtime[name] else 'UNVERIFIED'} |")

    optional_runtime = {
        name: value for name, value in runtime_gates.items()
        if name not in MINIMUM_RUNTIME_GATES
    }
    lines.extend([
        "",
        "## Optional measurements",
        "",
        "These improve tuning but do not block v1 under the current product specification.",
        "",
        "| Gate | Status |",
        "|---|---|",
    ])
    for name, passed in optional_runtime.items():
        lines.append(f"| `{name}` | {'VERIFIED' if passed else 'UNVERIFIED'} |")

    lines.extend([
        "",
        "## Rule",
        "",
        "The label `v1` is prohibited until the product specification, progression contract, bypass audit, all-mod guide coverage and minimum runtime gates pass together.",
        "",
    ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"v1_classification: {classification}")
    print(f"foundation_reports_passed: {sum(foundation_status.values())}/{len(foundation_status)}")
    print(f"product_reports_passed: {sum(product_status.values())}/{len(product_status)}")
    print(f"quest_count: {quest_metrics['quests']}")
    print(f"item_only_ratio: {quest_metrics['item_only_ratio']:.4f}")
    print(f"minimum_runtime_verified: {sum(required_runtime.values())}/{len(required_runtime)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
