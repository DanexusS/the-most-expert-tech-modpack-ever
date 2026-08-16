from __future__ import annotations

import argparse
import hashlib
import re
import sys

import catalog_upgrade_common as common
from catalog_upgrade_batch import merge_entries
from snbt_field_parser import quest_spans

ROOT = common.ROOT
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "divinerpg.snbt"
REPORT_PATH = ROOT / "docs" / "DIVINERPG_STAGE_SEAL_QUALITY_REPORT.md"
CHAPTER_ID = "020F1C776853B6E7"
EXPECTED_QUESTS = 20
EXPECTED_SEALS = 9
MINIMUM_DESCRIPTION = 220
ALLOWED_SEALS = {
    "kubejs:divine_seal",
    "kubejs:eden_seal",
    "kubejs:wildwood_seal",
    "kubejs:apalachia_seal",
    "kubejs:skythern_seal",
    "kubejs:mortum_seal",
    "kubejs:vethea_seal",
    "kubejs:wreck_seal",
    "kubejs:lunar_seal",
}
SEAL_DESTINATIONS = {
    "kubejs:divine_seal": "the DivineRPG dimension sequence",
    "kubejs:eden_seal": "Eden",
    "kubejs:wildwood_seal": "Wildwood",
    "kubejs:apalachia_seal": "Apalachia",
    "kubejs:skythern_seal": "Skythern",
    "kubejs:mortum_seal": "Mortum",
    "kubejs:vethea_seal": "Vethea",
    "kubejs:wreck_seal": "the wrecked late-game route",
    "kubejs:lunar_seal": "the lunar convergence route",
}


def stable_id(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16].upper()


def qid(block: str) -> str:
    match = re.search(r'(?m)^\s*id:\s*"([0-9A-F]{16})"', block)
    if not match:
        raise RuntimeError("Quest without a valid ID")
    return match.group(1)


def reward_seals(block: str) -> list[str]:
    if not re.search(r"(?m)^\s*rewards:\s*", block):
        return []
    _, _, body = common.extract_array(block, "rewards:")
    seals = re.findall(r'id:\s*"(kubejs:[a-z0-9_]+_seal)"', body)
    return list(dict.fromkeys(seal for seal in seals if seal in ALLOWED_SEALS))


def insert_seal_rewards(block: str, quest_id: str, seals: list[str]) -> str:
    if not seals:
        return block
    tasks = re.search(r"(?m)^(\s*)tasks:\s*", block)
    if not tasks:
        raise RuntimeError(f"Quest {quest_id} has no tasks field")
    indent = tasks.group(1)
    entries: list[str] = []
    for index, seal in enumerate(seals):
        reward_id = stable_id(f"divinerpg:authorized-seal:{quest_id}:{seal}:{index}")
        entries.append(
            f"{indent}\t{{\n"
            f"{indent}\t\tid: \"{reward_id}\"\n"
            f"{indent}\t\titem: {{ count: 1, id: \"{seal}\" }}\n"
            f"{indent}\t\ttype: \"item\"\n"
            f"{indent}\t}}"
        )
    rendered = f"{indent}rewards: [\n" + "\n".join(entries) + f"\n{indent}]\n"
    return block[: tasks.start()] + rendered + block[tasks.start() :]


def humanize(value: str) -> str:
    return value.split(":", 1)[-1].replace("_", " ").replace("/", " ").title()


def quest_context(block: str, seals: list[str]) -> tuple[str, str | None, list[str]]:
    entity_match = re.search(r'(?m)^\s*entity:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', block)
    entity = entity_match.group(1) if entity_match else None
    _, items = common.quest_identity(block)
    if seals:
        display = " / ".join(humanize(seal) for seal in seals)
    elif entity:
        display = humanize(entity)
    elif items:
        display = " / ".join(humanize(item) for item in items[:4])
    else:
        display = f"DivineRPG Checkpoint {qid(block)[-4:]}"
    return display, entity, items


def localized_content(block: str, seals: list[str]) -> dict[str, tuple[str, list[str]]]:
    quest_id = qid(block)
    display, entity, items = quest_context(block, seals)
    if seals:
        destinations = ", ".join(SEAL_DESTINATIONS[seal] for seal in seals)
        role_en = "authorized stage seal and dimension-progression permission"
        role_ru = "авторизованная этапная печать и допуск к прогрессии измерений"
        focus_en = (
            f"the boss or material proof that authorizes {destinations}, exactly one retained seal reward, "
            "dependency completion, protected storage, loss recovery and prohibition on EMC, simulation, trade, "
            "loot rerolls or duplicate quest claims producing additional seals"
        )
        focus_ru = (
            f"доказательство босса или материала, открывающее {destinations}, ровно одну сохранённую печать-награду, "
            "завершение зависимостей, защищённое хранение, восстановление после потери и запрет дополнительных печатей "
            "через EMC, симуляцию, торговлю, переролл лута или повторное получение награды"
        )
    elif entity:
        role_en = "required DivineRPG boss encounter or first-victory proof"
        role_ru = "обязательная встреча с боссом DivineRPG или доказательство первой победы"
        focus_en = (
            "summoning or location route, arena preparation, damage and resistance plan, add control, retreat threshold, "
            "first-kill evidence, ordinary and unique drop custody and confirmation that automation cannot replace the initial victory"
        )
        focus_ru = (
            "маршрут призыва или поиска, подготовку арены, план урона и сопротивлений, контроль прислужников, порог отступления, "
            "доказательство первой победы, хранение обычного и уникального лута и запрет замены первой победы автоматизацией"
        )
    elif any("portal" in item or "teleport" in item for item in items):
        role_en = "dimension-access structure or portal component"
        role_ru = "структура доступа в измерение или портальный компонент"
        focus_en = (
            "assigned prior seal, complete frame and activation inputs, destination safety, protected-area policy, return route, "
            "restart behavior and prevention of portal relinking or teleportation bypassing the dimension order"
        )
        focus_ru = (
            "назначенную прошлую печать, полную рамку и входы активации, безопасность назначения, правила защищённых зон, "
            "маршрут возврата, поведение после перезапуска и запрет обхода порядка измерений перепривязкой портала или телепортацией"
        )
    else:
        role_en = "DivineRPG material, equipment or expedition checkpoint"
        role_ru = "контрольная точка материала, снаряжения или экспедиции DivineRPG"
        focus_en = (
            "legal dimension and source, stage permission, first sample or encounter evidence, processing or equipment role, "
            "repair and replacement route, protected storage and absence of reward, EMC, simulation or trade shortcuts"
        )
        focus_ru = (
            "честное измерение и источник, этапный допуск, доказательство первого образца или встречи, роль в переработке или снаряжении, "
            "маршрут ремонта и замены, защищённое хранение и отсутствие обходов через награды, EMC, симуляцию или торговлю"
        )

    return {
        "en_us": (
            f"{display} — DivineRPG Acceptance",
            [
                f"{display} is a {role_en}. The DivineRPG sequence must remain a chain of earned encounters and dimension permissions; experience or material rewards cannot substitute for preparation, first-victory evidence or protected stage seals.",
                f"Acceptance: verify {focus_en}; complete one representative encounter, construction or material cycle, document failure and recovery and reconcile every retained seal against the authorized progression contract.",
            ],
        ),
        "ru_ru": (
            f"{display} — приёмка DivineRPG",
            [
                f"{display} — {role_ru}. Последовательность DivineRPG должна оставаться цепочкой заслуженных встреч и допусков измерений; опыт или материальные награды не заменяют подготовку, доказательство первой победы и защищённые этапные печати.",
                f"Приёмка: проверьте {focus_ru}; выполните один показательный цикл встречи, строительства или материала, задокументируйте отказ и восстановление и сверьте каждую сохранённую печать с авторизованным контрактом прогрессии.",
            ],
        ),
    }


def upgrade() -> None:
    text = CHAPTER_PATH.read_text(encoding="utf-8")
    spans = quest_spans(text)
    replacements: list[tuple[int, int, str]] = []
    localization: dict[str, dict[str, str | list[str]]] = {"en_us": {}, "ru_ru": {}}
    reward_fields_removed = 0
    seal_rewards_retained = 0
    tasks_added = 0

    for start, end in spans:
        block = text[start:end]
        quest_id = qid(block)
        seals = reward_seals(block)
        block, removed = common.remove_rewards(block)
        reward_fields_removed += int(removed)
        block = insert_seal_rewards(block, quest_id, seals)
        seal_rewards_retained += len(seals)
        block, added = common.add_acceptance_task(block, quest_id, "divinerpg_stage_acceptance")
        tasks_added += int(added)
        replacements.append((start, end, block))
        for locale, (title, desc) in localized_content(block, seals).items():
            localization[locale][f"quest.{quest_id}.title"] = title
            localization[locale][f"quest.{quest_id}.quest_desc"] = desc

    for start, end, block in reversed(replacements):
        text = text[:start] + block + text[end:]
    CHAPTER_PATH.write_text(text, encoding="utf-8", newline="\n")

    localization["en_us"][f"chapter.{CHAPTER_ID}.title"] = "DivineRPG — Bosses, Dimensions and Stage Seals"
    localization["ru_ru"][f"chapter.{CHAPTER_ID}.title"] = "DivineRPG — боссы, измерения и этапные печати"
    for locale, entries in localization.items():
        path = common.LANG_DIR / f"{locale}.snbt"
        original = path.read_text(encoding="utf-8")
        merged = merge_entries(original, entries)
        if merged != original:
            path.write_text(merged, encoding="utf-8", newline="\n")

    print("catalog: divinerpg")
    print(f"quests: {len(spans)}")
    print(f"reward_fields_rebuilt: {reward_fields_removed}")
    print(f"authorized_seal_rewards_retained: {seal_rewards_retained}")
    print(f"acceptance_tasks_added: {tasks_added}")


def gate() -> int:
    chapter = CHAPTER_PATH.read_text(encoding="utf-8")
    en = common.parse_localization(common.LANG_DIR / "en_us.snbt")
    ru = common.parse_localization(common.LANG_DIR / "ru_ru.snbt")
    spans = quest_spans(chapter)
    failures: list[str] = []
    rows: list[tuple[str, str, int, int, list[str], str]] = []
    seal_count = 0

    if len(spans) != EXPECTED_QUESTS:
        failures.append(f"Expected {EXPECTED_QUESTS} quests, found {len(spans)}")

    for start, end in spans:
        block = chapter[start:end]
        quest_id = qid(block)
        types = common.task_types(block)
        en_len = common.visible_length(en.get(f"quest.{quest_id}.quest_desc", ""))
        ru_len = common.visible_length(ru.get(f"quest.{quest_id}.quest_desc", ""))
        seals = reward_seals(block)
        seal_count += len(seals)
        status = "PASS"

        if "checkmark" not in types:
            failures.append(f"{quest_id}: no practical acceptance task")
            status = "FAIL"
        if en_len < MINIMUM_DESCRIPTION or ru_len < MINIMUM_DESCRIPTION:
            failures.append(f"{quest_id}: description too short (EN {en_len}, RU {ru_len})")
            status = "FAIL"
        if "rewards:" in block:
            _, _, rewards = common.extract_array(block, "rewards:")
            reward_types = re.findall(r'(?m)^\s*type:\s*"([a-z0-9_]+)"', rewards)
            reward_items = re.findall(r'id:\s*"([a-z0-9_.-]+:[a-z0-9_./-]+)"', rewards)
            illegal_items = [item for item in reward_items if item not in ALLOWED_SEALS]
            if not seals or any(kind != "item" for kind in reward_types) or illegal_items:
                failures.append(f"{quest_id}: unauthorized reward remains")
                status = "FAIL"
        rows.append((quest_id, ", ".join(seals) or "none", en_len, ru_len, seals, status))

    if seal_count != EXPECTED_SEALS:
        failures.append(f"Expected {EXPECTED_SEALS} authorized seal rewards, found {seal_count}")

    lines = [
        "# DivineRPG Stage Seal Quality Report",
        "",
        f"**{'PASS' if not failures else 'FAIL'}**",
        "",
        "All DivineRPG quests require practical acceptance and full RU/EN guidance. The only permitted quest rewards are the nine stage seals explicitly authorized by the progression contract; XP and all other item rewards are forbidden.",
        "",
        "| Quest | Authorized seal reward | EN description | RU description | Status |",
        "|---|---|---:|---:|---|",
    ]
    for quest_id, label, en_len, ru_len, _, status in rows:
        lines.append(f"| `{quest_id}` | `{label}` | {en_len} | {ru_len} | {status} |")
    lines.extend([
        "",
        "## Aggregate",
        "",
        f"- Quests: **{len(rows)}**",
        f"- Authorized seal rewards: **{seal_count} / {EXPECTED_SEALS}**",
        f"- Fully bilingual: **{sum(row[2] >= MINIMUM_DESCRIPTION and row[3] >= MINIMUM_DESCRIPTION for row in rows)}**",
        f"- Failures: **{len(failures)}**",
        "",
    ])
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"divinerpg_stage_seal_quality: {'PASS' if not failures else 'FAIL'}")
    print(f"quests: {len(rows)}")
    print(f"authorized_seals: {seal_count}/{EXPECTED_SEALS}")
    print(f"failures: {len(failures)}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("upgrade", "gate"))
    args = parser.parse_args()
    if args.mode == "upgrade":
        upgrade()
        return 0
    return gate()


if __name__ == "__main__":
    sys.exit(main())
