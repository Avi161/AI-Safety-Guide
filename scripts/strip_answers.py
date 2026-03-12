#!/usr/bin/env python3
"""
Generate questions-only notebooks from tagged answer notebooks.

Usage:
    python scripts/strip_answers.py [input_dir [output_dir]]

    input_dir  - directory to scan for *.ipynb files  (default: .)
    output_dir - where to write stripped notebooks     (default: questions/)

Cell tag behaviour:
  answer      -> cell is removed entirely.
  answer-code -> lines after the last '# YOUR CODE HERE' comment are removed;
                 outputs and execution count are cleared.
                 If no stub comment exists, the entire cell source is replaced
                 with '# YOUR CODE HERE'.

Text transformation (applied to every markdown cell, no tag required):
  _Your answer: <content>_  ->  _Your answer: _

This covers inline sensemaking answers and reflection cells that mix question
text with a filled-in answer on the same line.
"""
import json
import re
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

    notebooks = sorted(input_dir.rglob("*.ipynb"))
    notebooks = [p for p in notebooks if "questions" not in p.parts]

    if not notebooks:
        print("No notebooks found.")
        return

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

    print(
        f"\nDone. Removed {total_removed} answer cell(s), "
        f"truncated {total_truncated} code cell(s) across {len(notebooks)} notebook(s).\n"
        f"Questions written to: {output_dir.resolve()}"
    )


if __name__ == "__main__":
    main()
