from __future__ import annotations

# Importing the corrected late-stage profile layer mutates the generator profile
# registry before the performance audit counts optimization quests.
import late_stage_workflow_profiles_corrected  # noqa: F401
import kubejs_hot_path_quality_gate as hot_path
import performance_configuration_audit as configuration


def main() -> int:
    configuration_result = configuration.main()
    if configuration_result:
        return configuration_result
    return hot_path.main()


if __name__ == "__main__":
    raise SystemExit(main())
