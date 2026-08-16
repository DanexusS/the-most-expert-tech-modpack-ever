from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
PROFILE_PATH = ROOT / "config" / "progression_project_profiles.json"
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "v1_stage_project_matrix.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
CHAPTER_ID = "A1E5D43186483C5B"

LESSONS = [
    {
        "slug": "entry_contract",
        "title_en": "Entry Contract",
        "title_ru": "Входной контракт",
        "desc_en": lambda stage, p: [
            f"Stage {stage['index']} — {stage['title_en']} begins only after the previous milestone is complete. The required domains are {', '.join(stage['required_domains'])}; none is decorative in the main route.",
            f"Before building new machinery, list the legal inputs, the three most important gated outputs ({', '.join(stage['gated_outputs'][:3])}) and the condition that would make the stage unsafe or premature."
        ],
        "desc_ru": lambda stage, p: [
            f"Этап {stage['index']} — «{stage['title_ru']}» начинается только после завершения предыдущего допуска. Обязательные направления: {', '.join(stage['required_domains'])}; ни одно не является декоративным.",
            f"До постройки новых машин перечислите законные входы, три ключевых закрытых выхода ({', '.join(stage['gated_outputs'][:3])}) и условие, при котором этап станет преждевременным или небезопасным."
        ],
    },
    {
        "slug": "supply_contract",
        "title_en": "Supply Contract",
        "title_ru": "Контракт снабжения",
        "desc_en": lambda stage, p: [p["supply_en"], "Acceptance: inputs have labelled source, minimum and maximum stock, overflow destination and a replacement route that does not depend on a random reward."],
        "desc_ru": lambda stage, p: [p["supply_ru"], "Приёмка: у входов есть подписанный источник, минимальный и максимальный запас, направление переполнения и путь замены без случайной награды."],
    },
    {
        "slug": "core_process",
        "title_en": "Core Process",
        "title_ru": "Основной процесс",
        "desc_en": lambda stage, p: [p["process_en"], "Acceptance: complete three representative cycles, account for every consumed input and returned container or tool, and identify the slowest operation."],
        "desc_ru": lambda stage, p: [p["process_ru"], "Приёмка: выполните три типовых цикла, учтите каждый расходуемый вход и возвращаемый контейнер или инструмент и определите самую медленную операцию."],
    },
    {
        "slug": "cross_mod_interface",
        "title_en": "Cross-Mod Interface",
        "title_ru": "Межмодовый интерфейс",
        "desc_en": lambda stage, p: [p["integration_en"], "Acceptance: document exactly which mod owns each transformation, which buffer separates them and why no circular or later-stage dependency exists."],
        "desc_ru": lambda stage, p: [p["integration_ru"], "Приёмка: задокументируйте, какой мод владеет каждым преобразованием, какой буфер их разделяет и почему нет цикла или зависимости от будущего этапа."],
    },
    {
        "slug": "measurement_and_buffers",
        "title_en": "Measurement and Buffers",
        "title_ru": "Измерения и буферы",
        "desc_en": lambda stage, p: [p["measurement_en"], "Acceptance: write the measured values in the quest notes or an in-game clipboard and size buffers from observed rates rather than guesswork."],
        "desc_ru": lambda stage, p: [p["measurement_ru"], "Приёмка: запишите измеренные значения в заметки квеста или игровой планшет и рассчитайте буферы по наблюдаемой скорости, а не наугад."],
    },
    {
        "slug": "controlled_failure",
        "title_en": "Controlled Failure Test",
        "title_ru": "Контролируемое испытание отказа",
        "desc_en": lambda stage, p: [p["failure_en"], "Acceptance: the failure remains local, no rare input is voided, the reason is visible and the system can be made safe without destroying healthy sections."],
        "desc_ru": lambda stage, p: [p["failure_ru"], "Приёмка: отказ остаётся локальным, редкие входы не уничтожаются, причина видима, а систему можно обезопасить без разрушения исправных секций."],
    },
    {
        "slug": "automation_proof",
        "title_en": "Automation Proof",
        "title_ru": "Доказательство автоматизации",
        "desc_en": lambda stage, p: [p["automation_en"], "Acceptance: run the system unattended for a representative batch, then show that empty input, full output and chunk reload do not create duplication or deadlock."],
        "desc_ru": lambda stage, p: [p["automation_ru"], "Приёмка: выполните типовую партию без вмешательства и покажите, что пустой вход, полный выход и перезагрузка чанка не создают копирование или тупик."],
    },
    {
        "slug": "anti_bypass_audit",
        "title_en": "Anti-Bypass Audit",
        "title_ru": "Аудит обходов",
        "desc_en": lambda stage, p: [p["bypass_en"], "Acceptance: every gated output has one authoritative path or explicitly equivalent paths, zero unauthorized rewards and an explicit policy for EMC, loot, trade and resource simulation."],
        "desc_ru": lambda stage, p: [p["bypass_ru"], "Приёмка: у каждого закрытого выхода есть один авторитетный путь или явно равноценные пути, нет запрещённых наград и заданы правила EMC, лута, торговли и симуляции."],
    },
    {
        "slug": "recovery_and_repeatability",
        "title_en": "Recovery and Repeatability",
        "title_ru": "Восстановление и повторяемость",
        "desc_en": lambda stage, p: [p["recovery_en"], "Acceptance: recovery uses stored ordinary spares and documented state, not administrator commands, creative items or a second copy of a unique permission."],
        "desc_ru": lambda stage, p: [p["recovery_ru"], "Приёмка: восстановление использует сохранённые обычные запчасти и задокументированное состояние, а не команды администратора, creative-предметы или вторую копию уникального допуска."],
    },
    {
        "slug": "stage_acceptance",
        "title_en": "Stage Acceptance",
        "title_ru": "Приёмка этапа",
        "desc_en": lambda stage, p: [
            f"Produce and retain the milestone {stage['milestone']} after completing supply, process, integration, measurement, failure, automation, bypass and recovery checks for {stage['title_en']}.",
            "The milestone proves infrastructure once; it must not become a repeated manual tax. Keep the factory capable of reproducing ordinary consumed components before entering the next stage."
        ],
        "desc_ru": lambda stage, p: [
            f"Получите и сохраните допуск {stage['milestone']} после проверок снабжения, процесса, интеграции, измерений, отказа, автоматизации, обходов и восстановления этапа «{stage['title_ru']}».",
            "Допуск один раз подтверждает инфраструктуру и не должен становиться повторным ручным налогом. До следующего этапа фабрика обязана воспроизводить обычные расходуемые компоненты."
        ],
        "milestone_task": True,
    },
]


def stable_id(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16].upper()


def render(value: str | list[str]) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def upsert(text: str, key: str, value: str | list[str]) -> str:
    rendered = f"\t{key}: {render(value)}\n"
    pattern = re.compile(rf"(?ms)^\t{re.escape(key)}:.*?(?=^\t[A-Za-z0-9_.-]+:|^\}}\s*$)")
    updated, count = pattern.subn(rendered, text, count=1)
    if count:
        return updated
    closing = text.rfind("}")
    if closing < 0:
        raise RuntimeError("Localization file has no closing brace")
    return text[:closing].rstrip() + "\n" + rendered + "}\n"


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    profile_doc = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    profiles = profile_doc["profiles"]
    stages = contract["stages"]
    if len(stages) != 18:
        raise RuntimeError(f"Expected 18 progression stages, found {len(stages)}")
    if len(LESSONS) != int(profile_doc.get("quests_per_stage", 10)):
        raise RuntimeError("Lesson count does not match project profile contract")

    quest_blocks: list[str] = []
    localization: dict[str, dict[str, str | list[str]]] = {"en_us": {}, "ru_ru": {}}
    previous_quest = ""

    for stage_index, stage in enumerate(stages):
        profile = profiles.get(stage["id"])
        if profile is None:
            raise RuntimeError(f"Missing project profile for stage {stage['id']}")
        column = stage_index % 9
        row = stage_index // 9

        for lesson_index, lesson in enumerate(LESSONS):
            quest_id = stable_id(f"v1_stage_project:{stage['id']}:{lesson['slug']}")
            check_id = stable_id(f"v1_stage_project:check:{stage['id']}:{lesson['slug']}")
            dependencies = f"\n\t\t\tdependencies: [\"{previous_quest}\"]" if previous_quest else ""
            task_blocks = [
                "\t\t\t\t{\n"
                f"\t\t\t\t\tid: \"{check_id}\"\n"
                "\t\t\t\t\ttype: \"checkmark\"\n"
                "\t\t\t\t}"
            ]
            if lesson.get("milestone_task"):
                item_task_id = stable_id(f"v1_stage_project:item:{stage['id']}:{stage['milestone']}")
                task_blocks.insert(
                    0,
                    "\t\t\t\t{\n"
                    f"\t\t\t\t\tid: \"{item_task_id}\"\n"
                    f"\t\t\t\t\titem: {{ count: 1, id: \"{stage['milestone']}\" }}\n"
                    "\t\t\t\t\ttype: \"item\"\n"
                    "\t\t\t\t}",
                )

            x = column * 8.0
            y = row * 24.0 + lesson_index * 2.0
            quest_blocks.append(
                "\t\t{" + dependencies + "\n"
                f"\t\t\ticon: {{ id: \"{stage['milestone']}\" }}\n"
                f"\t\t\tid: \"{quest_id}\"\n"
                "\t\t\tshape: \"hexagon\"\n"
                "\t\t\ttasks: [\n"
                + "\n".join(task_blocks)
                + "\n\t\t\t]\n"
                f"\t\t\tx: {x:.1f}d\n"
                f"\t\t\ty: {y:.1f}d\n"
                "\t\t}"
            )

            title_en = f"{stage['index']}. {stage['title_en']} — {lesson['title_en']}"
            title_ru = f"{stage['index']}. {stage['title_ru']} — {lesson['title_ru']}"
            localization["en_us"][f"quest.{quest_id}.title"] = title_en
            localization["ru_ru"][f"quest.{quest_id}.title"] = title_ru
            localization["en_us"][f"quest.{quest_id}.quest_desc"] = lesson["desc_en"](stage, profile)
            localization["ru_ru"][f"quest.{quest_id}.quest_desc"] = lesson["desc_ru"](stage, profile)
            previous_quest = quest_id

    chapter = (
        "{\n"
        "\tdefault_hide_dependency_lines: false\n"
        "\tdefault_quest_shape: \"hexagon\"\n"
        "\tfilename: \"v1_stage_project_matrix\"\n"
        "\tgroup: \"177A10C99EDDA376\"\n"
        "\ticon: { id: \"kubejs:creative_convergence_matrix\" }\n"
        f"\tid: \"{CHAPTER_ID}\"\n"
        "\torder_index: 1\n"
        "\tprogression_mode: \"linear\"\n"
        "\tquest_links: []\n"
        "\tquests: [\n"
        + "\n".join(quest_blocks)
        + "\n\t]\n}\n"
    )
    previous = CHAPTER_PATH.read_text(encoding="utf-8") if CHAPTER_PATH.exists() else ""
    if previous != chapter:
        CHAPTER_PATH.write_text(chapter, encoding="utf-8", newline="\n")

    for locale, entries in localization.items():
        path = LANG_DIR / f"{locale}.snbt"
        text = path.read_text(encoding="utf-8")
        original = text
        text = upsert(
            text,
            f"chapter.{CHAPTER_ID}.title",
            "v1 Stage Project Matrix" if locale == "en_us" else "Проектная матрица этапов v1",
        )
        for key, value in entries.items():
            text = upsert(text, key, value)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")

    print(f"stage_project_stages: {len(stages)}")
    print(f"stage_project_quests: {len(quest_blocks)}")
    print(f"final_quest: {previous_quest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
