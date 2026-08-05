from __future__ import annotations

import argparse
import sys
from pathlib import Path

import catalog_upgrade_common as common


def select_category(policy: dict, item_id: str | None) -> dict:
    if item_id is None:
        return policy["checkpoint"]
    namespace, path = item_id.split(":", 1)
    namespaces = set(policy.get("primary_namespaces", [policy["primary_namespace"]]))
    prefixes = tuple(policy.get("primary_namespace_prefixes", []))
    is_primary = namespace in namespaces or any(namespace.startswith(prefix) for prefix in prefixes)
    if not is_primary:
        return policy["cross_mod"]
    for category in policy["categories"]:
        if any(token in path for token in category["tokens"]):
            return category
    return policy["default"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("upgrade", "gate"))
    parser.add_argument("policy", type=Path)
    args = parser.parse_args()
    policy_path = args.policy if args.policy.is_absolute() else common.ROOT / args.policy
    policy = common.load_policy(policy_path)
    common.select_category = select_category
    if args.mode == "upgrade":
        common.upgrade(policy)
        return 0
    return common.gate(policy)


if __name__ == "__main__":
    sys.exit(main())
