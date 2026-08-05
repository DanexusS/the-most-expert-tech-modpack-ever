from __future__ import annotations

import performance_configuration_audit as audit
from advanced_stage_workflow_profiles import ADVANCED_STAGE_WORKFLOW_PROFILES


def main() -> int:
    overlap = set(audit.workflow.WORKFLOW_STAGES) & set(
        ADVANCED_STAGE_WORKFLOW_PROFILES
    )
    if overlap:
        raise RuntimeError(
            "Duplicate workflow stage profiles: " + ", ".join(sorted(overlap))
        )
    audit.workflow.WORKFLOW_STAGES.update(ADVANCED_STAGE_WORKFLOW_PROFILES)
    return audit.main()


if __name__ == "__main__":
    raise SystemExit(main())
