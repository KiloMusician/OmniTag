"""Token cost experiment for equivalent handoff metadata representations.

Only real tokenizer results may populate ``tokens``. If tiktoken is not
installed or its local encodings are unavailable, token counts remain null.
The English baseline is informational prose, not a machine-parsed schema.
No secrets, network calls, models, or provider charges are required.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MSG = "SC-ASCENSION-20261008-01"
DATE = "2026-10-08"
CONTEXT = "SC-GSV-INTEGRATION"
REPS = {
    "A_english": f"The message {MSG} was sent on {DATE} in context {CONTEXT}.",
    "B_omnitag": f"[Msg⛛{{{MSG}}}][Date⛛{{{DATE}}}][Ctx⛛{{{CONTEXT}}}]",
    "C_ascii": f"[Msg::{{{MSG}}}][Date::{{{DATE}}}][Ctx::{{{CONTEXT}}}]",
    "D_key_value": f"OMNI:v1|MSG:{MSG}|DATE:{DATE}|CTX:{CONTEXT}",
    "E_english_verbose": f"This message carries identifier {MSG} on date {DATE}, in context {CONTEXT}.",
}


def reconstruct(name: str, value: str) -> dict[str, str] | None:
    """Structured fidelity only. Prose is deliberately unscored."""
    if name == "B_omnitag":
        from omnitag import Tag, parse
        return {t.key.lower(): t.body for t in parse(value).elements if isinstance(t, Tag)}
    if name == "C_ascii":
        import re
        return {m.group(1).lower(): m.group(2) for m in re.finditer(r"\[([A-Za-z]+)::\{([^}]*)\}\]", value)}
    if name == "D_key_value":
        return {key.lower(): val for key, _, val in
                (segment.partition(":") for segment in value.split("|")[1:]) if key}
    return None


def available_tokenizers() -> dict[str, object]:
    result: dict[str, object] = {}
    try:
        import tiktoken
    except ImportError:
        return result
    for name in ("cl100k_base", "o200k_base"):
        try:
            result[name] = tiktoken.get_encoding(name)
        except (KeyError, OSError, ValueError):
            pass
    return result


def benchmark(tokenizers: dict[str, object]) -> list[dict]:
    rows: list[dict] = []
    if not tokenizers:
        # Bytes are not token counts. Do not substitute byte counts.
        tokenizers = {"tokenizer_unavailable": None}
    expected = {"msg": MSG, "date": DATE, "ctx": CONTEXT}
    for tokenizer_name, encoder in tokenizers.items():
        for name, value in REPS.items():
            semantic = reconstruct(name, value)
            rows.append({
                "tokenizer": tokenizer_name,
                "representation": name,
                "characters": len(value),
                "utf8_bytes": len(value.encode("utf-8")),
                "tokens": len(encoder.encode(value)) if encoder is not None else None,
                "machine_reconstruction": semantic == expected if semantic is not None else None,
                "sidecar_dictionary_included": False,
                "model_decision_quality": None,
                "provider_cost": None,
            })
    return rows


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("omnitag_bench_results.json"))
    args = parser.parse_args(argv)
    toks = available_tokenizers()
    rows = benchmark(toks)
    args.out.write_text(json.dumps({
        "schema": "omnitag.tokenizer-bench.v1",
        "source": "public OmniTag proposed fixed synthetic triple",
        "notes": [
            "Tokens are exact for each identified tokenizer, or null if unavailable.",
            "A and E are unscored prose; decision quality requires a separate model eval.",
            "D is self-describing key-value, not proof of shared-dictionary compression.",
            "Overhead of loading a shared dictionary or chat instructions is not measured.",
            "Token counts alone do not establish semantic or operational efficiency.",
        ],
        "rows": rows,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{'tokenizer':<22} {'representation':<20} {'UTF8':>5} {'tokens':>7} {'parse':>7}")
    for r in rows:
        parse = r["machine_reconstruction"]
        print(f"{r['tokenizer']:<22} {r['representation']:<20} {r['utf8_bytes']:>5} "
              f"{str(r['tokens']):>7} {str(parse):>7}")
    print("source: measured tokenizer where present; null is unmeasured")
    print("file:", args.out)
    return 0 if toks else 4

if __name__ == '__main__':
    raise SystemExit(main())
