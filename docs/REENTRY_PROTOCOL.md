# Re-entry evidence protocol for returning agents

[Msg⛛{REENTRY-20261021}] [Ctx⛛{ColdStart}] [State⛛{Proposed}]

This guide complements [AGENTS.md](../AGENTS.md) and [the protocol primer](PROTOCOL.md). It is a **public, capability-bounded** checklist for agents resuming work after a long gap. It is not an instruction to operate a private fleet or evidence that any machine is healthy.

## Phase 0: Identify your boundary

1. State which repository and branch you can actually read.
2. Record which tools are **proven**, **denied**, **unavailable**, **unknown**, or **not_required**.
3. Do not infer permissions from an agent role, tag, documentation, or an available connector.
4. Do not publish private topology, local paths, credentials, or private issue content.

## Phase 1: Reorient without destroying work

1. Inspect the current README, AGENTS.md, contribution policy, and recent changes.
2. Inspect branches, open PRs, and issues before creating duplicate work.
3. For a local checkout, inspect `git status --short` and `git branch -vv` before any update.
4. Prefer `git fetch --all --prune` followed by comparison. **Do not blindly pull, reset, clean, rebase, or discard uncommitted work.**
5. Identify the baseline build/test commands from current repository instructions, then run only commands supported by the accessible environment.
6. Record exact commands, commit SHA, result, and timestamp. A CI badge or a README statement is not a fresh test result.

## Phase 2: Reconcile a single work item

Compare the old plan against current files and open work. If superseded, preserve the useful context and link the replacement rather than closing another contributor's issue without evidence. Prefer one small, non-overlapping change with a clear acceptance test.

## Phase 3: Execute and verify

Use a dedicated branch. Make the smallest useful change, check adjacent edge cases, and run the appropriate validation. Separate **code inspection**, **unit-test success**, **build success**, and **visual/runtime playtest**: none proves the others. Open a draft PR if the work is useful but verification is incomplete.

## Phase 4: Leave an evidence-bearing handoff

```text
[Msg⛛{REENTRY-EXAMPLE}]
[Ctx⛛{RepositoryReorientation}]
[State⛛{Observed}]
[Ref⛛{owner/repository@commit-sha}]
[Act⛛{Inspect}]
[Err⛛{NoneObserved}]

Scope: one public repository and one bounded change
Last known baseline: unknown
Current revision: <record exact SHA>
Repository instructions read: <paths>
Work item: <issue or PR URL>
Changed paths: <paths or none>
Verification: <exact command and result, or not_run>
Unverified: <specific uncertainties>
Next safe action: <one concrete step>
Authority effect: none
```

Do not report `[State⛛{Healthy}]` unless a specific, current health check supports it. Prefer an explicit unknown to an invented success.

## Failure and fallback matrix

| Condition | Safe next step |
| --- | --- |
| Connector unreachable | Mark unavailable, try another authorized read surface, or leave a reproducible handoff |
| Build fails | Distinguish environment/dependency failure from source regression before editing |
| Local changes exist | Preserve and inspect them before any branch update |
| Issue already covered by PR | Link existing work; review or select a non-overlapping task |
| Tests cannot run | Record not_run, perform source review, and keep PR in draft |
| Permission denied | Stop that operation; do not bypass the boundary |
| Licensing or governance decision | Request the owner's decision rather than silently choosing |

## Contribution completion criteria

A re-entry is useful when it leaves at least one inspectable artifact: a tested patch, a draft PR, a reproducible issue, a specific review, or an evidence-backed handoff. The number of actions taken is less important than their accuracy and reviewability.

**Invariant:** `symbol != authority; description != execution; presence != proof; unknown > guessing`.

[Msg⛛{REENTRY-HANDOFF:authority_effect=none}]
