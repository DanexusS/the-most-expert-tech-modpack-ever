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
            symbol_counts = Counter(
                char for row in rows for char in row if not char.isspace()
            )
            candidates.append(
                (
                    start,
                    outputs[0],
                    {
                        "ingredients": ingredients,
                        "source": str(path.relative_to(ROOT)),
                        "slot_count": sum(symbol_counts.values()),
                        "rows": rows,
                        "authoritative": bool(
                            re.search(r"\bauthoritative\s*:\s*true\b", block)
                        ),
                        "max_symbol_slots": max(symbol_counts.values(), default=0),
                    },
                )
            )

        # Paths are processed in load order and later declarations replace earlier
        # declarations for the same output, matching KubeJS recipe-layer intent.
        for _, output, definition in sorted(candidates):
            recipes[output] = definition
    return recipes


def milestone_map(contract: dict) -> dict[str, tuple[int, str]]:
    return {
        stage["milestone"]: (int(stage["index"]), stage["id"])
        for stage in contract["stages"]
    }


def milestone_thresholds(stage: int) -> tuple[int, int, int, int]:
    # Direct ingredient count is intentionally modest: expert components hide
    # substantial work. Provenance and transitive gated convergence measure the
    # actual cross-mod depth instead of punishing reusable assemblies.
    if stage == 1:
        return 4, 2, 5, 0
    if stage <= 3:
        return 4, 3, 7, 1
    if stage <= 8:
        return 4, 3, 7, 2
    return 4, 4, 9, 2


def namespace_of(item: str) -> str:
    return item.split(":", 1)[0]


def transitive_provenance(
    item: str,
    recipes: dict[str, dict],
    memo: dict[str, set[str]],
    stack: set[str],
) -> set[str]:
    if item in memo:
        return set(memo[item])
    if item in stack:
        return {namespace_of(item)}

    definition = recipes.get(item)
    if definition is None:
        result = {namespace_of(item)}
    else:
        next_stack = set(stack)
        next_stack.add(item)
        result: set[str] = set()
        for ingredient in definition["ingredients"]:
            result.update(
                transitive_provenance(ingredient, recipes, memo, next_stack)
            )
        if not result:
            result.add(namespace_of(item))

    memo[item] = set(result)
    return result


def transitive_gated_dependencies(
    item: str,
    output_stage: int,
    stages: dict[str, tuple[int, str]],
    recipes: dict[str, dict],
    memo: dict[tuple[str, int], set[str]],
    stack: set[str],
) -> set[str]:
    key = (item, output_stage)
    if key in memo:
        return set(memo[key])
    if item in stack:
        return set()

    result: set[str] = set()
    definition = recipes.get(item)
    if definition is not None:
        next_stack = set(stack)
        next_stack.add(item)
        for ingredient in definition["ingredients"]:
            ingredient_stage = stages.get(ingredient)
            if ingredient_stage is not None and ingredient_stage[0] < output_stage:
                result.add(ingredient)
            result.update(
                transitive_gated_dependencies(
                    ingredient,
                    output_stage,
                    stages,
                    recipes,
                    memo,
                    next_stack,
                )
            )

    memo[key] = set(result)
    return result


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    stages = dependency.stage_map(contract)
    milestones = milestone_map(contract)
    recipes = parse_recipe_details()
    provenance_memo: dict[str, set[str]] = {}
    gated_memo: dict[tuple[str, int], set[str]] = {}

    failures: list[str] = []
    rows: list[dict] = []

    for output, (stage_index, stage_id) in sorted(
        stages.items(), key=lambda entry: (entry[1][0], entry[0])
    ):
        definition = recipes.get(output)
        if definition is None:
            continue

        ingredients = list(dict.fromkeys(definition["ingredients"]))
        direct_namespaces = {namespace_of(item) for item in ingredients}
        provenance_namespaces: set[str] = set()
        for ingredient in ingredients:
            provenance_namespaces.update(
                transitive_provenance(ingredient, recipes, provenance_memo, set())
            )

        direct_prior = {
            item
            for item in ingredients
            if item in stages and stages[item][0] < stage_index
        }
        transitive_prior = transitive_gated_dependencies(
            output,
            stage_index,
            stages,
            recipes,
            gated_memo,
            set(),
        )
        is_milestone = output in milestones
        item_failures: list[str] = []

        if output in ingredients:
            item_failures.append("direct self-reference")
        if len(ingredients) < 2:
            item_failures.append("fewer than two distinct direct ingredients")
        if int(definition["slot_count"]) < 3:
            item_failures.append("fewer than three occupied crafting slots")
        if stage_index >= 4 and len(provenance_namespaces) < 2:
            item_failures.append("single-provenance strategic recipe")
        if stage_index >= 4 and not definition["authoritative"]:
            item_failures.append("missing authoritative recipe marker")
        if (
            int(definition["slot_count"]) >= 7
            and int(definition["max_symbol_slots"])
            >= int(definition["slot_count"]) - 1
        ):
            item_failures.append("one ingredient dominates almost every slot")

        if is_milestone:
            min_direct, min_provenance, min_slots, min_prior = milestone_thresholds(
                stage_index
            )
            if len(ingredients) < min_direct:
                item_failures.append(
                    f"milestone has {len(ingredients)} direct ingredients; requires {min_direct}"
                )
            if len(provenance_namespaces) < min_provenance:
                item_failures.append(
                    "milestone has "
                    f"{len(provenance_namespaces)} provenance namespaces; "
                    f"requires {min_provenance}"
                )
            if int(definition["slot_count"]) < min_slots:
                item_failures.append(
                    f"milestone occupies {definition['slot_count']} slots; requires {min_slots}"
                )
            if len(transitive_prior) < min_prior:
                item_failures.append(
                    "milestone consumes "
                    f"{len(transitive_prior)} transitive prior gated outputs; "
                    f"requires {min_prior}"
                )
            if not definition["authoritative"]:
                item_failures.append("milestone is not marked authoritative")

        failures.extend(f"{output}: {failure}" for failure in item_failures)
        rows.append(
            {
                "stage": stage_index,
                "stage_id": stage_id,
                "output": output,
                "milestone": is_milestone,
                "ingredients": len(ingredients),
                "direct_namespaces": len(direct_namespaces),
                "provenance_namespaces": len(provenance_namespaces),
                "slots": int(definition["slot_count"]),
                "direct_prior": len(direct_prior),
                "transitive_prior": len(transitive_prior),
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
        "This gate evaluates the final shaped recipe for each staged output. It expands reusable assemblies recursively, so cross-mod provenance and prior-stage convergence are measured through the complete dependency tree rather than by counting only direct KubeJS ingredients. Runtime throughput and player testing remain separate gates.",
        "",
        "| Stage | Output | Milestone | Direct ingredients | Direct NS | Provenance NS | Slots | Direct prior | Transitive prior | Authoritative | Status |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['stage']} | `{row['output']}` | "
            f"{'yes' if row['milestone'] else 'no'} | {row['ingredients']} | "
            f"{row['direct_namespaces']} | {row['provenance_namespaces']} | "
            f"{row['slots']} | {row['direct_prior']} | "
            f"{row['transitive_prior']} | "
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
