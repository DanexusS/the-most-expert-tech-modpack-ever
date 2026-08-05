from __future__ import annotations

import sys
from pathlib import Path

from simulation_catalog_quality_common import run_quality_gate
from upgrade_hostile_neural_networks_catalog import CHAPTER_PATH, LANG_DIR

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "HOSTILE_NEURAL_NETWORKS_QUALITY_REPORT.md"


def main() -> int:
    failures, quests = run_quality_gate(
        CHAPTER_PATH,
        LANG_DIR,
        REPORT_PATH,
        "Hostile Neural Networks Catalogue Quality Report",
        "Hostile Neural Networks",
        "hostile_neural_networks",
        51,
    )
    print(f"hostile_neural_networks_quality: {'PASS' if not failures else 'FAIL'}")
    print(f"quests: {quests}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
