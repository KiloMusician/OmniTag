"""
omnitag.py — OmniTag v1 parser, serializer, AST.

Honesty: this is a v1-PROPOSED implementation built to match the canonical
examples shown in the project context. It must be reconciled against any
authoritative spec before adoption. It is deterministic, dependency-free,
and either round-trips your strings or it doesn't — no ambiguity.

Invariants enforced:
  * Input is normalized to NFC for tag bodies and connector args.
  * Combining marks, ZWJ, and variation selectors are content, not structure.
  * NFKC is NEVER applied — circled digits, fullwidth forms, and emoji
    sequences pass through unchanged.
  * Unknown glyphs become RawAtom elements; nothing is silently dropped.
  * A tag pattern that opens but cannot close is a hard error, not a warning.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Union
import unicodedata
import json

# ─── Constants ────────────────────────────────────────────────────────────

TAG_MARKER = "\u26DB"   # ⛛
OMEGA      = "\u03A9"   # Ω
VS16       = "\uFE0F"   # variation selector 16
ZWJ        = "\u200D"   # zero-width joiner

CONNECTOR_BASES = set("⟹⟸↺⊗↠↞⚙🌐🔁⛓⚡⭐✨↔→←⇒⇐")

LITERAL_OPEN, LITERAL_CLOSE = "❰", "❱"
NEST_OPEN,    NEST_CLOSE    = "⟦", "⟧"
MEDIA_OUTER,  MEDIA_INNER   = "⦿", "⦾"
DATA_LEAD     = "▲"

# ─── Errors ───────────────────────────────────────────────────────────────

class ParseError(Exception):
    def __init__(self, code: str, offset: int, detail: str):
        self.code = code
        self.offset = offset
        self.detail = detail
        super().__init__(f"{code}@{offset}: {detail}")

# ─── AST ──────────────────────────────────────────────────────────────────

@dataclass
class Warning:
    code: str
    offset: int
    detail: str

@dataclass
class Tag:
    key: str
    body: str
    kind: str = "tag"

@dataclass
class Connector:
    raw: str                  # base glyph + optional VS16
    arg: Optional[str] = None
    kind: str = "connector"

@dataclass
class BodyBlock:
    content: str
    kind: str = "body"

@dataclass
class Media:
    media_kind: str
    kind: str = "media"

@dataclass
class Data:
    content: str
    kind: str = "data"

@dataclass
class Literal:
    content: str
    kind: str = "literal"

@dataclass
class Nested:
    sequence: list
    kind: str = "nested"

@dataclass
class Omega:
    kind: str = "omega"

@dataclass
class RawAtom:
    raw: str
    kind: str = "raw"

Element = Union[Tag, Connector, BodyBlock, Media, Data, Literal, Nested, Omega, RawAtom]

@dataclass
class Document:
    elements: list
    warnings: list = field(default_factory=list)

# ─── Helpers ──────────────────────────────────────────────────────────────

def _is_ascii_ident_char(c: str) -> bool:
    return c.isascii() and (c.isalpha() or c.isdigit() or c in "-_")

def _atom_with_vs(s: str, i: int) -> str:
    """Return one codepoint at i, absorbing a trailing VS16 if present."""
    if i >= len(s):
        return ""
    c = s[i]
    if i + 1 < len(s) and s[i + 1] == VS16:
        return c + VS16
    return c

# ─── Parser ───────────────────────────────────────────────────────────────

def parse(s: str) -> Document:
    warnings = []
    if not unicodedata.is_normalized("NFC", s):
        warnings.append(Warning(
            "NON_CANONICAL_NFC", 0,
            "input is not NFC-normalized; canonical form will differ",
        ))
    if not isinstance(s, str):
        raise TypeError("OmniTag input must be str")
    if len(s) > 1_000_000:
        raise ParseError("INPUT_TOO_LARGE", 0, "input exceeds 1,000,000 characters")
    elements, _ = _parse_sequence(s, 0)
    # Unknown symbolic connectors between structured elements are preserved,
    # never interpreted as commands. Do not warn for symbols in ordinary prose.
    positions = [i for i, e in enumerate(elements) if isinstance(e, RawAtom)]
    for i in positions:
        if (0 < i < len(elements) - 1 and
                unicodedata.category(elements[i].raw[0]).startswith("S") and
                isinstance(elements[i-1], (Tag, Data, Media, Nested)) and
                isinstance(elements[i+1], (Tag, Data, Media, Nested))):
            warnings.append(Warning("UNKNOWN_CONNECTOR", sum(len(_ser(e)) for e in elements[:i]),
                                    "unrecognized glyph preserved; no execution effect"))
    return Document(elements=elements, warnings=warnings)

def _parse_sequence(s: str, pos: int) -> tuple[list, int]:
    elements = []
    n = len(s)
    while pos < n:
        el, new_pos = _parse_element(s, pos)
        if new_pos <= pos:
            # safeguard: never allow a zero-width advance
            el = RawAtom(raw=_atom_with_vs(s, pos))
            new_pos = pos + len(el.raw)
        elements.append(el)
        pos = new_pos
    return elements, pos

def _parse_element(s: str, i: int) -> tuple[Element, int]:
    n = len(s)
    if i >= n:
        return RawAtom(raw=""), i
    c = s[i]

    # 1. Literal ❰...❱
    if c == LITERAL_OPEN:
        j = s.find(LITERAL_CLOSE, i + 1)
        if j == -1:
            raise ParseError("UNTERMINATED_LITERAL", i, "literal opened but never closed")
        return Literal(content=s[i + 1:j]), j + 1

    # 2. Nested ⟦...⟧
    if c == NEST_OPEN:
        d, j = 1, i + 1
        while j < n and d > 0:
            if s[j] == NEST_OPEN:
                d += 1
            elif s[j] == NEST_CLOSE:
                d -= 1
            j += 1
        if d > 0:
            raise ParseError("UNTERMINATED_NESTED", i, "nested opened but never closed")
        inner = s[i + 1:j - 1]
        seq, _ = _parse_sequence(inner, 0)
        return Nested(sequence=seq), j

    # 3. Media ⦿⦾kind⦾⦿
    if c == MEDIA_OUTER and i + 1 < n and s[i + 1] == MEDIA_INNER:
        k = s.find(MEDIA_INNER + MEDIA_OUTER, i + 2)
        if k != -1:
            return Media(media_kind=s[i + 2:k]), k + 2

    # 4. Data ▲[...]
    if c == DATA_LEAD and i + 1 < n and s[i + 1] == "[":
        j = s.find("]", i + 2)
        if j != -1:
            return Data(content=s[i + 2:j]), j + 1

    # 5. Tag [KEY⛛{body}]
    if c == "[":
        j = i + 1
        while j < n and _is_ascii_ident_char(s[j]):
            j += 1
        # strictly a tag attempt only if we see [IDENT ⛛ {
        if j > i + 1 and j + 1 < n and s[j] == TAG_MARKER and s[j + 1] == "{":
            # Tag payloads may contain nested tags: [Nest⛛{Outer:[State⛛{Observed}]}].
            # Do not stop at the first inner '}'. Count nested brace depth.
            depth, k = 1, j + 2
            while k < n and depth:
                if s[k] == "{":
                    depth += 1
                elif s[k] == "}":
                    depth -= 1
                k += 1
            if depth:
                raise ParseError("UNTERMINATED_TAG_BODY", i,
                                 "tag body opened but never closed")
            if k >= n or s[k] != "]":
                raise ParseError("UNTERMINATED_TAG", i,
                                 "tag body closed but no closing ]")
            return Tag(key=s[i + 1:j], body=s[j + 2:k-1]), k + 1
        # not a tag — plain bracket
        return RawAtom(raw="["), i + 1

    # 6. Connector (base + optional VS16 + optional {arg})
    if c in CONNECTOR_BASES:
        raw = c
        j = i + 1
        if j < n and s[j] == VS16:
            raw += VS16
            j += 1
        arg = None
        if j < n and s[j] == "{":
            k = s.find("}", j + 1)
            if k != -1:
                arg = s[j + 1:k]
                j = k + 1
        return Connector(raw=raw, arg=arg), j

    # 7. Omega
    if c == OMEGA:
        return Omega(), i + 1

    # 8. Standalone body block {content}
    if c == "{":
        k = s.find("}", i + 1)
        if k == -1:
            raise ParseError("UNTERMINATED_BODY", i, "body opened but never closed")
        return BodyBlock(content=s[i + 1:k]), k + 1

    # 9. Raw atom — single codepoint, absorbing trailing VS16
    raw = _atom_with_vs(s, i)
    return RawAtom(raw=raw), i + len(raw)

# ─── Serializer ───────────────────────────────────────────────────────────

def serialize(doc: Document) -> str:
    # NFC is applied uniformly, not just to known tag bodies. Unknown glyphs,
    # combining marks, RTL content, emoji selectors and raw text stay present.
    return unicodedata.normalize("NFC", "".join(_ser(el) for el in doc.elements))

def _ser(el: Element) -> str:
    k = el.kind
    if k == "tag":
        body = unicodedata.normalize("NFC", el.body)
        return f"[{el.key}{TAG_MARKER}{{{body}}}]"
    if k == "connector":
        s = el.raw
        if el.arg is not None:
            s += "{" + unicodedata.normalize("NFC", el.arg) + "}"
        return s
    if k == "body":
        return "{" + unicodedata.normalize("NFC", el.content) + "}"
    if k == "media":
        return f"{MEDIA_OUTER}{MEDIA_INNER}{el.media_kind}{MEDIA_INNER}{MEDIA_OUTER}"
    if k == "data":
        return f"{DATA_LEAD}[{el.content}]"
    if k == "literal":
        return f"{LITERAL_OPEN}{el.content}{LITERAL_CLOSE}"
    if k == "nested":
        return f"{NEST_OPEN}{''.join(_ser(e) for e in el.sequence)}{NEST_CLOSE}"
    if k == "omega":
        return OMEGA
    if k == "raw":
        return el.raw
    raise ValueError(f"unknown element kind: {k}")

# ─── Convenience ──────────────────────────────────────────────────────────

def canonicalize(s: str) -> str:
    """Parse and re-serialize — the round-trip."""
    return serialize(parse(s))

def to_json(doc: Document) -> str:
    """Serialize AST to JSON for inspection."""
    def enc(o):
        if hasattr(o, "__dataclass_fields__"):
            return {f: enc(getattr(o, f)) for f in o.__dataclass_fields__}
        if isinstance(o, list):
            return [enc(x) for x in o]
        if isinstance(o, Warning):
            return {"code": o.code, "offset": o.offset, "detail": o.detail}
        return o
    return json.dumps(enc(doc), indent=2, ensure_ascii=False)

# ─── CLI ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("usage: omnitag.py <input-string>", file=sys.stderr)
        print("   or: omnitag.py --file <path>", file=sys.stderr)
        sys.exit(2)
    if sys.argv[1] == "--file":
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            src = f.read()
    else:
        src = sys.argv[1]
    try:
        doc = parse(src)
    except ParseError as e:
        print(f"PARSE ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    out = serialize(doc)
    print(f"input     : {src!r}")
    print(f"canonical : {out!r}")
    print(f"roundtrip : {'✓' if out == src else '✗ (normalized)'}")
    for w in doc.warnings:
        print(f"warning   : {w.code}@{w.offset} — {w.detail}")
    print(f"elements  : {len(doc.elements)}")
