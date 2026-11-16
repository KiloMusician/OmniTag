"""Opt-in, lossless scanner for simple OmniTag annotations.

Only complete flat tags are recognized. Nested annotations are an opaque
fragment: the scanner deliberately does not strip or execute inner tags.
Offsets refer to Python Unicode codepoints, not grapheme clusters.
"""
from dataclasses import dataclass
import re

_PREFIX = re.compile(r"\[([A-Za-z][A-Za-z0-9_-]{0,63})⛛\{")


@dataclass(frozen=True)
class Tag:
    name: str
    value: str
    start: int
    end: int


def scan(text: str) -> list[Tag]:
    """Find flat tags, preserving nested expressions as opaque text.

    A regex for flat matches alone would detect inner [State⛛{...}] inside
    [Nest⛛{...}], causing render_plain to corrupt the outer expression.
    Scan from each candidate prefix through balanced braces; never emit the
    interior of a nested candidate as an independent flat annotation.
    """
    if not isinstance(text, str):
        raise TypeError("text must be str")
    tags: list[Tag] = []
    cursor = 0
    while True:
        match = _PREFIX.search(text, cursor)
        if match is None:
            break
        value_start = match.end()
        depth = 1
        nested = False
        end = value_start
        while end < len(text) and depth:
            char = text[end]
            if char == "{":
                depth += 1
                nested = True
            elif char == "}":
                depth -= 1
            end += 1
        if depth != 0:
            # An unclosed outer value owns the remaining text. Treat it
            # as opaque, especially any well-formed inner tag; otherwise
            # render_plain would silently strip the inner expression.
            break
        if end < len(text) and text[end] == "]":
            if not nested:
                tags.append(Tag(match.group(1), text[value_start:end - 1],
                                match.start(), end + 1))
            cursor = end + 1
        else:
            # Braces closed but closing bracket was absent: this outer
            # candidate is invalid. Its interior must remain opaque;
            # resume only AFTER the candidate's closing brace.
            cursor = end
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
    """Remove flat annotations without altering nested or malformed syntax."""
    return "".join(fragment for kind, fragment in split(text) if kind == "text")
