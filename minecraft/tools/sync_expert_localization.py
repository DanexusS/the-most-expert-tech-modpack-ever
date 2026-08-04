from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"

ENTRIES = {
    "en_us": {
        "quest.A17E4D09B8C2F101.title": '"Field Engineering Kit"',
        "quest.A17E4D09B8C2F101.quest_desc": '["Build a practical foundation from Immersive Engineering components, copper and glass.", "This branch represents manual fabrication and structural engineering before large-scale automation."]',
        "quest.B29F510AC7D3E202.title": '"Power Regulation Unit"',
        "quest.B29F510AC7D3E202.quest_desc": '["Combine basic electrical control, a Modern Industrialization motor and black quartz.", "This branch teaches that power distribution and motion control are separate from Create mechanics."]',
        "quest.C3A0621BD8E4F303.title": '"Materials Analysis Matrix"',
        "quest.C3A0621BD8E4F303.quest_desc": '["Prepare an analytical matrix from quartz, redstone, glass and a comparator.", "It represents measurement, material classification and precise control before advanced circuits."]',
        "quest.D4B1732CE9F50404.title": '"Industrial Kinetic Interface"',
        "quest.D4B1732CE9F50404.quest_desc": '["Create begins here as a specialized mechanical automation branch, not as the only opening path.", "Join the common mechanical core with andesite technology and an electric motor before constructing the industrial frame."]',
    },
    "ru_ru": {
        "quest.A17E4D09B8C2F101.title": '"Комплект полевого инженера"',
        "quest.A17E4D09B8C2F101.quest_desc": '["Соберите практическую основу из компонентов Immersive Engineering, меди и стекла.", "Эта ветвь отвечает за ручное изготовление и прочные конструкции до появления крупной автоматизации."]',
        "quest.B29F510AC7D3E202.title": '"Блок регулирования энергии"',
        "quest.B29F510AC7D3E202.quest_desc": '["Объедините базовое управление электричеством, мотор Modern Industrialization и чёрный кварц.", "Эта ветвь показывает, что распределение энергии и управление движением не обязаны начинаться с механик Create."]',
        "quest.C3A0621BD8E4F303.title": '"Матрица анализа материалов"',
        "quest.C3A0621BD8E4F303.quest_desc": '["Подготовьте аналитическую матрицу из кварца, редстоуна, стекла и компаратора.", "Она представляет измерение, классификацию материалов и точное управление до сложных электронных схем."]',
        "quest.D4B1732CE9F50404.title": '"Кинетический промышленный интерфейс"',
        "quest.D4B1732CE9F50404.quest_desc": '["Create начинается здесь как отдельная ветвь механической автоматизации, а не как единственный старт сборки.", "Объедините общее механическое ядро с андезитовой технологией и электромотором перед созданием промышленной рамы."]',
    },
}


def format_block(entries: dict[str, str]) -> str:
    return "\n".join(f"\t{key}: {value}" for key, value in entries.items())


def synchronize(locale: str, entries: dict[str, str]) -> bool:
    path = LANG_DIR / f"{locale}.snbt"
    if not path.is_file():
        raise FileNotFoundError(f"Missing FTB Quests localization file: {path}")

    text = path.read_text(encoding="utf-8")
    present = {key for key in entries if f"{key}:" in text}
    if present == set(entries):
        print(f"{locale}: expert quest localization already synchronized")
        return False
    if present:
        missing = sorted(set(entries) - present)
        raise RuntimeError(
            f"{locale}: partial expert localization detected; missing keys: {missing}"
        )

    closing = text.rfind("}")
    if closing < 0 or text[closing + 1 :].strip():
        raise RuntimeError(f"{locale}: localization file has an unexpected ending")

    prefix = text[:closing].rstrip()
    updated = f"{prefix}\n{format_block(entries)}\n}}\n"
    path.write_text(updated, encoding="utf-8", newline="\n")
    print(f"{locale}: added {len(entries)} expert quest localization keys")
    return True


def main() -> int:
    changed = False
    for locale, entries in ENTRIES.items():
        changed = synchronize(locale, entries) or changed
    print("Localization synchronized" if changed else "Localization unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
