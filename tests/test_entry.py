"""Tests for the excuse entry: gate, shape, determinism."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / "main.py"


def run_main(out_dir: Path) -> Path:
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=str(out_dir))
    subprocess.run([sys.executable, str(MAIN)], env=env, check=True,
                   capture_output=True, text=True)
    return out_dir / "entry.txt"


class TestEntry(unittest.TestCase):
    def test_one_line_within_gate(self):
        with tempfile.TemporaryDirectory() as td:
            dest = run_main(Path(td))
            text = dest.read_text(encoding="utf-8")
            self.assertTrue(1 <= len(text) <= 200, f"{len(text)} chars")
            self.assertNotIn("\n", text)
            self.assertNotIn("\r", text)
            self.assertTrue(text.strip(), "entry is only whitespace")

    def test_no_trailing_newline_or_blank_line(self):
        with tempfile.TemporaryDirectory() as td:
            dest = run_main(Path(td))
            raw = dest.read_bytes()
            self.assertFalse(raw.endswith(b"\n"), "trailing newline")
            self.assertEqual(raw.decode("utf-8").count("\n"), 0)

    def test_byte_identical_reruns(self):
        with tempfile.TemporaryDirectory() as td:
            a = run_main(Path(td) / "a")
            b = run_main(Path(td) / "b")
            self.assertEqual(a.read_bytes(), b.read_bytes())

    def test_output_mode_readable(self):
        with tempfile.TemporaryDirectory() as td:
            dest = run_main(Path(td))
            self.assertEqual(dest.stat().st_mode & 0o777, 0o644)

    def test_stdlib_only(self):
        src = MAIN.read_text(encoding="utf-8")
        allowed = {"os", "pathlib", "sys"}
        for line in src.splitlines():
            if line.startswith("import ") or line.startswith("from "):
                mod = line.split()[1].split(".")[0]
                self.assertIn(mod, allowed, f"non-stdlib import: {line}")


if __name__ == "__main__":
    unittest.main()
