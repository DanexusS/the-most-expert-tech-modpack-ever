from __future__ import annotations

import generate_early_stage_workflow_expansions as workflow
from advanced_stage_workflow_profiles import ADVANCED_STAGE_WORKFLOW_PROFILES
from mid_stage_workflow_profiles import MID_STAGE_WORKFLOW_PROFILES


def main() -> int:
    additions = {}
    for profiles in (MID_STAGE_WORKFLOW_PROFILES, ADVANCED_STAGE_WORKFLOW_PROFILES):
        overlap = (set(workflow.WORKFLOW_STAGES) | set(additions)) & set(profiles)
        if overlap:
            raise RuntimeError(
                "Duplicate workflow stage profiles: " + ", ".join(sorted(overlap))
            )
        additions.update(profiles)
    workflow.WORKFLOW_STAGES.update(additions)
    return workflow.main()


if __name__ == "__main__":
    raise SystemExit(main())
