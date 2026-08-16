from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "config" / "v1_runtime_evidence.json"
REPORT_PATH = ROOT / "docs" / "RUNTIME_EVIDENCE_STRUCTURE_QUALITY_REPORT.md"
MANDATORY_GATES = (
    "clean_client_start",
    "new_world_create_save_reopen",
    "kubejs_milestone_items_exist",
    "strategic_recipes_verified",
    "representative_quest_tasks_complete",
    "language_switch_verified",
    "second_clean_restart_and_world_reopen",
)
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
TIMESTAMP_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)


def valid_timestamp(value: object) -> bool:
    return isinstance(value, str) and bool(TIMESTAMP_RE.fullmatch(value))


def positive_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def gate_verified(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return isinstance(value, dict) and value.get("verified") is True


def main() -> int:
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    failures: list[str] = []
    rows: list[dict] = []

    if evidence.get("schema_version") != 2:
        failures.append("schema_version must be 2")

    gates = evidence.get("gates")
    if not isinstance(gates, dict):
        failures.append("gates must be an object")
        gates = {}

    for required_gate in MANDATORY_GATES:
        if required_gate not in gates:
            failures.append(f"missing mandatory gate: {required_gate}")

    any_verified = False
    for name, record in sorted(gates.items()):
        gate_failures: list[str] = []
        if not isinstance(record, dict):
            gate_failures.append("gate record must be an object")
            record = {}

        verified = record.get("verified")
        if not isinstance(verified, bool):
            gate_failures.append("verified must be boolean")
            verified = False
        any_verified = any_verified or bool(verified)

        checked_at = record.get("checked_at")
        if checked_at is not None and not valid_timestamp(checked_at):
            gate_failures.append("checked_at must be ISO-8601 with timezone or null")

        coverage = record.get("coverage")
        current = -1
        required = -1
        if not isinstance(coverage, dict):
            gate_failures.append("coverage must be an object")
        else:
            current = coverage.get("current")
            required = coverage.get("required")
            if not isinstance(current, int) or isinstance(current, bool) or current < 0:
                gate_failures.append("coverage.current must be a non-negative integer")
            if not isinstance(required, int) or isinstance(required, bool) or required <= 0:
                gate_failures.append("coverage.required must be a positive integer")

        gate_evidence = record.get("evidence")
        if not isinstance(gate_evidence, list) or any(
            not isinstance(item, str) or len(item.strip()) < 8 for item in gate_evidence
        ):
            gate_failures.append("evidence must be a list of non-trivial string references")
            gate_evidence = []

        notes = record.get("notes")
        if not isinstance(notes, list) or any(not isinstance(item, str) for item in notes):
            gate_failures.append("notes must be a list of strings")

        if verified:
            if not valid_timestamp(checked_at):
                gate_failures.append("verified gate requires checked_at")
            if not gate_evidence:
                gate_failures.append("verified gate requires at least one evidence reference")
            if isinstance(current, int) and isinstance(required, int) and current < required:
                gate_failures.append(
                    f"verified coverage is incomplete ({current}/{required})"
                )

        failures.extend(f"{name}: {failure}" for failure in gate_failures)
        rows.append(
            {
                "name": name,
                "verified": bool(verified),
                "current": current,
                "required": required,
                "evidence": len(gate_evidence),
                "status": "PASS" if not gate_failures else "FAIL",
            }
        )

    pack_commit = evidence.get("pack_commit")
    measured_at = evidence.get("measured_at")
    environment = evidence.get("environment")
    if any_verified:
        if not isinstance(pack_commit, str) or not COMMIT_RE.fullmatch(pack_commit):
            failures.append("verified evidence requires a 40-character lowercase pack_commit")
        if not valid_timestamp(measured_at):
            failures.append("verified evidence requires measured_at with timezone")
        if not isinstance(environment, dict):
            failures.append("verified evidence requires an environment object")
        else:
            if not isinstance(environment.get("java"), str) or not environment["java"].strip():
                failures.append("verified evidence requires environment.java")
            if not isinstance(environment.get("memory_mib"), int) or environment["memory_mib"] <= 0:
                failures.append("verified evidence requires positive environment.memory_mib")
            for field in ("hardware_note", "test_world", "instance_note"):
                if not isinstance(environment.get(field), str) or not environment[field].strip():
                    failures.append(f"verified evidence requires environment.{field}")

    if gate_verified(gates.get("second_clean_restart_and_world_reopen")):
        for prerequisite in (
            "clean_client_start",
            "new_world_create_save_reopen",
        ):
            if not gate_verified(gates.get(prerequisite)):
                failures.append(
                    "second_clean_restart_and_world_reopen requires " + prerequisite
                )
    if gate_verified(gates.get("strategic_recipes_verified")) and not gate_verified(
        gates.get("kubejs_milestone_items_exist")
    ):
        failures.append(
            "strategic_recipes_verified requires kubejs_milestone_items_exist"
        )
    if gate_verified(gates.get("language_switch_verified")) and not gate_verified(
        gates.get("clean_client_start")
    ):
        failures.append("language_switch_verified requires clean_client_start")

    measurements = evidence.get("measurements")
    if not isinstance(measurements, dict):
        failures.append("measurements must be an object")
        measurements = {}

    if gate_verified(gates.get("startup_and_world_load_regression_below_10_percent")):
        required_measurements = (
            "baseline_startup_seconds_median",
            "candidate_startup_seconds_median",
            "baseline_world_load_seconds_median",
            "candidate_world_load_seconds_median",
        )
        for field in required_measurements:
            if not positive_number(measurements.get(field)):
                failures.append(f"startup regression gate requires {field}")
        if all(positive_number(measurements.get(field)) for field in required_measurements):
            if measurements["candidate_startup_seconds_median"] > measurements["baseline_startup_seconds_median"] * 1.10:
                failures.append("candidate startup regression exceeds 10 percent")
            if measurements["candidate_world_load_seconds_median"] > measurements["baseline_world_load_seconds_median"] * 1.10:
                failures.append("candidate world-load regression exceeds 10 percent")

    if gate_verified(gates.get("thirty_minute_soak_tps_gate")):
        if not positive_number(measurements.get("soak_tps_p05")):
            failures.append("soak gate requires soak_tps_p05")
        if not positive_number(measurements.get("soak_mspt_p95")):
            failures.append("soak gate requires soak_mspt_p95")

    if gate_verified(gates.get("heap_stability_gate")):
        first = measurements.get("heap_after_first_cycle_mib")
        second = measurements.get("heap_after_second_cycle_mib")
        if not positive_number(first) or not positive_number(second):
            failures.append("heap stability gate requires two positive heap measurements")
        elif second > first * 1.10:
            failures.append("second post-GC heap measurement exceeds first by more than 10 percent")

    if gate_verified(gates.get("log_rate_gate")):
        rate = measurements.get("maximum_repeated_log_lines_per_minute")
        if not isinstance(rate, (int, float)) or isinstance(rate, bool) or rate < 0:
            failures.append("log rate gate requires a non-negative repeated-log measurement")

    lines = [
        "# Runtime Evidence Structure Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "This gate validates the evidence schema and rejects unsupported runtime claims. A structurally valid file may still contain only UNVERIFIED gates; that is expected until an actual client or server run is recorded.",
        "",
        "| Gate | Verified | Coverage | Evidence refs | Structure |",
        "|---|---|---:|---:|---|",
    ]
    for row in rows:
        coverage_text = (
            f"{row['current']}/{row['required']}"
            if row["current"] >= 0 and row["required"] >= 0
            else "invalid"
        )
        lines.append(
            f"| `{row['name']}` | {'yes' if row['verified'] else 'no'} | "
            f"{coverage_text} | {row['evidence']} | {row['status']} |"
        )

    lines.extend(
        [
            "",
            "## Aggregate",
            "",
            f"- Gates recorded: **{len(rows)}**",
            f"- Mandatory gates recorded: **{sum(name in gates for name in MANDATORY_GATES)} / {len(MANDATORY_GATES)}**",
            f"- Mandatory gates verified: **{sum(gate_verified(gates.get(name)) for name in MANDATORY_GATES)} / {len(MANDATORY_GATES)}**",
            f"- Structural or claim failures: **{len(failures)}**",
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"runtime_evidence_structure: {'PASS' if not failures else 'FAIL'}")
    print(f"runtime_gates_recorded: {len(rows)}")
    print(
        "mandatory_runtime_verified: "
        f"{sum(gate_verified(gates.get(name)) for name in MANDATORY_GATES)}/{len(MANDATORY_GATES)}"
    )
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
