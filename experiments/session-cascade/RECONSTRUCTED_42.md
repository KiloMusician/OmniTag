# Reconstructed 42-technique OmniTag catalog (candidate v0.1)

[State⛛{Proposed}] [Ctx⛛{Research-Reconstruction}]

**Provenance and limitations:** The session establishes the 42-technique objective, but the original authoritative list is not available. All 42 labels below are **newly reconstructed proposals**, not claimed historical recovery. This proposal follows the current public `docs/PROTOCOL.md` grammar and the public `AGENTS.md` capability and security boundaries.

## Design contract

Given event `E_t`, explicit state `S_t`, declared profile `P`, and selected transformations `F_i`:

`S_(t+1) = Validate_P(Compose(F_i in dependency order)(S_t, E_t))`

The numbered catalog is **not** an execution order. An eventual scheduler should enforce dependency edges and versioned inputs. Symbols do not grant permission or prove execution.

## 42 proposed techniques

| ID | Technique | Contract |
|---|---|---|
| T01 | Event admission | Validate event envelope |
| T02 | Role classification | Track declared actor role |
| T03 | Message sequencing | Monotonic local sequence |
| T04 | Session identity | Stable explicit session key |
| T05 | Timestamp normalization | UTC time when evidenced |
| T06 | Unicode policy | Explicit normalization version |
| T07 | Flat tag parsing | Parse [Tag⛛{Value}] |
| T08 | Nested tag parsing | Bounded recursive grammar |
| T09 | Unknown-tag preservation | Tolerant interoperability |
| T10 | Profile validation | Apply declared schema |
| T11 | Content digest | Hash source event |
| T12 | Source attribution | Link to verifiable origin |
| T13 | Claim typing | Observed/inferred/proposed |
| T14 | Capability typing | Proven/denied/unavailable/unknown/not_required |
| T15 | Uncertainty annotation | Represent epistemic limits |
| T16 | Temporal scoping | Current versus historical |
| T17 | Entity extraction | Identify referents |
| T18 | Alias reconciliation | Preserve name provenance |
| T19 | Reference linking | Connect durable IDs |
| T20 | Deduplication | Avoid duplicate event effects |
| T21 | Contradiction detection | Flag incompatible claims |
| T22 | Conflict retention | Keep unresolved alternatives |
| T23 | Recency policy | Explicit evidence freshness |
| T24 | Priority scoring | Transparent bounded ranking |
| T25 | Task extraction | Derive reviewable tasks |
| T26 | Dependency mapping | Build task DAG |
| T27 | Action status | Proposed/attempted/verified |
| T28 | Failure classification | Record observed error class |
| T29 | Privacy filtering | Exclude secrets |
| T30 | Retention control | Scope and expiry |
| T31 | Memory candidate selection | Propose useful durable facts |
| T32 | Human approval gate | Consent and review |
| T33 | State folding | Deterministic reducer |
| T34 | Replay verification | Recompute from events |
| T35 | Canonical serialization | Stable JSON encoding |
| T36 | Integrity checksum | Detect accidental drift |
| T37 | Budgeted compression | Bounded summary |
| T38 | Semantic loss audit | Detect missing meaning |
| T39 | Handoff capsule | Portable context packet |
| T40 | Session footer | Visible compact state |
| T41 | Cross-agent reconciliation | Evidence-based merging |
| T42 | Evolution feedback | Version and evaluate |

## Reference implementation

`experiments/session-cascade/omnitag.py` implements a deliberately small subset: basic admission and role validation, session IDs, local sequencing, flat tolerant tag parsing, bounded tag validation, SHA-256 event digests, deterministic folding/replay, canonical JSON, checksum and session footer. This **does not** implement 42 independent algorithms.

Example:

```python
from omnitag import SessionState, parse_tags
s = SessionState("demo")
s.ingest("user", "Please review PR-17", {"Ctx": "Review", "Ref": "PR-17"})
print(s.footer())
print(parse_tags("[Msg⛛{42}] [State⛛{Observed}]"))
```

## Semantics and security

- Preserve unknown tags in tolerant mode; strict mode may reject unparsed text.
- The flat parser does not claim nested grammar support. Nested tokens are a future technique.
- Session state is **local and ephemeral** unless an external caller explicitly stores it.
- Event content is not retained by the reference reducer, only SHA-256 digests. Digests are **not anonymization**, and low-entropy messages may be guessable.
- A checksum detects drift but does not authenticate authors or establish provenance.
- No secret-bearing tags, permission escalation, implicit agent memory, or hidden reasoning extraction.
- `[Act⛛{Merge}]` is metadata, not evidence of a merge.
- Reconcile with current organization topology before integration into NuSyQ-Hub. `OmniTagProtocol` is a migration rendezvous, not a replacement control plane.

## Implementation roadmap

**Phase A: lexical and state contract.** Expand grammar tests for Unicode, nesting, malformed tags, escaping, and versioned schema. Prove replay and atomic failure handling.

**Phase B: provenance and evidence.** Add typed claims, source references, time scope, capability receipts, conflict retention and privacy policy.

**Phase C: semantic transforms.** Implement alias graphs, deduplication, task/dependency extraction, budgeted summaries and semantic-loss checks. Evaluate on a public synthetic corpus, not private user chats.

**Phase D: handoff and interoperability.** Add exportable capsules, explicit approvals, adapter contracts and versioned migrations. Integrate only after live organization repository access is verified.

## Acceptance gates

1. Stdlib tests pass in CI on supported Python versions.
2. Strict/tolerant parser behavior is documented with fixtures.
3. Invalid event ingestion leaves the reducer unchanged.
4. Replay reproduces the same footer byte-for-byte.
5. Security review covers sensitive tags and content digests.
6. Any claims of remote deployment or merge carry actual tool receipts.

[Msg⛛{42}][State⛛{Proposed}][Act⛛{Review}]
