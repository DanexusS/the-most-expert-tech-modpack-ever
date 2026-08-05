from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import recipe_dependency_audit as dependency

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
REPORT_PATH = ROOT / "docs" / "RECIPE_FAIRNESS_REPORT.md"
SERVER_SCRIPTS = ROOT / "kubejs" / "server_scripts"
OUTPUT_RE = re.compile(r"output:\s*['\"]([^'\"]+)['\"]")
ITEM_RE = re.compile(r"['\"]([a-z0-9_.-]+:[a-z0-9_./-]+)['\"]")
STRING_RE = re.compile(r"['\"]([^'\"]*)['\"]")


def parse_recipe_details() -> dict[str, dict]:
    recipes: dict[str, dict] = {}
    for path in sorted(SERVER_SCRIPTS.glob("*.js")):
        text = path.read_text(encoding="utf-8")
        candidates: list[tuple[int, str, dict]] = []
        for start, end in dependency.brace_spans(text):
            block = text[start:end]
            outputs = OUTPUT_RE.findall(block)
            if len(outputs) != 1 or "key:" not in block or "pattern:" not in block:
                continue

            key_marker = block.find("key:")
            key_start = block.find("{", key_marker)
            if key_start < 0:
                continue
            key_end = dependency.matching_delimiter(block, key_start, "{", "}")
            ingredients = ITEM_RE.findall(block[key_start : key_end + 1])
            if not ingredients:
                continue

            pattern_marker = block.find("pattern:")
            pattern_start = block.find("[", pattern_marker)
            if pattern_start < 0:
                continue
            pattern_end = dependency.matching_delimiter(block, pattern_start, "[", "]")
            rows = STRING_RE.findall(block[pattern_start : pattern_end + 1])
            symbol_counts = Counter(char for row in rows for char in row if not char.isspace())
            slot_count = sum(symbol_counts.values())

            definition = {
                "ingredients": ingredients,
                "source": str(path.relative_to(ROOT)),
                "slot_count": slot_count,
                "rows": rows,
                "authoritative": bool(
                    re.search(r"\bauthoritative\s*:\s*true\b", block)
                ),
                "max_symbol_slots": max(symbol_counts.values(), default=0),
            }
            candidates.append((start, outputs[0], definition))

        for _, output, definition in sorted(candidates):
            recipes[output] = definition
    return recipes


def milestone_map(contract: dict) -> dict[str, tuple[int, str]]:
    return {
        stage["milestone"]: (int(stage["index"]), stage["id"])
        for stage in contract["stages"]
    }


def milestone_thresholds(stage: int) -> tuple[int, int, int, int]:
    if stage == 1:
        return 4, 2, 5, 0
    if stage <= 3:
        return 5, 2, 7, 1
    if stage <= 8:
        return 6, 3, 7, 2
    return 7, 3, 9, 2


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    stages = dependency.stage_map(contract)
    milestones = milestone_map(contract)
    recipes = parse_recipe_details()

    failures: list[str] = []
    rows: list[dict] = []

    for output, (stage_index, stage_id) in sorted(
        stages.items(), key=lambda entry: (entry[1][0], entry[0])
    ):
        definition = recipes.get(output)
        if definition is None:
            continue

        ingredients = list(dict.fromkeys(definition["ingredients"]))
        namespaces = {item.split(":", 1)[0] for item in ingredients}
        prior_dependencies = {
            item
            for item in ingredients
            if item in stages and stages[item][0] < stage_index
        }
        is_milestone = output in milestones
        item_failures: list[str] = []

        if output in ingredients:
            item_failures.append("direct self-reference")
        if len(ingredients) < 2:
            item_failures.append("fewer than two distinct ingredients")
        if int(definition["slot_count"]) < 3:
            item_failures.append("fewer than three occupied crafting slots")
        if stage_index >= 4 and len(namespaces) < 2:
            item_failures.append("single-namespace strategic recipe")
        if stage_index >= 4 and not definition["authoritative"]:
            item_failures.append("missing authoritative recipe marker")
        if (
            int(definition["slot_count"]) >= 7
            and int(definition["max_symbol_slots"]) >= int(definition["slot_count"]) - 1
        ):
            item_failures.append("one ingredient dominates almost every slot")

        if is_milestone:
            min_ingredients, min_namespaces, min_slots, min_prior = milestone_thresholds(
                stage_index
            )
            if len(ingredients) < min_ingredients:
                item_failures.append(
                    f"milestone has {len(ingredients)} ingredients; requires {min_ingredients}"
                )
            if len(namespaces) < min_namespaces:
                item_failures.append(
                    f"milestone uses {len(namespaces)} namespaces; requires {min_namespaces}"
                )
            if int(definition["slot_count"]) < min_slots:
                item_failures.append(
                    f"milestone occupies {definition['slot_count']} slots; requires {min_slots}"
                )
            if len(prior_dependencies) < min_prior:
                item_failures.append(
                    f"milestone consumes {len(prior_dependencies)} prior gated outputs; requires {min_prior}"
                )
            if not definition["authoritative"]:
                item_failures.append("milestone is not marked authoritative")

        for failure in item_failures:
            failures.append(f"{output}: {failure}")

        rows.append(
            {
                "stage": stage_index,
                "stage_id": stage_id,
                "output": output,
                "milestone": is_milestone,
                "ingredients": len(ingredients),
                "namespaces": len(namespaces),
                "slots": int(definition["slot_count"]),
                "prior": len(prior_dependencies),
                "authoritative": bool(definition["authoritative"]),
                "status": "PASS" if not item_failures else "FAIL",
                "source": definition["source"],
            }
        )

    lines = [
        "# Strategic Recipe Fairness Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "This gate checks shaped recipes for staged outputs. It enforces meaningful ingredient diversity, cross-mod integration, occupied crafting space, prior-stage convergence and authoritative replacement markers. It does not equate raw ingredient count with play quality; runtime throughput and player testing remain separate gates.",
        "",
        "| Stage | Output | Milestone | Ingredients | Namespaces | Slots | Prior gated | Authoritative | Status |",
        "|---:|---|---|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['stage']} | `{row['output']}` | "
            f"{'yes' if row['milestone'] else 'no'} | {row['ingredients']} | "
            f"{row['namespaces']} | {row['slots']} | {row['prior']} | "
            f"{'yes' if row['authoritative'] else 'no'} | {row['status']} |"
        )

    lines.extend(
        [
            "",
            "## Aggregate",
            "",
            f"- Parsed shaped strategic outputs: **{len(rows)}**",
            f"- Milestones with shaped recipes: **{sum(row['milestone'] for row in rows)} / 18**",
            f"- Authoritative strategic recipes: **{sum(row['authoritative'] for row in rows)} / {len(rows)}**",
            f"- Failures: **{len(failures)}**",
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"recipe_fairness: {'PASS' if not failures else 'FAIL'}")
    print(f"strategic_recipes: {len(rows)}")
    print(f"milestone_recipes: {sum(row['milestone'] for row in rows)}/18")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
