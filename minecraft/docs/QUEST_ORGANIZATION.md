# Quest Book Organization

## Mandatory route

The main progression is divided into **18 separate stage chapters**. Each stage chapter contains **22 mandatory quests**:

- 12 substage quests: system contract, infrastructure build and production acceptance for each of the four substages;
- 10 stage-project quests: supply, process, integration, measurement, controlled failure, automation, bypass review, recovery and final milestone acceptance.

The first quest of every stage after Stage 1 depends on the final quest of the previous stage. The last quest of every stage requires the real milestone item from `expert_progression_contract.json`.

## Optional stage annexes

Every main stage has a separate optional annex with six quests:

1. domain map and mod responsibilities;
2. authoritative recipe and gate map;
3. alternative architecture;
4. diagnostic playbook;
5. capacity and scaling;
6. expert extension project.

Annexes unlock when their stage begins, but never block the next stage. They deepen the relevant mods, show alternative designs and provide troubleshooting without turning optional knowledge into a mandatory grind.

## Curated manuals and legacy catalogues

The seven Core Technology Manuals remain supplementary references. Full catalogue upgrades explain individual machines, items and mechanics. Stage chapters define progression requirements; manuals and catalogues explain how the underlying mods work.

This separation prevents three common problems:

- one enormous progression chapter that is difficult to navigate;
- item catalogues being mistaken for the main route;
- optional experiments blocking mandatory progression.

## Release checks

`stage_chapter_organization_quality_gate.py` verifies:

- 18 main stage chapters with 22 quests each;
- 18 optional annex chapters with six quests each;
- one continuous dependency chain across stage boundaries;
- exactly one milestone item check at the end of each stage;
- full RU/EN titles and detailed descriptions;
- no quest rewards in the organized progression chapters;
- removal of the two old monolithic progression chapters.
