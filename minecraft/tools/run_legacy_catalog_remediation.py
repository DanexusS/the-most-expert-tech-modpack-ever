from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "config" / "legacy_catalog_remediation_manifest.json"
POLICY_RUNNER_PATH = ROOT / "tools" / "catalog_upgrade_multinamespace.py"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("upgrade", "gate"))
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    policies = manifest.get("policies", [])
    tools = manifest.get("tools", [])
    if not policies and not tools:
        raise RuntimeError("Legacy remediation manifest has no policies or tools")

    for policy in policies:
        subprocess.run(
            [sys.executable, str(POLICY_RUNNER_PATH), args.mode, policy],
            cwd=ROOT,
            check=True,
        )
    for tool in tools:
        tool_path = Path(tool)
        if not tool_path.is_absolute():
            tool_path = ROOT / tool_path
        subprocess.run(
            [sys.executable, str(tool_path), args.mode],
            cwd=ROOT,
            check=True,
        )

    print(f"legacy_remediation_mode: {args.mode}")
    print(f"legacy_remediation_policies: {len(policies)}")
    print(f"legacy_remediation_tools: {len(tools)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
