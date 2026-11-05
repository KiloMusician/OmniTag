# Size-Constrained Games: Session Harvest (2026-10-23)

[Msg⛛{SIZE-GAME-HARVEST}] [Ctx⛛{Research}] [State⛛{Proposed}]

## Scope and provenance
This is a **research and design handoff**, not a verified world-record ranking, production benchmark, or implementation claim. Origin: operator discussion of games under 5 GB, 1 GB, 500 MB, 100 MB, 25 MB, 10 MB, 5 MB, 1 MB, 100 KB, 4 KB, and smaller, plus single-file games. Public OmniTag stores the compact interoperable receipt; game-specific implementations belong in an appropriate game repository.

## Concepts worth preserving
1. **Size ladder:** measure final shipped artifact across explicit decimal thresholds, recording platform, build flags, dependency policy, and whether runtime/browser/engine is included.
2. **Single-file challenge:** distinguish single source file, single distributable executable, and single HTML file; do not conflate them.
3. **Procedural synthesis:** compact seeds and generators can replace stored levels, textures, geometry, sound, and narrative variants; measure CPU and startup penalties.
4. **Dual-budget benchmark:** distinguish download/install size, peak RSS RAM, VRAM, disk expansion, runtime dependencies, and startup latency.
5. **Complexity-per-byte experiment:** define repeatable gameplay metrics (mechanics, unique interactions, playable minutes, deterministic seed coverage) instead of subjective 'infinite content' claims.
6. **Build-size CI:** compare artifact sizes with baseline and flag tier crossings; preserve a machine-readable result with exact commit SHA and build command.
7. **Technique comparison:** compare Godot, native, browser, and script runtimes using the same tiny playable design; record included/excluded engines fairly.

## Historically notable leads requiring independent verification
- .theprodukkt's **.kkrieger** (commonly described as a ~96 KB first-person shooter): inspect primary releases and distinguish compressed executable from runtime RAM.
- Demoscene 4K and 64K intro categories: not all entries are games.
- **js13kGames**: browser games with a 13 KB submission constraint; check current rules for precise counting.
- One-file HTML, Lua, Python, and executable experiments; check external interpreter/browser dependency.

## Investigation: reproducible size budget
**Hypothesis:** a shared measurement manifest can prevent misleading 'under N KB' claims.

Proposed fields: `artifact_path`, `sha256`, `bytes_on_disk`, `compressed_bytes`, `platform`, `build_command`, `engine_runtime_included`, `external_dependencies`, `peak_rss_bytes`, `peak_vram_bytes`, `startup_ms`, `seed`, `git_sha`, `measured_at`, `evidence_status`.

**Validation plan:** produce two reproducible tiny games (one HTML single-file, one Godot or native) with identical movement, collision, win condition and seed; measure using identical machine and documented tools. Verify hashes and size tiers automatically. Treat unmeasured metrics as unknown.

## Prioritized follow-ups
| Priority | Type | Next action |
| --- | --- | --- |
| P1 | Tooling | Draft portable size-measurement manifest and validation tests in game repository |
| P1 | Game design | Implement one-file playable prototype with deterministic seed |
| P1 | Performance | Compare disk size vs RAM/startup/CPU tradeoffs |
| P2 | Research | Verify notable historical examples and contest rules from primary sources |
| P2 | Architecture | Investigate optional compact OmniTag evidence receipt mapping, without making OmniTag a game engine |

## Context-gap / safety
Only the connected public `KiloMusician/OmniTag` repository was inspected for this contribution. Its README explicitly limits the repository to a public semantic metadata dialect and evidence-bearing handoffs, not an operational control plane. No private colony runtime, local Git checkout, build, or game-engine validation was available in this run. No current GitHub HEAD for other repos has been inferred.

## Handoff
Reuse the public protocol and existing validation workflow. Do not add an overlapping parser, game engine, or speculative autonomous system. Move executable prototypes to the proper game repository once identified. Keep all claims source-attributed and status-tagged.
