from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KUBEJS = ROOT / "kubejs"
POLICY_PATH = ROOT / "config" / "expert_performance_policy.json"
REPORT_PATH = ROOT / "docs" / "KUBEJS_HOT_PATH_QUALITY_REPORT.md"

EVENT_RE = re.compile(
    r"\b(?P<owner>ServerEvents|StartupEvents|EntityEvents|LivingEntityEvents|PlayerEvents|BlockEvents|ItemEvents|LevelEvents)"
    r"\.(?P<event>[A-Za-z_][A-Za-z0-9_]*)\s*\("
)
FILE_IO_RE = re.compile(
    r"\b(?:JsonIO\.(?:read|write)|InventoryFiles\.(?:read|write|writeString)|Files\.(?:read|write|readString|writeString)|"
    r"createDirectories\s*\(|Paths\.get\s*\()"
)
REGISTRY_SCAN_RE = re.compile(
    r"(?:Object\.keys\s*\(\s*Platform\.mods\s*\)|Platform\.mods\s*\.\s*(?:forEach|values|entries)|"
    r"BuiltInRegistries\.[A-Z0-9_]+\s*\.\s*(?:forEach|stream|keySet|entrySet)\s*\()"
)
CONSOLE_RE = re.compile(r"\bconsole\.(?:log|info|warn|error)\s*\(")


def matching_delimiter(text: str, start: int, opening: str, closing: str) -> int:
    depth = 0
    quote: str | None = None
    escaped = False
    line_comment = False
    block_comment = False
    index = start
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if line_comment:
            if char == "\n":
                line_comment = False
            index += 1
            continue
        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 2
                continue
            index += 1
            continue
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            index += 1
            continue
        if char == "/" and next_char == "/":
            line_comment = True
            index += 2
            continue
        if char == "/" and next_char == "*":
            block_comment = True
            index += 2
            continue
        if char in ("'", '"', "`"):
            quote = char
            index += 1
            continue
        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return -1


def event_category(owner: str, event: str) -> str | None:
    normalized = event.lower()
    if "tick" in normalized:
        return "tick"
    if owner in {"EntityEvents", "LivingEntityEvents"} and normalized in {
        "spawned",
        "checkspawn",
        "check_spawn",
    }:
        return "spawn"
    if owner in {"EntityEvents", "LivingEntityEvents"} and "hurt" in normalized:
        return "hurt"
    return None


def main() -> int:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    budgets = policy["hot_path_budgets"]
    startup = policy["startup_io"]
    diagnostic_property = str(startup["diagnostic_mod_inventory_property"])

    failures: list[str] = []
    counts: Counter[str] = Counter()
    handler_rows: list[dict[str, str]] = []
    guarded_startup_writes = 0
    unguarded_startup_writes = 0

    for path in sorted(KUBEJS.rglob("*.js")):
        text = path.read_text(encoding="utf-8")
        relative = str(path.relative_to(ROOT))

        if "startup_scripts" in path.parts and FILE_IO_RE.search(text):
            guard_tokens = (
                f"System.getProperty('{diagnostic_property}'",
                f'System.getProperty("{diagnostic_property}"',
                f"getProperty('{diagnostic_property}'",
                f'getProperty("{diagnostic_property}"',
            )
            guarded = any(token in text for token in guard_tokens)
            if guarded:
                guarded_startup_writes += 1
            else:
                unguarded_startup_writes += 1
                if bool(startup["forbid_unguarded_startup_file_writes"]):
                    failures.append(f"{relative}: startup file I/O is not guarded by {diagnostic_property}")

        for match in EVENT_RE.finditer(text):
            owner = match.group("owner")
            event = match.group("event")
            category = event_category(owner, event)
            if category is None:
                continue
            counts[category] += 1

            open_paren = text.find("(", match.start())
            close_paren = matching_delimiter(text, open_paren, "(", ")")
            block = text[match.start() : close_paren + 1] if close_paren >= 0 else text[match.start() :]
            issues: list[str] = []
            if bool(budgets["forbid_file_io_in_high_frequency_handlers"]) and FILE_IO_RE.search(block):
                issues.append("file I/O")
            if bool(budgets["forbid_registry_full_scans_in_high_frequency_handlers"]) and REGISTRY_SCAN_RE.search(block):
                issues.append("full registry/mod scan")
            if bool(budgets["forbid_console_calls_in_high_frequency_handlers"]) and CONSOLE_RE.search(block):
                issues.append("console call")

            if issues:
                failures.append(
                    f"{relative}: {owner}.{event} contains " + ", ".join(issues)
                )
            handler_rows.append(
                {
                    "file": relative,
                    "handler": f"{owner}.{event}",
                    "category": category,
                    "status": "FAIL" if issues else "PASS",
                }
            )

    maximums = {
        "tick": int(budgets["maximum_tick_subscriptions"]),
        "spawn": int(budgets["maximum_spawn_subscriptions"]),
        "hurt": int(budgets["maximum_hurt_subscriptions"]),
    }
    for category, maximum in maximums.items():
        if counts[category] > maximum:
            failures.append(
                f"{category} subscriptions exceed budget: {counts[category]} > {maximum}"
            )

    combat_path = KUBEJS / "server_scripts" / "combat_scaling.js"
    combat = combat_path.read_text(encoding="utf-8") if combat_path.is_file() else ""
    identity_cache_ok = all(
        token in combat
        for token in (
            "java.util.IdentityHashMap",
            "var TYPE_PROFILE_CACHE",
            "profileForType(entity.getType())",
        )
    )
    if bool(policy["combat_scaling"]["require_entity_type_identity_cache"]) and not identity_cache_ok:
        failures.append("combat_scaling.js lacks the required EntityType identity cache")

    lines = [
        "# KubeJS Hot Path Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "This static gate scans frequent KubeJS handlers and startup scripts. It rejects synchronous file I/O, full registry scans and console output in tick/spawn/hurt paths, and requires diagnostic startup writes to be explicitly enabled.",
        "",
        "## Budgets",
        "",
        "| Category | Current | Maximum | Status |",
        "|---|---:|---:|---|",
    ]
    for category in ("tick", "spawn", "hurt"):
        lines.append(
            f"| {category} subscriptions | {counts[category]} | {maximums[category]} | "
            f"{'PASS' if counts[category] <= maximums[category] else 'FAIL'} |"
        )
    lines.extend(
        [
            f"| Guarded startup file writers | {guarded_startup_writes} | diagnostic only | PASS |",
            f"| Unguarded startup file writers | {unguarded_startup_writes} | 0 | {'PASS' if unguarded_startup_writes == 0 else 'FAIL'} |",
            f"| Combat EntityType identity cache | {'present' if identity_cache_ok else 'missing'} | required | {'PASS' if identity_cache_ok else 'FAIL'} |",
            "",
            "## High-frequency handlers",
            "",
            "| File | Handler | Category | Status |",
            "|---|---|---|---|",
        ]
    )
    for row in handler_rows:
        lines.append(
            f"| `{row['file']}` | `{row['handler']}` | {row['category']} | {row['status']} |"
        )
    lines.extend(
        [
            "",
            "## Aggregate",
            "",
            f"- High-frequency subscriptions: **{sum(counts.values())}**",
            f"- Guarded startup file writers: **{guarded_startup_writes}**",
            f"- Unguarded startup file writers: **{unguarded_startup_writes}**",
            f"- Failures: **{len(failures)}**",
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"kubejs_hot_path: {'PASS' if not failures else 'FAIL'}")
    print(f"tick_subscriptions: {counts['tick']}/{maximums['tick']}")
    print(f"spawn_subscriptions: {counts['spawn']}/{maximums['spawn']}")
    print(f"hurt_subscriptions: {counts['hurt']}/{maximums['hurt']}")
    print(f"guarded_startup_writes: {guarded_startup_writes}")
    print(f"unguarded_startup_writes: {unguarded_startup_writes}")
    print(f"failures: {len(failures)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
