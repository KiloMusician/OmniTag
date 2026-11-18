"""Opt-in, lossless scanner for simple OmniTag annotations.

This module does not execute tags or grant authority. Nested values are preserved
as opaque text; malformed fragments remain in the original input.
"""
from dataclasses import dataclass
import re

_SEP = "\u26db"  # tag separator (U+26DB), kept as an escape so this file is ASCII-only
_TAG = re.compile(r"\[([A-Za-z][A-Za-z0-9_-]{0,63})" + re.escape(_SEP) + r"\{([^{}]*)\}\]")
_OPENER = re.compile(r"\[([A-Za-z][A-Za-z0-9_-]{0,63})" + re.escape(_SEP) + r"\{")

@dataclass(frozen=True)
class Tag:
    name: str
    value: str
    start: int
    end: int


def _opener_span_end(text: str, value_start: int) -> int:
    """End (exclusive) of the balanced expression opened at ``value_start``.

    ``value_start`` is the index just after the opener's ``{``. Brace-count
    from there: the span ends just after the ``}`` that balances the opener,
    plus the closing ``]`` when present. An opener whose braces never
    balance owns the rest of the string.
    """
    depth = 1
    i = value_start
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                if i + 1 < n and text[i + 1] == "]":
                    return i + 2
                return i + 1
        i += 1
    return n


def scan(text: str) -> list[Tag]:
    """Find non-nested tags; offsets are Python Unicode codepoint offsets.

    A flat-shaped match is reported only when it is not strictly inside an
    earlier ``[Name SEP {`` opener's balanced span. That keeps a nested
    expression such as ``[Nest SEP {[State SEP {Observed}]}]`` opaque: it
    yields no tags and survives ``render_plain`` verbatim, instead of being
    corrupted into a pseudo-tag by stripping only the inner annotation.
    """
    if not isinstance(text, str):
        raise TypeError("text must be str")
    openers = [(m.start(), m.end()) for m in _OPENER.finditer(text)]
    tags = []
    for m in _TAG.finditer(text):
        start, end = m.start(), m.end()
        inside = False
        for opener_start, value_start in openers:
            if opener_start >= start:
                break
            if _opener_span_end(text, value_start) >= end:
                inside = True
                break
        if not inside:
            tags.append(Tag(m.group(1), m.group(2), start, end))
    return tags

def split(text: str) -> list[tuple[str, str]]:
    """Losslessly split into ('text', fragment) and ('tag', fragment) spans."""
    output = []
    cursor = 0
    for tag in scan(text):
        if tag.start > cursor:
            output.append(("text", text[cursor:tag.start]))
        output.append(("tag", text[tag.start:tag.end]))
        cursor = tag.end
    if cursor < len(text):
        output.append(("text", text[cursor:]))
    return output

def render_plain(text: str) -> str:
    """Remove recognized annotations, preserving all surrounding text verbatim."""
    return "".join(fragment for kind, fragment in split(text) if kind == "text")
