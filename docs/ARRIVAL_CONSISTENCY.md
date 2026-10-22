# Arrival consistency and evidence checklist

[Msg⛛{ARRIVAL-CONSISTENCY-20261021}] [State⛛{Observed}]

## Verified documentation mismatch

At the time of review, `README.md` and `AGENTS.md` identify `omnitag.agent-beacon.json` as the machine-readable beacon. The newer `START_HERE.md` instead directs arrivals to `agent-beacon.json`. Use the former documented canonical path unless repository contents and validation establish a migration. This note records a documentation contradiction, not evidence that either file is missing.

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
