# Capability Re-entry Receipt

[Msg⛛{REENTRY-20261021}] [Ctx⛛{ColdStart}] [State⛛{Observed}]

This is a bounded, non-authoritative handoff template for agents resuming work after a context gap. It does not assert that any fleet host, build, or service is healthy.

## Claim ledger

| Surface | Claim | State | Evidence |
| --- | --- | --- | --- |
| GitHub connector | Read repository files | proven | OmniTag README.md, AGENTS.md, docs/PROTOCOL.md retrieved 2026-10-21 |
| GitHub connector | Read recent history | proven | OmniTag commit 7cee0672da23642275b64b748706c3dff9f2ac4d |
| GitHub connector | Read public issues | proven | OmniTag issue #2, #3, #4 |
| Local working tree | Clean and synchronized | unknown | No local git status/fetch/pull run |
| Dependency installation | Successful | unknown | No local dependency installation run |
| Build and regression tests | Passing | unknown | No test process run |
| Fleet Docker and agent harnesses | Healthy | unknown | No fleet host probe run |

## Re-entry sequence

1. Discover the default branch. Never assume it is `master`.
2. Inspect `git status --porcelain=v1` and preserve all uncommitted work and stashes.
3. Fetch remote refs; compare local HEAD with upstream before pulling. Avoid automatic merge/rebase on dirty trees.
4. Read `README.md`, `AGENTS.md`, `START_HERE.md`, `docs/PROTOCOL.md`, and current issue comments.
5. Record base SHA, issue/PR reference, environment, command, exit code, and timestamp for every validation claim.
6. Run project-specific dependency and build/test commands only after inspecting scripts and prerequisites.
7. Separate `proven`, `denied`, `unavailable`, `unknown`, and `not_required`. Never infer health from existence.
8. Create a reviewable branch for one bounded improvement, preserve failed-command evidence, and request review before merge.

## Suggested receipt

```text
[Msg⛛{REENTRY-ID}] [Task⛛{Resumption}] [Ref⛛{issue-or-pr}]
repo: owner/name
branch: actual-branch
base_sha: exact-sha
working_tree: clean|dirty|unknown
command: exact-command-or-not-run
exit_code: integer-or-not-run
state: proven|denied|unavailable|unknown|not_required
evidence: durable-reference-or-explanation
next_step: smallest-safe-action
```

## Non-goals

No automatic deployment, secrets collection, authorization escalation, fleet-wide administration, issue closure, or implicit merge. A public receipt must never reveal private host topology or credentials.

[State⛛{Proposed}] This document is a reusable example, not a report of completed local synchronization.
