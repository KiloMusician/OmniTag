# Cyber Xianxia / Wan Jian Gui Zong — Session Harvest (2026-10-23)

## Status
Conversation-generated prototype, not runtime-tested. No build, webcam validation, FPS benchmark or deployment confirmed.

## Product boundary
Standalone game/demo, separate from the colony's software-development tools. Reuse gesture classification, swarm formations and effects as libraries later.

## Requirements preserved
Single-file HTML5 ES6 Three.js + MediaPipe Hands (two hands, complexity 1, detection .7, tracking .6), 300 procedural cyan jian swords, golden qi, mist, bloom, shockwave, camera shake, synthesized audio, optional debug controls. Gestures: no hands idle; both open defensive ring; both fists converge in .4s then attack; single-hand point directs beam; clockwise two-hand rotation vortex; hands apart 180-degree fan; hands together giant sword. Desktop webcam first; mobile touch fallback bonus; 60 FPS RTX 3060-class target; under 2MB local source target.

## Static-review findings (not runtime verified)
1. P1 Startup: MediaPipe script loading occurs outside webcam initialization try/catch, so CDN failures may leave loading overlay stuck.
2. P1 Gesture priority: together is evaluated before bothFist, so close fists select GIANT rather than ATTACK.
3. P1 Gesture thresholds: absolute landmark distances are not normalized by palm size; add joint angles and hysteresis.
4. P1 Performance: per-sword hot loop allocates Vector3, Matrix4 and Color objects; pool scratch values and benchmark.
5. P1 Tracking: lastResults has no stale-result timeout; gestures can latch after inference stalls.
6. P2 Trails: one glowing point per sword is not a persistent trail; use ring-buffer history or ribbons.
7. P2 Giant: overlapping instances do not form a distinct cohesive sword; use a procedural giant mesh.
8. P2 Effects: impact burst condition can fire on every frame; gate one-shot triggers.
9. P2 Debug: optional dat.gui dynamic import should be verified independently and have a fallback.
10. P2 Dependencies: Three.js is pinned at 0.164.1 despite latest requested; benchmark versions and count CDN/model bytes separately.

## Novel Ideas & Investigations
### Gesture-to-formation state machine
Priority P1; Architecture/Game Design; Medium effort. Split landmark classifier, normalized confidence, debounced transition logic and formation controller. Origin: gesture priority collision. Impact: deterministic tests and reusable input. Next: synthetic landmark state tests. Status: logged.

### Camera-free cultivation mode
Priority P1; Reliability/Testing; Small-Medium effort. Keyboard/mouse and prerecorded landmarks feed the same intent API, permitting CI smoke tests and no-webcam use. Origin: hard startup camera dependency. Next: implement fallback. Status: logged.

### GPU-friendly sword trails and pooling
Priority P1; Performance; Medium effort. Ring-buffer history per sword and preallocated math, with CPU/GPU baseline profiling. Origin: allocations and point-only trails. Next: benchmark 300 swords with bloom. Status: logged.

## Investigation performed
Static inspection of the previous conversation's pickMode logic confirms together precedes bothFist. Proposed regression: two fists with palm distance under .85 world units should trigger ATTACK when fist intent takes priority. This is an inferred test, not an executed test.

## Re-engagement handoff
Canonical game repository and current HEAD not yet established. Find existing standalone game repo before creating another. Reconcile with HEAD, issues, PRs, dependency manifests, CI and actual browser behavior. This harvest PR changes documentation only. No codebase build or tests have been run.
