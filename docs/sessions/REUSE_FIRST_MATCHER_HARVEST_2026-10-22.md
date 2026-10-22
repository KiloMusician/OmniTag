# Reuse-first agent discovery: session harvest (2026-10-22)

[Msg⛛{20261022-REUSE-FIRST-HARVEST}] [State⛛{Proposed}] [Ctx⛛{AgentHandoff}]

## Scope and evidence
This harvest derives from a conversation about a legacy Lua vulnerability-title matcher, modernization, and a coding assistant that repeatedly creates redundant files. It is **not** evidence that the Lua matcher exists in this repository, nor that proposed code was executed. Live source checks found the public `AGENTS.md`, `README.md`, `scripts/validate_public_surface.py`, and an existing session review. Reuse those surfaces before adding an independent framework.

## Extracted concepts
1. **Repository retrieval before generation (P1):** Treat each request as a query against existing APIs, imports, tests, docs, issues, and integrations. Rank candidate modules by exact symbol/API match, dependency proximity, behavior and tests; return citations to actual paths and revisions.
2. **Evidence-bearing reuse decision (P1):** Before creating a new file, record the candidate files inspected, why extension is unsuitable, expected compatibility impact, and the smallest change that solves the task. New files are allowed when genuinely justified; no blanket ban.
3. **Context-gap recovery (P1):** On agent resumption inspect HEAD, working-tree state, recent commits, current issues/PRs, relevant build/test commands, and changed interfaces. Do not pull over uncommitted work or assume branch names.
4. **Matcher-inspired index (P2):** Reuse deterministic tokenization, literal matching, scoring and optional inverted indices for *repository discovery*, not for asserting vulnerability status. Exact package/version matching requires structured semantics rather than fuzzy numeric proximity.
5. **Duplicate-function detection (P2):** Search symbol definitions and call sites before implementation; report likely duplicates for human review, not automatic deletion.
6. **Provenance and handoff (P1):** Each claim should distinguish observed, inferred, proposed, implemented and verified; carry source ref, commit/branch, test evidence, and next action. Tags are metadata, never authority.
7. **Cross-language adaptation (P2):** Prefer existing Python, TypeScript, Godot/GDScript and other repo-native components. The Lua example is a *design analogy*, not a mandate to introduce Lua.

## Corrective findings about the earlier illustrative Lua starter
- Punctuation removal split `2.4.58` into separate tokens, contradicting a test expecting `2.4.58`.
- `gsub` strip terms were Lua patterns and could remove substrings inside unrelated words.
- The semicolon parser could truncate empty fields and did not implement quoted CSV.
- Missing DB and missing JSON dependency could be silently accepted, hiding invalid runs.
- `match_level` accepted L1-L4 while implementation always used L0.
- The benchmark repeated full-database ranking, so its reported unit was calls rather than entries.
- CI used `luacheck ... || true`, defeating the lint gate.
- The suggested configuration example contained comments, invalid in JSON.
These are review findings on conversation examples, not verified repository defects.

## Proposed agent loop
```text
OBSERVE current branch/HEAD and WIP
 -> DISCOVER existing functions, integrations and tests
 -> RANK candidate reuse paths with citations
 -> PLAN minimal compatible delta
 -> VERIFY baseline, targeted tests and integration effects
 -> IMPLEMENT in existing surface where possible
 -> TEST and document evidence
 -> HANDOFF with branch, commit, PR, blockers and next action
```

## Acceptance criteria for a future implementation
- Given a task with an existing implementation, an agent cites the implementation and extends it rather than inventing a duplicate.
- A new-file proposal includes search evidence and a justified exception.
- Candidate retrieval is measured on fixture tasks for recall, false positives, duplicate-file rate and time-to-working-change.
- No destructive fetch/pull/reset/merge against dirty trees without preserving WIP.
- The existing OmniTag public validator and protocol remain authoritative for this public surface; do not invent parallel registries.
- No claim of live GitHub, local IDE or colony runtime health without direct verification.

## Investigation status
Documentation-level design spike completed: adapted the title-matcher pipeline into a ranked repository-API discovery workflow, identified seven correctness traps in the prior example, and mapped it to existing agent onboarding. No code benchmark or live Copilot trial was performed.

## Handoff
Next: inspect existing issue/PR coverage for retrieval and reuse-first enforcement; implement a small fixture-based evaluation inside an appropriate existing repository after confirming language and test framework. Keep public OmniTag documentation free of private infrastructure details.
