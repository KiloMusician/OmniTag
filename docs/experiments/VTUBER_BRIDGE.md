# VTuber bridge: session recovery and bounded experiment

[Msg⛛{VTUBER-01}] [Ctx⛛{Research}] [State⛛{Proposed}] [Ref⛛{Issue-22}]

## Provenance
Recovered from a 2026-10-21 user discussion about 'Visage/Vasage', VSeeFace, pricing, licenses, and integration with live streaming. Product identification for 'Visage/Vasage' remains uncertain. This is an architectural proposal, not a description of shipped code.

## Corrections
- VSeeFace is free-to-use Windows VTuber software, **not generally open-source** and not public domain.
- VRoid Studio is free avatar creation software, not a streaming platform.
- OBS Studio supplies streaming and composition; avatar software supplies rendering/tracking.
- Commercial-use terms, OSC/VMC details, VRM compatibility, and current prices must be verified against vendor documentation before implementation.

## Reuse-first integration
Webcam/audio/MIDI/chat inputs -> source-specific adapters -> normalized event bus -> VMC/OSC or engine adapter -> VRM avatar/Godot/OBS scene.

Proposed event envelope:
```json
{"schema_version":1,"source":"midi","timestamp_ms":0,"kind":"expression","name":"surprised","value":0.75,"actor_id":"local-avatar"}
```

Contract constraints: explicit schema version; normalized values in [0,1]; monotonic or documented timestamp basis; bounded queue; source allowlist; no camera frames in telemetry by default; separate opt-in for network transmission; safe fallback when tracking disconnects.

## First implementation slice
1. Research verified VSeeFace/VMC interoperability and licenses.
2. Specify typed event schema and validation tests, including malformed inputs and reconnects.
3. Prototype a local-only OSC adapter with synthetic events, no hardware requirement.
4. Add an OBS/Godot integration example only after verifying compatible runtimes.
5. Benchmark latency and CPU/GPU overhead before live-stream deployment.

## Not implemented
No running bridge, installed dependencies, end-to-end tests, or streaming integration is asserted here.

Tracking: https://github.com/KiloMusician/OmniTag/issues/22
