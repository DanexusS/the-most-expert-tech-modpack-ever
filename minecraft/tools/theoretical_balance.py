from __future__ import annotations

import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "config" / "expert_balance_model.json"
COMBAT_PATH = ROOT / "kubejs" / "server_scripts" / "combat_scaling.js"
REPORT_PATH = ROOT / "docs" / "THEORETICAL_BALANCE_REPORT.md"
RECIPE_PATHS = (
    ROOT / "kubejs" / "server_scripts" / "expert_recipes.js",
    ROOT / "kubejs" / "server_scripts" / "expert_recipe_extensions.js",
)

PROFILE_VALUE_RE = re.compile(r"(health|damage|armor|knockback)\s*:\s*([0-9]+(?:\.[0-9]+)?)")
RECIPE_RE = re.compile(
    r"\{\s*id:\s*['\"]([^'\"]+)['\"]"
    r".*?output:\s*['\"]([^'\"]+)['\"]"
    r".*?pattern:\s*\[([^\]]+)\]"
    r".*?key:\s*\{(.*?)\}\s*\}",
    re.S,
)
STRING_RE = re.compile(r"['\"]([^'\"]+)['\"]")
ITEM_RE = re.compile(r":\s*['\"]([a-z0-9_.-]+:[a-z0-9_./-]+)['\"]")


@dataclass(frozen=True)
class Profile:
    health: float
    damage: float
    armor: float
    knockback: float


@dataclass(frozen=True)
class RecipeMetric:
    recipe_id: str
    output: str
    occupied_slots: int
    namespaces: int
    kubejs_dependencies: int
    complexity: float


def parse_profile(body: str) -> Profile:
    values = {name: float(value) for name, value in PROFILE_VALUE_RE.findall(body)}
    missing = {"health", "damage", "armor", "knockback"} - set(values)
    if missing:
        raise RuntimeError(f"Incomplete combat profile; missing {sorted(missing)}")
    return Profile(**values)


def extract_object(text: str, variable: str) -> str:
    marker = f"var {variable} = Object.freeze({{"
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f"Combat profile object not found: {variable}")
    content_start = start + len(marker)
    depth = 1
    index = content_start
    in_string = False
    quote = ""
    escaped = False
    while index < len(text):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                in_string = False
        elif char in "'\"":
            in_string = True
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[content_start:index]
        index += 1
    raise RuntimeError(f"Unclosed combat profile object: {variable}")


def parse_combat_profiles() -> tuple[dict[str, Profile], dict[str, Profile], dict[str, Profile]]:
    text = COMBAT_PATH.read_text(encoding="utf-8")
    defaults = {
        "hostile": parse_profile(extract_object(text, "DEFAULT_HOSTILE_PROFILE")),
        "boss": parse_profile(extract_object(text, "DEFAULT_BOSS_PROFILE")),
    }

    def parse_namespace_map(variable: str) -> dict[str, Profile]:
        body = extract_object(text, variable)
        result: dict[str, Profile] = {}
        for match in re.finditer(r"([a-z0-9_]+)\s*:\s*Object\.freeze\(\{(.*?)\}\)", body, re.S):
            result[match.group(1)] = parse_profile(match.group(2))
        if not result:
            raise RuntimeError(f"No namespace profiles parsed from {variable}")
        return result

    return defaults, parse_namespace_map("NAMESPACE_PROFILES"), parse_namespace_map("BOSS_NAMESPACE_PROFILES")


def resolve_profile(spec: dict[str, str], defaults: dict[str, Profile], regular: dict[str, Profile], bosses: dict[str, Profile]) -> Profile:
    if spec["scope"] == "default":
        return defaults[spec["kind"]]
    namespace = spec["namespace"]
    table = bosses if spec["kind"] == "boss" else regular
    if namespace not in table:
        raise RuntimeError(f"Missing modeled namespace profile: {spec}")
    return table[namespace]


def damage_after_armor(raw_damage: float, armor: float, toughness: float) -> float:
    # Deliberately documented approximation of the modern Java armor curve.
    divisor = 2.0 + toughness / 4.0
    effective_armor = min(20.0, max(armor / 5.0, armor - raw_damage / divisor))
    return max(0.001, raw_damage * (1.0 - effective_armor / 25.0))


def hits_to_kill(health: float, damage: float) -> int:
    return max(1, math.ceil(health / max(0.001, damage)))


def parse_recipes(model: dict) -> list[RecipeMetric]:
    namespace_weight = float(model["recipe_complexity"]["namespace_weight"])
    kubejs_weight = float(model["recipe_complexity"]["kubejs_dependency_weight"])
    metrics: list[RecipeMetric] = []

    for path in RECIPE_PATHS:
        text = path.read_text(encoding="utf-8")
        for recipe_id, output, pattern_body, key_body in RECIPE_RE.findall(text):
            rows = STRING_RE.findall(pattern_body)
            ingredients = ITEM_RE.findall(key_body)
            occupied_slots = sum(1 for row in rows for char in row if char != " ")
            namespaces = {item.split(":", 1)[0] for item in ingredients}
            kubejs_dependencies = len({item for item in ingredients if item.startswith("kubejs:")})
            complexity = (
                occupied_slots
                + namespace_weight * max(0, len(namespaces) - 1)
                + kubejs_weight * kubejs_dependencies
            )
            metrics.append(
                RecipeMetric(
                    recipe_id=recipe_id,
                    output=output,
                    occupied_slots=occupied_slots,
                    namespaces=len(namespaces),
                    kubejs_dependencies=kubejs_dependencies,
                    complexity=complexity,
                )
            )
    return sorted(metrics, key=lambda metric: metric.recipe_id)


def gate_result(value: float, gate: dict) -> tuple[bool, str]:
    minimum = float(gate["min"])
    maximum = float(gate["max"])
    passed = minimum <= value <= maximum
    return passed, f"{minimum:g}–{maximum:g}"


def render_report(model: dict, combat_rows: list[dict], recipe_rows: list[RecipeMetric], failures: list[str]) -> str:
    lines = [
        "# Theoretical Balance Report",
        "",
        "Generated by `tools/theoretical_balance.py`. Values are deterministic static estimates and must be replaced by measured runtime data before release approval.",
        "",
        "## Assumptions",
        "",
    ]
    lines.extend(f"- {note}" for note in model["notes"])
    lines.extend(
        [
            "",
            "## Combat gates",
            "",
            "| Archetype | Scaled HP | Total armor | Selected weapon result | Target | Selected defense result | Target | Status |",
            "|---|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for row in combat_rows:
        lines.append(
            "| {label} | {health:.1f} | {armor:.1f} | {weapon_value:.1f} {weapon_unit} | {weapon_target} | "
            "{defense_value:.1f} hits | {defense_target} | {status} |".format(**row)
        )

    lines.extend(
        [
            "",
            "## Recipe complexity",
            "",
            "Complexity = occupied crafting slots + namespace breadth weight + KubeJS milestone dependency weight.",
            "",
            "| Recipe | Output | Slots | Namespaces | KubeJS gates | Complexity |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for metric in recipe_rows:
        lines.append(
            f"| `{metric.recipe_id}` | `{metric.output}` | {metric.occupied_slots} | {metric.namespaces} | "
            f"{metric.kubejs_dependencies} | {metric.complexity:.1f} |"
        )

    lines.extend(["", "## Result", ""])
    if failures:
        lines.append("**FAIL**")
        lines.extend(f"- {failure}" for failure in failures)
    else:
        lines.append("**PASS** — every configured theoretical gate is inside its declared range.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    defaults, regular, bosses = parse_combat_profiles()
    weapons = {entry["id"]: entry for entry in model["weapon_tiers"]}
    players = {entry["id"]: entry for entry in model["player_tiers"]}
    failures: list[str] = []
    combat_rows: list[dict] = []

    for archetype in model["combat_archetypes"]:
        profile = resolve_profile(archetype["profile"], defaults, regular, bosses)
        scaled_health = float(archetype["base_health"]) * profile.health
        total_armor = float(archetype["base_armor"]) + profile.armor

        weapon_gate = archetype["weapon_gate"]
        weapon = weapons[weapon_gate["tier"]]
        dealt = damage_after_armor(float(weapon["damage"]), total_armor, 0.0)
        hits = hits_to_kill(scaled_health, dealt)
        ttk = max(0.0, (hits - 1) / float(weapon["attacks_per_second"]))
        weapon_value = float(hits) if weapon_gate["metric"] == "hits" else ttk
        weapon_unit = "hits" if weapon_gate["metric"] == "hits" else "seconds"
        weapon_ok, weapon_target = gate_result(weapon_value, weapon_gate)

        defense_gate = archetype["defense_gate"]
        player = players[defense_gate["tier"]]
        incoming_raw = float(archetype["base_attack"]) * profile.damage
        incoming = damage_after_armor(incoming_raw, float(player["armor"]), float(player["toughness"]))
        survival_hits = hits_to_kill(float(player["health"]), incoming)
        defense_ok, defense_target = gate_result(float(survival_hits), defense_gate)

        if not weapon_ok:
            failures.append(
                f"{archetype['id']}: {weapon_gate['metric']}={weapon_value:.2f}, expected {weapon_target}"
            )
        if not defense_ok:
            failures.append(
                f"{archetype['id']}: survival_hits={survival_hits}, expected {defense_target}"
            )

        combat_rows.append(
            {
                "label": archetype["label"],
                "health": scaled_health,
                "armor": total_armor,
                "weapon_value": weapon_value,
                "weapon_unit": weapon_unit,
                "weapon_target": weapon_target,
                "defense_value": float(survival_hits),
                "defense_target": defense_target,
                "status": "PASS" if weapon_ok and defense_ok else "FAIL",
            }
        )

    recipe_rows = parse_recipes(model)
    complexity_model = model["recipe_complexity"]
    minimum = float(complexity_model["target_minimum_for_extensions"])
    maximum = float(complexity_model["target_maximum_for_extensions"])
    extension_rows = [row for row in recipe_rows if row.recipe_id.startswith("kubejs:expert_extension/")]
    if not extension_rows:
        failures.append("No expert extension recipes were parsed")
    for row in extension_rows:
        if not minimum <= row.complexity <= maximum:
            failures.append(
                f"{row.recipe_id}: recipe complexity {row.complexity:.1f}, expected {minimum:g}–{maximum:g}"
            )

    report = render_report(model, combat_rows, recipe_rows, failures)
    REPORT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(f"Theoretical balance report: {'FAIL' if failures else 'PASS'}")
    print(f"combat_archetypes: {len(combat_rows)}")
    print(f"modeled_recipes: {len(recipe_rows)}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
