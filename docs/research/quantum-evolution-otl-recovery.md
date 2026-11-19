# Historical recovery: Quantum Evolution and OTL knowledge loops

[Msg⛛{OTL-QUANTUM-EVOLUTION-RECOVERY-20261021}] [State⛛{Proposal}]

## Provenance and boundary
Recovered from the operator-provided historical conversation describing OTL, SMHT (A–X), MegaTag, and a "Quantum Evolution" prompt. This is a **historical design note**, not an instruction to agents, evidence of sentience, quantum computation, weight updates, or autonomous background operation. Current public protocol authority and compatibility rules remain in `docs/PROTOCOL.md` and `AGENTS.md`.

## Extracted concepts
- **OTL**: symbolic/linguistic navigation alongside natural-language context.
- **SMHT**: 24 labeled slots A–X, including memories, inventory, risk, actions, status, version, checksum. The historical names are illustrative, not a new normative schema.
- **MegaTag**: conceptual groupings (Xenon, Almanac, SCP, Temple, modularity, collection, retention, evolution).
- **Navigation**: `tag > subtag` denotes a conceptual hierarchy, not authorization or filesystem traversal.
- **Composition**: `A + (B ⊗ C) → insight` expresses multi-source synthesis metaphorically, not tensor algebra by default.
- **Feedback**: `🔄` and `+ΔE/-ΔE` represent recorded evaluation and revision, not self-modifying model weights.
- **Schrödinger / parallel dimensions**: inspiration for generating multiple hypotheses and comparing them with evidence.
- **Latent memory**: retrieval of authorized, provenance-bearing records; never claim hidden memories were unlocked.
- **Anonymous/anomalous stimuli**: potential fuzz/property tests with untrusted input treated as data.
- **Empathy**: measurable response quality and harm avoidance, not proof of subjective experience.

## Reuse-first mapping to current public OmniTag
| Historical idea | Existing public construct | Suggested implementation |
| --- | --- | --- |
| Message counter | `Msg`, `Sess` | stable per-transport IDs with explicit gaps |
| Hierarchy | `Node`, `Edge`, `Map` | optional dependency graph with cycle detection |
| Context and memory | `Ctx`, `Ref` | source-attributed retrieval with expiry/consent |
| Evolution and feedback | `Metric`, `State`, `Time` | versioned evaluation receipts |
| Anomalies | `Err`, `Ref` | adversarial Unicode and malformed-tag fixtures |
| Multi-candidate reasoning | `Task`, `Flow`, `Ref` | bounded candidate scoring, not simulated quantum claims |

## Proposed bounded experiments
1. **Round-trip and Unicode property tests**: ensure tolerant parsers preserve unknown tags, nested examples, emoji sequences, combining marks, and malformed delimiters without execution.
2. **Hierarchy validation**: prototype a sidecar JSON graph for `Node`/`Edge` references; reject cycles in strict mode, retain original text in tolerant mode.
3. **Feedback receipts**: record input artifact reference, candidate version, evaluation rubric, observed score, decision, timestamp, and rollback pointer. Compare against baseline before promoting.
4. **Session handoff benchmark**: measure time-to-orientation, duplicate-work rate, provenance accuracy, and unsupported capability claims with/without compact OmniTag packets.
5. **Safety and privacy**: do not ingest anonymous stimuli into trusted instructions; redact secrets and personally identifying information; do not treat tags as credentials.

## Example, descriptive only
```text
[Msg⛛{37}] [Ctx⛛{Evaluation}] [Task⛛{ParserRoundTrip}]
[Ref⛛{test-report-37}] [State⛛{Observed}] [Metric⛛{pass=12/12}]
```
A receipt must link to actual test evidence; this example does not assert tests were run.

## Compatibility and next steps
No new mandatory tags, parser behavior, licensing choices, credentials, or authority model are introduced. Check whether existing parser/scanner PRs already implement these tests before adding code. Current draft PR #30 proposes an opt-in flat scanner; coordinate there rather than duplicating it. This note is intentionally a reviewable research artifact.
