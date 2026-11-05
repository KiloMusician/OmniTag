# Radio catalog integration: session harvest (2026-10-23)

[Msg⛛{RADIO-CATALOG-HARVEST}] [State⛛{Proposed}] [Ctx⛛{External-Integration}]

## Provenance and scope
Harvested from a discussion about a friend's Telegram-controlled request-radio project. **The friend's repository was not supplied or identified.** This document is an interoperability handoff, not a claim that OmniTag owns the radio backend or that the Jamendo integration is deployed.

## Requirements extracted
- Listeners request tracks through Telegram; a backend resolves requests against a catalog and queues tracks for a playout worker.
- Prefer downloadable, non-DRM media where the provider grants suitable usage rights.
- Startup is based in Canada with near-zero budget.
- Reduce upstream calls using cached search, local metadata snapshots, queued sync, conditional refresh, backoff, and deduplication.
- Jamendo is the first proposed catalog adapter; Tribe of Noise is a candidate pending API/rights verification.
- No provider has been established to offer unlimited requests or unrestricted broadcast/download rights.

## Architecture decision candidate
Telegram webhook -> request validation -> catalog adapter -> canonical track index -> durable queue -> rights/entitlement gate -> playout adapter -> audit/event log.

Provider interface: search(query, limit, offset), get_track(id), resolve_playback(id), refresh_catalog(cursor). Separate metadata/search permissions from download, broadcast, public performance, and redistribution rights.

Canonical track: provider, provider_track_id, title, artist, duration, genre, source_url, license_id, attribution, provenance_timestamp, allowed_uses. Queue record: idempotency_key, requester_id, track_ref, status, created_at, retry_count, last_error.

## Critical correction to earlier draft
The prior illustrative Python code called `/tracks/file` using a JSON parser and expected `results[0].audio`. That response contract was **not verified** and may be a redirect/binary response. Do not merge or deploy the code without checking official documentation and integration tests. The earlier SQLite cache was synchronous, had no request coalescing, and the sample API had no Telegram authentication or durable queue.

## Novel Ideas & Investigations
### Provider-agnostic rights gate
- Priority: P1; Category: Architecture/Security; Effort: Medium
- Origin: DJ pool and internet radio are distinct licensing models.
- Impact: Prevents unauthorized download/airplay even when metadata search succeeds.
- Next: verify Canadian internet radio rights and provider agreements; test fail-closed authorization.
- Status: Logged.

### Request coalescing and idempotent queue
- Priority: P1; Category: Performance/Reliability; Effort: Medium
- Origin: User's concern about upstream API throttling.
- Impact: Multiple Telegram requests for the same song need not trigger duplicate upstream fetches or queue entries.
- Next: implement SQLite/Postgres unique idempotency keys and single-flight cache refresh in the actual backend.
- Status: Logged.

### Provider contract tests with offline fixtures
- Priority: P1; Category: Testing; Effort: Small
- Origin: Unverified `/tracks/file` assumptions in prior scaffold.
- Impact: Stops false-positive claims of working downloads.
- Next: assert redirect, JSON error, 429, timeout, missing track, and license-denied behaviors; run live smoke test only with authorized credentials.
- Status: Logged.

### OmniTag event envelope for radio requests
- Priority: P2; Category: Interoperability; Effort: Small
- Origin: Reusable event tracking across Telegram, provider, queue and playout.
- Example: `[Msg⛛{radio-request-42}] [Ctx⛛{RadioQueue}] [State⛛{Queued}] [Ref⛛{jamendo:123}] [Act⛛{Enqueue}]`
- Next: validate against existing OmniTag grammar; keep business data in JSON, tags as inspectable annotations.
- Status: Logged.

## Re-engagement notes
- GitHub accessible: `KiloMusician/OmniTag`, default branch `main`. Current observed HEAD: `6abd0a5b74c65e72127dda81eb467ea811dbcdcc` (2026-10-22).
- Public README explicitly describes this repo as a symbolic metadata/interoperability experiment, **not** an operational control plane. Therefore do not inject radio runtime code here.
- Friend's repo, build, dependencies, CI, issues and live API credentials: **unknown/not inspected**.
- No `git pull`, package install, or build performed on the friend's machine. No live Jamendo endpoint verified.
- Follow-up: identify the actual radio repository, inspect HEAD and open issues, then adapt to its existing stack before writing production code.

## Execution ledger
- Branch: `harvest/radio-catalog-integration-20261023`
- Changes: documentation-only harvest
- Tests: not run (no runtime code changed)
- Commits/PR: tracked by GitHub actions after this file is added.
