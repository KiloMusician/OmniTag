# Evidence-bearing re-entry receipt (2026-10-21)

[Msg⛛{REENTRY-20261021}] [Ctx⛛{ColdStart}] [State⛛{Observed}]

## Scope
This is a bounded public interoperability example, not a health report for the private colony. It demonstrates how an agent should resume after a long absence without conflating retrieved documentation, live observations, and unverified assumptions.

## Evidence ledger

| Claim | State | Evidence |
| --- | --- | --- |
| Public repository default branch is `main` | observed | GitHub repository metadata retrieved 2026-10-21 |
| README identifies OmniTag as a public metadata dialect | observed | `README.md` on `main` |
| Protocol defines tolerant and strict parser modes | observed | `docs/PROTOCOL.md` on `main` |
| Public license selected | unresolved | Issue #3 explicitly reserves choice for human owner |
| Build and test suite currently pass | unknown | No local checkout or CI run was executed in this receipt |
| Local Docker fleet is healthy | unknown | No fleet runtime was inspected |
| This receipt grants operational authority | false | Symbols and documents do not grant permissions |

## Minimal re-entry algorithm

1. Discover the actual default branch; never assume `master`.
2. Read `README.md`, `AGENTS.md`, protocol and contribution instructions from that branch.
3. Compare against the last *verified* commit, if known; otherwise label the historical baseline unknown.
4. Inspect issues and PRs before creating new work.
5. Distinguish `observed`, `proposed`, `unknown`, `denied`, and `unavailable` in handoff notes.
6. Run build/tests in an authorized execution environment; record commands, exit codes, and commit SHA.
7. Make a small, reversible branch change, request review, and do not claim CI or runtime health without evidence.

## Machine-friendly receipt

```json
{
  "message": "REENTRY-20261021",
  "repository": "KiloMusician/OmniTag",
  "baseline_branch": "main",
  "observation_date": "2026-10-21",
  "documentation_read": ["README.md", "AGENTS.md", "docs/PROTOCOL.md"],
  "build": {"state": "unknown", "reason": "not executed"},
  "fleet": {"state": "unknown", "reason": "not inspected"},
  "license": {"state": "unresolved", "reference": "issues/3"},
  "authority_effect": "none"
}
```

This receipt is intentionally portable: a future agent can extend it with commit hashes, test results, and links to CI without rewriting historical uncertainty as success.
