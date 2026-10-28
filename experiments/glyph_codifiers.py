"""Opt-in, source-preserving glyph codifier experiment. No action authority."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
import unicodedata

FORMAT = "omnitag-glyph-codifiers/v1"
_ID = re.compile(r"^XG\.[A-Z][A-Z0-9_]*\.[A-Z][A-Z0-9_]*$")
_BIDI = set("\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069")


@dataclass(frozen=True)
class Codifier:
    id: str
    surface: str
    gloss: str
    fallback: str


# Provisional, project-scoped readings, NOT facts decoded from StockLens.
REGISTRY = (
    Codifier("XG.FRM.PACKET", "⧉", "packet boundary", "<packet>"),
    Codifier("XG.FRM.CONTEXT", "⧠", "context frame", "<context>"),
    Codifier("XG.FRM.SCOPE", "∷", "namespace separator", "::"),
    Codifier("XG.OP.ROUTE", "↠", "routed flow", "->route"),
    Codifier("XG.OP.TRANSFORM", "⟹", "proposed transformation", "=>"),
    Codifier("XG.OP.BIND", "⊗", "cross-link", "*bind*"),
    Codifier("XG.OP.MERGE", "⊕", "merge", "+"),
    Codifier("XG.OP.REVISIT", "↻", "revisit or iterate", "~again"),
    Codifier("XG.OP.OBSERVE", "⊚", "observe or sample", "observe"),
    Codifier("XG.STATE.PARTIAL", "◍", "partial state", "partial"),
    Codifier("XG.STATE.UNKNOWN", "◌", "unknown state", "unknown"),
    Codifier("XG.META.NOISE", "⌁", "uncertain rendering", "[noise?]"),
    Codifier("XG.META.CHECKPOINT", "⟐", "checkpoint marker", "[checkpoint]"),
)


def check_registry(entries=REGISTRY):
    """Reject ambiguous surfaces/IDs and invisible or bidi-control codifiers."""
    by_id, by_surface = {}, {}
    for entry in entries:
        if not all(isinstance(v, str) and v for v in
                   (entry.id, entry.surface, entry.gloss, entry.fallback)):
            raise ValueError("codifier fields must be nonempty strings")
        if not _ID.fullmatch(entry.id):
            raise ValueError("invalid codifier ID")
        if entry.id in by_id or entry.surface in by_surface:
            raise ValueError("duplicate codifier ID or surface")
        if any(c in _BIDI or unicodedata.category(c) == "Cs" for c in entry.surface):
            raise ValueError("unsafe Unicode in codifier surface")
        if all(unicodedata.category(c)[0] in "CM" for c in entry.surface):
            raise ValueError("invisible-only glyph codifier")
        by_id[entry.id] = entry
        by_surface[entry.surface] = entry
    return by_id


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def encode(source, entries=REGISTRY):
    """Greedy exact-surface scan; preserve every unmatched code point verbatim.

    Offsets count Python code points, NOT UTF-8 bytes or grapheme clusters.
    Input is NEVER normalized, including NFC/NFD, ZWJ and PUA sequences.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")
    check_registry(entries)
    sorted_entries = sorted(entries, key=lambda e: (-len(e.surface), e.id))
    parts = []
    raw_start = i = 0
    while i < len(source):
        entry = next((e for e in sorted_entries if source.startswith(e.surface, i)), None)
        if entry is None:
            i += 1
            continue
        if raw_start < i:
            parts.append({"kind": "raw", "text": source[raw_start:i],
                          "start": raw_start, "end": i})
        end = i + len(entry.surface)
        parts.append({"kind": "glyph", "id": entry.id, "text": entry.surface,
                      "start": i, "end": end})
        i = raw_start = end
    if raw_start < len(source):
        parts.append({"kind": "raw", "text": source[raw_start:],
                      "start": raw_start, "end": len(source)})
    return {"format": FORMAT, "source_sha256": digest(source),
            "interpretation": "proposed_not_evidence", "parts": parts}


def restore(packet, entries=REGISTRY):
    """Validate a transcript packet before reconstructing exact source text."""
    by_id = check_registry(entries)
    if packet.get("format") != FORMAT or packet.get("interpretation") != "proposed_not_evidence":
        raise ValueError("unsupported packet format or interpretation")
    cursor, fragments = 0, []
    for part in packet["parts"]:
        value = part["text"]
        if not isinstance(value, str) or part["start"] != cursor or part["end"] != cursor + len(value):
            raise ValueError("non-contiguous or malformed span")
        if part["kind"] == "glyph":
            if part["id"] not in by_id or by_id[part["id"]].surface != value:
                raise ValueError("codifier identity/surface mismatch")
        elif part["kind"] != "raw":
            raise ValueError("unknown part kind")
        fragments.append(value)
        cursor += len(value)
    source = "".join(fragments)
    if digest(source) != packet["source_sha256"]:
        raise ValueError("source digest mismatch")
    return source


def gloss(packet, entries=REGISTRY):
    """Human-facing VIEW; never execute it or confuse it with a translation."""
    restore(packet, entries)
    by_id = check_registry(entries)
    return "".join(by_id[p["id"]].fallback if p["kind"] == "glyph"
                   else p["text"] for p in packet["parts"])


def inspect_unicode(source):
    """Literal scalar inventory; never claim grapheme or linguistic identity.

    This helps distinguish source bytes from rendered glyph appearance.
    No normalization or interpretation is applied to the source.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")
    return {
        "source_sha256": digest(source),
        "nfc_would_change": unicodedata.normalize("NFC", source) != source,
        "nfd_would_change": unicodedata.normalize("NFD", source) != source,
        "scalars": [
            {"offset": i, "codepoint": f"U+{ord(c):04X}",
             "name": unicodedata.name(c, "<unnamed>"),
             "category": unicodedata.category(c),
             "combining_class": unicodedata.combining(c)}
            for i, c in enumerate(source)
        ],
    }
