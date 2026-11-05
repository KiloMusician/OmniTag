# Historical session extraction: recursive calibration (2026-10-21)

[Msg⛛{REENGAGE-20261021}] [Ctx⛛{HistoricalReview}] [State⛛{Proposed}]

## Provenance
Historical ΞNuSyQ random-topics conversation, Msg⛛{2}, supplied by the operator. This is a source-attributed *design extraction*, not a claim that the proposed modules exist in software.

## Distinct ideas worth retaining
- **Assumption dissection:** enumerate premises and mark which are evidenced, inferred, or unknown.
- **Oppositional layering:** deliberately formulate a competing interpretation before accepting a conclusion.
- **Counterfactual stress analysis:** ask which evidence would falsify a hypothesis.
- **Structural plausibility collapse testing:** reject internally inconsistent explanations before elaboration.
- **Chronological memory anchors:** connect claims to message IDs, timestamps, and durable references; never imply complete recall from a sequence number.
- **Response verification:** report a short evidence summary, unresolved uncertainties, and actionable next checks.

## Compatible mapping onto the current public protocol
Do **not** introduce redundant tags. Reuse `Msg`, `Ctx`, `State`, `Ref`, `Act`, `Time`, and `Metric` from docs/PROTOCOL.md.

Example:

```text
[Msg⛛{CAL-1}] [Ctx⛛{HypothesisReview}] [State⛛{Proposed}]
Claim: the issue is caused by a dependency upgrade.
[Ref⛛{build-log-17}] Evidence: the first failure appears after the upgrade.
[Act⛛{CompareBaseline}] Counterexample: test the same revision with the old dependency lockfile.
[State⛛{Unknown}] Root cause remains unverified.
```

## Engineering experiment
Build a small **calibration receipt** checker that verifies each claim has:
1. a provenance reference or an explicit unknown marker;
2. at least one falsification or alternative hypothesis for nontrivial decisions;
3. a measurable stop condition;
4. an explicit outcome (proven, denied, unavailable, unknown, or not_required).

Suggested tests: missing reference, unsupported certainty, contradictory states, unknown extension tags, and a valid multi-message handoff. Preserve original text in tolerant mode.

## Historical correction
The GTA VI exchange in the same session supplied a precise day count based on an approximate 2014 development start, without a documented start day. That count should **not** be reused as a verified day-accurate historical fact. Distinguish early conceptual work from full production, and only compute exact day counts from an explicitly dated anchor.

## Boundaries
- Recursive calibration is a methodology, not evidence of autonomous learning or quantum computation.
- Symbolic labels are metadata, not executable instructions or authority.
- Do not require disclosure of hidden reasoning; request concise, observable justification instead.
- No repository build or test execution is claimed by this historical extraction.

## Next implementation slice
Create a deterministic example-driven validator or fixture suite for calibration receipts, then connect it to the existing public-surface CI only after checking the current validator architecture.

[State⛛{Proposed}] [Act⛛{Review}]
