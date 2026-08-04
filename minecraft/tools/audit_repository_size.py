from __future__ import annotations

import collections
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = REPO_ROOT / "minecraft" / "docs" / "REPOSITORY_SIZE_AUDIT.md"

IGNORED_PARTS = {".git", ".idea", ".vscode", "__pycache__"}
RUNTIME_PARTS = {
    "logs",
    "crash-reports",
    "saves",
    "world",
    "backups",
    "cache",
    ".cache",
    "screenshots",
}
ARCHIVE_EXTENSIONS = {".jar", ".zip", ".7z", ".rar", ".mrpack"}


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024.0 or unit == "TiB":
            return f"{value:.2f} {unit}"
        value /= 1024.0
    raise AssertionError("unreachable")


def tracked_files() -> list[tuple[Path, int]]:
    files: list[tuple[Path, int]] = []
    for path in REPO_ROOT.rglob("*"):
        relative = path.relative_to(REPO_ROOT)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        if not path.is_file():
            continue
        try:
            files.append((relative, path.stat().st_size))
        except OSError:
            continue
    return files


def main() -> int:
    files = tracked_files()
    total = sum(size for _, size in files)

    by_top_level: collections.Counter[str] = collections.Counter()
    by_extension: collections.Counter[str] = collections.Counter()
    runtime_files: list[tuple[Path, int]] = []
    archives: list[tuple[Path, int]] = []

    for path, size in files:
        top = path.parts[0] if path.parts else "."
        by_top_level[top] += size
        extension = path.suffix.lower() or "[no extension]"
        by_extension[extension] += size
        if any(part in RUNTIME_PARTS for part in path.parts):
            runtime_files.append((path, size))
        if extension in ARCHIVE_EXTENSIONS:
            archives.append((path, size))

    largest = sorted(files, key=lambda entry: entry[1], reverse=True)[:40]
    largest_extensions = by_extension.most_common(20)

    lines = [
        "# Repository Size Audit",
        "",
        "This report is generated deterministically by `minecraft/tools/audit_repository_size.py`.",
        "It measures the checked-out source tree, excluding Git internals and editor caches.",
        "",
        "## Summary",
        "",
        f"- Files: **{len(files):,}**",
        f"- Total checked-out size: **{human_size(total)}**",
        f"- Archive/JAR files: **{len(archives)}** ({human_size(sum(size for _, size in archives))})",
        f"- Runtime-state files in tracked directories: **{len(runtime_files)}** ({human_size(sum(size for _, size in runtime_files))})",
        "",
        "## Top-level directories",
        "",
        "| Path | Size | Share |",
        "|---|---:|---:|",
    ]

    for name, size in by_top_level.most_common():
        share = (size / total * 100.0) if total else 0.0
        lines.append(f"| `{name}` | {human_size(size)} | {share:.2f}% |")

    lines.extend([
        "",
        "## Largest files",
        "",
        "| File | Size |",
        "|---|---:|",
    ])
    for path, size in largest:
        lines.append(f"| `{path.as_posix()}` | {human_size(size)} |")

    lines.extend([
        "",
        "## Largest extension groups",
        "",
        "| Extension | Size |",
        "|---|---:|",
    ])
    for extension, size in largest_extensions:
        lines.append(f"| `{extension}` | {human_size(size)} |")

    lines.extend([
        "",
        "## Tracked archives and mod binaries",
        "",
    ])
    if archives:
        lines.extend(["| File | Size |", "|---|---:|"])
        for path, size in sorted(archives, key=lambda entry: entry[1], reverse=True):
            lines.append(f"| `{path.as_posix()}` | {human_size(size)} |")
    else:
        lines.append("No tracked JAR or archive files were detected.")

    lines.extend([
        "",
        "## Runtime-state files",
        "",
    ])
    if runtime_files:
        lines.extend(["| File | Size |", "|---|---:|"])
        for path, size in sorted(runtime_files, key=lambda entry: entry[1], reverse=True):
            lines.append(f"| `{path.as_posix()}` | {human_size(size)} |")
    else:
        lines.append("No tracked runtime-state files were detected in known runtime directories.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rendered = "\n".join(lines).rstrip() + "\n"
    previous = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else None
    if previous == rendered:
        print("Repository size report unchanged")
        return 0

    OUTPUT.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"Repository size report updated: {human_size(total)} across {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
