# Session review: glyph codifier re-entry (2026-10-25)

[Msg⛛{SESSION-GLYPHOPS-20261025}] [State⛛{proposed}]

## Context-gap receipt

| Item | Evidence and limit |
| --- | --- |
| Live owner/repo | `KiloMusician/OmniTag`, public, writable via GitHub connector; default `main` |
| HEAD at orientation | `6abd0a5b74c65e72127dda81eb467ea811dbcdcc` (merged #25, lexemic rotation); recheck at merge |
| Current spec | `docs/PROTOCOL.md`; tags stay visible metadata, not execution or authority |
| Existing work | Draft PR #5 Unicode parser; #13 display profile; #30 flat scanner; merged #25 lexemic rotation; issue #36 Unicode tests |
| Working tree | GitHub API snapshot. No authenticated local checkout; direct container `git ls-remote` failed DNS resolution |
| Baseline | Recent existing `Validate public surface` workflow runs succeeded on other branches; no comprehensive main-branch clean build established |
| Local prototype | New `glyph_codifiers.py` and 14 new unittest cases passed in isolated Python container; public GitHub CI must independently confirm |
| Boundaries | No StockLens raw transcript, token, secret, private route, repository mirroring, or live-gateway availability claimed |

## Deliverables

| Change | Function |
| --- | --- |
| `experiments/glyph_codifiers.py` | unique semantic IDs; source-preserving Unicode overlays; digest-backed restoration |
| `tests/test_glyph_codifiers.py` | 14 deterministic stdlib unit tests |
| `docs/GLYPH_CODIFIERS_EXPERIMENT.md` | provenance, design, compatibility, admissions, non-goals |
| `.github/workflows/glyph-codifiers.yml` | scoped independent CI |
| This review | durable handoff |

## Novel ideas & investigations

### 1. Dual-view semantic packet, not a secret glyph decoder
- **Origin:** Screenshot-inspired conlang extrapolation.
- **Impact:** Machine ID, Unicode surface, human fallback, and raw preservation can coexist without sacrificing fidelity.
- **Priority/category/effort:** P1 / Feature / Medium.
- **Action/status:** Do now; opt-in prototype plus unit tests prepared. No canonical migration.

### 2. Truth-state separation for translations
- **Origin:** Prior conversation repeatedly inferred operational actions from screenshot text.
- **Impact:** `observed` glyph sequence, `proposed` semantics, and `proven` execution must never be collapsed. A visible HTTP status is an archived text observation, not a current health check.
- **Priority/category/effort:** P1 / Architecture+Security / Small.
- **Action/status:** Implemented `interpretation=proposed_not_evidence` in packets; document limits.

### 3. Semantic plane codifier governance
- **Origin:** Candidate P00–P50 families spanning operators, grammar, epistemics, permissions, resources, memory, telemetry, and Unicode rendering.
- **Impact:** Prevents collision between mathematics, religious imagery, program roles, execution policy and display skin.
- **Priority/category/effort:** P1 / Architecture / Large.
- **Action/status:** Prototype a collision-free 13-entry subset now; future schema/registry RFC; do not declare all 51 planes standardized.

### 4. Unicode shape is not identity
- **Origin:** Combining marks, supplementary glyphs, PUA, emoji sequences, glyph fog.
- **Impact:** Exact raw text survives NFC/NFD variance; terminal shaping cannot silently change bytes or claim meaning.
- **Priority/category/effort:** P1 / Testing / Small.
- **Action/status:** Source-preserving restore and tests; broader grapheme/fallback investigation remains.

### 5. Compression must be measured, not inferred
- **Origin:** Dense syntax promises compactness but Unicode tokenization may expand cost.
- **Impact:** Enables honest benchmark of readability and model token counts.
- **Priority/category/effort:** P2 / Performance / Medium.
- **Action/status:** Logged; PR #5 already includes an honest tokenizer baseline, reuse rather than replicate.

## Re-entry decisions

1. Do not modify canonical `[Tag⛛{Value}]` grammar. This is an **independent opt-in glyph overlay**, not a second OmniTag parser.
2. Work on a fresh branch from confirmed `main`, preserving every open PR and WIP branch.
3. No destructive merge, no branch reset, no cloud-runtime claims. Review CI and test evidence before promotion.
4. Do not reproduce unverified screenshot-derived endpoints or claim machine emergence/consciousness.

## Resume handoff

Check the linked PR/issue, compare HEAD with this session's orientation hash, run the new test suite and public validator, inspect CI, and reconcile with PR #30 and issue #36. If tests fail, preserve failure logs and fix the existing branch; avoid creating a competing parser. The proposed registry is intentionally versioned and not production authority.
