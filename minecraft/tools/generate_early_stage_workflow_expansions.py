from __future__ import annotations

import json
import re
from pathlib import Path

from catalog_upgrade_common import matching_delimiter, quest_spans
from manual_generator_common import format_array, stable_id, upsert_localization

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"

WORKFLOW_STAGES: dict[str, dict] = {
    "field_foundations": {
        "branches": [
            {
                "slug": "materials_lab",
                "title_en": "Materials analysis workshop",
                "title_ru": "Мастерская анализа материалов",
                "assemblies": ["kubejs:survey_lens"],
                "target": "kubejs:materials_analysis_matrix",
                "focus_en": "glass preparation, quartz classification, optical alignment and a repeatable comparison standard",
                "focus_ru": "подготовку стекла, классификацию кварца, юстировку оптики и повторяемый эталон сравнения",
            },
            {
                "slug": "regulated_wiring",
                "title_en": "Regulated wiring bench",
                "title_ru": "Стенд регулируемой проводки",
                "assemblies": [
                    "kubejs:insulated_wiring_bundle",
                    "kubejs:manual_control_board",
                ],
                "target": "kubejs:power_regulation_unit",
                "focus_en": "insulation, polarity, redstone control, motor demand and safe isolation of the first powered workbench",
                "focus_ru": "изоляцию, полярность, редстоун-управление, нагрузку двигателя и безопасное отключение первого электрифицированного стенда",
            },
            {
                "slug": "field_tooling",
                "title_en": "Field tooling and repair",
                "title_ru": "Полевая оснастка и ремонт",
                "assemblies": ["kubejs:field_tool_frame"],
                "target": None,
                "focus_en": "reusable tools, protected spares, repair access and a compact kit layout that survives an early-base failure",
                "focus_ru": "многоразовые инструменты, защищённые запчасти, доступ для ремонта и компактную укладку, переживающую отказ ранней базы",
            },
        ],
        "integration_item": "kubejs:field_engineering_kit",
        "optimization_en": "manual batch time, tool travel, protected storage, idle furnaces and recovery after losing one workstation",
        "optimization_ru": "время ручной партии, перемещения с инструментами, защищённое хранение, простаивающие печи и восстановление после потери одного рабочего места",
    },
    "steam_metallurgy": {
        "branches": [
            {
                "slug": "structural_standard",
                "title_en": "Structural standard line",
                "title_ru": "Линия конструкционного стандарта",
                "assemblies": ["kubejs:metallurgical_bracing"],
                "target": "kubejs:structural_lattice",
                "focus_en": "repeatable bracing, dimensional consistency, returned field tooling and a common mounting standard for later machines",
                "focus_ru": "повторяемые распорки, постоянство размеров, возврат полевой оснастки и общий монтажный стандарт поздних машин",
            },
            {
                "slug": "bronze_steam",
                "title_en": "Bronze steam plant",
                "title_ru": "Бронзовая паровая установка",
                "assemblies": ["kubejs:steam_valve_assembly"],
                "target": "modern_industrialization:bronze_boiler",
                "depends_on": ["structural_standard"],
                "focus_en": "water reserve, valve direction, fuel buffering, steam demand and dry-boiler prevention",
                "focus_ru": "резерв воды, направление клапанов, буфер топлива, спрос пара и защиту котла от работы всухую",
            },
            {
                "slug": "refractory_steel",
                "title_en": "Refractory steel route",
                "title_ru": "Огнеупорный путь к стали",
                "assemblies": ["kubejs:refractory_binder"],
                "target": "immersiveengineering:blastbrick_reinforced",
                "depends_on": ["structural_standard"],
                "focus_en": "refractory preparation, coke supply, slag and creosote handling, steel-plate yield and blocked-output shutdown",
                "focus_ru": "подготовку огнеупора, снабжение коксом, работу со шлаком и креозотом, выход стальных пластин и остановку при полном выходе",
            },
        ],
        "integration_item": "kubejs:structural_lattice",
        "optimization_en": "water and fuel reserves, heat-up losses, creosote storage, steel batch size and safe cooling before maintenance",
        "optimization_ru": "резервы воды и топлива, потери на разогрев, хранение креозота, размер партии стали и безопасное охлаждение перед обслуживанием",
    },
    "regulated_electricity": {
        "branches": [
            {
                "slug": "protected_distribution",
                "title_en": "Protected low-voltage distribution",
                "title_ru": "Защищённое низковольтное распределение",
                "assemblies": [
                    "kubejs:low_voltage_busbar",
                    "kubejs:circuit_protection_module",
                ],
                "target": "kubejs:electrical_bus",
                "focus_en": "conductor capacity, protection thresholds, polarity, branch isolation and a visible overload state",
                "focus_ru": "пропускную способность проводников, пороги защиты, полярность, изоляцию ответвлений и видимое состояние перегрузки",
            },
            {
                "slug": "machine_enclosure",
                "title_en": "Powered machine enclosure",
                "title_ru": "Корпус электрической машины",
                "assemblies": ["kubejs:reserve_switchgear"],
                "target": "modern_industrialization:basic_machine_hull",
                "depends_on": ["protected_distribution"],
                "focus_en": "steel enclosure ancestry, service disconnect, circuit and motor stocking, side access and safe replacement",
                "focus_ru": "происхождение стального корпуса, сервисный разъединитель, запас схем и двигателей, доступ со сторон и безопасную замену",
            },
            {
                "slug": "mechanical_integration",
                "title_en": "Electromechanical integration",
                "title_ru": "Электромеханическая интеграция",
                "assemblies": [
                    "modern_industrialization:motor",
                    "modern_industrialization:electronic_circuit",
                ],
                "target": None,
                "depends_on": ["machine_enclosure"],
                "focus_en": "motor starting demand, protected bus connection, ordinary spare parts and the cold-start order of the shared workshop",
                "focus_ru": "пусковой спрос двигателя, подключение к защищённой шине, обычные запчасти и порядок холодного запуска общей мастерской",
            },
        ],
        "integration_item": "kubejs:mechanical_core",
        "optimization_en": "peak load, transfer limits, reserve duration, idle consumers, branch isolation and black-start sequencing",
        "optimization_ru": "пиковую нагрузку, пределы передачи, длительность резерва, потребителей в простое, изоляцию ветвей и последовательность холодного запуска",
    },
    "kinetic_automation": {
        "branches": [
            {
                "slug": "stress_control",
                "title_en": "Stress measurement and control",
                "title_ru": "Измерение и управление нагрузкой",
                "assemblies": ["kubejs:stress_sensor"],
                "target": "kubejs:kinetic_regulator",
                "focus_en": "stress capacity, rotational speed, overload indication, emergency disengagement and a repeatable baseline load",
                "focus_ru": "допустимую нагрузку, скорость вращения, индикацию перегруза, аварийное расцепление и повторяемую базовую нагрузку",
            },
            {
                "slug": "transmission_alignment",
                "title_en": "Transmission alignment",
                "title_ru": "Выравнивание передачи",
                "assemblies": ["kubejs:gearbox_alignment_frame"],
                "target": "create:mechanical_press",
                "focus_en": "shaft alignment, gear ratio, direction changes, service clearance and isolation of a jammed processing machine",
                "focus_ru": "соосность валов, передаточное отношение, смену направления, сервисный зазор и изоляцию заклинившей машины",
            },
            {
                "slug": "sequenced_assembly",
                "title_en": "Sequenced assembly controller",
                "title_ru": "Контроллер последовательной сборки",
                "assemblies": ["kubejs:sequencing_cam"],
                "target": "create:precision_mechanism",
                "depends_on": ["stress_control", "transmission_alignment"],
                "focus_en": "ordered operations, incomplete-item routing, returned tools, input filtering and recovery after an interrupted sequence",
                "focus_ru": "порядок операций, маршрут незавершённого предмета, возврат инструментов, фильтрацию входа и восстановление после прерывания последовательности",
            },
        ],
        "integration_item": "kubejs:kinetic_interface",
        "optimization_en": "stress reserve, shaft length, rotational speed, machine parallelism, belt congestion and chunk-reload recovery",
        "optimization_ru": "запас нагрузки, длину валов, скорость вращения, параллельность машин, перегрузку лент и восстановление после перезагрузки чанка",
    },
}

BRANCH_STEPS = ("requirements", "assemblies", "mechanism", "production")
OPTIMIZATION_STEPS = (
    "baseline",
    "bottleneck",
    "buffers",
    "idle_shutdown",
    "chunk_recovery",
)
CONVERGENCE_STEPS = ("integration", "recovery")


def workflow_id(stage_id: str, *parts: str) -> str:
    return stable_id(":".join(("early_stage_workflow", stage_id, *parts)))


def expanded_stage_ids() -> set[str]:
    return set(WORKFLOW_STAGES)


def workflow_quest_ids(stage_id: str) -> list[str]:
    profile = WORKFLOW_STAGES.get(stage_id)
    if profile is None:
        return []
    ids: list[str] = []
    for branch in profile["branches"]:
        ids.extend(workflow_id(stage_id, branch["slug"], step) for step in BRANCH_STEPS)
    ids.extend(workflow_id(stage_id, "optimization", step) for step in OPTIMIZATION_STEPS)
    ids.extend(workflow_id(stage_id, step) for step in CONVERGENCE_STEPS)
    return ids


def workflow_final_id(stage_id: str) -> str:
    return workflow_id(stage_id, "recovery")


def expected_dependencies(stage_id: str, entry_id: str) -> dict[str, list[str]]:
    profile = WORKFLOW_STAGES[stage_id]
    result: dict[str, list[str]] = {}
    branch_finals: dict[str, str] = {}
    for branch in profile["branches"]:
        slug = branch["slug"]
        roots = [branch_finals[value] for value in branch.get("depends_on", [])]
        root_dependencies = roots or [entry_id]
        previous = ""
        for position, step in enumerate(BRANCH_STEPS):
            quest_id = workflow_id(stage_id, slug, step)
            result[quest_id] = root_dependencies if position == 0 else [previous]
            previous = quest_id
        branch_finals[slug] = previous

    previous = ""
    for position, step in enumerate(OPTIMIZATION_STEPS):
        quest_id = workflow_id(stage_id, "optimization", step)
        result[quest_id] = [entry_id] if position == 0 else [previous]
        previous = quest_id
    optimization_final = previous

    integration = workflow_id(stage_id, "integration")
    result[integration] = list(branch_finals.values()) + [optimization_final]
    recovery = workflow_final_id(stage_id)
    result[recovery] = [integration]
    return result


def expected_item_tasks(stage_id: str) -> dict[str, list[str]]:
    profile = WORKFLOW_STAGES[stage_id]
    result: dict[str, list[str]] = {}
    for branch in profile["branches"]:
        result[workflow_id(stage_id, branch["slug"], "assemblies")] = list(
            branch["assemblies"]
        )
        if branch.get("target"):
            result[workflow_id(stage_id, branch["slug"], "mechanism")] = [
                branch["target"]
            ]
    result[workflow_id(stage_id, "integration")] = [profile["integration_item"]]
    return result


def task_block(namespace: str, items: list[str] | None = None) -> str:
    tasks: list[str] = []
    for position, item_id in enumerate(items or []):
        task_id = stable_id(f"{namespace}:item:{position}:{item_id}")
        tasks.append(
            "\t\t{\n"
            f"\t\t\tid: \"{task_id}\"\n"
            f"\t\t\titem: {{ count: 1, id: \"{item_id}\" }}\n"
            "\t\t\ttype: \"item\"\n"
            "\t\t}"
        )
    check_id = stable_id(f"{namespace}:check")
    tasks.append(
        "\t\t{\n"
        f"\t\t\tid: \"{check_id}\"\n"
        "\t\t\ttype: \"checkmark\"\n"
        "\t\t}"
    )
    return "[\n" + "\n".join(tasks) + "\n\t]"


def dependency_line(values: list[str]) -> str:
    return "[" + " ".join(f'\"{value}\"' for value in values) + "]"


def quest_block(
    quest_id: str,
    dependencies: list[str],
    icon: str,
    x: float,
    y: float,
    items: list[str] | None = None,
    shape: str = "hexagon",
) -> str:
    return (
        "\t{\n"
        f"\t\tdependencies: {dependency_line(dependencies)}\n"
        f"\t\ticon: {{ id: \"{icon}\" }}\n"
        f"\t\tid: \"{quest_id}\"\n"
        f"\t\tshape: \"{shape}\"\n"
        f"\t\ttasks: {task_block(quest_id, items)}\n"
        f"\t\tx: {x:.1f}d\n"
        f"\t\ty: {y:.1f}d\n"
        "\t}"
    )


def branch_content(stage: dict, branch: dict, step: str) -> tuple[str, list[str], str, list[str]]:
    stage_en = stage["title_en"]
    stage_ru = stage["title_ru"]
    title_en = branch["title_en"]
    title_ru = branch["title_ru"]
    assemblies = ", ".join(branch["assemblies"])
    target = branch.get("target") or "the verified subsystem"
    target_ru = branch.get("target") or "проверенную подсистему"
    focus_en = branch["focus_en"]
    focus_ru = branch["focus_ru"]

    if step == "requirements":
        return (
            f"{title_en} — prepare the route",
            [
                f"Before crafting the final subsystem for {stage_en}, define the legal inputs and the machine or hand-tool sequence for {title_en.lower()}. The route must cover {focus_en}.",
                "Prepare a labelled input buffer for at least two attempts, identify returned tools and containers, and confirm that no quest reward, trade, EMC value or later-stage machine replaces the intended work.",
            ],
            f"{title_ru} — подготовка пути",
            [
                f"До крафта готовой подсистемы этапа «{stage_ru}» определите законные входы и последовательность машин или инструментов для направления «{title_ru.lower()}». Путь должен охватывать {focus_ru}.",
                "Подготовьте подписанный входной буфер минимум на две попытки, отметьте возвращаемые инструменты и контейнеры и исключите замену работы наградой, торговлей, EMC или машиной будущего этапа.",
            ],
        )
    if step == "assemblies":
        return (
            f"{title_en} — intermediate assemblies",
            [
                f"Produce the actual intermediate assemblies: {assemblies}. These components separate material preparation from the final mechanism and make failures diagnosable instead of hiding every cost in one 3×3 recipe.",
                "Acceptance: produce a second set from stored ordinary materials, record the slowest input and keep one normal spare. The assemblies are consumable batch parts, not permanent permissions.",
            ],
            f"{title_ru} — промежуточные узлы",
            [
                f"Изготовьте реальные промежуточные узлы: {assemblies}. Они отделяют подготовку материалов от готового механизма и позволяют диагностировать отказ вместо сокрытия всей стоимости в одном крафте 3×3.",
                "Приёмка: изготовьте второй комплект из обычного запаса, запишите самый медленный вход и сохраните одну стандартную запчасть. Эти узлы являются расходуемыми деталями партии, а не постоянными допусками.",
            ],
        )
    if step == "mechanism":
        return (
            f"{title_en} — working mechanism",
            [
                f"Combine the prepared assemblies into {target}. The finished mechanism is evidence that the preceding material, tooling and control steps work together; obtaining an unrelated copy does not prove the production route.",
                f"Acceptance: inspect {focus_en}; perform one valid operation and one deliberately invalid or blocked operation, then return the system to a safe state without deleting rare inputs.",
            ],
            f"{title_ru} — рабочий механизм",
            [
                f"Объедините подготовленные узлы в {target_ru}. Готовый механизм подтверждает совместную работу предыдущих материалов, оснастки и управления; случайно полученная копия не доказывает производственный путь.",
                f"Приёмка: проверьте {focus_ru}; выполните одну штатную и одну намеренно неверную или заблокированную операцию, затем безопасно восстановите систему без уничтожения редких входов.",
            ],
        )
    return (
        f"{title_en} — repeatable production",
        [
            f"Turn {title_en.lower()} into a repeatable part of {stage_en}. Feed inputs from labelled storage, route every output and byproduct, and remove the need to rearrange inventories between normal cycles.",
            "Run a representative unattended batch, record input rate, output rate and reserve, and prove that empty input or full output stops only this branch rather than deadlocking the whole stage.",
        ],
        f"{title_ru} — повторяемое производство",
        [
            f"Превратите направление «{title_ru.lower()}» в повторяемую часть этапа «{stage_ru}». Подавайте входы из подписанного хранения, отведите каждый выход и побочный продукт и исключите ручную перестановку между штатными циклами.",
            "Выполните типовую автономную партию, запишите скорость входа, выхода и резерв и докажите, что пустой вход или полный выход останавливает только эту ветвь, а не блокирует весь этап.",
        ],
    )


def optimization_content(stage: dict, profile: dict, step: str) -> tuple[str, list[str], str, list[str]]:
    focus_en = profile["optimization_en"]
    focus_ru = profile["optimization_ru"]
    titles = {
        "baseline": ("Measure the baseline", "Измерьте исходное состояние"),
        "bottleneck": ("Find the real bottleneck", "Найдите настоящее узкое место"),
        "buffers": ("Right-size buffers", "Рассчитайте буферы"),
        "idle_shutdown": ("Control idle cost", "Управляйте стоимостью простоя"),
        "chunk_recovery": ("Recover after reload", "Восстановление после перезагрузки"),
    }
    title_en, title_ru = titles[step]
    detail_en = {
        "baseline": f"Measure one normal cycle of Stage {stage['index']} before changing the design. Record {focus_en}; a faster machine is irrelevant when another branch is already limiting the batch.",
        "bottleneck": "Increase demand gradually and identify the first queue, empty input or overloaded network. Change only the limiting section and compare the result with the recorded baseline.",
        "buffers": "Size input, intermediate and output buffers from measured rates. Keep enough reserve for recovery, but avoid inventories so large that a fault remains hidden for hours.",
        "idle_shutdown": "Stop avoidable power, fuel, rotation, pressure or entity work when demand is absent. The shutdown must not lose recipe state, void inputs or require rebuilding the line.",
        "chunk_recovery": "Reload the relevant chunks or simulate a clean restart. Verify filters, directions, ownership and machine state, then document the shortest safe recovery procedure.",
    }[step]
    detail_ru = {
        "baseline": f"До изменения конструкции измерьте один штатный цикл этапа {stage['index']}. Запишите {focus_ru}; ускорение отдельной машины бесполезно, если партию уже ограничивает другая ветвь.",
        "bottleneck": "Постепенно увеличивайте спрос и найдите первую очередь, пустой вход или перегруженную сеть. Измените только ограничивающий участок и сравните результат с исходным измерением.",
        "buffers": "Рассчитайте входные, промежуточные и выходные буферы по измеренной скорости. Оставьте резерв для восстановления, но не скрывайте отказ гигантским складом на несколько часов.",
        "idle_shutdown": "Отключайте ненужное питание, топливо, вращение, давление или работу существ при отсутствии спроса. Остановка не должна терять состояние рецепта, уничтожать входы или требовать перестройки линии.",
        "chunk_recovery": "Перезагрузите соответствующие чанки или смоделируйте чистый перезапуск. Проверьте фильтры, направления, владение и состояние машин, затем задокументируйте кратчайший безопасный порядок восстановления.",
    }[step]
    return (
        f"Optimization — {title_en}",
        [detail_en, "Acceptance requires a before/after observation and a concrete design change; checking the box without measuring or modifying the system is not completion."],
        f"Оптимизация — {title_ru}",
        [detail_ru, "Для приёмки нужны наблюдение до и после и конкретное изменение конструкции; отметка без измерения или изменения системы не завершает квест."],
    )


def convergence_content(stage: dict, profile: dict, step: str) -> tuple[str, list[str], str, list[str]]:
    if step == "integration":
        return (
            f"Stage {stage['index']} integration build",
            [
                f"Combine the completed production branches and the optimization branch into the stage capability {profile['integration_item']}. Preserve clear buffers between subsystems so a failure has one visible owner.",
                "Produce the integration item through the authoritative recipe, verify every prerequisite branch remains reproducible, and reject any alternate acquisition that skips an intermediate assembly or a declared earlier-stage standard.",
            ],
            f"Интеграционная сборка этапа {stage['index']}",
            [
                f"Объедините завершённые производственные ветви и ветвь оптимизации в возможность этапа {profile['integration_item']}. Сохраните явные буферы между подсистемами, чтобы у отказа был один понятный владелец.",
                "Получите интеграционный предмет авторитетным рецептом, проверьте воспроизводимость каждой предыдущей ветви и отклоните любой путь, пропускающий промежуточный узел или заявленный стандарт раннего этапа.",
            ],
        )
    return (
        f"Stage {stage['index']} recovery rehearsal",
        [
            "Before professional stage certification, rehearse recovery from one failed branch: isolate it, preserve healthy buffers, replace ordinary consumables and restart in the documented order.",
            "Keep the integration item as proof, restore a production-ready spare batch and confirm that the following certification quests can be completed without administrator commands, creative items or random rewards.",
        ],
        f"Репетиция восстановления этапа {stage['index']}",
        [
            "До профессиональной сертификации этапа отработайте восстановление одной отказавшей ветви: изолируйте её, сохраните исправные буферы, замените обычные расходники и запустите систему в задокументированном порядке.",
            "Сохраните интеграционный предмет как доказательство, восстановите запас деталей для следующей партии и подтвердите возможность продолжения без команд администратора, creative-предметов и случайных наград.",
        ],
    )


def replace_dependencies(block: str, dependencies: list[str]) -> str:
    rendered = f"dependencies: {dependency_line(dependencies)}"
    pattern = re.compile(r"dependencies:\s*\[[^\]]*\]")
    updated, count = pattern.subn(rendered, block, count=1)
    if count:
        return updated
    insertion = block.find("\n") + 1
    return block[:insertion] + f"\t\t{rendered}\n" + block[insertion:]


def generate_stage(stage: dict, profile: dict) -> tuple[str, dict[str, dict[str, str]]]:
    index = int(stage["index"])
    filename = f"main_stage_{index:02d}_{stage['id']}"
    path = CHAPTER_DIR / f"{filename}.snbt"
    text = path.read_text(encoding="utf-8")
    entry_id = stable_id(
        f"expert_progression_spine:{stage['id']}:{stage['substages'][-1]}:acceptance"
    )
    first_matrix_id = stable_id(f"v1_stage_project:{stage['id']}:entry_contract")
    spans = quest_spans(text)
    first_matrix_span: tuple[int, int] | None = None
    for start, end in spans:
        if f'id: "{first_matrix_id}"' in text[start:end]:
            first_matrix_span = (start, end)
            break
    if first_matrix_span is None:
        raise RuntimeError(f"{filename}: first stage-project quest not found")

    dependencies = expected_dependencies(stage["id"], entry_id)
    items_by_quest = expected_item_tasks(stage["id"])
    blocks: list[str] = []
    localization: dict[str, dict[str, str]] = {"en_us": {}, "ru_ru": {}}

    for branch_index, branch in enumerate(profile["branches"]):
        for step_index, step in enumerate(BRANCH_STEPS):
            quest_id = workflow_id(stage["id"], branch["slug"], step)
            items = items_by_quest.get(quest_id)
            blocks.append(
                quest_block(
                    quest_id,
                    dependencies[quest_id],
                    items[0] if items else stage["milestone"],
                    branch_index * 8.0 + step_index * 1.7,
                    31.0 + step_index * 3.0,
                    items,
                    "diamond" if step == "mechanism" else "hexagon",
                )
            )
            title_en, desc_en, title_ru, desc_ru = branch_content(stage, branch, step)
            localization["en_us"][f"quest.{quest_id}.title"] = json.dumps(title_en, ensure_ascii=False)
            localization["en_us"][f"quest.{quest_id}.quest_desc"] = format_array(desc_en)
            localization["ru_ru"][f"quest.{quest_id}.title"] = json.dumps(title_ru, ensure_ascii=False)
            localization["ru_ru"][f"quest.{quest_id}.quest_desc"] = format_array(desc_ru)

    for step_index, step in enumerate(OPTIMIZATION_STEPS):
        quest_id = workflow_id(stage["id"], "optimization", step)
        blocks.append(
            quest_block(
                quest_id,
                dependencies[quest_id],
                stage["milestone"],
                27.0 + step_index * 1.8,
                31.0 + step_index * 3.0,
                None,
                "gear",
            )
        )
        title_en, desc_en, title_ru, desc_ru = optimization_content(stage, profile, step)
        localization["en_us"][f"quest.{quest_id}.title"] = json.dumps(title_en, ensure_ascii=False)
        localization["en_us"][f"quest.{quest_id}.quest_desc"] = format_array(desc_en)
        localization["ru_ru"][f"quest.{quest_id}.title"] = json.dumps(title_ru, ensure_ascii=False)
        localization["ru_ru"][f"quest.{quest_id}.quest_desc"] = format_array(desc_ru)

    for step_index, step in enumerate(CONVERGENCE_STEPS):
        quest_id = workflow_id(stage["id"], step)
        items = items_by_quest.get(quest_id)
        blocks.append(
            quest_block(
                quest_id,
                dependencies[quest_id],
                profile["integration_item"],
                15.0 + step_index * 4.0,
                48.0,
                items,
                "diamond" if step == "integration" else "hexagon",
            )
        )
        title_en, desc_en, title_ru, desc_ru = convergence_content(stage, profile, step)
        localization["en_us"][f"quest.{quest_id}.title"] = json.dumps(title_en, ensure_ascii=False)
        localization["en_us"][f"quest.{quest_id}.quest_desc"] = format_array(desc_en)
        localization["ru_ru"][f"quest.{quest_id}.title"] = json.dumps(title_ru, ensure_ascii=False)
        localization["ru_ru"][f"quest.{quest_id}.quest_desc"] = format_array(desc_ru)

    first_start, first_end = first_matrix_span
    first_block = replace_dependencies(text[first_start:first_end], [workflow_final_id(stage["id"])])
    expanded = text[:first_start] + "\n".join(blocks) + "\n" + first_block + text[first_end:]
    path.write_text(expanded, encoding="utf-8", newline="\n")
    return filename, localization


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    stages = {stage["id"]: stage for stage in contract["stages"]}
    all_localization: dict[str, dict[str, str]] = {"en_us": {}, "ru_ru": {}}
    generated = 0
    for stage_id, profile in WORKFLOW_STAGES.items():
        stage = stages.get(stage_id)
        if stage is None:
            raise RuntimeError(f"Workflow stage missing from progression contract: {stage_id}")
        _, localization = generate_stage(stage, profile)
        for locale in all_localization:
            all_localization[locale].update(localization[locale])
        generated += len(workflow_quest_ids(stage_id))

    for locale, entries in all_localization.items():
        path = LANG_DIR / f"{locale}.snbt"
        text = path.read_text(encoding="utf-8")
        for key, value in entries.items():
            text = upsert_localization(text, key, value)
        path.write_text(text, encoding="utf-8", newline="\n")

    print(f"expanded_early_stages: {len(WORKFLOW_STAGES)}")
    print(f"early_stage_workflow_quests: {generated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
