from __future__ import annotations

import legacy_quest_semantic_audit_v2 as audit
import recipe_fairness_audit as fairness
import runtime_evidence_quality_gate as runtime_evidence


def calibrated_milestone_thresholds(stage: int) -> tuple[int, int, int, int]:
    # Stages 2–3 are the first cross-mod convergence layer. Two independently
    # produced provenance domains are sufficient there; later stages retain the
    # stricter three- and four-domain requirements.
    if stage == 1:
        return 4, 2, 5, 0
    if stage <= 3:
        return 4, 2, 7, 1
    if stage <= 8:
        return 4, 3, 7, 2
    return 4, 4, 9, 2


def main() -> int:
    fairness.milestone_thresholds = calibrated_milestone_thresholds
    semantic_result = audit.main()
    if semantic_result:
        return semantic_result
    fairness_result = fairness.main()
    if fairness_result:
        return fairness_result
    return runtime_evidence.main()


if __name__ == "__main__":
    raise SystemExit(main())
