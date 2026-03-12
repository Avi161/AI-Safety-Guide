#!/usr/bin/env python3
"""
Generate questions-only notebooks and .py files from tagged answer sources.

Usage:
    python scripts/strip_answers.py [input_dir [output_dir]]

    input_dir  - directory to scan for *.ipynb and *.py files  (default: .)
    output_dir - where to write stripped output                 (default: questions/)

Notebook cell tag behaviour:
  answer      -> cell is removed entirely.
  answer-code -> lines after the last '# YOUR CODE HERE' comment are removed;
                 outputs and execution count are cleared.
                 If no stub comment exists, the entire cell source is replaced
                 with '# YOUR CODE HERE'.

Notebook text transformation (applied to every markdown cell, no tag required):
  _Your answer: <content>_  ->  _Your answer: _

Python file behaviour:
  Lines between '# === ANSWER ===' and '# === END ANSWER ===' (inclusive) are
  removed. Everything outside those markers is kept unchanged.

Extra files copied as-is:
  README.md, requirements.txt
"""
import json
import re
import shutil
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_ANSWER_RE = re.compile(r"_Your answer:.*?(?=_)_", re.DOTALL)


def has_tag(cell: dict, tag: str) -> bool:
    return tag in cell.get("metadata", {}).get("tags", [])


def strip_inline_answers(source: str) -> str:
    """Replace filled '_Your answer: ..._' spans with empty placeholders."""
    return _ANSWER_RE.sub("_Your answer: _", source)


def truncate_at_stub(source: str) -> str:
    """
    Keep every line up to and including the last '# YOUR CODE HERE' line.
    If the stub is absent, replace the entire source with the stub.
    """
    lines = source.splitlines(keepends=True)
    last_stub_idx = None
    for i, line in enumerate(lines):
        if "# YOUR CODE HERE" in line:
            last_stub_idx = i

    if last_stub_idx is None:
        return "# YOUR CODE HERE\n"

    kept = lines[: last_stub_idx + 1]
    # Preserve a trailing newline.
    if kept and not kept[-1].endswith("\n"):
        kept[-1] += "\n"
    return "".join(kept)


# ---------------------------------------------------------------------------
# Per-.py-file processing
# ---------------------------------------------------------------------------

_ANSWER_START = "# === ANSWER ==="
_ANSWER_END = "# === END ANSWER ==="


def strip_py_file(py_path: Path, out_path: Path) -> int:
    """
    Remove answer blocks from a .py file.
    Returns the number of blocks removed.
    """
    lines = py_path.read_text(encoding="utf-8").splitlines(keepends=True)
    out_lines = []
    inside = False
    blocks_removed = 0

    for line in lines:
        stripped = line.strip()
        if stripped == _ANSWER_START:
            inside = True
            blocks_removed += 1
            continue
        if stripped == _ANSWER_END:
            inside = False
            continue
        if not inside:
            out_lines.append(line)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(out_lines), encoding="utf-8")
    return blocks_removed


# ---------------------------------------------------------------------------
# Extra file copying
# ---------------------------------------------------------------------------

_EXTRA_FILES = ("README.md", "requirements.txt")


def copy_extra_files(input_dir: Path, output_dir: Path) -> list[str]:
    """Copy README.md and requirements.txt from input_dir to output_dir if present."""
    copied = []
    for name in _EXTRA_FILES:
        src = input_dir / name
        if src.exists():
            dst = output_dir / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied.append(name)
    return copied


# ---------------------------------------------------------------------------
# Per-notebook processing
# ---------------------------------------------------------------------------

def strip_notebook(nb_path: Path, out_path: Path) -> tuple[int, int]:
    """Return (cells_removed, cells_truncated)."""
    with open(nb_path) as f:
        nb = json.load(f)

    new_cells = []
    removed = 0
    truncated = 0

    for cell in nb["cells"]:
        if has_tag(cell, "answer"):
            removed += 1
            continue

        if has_tag(cell, "answer-code"):
            cell = dict(cell)  # shallow copy — don't mutate the original
            src = "".join(cell["source"])
            cell["source"] = [truncate_at_stub(src)]
            cell["outputs"] = []
            cell["execution_count"] = None
            new_cells.append(cell)
            truncated += 1
            continue

        # No answer tag — keep the cell, but scrub inline answers from markdown.
        if cell["cell_type"] == "markdown":
            src = "".join(cell["source"])
            stripped = strip_inline_answers(src)
            if stripped != src:
                cell = dict(cell)
                cell["source"] = [stripped]

        new_cells.append(cell)

    nb["cells"] = new_cells
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    return removed, truncated


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    input_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("questions")

    # --- Notebooks ---
    notebooks = sorted(input_dir.rglob("*.ipynb"))
    notebooks = [p for p in notebooks if "questions" not in p.parts]

    total_removed = total_truncated = 0
    for nb_path in notebooks:
        rel = nb_path.relative_to(input_dir)
        out_path = output_dir / rel
        removed, truncated = strip_notebook(nb_path, out_path)
        print(
            f"  {rel}  ->  {out_path.relative_to(output_dir.parent)}"
            f"  (-{removed} cells, ~{truncated} truncated)"
        )
        total_removed += removed
        total_truncated += truncated

    if notebooks:
        print(
            f"\nNotebooks: removed {total_removed} answer cell(s), "
            f"truncated {total_truncated} code cell(s) across {len(notebooks)} file(s)."
        )

    # --- Python files (skip scripts/ directory itself) ---
    py_files = sorted(input_dir.rglob("*.py"))
    py_files = [
        p for p in py_files
        if "questions" not in p.parts and "scripts" not in p.parts
    ]

    total_blocks = 0
    for py_path in py_files:
        rel = py_path.relative_to(input_dir)
        out_path = output_dir / rel
        blocks = strip_py_file(py_path, out_path)
        print(f"  {rel}  ->  {out_path.relative_to(output_dir.parent)}  (-{blocks} answer block(s))")
        total_blocks += blocks

    if py_files:
        print(f"\nPython files: removed {total_blocks} answer block(s) across {len(py_files)} file(s).")

    # --- Extra files ---
    # Walk each subdirectory that had notebooks and copy README/requirements
    processed_dirs = {nb.parent for nb in notebooks} | {py.parent for py in py_files}
    all_copied = []
    for src_dir in sorted(processed_dirs):
        rel_dir = src_dir.relative_to(input_dir)
        dst_dir = output_dir / rel_dir
        copied = copy_extra_files(src_dir, dst_dir)
        for name in copied:
            print(f"  {rel_dir / name}  ->  {dst_dir.relative_to(output_dir.parent) / name}  (copied)")
        all_copied.extend(copied)

    if all_copied:
        print(f"\nExtra files copied: {len(all_copied)}")

    print(f"\nQuestions written to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
