from __future__ import annotations

import json
from pathlib import Path

from manual_generator_common import generate_manual_data

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "config" / "guide_sources"
SOURCES = [
    SOURCE_DIR / "manual5_productive_bees.json",
    SOURCE_DIR / "manual5_hostile_neural_networks.json",
    SOURCE_DIR / "manual5_woot.json",
    SOURCE_DIR / "manual5_mob_grinding_utils.json",
    SOURCE_DIR / "manual5_minecolonies.json",
]


def main() -> int:
    modules = []
    for path in SOURCES:
        document = json.loads(path.read_text(encoding="utf-8"))
        if "slug" not in document or "lessons" not in document:
            raise RuntimeError(f"Invalid manual module source: {path}")
        modules.append(document)

    data = {
        "filename": "core_technology_manual_5",
        "title_en": "Core Technology Manual V",
        "title_ru": "Основной технический справочник V",
        "icon": "kubejs:bioindustrial_matrix",
        "order_index": 8,
        "module_spacing": 8,
        "lesson_spacing": 2,
        "modules": modules,
    }
    quest_total, _ = generate_manual_data(ROOT, data)
    if quest_total != 50:
        raise RuntimeError(f"Core Technology Manual V expected 50 quests, found {quest_total}")
    print(f"Core Technology Manual V verified: {quest_total} quests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
