from __future__ import annotations

import generate_early_stage_workflow_expansions as workflow
from mid_stage_workflow_profiles import MID_STAGE_WORKFLOW_PROFILES


def main() -> int:
    overlap = set(workflow.WORKFLOW_STAGES) & set(MID_STAGE_WORKFLOW_PROFILES)
    if overlap:
        raise RuntimeError(
            "Duplicate workflow stage profiles: " + ", ".join(sorted(overlap))
        )
    workflow.WORKFLOW_STAGES.update(MID_STAGE_WORKFLOW_PROFILES)
    return workflow.main()


if __name__ == "__main__":
    raise SystemExit(main())
