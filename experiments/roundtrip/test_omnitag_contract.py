"""Unittest adapter and adversarial verification for the proposed parser."""
import unittest
import unicodedata
from unittest.mock import patch

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


    def test_unknown_connector_offsets_use_original_input_indices(self):
        # NFC normalization changes codepoint length. Warnings locate input spans,
        # not positions in the canonicalized output.
        src = "cafe\u0301 [Msg⛛{1}]🜁[State⛛{OK}]"
        doc = omnitag.parse(src)
        warnings = [w for w in doc.warnings if w.code == "UNKNOWN_CONNECTOR"]
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0].offset, src.index("🜁"))

    def test_parse_does_not_serialize_every_warning_prefix(self):
        # Regresses quadratic cost: 2000 unknown connectors between tags
        # previously re-serialized all earlier elements for each warning.
        src = "[Msg⛛{1}]🜁[State⛛{OK}]" * 2000
        with patch.object(omnitag, "_ser", side_effect=AssertionError("parser re-serialized AST")):
            doc = omnitag.parse(src)
        self.assertEqual(len([w for w in doc.warnings if w.code == "UNKNOWN_CONNECTOR"]), 2000)

    def test_extreme_nesting_returns_bounded_parse_error(self):
        src = "⟦" * 900 + "[Msg⛛{1}]" + "⟧" * 900
        with self.assertRaises(omnitag.ParseError) as cm:
            omnitag.parse(src)
        self.assertEqual(cm.exception.code, "NESTING_TOO_DEEP")

    def test_modest_nesting_still_roundtrips(self):
        src = "⟦" * 12 + "[Msg⛛{1}]" + "⟧" * 12
        self.assertEqual(omnitag.canonicalize(src), src)

    def test_non_string_input_has_explicit_type_error(self):
        with self.assertRaisesRegex(TypeError, "must be str"):
            omnitag.parse(None)


if __name__ == '__main__':
    unittest.main()
