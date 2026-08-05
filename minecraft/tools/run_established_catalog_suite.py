from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "catalog_upgrade_batch.py"
POLICIES = [
    "config/catalog_policies/storage_systems_full.json",
    "config/catalog_policies/mekanism_part_1_full.json",
    "config/catalog_policies/amateur_archaeologist_full.json",
    "config/catalog_policies/ice_and_fire_full.json",
    "config/catalog_policies/ae2_full.json",
    "config/catalog_policies/draconic_evolution_full.json",
    "config/catalog_policies/ars_nouveau_full.json",
    "config/catalog_policies/extended_crafting_full.json",
    "config/catalog_policies/pneumaticcraft_full.json",
    "config/catalog_policies/avaritia_full.json",
    "config/catalog_policies/rftools_full.json",
    "config/catalog_policies/cataclysm_full.json",
    "config/catalog_policies/mob_grinding_utils_full.json",
    "config/catalog_policies/occultism_full.json",
    "config/catalog_policies/ender_io_full.json",
    "config/catalog_policies/modern_industrialization_full.json",
    "config/catalog_policies/create_full.json",
    "config/catalog_policies/mekanism_part_2_full.json",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("upgrade", "gate"))
    args = parser.parse_args()

    for policy in POLICIES:
        subprocess.run(
            [sys.executable, str(RUNNER), args.mode, policy],
            cwd=ROOT,
            check=True,
        )

    print(f"established_catalog_mode: {args.mode}")
    print(f"established_catalog_policies: {len(POLICIES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
