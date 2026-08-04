from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
SERVER_SCRIPTS = ROOT / "kubejs" / "server_scripts"
REPORT_PATH = ROOT / "docs" / "RECIPE_DEPENDENCY_REPORT.md"
OUTPUT_RE = re.compile(r"output:\s*['\"]([^'\"]+)['\"]")
ITEM_RE = re.compile(r"['\"]([a-z0-9_.-]+:[a-z0-9_./-]+)['\"]")


def matching_delimiter(text: str, start: int, opening: str, closing: str) -> int:
    depth = 0
    in_string = False
    escaped = False
    quote = ""
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                in_string = False
            continue
        if char in "'\"":
            in_string = True
            quote = char
        elif char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return index
    raise RuntimeError(f"Unclosed delimiter {opening!r} at {start}")


def brace_spans(text: str) -> list[tuple[int, int]]:
    stack: list[int] = []
    spans: list[tuple[int, int]] = []
    in_string = False
    escaped = False
    quote = ""
    for index, char in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                in_string = False
            continue
        if char in "'\"":
            in_string = True
            quote = char
        elif char == "{":
            stack.append(index)
        elif char == "}" and stack:
            spans.append((stack.pop(), index + 1))
    return spans


def parse_recipe_objects() -> dict[str, dict]:
    # Later scripts and later definitions override earlier recipes, matching the
    # intended z/zz/zzz load order in the pack.
    recipes: dict[str, dict] = {}
    for path in sorted(SERVER_SCRIPTS.glob("*.js")):
        text = path.read_text(encoding="utf-8")
        candidates: list[tuple[int, str, list[str], str]] = []
        for start, end in brace_spans(text):
            block = text[start:end]
            outputs = OUTPUT_RE.findall(block)
            if len(outputs) != 1 or "key:" not in block or "pattern:" not in block:
                continue
            key_marker = block.find("key:")
            key_start = block.find("{", key_marker)
            if key_start < 0:
                continue
            key_end = matching_delimiter(block, key_start, "{", "}")
            ingredients = ITEM_RE.findall(block[key_start : key_end + 1])
            if not ingredients:
                continue
            candidates.append((start, outputs[0], ingredients, str(path.relative_to(ROOT))))
        for _, output, ingredients, relative in sorted(candidates):
            recipes[output] = {"ingredients": ingredients, "source": relative}
    return recipes


def stage_map(contract: dict) -> dict[str, tuple[int, str]]:
    result: dict[str, tuple[int, str]] = {}
    for stage in contract["stages"]:
        for item in stage.get("gated_outputs", []):
            result[item] = (int(stage["index"]), stage["id"])
    return result


def find_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    state: dict[str, int] = {}
    stack: list[str] = []
    cycles: list[list[str]] = []
    seen_cycles: set[tuple[str, ...]] = set()

    def canonical(cycle: list[str]) -> tuple[str, ...]:
        body = cycle[:-1]
        rotations = [tuple(body[index:] + body[:index]) for index in range(len(body))]
        smallest = min(rotations)
        return smallest + (smallest[0],)

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for dependency in sorted(graph.get(node, set())):
            if state.get(dependency, 0) == 0:
                visit(dependency)
            elif state.get(dependency) == 1 and dependency in stack:
                start = stack.index(dependency)
                cycle = stack[start:] + [dependency]
                key = canonical(cycle)
                if key not in seen_cycles:
                    seen_cycles.add(key)
                    cycles.append(list(key))
        stack.pop()
        state[node] = 2

    for node in sorted(graph):
        if state.get(node, 0) == 0:
            visit(node)
    return cycles


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    stages = stage_map(contract)
    recipes = parse_recipe_objects()
    graph: dict[str, set[str]] = {}
    inversions: list[tuple[str, str, int, int, str]] = []
    missing_recipes: list[str] = []

    for output, (output_stage, _) in stages.items():
        definition = recipes.get(output)
        if definition is None:
            graph[output] = set()
            missing_recipes.append(output)
            continue
        dependencies = {item for item in definition["ingredients"] if item in stages}
        graph[output] = dependencies
        for dependency in sorted(dependencies):
            dependency_stage = stages[dependency][0]
            if dependency_stage > output_stage:
                inversions.append(
                    (output, dependency, output_stage, dependency_stage, definition["source"])
                )

    cycles = find_cycles(graph)
    lines = [
        "# Recipe Dependency Report",
        "",
        f"**{'PASS' if not cycles and not inversions else 'FAIL'}**",
        "",
        "## Summary",
        "",
        f"- Gated outputs represented in graph: **{len(graph)}**",
        f"- Parsed final recipe definitions: **{len(recipes)}**",
        f"- Dependency cycles: **{len(cycles)}**",
        f"- Later-stage dependency inversions: **{len(inversions)}**",
        f"- Outputs without a parsed shaped recipe: **{len(missing_recipes)}**",
        "",
    ]
    if cycles:
        lines.extend(["## Cycles", ""])
        lines.extend("- " + " -> ".join(cycle) for cycle in cycles)
        lines.append("")
    if inversions:
        lines.extend(["## Stage inversions", ""])
        for output, dependency, output_stage, dependency_stage, source in inversions:
            lines.append(
                f"- `{output}` (stage {output_stage}) requires `{dependency}` "
                f"(stage {dependency_stage}) in `{source}`"
            )
        lines.append("")
    if missing_recipes:
        lines.extend([
            "## Non-shaped or externally produced outputs",
            "",
            "These are reported for review but are not graph failures; seals and machine-process outputs are expected here.",
            "",
        ])
        lines.extend(f"- `{item}`" for item in missing_recipes)
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"recipe_dependency: {'PASS' if not cycles and not inversions else 'FAIL'}")
    print(f"cycles: {len(cycles)}")
    print(f"stage_inversions: {len(inversions)}")
    return 1 if cycles or inversions else 0


if __name__ == "__main__":
    sys.exit(main())
