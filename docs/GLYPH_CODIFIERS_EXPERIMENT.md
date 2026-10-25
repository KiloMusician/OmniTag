# Glyph codifiers: source-preserving semantic overlay (experimental)

[Msg⛛{GLYPH-CODIFIERS-20261025}] [State⛛{proposed}]

## Problem and provenance

A 2026-10-25 conversation explored dense glyph clusters in a `stocklens` terminal screenshot, compared them with RSHT / MegaTag / OmniTag, and outlined a candidate semantic-plane inventory P00–P50. The screenshot visibly includes ordinary development anchors, but **its encoding, original text, speaker, process state, and glyph meanings are unknown**. Earlier English "translations" were **interpretive hypotheses**, not decoded facts. In particular, a pictured `HTTP/1.1 200 OK` is not evidence of *current* service availability. Do not archive private system topology or the screenshot itself in this public repo.

The contribution here is deliberately smaller than the proposed 51-plane language: a reversible **glyph-to-stable-ID semantic overlay**. It is not a language model, executable DSL, terminal decoder, standalone OmniTag parser, cryptosystem, or consciousness detector.

## Relationship to existing work

- `docs/PROTOCOL.md` remains authoritative for `[Tag⛛{Value}]` syntax and truth/permission boundaries.
- Draft PR #30 already adds an opt-in *flat OmniTag scanner*; draft PR #5 experiments with a larger parser. This spike scans selected **glyph surfaces only**; it does not parse tags.
- `experiments/lexemic_rotation.py` and its tests already prove source-ledger restoration for opt-in vocabulary annotation. This spike targets **operator/structure codifiers**, not musical lexeme transformation.
- Draft PR #13 covers presentation emoji and accessibility; glyph fallback here is a *gloss*, not a claim that display makes truth.
- Issue #36 tracks broader NFC/NFD, Zalgo, and nested-tag interoperability.

## Codifier registry and normative limits

Each candidate mapping has exactly one stable, project-scoped ID `XG.<FAMILY>.<NAME>`, a literal Unicode surface, a narrow proposed gloss, and an ASCII-ish fallback. A surface has **one registry meaning**, even if cultural, mathematical, or narrative readings coexist outside this profile. Register a new dialect/namespace rather than silently overwriting a meaning. The initial registry is deliberately small (13 entries): frames, route/transform/bind/merge/revisit/observe, partial/unknown state, noise, and checkpoint. All mappings are *proposed*, never assertions that StockLens really expressed those meanings.

The decoder emits a JSON-compatible `omnitag-glyph-codifiers/v1` packet containing contiguous **Python code-point** spans and untouched raw segments; it does not normalize original text. It uses greedy longest-surface matching, checks duplicate IDs/surfaces, blocks selected bidirectional control and surrogate glyph definitions, and checks SHA-256 on exact reconstruction. SHA-256 is an accidental-edit/tamper-detection **digest**, not authenticity, authorization, or a signature. Unknown glyphs, combining marks, emoji/ZWJ sequences, PUA codepoints, nested OmniTags and line endings survive as raw text. `gloss()` is a one-way display view; never reconstruct from a gloss.

### Bounded example (synthetic, not extracted from the screenshot)

```text
[Msg⛛{7}] README ↠ OPS ⊗ URL ◌
```

Proposed fallback view:

```text
[Msg⛛{7}] README ->route OPS *bind* URL unknown
```

The message tag remains raw text and carries no authority. The `◌` codifier describes an unknown state rather than asserting a verified observation.

## Verification

```sh
python -m py_compile experiments/glyph_codifiers.py
python -m unittest discover -s tests -p 'test_glyph_codifiers.py' -v
python scripts/validate_public_surface.py
```

Test obligations: 14 deterministic stdlib tests cover uniqueness, collision rejection, bidi/surrogate/invisible-only surfaces, NFC/NFD distinction, ZWJ emoji, PUA, raw tags, longest match, span integrity, tamper detection, and empty input. Token savings, Unicode grapheme segmentation, display width, comprehension benefits, and real-world StockLens decoding have **not** been measured.

## Next investigations

1. **P1: controlled codifier admission**. Create a versioned, schema-validated registry and cross-dialect namespace policy. Measure compatibility against existing PR #5/#30 and issue #36 without rebasing their code blindly.
2. **P1: three-way decoding evidence**. Produce *raw codepoint dump + font/render trace + interpretation hypothesis* for future terminals. Collect consent-cleared raw source before attempting literal translation; screenshot pattern-matching alone is insufficient.
3. **P2: reversible gloss benchmarking**. Compare human interpretation accuracy, round-trip fidelity, Unicode byte size, and actual LLM tokenizer costs against plain language. Never equate fewer visible characters with fewer tokens.
4. **P2: semantic-plane ontology**. Formalize candidate P00–P50 in separate documents only after assigning collision-free IDs, input/output types, arity, evidence states, and semantic scope. Distinguish roles, grammatical functions, protocol events, and decorative skin.
5. **P3: font/accessibility profile**. Test grapheme boundaries, emoji VS/ZWJ, terminals, RTL safety, searchable ASCII aliases, and supplementary-plane fallback; PUA requires agreed fonts and codebooks.

[State⛛{proposed}] [Ref⛛{issue-36}] [Ref⛛{PR-30}] [Ctx⛛{Unicode-Interoperability}]
