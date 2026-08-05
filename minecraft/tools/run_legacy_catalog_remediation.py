from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "config" / "legacy_catalog_remediation_manifest.json"
RUNNER_PATH = ROOT / "tools" / "catalog_upgrade_multinamespace.py"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("upgrade", "gate"))
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    policies = manifest.get("policies", [])
    if not policies:
        raise RuntimeError("Legacy remediation manifest has no policies")

    for policy in policies:
        subprocess.run(
            [sys.executable, str(RUNNER_PATH), args.mode, policy],
            cwd=ROOT,
            check=True,
        )
    print(f"legacy_remediation_mode: {args.mode}")
    print(f"legacy_remediation_policies: {len(policies)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
