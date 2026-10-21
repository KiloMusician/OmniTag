# Re-entry evidence receipt

[Msg⛛{REENTRY-EVIDENCE-V1}] [Ctx⛛{AgentHandoff}] [State⛛{Proposed}]

This example documents a safe return to a changed repository. It is a **template**, not evidence that a build, fleet, or external service has been checked.

## Record

| Field | Value |
| --- | --- |
| Repository | `owner/repository` (replace with verified identity) |
| Baseline ref | `main` (confirm actual default branch) |
| Baseline commit | `unknown` until resolved from Git |
| Prior working commit | `unknown` until independently identified |
| Working tree | `unknown` until inspected |
| Dependency install | `not_required` for read-only orientation |
| Build | `unknown` until executed |
| Tests | `unknown` until executed |
| Issue assignment | `unknown` until verified |
| External runner | `unavailable` only if a connection attempt actually failed |

## Safe reconciliation

1. Read the repository's current arrival instructions and default branch.
2. Inspect status, uncommitted changes, remotes, and recent commits before pulling. A dirty tree is not permission to overwrite work.
3. Fetch references without changing working files. Compare the prior known commit with current HEAD; document any missing baseline as unknown.
4. Read changed dependency manifests, lockfiles, CI, migrations, and architecture notes.
5. Run the smallest reproducible baseline checks in an authorized runner; record commands, exit codes, environment, and commit SHA.
6. Recheck issue and PR status, including comments, before selecting work.
7. Make one bounded change on a new branch; verify it and submit for review.

Do not silently discard WIP, close issues, rebase shared branches, install untrusted dependencies, or claim build success without evidence.

## Example handoff

```text
[Msg⛛{REENTRY-001}] [Ctx⛛{RepositorySync}]
[State⛛{Observed}] [Ref⛛{owner/repository@<verified-sha>}]
Readme and contribution rules reviewed.

[State⛛{Unknown}] [Task⛛{BuildVerification}]
No authorized build runner was exercised.

[State⛛{Proposed}] [Act⛛{ReviewPR}]
One documentation-only change is awaiting review.
```

## Evidence checklist

For each claimed action, attach a durable reference or a command transcript with its exit status. Keep secrets and private infrastructure identifiers out of public receipts. If a tool is unavailable, distinguish that from authorization denial and continue with a genuinely independent lane.

**Invariant:** symbolic status is not operational proof. A green-looking receipt cannot replace an executed test.
