from __future__ import annotations

from pathlib import Path

from simulation_catalog_common import upgrade_catalog

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_PATH = ROOT / "config" / "ftbquests" / "quests" / "chapters" / "hostile_neural_networks.snbt"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"


def human_name(resource_id: str) -> str:
    return resource_id.split(":", 1)[1].replace("/", " ").replace("_", " ").title()


def content_builder(quest_id: str, resources: list[str]) -> dict[str, tuple[str, list[str]]]:
    paths = [resource.split(":", 1)[1] for resource in resources if ":" in resource]
    display = " / ".join(human_name(resource) for resource in resources[:3]) or f"Neural Checkpoint {quest_id[-4:]}"

    if any("deep_learner" in path for path in paths):
        role_en = "portable model-training controller"
        role_ru = "переносной контроллер обучения моделей"
        focus_en = "model slot limits, legal training kills, learner recovery and separation of first-victory evidence from repeat data"
        focus_ru = "лимиты слотов моделей, разрешённые обучающие убийства, восстановление устройства и отделение первой победы от повторных данных"
    elif any("blank_data_model" in path or path == "data_model" for path in paths):
        role_en = "unbound simulation model"
        role_ru = "непривязанная модель симуляции"
        focus_en = "binding the intended creature, preventing model substitution, requiring the legitimate encounter and blacklisting bosses or signature rewards"
        focus_ru = "привязку нужного существа, запрет подмены модели, требование честной встречи и чёрный список боссов или уникальных наград"
    elif any("sim_chamber" in path or "simulation_chamber" in path for path in paths):
        role_en = "powered prediction simulator"
        role_ru = "энергозависимый симулятор предсказаний"
        focus_en = "energy reserve, matrix supply, model tier, cycle time, failed-input quarantine and a hard stop when output storage is full"
        focus_ru = "резерв энергии, подачу матриц, уровень модели, время цикла, карантин неверных входов и жёсткую остановку при полном выходе"
    elif any("loot_fabricator" in path or "fabricator" in path for path in paths):
        role_en = "prediction-to-loot fabricator"
        role_ru = "фабрикатор лута из предсказаний"
        focus_en = "selected output recipe, prediction ownership, output ratios, unique-drop exclusion and prevention of cross-model recipe contamination"
        focus_ru = "выбранный рецепт выхода, владение предсказаниями, соотношения выхода, запрет уникального лута и защиту от смешивания моделей"
    elif any("prediction_matrix" in path for path in paths):
        role_en = "consumable simulation input"
        role_ru = "расходный вход симуляции"
        focus_en = "sustained matrix production, batch cost, input buffering and the absence of free matrices from quests, loot or EMC"
        focus_ru = "устойчивое производство матриц, стоимость партии, входной буфер и отсутствие бесплатных матриц из квестов, лута или EMC"
    elif any("prediction" in path for path in paths):
        model_resources = [resource for resource in resources if resource.startswith("hostilenetworks:") and "prediction" not in resource]
        model_name = human_name(model_resources[-1]) if model_resources else "selected creature"
        role_en = f"prediction for {model_name}"
        role_ru = f"предсказание для {model_name}"
        focus_en = "model-specific output selection, legal first encounter, simulation cost and explicit exclusion of boss-only, quest-only and capability-granting drops"
        focus_ru = "выбор выхода конкретной модели, честную первую встречу, стоимость симуляции и явный запрет боссового, квестового и дающего возможности лута"
    else:
        role_en = "Hostile Neural Networks integration component"
        role_ru = "компонент интеграции Hostile Neural Networks"
        focus_en = "its real role in training, prediction production or fabrication, the declared stage and every alternative acquisition path"
        focus_ru = "его роль в обучении, производстве предсказаний или фабрикации, заявленный этап и каждый альтернативный путь получения"

    en_desc = [
        f"{display} is a {role_en}. Neural simulation is repeat-production infrastructure, not a substitute for discovering, fighting and understanding the represented creature for the first time.",
        f"Acceptance: verify {focus_en}; complete a representative unattended cycle, record energy, consumables, time and output, and prove that random rewards, model swapping, trades, EMC, Woot, spawners or loot-table shortcuts cannot produce restricted drops early."
    ]
    ru_desc = [
        f"{display} — {role_ru}. Нейросимуляция является инфраструктурой повторного производства, а не заменой первого обнаружения, боя и изучения представленного существа.",
        f"Приёмка: проверьте {focus_ru}; выполните типовой автономный цикл, запишите энергию, расходники, время и выход и исключите ранний ограниченный лут через награды, подмену модели, торговлю, EMC, Woot, спавнеры и обход таблиц лута."
    ]
    return {
        "en_us": (f"{display} — Simulation Legitimacy", en_desc),
        "ru_ru": (f"{display} — легитимность симуляции", ru_desc),
    }


def main() -> int:
    quests, rewards_removed, tasks_added = upgrade_catalog(
        CHAPTER_PATH,
        LANG_DIR,
        "Hostile Neural Networks",
        "hostile_neural_networks",
        content_builder,
    )
    print(f"hostile_neural_networks_quests: {quests}")
    print(f"reward_fields_removed: {rewards_removed}")
    print(f"acceptance_tasks_added: {tasks_added}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
