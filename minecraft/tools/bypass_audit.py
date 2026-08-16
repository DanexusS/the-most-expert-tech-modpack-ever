from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
POLICY_PATH = ROOT / "config" / "expert_bypass_policy.json"
REPORT_PATH = ROOT / "docs" / "BYPASS_AUDIT_REPORT.md"
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
SERVER_SCRIPTS = ROOT / "kubejs" / "server_scripts"

OUTPUT_RE = re.compile(r"output:\s*['\"]([^'\"]+)['\"]")
REMOVE_OUTPUT_RE = re.compile(r"event\.remove\(\{\s*output:\s*['\"]([^'\"]+)['\"]")


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
    raise RuntimeError(f"Unclosed delimiter at {start}")


def brace_blocks(text: str) -> list[str]:
    stack: list[int] = []
    blocks: list[str] = []
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
            start = stack.pop()
            blocks.append(text[start : index + 1])
    return blocks


def named_arrays(text: str, marker: str) -> list[str]:
    arrays: list[str] = []
    offset = 0
    while True:
        marker_index = text.find(marker, offset)
        if marker_index < 0:
            break
        start = text.find("[", marker_index)
        if start < 0:
            break
        end = matching_delimiter(text, start, "[", "]")
        arrays.append(text[start + 1 : end])
        offset = end + 1
    return arrays


def object_blocks(text: str, marker: str) -> list[str]:
    blocks: list[str] = []
    offset = 0
    while True:
        marker_index = text.find(marker, offset)
        if marker_index < 0:
            break
        start = text.find("{", marker_index)
        if start < 0:
            break
        end = matching_delimiter(text, start, "{", "}")
        blocks.append(text[start + 1 : end])
        offset = end + 1
    return blocks


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def gated_outputs(contract: dict) -> dict[str, str]:
    result: dict[str, str] = {}
    for stage in contract.get("stages", []):
        stage_id = stage["id"]
        for item in stage.get("gated_outputs", []):
            result[item] = stage_id
    return result


def recipe_evidence(items: set[str]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    declarations: dict[str, list[str]] = defaultdict(list)
    removals: dict[str, list[str]] = defaultdict(list)
    for path in sorted(SERVER_SCRIPTS.rglob("*.js")):
        relative = str(path.relative_to(ROOT))
        text = path.read_text(encoding="utf-8")
        for item in OUTPUT_RE.findall(text):
            if item in items:
                declarations[item].append(relative)
        for item in REMOVE_OUTPUT_RE.findall(text):
            if item in items:
                removals[item].append(relative)
        # The v1 helper performs event.remove when an object is marked
        # authoritative. Treat that declaration as explicit removal evidence.
        for block in brace_blocks(text):
            if not re.search(r"\bauthoritative\s*:\s*true\b", block):
                continue
            for item in OUTPUT_RE.findall(block):
                if item in items:
                    removals[item].append(relative + " (authoritative definition)")
    return declarations, removals


def quest_reward_sources(items: set[str]) -> dict[str, list[str]]:
    sources: dict[str, list[str]] = defaultdict(list)
    for path in sorted(CHAPTER_DIR.glob("*.snbt")):
        text = path.read_text(encoding="utf-8")
        for reward_array in named_arrays(text, "rewards:"):
            for item_block in object_blocks(reward_array, "item:"):
                match = re.search(r'(?m)^\s*id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', item_block)
                if match and match.group(1) in items:
                    sources[match.group(1)].append(str(path.relative_to(ROOT)))
    return sources


def data_sources(items: set[str]) -> dict[str, list[str]]:
    sources: dict[str, list[str]] = defaultdict(list)
    roots = [
        ROOT / "kubejs" / "data",
        ROOT / "defaultconfigs",
        ROOT / "datapacks",
        ROOT / "config" / "openloader",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".json", ".snbt", ".toml", ".cfg", ".js"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for item in items:
                if item in text:
                    sources[item].append(str(path.relative_to(ROOT)))
    return sources


def stage_index(contract: dict, stage_id: str) -> int:
    return next(stage["index"] for stage in contract["stages"] if stage["id"] == stage_id)


def audit(contract: dict, policy: dict) -> dict:
    stage_by_item = gated_outputs(contract)
    items = set(stage_by_item)
    declarations, removals = recipe_evidence(items)
    quest_rewards = quest_reward_sources(items)
    data_mentions = data_sources(items)

    reward_allowlist = set(policy.get("quest_reward_allowlist", []))
    loot_allowlist = set(policy.get("loot_allowlist", []))
    authorized_non_recipe = policy.get("authorized_non_recipe_sources", {})
    emc_blacklist = set(policy.get("emc_blacklist", []))
    simulation_blacklist = set(policy.get("resource_simulation_blacklist", []))
    trade_blacklist = set(policy.get("trade_blacklist", []))

    unauthorized_rewards = {
        item: paths for item, paths in quest_rewards.items() if item not in reward_allowlist
    }
    unauthorized_data = {
        item: paths for item, paths in data_mentions.items() if item not in loot_allowlist
    }
    no_authoritative_path = sorted(
        item for item in items
        if item not in declarations and item not in authorized_non_recipe
    )
    recipe_without_removal = sorted(
        item for item in items
        if item in declarations
        and not item.startswith("kubejs:")
        and item not in removals
    )

    late_items = {
        item for item, stage in stage_by_item.items()
        if stage_index(contract, stage) >= 9
    }
    emc_policy_gaps = sorted(late_items - emc_blacklist)

    simulation_sensitive = {
        item for item, stage in stage_by_item.items()
        if stage_index(contract, stage) >= 12
    }
    simulation_policy_gaps = sorted(simulation_sensitive - simulation_blacklist)

    trade_sensitive = {
        item for item, stage in stage_by_item.items()
        if stage_index(contract, stage) >= 10 and not item.startswith("kubejs:")
    }
    trade_policy_gaps = sorted(trade_sensitive - trade_blacklist)

    return {
        "stage_by_item": stage_by_item,
        "declarations": declarations,
        "removals": removals,
        "authorized_non_recipe": {
            item: reason for item, reason in authorized_non_recipe.items() if item in items
        },
        "quest_rewards": quest_rewards,
        "data_mentions": data_mentions,
        "unauthorized_rewards": unauthorized_rewards,
        "unauthorized_data": unauthorized_data,
        "no_authoritative_path": no_authoritative_path,
        "recipe_without_removal": recipe_without_removal,
        "emc_policy_gaps": emc_policy_gaps,
        "simulation_policy_gaps": simulation_policy_gaps,
        "trade_policy_gaps": trade_policy_gaps,
    }


def blocking(result: dict) -> bool:
    return any([
        result["unauthorized_rewards"],
        result["unauthorized_data"],
        result["no_authoritative_path"],
        result["recipe_without_removal"],
        result["emc_policy_gaps"],
        result["simulation_policy_gaps"],
        result["trade_policy_gaps"],
    ])


def render(result: dict) -> str:
    lines = [
        "# Bypass Audit Report",
        "",
        f"**{'IN PROGRESS' if blocking(result) else 'PASS'}**",
        "",
        "This report tracks known static acquisition paths. A PASS means the source tree contains an explicit policy and authoritative recipe or process evidence; it does not claim that every third-party runtime mechanic has already been tested.",
        "",
        "## Summary",
        "",
        f"- Gated outputs: **{len(result['stage_by_item'])}**",
        f"- Outputs with recipe declarations: **{len(result['declarations'])}**",
        f"- Outputs with explicit recipe removal evidence: **{len(result['removals'])}**",
        f"- Authorized process or unique-permission outputs: **{len(result['authorized_non_recipe'])}**",
        f"- Unauthorized quest reward outputs: **{len(result['unauthorized_rewards'])}**",
        f"- Unallowlisted data/loot mentions: **{len(result['unauthorized_data'])}**",
        f"- Outputs without an authoritative path: **{len(result['no_authoritative_path'])}**",
        f"- Non-KubeJS recipe outputs without removal evidence: **{len(result['recipe_without_removal'])}**",
        f"- Late outputs missing EMC policy: **{len(result['emc_policy_gaps'])}**",
        f"- Stage 12+ outputs missing simulation policy: **{len(result['simulation_policy_gaps'])}**",
        f"- Stage 10+ non-KubeJS outputs missing trade policy: **{len(result['trade_policy_gaps'])}**",
        "",
    ]

    sections = [
        ("Unauthorized quest rewards", result["unauthorized_rewards"]),
        ("Unallowlisted data or loot sources", result["unauthorized_data"]),
        ("Outputs without an authoritative path", result["no_authoritative_path"]),
        ("Non-KubeJS outputs without removal evidence", result["recipe_without_removal"]),
        ("EMC policy gaps", result["emc_policy_gaps"]),
        ("Resource simulation policy gaps", result["simulation_policy_gaps"]),
        ("Trade policy gaps", result["trade_policy_gaps"]),
    ]
    for title, values in sections:
        if not values:
            continue
        lines.extend([f"## {title}", ""])
        if isinstance(values, dict):
            for item, paths in sorted(values.items()):
                lines.append(f"- `{item}`: {', '.join(sorted(set(paths)))}")
        else:
            lines.extend(f"- `{item}`" for item in values)
        lines.append("")

    if result["authorized_non_recipe"]:
        lines.extend(["## Authorized non-crafting paths", ""])
        for item, reason in sorted(result["authorized_non_recipe"].items()):
            lines.append(f"- `{item}` — {reason}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    result = audit(load_json(CONTRACT_PATH), load_json(POLICY_PATH))
    REPORT_PATH.write_text(render(result), encoding="utf-8", newline="\n")
    print(f"bypass_audit: {'IN PROGRESS' if blocking(result) else 'PASS'}")
    print(f"gated_outputs: {len(result['stage_by_item'])}")
    print(f"unauthorized_rewards: {len(result['unauthorized_rewards'])}")
    print(f"missing_paths: {len(result['no_authoritative_path'])}")
    print(f"missing_removals: {len(result['recipe_without_removal'])}")
    print(f"trade_policy_gaps: {len(result['trade_policy_gaps'])}")
    return 1 if args.strict and blocking(result) else 0


if __name__ == "__main__":
    raise SystemExit(main())
