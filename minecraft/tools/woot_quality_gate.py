from __future__ import annotations

import sys
from pathlib import Path

from simulation_catalog_quality_common import run_quality_gate
from upgrade_woot_catalog import CHAPTER_PATH, LANG_DIR

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "WOOT_QUALITY_REPORT.md"


def main() -> int:
    failures, quests = run_quality_gate(
        CHAPTER_PATH,
        LANG_DIR,
        REPORT_PATH,
        "Woot Catalogue Quality Report",
        "Woot",
        "woot",
        58,
    )
    print(f"woot_quality: {'PASS' if not failures else 'FAIL'}")
    print(f"quests: {quests}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
