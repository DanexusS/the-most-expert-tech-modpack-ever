from __future__ import annotations

from late_stage_workflow_profiles import LATE_STAGE_WORKFLOW_PROFILES

# Mutate the shared profile document before generators import it. This keeps
# workflow generation, depth generation, performance checks and quality gates
# on the same cycle-free targets.
LATE_STAGE_WORKFLOW_PROFILES["contained_transmutation"]["branches"][2][
    "target"
] = "extendedcrafting:ultimate_catalyst"
LATE_STAGE_WORKFLOW_PROFILES["extreme_fabrication"]["branches"][2][
    "target"
] = "avaritia:crystal_matrix_ingot"
