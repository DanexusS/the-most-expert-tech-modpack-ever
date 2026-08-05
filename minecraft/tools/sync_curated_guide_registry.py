from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "config" / "mod_guide_registry.json"
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"

# The core projects below are covered by a reviewed conceptual manual in
# addition to their legacy item/reference chapter. This mapping is intentionally
# limited to meaningful gameplay/progression projects; it is not a 501-project
# manifest classification exercise.
CURATED_GUIDES: dict[int, str] = {
    223565: "core_technology_manual_3",  # Draconic Evolution
    223794: "core_technology_manual_1",  # Applied Energistics 2
    226410: "core_technology_manual_2",  # ProjectE
    228404: "core_technology_manual_3",  # Actually Additions
    231951: "core_technology_manual_1",  # Immersive Engineering
    246640: "core_technology_manual_2",  # Mystical Agriculture
    266515: "core_technology_manual_2",  # Industrial Foregoing
    268387: "core_technology_manual_3",  # Extended Crafting
    268560: "core_technology_manual_1",  # Mekanism
    281849: "core_technology_manual_2",  # PneumaticCraft
    328085: "core_technology_manual_1",  # Create
    363543: "core_technology_manual_3",  # DivineRPG
    405388: "core_technology_manual_1",  # Modern Industrialization
    633483: "core_technology_manual_2",  # Powah
}


def main() -> int:
    document = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    projects = {int(entry["project_id"]): entry for entry in document.get("projects", [])}
    changed = 0
    reviewed = 0
    missing: list[str] = []

    for project_id, chapter in CURATED_GUIDES.items():
        entry = projects.get(project_id)
        chapter_path = CHAPTER_DIR / f"{chapter}.snbt"
        if entry is None:
            missing.append(f"project {project_id}")
            continue
        if not chapter_path.is_file():
            missing.append(chapter)
            if entry.get("guide_status") == "reviewed":
                entry["guide_status"] = "draft"
                changed += 1
            continue

        reviewed += 1
        desired = {
            "chapter": chapter,
            "guide_status": "reviewed",
            "review_basis": "Curated bilingual manual generated from reviewed source modules; legacy item chapter remains supplementary.",
        }
        for key, value in desired.items():
            if entry.get(key) != value:
                entry[key] = value
                changed += 1

    document["projects"] = sorted(projects.values(), key=lambda entry: int(entry["project_id"]))
    rendered = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    if rendered != REGISTRY_PATH.read_text(encoding="utf-8"):
        REGISTRY_PATH.write_text(rendered, encoding="utf-8", newline="\n")

    print(f"curated_guides_reviewed: {reviewed}/{len(CURATED_GUIDES)}")
    print(f"registry_fields_changed: {changed}")
    if missing:
        print("missing_curated_guides: " + ", ".join(missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
