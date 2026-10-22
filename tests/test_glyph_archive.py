"""Offline deterministic tests of byte-level glyph receipt contracts."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "experiments" / "glyph_archive.py"
spec = importlib.util.spec_from_file_location("glyph_archive", SOURCE)
glyph_archive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(glyph_archive)


class GlyphArchiveTests(unittest.TestCase):
    def setUp(self):
        self.raw = "[Msg⛛{392}↗️Σ∞]\r\n𓇯𓇯👩🏽‍🚀\n𐒠𞿺\x03 ΞNuSyQ\r".encode("utf-8")

    def test_capture_is_source_byte_preserving_and_multiplane(self):
        receipt = glyph_archive.build_manifest(self.raw, "Msg-392", ["𓇯", "👩🏽‍🚀", "missing"])
        self.assertEqual(receipt["tracked_glyphs"][0]["occurrences"], 2)
        self.assertEqual(receipt["tracked_glyphs"][1]["occurrences"], 1)
        self.assertEqual(receipt["tracked_glyphs"][2]["occurrences"], 0)
        self.assertIn("0", receipt["unicode_plane_counts"])
        self.assertIn("1", receipt["unicode_plane_counts"])
        self.assertEqual(receipt["line_endings"], {"crlf": 1, "lf_only": 1, "cr_only": 1})
        self.assertTrue(any(x["codepoint"] == "U+0003" for x in receipt["special_codepoints"]))
        self.assertTrue(any(x["codepoint"] == "U+200D" for x in receipt["special_codepoints"]))
        self.assertTrue(any(x["codepoint"] == "U+FE0F" for x in receipt["special_codepoints"]))
        self.assertEqual(receipt["verification_scope"], "byte_integrity_only_not_truth_or_authenticity")

    def test_capture_verify_and_unmodified_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, manifest = root / "source.txt", root / "receipt.json"
            source.write_bytes(self.raw)
            original = source.read_bytes()
            created = glyph_archive.capture(source, manifest, "Msg-392", ["𓇯"])
            self.assertEqual(created, glyph_archive.verify(source, manifest))
            self.assertEqual(source.read_bytes(), original)
            self.assertNotIn("ΞNuSyQ", manifest.read_text(encoding="utf-8"))
            self.assertFalse(created["contains_source_text"])

    def test_detect_source_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, manifest = root / "source.txt", root / "receipt.json"
            source.write_bytes(self.raw)
            glyph_archive.capture(source, manifest, "Msg-392", ["𓇯"])
            source.write_bytes(self.raw + b".")
            with self.assertRaisesRegex(ValueError, "mismatch"):
                glyph_archive.verify(source, manifest)

    def test_detect_manifest_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, manifest = root / "source.txt", root / "receipt.json"
            source.write_bytes(self.raw)
            glyph_archive.capture(source, manifest, "Msg-392", ["𓇯"])
            doc = json.loads(manifest.read_text(encoding="utf-8"))
            doc["tracked_glyphs"][0]["occurrences"] = 999
            manifest.write_text(json.dumps(doc), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "mismatch"):
                glyph_archive.verify(source, manifest)

    def test_reject_duplicate_manifest_object_keys(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, manifest = root / "source.txt", root / "receipt.json"
            source.write_bytes(self.raw)
            glyph_archive.capture(source, manifest, "Msg-392", ["𓇯"])
            data = manifest.read_text(encoding="utf-8")
            data = data.replace('"format":', '"format": "malicious", "format":', 1)
            manifest.write_text(data, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate manifest key"):
                glyph_archive.verify(source, manifest)

    def test_invalid_unicode_and_invalid_refs(self):
        for raw in [b"\xff", b"\xed\xa0\x80"]:
            with self.assertRaises(UnicodeDecodeError):
                glyph_archive.build_manifest(raw, "Msg-392")
        for ref in ["", "/private/path", "me@example.com", "x" * 121]:
            with self.assertRaises(ValueError):
                glyph_archive.build_manifest(b"abc", ref)

    def test_nfc_is_observed_not_applied(self):
        decomposed = "e\u0301".encode("utf-8")
        data = glyph_archive.build_manifest(decomposed, "NFC-fixture", ["é", "e\u0301"])
        self.assertTrue(data["normalization_observations"]["nfc_changes_text"])
        self.assertEqual([x["occurrences"] for x in data["tracked_glyphs"]], [0, 1])
        self.assertEqual(data["source_bytes"], len(decomposed))

    def test_manifest_no_overwrites(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, manifest = root / "source.txt", root / "receipt.json"
            source.write_bytes(self.raw)
            with self.assertRaises(ValueError):
                glyph_archive.capture(source, source, "Msg-392", [])
            glyph_archive.capture(source, manifest, "Msg-392", [])
            with self.assertRaises(FileExistsError):
                glyph_archive.capture(source, manifest, "Msg-392", [])

    def test_duplicate_or_empty_glyph_rejected(self):
        for glyphs in [["𓇯", "𓇯"], [""], ["z" * 65]]:
            with self.assertRaises(ValueError):
                glyph_archive.build_manifest(self.raw, "Msg-392", glyphs)

    def test_cli_receipt_round_trip(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, manifest = root / "source.txt", root / "receipt.json"
            source.write_bytes(self.raw)
            capture = subprocess.run([sys.executable, str(SOURCE), "capture", "--source", str(source),
                                      "--manifest", str(manifest), "--ref", "Msg-392", "--glyph", "𓇯"],
                                     capture_output=True, text=True)
            self.assertEqual(capture.returncode, 0, capture.stderr)
            verify = subprocess.run([sys.executable, str(SOURCE), "verify", "--source", str(source),
                                     "--manifest", str(manifest)], capture_output=True, text=True)
            self.assertEqual(verify.returncode, 0, verify.stderr)
            self.assertEqual(json.loads(verify.stdout)["status"], "byte_integrity_verified")

    def test_byte_drift_even_when_normalization_matches(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, manifest = root / "source.txt", root / "receipt.json"
            source.write_bytes("e\u0301".encode())
            glyph_archive.capture(source, manifest, "Diff-fixture", [])
            source.write_bytes("é".encode())
            with self.assertRaisesRegex(ValueError, "mismatch"):
                glyph_archive.verify(source, manifest)

    def test_deterministic_receipts(self):
        a = glyph_archive.build_manifest(self.raw, "Msg-392", ["𓇯"])
        b = glyph_archive.build_manifest(self.raw, "Msg-392", ["𓇯"])
        self.assertEqual(json.dumps(a, ensure_ascii=False, sort_keys=True),
                         json.dumps(b, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
