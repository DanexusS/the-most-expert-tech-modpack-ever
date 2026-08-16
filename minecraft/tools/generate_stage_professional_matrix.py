from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
PROFILE_PATH = ROOT / "config" / "progression_project_profiles.json"
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "v1_stage_professional_matrix.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
CHAPTER_ID = "E71E3C2F8C5D94A6"

LESSONS = [
    {
        "slug": "capacity_planning",
        "title_en": "Capacity Planning",
        "title_ru": "Планирование мощности",
        "en": lambda stage, p: [
            p["measurement_en"],
            f"Professional acceptance: calculate capacity for twice the current representative load, define the limiting machine or network, and reserve ordinary materials for one expansion of {stage['title_en']}."
        ],
        "ru": lambda stage, p: [
            p["measurement_ru"],
            f"Профессиональная приёмка: рассчитайте мощность для удвоенной типовой нагрузки, определите ограничивающую машину или сеть и зарезервируйте обычные материалы для одного расширения этапа «{stage['title_ru']}»."
        ],
    },
    {
        "slug": "quality_control",
        "title_en": "Quality Control",
        "title_ru": "Контроль качества",
        "en": lambda stage, p: [
            p["process_en"],
            "Professional acceptance: define valid inputs, rejected inputs, expected yield, returned tools or containers and a quarantine path that prevents rare components from entering the wrong recipe."
        ],
        "ru": lambda stage, p: [
            p["process_ru"],
            "Профессиональная приёмка: задайте допустимые и отклоняемые входы, ожидаемый выход, возвращаемые инструменты или контейнеры и карантин, не допускающий редкие компоненты в неверный рецепт."
        ],
    },
    {
        "slug": "observability",
        "title_en": "Observability and Diagnostics",
        "title_ru": "Наблюдаемость и диагностика",
        "en": lambda stage, p: [
            p["failure_en"],
            "Professional acceptance: expose at least three useful indicators—rate, reserve, load, pressure, temperature, channels or blocked state—and make the root cause visible without opening every machine."
        ],
        "ru": lambda stage, p: [
            p["failure_ru"],
            "Профессиональная приёмка: выведите минимум три полезных показателя — скорость, резерв, нагрузку, давление, температуру, каналы или блокировку — и сделайте причину видимой без открытия каждой машины."
        ],
    },
    {
        "slug": "modular_scaling",
        "title_en": "Modular Scaling",
        "title_ru": "Модульное масштабирование",
        "en": lambda stage, p: [
            p["automation_en"],
            f"Professional acceptance: add one parallel production module to {stage['title_en']} with its own input, output and maintenance boundary; throughput must increase without duplicating a gated permission."
        ],
        "ru": lambda stage, p: [
            p["automation_ru"],
            f"Профессиональная приёмка: добавьте один параллельный модуль этапа «{stage['title_ru']}» с собственными границами входа, выхода и обслуживания; выпуск должен вырасти без копирования закрытого допуска."
        ],
    },
    {
        "slug": "redundancy_and_failover",
        "title_en": "Redundancy and Failover",
        "title_ru": "Резервирование и переключение",
        "en": lambda stage, p: [
            p["recovery_en"],
            "Professional acceptance: identify one single point of failure, provide a bounded spare or alternate ordinary path, and prove that failure degrades production safely rather than deleting progress or unique items."
        ],
        "ru": lambda stage, p: [
            p["recovery_ru"],
            "Профессиональная приёмка: найдите одну единственную точку отказа, предусмотрите ограниченный запас или обычный альтернативный путь и докажите безопасное снижение производства без удаления прогресса или уникальных предметов."
        ],
    },
    {
        "slug": "maintenance_standard",
        "title_en": "Maintenance Standard",
        "title_ru": "Стандарт обслуживания",
        "en": lambda stage, p: [
            p["supply_en"],
            "Professional acceptance: label consumables and spares, define inspection or replacement intervals, keep service access clear and document the shutdown order before touching the live system."
        ],
        "ru": lambda stage, p: [
            p["supply_ru"],
            "Профессиональная приёмка: подпишите расходники и запчасти, задайте интервалы проверки или замены, сохраните доступ для обслуживания и задокументируйте порядок остановки до работы с системой."
        ],
    },
    {
        "slug": "ownership_and_permissions",
        "title_en": "Ownership and Permissions",
        "title_ru": "Владение и разрешения",
        "en": lambda stage, p: [
            p["bypass_en"],
            "Professional acceptance: define who may configure, request, teleport, extract or trigger the system; shared multiplayer access must not expose protected reserves, unique proofs or another player's network."
        ],
        "ru": lambda stage, p: [
            p["bypass_ru"],
            "Профессиональная приёмка: задайте, кто может настраивать, запрашивать, телепортироваться, извлекать или запускать систему; общий доступ не должен раскрывать защищённые резервы, уникальные доказательства или чужую сеть."
        ],
    },
    {
        "slug": "professional_certification",
        "title_en": "Professional Certification",
        "title_ru": "Профессиональная сертификация",
        "en": lambda stage, p: [
            f"Certify Stage {stage['index']} — {stage['title_en']} by presenting measured capacity, quality controls, diagnostics, modular expansion, failover, maintenance and permission policy together with the milestone {stage['milestone']}.",
            "Certification is evidence of a maintainable system, not an instruction to consume the milestone repeatedly. Ordinary components must remain reproducible and all bypass controls must still pass after a clean restart."
        ],
        "ru": lambda stage, p: [
            f"Сертифицируйте этап {stage['index']} — «{stage['title_ru']}»: представьте измеренную мощность, контроль качества, диагностику, модульное расширение, переключение, обслуживание и права вместе с допуском {stage['milestone']}.",
            "Сертификация подтверждает обслуживаемую систему и не требует повторного расхода допуска. Обычные компоненты должны воспроизводиться, а все антиобходы — сохраняться после чистого перезапуска."
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
    profiles = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))["profiles"]
    stages = contract["stages"]
    if len(stages) != 18:
        raise RuntimeError(f"Expected 18 stages, found {len(stages)}")

    quest_blocks: list[str] = []
    localization: dict[str, dict[str, str | list[str]]] = {"en_us": {}, "ru_ru": {}}
    previous_id = ""

    for stage_position, stage in enumerate(stages):
        profile = profiles[stage["id"]]
        column = stage_position % 9
        row = stage_position // 9
        for lesson_position, lesson in enumerate(LESSONS):
            quest_id = stable_id(f"v1_stage_professional:{stage['id']}:{lesson['slug']}")
            check_id = stable_id(f"v1_stage_professional:check:{stage['id']}:{lesson['slug']}")
            dependencies = f"\n\t\t\tdependencies: [\"{previous_id}\"]" if previous_id else ""
            tasks = [
                "\t\t\t\t{\n"
                f"\t\t\t\t\tid: \"{check_id}\"\n"
                "\t\t\t\t\ttype: \"checkmark\"\n"
                "\t\t\t\t}"
            ]
            if lesson.get("milestone_task"):
                item_id = stable_id(f"v1_stage_professional:item:{stage['id']}")
                tasks.insert(
                    0,
                    "\t\t\t\t{\n"
                    f"\t\t\t\t\tid: \"{item_id}\"\n"
                    f"\t\t\t\t\titem: {{ count: 1, id: \"{stage['milestone']}\" }}\n"
                    "\t\t\t\t\ttype: \"item\"\n"
                    "\t\t\t\t}",
                )
            x = column * 8.0
            y = row * 21.0 + lesson_position * 2.2
            quest_blocks.append(
                "\t\t{" + dependencies + "\n"
                f"\t\t\ticon: {{ id: \"{stage['milestone']}\" }}\n"
                f"\t\t\tid: \"{quest_id}\"\n"
                "\t\t\tshape: \"gear\"\n"
                "\t\t\ttasks: [\n"
                + "\n".join(tasks)
                + "\n\t\t\t]\n"
                f"\t\t\tx: {x:.1f}d\n"
                f"\t\t\ty: {y:.1f}d\n"
                "\t\t}"
            )
            localization["en_us"][f"quest.{quest_id}.title"] = f"{stage['index']}. {stage['title_en']} — {lesson['title_en']}"
            localization["ru_ru"][f"quest.{quest_id}.title"] = f"{stage['index']}. {stage['title_ru']} — {lesson['title_ru']}"
            localization["en_us"][f"quest.{quest_id}.quest_desc"] = lesson["en"](stage, profile)
            localization["ru_ru"][f"quest.{quest_id}.quest_desc"] = lesson["ru"](stage, profile)
            previous_id = quest_id

    chapter = (
        "{\n"
        "\tdefault_hide_dependency_lines: false\n"
        "\tdefault_quest_shape: \"gear\"\n"
        "\tfilename: \"v1_stage_professional_matrix\"\n"
        "\tgroup: \"177A10C99EDDA376\"\n"
        "\ticon: { id: \"kubejs:creative_convergence_matrix\" }\n"
        f"\tid: \"{CHAPTER_ID}\"\n"
        "\torder_index: 2\n"
        "\tprogression_mode: \"linear\"\n"
        "\tquest_links: []\n"
        "\tquests: [\n"
        + "\n".join(quest_blocks)
        + "\n\t]\n}\n"
    )
    previous = CHAPTER_PATH.read_text(encoding="utf-8") if CHAPTER_PATH.exists() else ""
    if chapter != previous:
        CHAPTER_PATH.write_text(chapter, encoding="utf-8", newline="\n")

    for locale, entries in localization.items():
        path = LANG_DIR / f"{locale}.snbt"
        text = path.read_text(encoding="utf-8")
        original = text
        text = upsert(
            text,
            f"chapter.{CHAPTER_ID}.title",
            "v1 Professional Stage Certification" if locale == "en_us" else "Профессиональная сертификация этапов v1",
        )
        for key, value in entries.items():
            text = upsert(text, key, value)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")

    print(f"professional_stages: {len(stages)}")
    print(f"professional_quests: {len(quest_blocks)}")
    print(f"final_quest: {previous_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
