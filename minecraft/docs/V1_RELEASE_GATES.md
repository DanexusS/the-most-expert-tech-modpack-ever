# v1 Release Gates

The branch may be called **v1** only when every mandatory gate below has evidence. A green static CI run is necessary but not sufficient.

## 1. Static structure — mandatory

- JavaScript syntax: PASS.
- KubeJS JSON syntax: PASS.
- FTB Quests SNBT balance: PASS.
- Duplicate FTB object IDs: 0.
- Missing quest dependency targets: 0.
- Duplicate explicit KubeJS recipe IDs: 0.
- Tracked runtime artifacts: 0.
- Generated localization and audit files are reproducible and leave a clean working tree.

## 2. Theoretical balance — mandatory before runtime testing

- Every configured combat archetype is inside its declared hit-count, TTK and survival range.
- Strategic extension recipes remain inside the declared relative-complexity range.
- Model assumptions are stored in `config/expert_balance_model.json`.
- The generated `THEORETICAL_BALANCE_REPORT.md` contains PASS.
- A theoretical PASS does not override measured gameplay. Runtime measurements replace assumptions when they disagree.

## 3. Quest quality — mandatory for the critical path

- `expert_progression` and `engineering_foundations_guide` pass the core quality audit.
- Every mandatory expert milestone has:
  - a real task;
  - a production acceptance task;
  - Russian and English title and description;
  - a dependency path;
  - no single task requiring more than 64 items.
- All chapter titles and all mandatory progression quests are bilingual.
- Optional legacy/reference chapters may use the English fallback in v1 only when the missing Russian keys remain listed in `QUEST_QUALITY_REPORT.md`; they must not silently display broken keys.
- The lowest-scoring legacy chapters are reviewed in priority order. Generic mass-generated descriptions do not count as an improvement.

## 4. Runtime correctness — mandatory and currently unverified

Evidence must come from a clean full restart, not only `/reload`.

- Client reaches the main menu without KubeJS startup errors.
- A new test world can be created, saved, closed and reopened.
- Every registered `kubejs:` milestone item exists.
- Every replaced strategic recipe is present when its target mod item IDs exist.
- Missing optional item IDs produce one clear warning and do not delete the original recipe.
- At least one regular hostile and one boss from every scaled namespace spawn with the intended attributes.
- FTB Quests loads all chapters and can complete representative item, checkmark and kill tasks.
- Russian and English switching is checked without restarting the world.

## 5. Runtime balance — mandatory

Measured samples must include early, midgame and late equipment.

- Common hostile encounter: neither one-hit trivial nor prolonged beyond the modeled early range.
- Armored mod hostile: midgame weapon result stays within the modeled range or the model is revised.
- Major elite: late-game weapon result stays within the modeled range or the profile is revised.
- Major boss: active combat TTK remains inside the declared range after excluding invulnerability phases and scripted downtime.
- Boss damage must leave the intended late-game test player at least three survivable hits in the representative scenario.

## 6. Performance and stability — mandatory

Absolute startup time is hardware-dependent, so v1 uses repeatable baselines.

- Compare the same world, Java build, memory allocation and graphics settings against `main`.
- Median startup and world-load time must not regress by more than 10% without a documented reason.
- A 30-minute controlled factory/combat soak must maintain at least 18 TPS for 95% of samples.
- No monotonic heap growth after two forced-save and unload/reload cycles.
- No repeating log line above 60 occurrences per minute unless explicitly allowlisted.
- No crash, watchdog termination, deadlock warning or corrupted quest state.

## 7. Release decision

The release decision is binary:

- **Not v1:** any mandatory gate lacks evidence or fails.
- **v1 candidate:** all static, theoretical and quest gates pass; runtime evidence is complete.
- **v1:** the candidate passes a second clean restart and world reopen with no new blocking issue.
