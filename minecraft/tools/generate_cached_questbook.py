from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
CONTRACT_PATH = ROOT / "config" / "expert_progression_contract.json"
STATE_PATH = ROOT / "config" / "generated_content_fingerprint.json"


def input_paths() -> list[Path]:
    paths: set[Path] = {
        Path(__file__).resolve(),
        CONTRACT_PATH,
        ROOT / "config" / "progression_project_profiles.json",
        TOOLS / "manual_generator_common.py",
        TOOLS / "generate_organized_stage_questbook.py",
        TOOLS / "generate_stage_workflow_expansions.py",
        TOOLS / "generate_stage_depth_program.py",
        TOOLS / "generate_early_stage_workflow_expansions.py",
        TOOLS / "mid_stage_workflow_profiles.py",
        TOOLS / "advanced_stage_workflow_profiles.py",
        TOOLS / "late_stage_workflow_profiles.py",
        TOOLS / "late_stage_workflow_profiles_corrected.py",
    }
    paths.update((ROOT / "config" / "guide_sources").glob("*.json"))
    paths.update(TOOLS.glob("generate_core_technology_manual*.py"))
    paths.update(TOOLS.glob("generate_stage_*matrix.py"))
    return sorted(path for path in paths if path.is_file())


def fingerprint(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        relative = path.relative_to(ROOT).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def expected_outputs() -> list[Path]:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    outputs = [
        CHAPTER_DIR / f"core_technology_manual_{index}.snbt"
        for index in range(1, 8)
    ]
    for stage in contract["stages"]:
        index = int(stage["index"])
        stage_id = stage["id"]
        outputs.append(CHAPTER_DIR / f"main_stage_{index:02d}_{stage_id}.snbt")
        outputs.append(CHAPTER_DIR / f"stage_annex_{index:02d}_{stage_id}.snbt")
    return outputs


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT.parent, check=True)


def generate() -> None:
    for index in range(1, 8):
        suffix = "" if index == 1 else f"_{index}"
        run([sys.executable, str(TOOLS / f"generate_core_technology_manual{suffix}.py")])
    run([sys.executable, str(TOOLS / "generate_organized_stage_questbook.py")])
    run([sys.executable, str(TOOLS / "generate_stage_workflow_expansions.py")])
    run(
        [
            sys.executable,
            "-c",
            (
                "import sys; sys.path.insert(0, 'minecraft/tools'); "
                "import late_stage_workflow_profiles_corrected; "
                "import generate_stage_depth_program as m; "
                "raise SystemExit(m.main())"
            ),
        ]
    )


def sync_registry() -> None:
    run([sys.executable, str(TOOLS / "sync_curated_guide_registry.py")])


def main() -> int:
    inputs = input_paths()
    current = fingerprint(inputs)
    outputs = expected_outputs()
    missing = [path for path in outputs if not path.is_file()]

    previous = {}
    if STATE_PATH.is_file():
        previous = json.loads(STATE_PATH.read_text(encoding="utf-8"))

    cache_hit = (
        previous.get("schema_version") == 1
        and previous.get("input_fingerprint") == current
        and not missing
    )

    if cache_hit:
        print("questbook_generation: CACHE_HIT")
        print(f"generated_outputs_verified: {len(outputs)}")
    else:
        print("questbook_generation: CACHE_MISS")
        if missing:
            print("missing_generated_outputs: " + ", ".join(
                path.relative_to(ROOT).as_posix() for path in missing
            ))
        generate()
        missing_after = [path for path in outputs if not path.is_file()]
        if missing_after:
            raise RuntimeError(
                "Generation completed without expected outputs: "
                + ", ".join(path.relative_to(ROOT).as_posix() for path in missing_after)
            )
        state = {
            "schema_version": 1,
            "input_fingerprint": current,
            "input_files": [path.relative_to(ROOT).as_posix() for path in inputs],
            "generated_outputs": [path.relative_to(ROOT).as_posix() for path in outputs],
        }
        STATE_PATH.write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(f"generated_outputs_updated: {len(outputs)}")

    # Registry synchronization is cheap and also depends on manifest inventory,
    # so it remains unconditional even when generated chapters are cached.
    sync_registry()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
