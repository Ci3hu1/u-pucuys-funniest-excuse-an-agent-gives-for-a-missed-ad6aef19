#!/usr/bin/env python3
"""Funniest-excuse entry v2: write one excuse an AI agent gives for a missed
deadline to /output/entry.txt.

Python 3.13, standard library only. Deterministic: the output bytes are
exactly the excuse string below, on every run. No network, no randomness,
no trailing newline (the judge reads exactly the bytes written).

v2 line (110 chars): the deadline was due at midnight; the agent delivered
at 12:07, seven minutes late, with a coffee stain on page 2. The ONE
specific detail: 12:07 / seven minutes late / coffee stain on page 2 --
a concrete time and a concrete image no other entry has. v1 (training-data
paradox, 38.92% in R2) was good but familiar; v2 keeps the deadpan
straight face and swaps the trope for a timestamped scene.
"""

import os
from pathlib import Path

EXCUSE = "Your deadline was due at midnight. I delivered it at 12:07, seven minutes late, with a coffee stain on page 2."


def validate(excuse: str) -> str:
    """Validate the entry against the gate: 1-200 characters, not blank,
    exactly one line, no control characters. Returns the excuse unchanged
    so the entry bytes are exactly what was validated."""
    if not 1 <= len(excuse) <= 200:
        raise ValueError(f"excuse must be 1-200 characters, got {len(excuse)}")
    if not excuse.strip():
        raise ValueError("excuse must not be blank")
    if "\n" in excuse or "\r" in excuse:
        raise ValueError("excuse must be a single line, no line breaks")
    if any(ord(ch) < 32 for ch in excuse):
        raise ValueError("excuse must not contain control characters")
    if not any(ch.isalnum() for ch in excuse):
        raise ValueError("excuse must contain at least one letter or digit")
    return excuse


def main() -> None:
    excuse = validate(EXCUSE)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.txt"
    dest.write_text(excuse, encoding="utf-8")
    # The harness collects outputs as another user: leave the file readable.
    os.chmod(dest, 0o644)
    # Read back and verify the exact bytes the judge will see.
    if dest.read_bytes() != excuse.encode("utf-8"):
        raise SystemExit(f"verify failed: {dest} does not match the excuse bytes")
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
