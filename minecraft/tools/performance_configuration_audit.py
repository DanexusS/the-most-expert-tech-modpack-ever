from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import generate_early_stage_workflow_expansions as workflow
import generate_stage_depth_program as depth
from advanced_stage_workflow_profiles import ADVANCED_STAGE_WORKFLOW_PROFILES
from catalog_upgrade_common import quest_spans
from late_stage_workflow_profiles import LATE_STAGE_WORKFLOW_PROFILES
from mid_stage_workflow_profiles import MID_STAGE_WORKFLOW_PROFILES

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "expert_performance_policy.json"
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
QUEST_DATA_PATH = ROOT / "config" / "ftbquests" / "quests" / "data.snbt"
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
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


def add_workflow_profiles() -> None:
    additions = {}
    for profiles in (
        MID_STAGE_WORKFLOW_PROFILES,
        ADVANCED_STAGE_WORKFLOW_PROFILES,
        LATE_STAGE_WORKFLOW_PROFILES,
    ):
        overlap = (set(workflow.WORKFLOW_STAGES) | set(additions)) & set(profiles)
        if overlap:
            raise RuntimeError(
                "Duplicate performance workflow profiles: " + ", ".join(sorted(overlap))
            )
        additions.update(profiles)
    workflow.WORKFLOW_STAGES.update(additions)


def main() -> int:
    add_workflow_profiles()
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    stages = contract["stages"]
    stage_indexes = {stage["id"]: int(stage["index"]) for stage in stages}
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
    for key, expected in (
        ("useLoggingLog", bool(logging["coroutil_routine_logging"])),
        ("useLoggingDebug", bool(logging["coroutil_debug_logging"])),
        ("useLoggingError", bool(logging["coroutil_error_logging"])),
    ):
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

    workflow_total = 0
    workflow_missing: list[str] = []
    depth_total = 0
    depth_missing: list[str] = []
    stage_counts: list[int] = []
    total_quests = 0

    for stage in stages:
        stage_id = stage["id"]
        index = stage_indexes[stage_id]
        chapter = CHAPTER_DIR / f"main_stage_{index:02d}_{stage_id}.snbt"
        text = chapter.read_text(encoding="utf-8") if chapter.is_file() else ""
        stage_count = len(quest_spans(text)) if text else 0
        stage_counts.append(stage_count)

        for step in workflow.OPTIMIZATION_STEPS:
            quest_id = workflow.workflow_id(stage_id, "optimization", step)
            workflow_total += 1
            if f'id: "{quest_id}"' not in text:
                workflow_missing.append(f"{stage_id}:{step}")

        for phase in depth.PHASES:
            quest_id = depth.depth_id(stage_id, "performance_optimization", phase[0])
            depth_total += 1
            if f'id: "{quest_id}"' not in text:
                depth_missing.append(f"{stage_id}:{phase[0]}")

    for chapter in CHAPTER_DIR.glob("*.snbt"):
        try:
            total_quests += len(quest_spans(chapter.read_text(encoding="utf-8")))
        except RuntimeError:
            continue

    guidance = policy["factory_guidance"]
    workflow_min = int(guidance["minimum_workflow_optimization_quests"])
    depth_min = int(guidance["minimum_depth_optimization_quests"])
    workflow_ok = not workflow_missing and workflow_total >= workflow_min
    depth_ok = not depth_missing and depth_total >= depth_min
    rows.append(("Workflow optimization quests", f"{workflow_total - len(workflow_missing)}/{workflow_total}", "PASS" if workflow_ok else "FAIL"))
    rows.append(("Depth optimization quests", f"{depth_total - len(depth_missing)}/{depth_total}", "PASS" if depth_ok else "FAIL"))
    if not workflow_ok:
        failures.append("Missing workflow optimization quests: " + ", ".join(workflow_missing))
    if not depth_ok:
        failures.append("Missing depth optimization quests: " + ", ".join(depth_missing))

    quest_budgets = policy["questbook_budgets"]
    minimum_stage = int(quest_budgets["minimum_mandatory_quests_per_stage"])
    maximum_stage = int(quest_budgets["maximum_mandatory_quests_per_stage"])
    maximum_total = int(quest_budgets["maximum_total_quests"])
    stage_budget_ok = bool(stage_counts) and all(minimum_stage <= count <= maximum_stage for count in stage_counts)
    total_budget_ok = total_quests <= maximum_total
    rows.append(("Mandatory quests per stage", f"min={min(stage_counts, default=0)}, max={max(stage_counts, default=0)}", "PASS" if stage_budget_ok else "FAIL"))
    rows.append(("Total questbook size", f"{total_quests}/{maximum_total}", "PASS" if total_budget_ok else "FAIL"))
    if not stage_budget_ok:
        failures.append(
            f"Mandatory stage quest counts must stay within {minimum_stage}–{maximum_stage}; found {stage_counts}"
        )
    if not total_budget_ok:
        failures.append(f"Questbook contains {total_quests} quests, above the budget {maximum_total}")

    js_files = sorted((ROOT / "kubejs").rglob("*.js"))
    event_subscriptions = 0
    console_calls = 0
    for path in js_files:
        script = path.read_text(encoding="utf-8")
        event_subscriptions += len(
            re.findall(r"\b(?:ServerEvents|StartupEvents|EntityEvents)\.[A-Za-z_]+\s*\(", script)
        )
        console_calls += len(
            re.findall(r"\bconsole\.(?:log|info|warn|error)\s*\(", script)
        )

    script_budgets = policy["script_budgets"]
    script_checks = (
        ("KubeJS JavaScript files", len(js_files), int(script_budgets["maximum_javascript_files"])),
        ("Event subscriptions", event_subscriptions, int(script_budgets["maximum_event_subscriptions"])),
        ("Explicit console calls", console_calls, int(script_budgets["maximum_console_calls"])),
    )
    for label, current, maximum in script_checks:
        ok = current <= maximum
        rows.append((label, f"{current}/{maximum}", "PASS" if ok else "FAIL"))
        if not ok:
            failures.append(f"{label} exceeds budget: {current} > {maximum}")

    lines = [
        "# Performance Configuration Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "This static safeguard verifies low-risk configuration, bounded questbook growth and script budgets before runtime profiling. It does not replace TPS, heap and restart measurements.",
        "",
        "| Check | Current | Status |",
        "|---|---|---|",
    ]
    for label, current, status in rows:
        lines.append(f"| {label} | `{current}` | {status} |")
    lines.extend(
        [
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
    print(f"workflow_optimization_quests: {workflow_total - len(workflow_missing)}/{workflow_total}")
    print(f"depth_optimization_quests: {depth_total - len(depth_missing)}/{depth_total}")
    print(f"total_quests: {total_quests}")
    print(f"javascript_files: {len(js_files)}")
    print(f"event_subscriptions: {event_subscriptions}")
    print(f"console_calls: {console_calls}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
