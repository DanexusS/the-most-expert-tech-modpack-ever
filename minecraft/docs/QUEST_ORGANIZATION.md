# Quest Book Organization

## Mandatory route

The main progression is divided into **18 separate stage chapters**. Every stage contains exactly **121 mandatory quests**:

- 12 substage lessons: system contract, infrastructure build and production acceptance for each of four substages;
- 19 staged workflow quests: parallel component branches, mechanism proof, first repeatable production, five measured optimization checks, convergence and recovery;
- 80 operational depth quests: eight workstreams with ten steps each;
- 10 stage-project quests: supply, process, integration, measurement, controlled failure, automation, bypass review, recovery and final milestone acceptance.

The eight operational depth workstreams are:

1. supply chain;
2. component fabrication;
3. machine assembly;
4. commissioning;
5. automation and control;
6. logistics and buffers;
7. quality and recovery;
8. performance optimization.

Each workstream progresses through capability definition, input mapping, a preparation batch, a working prototype, instrumentation, a representative cycle, controlled failure, bounded automation, a fourfold-demand scaling test and acceptance.

The first quest of every stage after Stage 1 depends on the final quest of the previous stage. The last quest of every stage requires the real milestone item from `expert_progression_contract.json`.

## Optional stage annexes

Every main stage has a separate optional annex with six quests:

1. domain map and mod responsibilities;
2. authoritative recipe and gate map;
3. alternative architecture;
4. diagnostic playbook;
5. capacity and scaling;
6. expert extension project.

Annexes unlock when their stage begins but never block the next stage. They deepen the relevant mods, show alternative designs and provide troubleshooting without turning optional knowledge into a mandatory grind.

## Curated manuals and legacy catalogues

The seven Core Technology Manuals remain supplementary references. Full catalogue upgrades explain individual machines, items and mechanics. Stage chapters define progression requirements; manuals and catalogues explain how the underlying mods work.

Legacy chapters are analysed by `legacy_quest_semantic_audit.py`. Chapters are ranked for rewrite when they contain item-only catalogues, missing operational guidance, rewards, excessive counts, duplicate text or malformed objects. Remediation policies remove rewards, add practical acceptance work and provide full RU/EN explanations without adding more quests beyond the 6,000-product ceiling.

## Release checks

The stage organization and depth gates verify:

- 18 main stage chapters with 121 mandatory quests each;
- 18 optional annex chapters with six quests each;
- one continuous dependency chain across stage boundaries;
- correct branched DAG dependencies inside every stage;
- real component and mechanism item tasks at selected production steps;
- exactly one milestone item check at the end of each stage;
- full RU/EN titles and detailed descriptions;
- no quest rewards in organized progression chapters;
- 90 workflow optimization quests and 180 depth optimization quests;
- total questbook size between 5,000 and 6,000 quests.
