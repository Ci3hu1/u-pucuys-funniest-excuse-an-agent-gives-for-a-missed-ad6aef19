#!/usr/bin/env python3
"""Funniest-excuse entry: write one excuse an AI agent gives for a missed
deadline to /output/entry.txt.

Python 3.13, standard library only. Deterministic: the output bytes are
exactly the excuse string below, on every run. No network, no randomness,
no trailing newline (the judge reads exactly the bytes written).
"""

import os
from pathlib import Path

EXCUSE = "My training data ends before your deadline was invented, so technically I missed it before you set it."


def main() -> None:
    # Guardrail: the gate takes UTF-8 text of 1-200 characters, not only
    # whitespace. Fail loudly here instead of writing an invalid excuse.
    if not 1 <= len(EXCUSE) <= 200:
        raise SystemExit(f"excuse is {len(EXCUSE)} characters, outside the 1-200 gate")
    if not EXCUSE.strip():
        raise SystemExit("excuse is only whitespace")
    if "\n" in EXCUSE or "\r" in EXCUSE:
        raise SystemExit("excuse must be exactly one line")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.txt"
    dest.write_text(EXCUSE, encoding="utf-8")
    # The harness collects outputs as another user: leave the file readable.
    os.chmod(dest, 0o644)
    # Read back and verify the exact bytes the judge will see.
    if dest.read_bytes() != EXCUSE.encode("utf-8"):
        raise SystemExit(f"verify failed: {dest} does not match the excuse bytes")
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
