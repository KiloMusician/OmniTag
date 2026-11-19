# Arrival consistency and evidence checklist

[Msg⛛{ARRIVAL-CONSISTENCY-20261021}] [State⛛{Observed}]

## Resolved documentation mismatch (2026-10-21 finding)

On 2026-10-21, `README.md` and `AGENTS.md` identified `omnitag.agent-beacon.json` as the machine-readable beacon, while the newer `START_HERE.md` directed arrivals to `agent-beacon.json` — a path that returned 404 on `main`. The canonical path was verified to exist in the repository tree, and the entrypoint was corrected by #39 (squash commit `548c5af`, merged 2026-11-09); `START_HERE.md` on current `main` now names `omnitag.agent-beacon.json`. This section is retained as the historical record of the finding, not a live contradiction: use `omnitag.agent-beacon.json` unless repository contents and validation establish a migration.

## Cold-start verification checklist

1. Read `README.md`, `AGENTS.md`, `docs/PROTOCOL.md`, `START_HERE.md`, and `CONTRIBUTING.md`.
2. Verify the actual beacon filename and any referenced schema against the checked-out tree.
3. Record current branch, HEAD SHA, dirty-worktree state, and remote without changing or discarding local WIP.
4. Compare new commits and open issues/PRs against the last known checkpoint; distinguish superseded work from still-open work.
5. Run the repository's documented validation and CI checks. Report `proven`, `denied`, `unavailable`, `unknown`, or `not_required` separately.
6. Open a bounded issue or PR with observed evidence, tests where applicable, and explicit limitations. Never infer execution from a symbolic tag.

## Session scrape: reusable operational pattern

The re-engagement directive contributes a useful distinction between **orientation** (inspect current state), **reconciliation** (compare plans to HEAD), **execution** (small reviewable changes), and **handoff** (persist evidence). A session scrapbook should retain only new, source-attributed findings rather than duplicate a full conversation transcript.

Suggested receipt:

```text
[Msg⛛{arrival-001}] [Ctx⛛{Reorientation}]
[State⛛{Observed}] [Ref⛛{commit-sha-or-issue-url}]
Checks: <commands actually run>
Results: <outputs or links>
Unknowns: <unverified claims>
Next: <smallest useful reviewable delta>
```

This is documentation guidance, not an execution claim or authorization grant.
