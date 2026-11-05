"""Opt-in, lossless scanner for simple OmniTag annotations.

This module does not execute tags or grant authority. Nested values are preserved
as opaque text; malformed fragments remain in the original input.
"""
from dataclasses import dataclass
import re

_TAG = re.compile(r"\[([A-Za-z][A-Za-z0-9_-]{0,63})⛛\{([^{}]*)\}\]")

@dataclass(frozen=True)
class Tag:
    name: str
    value: str
    start: int
    end: int

def scan(text: str) -> list[Tag]:
    """Find non-nested tags; offsets are Python Unicode codepoint offsets."""
    if not isinstance(text, str):
        raise TypeError("text must be str")
    return [Tag(m.group(1), m.group(2), m.start(), m.end()) for m in _TAG.finditer(text)]

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
