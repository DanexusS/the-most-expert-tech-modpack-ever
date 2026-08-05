from __future__ import annotations

import legacy_quest_semantic_audit as audit
import recipe_fairness_audit as fairness
from snbt_field_parser import quest_spans


def main() -> int:
    audit.quest_spans = quest_spans
    semantic_result = audit.main()
    if semantic_result:
        return semantic_result
    return fairness.main()


if __name__ == "__main__":
    raise SystemExit(main())
