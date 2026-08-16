from __future__ import annotations

# Importing the corrected late-stage profile layer mutates the generator profile
# registry before the performance audit counts optimization quests.
import late_stage_workflow_profiles_corrected  # noqa: F401
import kubejs_hot_path_quality_gate as hot_path
import performance_configuration_audit as configuration
import runtime_performance_quality_gate as runtime_gate


def main() -> int:
    result = configuration.main()
    if result:
        return result
    result = hot_path.main()
    if result:
        return result
    return runtime_gate.main()


if __name__ == "__main__":
    raise SystemExit(main())
