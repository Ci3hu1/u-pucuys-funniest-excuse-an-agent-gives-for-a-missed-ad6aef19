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


class TestV2Line(unittest.TestCase):
    EXPECTED = "Your deadline was due at midnight. I delivered it at 12:07, seven minutes late, with a coffee stain on page 2."

    def test_v2_line_exact_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            dest = run_main(Path(td))
            self.assertEqual(dest.read_bytes(), self.EXPECTED.encode("utf-8"))

    def test_v2_line_length(self):
        self.assertEqual(len(self.EXPECTED), 110)

    def test_v2_specific_detail(self):
        self.assertIn("12:07", self.EXPECTED)
        self.assertIn("coffee stain on page 2", self.EXPECTED)
        self.assertIn("seven minutes late", self.EXPECTED)

    def test_validate_rejects_punctuation_only(self):
        sys.path.insert(0, str(ROOT))
        import main as entry
        with self.assertRaises(ValueError):
            entry.validate("!!!")


if __name__ == "__main__":
    unittest.main()
