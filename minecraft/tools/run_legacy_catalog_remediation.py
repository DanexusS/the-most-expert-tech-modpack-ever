from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from legacy_catalog_policy_suite import gate_policies, upgrade_policies

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "config" / "legacy_catalog_remediation_manifest.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("upgrade", "gate"))
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    policies = manifest.get("policies", [])
    tools = manifest.get("tools", [])
    if not policies and not tools:
        raise RuntimeError("Legacy remediation manifest has no policies or tools")

    result = (
        upgrade_policies(policies)
        if args.mode == "upgrade"
        else gate_policies(policies)
    )

    for tool in tools:
        tool_path = Path(tool)
        if not tool_path.is_absolute():
            tool_path = ROOT / tool_path
        completed = subprocess.run(
            [sys.executable, str(tool_path), args.mode],
            cwd=ROOT,
            check=False,
        )
        result = max(result, completed.returncode)

    print(f"legacy_remediation_mode: {args.mode}")
    print(f"legacy_remediation_policies: {len(policies)}")
    print(f"legacy_remediation_tools: {len(tools)}")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
