from __future__ import annotations

import json
from pathlib import Path

from manual_generator_common import generate_manual_data

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "config" / "guide_sources"
SOURCES = [
    SOURCE_DIR / "manual7_mowzies_mobs.json",
    SOURCE_DIR / "manual7_mutant_monsters.json",
    SOURCE_DIR / "manual7_earth_mobs.json",
    SOURCE_DIR / "manual7_born_in_chaos.json",
    SOURCE_DIR / "manual7_simply_swords.json",
]


def main() -> int:
    modules = []
    for path in SOURCES:
        document = json.loads(path.read_text(encoding="utf-8"))
        if "slug" not in document or "lessons" not in document:
            raise RuntimeError(f"Invalid manual module source: {path}")
        if len(document["lessons"]) != 10:
            raise RuntimeError(
                f"Manual VII module {document.get('slug', path.name)} expected 10 lessons, "
                f"found {len(document['lessons'])}"
            )
        modules.append(document)

    data = {
        "filename": "core_technology_manual_7",
        "title_en": "Core Technology Manual VII",
        "title_ru": "Основной технический справочник VII",
        "icon": "minecraft:netherite_sword",
        "order_index": 10,
        "module_spacing": 8,
        "lesson_spacing": 2,
        "modules": modules,
    }
    quest_total, _ = generate_manual_data(ROOT, data)
    if quest_total != 50:
        raise RuntimeError(f"Core Technology Manual VII expected 50 quests, found {quest_total}")
    print(f"Core Technology Manual VII verified: {quest_total} quests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
