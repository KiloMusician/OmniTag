# Investment engine session harvest | 2026-10-23

[Msg⛛{INVESTMENT-ENGINE-HARVEST-20261023}] [Ctx⛛{Research}] [State⛛{Proposed}]

## Scope and placement
This document preserves design learnings from an investment automation discussion. It is **not** a live trading system, profit claim, broker authorization, or request to put finance execution inside OmniTag. Recommend a standalone investment-engine repository, with optional OmniTag metadata interoperability. The colony may orchestrate research but must not control brokerage secrets or bypass risk approval.

## Recovered requirements
- Start with unlevered, liquid equity/ETF strategies at weekly/monthly horizons; benchmark against buy-and-hold, cash, and simple passive allocations. This is a hypothesis, not a promise of superior returns.
- Each edge requires an economic rationale, falsification conditions, timestamped point-in-time data, source/license provenance, realistic spreads, fees, slippage, dividends, delistings, and corporate-action treatment.
- Use purged/embargoed walk-forward validation where applicable, untouched holdout data, multiple-testing controls, market-regime stress, and post-selection uncertainty reporting.
- Separate signal intent, portfolio target, independent risk approval, and broker order execution. Deny by default on stale feeds, missing risk state, broker mismatch, and unexpected positions.
- Research -> backtest -> shadow/paper -> capped live requires explicit promotion evidence; no automated live deployment merely because backtests improve.
- Champion/challenger and rollback; allow deactivation or cash allocation; forbid leverage escalation to recover losses.
- Append-only audit receipts for data snapshot, hypothesis, code commit, model hash, cost assumptions, validation report, order rationale, fills, reconciliation and incident response.
- Separate secrets and legal/tax compliance. Check Canadian account rules, broker access, regulatory implications, and data vendor terms before any live use.
- Do not assert 8-15% or other target returns as reliable forecasts; past and simulated returns are not guaranteed.

## Candidate ecosystem (verify license, maintenance and API versions before adoption)
LEAN, Qlib, zipline-reloaded, Optuna, MLflow, QuantStats, Great Expectations, Evidently; CCXT and Hummingbot only if crypto is later authorized. GPL or source-available dependencies require a licensing review. None is an established alpha source.

## Proposed bounded RFC: evidence-bearing investment decision receipt
Example **metadata only**, not executable instructions:

```json
{
  "msg": "INV-DECISION-0001",
  "context": "paper-research",
  "state": "proposed",
  "source_snapshot_sha256": "<hash>",
  "strategy_version": "<commit>",
  "signal_asof_utc": "<timestamp>",
  "validation_receipt": "<artifact-ref>",
  "risk_decision": "DENY",
  "risk_reason": "no-live-authorization",
  "order_id": null
}
```

Critical distinction: **OmniTag labels do not grant financial authority**. Risk decisions must be verified by independent code and broker-side controls, not interpreted from text tags.

## Novel ideas and investigations
### 1. Independent capital authority boundary
- Priority P0; category Security/Architecture; effort Medium.
- Origin: risk of conflating colony self-improvement with trading authority.
- Next: standalone RFC and threat model; fail-closed approval state machine.
- Status: documented.

### 2. Negative-result promotion gate
- Priority P1; category Research; effort Medium.
- Origin: optimizer can improve in-sample results while destroying out-of-sample performance.
- Next: test a no-trade challenger and passive benchmark, and block promotion unless evidence exceeds predeclared hurdle after costs.
- Status: documented.

### 3. Evidence receipt interoperability
- Priority P2; category Protocol; effort Small.
- Origin: OmniTag's evidence-bearing handoff design.
- Next: prototype JSON schema and round-trip test for non-authoritative research receipts.
- Status: documented; proposed only.

### 4. Temporal data integrity contract
- Priority P1; category Data/Testing; effort Large.
- Next: point-in-time fixtures for revisions, splits, delistings, stale feeds and holiday calendars.
- Status: documented.

## Reorientation receipt
- Confirmed public KiloMusician/OmniTag default branch main via GitHub connector.
- Read README and recent commit summaries; observed explicit public-beacon boundary and lack of declared public license.
- No verified access to the colony's private codebase from this repo inspection; no claim of full fetch/pull, dependency installation, clean build or baseline tests.
- No brokerage connections, live orders, or deployment attempted.
- Handoff: locate existing finance initiative across authorized repos before creating a standalone repository; avoid duplication.

## Proposed implementation phases
1. Inventory actual repository ownership and existing finance work.
2. Draft independent finance threat model and requirements, then create or identify standalone repository.
3. Implement reproducible historical-data ingestion and fail-closed risk contracts with tests.
4. Validate passive baselines and simple hypothesis under costs, walk-forward and stress.
5. Paper-trade with reconciliation and alerting; require human sign-off for any live capital.
