# Session recovery: terminal provenance, agent mediation and quest continuity (2026-10-22)

[Msg⛛{RECOVERY-20261022}] [Ctx⛛{Historical-session}] [State⛛{Proposal}] [Role⛛{Researcher}]

## Evidence and scope
Recovered from a historical ΞNuSyQ design conversation, **not** verified as currently implemented. This document is an idea-harvest and handoff, not an instruction to operate local processes. OmniTag remains a public symbolic interoperability experiment, not a local orchestration control plane. Do not move private host paths, credentials, logs or internal topology into this public repository.

## Distinct ideas and candidate owners
1. **Command provenance ledger** (P1; tooling): append-only structured records of terminal command, shell, cwd/repo, invocation class (once/setup/every-run), exit code, redacted stdout/stderr references, dependencies, and session ID. Prefer SQLite/JSONL for capture; pandas only for analysis. Shell history alone cannot reliably record all output. Candidate home: private NuSyQ-Hub ops tooling.
2. **Process-aware startup guardian** (P1; reliability): health-check Ollama HTTP service before launching; avoid duplicate servers and distinguish foreground blocking from freezes. Process IDs alone are not proof of readiness. Candidate: local operations manager.
3. **Human-readable agent intermediary** (P1; architecture): explain environment status, route authorized local-model queries, maintain explicit provenance and require approvals for side effects. Do not imply direct Copilot integration without a supported API. Candidate: private agent gateway.
4. **Context-aware ChatDev chamber** (P1; feature): load bounded repository context, isolate edits in a worktree, run tests, propose diffs and request review before integration. Candidate: private ChatDev adapter.
5. **Rosetta Quest graph** (P1; process): durable tasks with prerequisites, acceptance criteria, evidence, statuses and human approval gates; avoid duplicate work by linking canonical issues. Candidate: project issue tracker and private task service.
6. **Persistent multi-panel context UI** (P2; UX): local desktop/VS Code interface with service status, logs, task graph, agent threads and safe terminal actions. A UI view is not a source of authority.
7. **Context contracts and compendium** (P1; docs): machine-readable module purpose, dependencies, file ownership, context budgets, canonical references and decision history. Extend existing AGENTS.md / protocol rather than scattering duplicate guides.
8. **SCP-Drift classification** (P2; research): distinguish intentional narrative mode switches, accidental task derailment, recovered context, and unresolved ambiguity. Avoid claiming actual memory recovery from glyphs.
9. **QGL/Rosetta symbolic layer** (P2; interoperability): map ornate Unicode/conlang to plain-language semantic tags with normalization tests and explicit semantics. Glyph density is not quantum memory or guaranteed compression.
10. **Game-engine integrations** (P3; experimental): Godot and RimWorld experiments only after core provenance and sandboxing are proven.

## Candidate dependency sequence
Observe current repositories → verify existing owners/features → define provenance schema → instrument a single command runner → add process health checks → expose read-only dashboard → add quest graph → prototype one isolated agent task → review and integrate.

## Safety and duplication controls
- Do not automatically execute previously recorded commands.
- Redact secrets and personal data at capture time.
- Never infer a process is healthy from a stale status JSON.
- Preserve git worktrees and uncommitted changes; no unconditional pull/rebase.
- Keep machine-specific command logs and private memory outside this public repository.
- Link proposals to actual current issues before implementation.

## Investigation spike (design-only)
Example record:
```json
{"schema":1,"session":"local-session-id","shell":"pwsh","repo":"repo-alias","command_class":"every-run","argv_redacted":["python","-m","pytest"],"depends_on":["venv-ready"],"exit_code":0,"evidence":"local-log-id"}
```
Acceptance test for an eventual implementation: a command run twice creates two records with distinct event IDs; secrets never appear in either record; failed commands are recorded; dependencies refer to stable task IDs.

## Status / session accounting
- Historical session concepts extracted: 10.
- Local build, dependency install and regression tests: not performed, as GitHub connector does not provide a checked-out execution environment.
- GitHub HEAD and CI: require separate verification before any code implementation.
- This document is a proposed archival contribution, not proof of current implementation.
- Next owner: review for duplication with existing local NuSyQ-Hub and OmniTag issues, then create a focused implementation issue in the appropriate code repository.

[Act⛛{Review}] [State⛛{Evidence-bounded}] [Ref⛛{OmniTag-public-beacon}]
