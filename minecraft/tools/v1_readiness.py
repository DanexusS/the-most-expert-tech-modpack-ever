from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "config" / "v1_runtime_evidence.json"
REPORT_PATH = ROOT / "docs" / "V1_READINESS.md"

STATIC_REPORTS = {
    "Theoretical balance": ROOT / "docs" / "THEORETICAL_BALANCE_REPORT.md",
    "Quest quality": ROOT / "docs" / "QUEST_QUALITY_REPORT.md",
    "Create core route": ROOT / "docs" / "CREATE_CORE_QUALITY_REPORT.md",
    "Immersive Engineering core route": ROOT / "docs" / "IE_CORE_QUALITY_REPORT.md",
    "Modern Industrialization core route": ROOT / "docs" / "MI_CORE_QUALITY_REPORT.md",
}


def report_passed(path: Path) -> bool:
    return path.exists() and "**PASS**" in path.read_text(encoding="utf-8")


def main() -> int:
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    static_status = {name: report_passed(path) for name, path in STATIC_REPORTS.items()}
    runtime_gates = {name: bool(value) for name, value in evidence["gates"].items()}

    static_complete = all(static_status.values())
    second_restart = runtime_gates.get("second_clean_restart_and_world_reopen", False)
    runtime_except_second = all(
        value for name, value in runtime_gates.items()
        if name != "second_clean_restart_and_world_reopen"
    )

    if static_complete and runtime_except_second and second_restart:
        classification = "V1"
        decision = "All declared static and runtime gates have recorded evidence."
    elif static_complete and runtime_except_second:
        classification = "V1 CANDIDATE"
        decision = "All primary evidence exists; a second clean restart and world reopen remain mandatory."
    elif static_complete:
        classification = "STATIC CANDIDATE — NOT V1"
        decision = "Static and theoretical gates pass, but runtime evidence is incomplete."
    else:
        classification = "DEVELOPMENT — NOT V1"
        decision = "One or more mandatory static reports do not pass or do not exist."

    lines = [
        "# v1 Readiness",
        "",
        f"## Classification: **{classification}**",
        "",
        decision,
        "",
        "## Static and theoretical evidence",
        "",
        "| Gate | Status |",
        "|---|---|",
    ]
    for name, passed in static_status.items():
        lines.append(f"| {name} | {'PASS' if passed else 'MISSING / FAIL'} |")

    lines.extend([
        "",
        "## Runtime evidence",
        "",
        "| Gate | Status |",
        "|---|---|",
    ])
    for name, passed in runtime_gates.items():
        lines.append(f"| `{name}` | {'VERIFIED' if passed else 'UNVERIFIED'} |")

    measurements = evidence.get("measurements", {})
    lines.extend([
        "",
        "## Recorded measurements",
        "",
        "| Measurement | Value |",
        "|---|---:|",
    ])
    for name, value in measurements.items():
        rendered = "not measured" if value is None else str(value)
        lines.append(f"| `{name}` | {rendered} |")

    lines.extend([
        "",
        "## Rule",
        "",
        "The label `v1` is prohibited while any runtime gate is unverified. Theoretical calculations may tune test targets but cannot set runtime evidence to verified.",
        "",
    ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"v1_classification: {classification}")
    print(f"static_reports_passed: {sum(static_status.values())}/{len(static_status)}")
    print(f"runtime_gates_verified: {sum(runtime_gates.values())}/{len(runtime_gates)}")
    # The readiness classifier is informational. Blocking static gates already
    # fail in their own preceding CI steps.
    return 0


if __name__ == "__main__":
    sys.exit(main())
