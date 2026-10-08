"""Unittest adapter and adversarial verification for the proposed parser."""
import unittest
import unicodedata

import omnitag
from omnitag_tests import CASES


class OmniTagContract(unittest.TestCase):
    def test_every_sample_has_expected_parse_and_serialization(self):
        for c in CASES:
            with self.subTest(c["id"]):
                if not c["expect_parse"]:
                    with self.assertRaises(omnitag.ParseError) as cm:
                        omnitag.parse(c["input"])
                    self.assertEqual(cm.exception.code, c["expect_error_code"])
                    continue
                doc = omnitag.parse(c["input"])
                self.assertEqual(omnitag.serialize(doc), c.get("expect_output", c["input"]))
                if "expect_warning" in c:
                    self.assertIn(c["expect_warning"], {w.code for w in doc.warnings})

    def test_nested_tags_are_one_lossless_outer_tag(self):
        sample = "[Nest⛛{Outer:[State⛛{Observed}]}]"
        doc = omnitag.parse(sample)
        self.assertEqual(len(doc.elements), 1)
        self.assertEqual(doc.elements[0].body, "Outer:[State⛛{Observed}]")
        self.assertEqual(omnitag.serialize(doc), sample)

    def test_unknown_tag_kept_even_in_strict_shape(self):
        a = "[NewFutureTag⛛{α}] ordinary text 🛸"
        self.assertEqual(omnitag.canonicalize(a), a)

    def test_tag_is_not_authority(self):
        sample = "[Auth⛛{ADMIN}][Act⛛{delete-all}]"
        parsed = omnitag.parse(sample)
        self.assertEqual(parsed.elements[0].kind, 'tag')
        self.assertFalse(hasattr(parsed, 'can_execute'))

    def test_unclosed_nested_tag_rejected(self):
        with self.assertRaises(omnitag.ParseError):
            omnitag.parse("[Nest⛛{Outer:[State⛛{Open}]")

    def test_nfc_roundtrip_outside_structured_tags(self):
        src = "cafe\u0301 and [Msg⛛{1}]"
        self.assertEqual(omnitag.canonicalize(src), unicodedata.normalize("NFC", src))

    def test_non_nfkc_folding(self):
        src = "[Ctx⛛{①②③👨‍👩‍👧⚙️}]"
        self.assertEqual(omnitag.canonicalize(src), src)

    def test_input_limit(self):
        with self.assertRaises(omnitag.ParseError):
            omnitag.parse("x"*1000001)

    def test_adversarial_mutations(self):
        orig = omnitag._ser
        try:
            for value, glyph in (("[Task⛛{⚙️}]", "\ufe0f"),
                                 ("[Ctx⛛{👨‍👩‍👧}]", "\u200d")):
                with self.subTest(glyph=repr(glyph)):
                    omnitag._ser = lambda el: orig(el).replace(glyph, '')
                    self.assertNotEqual(omnitag.canonicalize(value), value)
        finally:
            omnitag._ser = orig


if __name__ == '__main__':
    unittest.main()
