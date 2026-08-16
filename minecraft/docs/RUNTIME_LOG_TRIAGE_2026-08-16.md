# Runtime log triage — 2026-08-16

This report records findings from the user-supplied `logs.zip`. Raw runtime logs are intentionally not committed. The archive was produced before commit `6e5ea239109fe4c5fb38caa628b515a32984a95b`, which removed the failing diagnostic startup exporter, so this run is **pre-fix evidence** and cannot verify `clean_client_start`.

## Environment observed in the log

- Minecraft: **1.21.1**
- NeoForge: **21.1.234**
- Java: **Oracle HotSpot 21.0.3+7-LTS-152**
- OS: **Windows 10 amd64**
- Launcher/instance: **PrismLauncher**
- GPU: **NVIDIA GeForce RTX 5070**, OpenGL 4.6.0, driver string **596.49**
- Exact CPU and allocated heap were not present in the supplied log archive and remain required for comparable performance evidence.

## Startup measurement

ModernFix reported:

- **Game took 143.43 seconds to start**

The log begins at approximately `09:36:05.872`; resource loading and menu-side initialization continue until shortly after `09:38:03`. This value is retained as a diagnostic candidate measurement only. It is not yet a release baseline because the run contained a KubeJS startup error and was not repeated three times in the same environment.

## Blocking issue found and fixed

KubeJS reported:

- **17 / 18 startup scripts loaded**;
- **1 startup error**;
- failure in `startup_scripts:mod_inventory_export.js` while trying to load `java.lang.System` through Rhino's class filter.

The exporter existed only for diagnostics and performed startup file I/O. It has been removed from the branch rather than bypassing the class filter. The static performance contract now requires **zero KubeJS startup file writers**.

Because the supplied run contained this error, `clean_client_start` remains **UNVERIFIED** and a fresh run on the post-fix commit is required.

## World/runtime coverage in this archive

No integrated-server or world lifecycle evidence was found in the supplied logs:

- no integrated server start;
- no spawn preparation;
- no player world login;
- no world save;
- no world reopen.

Therefore this archive does not verify:

- `new_world_create_save_reopen`;
- `kubejs_milestone_items_exist`;
- `strategic_recipes_verified`;
- `representative_quest_tasks_complete`;
- `language_switch_verified`;
- `second_clean_restart_and_world_reopen`.

## Actionable non-blocking startup noise

These entries should be rechecked after the KubeJS fix. They are not currently treated as release blockers without reproduction or functional impact.

1. **Euphoria Patcher** reports that ComplementaryShaders `r5.8.1` is absent, emits repeated ERROR lines and starts a shaderpacks-folder watcher. If the release does not ship/use the required shader, the patcher should be removed rather than left as an inactive error source.
2. **ProjectExpansion** declares a missing `accesstransformer.cfg`. This appears to be a mod packaging issue and should be checked for functional impact before release.
3. Several resource-pack metadata sections fail to parse, including one malformed `pack_format` value. The originating pack needs identification on the next clean run.
4. Resource-path/model noise includes an invalid Stellaris texture path with a space, an invalid UFO font path, several missing AE2 Additions formed models, and isolated missing textures/models from other mods.
5. Moonlight reports Fabric API/Connector presence and warns about compatibility risk. This is informational unless a reproducible incompatibility is observed.
6. A remote Blueprint rewards request failed. Network-dependent cosmetic/reward requests must not be allowed to become startup blockers.

## Performance stack observed

The runtime log confirms that the instance already includes multiple optimization layers, including ModernFix, FerriteCore, FastBoot, Better World Loading, Lithium, ServerCore, ImmediatelyFast, Spark, All The Leaks, GPU Memory Leak Fix, FastSuite/FastBench/FastFurnace and related rendering/world-loading optimizers. Further optimization should therefore be driven by measured bottlenecks and compatibility cleanup rather than adding optimization mods indiscriminately.

## Next evidence run

Use the newest `expert-overhaul-v1` commit after this report and perform:

1. three clean client launches on the same Java/RAM/hardware setup;
2. one new-world create/save/reopen cycle;
3. one second clean restart and reopen of the same test world;
4. archive `latest.log`, `debug.log`, and `logs/kubejs/*.log` from the clean run;
5. record exact allocated RAM and CPU model;
6. continue with the 18 milestone/recipe checks and the representative 30-minute performance soak only after startup is clean.

No runtime gate is marked verified by this report. It exists to preserve the measured pre-fix state and prevent the discovered startup error from being lost during iteration.
