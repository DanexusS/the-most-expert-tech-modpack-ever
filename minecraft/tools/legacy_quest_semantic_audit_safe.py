from __future__ import annotations

import legacy_quest_semantic_audit as audit
from snbt_field_parser import quest_spans


def main() -> int:
    audit.quest_spans = quest_spans
    return audit.main()


if __name__ == "__main__":
    raise SystemExit(main())
