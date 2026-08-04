from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
MAP_PATH = ROOT / "docs" / "PROGRESSION_MAP.md"


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    stages = {stage["id"]: stage for stage in contract["stages"]}
    electrical = stages["regulated_electricity"]
    kinetic = stages["kinetic_automation"]

    changed = False
    if electrical["index"] != 3:
        electrical["index"] = 3
        changed = True
    if kinetic["index"] != 4:
        kinetic["index"] = 4
        changed = True

    contract["stages"].sort(key=lambda stage: stage["index"])
    rendered = json.dumps(contract, ensure_ascii=False, indent=2) + "\n"
    previous = CONTRACT_PATH.read_text(encoding="utf-8")
    if rendered != previous:
        CONTRACT_PATH.write_text(rendered, encoding="utf-8", newline="\n")
        changed = True

    map_text = MAP_PATH.read_text(encoding="utf-8")
    old_rows = (
        "| 3 | Кинетическая автоматизация | Кинетический интерфейс | Create, нагрузка, передача вращения, линии обработки и последовательная сборка |\n"
        "| 4 | Регулируемая электротехника | Механическое ядро | Генерация, напряжение, буферы, защита и распределение энергии |"
    )
    new_rows = (
        "| 3 | Регулируемая электротехника | Механическое ядро | Генерация, напряжение, буферы, защита и распределение энергии |\n"
        "| 4 | Кинетическая автоматизация | Кинетический интерфейс | Create, нагрузка, передача вращения, линии обработки и последовательная сборка |"
    )
    if old_rows in map_text:
        MAP_PATH.write_text(map_text.replace(old_rows, new_rows), encoding="utf-8", newline="\n")
        changed = True

    print("Progression contract normalized" if changed else "Progression contract already normalized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
