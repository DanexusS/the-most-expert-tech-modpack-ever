from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "kubejs" / "server_scripts" / "combat_scaling.js"

REPLACEMENTS = {
    "cataclysm: Object.freeze({ health: 6.0, damage: 1.85, armor: 10.0, knockback: 0.40 })":
        "cataclysm: Object.freeze({ health: 5.0, damage: 1.75, armor: 8.0, knockback: 0.35 })",
    "mowziesmobs: Object.freeze({ health: 5.0, damage: 1.75, armor: 8.0, knockback: 0.35 })":
        "mowziesmobs: Object.freeze({ health: 4.5, damage: 1.65, armor: 6.0, knockback: 0.30 })",
    "divinerpg: Object.freeze({ health: 5.0, damage: 1.80, armor: 8.0, knockback: 0.35 })":
        "divinerpg: Object.freeze({ health: 4.5, damage: 1.70, armor: 6.0, knockback: 0.30 })",
    "twilightforest: Object.freeze({ health: 5.0, damage: 1.70, armor: 8.0, knockback: 0.35 })":
        "twilightforest: Object.freeze({ health: 4.5, damage: 1.60, armor: 6.0, knockback: 0.30 })",
    "iceandfire: Object.freeze({ health: 5.5, damage: 1.85, armor: 9.0, knockback: 0.40 })":
        "iceandfire: Object.freeze({ health: 5.0, damage: 1.75, armor: 7.0, knockback: 0.35 })",
    "Multi-attribute expert combat profile v1.0.1 loaded.":
        "Multi-attribute expert combat profile v1.1.0 loaded."
}


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        if new in text:
            continue
        if old not in text:
            raise RuntimeError(f"Expected combat profile text not found: {old}")
        text = text.replace(old, new, 1)
        changed += 1

    if changed:
        PATH.write_text(text, encoding="utf-8", newline="\n")
        print(f"Combat profile replacements applied: {changed}")
    else:
        print("Combat profiles already match theoretical targets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
