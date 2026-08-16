from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "config" / "v1_runtime_evidence.json"
POLICY_PATH = ROOT / "config" / "expert_performance_policy.json"
REPORT_PATH = ROOT / "docs" / "RUNTIME_PERFORMANCE_QUALITY_REPORT.md"

RELEASE_GATES = (
    "startup_and_world_load_regression_below_10_percent",
    "thirty_minute_soak_tps_gate",
    "heap_stability_gate",
    "log_rate_gate",
)


def verified(gates: dict, name: str) -> bool:
    record = gates.get(name)
    return isinstance(record, dict) and record.get("verified") is True


def number(value: object) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return None


def main() -> int:
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    targets = policy["release_runtime_targets"]
    gates = evidence.get("gates", {})
    measurements = evidence.get("measurements", {})
    failures: list[str] = []
    rows: list[tuple[str, str, str]] = []

    for name in RELEASE_GATES:
        if name not in gates:
            failures.append(f"missing release performance gate: {name}")

    startup_verified = verified(gates, RELEASE_GATES[0])
    baseline_startup = number(measurements.get("baseline_startup_seconds_median"))
    candidate_startup = number(measurements.get("candidate_startup_seconds_median"))
    baseline_world = number(measurements.get("baseline_world_load_seconds_median"))
    candidate_world = number(measurements.get("candidate_world_load_seconds_median"))
    startup_limit = float(targets["maximum_startup_regression_percent"])
    world_limit = float(targets["maximum_world_load_regression_percent"])
    startup_status = "UNVERIFIED"
    if startup_verified:
        required = (baseline_startup, candidate_startup, baseline_world, candidate_world)
        if any(value is None or value <= 0 for value in required):
            failures.append("startup/world-load gate requires four positive median measurements")
            startup_status = "FAIL"
        else:
            startup_regression = (candidate_startup / baseline_startup - 1.0) * 100.0
            world_regression = (candidate_world / baseline_world - 1.0) * 100.0
            if startup_regression > startup_limit:
                failures.append(
                    f"startup regression {startup_regression:.2f}% exceeds {startup_limit:.2f}%"
                )
            if world_regression > world_limit:
                failures.append(
                    f"world-load regression {world_regression:.2f}% exceeds {world_limit:.2f}%"
                )
            startup_status = "PASS" if startup_regression <= startup_limit and world_regression <= world_limit else "FAIL"
    rows.append(("Startup and world-load regression", f"≤{startup_limit:.1f}% / ≤{world_limit:.1f}%", startup_status))

    soak_verified = verified(gates, RELEASE_GATES[1])
    soak_tps = number(measurements.get("soak_tps_p05"))
    soak_mspt = number(measurements.get("soak_mspt_p95"))
    minimum_tps = float(targets["minimum_soak_tps_p05"])
    maximum_mspt = float(targets["maximum_soak_mspt_p95"])
    soak_status = "UNVERIFIED"
    if soak_verified:
        if soak_tps is None or soak_mspt is None:
            failures.append("soak gate requires soak_tps_p05 and soak_mspt_p95")
            soak_status = "FAIL"
        else:
            if soak_tps < minimum_tps:
                failures.append(f"soak TPS p05 {soak_tps:.2f} is below {minimum_tps:.2f}")
            if soak_mspt > maximum_mspt:
                failures.append(f"soak MSPT p95 {soak_mspt:.2f} exceeds {maximum_mspt:.2f}")
            soak_status = "PASS" if soak_tps >= minimum_tps and soak_mspt <= maximum_mspt else "FAIL"
    rows.append(("30-minute representative soak", f"TPS p05 ≥{minimum_tps:.1f}; MSPT p95 ≤{maximum_mspt:.1f}", soak_status))

    heap_verified = verified(gates, RELEASE_GATES[2])
    first_heap = number(measurements.get("heap_after_first_cycle_mib"))
    second_heap = number(measurements.get("heap_after_second_cycle_mib"))
    heap_limit = float(targets["maximum_post_gc_heap_growth_percent"])
    heap_status = "UNVERIFIED"
    if heap_verified:
        if first_heap is None or second_heap is None or first_heap <= 0 or second_heap <= 0:
            failures.append("heap gate requires two positive post-GC heap measurements")
            heap_status = "FAIL"
        else:
            heap_growth = (second_heap / first_heap - 1.0) * 100.0
            if heap_growth > heap_limit:
                failures.append(
                    f"post-GC heap growth {heap_growth:.2f}% exceeds {heap_limit:.2f}%"
                )
            heap_status = "PASS" if heap_growth <= heap_limit else "FAIL"
    rows.append(("Post-GC heap stability", f"growth ≤{heap_limit:.1f}%", heap_status))

    log_verified = verified(gates, RELEASE_GATES[3])
    log_rate = number(measurements.get("maximum_repeated_log_lines_per_minute"))
    log_limit = float(targets["maximum_repeated_log_lines_per_minute"])
    log_status = "UNVERIFIED"
    if log_verified:
        if log_rate is None or log_rate < 0:
            failures.append("log-rate gate requires a non-negative repeated-line measurement")
            log_status = "FAIL"
        else:
            if log_rate > log_limit:
                failures.append(
                    f"repeated log rate {log_rate:.2f}/min exceeds {log_limit:.2f}/min"
                )
            log_status = "PASS" if log_rate <= log_limit else "FAIL"
    rows.append(("Repeated-log rate", f"≤{log_limit:.0f} lines/min", log_status))

    lines = [
        "# Runtime Performance Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "This gate validates final-release performance evidence against the pack policy. UNVERIFIED rows are structurally valid but continue to block the final v1 label through the readiness classifier.",
        "",
        "| Gate | Release target | Evidence status |",
        "|---|---|---|",
    ]
    for label, target, status in rows:
        lines.append(f"| {label} | {target} | {status} |")
    lines.extend(
        [
            "",
            "## Aggregate",
            "",
            f"- Release performance gates recorded: **{sum(name in gates for name in RELEASE_GATES)} / {len(RELEASE_GATES)}**",
            f"- Release performance gates verified: **{sum(verified(gates, name) for name in RELEASE_GATES)} / {len(RELEASE_GATES)}**",
            f"- Invalid claims or threshold failures: **{len(failures)}**",
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"runtime_performance_structure: {'PASS' if not failures else 'FAIL'}")
    print(
        "release_performance_verified: "
        f"{sum(verified(gates, name) for name in RELEASE_GATES)}/{len(RELEASE_GATES)}"
    )
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
