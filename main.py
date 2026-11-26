#!/usr/bin/env python3
"""Entry for the make.fun bounty "The Dog Reviews the Mailman".

The mailman comes every day, smells of other dogs, and has
never once brought a package for the dog. This program is the
review the dog finally leaves: one star, one grudge, and a
promise to bark louder next time. It keeps the line as one
constant, checks it against the gate before writing anything,
and writes it byte-for-byte to entry.txt in the output
directory, with no trailing newline. If the line ever grew
past the gate, the program refuses to write instead of
handing the judge an invalid entry.

The output directory defaults to /output and can be pointed
elsewhere with MAKEFUN_OUTPUT_DIR, which is how the grading
sandbox aims the program at its own folder. The judge then
reads the single line and pairs it against the other dog
reviews, weighing the dog's voice, the mailman's visit, and
the punchline at the end. One star is generous — the mailman
has never once brought the dog anything.
"""

import os
import sys
from pathlib import Path

ENTRY = "One star. He comes every day, smells of other dogs, and has never once brought me a package. Would bark again, louder."

MAX_CHARS = 200


def validate(text: str) -> None:
    """Enforce the gate: 1-200 characters, one line, not only whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry contains control characters")


def write_entry(text: str, out_dir: Path) -> None:
    """Write the validated line to entry.txt, with no trailing newline."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # write_text writes exactly these bytes: no trailing newline added.
    path = out_dir / "entry.txt"
    path.write_text(text, encoding="utf-8")
    # The grader collects outputs as another user: leave it world-readable.
    path.chmod(0o644)


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    text = ENTRY.strip()
    try:
        validate(text)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    write_entry(text, out_dir)
    print(text)
    print(f"wrote entry.txt ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
