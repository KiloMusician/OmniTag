# OmniTag round-trip and tokenizer experiment

[Msg⛛{OMNITAG-ROUNDTRIP-EXPERIMENT-20261008}]

**Experimental profile.** The authoritative public [protocol primer](../../docs/PROTOCOL.md) still governs semantics. This code is a proposed implementation, not a normative grammar revision or permission system. This folder intentionally has no operational service endpoints or credentials.

## Run

From this folder:

```sh
python omnitag_tests.py
python -m unittest -v test_omnitag_contract.py
python omnitag_bench.py --out /tmp/omnitag_bench_results.json
```

The suite covers **18 test cases plus 2 meaningful mutation probes**, and 14 additional stdlib unit tests. The previous draft's mutation probe was invalid: it stripped U+FE0F (variation selector) and expected the family-emoji case to fail even though that case contains only U+200D (zero-width joiners). The corrected tests independently strip U+FE0F in the variation-selector case and U+200D in the family-emoji case. Both regressions are detected.

Parser behavior: preserve unknown tags and raw glyphs; NFC canonicalization without compatibility folding; brace-balanced nested tag bodies such as `[Nest⛛{Outer:[State⛛{Observed}]}]`. `[Role⛛{ADMIN}]` is notation, not authority. **Limitations:** no full strict-mode validator, dictionary registry, signed proof model, executable OmniTag semantics or universal nested EBNF is claimed.

## Parser hardening follow-up (2026-10-21)

After review of this experiment's existing draft PR, two concrete reliability defects were fixed **in this same branch**, without changing the advertised OmniTag syntax:

- `UNKNOWN_CONNECTOR` warnings now use original-input offsets captured during parsing, rather than repeatedly serializing all earlier AST elements (previously quadratic in the number of warnings). NFC normalization still happens only when serializing; offsets are for the original input.
- `⟦...⟧` recursion is bounded at 64 nested containers. More deeply nested inputs raise `ParseError(code="NESTING_TOO_DEEP")`, rather than leaking a Python `RecursionError`.
- Non-string input now produces the intended `TypeError` before NFC inspection.

Five regression tests cover those behaviors, including 2,000 warning-bearing segments and 900 nested delimiters. The original 18-case corpus and 2 Unicode mutation checks remain unchanged.

**Independent source-head witness:** isolated Linux checkout of commit `b658587a6394c2950252ec30554578a837da3bd4` on Python 3.14.4: `python3 -m unittest -v test_omnitag_contract.py` → 14 passed; `python3 omnitag_tests.py` → 18/18 cases and 2/2 mutation checks passed; `python3 scripts/validate_public_surface.py` → `status: ok`; `python3 -m compileall -q experiments/roundtrip` → exit 0. This is a runtime witness for the isolated experiment only, **not** a fleet health claim or a merge gate.

**Terminology:** the parser preserves unknown glyphs and round-trips NFC input. Non-NFC input is intentionally canonicalized to NFC, so byte-for-byte or codepoint-for-codepoint "losslessness" is **not** claimed for arbitrary input.

## Measured tokenizer experiment

A bounded synthetic semantic triple was tokenized with exact `tiktoken` encodings on 2026-10-08. The sample is `Msg=SC-ASCENSION-20261008-01`, `Date=2026-10-08`, `Ctx=SC-GSV-INTEGRATION`; no private room or credentials involved.

| Representation | `cl100k_base` | `o200k_base` |
|---|---:|---:|
| A: simple English sentence | 31 | 31 |
| B: Unicode OmniTag | 43 | 43 |
| C: ASCII-style tags | 34 | 34 |
| D: key-value fields | 35 | 35 |
| E: longer English sentence | 33 | 33 |

On this one task, Unicode OmniTag used **12 more tokens (+38.7%) than A** for both tokenizers. This does **not** imply OmniTag has no value. It offers structure and interoperability; its semantic fidelity, retrieval performance, and model reasoning quality have not been measured in this experiment.

`omnitag_bench.py` uses exact identified encodings **only when installed**. If unavailable, it returns exit 4 and reports token count `null`, along with the UTF-8 byte length. Byte length is never relabelled as token length. `D` is merely self-describing key-value syntax, not a genuine amortized dictionary-compression win.

## Source reconciliation

Source context: public OmniTag primer plus user-provided historic symbolic examples. The original pasted parser and example suite were subjected to executable tests and corrected. Legacy examples have richer notation and are deliberately **not** reclassified as invalid solely because a proposed mini-parser handles them as raw data. This implementation should remain tolerant, not try to impose a global authority on legacy ΞNuSyQ dialects.

## Next verification

- Peer-review the grammar limits, Unicode treatment, nested brace behavior and the mutation harness.
- Expand tests with real non-secret legacy corpus samples.
- Run multiple tokenizer families with equal task prompts and document shared dictionary overhead.
- Separately test whether structured tags improve retrieval and downstream decisions.
- Link any in-chat visualization to a separate Apps SDK/MCP implementation; parser source alone does not provide a UI or live connector.

[State⛛{EXPERIMENTAL}] [Auth⛛{NONE}]
