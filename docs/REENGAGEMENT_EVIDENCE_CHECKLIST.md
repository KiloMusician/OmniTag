# Evidence-first agent re-engagement checklist

[Msg⛛{REENGAGEMENT-EVIDENCE-v1}] [State⛛{Proposed}]

This public checklist supports cold-start contributors. It is not a fleet-health receipt or an instruction to bypass access boundaries.

## 1. Discover without mutating

- Identify the exact repository, default branch, working branch, and remote.
- Record the current commit SHA and the previous known SHA, if available.
- Inspect `git status --porcelain`, existing worktrees and stashes before pull, reset, checkout, rebase or clean.
- Read README, AGENTS, contribution rules, CI workflows and dependency manifests.
- Inspect open issues and PRs for duplicate or superseding work.

## 2. Synchronize safely

- Fetch remote refs when a working checkout is available.
- Do not blindly pull into a dirty tree or overwrite uncommitted work.
- Compare old and new refs, note renamed paths and breaking changes.
- Install dependencies only in an authorized environment after checking lockfiles and installation scripts.

## 3. Establish a baseline

Capture the exact commands, exit codes, environment, relevant commit SHA and log/artifact links for lint, tests and builds. Game-engine headless checks are not substitutes for editor/runtime playtests. A successful GitHub API read is not evidence that a local Docker daemon, agent harness or game is healthy.

## 4. Reconcile the work

Choose a bounded, non-duplicative issue. Preserve relevant WIP before creating a branch. Prefer a draft PR with evidence and explicit gaps. Do not close someone else's issue merely because it appears stale; verify resolution first.

## 5. Capability receipt

Use `proven`, `denied`, `unavailable`, `unknown`, or `not_required` independently for each surface. Include timestamp, actor, repo/ref, action, observed result, verification method, and rollback plan. Never include credentials or private topology in a public receipt.

```text
[Msg⛛{REENGAGE-RECEIPT}]
[Ctx⛛{ColdStart}]
[State⛛{Observed}]
[Ref⛛{owner/repo@sha}]
[Act⛛{Inspect}]
```

## 6. Handoff

State what was actually changed, what passed, what failed, what was not measured, and the next safe action. Distinguish proposed fixes from deployed fixes. Link issues and PRs rather than duplicating long histories.

## Non-negotiable invariants

`symbol != authority` · `description != execution` · `presence != proof` · `unknown > guessing`
