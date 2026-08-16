from __future__ import annotations

import json
from pathlib import Path

import generate_progression_spine as spine
import generate_stage_project_matrix as matrix
from manual_generator_common import format_array, stable_id, upsert_localization

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
PROFILE_PATH = ROOT / "config" / "progression_project_profiles.json"
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
DOCS_DIR = ROOT / "docs"

MAIN_GROUP_ID = "F56B9C180F65BF60"
ANNEX_GROUP_ID = "99948FA76BB60233"
LEGACY_CHAPTERS = (
    CHAPTER_DIR / "expert_progression_spine.snbt",
    CHAPTER_DIR / "v1_stage_project_matrix.snbt",
)
LEGACY_REPORTS = (
    DOCS_DIR / "PROGRESSION_SPINE_QUALITY_REPORT.md",
    DOCS_DIR / "STAGE_PROJECT_MATRIX_QUALITY_REPORT.md",
)

ANNEX_LESSONS = (
    (
        "domain_map",
        "Domain Map and Responsibilities",
        "Карта направлений и ответственности",
        lambda stage, profile: [
            f"This optional annex expands Stage {stage['index']} — {stage['title_en']}. Its gameplay domains are {', '.join(stage['required_domains'])}; assign one explicit responsibility to every domain before combining their machines or resources.",
            f"Deep-dive task: document which mod owns acquisition, transformation, storage, transport and control. Use {profile['integration_en']} as the integration target and identify one interface buffer between each pair of mods.",
        ],
        lambda stage, profile: [
            f"Это необязательное приложение углубляет этап {stage['index']} — «{stage['title_ru']}». Игровые направления: {', '.join(stage['required_domains'])}; до объединения машин или ресурсов назначьте каждому направлению явную ответственность.",
            f"Углублённая задача: укажите, какой мод отвечает за получение, преобразование, хранение, транспорт и управление. Используйте цель интеграции «{profile['integration_ru']}» и задайте буфер между каждой парой модов.",
        ],
    ),
    (
        "recipe_map",
        "Recipe and Gate Map",
        "Карта рецептов и допусков",
        lambda stage, profile: [
            f"The stage controls outputs such as {', '.join(stage['gated_outputs'][:5])}. A difficult recipe is fair only when every ingredient represents already-built infrastructure and the route scales after the first successful batch.",
            f"Deep-dive task: draw the authoritative recipe path, mark reusable permissions and returned tools, list every alternate source, and explain why no later-stage ingredient or circular dependency is required. Supply focus: {profile['supply_en']}",
        ],
        lambda stage, profile: [
            f"Этап контролирует выходы вроде {', '.join(stage['gated_outputs'][:5])}. Сложный рецепт справедлив только тогда, когда каждый ингредиент подтверждает уже построенную инфраструктуру, а путь масштабируется после первой партии.",
            f"Углублённая задача: нарисуйте авторитетный путь рецепта, отметьте многоразовые допуски и возврат инструментов, перечислите альтернативные источники и объясните отсутствие будущих ингредиентов и циклов. Фокус снабжения: {profile['supply_ru']}",
        ],
    ),
    (
        "alternative_architecture",
        "Alternative Architecture",
        "Альтернативная архитектура",
        lambda stage, profile: [
            f"The main branch defines the required capability, not one mandatory block layout. Within Stage {stage['index']}, alternative architectures are valid when they preserve the same inputs, outputs, rate, safety and anti-bypass boundary.",
            f"Deep-dive task: design a second implementation of {profile['process_en']}. Compare footprint, energy or fuel demand, throughput, operator effort and recovery cost without using a cheaper progression shortcut.",
        ],
        lambda stage, profile: [
            f"Основная ветка задаёт требуемую возможность, а не единственную раскладку блоков. На этапе {stage['index']} альтернативная архитектура допустима, если сохраняет входы, выходы, скорость, безопасность и защиту от обходов.",
            f"Углублённая задача: спроектируйте второй вариант процесса «{profile['process_ru']}». Сравните площадь, энергию или топливо, скорость, ручное обслуживание и стоимость восстановления без дешёвого пропуска прогрессии.",
        ],
    ),
    (
        "diagnostic_playbook",
        "Diagnostic Playbook",
        "Справочник диагностики",
        lambda stage, profile: [
            f"A professional installation must explain why it stopped. Stage {stage['index']} should expose readable input, output, reserve and error states instead of requiring blind block replacement.",
            f"Deep-dive task: turn {profile['failure_en']} into a diagnostic decision tree. Include empty input, blocked output, lost power or pressure, unloaded chunks, invalid recipe state and the first safe recovery action.",
        ],
        lambda stage, profile: [
            f"Профессиональная установка должна объяснять причину остановки. Этап {stage['index']} обязан показывать состояние входов, выходов, резерва и ошибки вместо слепой замены блоков.",
            f"Углублённая задача: превратите сценарий «{profile['failure_ru']}» в дерево диагностики. Включите пустой вход, полный выход, потерю энергии или давления, выгруженный чанк, неверный рецепт и первое безопасное действие восстановления.",
        ],
    ),
    (
        "capacity_scaling",
        "Capacity and Scaling",
        "Мощность и масштабирование",
        lambda stage, profile: [
            "Scaling is part of the lesson: the second batch should become faster through parallel machines, larger buffers or better logistics rather than through more repetitive clicking.",
            f"Deep-dive task: measure {profile['measurement_en']}. Calculate the smallest useful buffer, identify the bottleneck at 1x and 4x demand, and define the upgrade that preserves balanced upstream and downstream rates.",
        ],
        lambda stage, profile: [
            "Масштабирование является частью обучения: вторая партия должна ускоряться параллельными машинами, большими буферами или лучшей логистикой, а не дополнительными повторными кликами.",
            f"Углублённая задача: измерьте «{profile['measurement_ru']}». Рассчитайте минимальный полезный буфер, найдите узкое место при спросе 1x и 4x и задайте улучшение, сохраняющее баланс входных и выходных скоростей.",
        ],
    ),
    (
        "expert_extension",
        "Expert Extension Project",
        "Экспертный дополнительный проект",
        lambda stage, profile: [
            f"Complete an optional extension for Stage {stage['index']} that combines at least two of {', '.join(stage['required_domains'])} without replacing the main milestone or granting an early capability.",
            f"Project acceptance: run {profile['automation_en']}; then demonstrate {profile['recovery_en']} and perform the anti-bypass review described by {profile['bypass_en']}. Record one design lesson that should be reused in the next stage.",
        ],
        lambda stage, profile: [
            f"Выполните необязательный дополнительный проект этапа {stage['index']}, объединяющий минимум два направления из списка {', '.join(stage['required_domains'])}, но не заменяющий основной допуск и не открывающий раннюю возможность.",
            f"Приёмка проекта: выполните «{profile['automation_ru']}», затем покажите «{profile['recovery_ru']}» и проведите аудит обходов «{profile['bypass_ru']}». Запишите один принцип, который будет использован на следующем этапе.",
        ],
    ),
)


def matrix_task_block(stage: dict, lesson: dict) -> str:
    task_blocks: list[str] = []
    if lesson.get("milestone_task"):
        item_task_id = matrix.stable_id(
            f"v1_stage_project:item:{stage['id']}:{stage['milestone']}"
        )
        task_blocks.append(
            "\t\t\t{\n"
            f"\t\t\t\tid: \"{item_task_id}\"\n"
            f"\t\t\t\titem: {{ count: 1, id: \"{stage['milestone']}\" }}\n"
            "\t\t\t\ttype: \"item\"\n"
            "\t\t\t}"
        )
    check_id = matrix.stable_id(
        f"v1_stage_project:check:{stage['id']}:{lesson['slug']}"
    )
    task_blocks.append(
        "\t\t\t{\n"
        f"\t\t\t\tid: \"{check_id}\"\n"
        "\t\t\t\ttype: \"checkmark\"\n"
        "\t\t\t}"
    )
    return "[\n" + "\n".join(task_blocks) + "\n\t\t]"


def render_main_stage(
    stage: dict, profile: dict, previous_id: str
) -> tuple[str, str, dict[str, dict[str, str]], str]:
    stage_index = int(stage["index"])
    filename = f"main_stage_{stage_index:02d}_{stage['id']}"
    chapter_id = stable_id(f"chapter:{filename}")
    blocks: list[str] = []
    localization: dict[str, dict[str, str]] = {"en_us": {}, "ru_ru": {}}
    localization["en_us"][f"chapter.{chapter_id}.title"] = json.dumps(
        f"Stage {stage_index:02d} — {stage['title_en']}", ensure_ascii=False
    )
    localization["ru_ru"][f"chapter.{chapter_id}.title"] = json.dumps(
        f"Этап {stage_index:02d} — {stage['title_ru']}", ensure_ascii=False
    )

    current_previous = previous_id
    for sub_index, substage in enumerate(stage["substages"]):
        for lesson_index, (lesson, _, _) in enumerate(spine.LESSON_TYPES):
            quest_id = stable_id(
                f"expert_progression_spine:{stage['id']}:{substage}:{lesson}"
            )
            dependency = (
                f"\n\t\tdependencies: [\"{current_previous}\"]"
                if current_previous
                else ""
            )
            task_namespace = (
                f"expert_progression_spine:{stage['id']}:{substage}:{lesson}"
            )
            x = sub_index * 5.0 + lesson_index * 1.4
            y = sub_index * 3.5
            blocks.append(
                "\t{\n"
                f"\t\tid: \"{quest_id}\"{dependency}\n"
                f"\t\ticon: {{ id: \"{stage['milestone']}\" }}\n"
                f"\t\tshape: \"{'diamond' if lesson == 'acceptance' else 'hexagon'}\"\n"
                f"\t\ttasks: {spine.task_block(task_namespace, None)}\n"
                f"\t\tx: {x:.1f}d\n"
                f"\t\ty: {y:.1f}d\n"
                "\t}"
            )
            title_en, desc_en, title_ru, desc_ru = spine.descriptions(
                stage, substage, lesson
            )
            localization["en_us"][f"quest.{quest_id}.title"] = json.dumps(
                title_en, ensure_ascii=False
            )
            localization["en_us"][f"quest.{quest_id}.quest_desc"] = format_array(
                desc_en
            )
            localization["ru_ru"][f"quest.{quest_id}.title"] = json.dumps(
                title_ru, ensure_ascii=False
            )
            localization["ru_ru"][f"quest.{quest_id}.quest_desc"] = format_array(
                desc_ru
            )
            current_previous = quest_id

    for lesson_index, lesson in enumerate(matrix.LESSONS):
        quest_id = matrix.stable_id(
            f"v1_stage_project:{stage['id']}:{lesson['slug']}"
        )
        dependency = f"\n\t\tdependencies: [\"{current_previous}\"]"
        x = lesson_index % 5 * 4.0
        y = 18.0 + lesson_index // 5 * 4.0
        blocks.append(
            "\t{\n"
            f"\t\tid: \"{quest_id}\"{dependency}\n"
            f"\t\ticon: {{ id: \"{stage['milestone']}\" }}\n"
            f"\t\tshape: \"{'diamond' if lesson.get('milestone_task') else 'hexagon'}\"\n"
            f"\t\ttasks: {matrix_task_block(stage, lesson)}\n"
            f"\t\tx: {x:.1f}d\n"
            f"\t\ty: {y:.1f}d\n"
            "\t}"
        )
        localization["en_us"][f"quest.{quest_id}.title"] = json.dumps(
            f"{stage_index}. {stage['title_en']} — {lesson['title_en']}",
            ensure_ascii=False,
        )
        localization["ru_ru"][f"quest.{quest_id}.title"] = json.dumps(
            f"{stage_index}. {stage['title_ru']} — {lesson['title_ru']}",
            ensure_ascii=False,
        )
        localization["en_us"][f"quest.{quest_id}.quest_desc"] = format_array(
            lesson["desc_en"](stage, profile)
        )
        localization["ru_ru"][f"quest.{quest_id}.quest_desc"] = format_array(
            lesson["desc_ru"](stage, profile)
        )
        current_previous = quest_id

    chapter = (
        "{\n"
        "\tdefault_hide_dependency_lines: false\n"
        "\tdefault_quest_shape: \"hexagon\"\n"
        f"\tfilename: \"{filename}\"\n"
        f"\tgroup: \"{MAIN_GROUP_ID}\"\n"
        f"\ticon: {{ id: \"{stage['milestone']}\" }}\n"
        f"\tid: \"{chapter_id}\"\n"
        f"\torder_index: {stage_index}\n"
        "\tprogression_mode: \"linear\"\n"
        "\tquest_links: []\n"
        "\tquests: [\n"
        + "\n".join(blocks)
        + "\n\t]\n}\n"
    )
    return filename, current_previous, localization, chapter


def render_annex(
    stage: dict, profile: dict, entry_quest: str
) -> tuple[str, dict[str, dict[str, str]], str]:
    stage_index = int(stage["index"])
    filename = f"stage_annex_{stage_index:02d}_{stage['id']}"
    chapter_id = stable_id(f"chapter:{filename}")
    localization: dict[str, dict[str, str]] = {"en_us": {}, "ru_ru": {}}
    localization["en_us"][f"chapter.{chapter_id}.title"] = json.dumps(
        f"Stage {stage_index:02d} Annex — {stage['title_en']}", ensure_ascii=False
    )
    localization["ru_ru"][f"chapter.{chapter_id}.title"] = json.dumps(
        f"Приложение этапа {stage_index:02d} — {stage['title_ru']}", ensure_ascii=False
    )
    blocks: list[str] = []
    previous = entry_quest
    for index, (slug, title_en, title_ru, en_fn, ru_fn) in enumerate(ANNEX_LESSONS):
        quest_id = stable_id(f"stage_annex:{stage['id']}:{slug}")
        task_id = stable_id(f"stage_annex:task:{stage['id']}:{slug}")
        blocks.append(
            "\t{\n"
            f"\t\tdependencies: [\"{previous}\"]\n"
            f"\t\ticon: {{ id: \"{stage['milestone']}\" }}\n"
            f"\t\tid: \"{quest_id}\"\n"
            "\t\toptional: true\n"
            "\t\tshape: \"hexagon\"\n"
            "\t\ttasks: [{\n"
            f"\t\t\tid: \"{task_id}\"\n"
            "\t\t\ttype: \"checkmark\"\n"
            "\t\t}]\n"
            f"\t\tx: {index * 3.0:.1f}d\n"
            "\t\ty: 0.0d\n"
            "\t}"
        )
        localization["en_us"][f"quest.{quest_id}.title"] = json.dumps(
            title_en, ensure_ascii=False
        )
        localization["ru_ru"][f"quest.{quest_id}.title"] = json.dumps(
            title_ru, ensure_ascii=False
        )
        localization["en_us"][f"quest.{quest_id}.quest_desc"] = format_array(
            en_fn(stage, profile)
        )
        localization["ru_ru"][f"quest.{quest_id}.quest_desc"] = format_array(
            ru_fn(stage, profile)
        )
        previous = quest_id

    chapter = (
        "{\n"
        "\tdefault_hide_dependency_lines: false\n"
        "\tdefault_quest_shape: \"hexagon\"\n"
        f"\tfilename: \"{filename}\"\n"
        f"\tgroup: \"{ANNEX_GROUP_ID}\"\n"
        f"\ticon: {{ id: \"{stage['milestone']}\" }}\n"
        f"\tid: \"{chapter_id}\"\n"
        f"\torder_index: {stage_index}\n"
        "\tprogression_mode: \"flexible\"\n"
        "\tquest_links: []\n"
        "\tquests: [\n"
        + "\n".join(blocks)
        + "\n\t]\n}\n"
    )
    return filename, localization, chapter


def merge_localization(
    target: dict[str, dict[str, str]], source: dict[str, dict[str, str]]
) -> None:
    for locale in ("en_us", "ru_ru"):
        target[locale].update(source[locale])


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    profile_doc = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    profiles = profile_doc["profiles"]
    stages = contract["stages"]
    if len(stages) != 18:
        raise RuntimeError(f"Expected 18 stages, found {len(stages)}")

    localization: dict[str, dict[str, str]] = {"en_us": {}, "ru_ru": {}}
    localization["en_us"][f"chapter_group.{MAIN_GROUP_ID}.title"] = json.dumps(
        "v1 Main Progression — 18 Stages", ensure_ascii=False
    )
    localization["ru_ru"][f"chapter_group.{MAIN_GROUP_ID}.title"] = json.dumps(
        "Основная прогрессия v1 — 18 этапов", ensure_ascii=False
    )
    localization["en_us"][f"chapter_group.{ANNEX_GROUP_ID}.title"] = json.dumps(
        "Stage Annexes and Advanced Practice", ensure_ascii=False
    )
    localization["ru_ru"][f"chapter_group.{ANNEX_GROUP_ID}.title"] = json.dumps(
        "Приложения этапов и углублённая практика", ensure_ascii=False
    )

    previous_stage_final = ""
    main_count = 0
    annex_count = 0

    for stage in stages:
        profile = profiles.get(stage["id"])
        if profile is None:
            raise RuntimeError(f"Missing progression profile for {stage['id']}")
        first_quest = stable_id(
            f"expert_progression_spine:{stage['id']}:{stage['substages'][0]}:concept"
        )
        filename, previous_stage_final, stage_localization, chapter = render_main_stage(
            stage, profile, previous_stage_final
        )
        merge_localization(localization, stage_localization)
        (CHAPTER_DIR / f"{filename}.snbt").write_text(
            chapter, encoding="utf-8", newline="\n"
        )
        main_count += 22

        annex_filename, annex_localization, annex_chapter = render_annex(
            stage, profile, first_quest
        )
        merge_localization(localization, annex_localization)
        (CHAPTER_DIR / f"{annex_filename}.snbt").write_text(
            annex_chapter, encoding="utf-8", newline="\n"
        )
        annex_count += len(ANNEX_LESSONS)

    for legacy in (*LEGACY_CHAPTERS, *LEGACY_REPORTS):
        if legacy.exists():
            legacy.unlink()

    for locale, entries in localization.items():
        path = LANG_DIR / f"{locale}.snbt"
        text = path.read_text(encoding="utf-8")
        for key, value in entries.items():
            text = upsert_localization(text, key, value)
        path.write_text(text, encoding="utf-8", newline="\n")

    print(f"main_stage_chapters: {len(stages)}")
    print(f"main_stage_quests: {main_count}")
    print(f"annex_chapters: {len(stages)}")
    print(f"annex_quests: {annex_count}")
    print(f"organized_stage_quests: {main_count + annex_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
