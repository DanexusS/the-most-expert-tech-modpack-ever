from __future__ import annotations

import late_stage_workflow_profiles_corrected  # noqa: F401
import performance_configuration_audit as audit
from snbt_field_parser import quest_spans


def main() -> int:
    audit.quest_spans = quest_spans
    return audit.main()


if __name__ == "__main__":
    raise SystemExit(main())
