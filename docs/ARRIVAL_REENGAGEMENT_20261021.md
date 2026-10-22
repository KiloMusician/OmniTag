# Agent arrival: evidence-first re-engagement receipt

[Msg⛛{ARRIVAL-20261021}] [Ctx⛛{Reorientation}] [State⛛{Partial}]

## Observed, 2026-10-21

- GitHub connector read `README.md`, `AGENTS.md`, `docs/PROTOCOL.md`, and `scripts/validate_public_surface.py` from `KiloMusician/OmniTag` default branch `main`.
- Repository metadata reported push permission for this account; this does not prove workstation or fleet access.
- `OmniTagProtocol` uses `Entrance-Hallway` as default branch, not `main`.
- An organization search surfaced `GSV-Sublime-Optimization/NuSyQ-Hub`, default `master`. No local git fetch, dependency install, build, engine playtest, or fleet health probe was performed in this receipt.
- The public protocol defines capability states: proven, denied, unavailable, unknown, not_required. Do not treat symbolic state tags as execution proof.

## Proposed reusable arrival sequence

1. Discover repository owner, visibility, default branch, and permissions; never assume `main` or `master`.
2. Inspect `AGENTS.md`, README, current issues/PRs, build instructions, CI, and branch protection before changing files.
3. Record last-known SHA and current SHA. Inspect changed files and migrations before pulling. Preserve dirty worktrees and stashes; use a new worktree if possible.
4. Run baseline lint/tests/build on the actual target runtime. Mark unexecuted checks **unknown**, not green.
5. Choose one bounded issue, reuse existing utilities, commit on a dedicated branch, open a reviewable PR.
6. Attach a handoff receipt with evidence URLs, checks executed, results, remaining blockers, and next actions.

## Example receipt

```text
[Msg⛛{arrival-001}] [Ctx⛛{Reorientation}]
[Ref⛛{owner/repository@branch}]
[State⛛{Partial}]
Observed: documentation fetched through GitHub connector
Unknown: local build, fleet Docker health, Godot playtest, CI baseline
Action: open a bounded PR; do not assert production readiness
```

## Open questions for follow-up

- Which organization repositories and project boards are the current work authorities?
- Which workstation and agent harnesses are reachable through explicitly authorized tools?
- Can the current validator be exercised in CI and checked against schema drift?
- Are there existing receipts for repository-specific build/test baselines?

This note is intentionally public-safe. It contains no private network topology, credentials, local paths, or unverified health claims. It is a documentation contribution, not an assertion that synchronization or fleet maintenance is complete.
