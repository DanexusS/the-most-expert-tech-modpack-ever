from __future__ import annotations

from pathlib import Path

from simulation_catalog_common import upgrade_catalog

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "woot.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"


def human_name(resource_id: str) -> str:
    return resource_id.split(":", 1)[1].replace("/", " ").replace("_", " ").title()


def content_builder(quest_id: str, resources: list[str]) -> dict[str, tuple[str, list[str]]]:
    paths = [resource.split(":", 1)[1] for resource in resources if ":" in resource]
    display = " / ".join(human_name(resource) for resource in resources[:4]) or f"Woot Checkpoint {quest_id[-4:]}"

    if any("dye_liquifier" in path or "dye_fluid" in path or "dye_plate" in path for path in paths):
        role_en = "Woot material-preparation step"
        role_ru = "этап подготовки материалов Woot"
        focus_en = "dye input ownership, fluid and plate conversion ratios, batch buffering and the absence of free random material rewards"
        focus_ru = "владение красителями, соотношения жидкости и пластин, буфер партии и отсутствие бесплатных случайных материалов"
    elif any("stygian" in path or "anvil" in path or "hammer" in path for path in paths):
        role_en = "Stygian fabrication component"
        role_ru = "компонент стигийского производства"
        focus_en = "tool return, anvil workflow, material yield, repair stock and the first legitimate source of every rare input"
        focus_ru = "возврат инструмента, процесс наковальни, выход материала, запас ремонта и первый честный источник каждого редкого входа"
    elif any("factory_base" in path or "layout" in path or "factory_ctr" in path or "heart" in path for path in paths):
        role_en = "factory multiblock foundation"
        role_ru = "основа мультиблочной фабрики"
        focus_en = "validated layout, controller and heart placement, tier matching, chunk boundaries, restart state and safe disassembly"
        focus_ru = "проверенную схему, размещение контроллера и сердца, соответствие уровней, границы чанков, состояние после запуска и безопасный разбор"
    elif any("cell" in path or "pylon" in path or "plinth" in path or "factory_connect" in path or path in {"import", "export"} for path in paths):
        role_en = "factory structure or logistics module"
        role_ru = "структурный или логистический модуль фабрики"
        focus_en = "tier compatibility, import and export ownership, item or fluid limits, connection topology and full-output shutdown"
        focus_ru = "совместимость уровня, владение импортом и экспортом, лимиты предметов или жидкостей, топологию соединений и остановку при полном выходе"
    elif any("mob_shard" in path or "fake_spawner" in path for path in paths):
        role_en = "mob identity and capture component"
        role_ru = "компонент идентификации и захвата моба"
        focus_en = "a legitimate first encounter, exact mob identity, boss and unique-drop blacklist, shard ownership and prevention of model substitution"
        focus_ru = "честную первую встречу, точную идентичность моба, чёрный список боссов и уникального лута, владение осколком и запрет подмены модели"
    elif any("infuser" in path for path in paths):
        role_en = "factory material or fluid infuser"
        role_ru = "предметный или жидкостный инфузор фабрики"
        focus_en = "recipe isolation, input ratios, reusable components, byproducts, overflow and recovery from an interrupted infusion"
        focus_ru = "изоляцию рецепта, соотношения входов, многоразовые компоненты, побочные продукты, переполнение и восстановление прерванной инфузии"
    elif any("upgrade" in path for path in paths):
        role_en = "factory capability upgrade"
        role_ru = "улучшение возможностей фабрики"
        focus_en = "compatible tier, power and consumable increase, output-table effect and whether looting, mass or rate invalidates the current stage"
        focus_ru = "совместимый уровень, рост энергии и расходников, влияние на таблицу выхода и соответствие добычи, массы или скорости текущему этапу"
    elif any("creative" in path for path in paths):
        role_en = "creative-class factory component"
        role_ru = "творческий компонент фабрики"
        focus_en = "all endgame convergence requirements, non-renewable permission evidence and exclusion from ordinary recipes, rewards, trades and simulation outputs"
        focus_ru = "все требования финального схождения, невозобновляемое доказательство допуска и исключение из обычных рецептов, наград, торговли и симуляции"
    else:
        role_en = "Woot factory component"
        role_ru = "компонент фабрики Woot"
        focus_en = "its structural or production role, tier, power cost, consumables, output table and all restricted-drop controls"
        focus_ru = "его структурную или производственную роль, уровень, стоимость энергии, расходники, таблицу выхода и контроль ограниченного лута"

    en_desc = [
        f"{display} is a {role_en}. A Woot factory may reproduce ordinary drops after legitimate progression, but it must never replace first discovery, boss mastery or unique capability rewards.",
        f"Acceptance: verify {focus_en}; run a representative bounded batch, record power, consumables, cycle time and output, and prove that random quest rewards, alternate shards, spawner data, EMC, neural models or loot-table aliases cannot automate a restricted encounter."
    ]
    ru_desc = [
        f"{display} — {role_ru}. Фабрика Woot может повторно производить обычный лут после честной прогрессии, но не должна заменять первое обнаружение, освоение босса или уникальные награды-возможности.",
        f"Приёмка: проверьте {focus_ru}; выполните ограниченную типовую партию, запишите энергию, расходники, время и выход и исключите автоматизацию ограниченной встречи через случайные награды, подмену осколка, данные спавнера, EMC, нейромодели и алиасы лута."
    ]
    return {
        "en_us": (f"{display} — Factory Legitimacy", en_desc),
        "ru_ru": (f"{display} — легитимность фабрики", ru_desc),
    }


def main() -> int:
    quests, rewards_removed, tasks_added = upgrade_catalog(
        CHAPTER_PATH,
        LANG_DIR,
        "Woot",
        "woot",
        content_builder,
    )
    print(f"woot_quests: {quests}")
    print(f"reward_fields_removed: {rewards_removed}")
    print(f"acceptance_tasks_added: {tasks_added}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
