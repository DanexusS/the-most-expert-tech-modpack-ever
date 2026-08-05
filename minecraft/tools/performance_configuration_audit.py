from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import generate_early_stage_workflow_expansions as workflow
from mid_stage_workflow_profiles import MID_STAGE_WORKFLOW_PROFILES

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "expert_performance_policy.json"
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
QUEST_DATA_PATH = ROOT / "config" / "ftbquests" / "quests" / "data.snbt"
COROUTIL_PATH = ROOT / "config" / "CoroUtil" / "General.toml"
COMBAT_PATH = ROOT / "kubejs" / "server_scripts" / "combat_scaling.js"
GITIGNORE_PATH = ROOT / ".gitignore"
REPORT_PATH = ROOT / "docs" / "PERFORMANCE_CONFIGURATION_QUALITY_REPORT.md"


def snbt_bool(text: str, key: str) -> bool | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(true|false)\s*$", text)
    return None if match is None else match.group(1) == "true"


def snbt_number(text: str, key: str) -> float | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*([0-9]+(?:\.[0-9]+)?)(?:[dDfFlL])?\s*$", text)
    return None if match is None else float(match.group(1))


def toml_bool(text: str, key: str) -> bool | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*(true|false)\s*$", text)
    return None if match is None else match.group(1) == "true"


def main() -> int:
    overlap = set(workflow.WORKFLOW_STAGES) & set(MID_STAGE_WORKFLOW_PROFILES)
    if overlap:
        raise RuntimeError(
            "Duplicate workflow stage profiles: " + ", ".join(sorted(overlap))
        )
    workflow.WORKFLOW_STAGES.update(MID_STAGE_WORKFLOW_PROFILES)

    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    stage_indexes = {
        stage["id"]: int(stage["index"])
        for stage in contract["stages"]
    }
    quest_data = QUEST_DATA_PATH.read_text(encoding="utf-8")
    coroutil = COROUTIL_PATH.read_text(encoding="utf-8")
    combat = COMBAT_PATH.read_text(encoding="utf-8")
    gitignore = GITIGNORE_PATH.read_text(encoding="utf-8")
    failures: list[str] = []
    rows: list[tuple[str, str, str]] = []

    ftb = policy["ftb_quests"]
    detection = snbt_number(quest_data, "detection_delay")
    detection_ok = detection is not None and detection >= float(ftb["minimum_detection_delay_ticks"])
    rows.append(("FTB Quests detection delay", str(detection), "PASS" if detection_ok else "FAIL"))
    if not detection_ok:
        failures.append(
            f"FTB Quests detection_delay must be at least {ftb['minimum_detection_delay_ticks']} ticks; found {detection}"
        )

    grid_scale = snbt_number(quest_data, "grid_scale")
    grid_ok = grid_scale is not None and grid_scale <= float(ftb["maximum_grid_scale"])
    rows.append(("FTB Quests grid scale", str(grid_scale), "PASS" if grid_ok else "FAIL"))
    if not grid_ok:
        failures.append(
            f"FTB Quests grid_scale must be at most {ftb['maximum_grid_scale']}; found {grid_scale}"
        )

    for key, expected in (
        ("verify_on_load", bool(ftb["verify_on_load"])),
        ("drop_loot_crates", bool(ftb["drop_loot_crates"])),
    ):
        actual = snbt_bool(quest_data, key)
        ok = actual is expected
        rows.append((f"FTB Quests {key}", str(actual), "PASS" if ok else "FAIL"))
        if not ok:
            failures.append(f"FTB Quests {key} expected {expected}, found {actual}")

    logging = policy["logging"]
    logging_checks = (
        ("useLoggingLog", bool(logging["coroutil_routine_logging"])),
        ("useLoggingDebug", bool(logging["coroutil_debug_logging"])),
        ("useLoggingError", bool(logging["coroutil_error_logging"])),
    )
    for key, expected in logging_checks:
        actual = toml_bool(coroutil, key)
        ok = actual is expected
        rows.append((f"CoroUtil {key}", str(actual), "PASS" if ok else "FAIL"))
        if not ok:
            failures.append(f"CoroUtil {key} expected {expected}, found {actual}")

    combat_requirements = {
        "Profile cache": "var PROFILE_CACHE = Object.create(null)",
        "Stable modifier IDs": "var MODIFIER_IDS = Object.freeze",
        "Registry guard": "BuiltInRegistries.ENTITY_TYPE.containsKey",
    }
    for label, token in combat_requirements.items():
        ok = token in combat
        rows.append((f"Combat scaling — {label}", "present" if ok else "missing", "PASS" if ok else "FAIL"))
        if not ok:
            failures.append(f"Combat scaling safeguard missing: {label}")

    hygiene = policy["repository_hygiene"]
    for entry in hygiene["required_gitignore_entries"]:
        ok = entry in gitignore
        rows.append((f".gitignore {entry}", "present" if ok else "missing", "PASS" if ok else "FAIL"))
        if not ok:
            failures.append(f"Required runtime ignore entry missing: {entry}")

    for relative in hygiene["forbidden_tracked_paths"]:
        path = ROOT / relative.rstrip("/")
        exists = path.exists()
        rows.append((f"Runtime path {relative}", "tracked/present" if exists else "absent", "FAIL" if exists else "PASS"))
        if exists:
            failures.append(f"Runtime-generated path remains in source checkout: {relative}")

    optimization_total = 0
    optimization_missing: list[str] = []
    for stage_id in sorted(
        workflow.expanded_stage_ids(),
        key=lambda value: stage_indexes.get(value, 10_000),
    ):
        index = stage_indexes.get(stage_id)
        if index is None:
            optimization_missing.append(f"{stage_id}:missing-contract-stage")
            continue
        chapter = ROOT / "config" / "ftbquests" / "quests" / "chapters" / f"main_stage_{index:02d}_{stage_id}.snbt"
        text = chapter.read_text(encoding="utf-8") if chapter.is_file() else ""
        for step in workflow.OPTIMIZATION_STEPS:
            quest_id = workflow.workflow_id(stage_id, "optimization", step)
            optimization_total += 1
            if f'id: "{quest_id}"' not in text:
                optimization_missing.append(f"{stage_id}:{step}")
    optimization_ok = not optimization_missing
    rows.append(("Measured optimization quests", f"{optimization_total - len(optimization_missing)}/{optimization_total}", "PASS" if optimization_ok else "FAIL"))
    if optimization_missing:
        failures.append("Missing optimization workflow quests: " + ", ".join(optimization_missing))

    js_files = sorted((ROOT / "kubejs").rglob("*.js"))
    event_subscriptions = 0
    console_calls = 0
    for path in js_files:
        text = path.read_text(encoding="utf-8")
        event_subscriptions += len(re.findall(r"\b(?:ServerEvents|StartupEvents|EntityEvents)\.[A-Za-z_]+\s*\(", text))
        console_calls += len(re.findall(r"\bconsole\.(?:log|info|warn|error)\s*\(", text))

    lines = [
        "# Performance Configuration Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "This is a static safeguard report. It verifies low-risk configuration and script practices before runtime profiling; it does not replace the required TPS, heap and restart measurements.",
        "",
        "| Check | Current | Status |",
        "|---|---|---|",
    ]
    for label, current, status in rows:
        lines.append(f"| {label} | `{current}` | {status} |")
    lines.extend(
        [
            "",
            "## Script inventory",
            "",
            f"- KubeJS JavaScript files: **{len(js_files)}**",
            f"- Event subscriptions found: **{event_subscriptions}**",
            f"- Explicit console calls found: **{console_calls}**",
            f"- Required measured optimization quests: **{optimization_total}**",
            "",
            "## Runtime measurements still required",
            "",
            "- startup and world-open time;",
            "- 30-minute server TPS/MSPT soak with representative factories;",
            "- heap growth and post-GC stability;",
            "- entity and block-entity counts in loaded production chunks;",
            "- repeated-log rate during normal operation;",
            "- clean restart and world reopen after the soak.",
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(f"performance_configuration: {'PASS' if not failures else 'FAIL'}")
    print(f"optimization_quests: {optimization_total - len(optimization_missing)}/{optimization_total}")
    print(f"javascript_files: {len(js_files)}")
    print(f"event_subscriptions: {event_subscriptions}")
    print(f"console_calls: {console_calls}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
