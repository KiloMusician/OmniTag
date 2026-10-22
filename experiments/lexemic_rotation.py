"""Experimental, non-authoritative Unicode/serial-row lexeme annotator.

Only explicitly selected terms are annotated. Source text and an exact-span
ledger are retained to permit a byte-for-byte Unicode round trip.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

ROW = (0, 7, 2, 9, 4, 11, 5, 1, 8, 3, 10, 6)
MODES = ("P", "R", "I", "RI")
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUPER = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
# Explicit code point sets, not claims of natural-language equivalence.
PALETTES = {
    0: tuple("ΑΒΓΔΕΖΗΘΙΚΛΜ"),  # Greek, BMP
    1: tuple(chr(0x10400 + i) for i in range(12)),  # Deseret, SMP
    2: tuple(chr(0x20000 + i) for i in range(12)),  # CJK Ext B, SIP
}


def transform_row(row: Sequence[int], mode: str) -> tuple[int, ...]:
    """Music-theoretic prime/retrograde/inversion/retrograde-inversion."""
    if len(row) != 12 or set(row) != set(range(12)):
        raise ValueError("row must contain each pitch class 0..11 exactly once")
    if mode not in MODES:
        raise ValueError(f"unknown mode: {mode}")
    prime = tuple(row)
    transformed = prime if mode in ("P", "R") else tuple((2 * prime[0] - x) % 12 for x in prime)
    return transformed[::-1] if mode in ("R", "RI") else transformed


def is_boundary(text: str, index: int) -> bool:
    """Reject interior matches, Unicode combining marks, and path fragments."""
    if index < 0 or index >= len(text):
        return True
    c = text[index]
    return not (c == "_" or c in "/\\" or unicodedata.category(c)[0] in "LMN")


@dataclass(frozen=True)
class Event:
    term: str
    source_start: int
    source_end: int
    source_text: str
    output_start: int
    output_end: int
    occurrence: int
    mode: str | None
    plane: int | None
    row: tuple[int, ...] | None
    rendered: str


def annotate(text: str, terms: Sequence[str]) -> tuple[str, list[Event]]:
    """Annotate only declared lexemes; alternate 12-tone forms at 10x events.

    Events contain source and output offsets and unmodified source fragments;
    no claim of token reduction or quantum computation is made.
    """
    if not terms or any(not term or term.isspace() for term in terms):
        raise ValueError("supply nonempty terms")
    canonical = [unicodedata.normalize("NFC", term).casefold() for term in terms]
    if any(not all(unicodedata.category(c)[0] in "LMN" for c in term) for term in canonical):
        raise ValueError("terms must consist of letters, numbers or combining marks")
    if len(set(canonical)) != len(canonical):
        raise ValueError("duplicate terms after NFC+casefold")
    # NFC is used only for matching. Never normalize the source itself.
    pattern = re.compile("|".join(re.escape(term) for term in sorted(terms, key=len, reverse=True)), re.IGNORECASE)
    counts = dict.fromkeys(canonical, 0)
    output_parts: list[str] = []
    events: list[Event] = []
    src_cursor = out_cursor = 0
    for match in pattern.finditer(text):
        a, b = match.span()
        if not (is_boundary(text, a - 1) and is_boundary(text, b)):
            continue
        token = match.group()
        key = unicodedata.normalize("NFC", token).casefold()
        if key not in counts:
            continue
        gap = text[src_cursor:a]
        output_parts.append(gap)
        out_cursor += len(gap)
        counts[key] += 1
        n = counts[key]
        mode = None
        plane = None
        row = None
        if n % 10:
            rendered = token + str(n).translate(SUB)
        else:
            k = n // 10 - 1
            mode = MODES[k % len(MODES)]
            plane = k % len(PALETTES)
            row = transform_row(ROW, mode)
            glyphs = "".join(PALETTES[plane][p] for p in row)
            rendered = f"⟦{token}:{mode}{str(k + 1).translate(SUPER)}:D{plane}:{glyphs}⟧"
        start = out_cursor
        output_parts.append(rendered)
        out_cursor += len(rendered)
        events.append(Event(key, a, b, token, start, out_cursor, n, mode, plane, row, rendered))
        src_cursor = b
    output_parts.append(text[src_cursor:])
    return "".join(output_parts), events


def restore(annotated: str, events: Sequence[Event]) -> str:
    """Restore literal source, validating exact annotated spans against ledger."""
    pieces = []
    cursor = 0
    for event in events:
        if event.output_start < cursor or annotated[event.output_start:event.output_end] != event.rendered:
            raise ValueError("annotation/ledger mismatch")
        pieces.extend((annotated[cursor:event.output_start], event.source_text))
        cursor = event.output_end
    pieces.append(annotated[cursor:])
    return "".join(pieces)


def main(argv: Sequence[str] | None = None) -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("source", type=Path, help="UTF-8 source text")
    cli.add_argument("--term", action="append", required=True, help="explicit lexeme to annotate")
    cli.add_argument("--output", type=Path, required=True)
    cli.add_argument("--ledger", type=Path, required=True)
    args = cli.parse_args(argv)
    if args.source.resolve() in (args.output.resolve(), args.ledger.resolve()):
        cli.error("source, output and ledger must be different files")
    if args.output.resolve() == args.ledger.resolve():
        cli.error("output and ledger must be different files")
    with args.source.open("r", encoding="utf-8", newline="") as stream:
        original = stream.read()
    result, events = annotate(original, args.term)
    if restore(result, events) != original:
        raise ValueError("round-trip verification failed")
    args.output.write_text(result, encoding="utf-8", newline="")
    args.ledger.write_text(json.dumps({"format": "omnitag-lexemic-v1", "terms": args.term,
                                     "events": [asdict(e) for e in events]},
                                    ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"annotated {len(events)} occurrences; UTF-8 bytes {len(original.encode('utf-8'))} -> {len(result.encode('utf-8'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
