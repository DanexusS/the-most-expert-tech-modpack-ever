from __future__ import annotations

import json
from pathlib import Path

from manual_generator_common import generate_manual_data

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "config" / "guide_sources"
SOURCES = [
    SOURCE_DIR / "manual3_draconic_evolution.json",
    SOURCE_DIR / "manual3_extended_crafting.json",
    SOURCE_DIR / "manual3_avaritia.json",
    SOURCE_DIR / "manual3_divinerpg.json",
    SOURCE_DIR / "manual3_actually_additions.json",
]


def main() -> int:
    modules = []
    for path in SOURCES:
        document = json.loads(path.read_text(encoding="utf-8"))
        if "slug" not in document or "lessons" not in document:
            raise RuntimeError(f"Invalid manual module source: {path}")
        modules.append(document)

    data = {
        "filename": "core_technology_manual_3",
        "title_en": "Core Technology Manual III",
        "title_ru": "Основной технический справочник III",
        "icon": "kubejs:cosmic_catalyst",
        "order_index": 6,
        "module_spacing": 8,
        "lesson_spacing": 2,
        "modules": modules,
    }
    quest_total, _ = generate_manual_data(ROOT, data)
    if quest_total != 50:
        raise RuntimeError(f"Core Technology Manual III expected 50 quests, found {quest_total}")
    print(f"Core Technology Manual III verified: {quest_total} quests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
