# Historical four-lane recovery: Zeta-9, SystemRoot, feedback, Rosetta

[Msg⛛{HISTORICAL-RECOVERY-20261022}] [State⛛{Proposed}] [Ctx⛛{SessionArchaeology}]

## Provenance and scope

This note recovers **design intentions**, not claims of running systems, from the operator-provided historical files: `KardeshevPulse.txt`, `Overview.txt`, `lexicon.txt`, `GODOT.txt`, `GDscript.txt`, `Repository_Template.rtf`, `SystemRoot*.rtf`, and `ΞNuSyQ_MsgX_Protocol.txt`. These are historical session artifacts, not verified current source files. Do not treat symbolic notation as executable code, quantum hardware, authorization, or proof of runtime health.

Current public contract: `README.md`, `AGENTS.md`, `docs/PROTOCOL.md`, and `CONTRIBUTING.md`. Existing issue #32 already covers evaluation receipts/dependency graphs; avoid duplicate implementation. Existing parser work should be checked before writing a new parser.

## Four recovered lanes

| Lane | Historical signal | Bounded engineering target | Validation |
| --- | --- | --- | --- |
| Feedback kernel | Recursive feedback, temporal echo, neural loop, OmniTag state | Deterministic finite-state transitions with explicit inputs, limits, and audit receipts | Repeatability, termination, rollback, invalid input |
| Zeta-9 simulation | Planetary energy pulse, biome growth, settlement, resource and survival loops | Seeded simulation rules and Kardashev-inspired fictional progression, separate from scientific claims | Same seed = same world; conservation/accounting rules; capped updates |
| SystemRoot | Config, logging, fractal generation, persistence, visualization, API, authentication, testing, deployment | Dependency manifest and lifecycle graph mapping **existing** modules; no auto-created infrastructure | Missing-node detection, cycle detection, source-backed paths |
| Rosetta/OmniTag | Msg identifiers, symbolic lexicon, cross-agent handoff, Unicode glyphs | Reuse existing public grammar; optional provenance crosswalk for historical aliases | Unknown-tag preservation, Unicode roundtrip, no authority escalation |

## Recovered game-design material

The historical `Overview.txt` and `lexicon.txt` independently describe a multi-perspective Godot game: top-down exterior hack-and-slash, indoor side-scrolling Metroidvania, architect/RTS view, resource scavenging, visible equipment, crafting, city economy, survival, and eventual tower defense. Additional proposed systems include faction diplomacy, dynamic sound, day/night, procedural dungeons, NPC relationships, and multiplayer. Treat these as **candidate backlog** rather than completed mechanics.

The historical `GDscript.txt` is a conceptual class outline, not a validated Godot 4 runtime module. Historical `GODOT.txt` names Godot 4.3; the installed/current engine and project architecture must be checked before applying any version-specific instructions.

## Novel integration opportunity: typed evidence bridge

Introduce a **sidecar evidence record**, rather than a new magic tag, for each recovered claim:

```json
{
  "source": "historical:Overview.txt",
  "claim": "Dual perspective: indoor side-scroller, outdoor top-down",
  "classification": "design_proposal",
  "current_repository_ref": null,
  "verification": "not_measured",
  "next_action": "find existing implementation before opening feature work"
}
```

Classification vocabulary: `design_proposal`, `observed_code`, `measured_behavior`, `fictional_mechanic`, `superseded`. These classifications are proposed sidecar fields, **not** new normative OmniTag tags.

## Synchronization and execution gates

1. Inspect the current repository and issue/PR landscape; do not infer health from older notes.
2. Check branch protection, existing parser proposals, #32 scope, and relevant CI.
3. Verify baseline tests in an actual checkout/CI before changing runtime code.
4. Prefer one isolated, tested implementation PR per lane, preserving current architecture.
5. Never copy historical claims of “100% integrity,” “quantum activation,” or “system synchronized” into factual status reports without measurement.
6. Preserve private repository names, credentials, and topology outside public artifacts unless separately cleared for publication.

## Handoff

This file is a **public, non-secret archaeology receipt**. It intentionally does not introduce a new parser, duplicate issue #32, or modify runtime code. The next agent should reconcile existing implementations before selecting the first executable feature. No local build or test is claimed by this document.

[State⛛{Proposed}] [Act⛛{Review}] [Ref⛛{OmniTag-public-protocol}]
