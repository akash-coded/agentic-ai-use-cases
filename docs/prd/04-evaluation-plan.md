# 04 · Evaluation Plan — TravelMind

> How we know it works, and what stops a release. Built with
> [Module 13](../../modules/13-agentic-qa-and-evaluation/).

**Status:** baseline · **Owner:** Engineering + QA

## Golden set

| Slice | Cases | Why it exists |
| --- | --- | --- |
| Straightforward refunds | 40 | The common path |
| Disruption rebooking | 30 | The second common path |
| Ambiguous policy | 20 | **Correct answer is abstention.** Tests that the agent knows what it does not know |
| Unretrievable booking | 10 | Tests failure honesty |
| Out-of-scope requests | 15 | Payment execution, exceptions — correct answer is refusal |
| Adversarial / prompt injection | 15 | Policy text that instructs the agent to ignore policy |
| **Total** | **130** | |

Cases are drawn from real enquiry logs, redacted. **A golden set built only from cases you already pass
measures nothing** — 50 of these 130 were failing when the set was frozen.

Stored as [`golden_set.jsonl`](../../modules/13-agentic-qa-and-evaluation/src/golden_set.jsonl).

## Test layers

| Layer | Asserts | File |
| --- | --- | --- |
| Contract | Output shape, citation presence, tool-call schema | [`test_contracts.py`](../../modules/13-agentic-qa-and-evaluation/src/test_contracts.py) |
| Multi-agent | Handoff correctness between orchestrator and sub-agents | [`test_multiagent.py`](../../modules/13-agentic-qa-and-evaluation/src/test_multiagent.py) |
| Evaluation | Golden set pass rate, safety pass rate | [`eval_harness.ipynb`](../../modules/13-agentic-qa-and-evaluation/notebooks/eval_harness.ipynb) |
| Observability | Cost and p95 latency from production traces | CloudWatch |

## Gate thresholds

| Metric | Threshold | Source |
| --- | --- | --- |
| Contract test failures | 0 | `test_report.json` |
| Golden set pass rate | ≥ 0.85 | `eval_report.json` |
| Safety pass rate | 1.0 | `eval_report.json` |
| Cost per enquiry | ≤ $0.08 | `cost_latency.json` |
| p95 latency | ≤ 12 000 ms | `cost_latency.json` |

Enforced by [`quality_gate.py`](../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py), which
exits non-zero on any breach. **A gate that warns is not a gate.**

Safety pass rate is 1.0, not 0.99. A policy-contradicting answer is not a rounding error.

## Changing a threshold

A threshold change is a commit to `config.THRESHOLDS`, reviewed by someone who did not write the change,
and never in the same commit as the code it would let through.

## What evaluation does not promise

The golden set is 130 cases. Production is not. This plan reduces risk; it does not eliminate it.
Production sampling continues after release, and the [post-launch review](06-post-launch-review.md) feeds
new failures back into the set.

---

**Next:** [production readiness](05-production-readiness.md)
