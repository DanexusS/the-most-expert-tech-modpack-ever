from __future__ import annotations

import quest_quality_audit as audit
from snbt_field_parser import extract_array


def main() -> int:
    audit.extract_array = lambda text, marker: extract_array(text, marker)[2]
    return audit.main()


if __name__ == "__main__":
    raise SystemExit(main())
