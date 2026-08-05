from __future__ import annotations

import json
import re
from pathlib import Path

import generate_early_stage_workflow_expansions as workflow
import generate_stage_project_matrix as matrix
from advanced_stage_workflow_profiles import ADVANCED_STAGE_WORKFLOW_PROFILES
from catalog_upgrade_common import matching_delimiter, quest_spans
from late_stage_workflow_profiles import LATE_STAGE_WORKFLOW_PROFILES
from manual_generator_common import format_array, stable_id
from mid_stage_workflow_profiles import MID_STAGE_WORKFLOW_PROFILES

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
PROFILE_PATH = ROOT / "config" / "progression_project_profiles.json"
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
KEY_RE = re.compile(r"(?m)^\t([A-Za-z0-9_.-]+):")

TRACKS = (
    ("supply_chain", "Supply Chain", "Цепочка снабжения", "supply_en", "supply_ru"),
    ("component_fabrication", "Component Fabrication", "Производство компонентов", "process_en", "process_ru"),
    ("machine_assembly", "Machine Assembly", "Сборка механизма", "integration_en", "integration_ru"),
    ("commissioning", "Commissioning", "Ввод в эксплуатацию", "measurement_en", "measurement_ru"),
    ("automation_control", "Automation and Control", "Автоматизация и управление", "automation_en", "automation_ru"),
    ("logistics_buffers", "Logistics and Buffers", "Логистика и буферы", "supply_en", "supply_ru"),
    ("quality_recovery", "Quality and Recovery", "Качество и восстановление", "recovery_en", "recovery_ru"),
    ("performance_optimization", "Performance Optimization", "Оптимизация производительности", "measurement_en", "measurement_ru"),
)

PHASES = (
    (
        "contract",
        "Capability Contract",
        "Контракт возможности",
        "Define the exact capability, legal inputs, owned transformations, expected outputs and the boundary that prevents this workstream from opening a later-stage shortcut.",
        "Определите точную возможность, законные входы, владельцев преобразований, ожидаемые выходы и границу, не позволяющую этой ветви открыть возможность будущего этапа.",
    ),
    (
        "input_map",
        "Input and Source Map",
        "Карта входов и источников",
        "List every ordinary, renewable, unique and reusable input. Assign a labelled source, minimum reserve, overflow destination and replacement path without quest rewards or administrator intervention.",
        "Перечислите обычные, возобновляемые, уникальные и многоразовые входы. Назначьте подписанный источник, минимальный резерв, переполнение и путь замены без наград и вмешательства администратора.",
    ),
    (
        "preparation",
        "Preparation Batch",
        "Подготовительная партия",
        "Produce a small qualified batch of the required intermediate materials or assemblies. Record yield, returned tools, rejected pieces and the time needed to reproduce the batch.",
        "Произведите небольшую квалифицированную партию промежуточных материалов или сборок. Запишите выход, возврат инструментов, брак и время повторения партии.",
    ),
    (
        "prototype",
        "Working Prototype",
        "Рабочий прототип",
        "Build the smallest complete prototype that demonstrates the workstream without pretending that one crafted block is a finished factory. Keep service access and visible state from the first layout.",
        "Соберите минимальный законченный прототип, доказывающий работу ветви, но не выдавайте один блок за готовую фабрику. Сразу предусмотрите обслуживание и видимое состояние.",
    ),
    (
        "instrumentation",
        "Instrumentation",
        "Измерительные средства",
        "Expose useful measurements for rate, reserve, load, pressure, channels, heat, inventory or error state. The operator must identify the bottleneck without opening every machine.",
        "Выведите полезные измерения скорости, резерва, нагрузки, давления, каналов, тепла, запасов или ошибок. Оператор должен находить узкое место без открытия каждой машины.",
    ),
    (
        "first_cycle",
        "Representative Production Cycle",
        "Типовой производственный цикл",
        "Run a representative cycle from legal input to accepted output. Reconcile all consumed materials, returned containers and byproducts, then repeat the cycle to prove it was not a lucky one-off.",
        "Выполните типовой цикл от законного входа до принятого выхода. Сверьте расходы, возвращённые контейнеры и побочные продукты, затем повторите цикл, доказав, что результат не был случайным.",
    ),
    (
        "failure_mode",
        "Controlled Failure",
        "Контролируемый отказ",
        "Trigger one bounded failure: empty input, blocked output, lost power, invalid recipe, unloaded chunk or disabled link. The failure must remain local and must not destroy rare or unique progress.",
        "Вызовите один ограниченный отказ: пустой вход, полный выход, потерю энергии, неверный рецепт, выгруженный чанк или отключённую связь. Отказ должен остаться локальным и не уничтожить редкий прогресс.",
    ),
    (
        "automation",
        "Bounded Automation",
        "Ограниченная автоматизация",
        "Automate the normal cycle with explicit filters, priorities, stop conditions and ownership. Empty input, full output and restart must produce a safe idle state rather than duplication or deadlock.",
        "Автоматизируйте обычный цикл с явными фильтрами, приоритетами, условиями остановки и владением. Пустой вход, полный выход и перезапуск должны давать безопасный простой без копирования и тупика.",
    ),
    (
        "scale_test",
        "Fourfold Demand Test",
        "Испытание четырёхкратным спросом",
        "Raise representative demand to four times the baseline. Scale only the measured limiting section, preserve upstream and downstream balance and document the new ordinary-spare requirement.",
        "Увеличьте типовой спрос в четыре раза. Расширяйте только измеренное узкое место, сохраняйте баланс до и после него и задокументируйте новый запас обычных запчастей.",
    ),
    (
        "acceptance",
        "Workstream Acceptance",
        "Приёмка рабочей ветви",
        "Present the qualified inputs, repeatable output, measurements, automation boundary, controlled failure result, recovery procedure and one reusable design rule for the next workstream.",
        "Представьте квалифицированные входы, повторяемый выход, измерения, границу автоматизации, результат контролируемого отказа, процедуру восстановления и один принцип для следующей ветви.",
    ),
)


def depth_id(stage_id: str, track: str, phase: str) -> str:
    return stable_id(f"stage_depth:{stage_id}:{track}:{phase}")


def depth_quest_ids(stage_id: str) -> list[str]:
    return [depth_id(stage_id, track[0], phase[0]) for track in TRACKS for phase in PHASES]


def depth_final_id(stage_id: str) -> str:
    return depth_id(stage_id, "performance_optimization", "acceptance")


def merged_workflow_profiles() -> dict[str, dict]:
    result = dict(workflow.WORKFLOW_STAGES)
    for profiles in (
        MID_STAGE_WORKFLOW_PROFILES,
        ADVANCED_STAGE_WORKFLOW_PROFILES,
        LATE_STAGE_WORKFLOW_PROFILES,
    ):
        overlap = set(result) & set(profiles)
        if overlap:
            raise RuntimeError("Duplicate depth workflow profiles: " + ", ".join(sorted(overlap)))
        result.update(profiles)
    return result


def expected_dependencies(stage_id: str, entry_id: str) -> dict[str, list[str]]:
    finals: dict[str, str] = {}
    expected: dict[str, list[str]] = {}
    for track, *_ in TRACKS:
        if track == "supply_chain":
            root = [entry_id]
        elif track == "component_fabrication":
            root = [finals["supply_chain"]]
        elif track == "machine_assembly":
            root = [finals["component_fabrication"]]
        elif track == "commissioning":
            root = [finals["machine_assembly"]]
        elif track == "automation_control":
            root = [finals["commissioning"]]
        elif track == "logistics_buffers":
            root = [finals["supply_chain"]]
        elif track == "quality_recovery":
            root = [finals["machine_assembly"], finals["logistics_buffers"]]
        else:
            root = [finals["automation_control"], finals["quality_recovery"]]

        previous = ""
        for position, phase in enumerate(PHASES):
            quest_id = depth_id(stage_id, track, phase[0])
            expected[quest_id] = root if position == 0 else [previous]
            previous = quest_id
        finals[track] = previous
    return expected


def item_expectations(stage: dict, workflow_profile: dict) -> dict[str, list[tuple[str, int]]]:
    stage_id = stage["id"]
    assemblies = [
        item
        for branch in workflow_profile["branches"]
        for item in branch.get("assemblies", [])
    ]
    targets = [
        branch["target"]
        for branch in workflow_profile["branches"]
        if branch.get("target")
    ]
    gated = [item for item in stage.get("gated_outputs", []) if item != stage["milestone"]]
    result: dict[str, list[tuple[str, int]]] = {}
    if assemblies:
        result[depth_id(stage_id, "supply_chain", "preparation")] = [(assemblies[0], 2)]
        result[depth_id(stage_id, "component_fabrication", "first_cycle")] = [
            (item, 2) for item in assemblies[:4]
        ]
    if targets:
        result[depth_id(stage_id, "machine_assembly", "prototype")] = [
            (item, 1) for item in targets[:4]
        ]
        result[depth_id(stage_id, "automation_control", "automation")] = [
            (item, 1) for item in targets[:3]
        ]
    if gated:
        result[depth_id(stage_id, "commissioning", "first_cycle")] = [
            (item, 1) for item in gated[:4]
        ]
    return result


def render_tasks(namespace: str, items: list[tuple[str, int]]) -> str:
    blocks: list[str] = []
    for position, (item_id, count) in enumerate(items):
        task_id = stable_id(f"{namespace}:item:{position}:{item_id}:{count}")
        blocks.append(
            "\t\t{\n"
            f"\t\t\tid: \"{task_id}\"\n"
            f"\t\t\titem: {{ count: {count}, id: \"{item_id}\" }}\n"
            "\t\t\ttype: \"item\"\n"
            "\t\t}"
        )
    check_id = stable_id(f"{namespace}:check")
    blocks.append(
        "\t\t{\n"
        f"\t\t\tid: \"{check_id}\"\n"
        "\t\t\ttype: \"checkmark\"\n"
        "\t\t}"
    )
    return "[\n" + "\n".join(blocks) + "\n\t]"


def dependency_array(values: list[str]) -> str:
    return "[" + " ".join(f'\"{value}\"' for value in values) + "]"


def visible_name(value: str) -> str:
    return value.replace("_", " ").title()


def descriptions(stage: dict, profile: dict, track: tuple, phase: tuple) -> tuple[str, list[str], str, list[str]]:
    track_slug, track_en, track_ru, focus_en_key, focus_ru_key = track
    phase_slug, phase_en, phase_ru, action_en, action_ru = phase
    domains = ", ".join(stage["required_domains"])
    outputs = ", ".join(stage["gated_outputs"][:5])
    title_en = f"Stage {stage['index']} — {track_en}: {phase_en}"
    title_ru = f"Этап {stage['index']} — {track_ru}: {phase_ru}"
    focus_en = profile[focus_en_key]
    focus_ru = profile[focus_ru_key]
    en = [
        f"This mandatory {track_en.lower()} step belongs to Stage {stage['index']} — {stage['title_en']}. It develops {focus_en}. The participating domains are {domains}; protected outputs include {outputs}.",
        f"Acceptance for {phase_en.lower()}: {action_en} Record the result so the next step can reuse measured state instead of repeating blind trial and error.",
    ]
    ru = [
        f"Этот обязательный шаг ветви «{track_ru}» относится к этапу {stage['index']} — «{stage['title_ru']}». Он развивает направление: {focus_ru}. Участвующие области: {domains}; защищённые выходы: {outputs}.",
        f"Приёмка шага «{phase_ru}»: {action_ru} Запишите результат, чтобы следующий шаг использовал измеренное состояние, а не повторял слепые попытки.",
    ]
    return title_en, en, title_ru, ru


def quest_block(
    quest_id: str,
    dependencies: list[str],
    icon: str,
    x: float,
    y: float,
    items: list[tuple[str, int]],
    shape: str,
) -> str:
    return (
        "\t{\n"
        f"\t\tdependencies: {dependency_array(dependencies)}\n"
        f"\t\ticon: {{ id: \"{icon}\" }}\n"
        f"\t\tid: \"{quest_id}\"\n"
        f"\t\tshape: \"{shape}\"\n"
        f"\t\ttasks: {render_tasks(f'stage_depth:{quest_id}', items)}\n"
        f"\t\tx: {x:.1f}d\n"
        f"\t\ty: {y:.1f}d\n"
        "\t}"
    )


def quest_id_from_block(block: str) -> str:
    match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if match is None:
        raise RuntimeError("Quest block without a valid ID")
    return match.group(1)


def replace_dependencies(block: str, values: list[str]) -> str:
    replacement = f"\t\tdependencies: {dependency_array(values)}"
    updated, count = re.subn(
        r'(?m)^\s*dependencies:\s*\[[^\]]*\]\s*$',
        replacement,
        block,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not replace matrix entry dependency")
    return updated


def replace_entries(text: str, entries: dict[str, str]) -> str:
    matches = list(KEY_RE.finditer(text))
    closing = text.rfind("}")
    if closing < 0:
        raise RuntimeError("Localization file has no closing brace")
    if not matches:
        prefix = text[:closing].rstrip() + "\n"
        kept = []
    else:
        prefix = text[:matches[0].start()]
        kept: list[str] = []
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else closing
            if match.group(1) not in entries:
                kept.append(text[match.start():end])
    rendered = [f"\t{key}: {value}\n" for key, value in sorted(entries.items())]
    return prefix + "".join(kept).rstrip() + "\n" + "".join(rendered) + "}\n"


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    profiles = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))["profiles"]
    workflow_profiles = merged_workflow_profiles()
    localization: dict[str, dict[str, str]] = {"en_us": {}, "ru_ru": {}}
    total = 0

    for stage in contract["stages"]:
        stage_id = stage["id"]
        index = int(stage["index"])
        workflow_profile = workflow_profiles.get(stage_id)
        if workflow_profile is None:
            raise RuntimeError(f"Missing workflow profile for depth stage {stage_id}")
        profile = profiles[stage_id]
        chapter_path = CHAPTER_DIR / f"main_stage_{index:02d}_{stage_id}.snbt"
        text = chapter_path.read_text(encoding="utf-8")
        spans = quest_spans(text)
        blocks = [text[start:end] for start, end in spans]
        depth_ids = set(depth_quest_ids(stage_id))
        blocks = [block for block in blocks if quest_id_from_block(block) not in depth_ids]

        matrix_entry = matrix.stable_id(
            f"v1_stage_project:{stage_id}:{matrix.LESSONS[0]['slug']}"
        )
        matrix_position = next(
            (position for position, block in enumerate(blocks) if quest_id_from_block(block) == matrix_entry),
            None,
        )
        if matrix_position is None:
            raise RuntimeError(f"Matrix entry not found for {stage_id}")

        entry_id = workflow.workflow_final_id(stage_id)
        deps = expected_dependencies(stage_id, entry_id)
        items = item_expectations(stage, workflow_profile)
        generated: list[str] = []
        for track_index, track in enumerate(TRACKS):
            for phase_index, phase in enumerate(PHASES):
                quest_id = depth_id(stage_id, track[0], phase[0])
                title_en, desc_en, title_ru, desc_ru = descriptions(stage, profile, track, phase)
                localization["en_us"][f"quest.{quest_id}.title"] = json.dumps(title_en, ensure_ascii=False)
                localization["en_us"][f"quest.{quest_id}.quest_desc"] = format_array(desc_en)
                localization["ru_ru"][f"quest.{quest_id}.title"] = json.dumps(title_ru, ensure_ascii=False)
                localization["ru_ru"][f"quest.{quest_id}.quest_desc"] = format_array(desc_ru)
                generated.append(
                    quest_block(
                        quest_id,
                        deps[quest_id],
                        stage["milestone"],
                        track_index * 7.5,
                        28.0 + phase_index * 3.2,
                        items.get(quest_id, []),
                        "diamond" if phase[0] == "acceptance" else "hexagon",
                    )
                )
                total += 1

        blocks[matrix_position] = replace_dependencies(
            blocks[matrix_position], [depth_final_id(stage_id)]
        )
        blocks[matrix_position:matrix_position] = generated

        marker = text.find("quests:")
        array_start = text.find("[", marker)
        array_end = matching_delimiter(text, array_start, "[", "]")
        body = "\n" + "\n".join(blocks) + "\n\t"
        chapter_path.write_text(
            text[: array_start + 1] + body + text[array_end:],
            encoding="utf-8",
            newline="\n",
        )

    for locale, entries in localization.items():
        path = LANG_DIR / f"{locale}.snbt"
        path.write_text(
            replace_entries(path.read_text(encoding="utf-8"), entries),
            encoding="utf-8",
            newline="\n",
        )

    print(f"depth_stages: {len(contract['stages'])}")
    print(f"depth_quests: {total}")
    print(f"depth_per_stage: {len(TRACKS) * len(PHASES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
