from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "config" / "mod_guide_registry.json"

CORE_PROJECTS: dict[int, dict] = {
    223565: {
        "name": "Draconic Evolution",
        "mod_id": "draconicevolution",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 90,
        "chapter": "draconic_evolution",
        "guide_status": "draft",
        "notes": "Core late-game energy, equipment and awakened-material route."
    },
    223794: {
        "name": "Applied Energistics 2",
        "mod_id": "ae2",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 140,
        "chapter": "applied_energistics_2",
        "guide_status": "draft",
        "notes": "Core storage, channels, subnets and autocrafting route."
    },
    226410: {
        "name": "ProjectE",
        "mod_id": "projecte",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 70,
        "chapter": "projecte",
        "guide_status": "draft",
        "notes": "Contained transmutation; EMC access is a late progression permission."
    },
    228404: {
        "name": "Actually Additions",
        "mod_id": "actuallyadditions",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 80,
        "chapter": "actually_additions",
        "guide_status": "planned",
        "notes": "Early material analysis, reconstruction, power and utility engineering."
    },
    231951: {
        "name": "Immersive Engineering",
        "mod_id": "immersiveengineering",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 110,
        "chapter": "immersive_engineering",
        "guide_status": "draft",
        "notes": "Core metallurgy, structures, wiring and industrial process route."
    },
    246640: {
        "name": "Mystical Agriculture",
        "mod_id": "mysticalagriculture",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 100,
        "chapter": "mystical_ag",
        "guide_status": "draft",
        "notes": "Controlled renewable resource production; seeds must respect stage policy."
    },
    266515: {
        "name": "Industrial Foregoing",
        "mod_id": "industrialforegoing",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 100,
        "chapter": "industrial_foregoing",
        "guide_status": "draft",
        "notes": "Core bioindustry, fluids, machine frames and resource automation."
    },
    268387: {
        "name": "Extended Crafting",
        "mod_id": "extendedcrafting",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 60,
        "chapter": "extended_crafting",
        "guide_status": "draft",
        "notes": "Configured late-game tables, combination crafting and singularities."
    },
    268560: {
        "name": "Mekanism",
        "mod_id": "mekanism",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 140,
        "chapter": "mekanism_part_1",
        "guide_status": "draft",
        "notes": "Core gases, chemistry, ore multiplication, energy and antimatter."
    },
    281849: {
        "name": "PneumaticCraft: Repressurized",
        "mod_id": "pneumaticcraft",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 100,
        "chapter": "pneumaticcraft",
        "guide_status": "draft",
        "notes": "Core pressure, compressed materials, plastic and circuit production."
    },
    328085: {
        "name": "Create",
        "mod_id": "create",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 140,
        "chapter": "create",
        "guide_status": "draft",
        "notes": "Kinetic automation specialization after common electrical foundations."
    },
    363543: {
        "name": "DivineRPG",
        "mod_id": "divinerpg",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 140,
        "chapter": "divinerpg_codex",
        "guide_status": "draft",
        "notes": "Dimension progression and reusable boss permissions for technology gates."
    },
    405388: {
        "name": "Modern Industrialization",
        "mod_id": "modern_industrialization",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 140,
        "chapter": "Modern Industrialization",
        "guide_status": "draft",
        "notes": "Core steam-to-electric factory, circuits, machine tiers and throughput."
    },
    633483: {
        "name": "Powah!",
        "mod_id": "powah",
        "classification": "core_progression",
        "guide_tier": "core",
        "quest_target": 80,
        "chapter": "powah",
        "guide_status": "draft",
        "notes": "Core tiered generation, storage, transfer and resonant energy route."
    },
}


def main() -> int:
    document = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    projects = {int(entry["project_id"]): entry for entry in document.get("projects", [])}
    changed = 0
    missing: list[int] = []

    for project_id, values in CORE_PROJECTS.items():
        entry = projects.get(project_id)
        if entry is None:
            missing.append(project_id)
            continue
        for key, value in values.items():
            if entry.get(key) != value:
                entry[key] = value
                changed += 1

    document["projects"] = sorted(projects.values(), key=lambda entry: int(entry["project_id"]))
    rendered = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    previous = REGISTRY_PATH.read_text(encoding="utf-8")
    if rendered != previous:
        REGISTRY_PATH.write_text(rendered, encoding="utf-8", newline="\n")

    print(f"Core guide registry fields updated: {changed}")
    print(f"Core projects seeded: {len(CORE_PROJECTS) - len(missing)}/{len(CORE_PROJECTS)}")
    if missing:
        print("Core project IDs absent from manifest: " + ", ".join(map(str, missing)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
