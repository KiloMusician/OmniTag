# Emoji and Symbol Layering Interoperability

[Msg⛛{OMNITAG-EMOJI-LAYERING-v1}] [State⛛{Proposed}]

This note defines a **presentation profile**, not a change to OmniTag's core grammar. Emoji are optional visual cues; textual tag keys remain authoritative for parsing metadata.

## Three independent layers

1. **Semantic**: `[State⛛{Observed}]` expresses a parseable assertion.
2. **Visual**: `🔍` signals inspection to human readers.
3. **Evidence**: `[Ref⛛{issue-2}]` points to supporting material.

Example:

```text
🔍 [Task⛛{Audit}] [State⛛{Observed}] [Ref⛛{issue-2}]
Inspection found an ambiguous glyph mapping.
```

Removing the emoji must not change the machine-readable meaning.

## Composition rules

- Prefer **sequence** (`🔍🧪`) over attempting literal overlapping glyphs. Unicode emoji are rendered by the host font/platform and cannot be reliably positioned atop each other in plain text.
- Use a small stable visual vocabulary within a document: `🔍` inspect, `🧪` test, `🛠️` change, `⚠️` caution, `✅` verified. These are **suggested display conventions**, not protocol states.
- Never infer verification from `✅` alone. Pair with `[State⛛{proven}]` and an evidence reference when claiming a successful check.
- Avoid color-only meaning. Add ordinary words so screen readers and monochrome renderers retain context.
- Treat ZWJ sequences, skin-tone modifiers, variation selectors and combining marks as Unicode sequences, not necessarily one code point. Do not truncate or index emoji by byte or code point when a grapheme cluster is intended.
- Normalize only when a transport contract explicitly specifies normalization; avoid silently rewriting identifiers containing Unicode.
- For logs, CI and machine exchange, offer an ASCII fallback: `[Task⛛{Audit}] [State⛛{Observed}]`.
- Keep symbolic embellishments out of repository paths, executable commands, credentials and identifiers unless a consuming system explicitly supports them.

## Test vectors

| Input | Expected behavior |
| --- | --- |
| `🔍 [State⛛{Observed}]` | Parse State as Observed; ignore emoji as presentation |
| `⚠️ [Err⛛{Timeout}]` | Parse Err as Timeout without depending on emoji |
| `🧪 [Novel⛛{alpha}]` | Tolerant reader preserves unknown tag |
| `[State⛛{proven}]` | Still readable with no emoji |
| `👩‍💻 [Role⛛{Developer}]` | Emoji grapheme does not affect tag boundary |

## Acceptance criteria for a future validator

- Parses all five vectors consistently with the existing protocol.
- Preserves unknown tags in tolerant mode.
- Produces equivalent tag metadata when presentation emoji are removed.
- Never interprets glyphs as authority or proof.
- Records platform-specific rendering differences as display issues, not semantic failures.

[State⛛{Proposed}] [Ctx⛛{PublicInteroperability}] [Ref⛛{issue-2}]
