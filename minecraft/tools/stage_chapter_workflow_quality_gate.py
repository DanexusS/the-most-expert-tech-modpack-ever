from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import generate_early_stage_workflow_expansions as workflow
import generate_stage_depth_program as depth
import stage_chapter_organization_quality_gate as organization
from advanced_stage_workflow_profiles import ADVANCED_STAGE_WORKFLOW_PROFILES
from late_stage_workflow_profiles_corrected import LATE_STAGE_WORKFLOW_PROFILES
from mid_stage_workflow_profiles import MID_STAGE_WORKFLOW_PROFILES

ROOT = Path(__file__).resolve().parents[1]
REMEDIATION_RUNNER = ROOT / "tools" / "run_legacy_catalog_remediation.py"


def main() -> int:
    subprocess.run(
        [sys.executable, str(REMEDIATION_RUNNER), "gate"],
        cwd=ROOT,
        check=True,
    )

    for profiles in (
        MID_STAGE_WORKFLOW_PROFILES,
        ADVANCED_STAGE_WORKFLOW_PROFILES,
        LATE_STAGE_WORKFLOW_PROFILES,
    ):
        for stage_id, profile in profiles.items():
            existing = workflow.WORKFLOW_STAGES.get(stage_id)
            if existing is not None and existing != profile:
                raise RuntimeError(f"Conflicting workflow stage profile: {stage_id}")
            workflow.WORKFLOW_STAGES[stage_id] = profile

    # organization.main() calls depth.merged_workflow_profiles(). At this point
    # the shared workflow registry is already complete, so reuse it instead of
    # treating the second merge as a duplicate-profile error.
    depth.merged_workflow_profiles = lambda: dict(workflow.WORKFLOW_STAGES)
    return organization.main()


if __name__ == "__main__":
    raise SystemExit(main())
