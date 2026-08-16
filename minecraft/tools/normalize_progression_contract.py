from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
MAP_PATH = ROOT / "docs" / "PROGRESSION_MAP.md"

SEAL_STAGE = {
    "kubejs:divine_seal": "precision_manufacturing",
    "kubejs:eden_seal": "process_chemistry",
    "kubejs:wildwood_seal": "industrial_scale",
    "kubejs:apalachia_seal": "controlled_resources",
    "kubejs:skythern_seal": "applied_logistics",
    "kubejs:mortum_seal": "resonant_energy",
    "kubejs:vethea_seal": "draconic_engineering",
    "kubejs:wreck_seal": "contained_transmutation",
    "kubejs:lunar_seal": "extreme_fabrication",
}


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

    all_seals = set(SEAL_STAGE)
    for stage in contract["stages"]:
        original = list(stage.get("gated_outputs", []))
        stage["gated_outputs"] = [item for item in original if item not in all_seals]
        if stage["gated_outputs"] != original:
            changed = True

    for seal, stage_id in SEAL_STAGE.items():
        outputs = stages[stage_id].setdefault("gated_outputs", [])
        if seal not in outputs:
            outputs.append(seal)
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
        map_text = map_text.replace(old_rows, new_rows)
        changed = True

    seal_note = (
        "- Печати измерений распределяются по этапам их первого технологического применения: "
        "Divine — этап 5, Eden — 7, Wildwood — 8, Apalachia — 9, Skythern — 10, "
        "Mortum — 11, Vethea — 14, Wreck — 15, Lady Luna — 16.\n"
    )
    if seal_note not in map_text:
        marker = "## Правила переходов\n\n"
        if marker in map_text:
            map_text = map_text.replace(marker, marker + seal_note)
            changed = True

    MAP_PATH.write_text(map_text, encoding="utf-8", newline="\n")
    print("Progression contract normalized" if changed else "Progression contract already normalized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
