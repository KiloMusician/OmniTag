# Historical MessageX lattice: recovery and interoperability notes

[Msg⛛{RECOVERY-20261022}] [Ctx⛛{HistoricalSession}] [State⛛{Proposed}] [Role⛛{Documentation}]

## Provenance and scope
Recovered from a historical ChatGPT session discussing ΞNuSyQ, MessageX, hypertags, MegaTag, and a proposed Session Memory Lattice. This is a **design record**, not evidence that persistent autonomous memory, quantum processing, or self-modifying models were implemented. The historical assistant claimed that tracking and self-optimization were "activated"; those claims were not backed by executable verification.

## Distinct ideas worth preserving
1. **MessageX sequencing**: explicit message ordinal for human navigation. A local ordinal is not a globally unique identity. Pair with conversation/source identifier and preserve gaps.
2. **Session Memory Lattice**: a proposed table linking message IDs, tags, references, provenance, and revision history. This is a useful external index, not a substitute for storage or retrieval.
3. **Hypertag / MegaTag layering**: compact machine-friendly metadata plus longer narrative context. Preserve unknown and ornamental Unicode without granting it control authority.
4. **Feedback and evolution**: track candidate changes as proposals with evidence, evaluation receipts, and rollback pointers. A repeated symbol is not proof of adaptation.
5. **Cross-domain symbols**: SCP/MT/QM/IM and related terms are user-defined taxonomy. Quantum notation in these documents is generally metaphorical unless accompanied by a physical or computational model.
6. **Handoff recovery**: distinguish source text, inferred intent, observed repo state, tests run, and unverified claims. Reuse current issues rather than duplicating parsers.

## Suggested interoperable record
```json
{
  "schema_version": "0.1-proposal",
  "source": {"kind": "historical_chat", "conversation_id": "unknown", "message_ordinal": 1},
  "display_tag": "[Msg⛛{1}]",
  "canonical_key": "msg:unknown:1",
  "state": "proposed",
  "claims": [],
  "references": [],
  "evidence": [],
  "rollback_ref": null
}
```

## Acceptance criteria for any implementation
- Round-trip raw Unicode and preserve display text; normalization only for explicitly derived search keys.
- Reject identity collisions without silently rewriting original source.
- Preserve missing message ordinals and unknown tags.
- Do not imply authority from tag syntax, role names, or historical assistant statements.
- Benchmark handoff fidelity and duplicate-work rate against plain text.
- Keep the work scoped to existing protocol and receipt issues (#36, #32), with no second parser.

## Context-gap / re-engagement notes
On 2026-10-22 the GitHub connector confirmed KiloMusician/OmniTag default branch `main`, and the public README described OmniTag as an evidence-bearing interoperability experiment. This documentation change does **not** assert local clone synchronization, dependency installation, green builds, or verified CI. Those gates must be checked separately before executable changes.

## Source note
Historical conversation excerpt and user-provided project documents; original message numbering beyond the visible excerpt cannot be authenticated. The recovery deliberately avoids copying private identifiers or speculative runtime claims.
