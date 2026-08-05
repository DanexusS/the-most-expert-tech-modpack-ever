from __future__ import annotations

import quest_quality_audit as audit
from snbt_field_parser import extract_array


def optional_array(text: str, marker: str) -> str:
    try:
        return extract_array(text, marker)[2]
    except RuntimeError:
        return ""


def main() -> int:
    audit.extract_array = optional_array
    return audit.main()


if __name__ == "__main__":
    raise SystemExit(main())
