"""Stdlib-only characterization tests for experimental lexemic rotation."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "experiments" / "lexemic_rotation.py"
spec = importlib.util.spec_from_file_location("lexemic_rotation", SOURCE)
module = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class MusicTransformTests(unittest.TestCase):
    def test_four_distinct_modes_and_involution(self):
        P = module.transform_row(module.ROW, "P")
        R = module.transform_row(module.ROW, "R")
        I = module.transform_row(module.ROW, "I")
        RI = module.transform_row(module.ROW, "RI")
        self.assertEqual(R, tuple(reversed(P)))
        self.assertEqual(RI, tuple(reversed(I)))
        self.assertEqual(module.transform_row(I, "I"), P)
        self.assertEqual({*P}, set(range(12)))
        self.assertEqual(len({P, R, I, RI}), 4)

    def test_invalid_rows_and_modes(self):
        for row, mode in [(tuple(range(11)), "P"), ((0,) * 12, "R"), (module.ROW, "T")]:
            with self.assertRaises(ValueError):
                module.transform_row(row, mode)


class UnicodeLedgerTests(unittest.TestCase):
    def test_40_occurrences_cycle_and_lossless_restore(self):
        original = " ".join(["Sashuric"] * 40)
        annotated, ledger = module.annotate(original, ["Sashuric"])
        self.assertEqual([e.mode for e in ledger if e.mode], ["P", "R", "I", "RI"])
        self.assertEqual([e.plane for e in ledger if e.mode], [0, 1, 2, 0])
        self.assertEqual([e.occurrence for e in ledger if e.mode], [10, 20, 30, 40])
        self.assertIn("Sashuric₁", annotated)
        self.assertEqual(module.restore(annotated, ledger), original)

    def test_preserves_emoji_combining_and_paths(self):
        original = "👩🏽‍🚀 Sashuric sashuric_module.py xSashuric Sashuric/Stem Sashuric\u0301 \u200d ΞΦ\nSashuric"
        annotated, ledger = module.annotate(original, ["Sashuric"])
        self.assertEqual(len(ledger), 2)
        self.assertIn("👩🏽‍🚀", annotated)
        self.assertIn("sashuric_module.py", annotated)
        self.assertEqual(module.restore(annotated, ledger), original)

    def test_no_undeclared_terms_changed(self):
        original = "Fractal Recursive Sashuric\nFractal"
        annotated, ledger = module.annotate(original, ["Fractal"])
        self.assertIn("Recursive Sashuric", annotated)
        self.assertEqual([e.term for e in ledger], ["fractal", "fractal"])
        self.assertEqual(module.restore(annotated, ledger), original)

    def test_provenance_fail_closed(self):
        annotated, ledger = module.annotate("Fractal", ["Fractal"])
        with self.assertRaises(ValueError):
            module.restore(annotated.replace("₁", "₂"), ledger)

    def test_crlf_is_not_normalized_by_cli(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            src, out, ledger = (root / n for n in ("src.txt", "out.txt", "ledger.json"))
            src.write_bytes(b"Sashuric\r\nSashuric\r\n")
            module.main([str(src), "--term", "Sashuric", "--output", str(out), "--ledger", str(ledger)])
            self.assertEqual(out.read_bytes(), "Sashuric₁\r\nSashuric₂\r\n".encode())

    def test_ambiguous_lexeme_fails(self):
        for terms in [[], [""], ["Sashuric", "sashuric"], ["hello world"]]:
            with self.assertRaises(ValueError):
                module.annotate("hello world", terms)

    def test_cli_generates_independent_sidecar(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            src, out, ledger = (root / n for n in ("source.txt", "annotated.txt", "ledger.json"))
            src.write_text("Fractal Fractal\n", encoding="utf-8")
            self.assertEqual(module.main([str(src), "--term", "Fractal", "--output", str(out), "--ledger", str(ledger)]), 0)
            self.assertIn('"format": "omnitag-lexemic-v1"', ledger.read_text(encoding="utf-8"))
            self.assertEqual(out.read_text(encoding="utf-8"), "Fractal₁ Fractal₂\n")
            self.assertEqual(src.read_text(encoding="utf-8"), "Fractal Fractal\n")


if __name__ == "__main__":
    unittest.main()
