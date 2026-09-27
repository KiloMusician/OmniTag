# OmniTag Protocol Primer

[Msg⛛{OMNITAG-PROTOCOL-PRIMER}]

OmniTag is an extensible symbolic metadata notation designed to travel beside ordinary language.

Its canonical visual shape is:

```text
[Tag⛛{Value}]
```

The notation is deliberately simple. A tag names a semantic dimension; the value supplies the local payload.

## 1. Core examples

```text
[Msg⛛{42}]
[Ctx⛛{Review}]
[State⛛{Observed}]
[Ref⛛{PR-17}]
[Err⛛{Timeout}]
[Act⛛{Inspect}]
[Role⛛{Reviewer}]
[Time⛛{2026-09-26T10:00Z}]
```

These can be composed inline:

```text
[Msg⛛{42}] [Ctx⛛{Review}] [State⛛{Observed}] The schema and example disagree.
```

The sentence remains understandable if every tag is removed. That property is intentional.

## 2. Message identifiers

`[Msg⛛{X}]` is the best-known OmniTag form.

```text
[Msg⛛{1}]
[Msg⛛{2}]
[Msg⛛{3}]
```

A sequence can help trace conversation, packet, or handoff order. Sequence identifiers are metadata, not proof that all prior messages exist.

If a system detects a gap, it may annotate the gap explicitly rather than silently renumbering history.

## 3. Suggested public vocabulary

| Tag | Intended semantic dimension |
| --- | --- |
| `Msg` | message / transaction / packet identity |
| `Sess` | session identity |
| `Ctx` | context / intent |
| `State` | explicit state |
| `Ref` | external or durable reference |
| `Err` | error / failure class |
| `Act` | action, proposal, or observed operation |
| `Obj` | target object |
| `Role` | actor role |
| `Time` | time marker |
| `Date` | calendar marker |
| `Task` | task or phase |
| `Node` | graph node |
| `Edge` | graph edge |
| `Metric` | measured value |
| `Sem` | semantic meaning / interpretation |
| `Map` | mapping or projection |
| `Flow` | process / workflow state |

The vocabulary is extensible. This table is guidance, not a global registry.

## 4. Values

Values may be compact strings:

```text
[State⛛{Observed}]
```

or structured human-readable payloads:

```text
[Map⛛{old_name->current_name}]
[List⛛{alpha,beta,gamma}]
```

Keep values short enough that the tag still behaves like metadata rather than a second document.

When a value becomes complex, prefer a durable reference:

```text
[Ref⛛{issue-2}]
```

and put the rich content in the referenced artifact.

## 5. Nesting

Nesting is permitted when it genuinely compresses context:

```text
[Nest⛛{Outer:[State⛛{Observed}]}]
```

Avoid decorative nesting that increases decoding cost without adding semantics.

## 6. State vocabulary

For capability or reachability claims, OmniTag projects prefer causal precision:

```text
proven
denied
unavailable
unknown
not_required
```

Meanings:

- **proven**: directly exercised or supported by specific evidence;
- **denied**: an authorization or policy boundary explicitly refused the action;
- **unavailable**: the surface or service could not currently be reached;
- **unknown**: not measured;
- **not_required**: intentionally outside the current task.

A network outage is not a permission denial. An untested capability is not unavailable.

## 7. Authority model

OmniTag can describe authority but does not create it.

```text
[Role⛛{Reviewer}]
```

does not grant review rights.

```text
[Act⛛{Merge}]
```

does not merge anything.

```text
[State⛛{Healthy}]
```

does not prove health.

This is the core invariant:

```text
symbol != authority
description != execution
presence != proof
```

## 8. Security

Never place secrets directly in OmniTags.

Bad:

```text
[Auth⛛{actual-secret-value}]
```

Better:

```text
[Auth⛛{Required}]
[Ref⛛{secret-store-entry}]
```

Public OmniTag artifacts should not expose private topology, credentials, personal secrets, local filesystem paths that reveal sensitive information, or hidden system prompts.

## 9. Reasoning transparency

OmniTag can annotate conclusions, evidence, uncertainty, and short reasoning summaries.

It does **not** require a model to reveal private chain-of-thought or hidden internal reasoning.

Prefer observable summaries:

```text
[State⛛{Blocked}] [Err⛛{GatewayUnavailable}] Health probe could not connect.
```

## 10. Parser philosophy

A useful OmniTag parser should have two modes:

**Tolerant mode**

```text
unknown tag → preserve → display → continue
```

**Strict mode**

Validate a declared schema or profile when a downstream system explicitly requires it.

Tolerant mode is the better default for public interoperability because the vocabulary is intentionally extensible.

## 11. Plain-text interoperability

OmniTag is intentionally transport-light. It can live in:

- Markdown;
- issue comments;
- commit messages;
- logs;
- chat transcripts;
- JSON string fields;
- task receipts;
- documentation.

The surrounding transport remains responsible for identity, authentication, signatures, and execution.

## 12. Design test

Before adding a construct, ask:

```text
Does this compress meaning?
Can a human still inspect it?
Can an agent parse it without private context?
Does it preserve uncertainty?
Does it avoid inventing authority?
Will an old reader survive seeing it?
```

If the answer is yes, the construct probably belongs.

[Msg⛛{OMNITAG-PROTOCOL:human-readable∩machine-readable}]
