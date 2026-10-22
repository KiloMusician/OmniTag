# Lexemic rotation: bounded Sashuric / Music Hyper-Set experiment

[Msg⛛{OMNITAG-LEXEMIC-ROTATION-V1}] [State⛛{EXPERIMENTAL}]

## Provenance and non-goals

This experiment derives from the historical ΞNuSyQ₁-Hub₁ **Repository of Repositories** conversation: its unabridged preservation directive, contextual conlang transformations, the KiloEthereal vantage / static-memory anchor idea, RosetSyStone.qgl, KEVE, OmniTag/MegaTag/ΞHyperTag, and the distinct **post-tonal, atonal, and serial** music-analysis lenses. See existing research PR #21 and protocol docs/PROTOCOL.md rather than duplicating a runtime authority. Historical module names are **design candidates**, not proof those files exist or are healthy.

**Crucial correction:** the prior example replaced every tenth word with ξΛVξNΩ¹. That destroys lexical identity unless a mapping is carried separately. The experiment therefore handles only explicitly opted-in terms, retains the original source, and saves a sidecar span ledger to restore it. Glyphs are identifiers/annotations, not encoded meanings by themselves.

## Reproducible transform

The base twelve-tone pitch-class row is:

    0 7 2 9 4 11 5 1 8 3 10 6

Four operations are distinct, not aliases:

- **Prime (P):** row unchanged.
- **Retrograde (R):** row read backward.
- **Inversion (I):** each pitch class x maps to (2*row[0] - x) mod 12.
- **Retrograde inversion (RI):** inverted row read backward.

Each selected lexeme receives global subscripts for occurrences other than a multiple of ten. At occurrence 10, 20, 30, 40, etc., it receives a mode-and-plane marker. Modes rotate P, R, I, RI, while codepoint palettes rotate Unicode planes 0, 1, 2. Each palette has 12 explicitly enumerated glyphs; none is called an alphabetic translation. The event ledger records exact source and output character offsets, unmodified original spelling, occurrence, pitch row, mode, and plane. Text untouched by the annotation stays untouched during reverse reconstruction. The source and annotated file are deliberately separate.

This models contextual **symbolic transformation**, not physical quantum superposition, proof of consciousness, or demonstrated information compression. Higher codepoint density, Unicode bytes, grapheme clusters, tokenizer cost, display width, ambiguity, and accessibility are different measurements. The CLI prints actual UTF-8 source/output byte counts; it does **not** pretend to measure LLM tokens. Some outputs will be larger.

Doppelgängers in the source's terminology can be treated as a **confirmation phenomenon** only in the narrow, testable sense of independently produced equivalent reconstructions or representations; it is not a verified external entity or evidence of sentience. SCP containment language is narrative/conceptual unless a real executable safeguard is separately implemented.

## Run offline (Python standard library)

    python -m unittest discover -s tests -p 'test_lexemic_rotation.py' -v
    python experiments/lexemic_rotation.py source.txt --term Sashuric --term Fractal --output annotated.txt --ledger rotation-ledger.json
    python experiments/lexemic_rotation.py annotated.txt --restore --output restored.txt --ledger rotation-ledger.json

On restoration the CLI checks SHA-256 of both the entire annotated file and the reconstructed original against the versioned ledger, including text outside annotated spans. The tested procedure preserves original CRLF bytes. Input files must be UTF-8. The CLI refuses to overwrite its input and refuses to make the annotated file and ledger the same file. restore(annotated, events) checks that annotated spans still agree with the ledger before reconstructing the original string. Tests cover all four transforms, 40th-occurrence cycling, Unicode emoji/ZWJ and combining marks, file paths, unselected terms, tamper rejection, and CRLF retention.

## Admission criteria for a future implementation

1. Prefer source-preserving opt-in annotation over rewriting names or code identifiers. Preserve static/historical nodes as immutable evidence, not as self-asserted truth.
2. Give every RosetSyStone.qgl mapping a stable, inspectable lexicon definition, provenance, and exact inverse where possible. KEVE has no verified operational expansion here: do not invent one.
3. Have Music_Hyper_Set_Analysis supply algebraic transformations; do not conflate post-tonal theory, atonality, and serialism.
4. Add Unicode grapheme and shaping/normalization tests before claiming internationalized production readiness. Avoid private-use characters without font/support contracts.
5. Record a reversible original-to-transformed ledger independent of rendition. Use hashes or durable references when integrating with StaticMemoryNodes and KiloEthereal vantage snapshots.
6. Reconcile with experimental parser PR #5 and Unicode display PR #13 before admission into the canonical protocol. No new symbolic tag here grants permissions or trust.

[State⛛{REVIEW_REQUIRED}] [Metric⛛{LOCAL_UNIT_TESTS:10}] [Ref⛛{HISTORICAL_SESSION}]

## Session harvest: historical architecture mapped to testable contracts

This is a source-derived **candidate inventory**, not a new directory tree or evidence of deployed services. The old transcript repeatedly printed a conceptual Repository of Repositories with mutable filenames. The current live NuSyQ-Hub has an actual codebase and archive, so its current source and #201 authority map take priority over this sketch.

| Historical motif | Distinctive design requirement | Bounded future proof |
| --- | --- | --- |
| **Step 0: Point, Space, Motion** | Point = stable node/identity; space = versioned relations/edges; motion = ordered state transitions. These are three dimensions, not one synonym for recursion. | Compare graph snapshots and event ordering on a deterministic fixture. |
| **Step 1 through Step 7** | Six analysis/cultivation passes before unabridged delivery, with completeness checks on the final pass. | Snapshot expected path names and compare output inventory, count, hashes, and omissions. |
| **Repository of Repositories** | Preserve Temple (10 elevator-linked floors), House of Leaves, Oldest House, Containment Sector, anomaly boundaries, librarian, CLI, memory, sound and agent interfaces **without repeated fake tree tails**. | Match against Git-tracked tree; distinguish missing desired modules from existing implementations. |
| **Music Hyper-Set Analysis** | Post-tonal set-theoretic inquiry, atonality, and serialism are distinct; Prime, Retrograde, Inversion and Retrograde-Inversion are actual transformations, not visual synonyms. | Twelve-tone row invariants, pitch-class bijections, involutions, serial order fixtures. |
| **Lexemic transformation** | A threshold on selected words must carry iteration, mapping, context and an inverse; no universal tenth-word substitution. | This PR's opt-in interpreter, span ledger, checksum and 10/20/30/40 event tests. |
| **Multi-plane Unicode** | Choose combining marks and BMP/SMP/SIP glyphs contextually; rotate systematically and document *why* a domain was chosen. Domain numbers are not semantic authority. | Grapheme stability, normalization, screen reader, glyph availability and tokenizer comparison tests. |
| **RosetSyStone.qgl** | Bidirectional concordance linking glyphic tokens with source concepts and provenance. | Versioned mapping registry and round-trip fixtures before admitting a grammar. |
| **OmniTag / MegaTag / ΞHyperTag** | Message/event metadata, structural grouping and cross-layer reference are separate contracts. | Versioned envelopes and legacy adapter characterization under NuSyQ-Hub #201. |
| **KEVE / KiloEthereal Vantage** | Preserve a named historical vantage and snapshot semantics while explicitly leaving KEVE's expansion **unverified**. | Immutable source receipt + diff to current HEAD, no fabricated operational state. |
| **Static Memory Nodes** | A source-derived anchor must not overwrite history merely because a later transformation repeats or decorates it. | Append-only record with digest and provenance, plus replay tests. |
| **Oldest House / House of Leaves** | Separate protected ancestral history from branching explorations and unfinished thoughts. | Immutable archive test versus mutable draft/branch tests. |
| **Containment Sector / SCP constructs** | Useful metaphors for anomaly quarantine and review gates, with SCP narratives kept distinct from real software safeguards. | Fail-closed transition tests and authority boundary assertions. |
| **Doppelgängers** | Historical **confirmation phenomenon** should mean equivalent, independently reproducible outputs under a declared canonical comparison. | Two independent runs, same seed and same ledger digest; no consciousness inference. |
| **Raven / The Librarian** | Narrative roles distinguish exploratory divergence from archival provenance; no evidence of independent sentience follows from story text. | Explicit provenance annotations for simulated agent personas. |
| **124 Zeta Intersectional Questions** | Research cross-dependencies rather than treating every evocative module name as implemented code. | Issue-linked question-to-contract triage, prioritized by execution evidence. |

**Known limitations:** a Python regex is not a universal grapheme segmenter; mixed normalization forms, language-sensitive casefold equivalence, confusable punctuation and accessibility remain open. This is a safe offline laboratory, not a production parser, ontology, compression format, or runtime permission system.

[State⛛{ARCHAEOLOGY_PRESERVED|EXECUTABLE_EXPERIMENT_ONLY}]
