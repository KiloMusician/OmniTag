# Re-entry evidence handoff (2026-10-21)

[Msg⛛{REENTRY-EVIDENCE-20261021}] [Ctx⛛{AgentHandoff}] [State⛛{Observed}]

This is a reusable cold-start checklist for an agent returning after an unknown context gap. It is a proposal for evidence handling, not an instruction granting repository or machine authority.

## State matrix

| Check | Evidence required | If missing |
| --- | --- | --- |
| Identity and access | repository, authenticated principal, granted operations | unknown |
| Branch and working tree | default branch, HEAD SHA, status, stashes | unknown |
| Remote changes | fetch result, merge base, commit diff, changed files | unknown |
| Baseline | exact build/test command, exit code, environment | unverified |
| Issue ownership | issue link, latest comments, current assignee | unverified |
| Runtime | host, container, extension or harness probe with timestamp | unverified |

Never infer a passing build from a successful API request. Do not pull into a dirty tree, discard work in progress, or publish private paths and secrets in a public handoff.

## Resumption receipt

```text
[Msg⛛{REENTRY-RECEIPT}]
[Ctx⛛{RepositoryResumption}]
[State⛛{Observed|Blocked|Unverified}]
[Ref⛛{repository@commit-or-issue}]

observed_at_utc: <timestamp>
repository: <owner/repo>
base_ref: <branch>
head_sha: <sha or unknown>
working_tree: <clean|dirty|unknown>
remote_sync: <fetched|not_fetched|unavailable>
baseline_command: <command or not_run>
baseline_exit_code: <integer or unknown>
issue: <URL or unassigned>
blockers: <specific observed evidence>
next_safe_action: <bounded action>
```

## Safety and continuity

1. Read the current README, AGENTS, contribution rules, and relevant issue comments before editing.
2. Compare previous assumptions against current paths and commits. Do not automatically rebase or discard WIP.
3. Prefer one reversible branch and one focused change; test before proposing a PR.
4. Record **observed**, **inferred**, and **unknown** separately.
5. If a gateway is unavailable, try an authorized alternate read/write surface. Report that surface's actual scope rather than claiming the whole fleet is healthy.
6. Keep public receipts free of internal network topology, credentials, and private issue content.

This document is intentionally platform-neutral and requires no new dependency.

[Msg⛛{REENTRY-EVIDENCE:authority_effect=none}]
