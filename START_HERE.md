# Start Here — OmniTag

OmniTag is the **public dialect** of the colony's tagging lineage (RSHT 2024 → MegaTag 2025 → OmniTag 2026): the inline notation `[Tag⛛{Value}]` for attaching governed, claim-stated metadata to text and artifacts. This repo holds the dialect's grammar and design laws.

**This is not the rendezvous repo.** `OmniTagProtocol` is a migration meeting point, not the spec. The spec lives here, in `docs/PROTOCOL.md`.

## Read first

1. `docs/PROTOCOL.md` — the grammar. This is the specification; everything else is commentary.
2. `omnitag.agent-beacon.json` — the machine-readable public agent beacon and contribution contract (not an authentication or identity credential).
3. The design laws, which are load-bearing, not slogans:
   - **symbol != authority** — a tag's presence grants nothing.
   - **presence != proof** — a claim stated is not a claim verified.

## The claim-state vocabulary

Every OmniTag claim carries one of five states. Using them precisely is the whole discipline:

`proven` · `denied` · `unavailable` · `unknown` · `not_required`

If you cannot class a claim, the honest state is `unknown` — never upgrade a claim because it would be convenient.

## Known gap — read before building on this

⚠ **No license is declared yet** (see issue #3). Until the operator rules, treat the dialect as all-rights-reserved: fine to use inside the colony, not cleared for external redistribution or embedding in third-party products.

## Lineage, briefly

- **RSHT** (Rosetta Stone Hyper Tag Syntax, 2024) — the archive corpus ancestor; its importer exists (KiloMusician/dev) but the legacy corpus import is a host-side task still pending, so the lineage is SUPPORTED, not VERIFIED, at the root.
- **MegaTag** (2025) — the heavyweight JSON knowledge-graph generation; spec and processors live in NuSyQ-Hub.
- **ΞNuSyQ practice** (current) — Msg⛛ correlation headers, numbered receipts, `omni://` registered targets; the lived dialect this repo distills.

## Colony context

- Colony Map + onboarding: Drive Hub, reference folder (`2026-10-18-muse-colony-map-onboarding.md`).
- Definition layer: Kilo_Core `README.md` + `CAPABILITY_ATLAS.md`; neutral registry: prime_anchor.
- Coordination: Slack HQ #handoffs (coordination only — GitHub is the record).
