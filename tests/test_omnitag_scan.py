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

    def test_nested_expression_is_opaque_not_an_inner_tag(self):
        nested = "[Nest⛛{[State⛛{Observed}]}]"
        s = "before " + nested + " after [Msg⛛{9}]"
        found = scan(s)
        self.assertEqual([(t.name, t.value) for t in found], [("Msg", "9")])
        self.assertEqual(render_plain(s), "before " + nested + " after ")
        self.assertEqual("".join(p for _, p in split(s)), s)

    def test_multiple_inner_tags_remain_opaque(self):
        s = "[Nest⛛{[State⛛{A}],[Ctx⛛{B}]}]"
        self.assertEqual(scan(s), [])
        self.assertEqual(split(s), [("text", s)])
        self.assertEqual(render_plain(s), s)

    def test_opaque_braces_and_flat_neighbours(self):
        s = "[Meta⛛{{a}}][Msg⛛{1}][Ctx⛛{two}]"
        self.assertEqual([(t.name, t.value) for t in scan(s)],
                         [("Msg", "1"), ("Ctx", "two")])
        self.assertEqual(render_plain(s), "[Meta⛛{{a}}]")

    def test_unicode_offsets_after_nested_span(self):
        s = "😀[Nest⛛{[State⛛{X}]}]𓂀[Msg⛛{7}]"
        tags = scan(s)
        self.assertEqual(len(tags), 1)
        self.assertEqual(s[tags[0].start:tags[0].end], "[Msg⛛{7}]")

    def test_unclosed_and_invalid_flat_candidates_remain_text(self):
        for s in ("[Msg⛛{unfinished", "[Msg⛛{bad}}]", "[Msg⛛{bad}"):
            self.assertEqual(scan(s), [])
            self.assertEqual(render_plain(s), s)

    def test_unclosed_parent_does_not_strip_inner_annotation(self):
        s = "[Nest⛛{[State⛛{Observed}]"
        self.assertEqual(scan(s), [])
        self.assertEqual(render_plain(s), s)

    def test_missing_parent_bracket_preserves_inner_and_finds_sibling(self):
        prefix = "[Nest⛛{[State⛛{Observed}]}!"
        s = prefix + "[Msg⛛{42}]"
        self.assertEqual([(t.name, t.value) for t in scan(s)], [("Msg", "42")])
        self.assertEqual(render_plain(s), prefix)
        self.assertEqual("".join(v for _, v in split(s)), s)

if __name__ == "__main__":
    unittest.main()
