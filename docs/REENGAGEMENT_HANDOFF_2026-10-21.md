# Cold-start evidence handoff (2026-10-21)

[Msg⛛{OMNITAG-REENGAGEMENT-20261021}] [State⛛{Observed}]

## Scope and evidence

A connected GitHub search identified `KiloMusician/OmniTag` (public, default `main`) and `KiloMusician/OmniTagProtocol` (private, default `Entrance-Hallway`). The public README, AGENTS.md and docs/PROTOCOL.md were fetched from OmniTag's default branch. These are repository observations, **not** proof of local checkout synchronization, CI health, Docker health, or deployment health.

## Operational lesson

Never assume `master` or `main` is universal. Resolve the actual default branch before selecting the base for a fetch, comparison, or pull request. Do not blindly `git pull` over dirty local worktrees. Capture `git status --porcelain=v1`, current branch, HEAD and remotes first. Fetch safely, compare against upstream, preserve uncommitted changes, then select merge/rebase deliberately.

## Verification vocabulary

- proven: directly observed or tested, with a reference;
- denied: explicit authorization failure;
- unavailable: service or surface could not be reached;
- unknown: not measured;
- not_required: deliberately out of scope.

## Restart checklist

1. Resolve repo and default branch, fetch, and inspect dirty state before any pull.
2. Record baseline SHA, dependency lockfiles, changes since last known SHA, and relevant documentation.
3. Run project-native validation and CI; report actual commands, exit codes, and environment.
4. Read issue comments and PR changes before declaring an assignment active or superseded.
5. Choose a small, reversible, tested change on a fresh branch; leave a durable handoff.

## Current limitations

No live machine build, Godot editor playtest, Docker probe, or full fleet synchronization was executed in this handoff. Those states remain **unknown**, not healthy. The public protocol remains a metadata dialect and does not grant operational authority.

## References

- [Public README](../README.md)
- [Agent arrival contract](../AGENTS.md)
- [Protocol](PROTOCOL.md)
- [Public contribution frontier](https://github.com/KiloMusician/OmniTag/issues/2)
- [Human licensing gate](https://github.com/KiloMusician/OmniTag/issues/3)

[State⛛{HandoffReady}] [Act⛛{Review}]
