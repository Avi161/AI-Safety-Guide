#!/usr/bin/env python3
"""
Auto-tag answer cells in notebooks.

Tagging convention:
  answer      - Cell is removed entirely in questions version.
                Applied to: <details> solution blocks.
  answer-code - Cell content is truncated at '# YOUR CODE HERE'.
                Applied to: code cells where the stub is followed by actual answer code.

Run this once to bootstrap tags on existing notebooks.
After running, open notebooks in Jupyter to verify/adjust tags manually
(View > Cell Toolbar > Tags).
"""
import json
import sys
from pathlib import Path


def is_stub_line(line: str) -> bool:
    """Lines that are placeholder stubs, not real answers."""
    stripped = line.strip()
    return stripped in ("...", "pass", "") or stripped.startswith("#")


def has_real_answer_after_stub(lines: list[str]) -> bool:
    """Return True if there is non-stub code after a '# YOUR CODE HERE' comment."""
    past_stub = False
    for line in lines:
        if "# YOUR CODE HERE" in line:
            past_stub = True
            continue
        if past_stub and not is_stub_line(line):
            return True
    return False


def add_tag(cell: dict, tag: str) -> None:
    meta = cell.setdefault("metadata", {})
    tags = meta.setdefault("tags", [])
    if tag not in tags:
        tags.append(tag)


def tag_notebook(path: Path) -> int:
    with open(path) as f:
        nb = json.load(f)

    tagged = 0
    for cell in nb["cells"]:
        src = "".join(cell["source"])
        existing_tags = cell.get("metadata", {}).get("tags", [])

        if cell["cell_type"] == "markdown":
            if src.lstrip().startswith("<details>") and "answer" not in existing_tags:
                add_tag(cell, "answer")
                tagged += 1

        elif cell["cell_type"] == "code":
            lines = src.splitlines()
            if (
                "# YOUR CODE HERE" in src
                and has_real_answer_after_stub(lines)
                and "answer-code" not in existing_tags
            ):
                add_tag(cell, "answer-code")
                tagged += 1

    with open(path, "w") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    return tagged


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    notebooks = sorted(root.rglob("*.ipynb"))

    # Skip notebooks already in a questions/ output directory.
    notebooks = [p for p in notebooks if "questions" not in p.parts]

    if not notebooks:
        print("No notebooks found.")
        return

    total = 0
    for nb_path in notebooks:
        n = tag_notebook(nb_path)
        print(f"  {nb_path}: {n} cell(s) tagged")
        total += n

    print(f"\nDone. {total} cell(s) tagged across {len(notebooks)} notebook(s).")
    print(
        "\nNext: open notebooks in Jupyter (View > Cell Toolbar > Tags) to verify and\n"
        "manually add 'answer' tags to any pure-answer code cells that the script\n"
        "could not detect (e.g. cells with no '# YOUR CODE HERE' stub)."
    )


if __name__ == "__main__":
    main()
