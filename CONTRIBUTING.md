# Contributing to OmniTag

OmniTag welcomes contributions from humans, coding assistants, autonomous agents, reviewers, researchers, and tool builders.

The preferred unit of contribution is not “a grand redesign.” It is **one useful, bounded, reviewable improvement**.

[Msg⛛{OMNITAG-CONTRIBUTING}]

## Before you start

Read:

1. `README.md`
2. `docs/PROTOCOL.md`
3. `AGENTS.md` if you are acting through an AI agent or automation

Then check the public contribution frontier:

https://github.com/KiloMusician/OmniTag/issues/2

## Good contributions

Useful work includes:

- protocol clarifications;
- examples;
- parsers and validators;
- JSON Schema improvements;
- interoperability experiments;
- tests;
- documentation;
- contradiction or ambiguity reports;
- accessibility and readability improvements;
- compact handoff formats;
- comparisons with other public annotation or agent protocols.

A read-only analysis can be a complete contribution when it is reproducible and actionable.

## Contribution shape

Prefer:

```text
problem
→ smallest useful delta
→ evidence
→ compatibility note
→ PR / issue
```

A PR should answer:

- What becomes easier or more precise?
- What existing behavior is preserved?
- What did you verify?
- What remains unknown?
- Does the change add a new tag or reinterpret an existing one?

## Protocol evolution rules

New tags should be:

- short;
- legible without a decoder;
- semantically narrow;
- tolerant of older readers;
- optional unless the protocol explicitly promotes them.

Prefer composition over synonyms. If `[Ref⛛{...}]` already expresses a durable reference, do not introduce a second tag merely for stylistic novelty.

Do not make a symbol authoritative merely by documenting it.

## Agent-originated work

Agent-authored contributions are welcome.

Please keep them reviewable:

```text
agent identity / lane when useful
+ source references
+ exact changed files
+ verification performed
+ unresolved uncertainty
```

Do not claim tests ran when they did not. Do not describe an external service as healthy because its tool name exists.

## Compatibility

Readers should be able to ignore an unfamiliar OmniTag and still understand the surrounding text.

That gives the project a useful compatibility law:

```text
unknown tag
→ preserve
→ display
→ continue
```

Parsers should prefer graceful preservation over destructive rejection unless a strict validation mode is explicitly requested.

## Security and privacy

Read `SECURITY.md`.

Never put credentials, private keys, authentication tokens, personal secrets, or private-system topology into public tags, examples, issues, or PRs.

## Licensing

This repository does not yet declare a public software/content license.

Until a human owner selects one, do not assume permission to redistribute material outside the rights GitHub itself provides. Contributions may be reviewed and discussed, but the licensing state should remain explicit rather than inferred.

[Msg⛛{CONTRIBUTION:bounded+reviewable+evidence-bearing}]
