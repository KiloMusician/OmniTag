#!/usr/bin/env python3
"""Byte-faithful, content-minimizing provenance receipts for Unicode archives.

Never transforms, publishes, encrypts or asserts the truth of source text.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

FORMAT = "omnitag.glyph-archive/v1"
REF_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,119}\Z")
MAX_BYTES = 64 * 1024 * 1024


def _is_selector(n: int) -> bool:
    return n in (0xFE0E, 0xFE0F) or 0xE0100 <= n <= 0xE01EF


def _is_observable_special(character: str) -> bool:
    cat = unicodedata.category(character)
    return (_is_selector(ord(character)) or cat == "Cf" or
            (cat == "Cc" and character not in "\r\n\t"))


def build_manifest(raw: bytes, source_ref: str, glyphs: list[str] | tuple[str, ...] = ()) -> dict:
    """Analyze source *bytes*, without losing original Unicode encoding or line endings.

    Entries observe code points, not displayed grapheme clusters or factual claims.
    """
    if len(raw) > MAX_BYTES:
        raise ValueError("source exceeds 64 MiB safety limit")
    if not REF_PATTERN.fullmatch(source_ref):
        raise ValueError("source_ref must be a non-sensitive opaque identifier (1..120 ASCII chars)")
    if len(glyphs) != len(set(glyphs)):
        raise ValueError("duplicate exact glyph sequences")
    if any(not g or len(g) > 64 for g in glyphs):
        raise ValueError("tracked glyph sequences must contain 1..64 code points")
    text = raw.decode("utf-8", errors="strict")
    point_counts = Counter(text)
    tracked = [{"glyph": g, "occurrences": text.count(g)} for g in glyphs]
    specials = []
    for char in sorted((c for c in point_counts if _is_observable_special(c)), key=ord):
        specials.append({"codepoint": f"U+{ord(char):04X}",
                         "name": unicodedata.name(char, "<UNNAMED>"),
                         "category": unicodedata.category(char),
                         "occurrences": point_counts[char]})
    planes = Counter(str(ord(c) >> 16) for c in text)
    crlf = raw.count(b"\r\n")
    return {
        "format": FORMAT,
        "source_ref": source_ref,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "source_bytes": len(raw),
        "utf8_codepoints": len(text),
        "unicode_plane_counts": {k: planes[k] for k in sorted(planes, key=int)},
        "line_endings": {
            "crlf": crlf,
            "lf_only": raw.count(b"\n") - crlf,
            "cr_only": raw.count(b"\r") - crlf,
        },
        "normalization_observations": {
            "nfc_changes_text": unicodedata.normalize("NFC", text) != text,
            "nfkc_changes_text": unicodedata.normalize("NFKC", text) != text,
        },
        "tracked_glyphs": tracked,
        "special_codepoints": specials,
        "authority_effect": "none",
        "verification_scope": "byte_integrity_only_not_truth_or_authenticity",
        "contains_source_text": False,
    }


def capture(source: Path, manifest: Path, source_ref: str, glyphs: list[str]) -> dict:
    if source.resolve() == manifest.resolve():
        raise ValueError("manifest cannot overwrite the source")
    if manifest.exists():
        raise FileExistsError("manifest exists; create a new receipt rather than overwrite history")
    receipt = build_manifest(source.read_bytes(), source_ref, glyphs)
    manifest.write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return receipt


def verify(source: Path, manifest: Path) -> dict:
    doc = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(doc, dict) or doc.get("format") != FORMAT:
        raise ValueError("unsupported manifest format")
    glyph_records = doc.get("tracked_glyphs")
    if not isinstance(glyph_records, list) or any(not isinstance(e, dict) or
            not isinstance(e.get("glyph"), str) for e in glyph_records):
        raise ValueError("invalid glyph records")
    expected = build_manifest(source.read_bytes(), doc["source_ref"], [e["glyph"] for e in glyph_records])
    if expected != doc:
        raise ValueError("archive receipt mismatch; content or metadata changed")
    return doc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("capture", help="capture a receipt; do not rewrite the source")
    create.add_argument("--source", type=Path, required=True)
    create.add_argument("--manifest", type=Path, required=True)
    create.add_argument("--ref", required=True, help="opaque, non-sensitive source identifier")
    create.add_argument("--glyph", action="append", default=[], help="count literal glyph/sequence")
    check = commands.add_parser("verify", help="compare the source bytes to a prior receipt")
    check.add_argument("--source", type=Path, required=True)
    check.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "capture":
            result = capture(args.source, args.manifest, args.ref, args.glyph)
        else:
            result = verify(args.source, args.manifest)
    except (OSError, ValueError, UnicodeError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(f"glyph-archive: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"status": "captured" if args.command == "capture" else "verified",
                      "source_ref": result["source_ref"],
                      "sha256": result["source_sha256"],
                      "bytes": result["source_bytes"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
