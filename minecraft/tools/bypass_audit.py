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
        text = path.read_text(encoding="utf-8")
        for item in OUTPUT_RE.findall(text):
            if item in items:
                declarations[item].append(str(path.relative_to(ROOT)))
        for item in REMOVE_OUTPUT_RE.findall(text):
            if item in items:
                removals[item].append(str(path.relative_to(ROOT)))
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


def audit(contract: dict, policy: dict) -> dict:
    stage_by_item = gated_outputs(contract)
    items = set(stage_by_item)
    declarations, removals = recipe_evidence(items)
    quest_rewards = quest_reward_sources(items)
    data_mentions = data_sources(items)

    reward_allowlist = set(policy.get("quest_reward_allowlist", []))
    loot_allowlist = set(policy.get("loot_allowlist", []))
    emc_blacklist = set(policy.get("emc_blacklist", []))
    simulation_blacklist = set(policy.get("resource_simulation_blacklist", []))
    trade_blacklist = set(policy.get("trade_blacklist", []))

    unauthorized_rewards = {
        item: paths for item, paths in quest_rewards.items() if item not in reward_allowlist
    }
    unauthorized_data = {
        item: paths for item, paths in data_mentions.items() if item not in loot_allowlist
    }
    no_recipe = sorted(item for item in items if item not in declarations)
    recipe_without_removal = sorted(
        item for item in items
        if item in declarations and not item.startswith("kubejs:") and item not in removals
    )

    late_items = {
        item
        for item, stage in stage_by_item.items()
        if next(s["index"] for s in contract["stages"] if s["id"] == stage) >= 9
    }
    emc_policy_gaps = sorted(late_items - emc_blacklist)

    simulation_sensitive = {
        item for item, stage in stage_by_item.items()
        if next(s["index"] for s in contract["stages"] if s["id"] == stage) >= 12
    }
    simulation_policy_gaps = sorted(simulation_sensitive - simulation_blacklist)

    trade_sensitive = {
        item for item, stage in stage_by_item.items()
        if next(s["index"] for s in contract["stages"] if s["id"] == stage) >= 10
        and not item.startswith("kubejs:")
    }
    documented_trade_controls = trade_sensitive & trade_blacklist

    return {
        "stage_by_item": stage_by_item,
        "declarations": declarations,
        "removals": removals,
        "quest_rewards": quest_rewards,
        "data_mentions": data_mentions,
        "unauthorized_rewards": unauthorized_rewards,
        "unauthorized_data": unauthorized_data,
        "no_recipe": no_recipe,
        "recipe_without_removal": recipe_without_removal,
        "emc_policy_gaps": emc_policy_gaps,
        "simulation_policy_gaps": simulation_policy_gaps,
        "documented_trade_controls": sorted(documented_trade_controls),
    }


def render(result: dict) -> str:
    blocking = (
        result["unauthorized_rewards"]
        or result["unauthorized_data"]
        or result["no_recipe"]
        or result["recipe_without_removal"]
        or result["emc_policy_gaps"]
        or result["simulation_policy_gaps"]
    )
    lines = [
        "# Bypass Audit Report",
        "",
        f"**{'IN PROGRESS' if blocking else 'PASS'}**",
        "",
        "This report tracks known static acquisition paths. A PASS means the source tree contains an explicit policy and authoritative recipe evidence; it does not claim that every third-party runtime mechanic has already been tested.",
        "",
        "## Summary",
        "",
        f"- Gated outputs: **{len(result['stage_by_item'])}**",
        f"- Outputs with recipe declarations: **{len(result['declarations'])}**",
        f"- Outputs with explicit recipe removal evidence: **{len(result['removals'])}**",
        f"- Unauthorized quest reward outputs: **{len(result['unauthorized_rewards'])}**",
        f"- Unallowlisted data/loot mentions: **{len(result['unauthorized_data'])}**",
        f"- Outputs without recipe declaration: **{len(result['no_recipe'])}**",
        f"- Non-KubeJS outputs without removal evidence: **{len(result['recipe_without_removal'])}**",
        f"- Late outputs missing EMC policy: **{len(result['emc_policy_gaps'])}**",
        f"- Stage 12+ outputs missing simulation policy: **{len(result['simulation_policy_gaps'])}**",
        "",
    ]

    sections = [
        ("Unauthorized quest rewards", result["unauthorized_rewards"]),
        ("Unallowlisted data or loot sources", result["unauthorized_data"]),
        ("Outputs without an authoritative recipe declaration", result["no_recipe"]),
        ("Non-KubeJS outputs without removal evidence", result["recipe_without_removal"]),
        ("EMC policy gaps", result["emc_policy_gaps"]),
        ("Resource simulation policy gaps", result["simulation_policy_gaps"]),
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

    lines.extend([
        "## Trade policy coverage",
        "",
        "The following non-KubeJS late outputs already have an explicit trade blacklist entry:",
        "",
    ])
    lines.extend(f"- `{item}`" for item in result["documented_trade_controls"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    result = audit(load_json(CONTRACT_PATH), load_json(POLICY_PATH))
    REPORT_PATH.write_text(render(result), encoding="utf-8", newline="\n")
    blocking = any([
        result["unauthorized_rewards"],
        result["unauthorized_data"],
        result["no_recipe"],
        result["recipe_without_removal"],
        result["emc_policy_gaps"],
        result["simulation_policy_gaps"],
    ])
    print(f"bypass_audit: {'IN PROGRESS' if blocking else 'PASS'}")
    print(f"gated_outputs: {len(result['stage_by_item'])}")
    print(f"unauthorized_rewards: {len(result['unauthorized_rewards'])}")
    print(f"missing_recipes: {len(result['no_recipe'])}")
    print(f"missing_removals: {len(result['recipe_without_removal'])}")
    return 1 if args.strict and blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
