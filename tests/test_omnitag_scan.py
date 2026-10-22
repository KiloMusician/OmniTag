"""Regression tests for the opt-in OmniTag scanner."""
import unittest
from scripts.omnitag_scan import scan, split, render_plain

class ScanTests(unittest.TestCase):
    def test_basic(self):
        s = "[Msg⛛{42}] Hello"
        self.assertEqual([(t.name, t.value) for t in scan(s)], [("Msg", "42")])
        self.assertEqual(render_plain(s), " Hello")

    def test_lossless_unicode(self):
        s = "𓂀𝕄ₗₐ⧉𝕕𝕖𝕟𝕔 [Sem⛛{Ψ³}] e\u0301 \ue000"
        self.assertEqual("".join(part for _, part in split(s)), s)
        self.assertEqual(scan(s)[0].value, "Ψ³")

    def test_unknown_tags_survive(self):
        s = "[FutureTag⛛{unrecognized}]"
        self.assertEqual(split(s), [("tag", s)])

    def test_malformed_and_nested_remain_text(self):
        for s in ("[Msg⛛{missing]", "[Nest⛛{[State⛛{Observed}]}]"):
            self.assertEqual("".join(p for _, p in split(s)), s)

    def test_offsets(self):
        s = "😀[Msg⛛{1}]!"
        t = scan(s)[0]
        self.assertEqual(s[t.start:t.end], "[Msg⛛{1}]")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            scan(None)

if __name__ == "__main__":
    unittest.main()
