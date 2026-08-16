from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "expert_bypass_policy.json"
EMC_PATH = ROOT / "config" / "ProjectE" / "custom_emc.json"


def main() -> int:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    blacklist = set(policy.get("emc_blacklist", []))
    document = json.loads(EMC_PATH.read_text(encoding="utf-8"))
    entries = document.setdefault("entries", [])

    # Only plain item entries are controlled here. Variant entries with a data
    # component remain separate and are audited independently.
    plain_by_id = {
        entry.get("id"): entry
        for entry in entries
        if isinstance(entry, dict) and "data" not in entry and entry.get("id")
    }

    changed = 0
    for item_id in sorted(blacklist):
        entry = plain_by_id.get(item_id)
        if entry is None:
            entry = {"id": item_id, "emc": 0}
            entries.append(entry)
            plain_by_id[item_id] = entry
            changed += 1
        elif entry.get("emc") != 0:
            entry["emc"] = 0
            changed += 1

    entries.sort(key=lambda entry: (str(entry.get("id", "")), json.dumps(entry.get("data", {}), sort_keys=True)))
    rendered = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    previous = EMC_PATH.read_text(encoding="utf-8")
    if rendered != previous:
        EMC_PATH.write_text(rendered, encoding="utf-8", newline="\n")

    print(f"ProjectE EMC blacklist entries synchronized: {len(blacklist)}")
    print(f"ProjectE EMC entries changed: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
