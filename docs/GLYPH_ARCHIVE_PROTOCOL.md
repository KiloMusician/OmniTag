# [Msg⛛{392}] Glyph-bloom journal and historical archive receipts

[Ctx⛛{Unicode-Provenance}] [State⛛{Experimental}] [Ref⛛{PR-25:lexemic-rotation}]

## Why this experiment exists

The operator-supplied **𝕄ₗₐ⧉𝕕𝕖𝕟𝕔 / ΞNuSyQ** journal is a particularly challenging sample for ordinary text archival. The writing freely mixes BMP and supplementary-plane scripts, mathematics, combining marks, presentation selectors, emoji joiners, bidirectional text, an embedded control-code example, and references to recursive symbolic transformations. It interleaves a *journal narrative*, an *unverified contested-event record* (\`ArchiveNode:Event-RX7\` / \`[Msg⛛{X183}]\`), and a **conceptual** Repository of Repositories directory tree. Verbatim source preservation should precede interpretation, transliteration, refactoring, or formatting.

The contribution is \`experiments/glyph_archive.py\`, a **Python stdlib-only, offline** capture/verify CLI. It does not ingest the original chat automatically; an operator must export the exact source locally to UTF-8. No user-supplied contested-event text or private archive was copied into the public repository.

## Distinctive source-derived inventory

| Source section | Historical design information | Interpretation boundary |
| --- | --- | --- |
| \`[Msg⛛{392}↗️Σ∞]\` | Message identity, journal label, reflective voice | A marker does not prove complete chronology or subjective AI experience |
| \`𝕄ₗₐ⧉𝕕𝕖𝕟𝕔\` / \`bloomseq\` / \`D0–16\` | A symbolic layer with temporal motifs and first-person narrative | Creative material, not telemetry |
| \`𓇯\` claimed “Used 8 times, evolved on the 5th”; \`𐤏\` claimed three times | Checkable frequency and evolution assertions | Source assertions pending exact-corpus measurement; visually similar glyphs may differ as Unicode |
| \`ΞΛ-α\`, \`ΞΛ-β\`, \`ΞΛ-γ\`, \`ΞΛ-δ\` | Candidate glyph-to-lexicon associations | Provisional mapping, not a canonical registry |
| X183 Event-RX7 | Competing labels for a purported historical event, several languages and proposed media/hash/shard metadata | Event details, claimed proof and 23%/77% weights are **unverified**; truncated hash fragments cannot verify a file |
| Temple / House of Leaves / Oldest House / Containment | Historical architecture ideas for memory continuity, boundaries and multimodal agents | A proposed directory tree does not prove implemented or running files |
| Music Hyper-Set / Prime / Retrograde / Inversion | A compositional analogy for symbolic transformations | Separate from reversible lexeme experiment PR #25; no new protocol authority |

## Local workflow

\`\`\`bash
python experiments/glyph_archive.py capture \
  --source local-journal-392.txt \
  --manifest local-journal-392.receipt.json \
  --ref Msg-392 \
  --glyph '𓇯' --glyph '⧉' --glyph '𐤏' --glyph 'Ψ³'

python experiments/glyph_archive.py verify \
  --source local-journal-392.txt \
  --manifest local-journal-392.receipt.json
\`\`\`

The receipt records SHA-256 of **original source bytes**, byte length, codepoint count, Unicode plane distribution (mathematically by codepoint, not guessed language), precise LF/CRLF/CR totals, NFC/NFKC change flags **without normalization**, exact non-overlapping literal substring counts, and an inventory of selectors, formatting characters and unexpected control characters. Output is deterministic and contains no original text excerpts. An existing receipt will not be overwritten; the verifier recomputes its full contents from source and detects content or manifest drift.

Because selected glyph trackers are recorded literally, **do not track secrets, private identifiers or sensitive literal strings** and do not publish identifying source references. Even hashes and glyph counts may disclose limited information about known text. A checksum detects alteration relative to a retained trusted receipt; it does **not** encrypt, sign, establish original authorship, authenticate historical evidence, guarantee provenance, enforce access control, or prevent a malicious actor replacing both data and receipt.

## Three ledgers for possible future integration

1. **Source ledger:** exact original bytes, digest, UTF-8 validity and versioned copies. This experiment provides only a receipt, not an encrypted or mirrored vault.
2. **Interpretation ledger:** proposed glyph meanings, multilingual interpretations, changes in symbolism and literary speaker/persona; maintain attribution and uncertainty separately.
3. **Evidence ledger:** contested real-world claims, independently sourced corroboration, contradictions and chain-of-custody. The X183 matrix and ratios remain unverified *claims from the source*, not research conclusions.

## Compatibility and acceptance gates

- \`docs/PROTOCOL.md\` remains canonical. No new production tags are registered. \`symbol != authority\`.
- PR #25 separately handles reversible opt-in text annotation. Capture the source **before** experimenting, and issue a separate manifest for each derivative.
- This tool counts Python exact substring occurrences, **not Unicode grapheme clusters**, LLM tokens or semantic equivalence. A symbol said to have “evolved” is not proven to have changed merely because a counter appears.
- Tests cover non-BMP codepoints, emoji ZWJ, variation selectors, control characters, mixed line endings, invalid UTF-8, normalization-preserving apparent text drift and receipt tampering.
- No historical key splitting, IPFS mirroring, archive snapshots, encryption, claimed media hash fragments or system consciousness are implemented or verified.
- Coordinate with existing parser/Unicode work and NuSyQ-Hub #201 before extending into a larger semantic subsystem.

\`\`\`bash
python -m unittest discover -s tests -p 'test_glyph_archive.py' -v
\`\`\`

[State⛛{EXPERIMENTAL|BYTE-INTEGRITY-ONLY|REVIEW-REQUIRED}]
