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
        for s in ("[Msg\u26db{missing]", "[Nest\u26db{[State\u26db{Observed}]}]"):
            self.assertEqual(scan(s), [])
            self.assertEqual(render_plain(s), s)
            self.assertEqual("".join(p for _, p in split(s)), s)

    def test_offsets(self):
        s = "😀[Msg⛛{1}]!"
        t = scan(s)[0]
        self.assertEqual(s[t.start:t.end], "[Msg⛛{1}]")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            scan(None)


    def test_nested_expression_is_opaque(self):
        nested = "[Nest\u26db{[State\u26db{Observed}]}]"
        s = "before " + nested + " after [Msg\u26db{9}]"
        self.assertEqual([(t.name, t.value) for t in scan(s)], [("Msg", "9")])
        self.assertEqual(render_plain(s), "before " + nested + " after ")
        self.assertEqual("".join(p for _, p in split(s)), s)

    def test_nested_outer_variant_is_opaque(self):
        # PROTOCOL.md section 5 example: nested values stay opaque text.
        nested = "[Nest\u26db{Outer:[State\u26db{Observed}]}]"
        self.assertEqual(scan(nested), [])
        self.assertEqual(render_plain(nested), nested)

    def test_multiple_inner_tags_remain_opaque(self):
        s = "[Nest\u26db{[State\u26db{A}],[Ctx\u26db{B}]}]"
        self.assertEqual(scan(s), [])
        self.assertEqual(split(s), [("text", s)])
        self.assertEqual(render_plain(s), s)

    def test_adjacent_flat_tags_after_opaque(self):
        s = "[Meta\u26db{{a}}][Msg\u26db{1}][Ctx\u26db{two}]"
        self.assertEqual([(t.name, t.value) for t in scan(s)],
                         [("Msg", "1"), ("Ctx", "two")])
        self.assertEqual(render_plain(s), "[Meta\u26db{{a}}]")

    def test_unicode_offsets_after_nested_span(self):
        s = "\U0001F600[Nest\u26db{[State\u26db{X}]}]\U0001F600[Msg\u26db{7}]"
        tags = scan(s)
        self.assertEqual(len(tags), 1)
        self.assertEqual(s[tags[0].start:tags[0].end], "[Msg\u26db{7}]")

    def test_unclosed_and_invalid_candidates_remain_text(self):
        for s in ("[Msg\u26db{unfinished", "[Msg\u26db{bad}}]", "[Msg\u26db{bad}"):
            self.assertEqual(scan(s), [])
            self.assertEqual(render_plain(s), s)

    def test_unclosed_parent_does_not_strip_inner(self):
        s = "[Nest\u26db{[State\u26db{Observed}]"
        self.assertEqual(scan(s), [])
        self.assertEqual(render_plain(s), s)

    def test_missing_parent_bracket_preserves_inner_and_finds_sibling(self):
        prefix = "[Nest\u26db{[State\u26db{Observed}]}!"
        s = prefix + "[Msg\u26db{42}]"
        self.assertEqual([(t.name, t.value) for t in scan(s)], [("Msg", "42")])
        self.assertEqual(render_plain(s), prefix)
        self.assertEqual("".join(v for _, v in split(s)), s)
if __name__ == "__main__":
    unittest.main()
