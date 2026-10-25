"""Offline, stdlib-only regression tests for the optional codifier registry."""
import importlib.util
from pathlib import Path
import copy
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "experiments" / "glyph_codifiers.py"
spec = importlib.util.spec_from_file_location("glyph_codifiers", SOURCE)
module = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class CodifierTests(unittest.TestCase):
    def test_registry_is_unique(self):
        self.assertEqual(len(module.check_registry()), len(module.REGISTRY))

    def test_duplicate_id_and_surface_rejected(self):
        e = module.REGISTRY[0]
        for variant in (module.Codifier(e.id, "♜", "x", "x"),
                        module.Codifier("XG.OP.NEW", e.surface, "x", "x")):
            with self.assertRaisesRegex(ValueError, "duplicate"):
                module.check_registry(module.REGISTRY + (variant,))

    def test_forbid_bidi_and_invisible_only(self):
        for surface in ("x\u202e", "\u0301", "\ud800"):
            with self.assertRaises(ValueError):
                module.check_registry((module.Codifier("XG.OP.NEW", surface, "x", "x"),))

    def test_lossless_unicode_nfc_nfd_zwj_pua_and_unknown(self):
        sample = "[Msg⛛{7}] README ↠ OPS ⊗ URL ◌ e\u0301 é 👩🏽‍🚀 \ue000 𓂀\r\n"
        packet = module.encode(sample)
        self.assertEqual(module.restore(packet), sample)
        self.assertEqual(packet["interpretation"], "proposed_not_evidence")
        self.assertIn("e\u0301 é 👩🏽‍🚀 \ue000 𓂀", module.gloss(packet))

    def test_raw_omnitag_syntax_stays_raw(self):
        packet = module.encode("[State⛛{proven}] ⟹ something")
        self.assertEqual(packet["parts"][0]["kind"], "raw")
        self.assertEqual(module.restore(packet), "[State⛛{proven}] ⟹ something")

    def test_greedy_longest_surface(self):
        entries = (module.Codifier("XG.OP.A", "→", "A", "A"),
                   module.Codifier("XG.OP.B", "→→", "B", "B"))
        packet = module.encode("a→→b", entries)
        self.assertEqual(packet["parts"][1]["id"], "XG.OP.B")
        self.assertEqual(module.restore(packet, entries), "a→→b")

    def test_offsets_are_contiguous_codepoints(self):
        p = module.encode("😀⧉↻Ξ")
        self.assertEqual([(x["start"], x["end"]) for x in p["parts"]],
                         [(0, 1), (1, 2), (2, 3), (3, 4)])

    def test_tampering_with_glyph_is_rejected(self):
        p = module.encode("⟹")
        p["parts"][0]["text"] = "↠"
        with self.assertRaisesRegex(ValueError, "mismatch"):
            module.restore(p)

    def test_tampering_with_raw_or_offsets_is_rejected(self):
        p = module.encode("DOC↠OPS")
        altered = copy.deepcopy(p)
        altered["parts"][0]["text"] = "LOG"
        with self.assertRaisesRegex(ValueError, "digest"):
            module.restore(altered)
        altered = copy.deepcopy(p)
        altered["parts"][1]["start"] = 999
        with self.assertRaisesRegex(ValueError, "span"):
            module.restore(altered)

    def test_unknown_part_is_rejected_without_losing_raw_input(self):
        p = module.encode("⚗ unknown")
        self.assertEqual(module.restore(p), "⚗ unknown")
        p["parts"][0]["kind"] = "execute"
        with self.assertRaisesRegex(ValueError, "kind"):
            module.restore(p)

    def test_empty_source(self):
        p = module.encode("")
        self.assertEqual(p["parts"], [])
        self.assertEqual(module.restore(p), "")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            module.encode(None)


if __name__ == "__main__":
    unittest.main()
