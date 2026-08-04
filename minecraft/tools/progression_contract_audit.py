from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
REPORT_PATH = ROOT / "docs" / "PROGRESSION_CONTRACT_REPORT.md"
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
STARTUP_COMPONENTS = ROOT / "kubejs" / "startup_scripts" / "expert_components.js"
SERVER_SCRIPTS = ROOT / "kubejs" / "server_scripts"

OUTPUT_RE = re.compile(r"output:\s*['\"]([^'\"]+)['\"]")
REGISTERED_COMPONENT_RE = re.compile(r"\['([a-z0-9_]+)',\s*'[^']+',\s*'[^']+'\]")
QUEST_ID_RE = re.compile(r'(?m)^\s*id:\s*"([0-9A-F]{16})"')


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def recipe_outputs() -> Counter[str]:
    counter: Counter[str] = Counter()
    for path in sorted(SERVER_SCRIPTS.rglob("*.js")):
        for output in OUTPUT_RE.findall(path.read_text(encoding="utf-8")):
            counter[output] += 1
    return counter


def registered_kubejs_items() -> set[str]:
    text = STARTUP_COMPONENTS.read_text(encoding="utf-8")
    return {f"kubejs:{name}" for name in REGISTERED_COMPONENT_RE.findall(text)}


def quest_count() -> int:
    total = 0
    for path in CHAPTER_DIR.glob("*.snbt"):
        text = path.read_text(encoding="utf-8")
        marker = text.find("quests:")
        if marker < 0:
            continue
        # Every quest and task has an ID. Quest blocks are identified by the
        # first-level task marker count used by the existing quality audit.
        total += len(re.findall(r'(?m)^\t\t\{\n(?:.|\n)*?^\t\t\}', text[marker:]))
    # The broad block pattern may undercount unusual formatting. Use the stable
    # known relationship from quest files when the quality report is available.
    quality_report = ROOT / "docs" / "QUEST_QUALITY_REPORT.md"
    if quality_report.is_file():
        match = re.search(r"Quests parsed:\s*\*\*([0-9]+)\*\*", quality_report.read_text(encoding="utf-8"))
        if match:
            return int(match.group(1))
    return total


def audit(contract: dict) -> tuple[list[str], dict]:
    failures: list[str] = []
    stages = contract.get("stages", [])
    indices = [stage.get("index") for stage in stages]
    stage_ids = [stage.get("id") for stage in stages]
    milestones = [stage.get("milestone") for stage in stages]
    all_gated = [item for stage in stages for item in stage.get("gated_outputs", [])]
    outputs = recipe_outputs()
    registered = registered_kubejs_items()

    if len(stages) != 18:
        failures.append(f"Expected 18 macro stages, found {len(stages)}")
    if indices != list(range(1, len(stages) + 1)):
        failures.append(f"Stage indices are not sequential: {indices}")
    if len(stage_ids) != len(set(stage_ids)):
        failures.append("Duplicate stage IDs")
    if len(milestones) != len(set(milestones)):
        failures.append("Duplicate milestone item IDs")

    quest_budget = sum(int(stage.get("quest_budget", 0)) for stage in stages)
    target_min = int(contract.get("quest_target_min", 5000))
    target_max = int(contract.get("quest_target_max", 6000))
    if not target_min <= quest_budget <= target_max:
        failures.append(f"Quest budget {quest_budget} is outside {target_min}-{target_max}")
    if quest_budget != int(contract.get("quest_target", quest_budget)):
        failures.append("Stage quest budgets do not equal quest_target")

    substage_count = sum(len(stage.get("substages", [])) for stage in stages)
    minimum_substages = int(contract.get("minimum_substages", 60))
    if substage_count < minimum_substages:
        failures.append(f"Only {substage_count} substages; minimum is {minimum_substages}")

    for stage in stages:
        if len(stage.get("substages", [])) < 4:
            failures.append(f"{stage.get('id')}: fewer than four substages")
        if stage.get("index", 0) > 1 and len(set(stage.get("required_domains", []))) < 2:
            failures.append(f"{stage.get('id')}: fewer than two required domains")
        milestone = stage.get("milestone", "")
        if milestone.startswith("kubejs:") and milestone not in registered:
            failures.append(f"{stage.get('id')}: unregistered milestone {milestone}")

    duplicate_gates = sorted(item for item, count in Counter(all_gated).items() if count > 1)
    if duplicate_gates:
        failures.append("Gated outputs assigned to multiple stages: " + ", ".join(duplicate_gates))

    missing_authoritative = sorted(item for item in all_gated if outputs[item] == 0)
    multiple_recipe_mentions = sorted(item for item in all_gated if outputs[item] > 1)

    current_quests = quest_count()
    metrics = {
        "stages": len(stages),
        "substages": substage_count,
        "quest_budget": quest_budget,
        "current_quests": current_quests,
        "quest_gap": max(0, quest_budget - current_quests),
        "gated_outputs": len(all_gated),
        "missing_authoritative": missing_authoritative,
        "multiple_recipe_mentions": multiple_recipe_mentions,
        "structural_failures": failures,
    }
    return failures, metrics


def render(metrics: dict) -> str:
    structural_failures = metrics["structural_failures"]
    missing = metrics["missing_authoritative"]
    status = "PASS" if not structural_failures and not missing else "IN PROGRESS"
    lines = [
        "# Progression Contract Report",
        "",
        f"**{status}**",
        "",
        "## Contract metrics",
        "",
        f"- Macro stages: **{metrics['stages']}**",
        f"- Mandatory substages: **{metrics['substages']}**",
        f"- Planned quest budget: **{metrics['quest_budget']}**",
        f"- Current parsed quests: **{metrics['current_quests']}**",
        f"- Remaining quest budget: **{metrics['quest_gap']}**",
        f"- Gated outputs: **{metrics['gated_outputs']}**",
        f"- Gated outputs without a recipe declaration: **{len(missing)}**",
        "",
    ]
    if structural_failures:
        lines.extend(["## Structural failures", ""])
        lines.extend(f"- {failure}" for failure in structural_failures)
        lines.append("")
    if missing:
        lines.extend(["## Outputs still requiring an authoritative path", ""])
        lines.extend(f"- `{item}`" for item in missing)
        lines.append("")
    if metrics["multiple_recipe_mentions"]:
        lines.extend([
            "## Outputs mentioned by multiple recipe definitions",
            "",
            "These are not automatically failures because the v1 override removes legacy outputs at runtime, but each entry requires bypass review.",
            "",
        ])
        lines.extend(f"- `{item}`" for item in metrics["multiple_recipe_mentions"])
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    failures, metrics = audit(load_contract())
    REPORT_PATH.write_text(render(metrics), encoding="utf-8", newline="\n")
    incomplete = bool(failures or metrics["missing_authoritative"])
    print(f"progression_contract: {'IN PROGRESS' if incomplete else 'PASS'}")
    print(f"stages: {metrics['stages']}")
    print(f"substages: {metrics['substages']}")
    print(f"quest_budget: {metrics['quest_budget']}")
    print(f"quest_gap: {metrics['quest_gap']}")
    print(f"missing_authoritative: {len(metrics['missing_authoritative'])}")
    return 1 if args.strict and incomplete else 0


if __name__ == "__main__":
    raise SystemExit(main())
