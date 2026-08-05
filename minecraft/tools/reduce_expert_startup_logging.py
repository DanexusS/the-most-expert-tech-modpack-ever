from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = (
    "kubejs/server_scripts/expert_recipe_extensions.js",
    "kubejs/server_scripts/expert_recipes.js",
    "kubejs/server_scripts/zz_expert_progression_v1.js",
    "kubejs/server_scripts/zzz_authoritative_stage_paths.js",
    "kubejs/server_scripts/zzzz_infinity_path.js",
    "kubejs/server_scripts/zzzz_stage_order_corrections.js",
    "kubejs/server_scripts/zzzzz_early_stage_component_paths.js",
    "kubejs/server_scripts/zzzzzz_mid_stage_component_paths.js",
    "kubejs/server_scripts/zzzzzzz_late_stage_component_paths.js",
    "kubejs/server_scripts/zzzzzzz_mid_stage_convergence_corrections.js",
    "kubejs/server_scripts/zzzzzzzz_advanced_stage_component_paths.js",
    "kubejs/server_scripts/zzzzzzzz_late_cycle_corrections.js",
    "kubejs/server_scripts/zzzzzzzzz_authoritative_component_corrections.js",
)


def matching_parenthesis(text: str, start: int) -> int:
    depth = 0
    quote: str | None = None
    escaped = False
    line_comment = False
    block_comment = False
    index = start
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if line_comment:
            if char == "\n":
                line_comment = False
            index += 1
            continue
        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 2
                continue
            index += 1
            continue
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            index += 1
            continue
        if char == "/" and next_char == "/":
            line_comment = True
            index += 2
            continue
        if char == "/" and next_char == "*":
            block_comment = True
            index += 2
            continue
        if char in ("'", '"', "`"):
            quote = char
            index += 1
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    raise RuntimeError("Unterminated console.info call")


def remove_info_calls(text: str) -> tuple[str, int]:
    marker = "console.info("
    removed = 0
    cursor = 0
    chunks: list[str] = []
    while True:
        start = text.find(marker, cursor)
        if start < 0:
            chunks.append(text[cursor:])
            break

        line_start = text.rfind("\n", 0, start) + 1
        if text[line_start:start].strip():
            raise RuntimeError("console.info must be a standalone statement")
        open_paren = start + len("console.info")
        close_paren = matching_parenthesis(text, open_paren)
        statement_end = close_paren + 1
        while statement_end < len(text) and text[statement_end] in " \t;":
            statement_end += 1
        if statement_end < len(text) and text[statement_end] == "\r":
            statement_end += 1
        if statement_end < len(text) and text[statement_end] == "\n":
            statement_end += 1

        chunks.append(text[cursor:line_start])
        cursor = statement_end
        removed += 1

    return "".join(chunks), removed


def main() -> int:
    total_removed = 0
    changed_files = 0
    for relative in TARGETS:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"Expected expert recipe layer is missing: {relative}")
        text = path.read_text(encoding="utf-8")
        updated, removed = remove_info_calls(text)
        if "console.info(" in updated:
            raise RuntimeError(f"Unremoved console.info call in {relative}")
        total_removed += removed
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed_files += 1

    print(f"expert_startup_info_calls_removed: {total_removed}")
    print(f"expert_startup_files_changed: {changed_files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
