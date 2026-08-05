from __future__ import annotations

from copy import deepcopy

from late_stage_workflow_profiles import LATE_STAGE_WORKFLOW_PROFILES as _BASE

LATE_STAGE_WORKFLOW_PROFILES = deepcopy(_BASE)
LATE_STAGE_WORKFLOW_PROFILES["contained_transmutation"]["branches"][2][
    "target"
] = "extendedcrafting:ultimate_catalyst"
LATE_STAGE_WORKFLOW_PROFILES["extreme_fabrication"]["branches"][2][
    "target"
] = "avaritia:crystal_matrix_ingot"
