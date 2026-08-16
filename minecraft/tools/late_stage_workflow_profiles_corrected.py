from __future__ import annotations

import catalog_upgrade_common
from late_stage_workflow_profiles import LATE_STAGE_WORKFLOW_PROFILES
from snbt_field_parser import quest_spans

# Mutate the shared profile document before generators import it. This keeps
# workflow generation, depth generation, performance checks and quality gates
# on the same cycle-free targets.
LATE_STAGE_WORKFLOW_PROFILES["contained_transmutation"]["branches"][2][
    "target"
] = "extendedcrafting:ultimate_catalyst"
LATE_STAGE_WORKFLOW_PROFILES["extreme_fabrication"]["branches"][2][
    "target"
] = "avaritia:crystal_matrix_ingot"

# Some legacy chapters contain strings such as "ftbquests:icon" before the
# actual quests field. Share the line-anchored parser with every tool imported
# after this correction module, including performance and depth audits.
catalog_upgrade_common.quest_spans = quest_spans
