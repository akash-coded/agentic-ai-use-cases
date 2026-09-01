# 01 · Discovery PRD — TravelMind

> Produced after Gate 1. Establishes what good looks like, what it costs, and what would make us stop.

**Status:** approved at Gate 2 · **Owner:** Product + Architect

## 1. Problem statement

Refund and disruption enquiries follow published policy but require information from three systems
(bookings, fare rules, disruption feed). Staff resolution averages several minutes, dominated by lookup
rather than judgement.

## 2. Users and jobs

| User | Job to be done | Today | With TravelMind |
| --- | --- | --- | --- |
| Ops agent | Decide a refund against policy | Manual lookup across 3 systems | Decision + citation, verified by the agent |
| Ops lead | Audit a decision | Reconstruct from notes | Trace with policy citation |
| Customer | Get an answer | Waits | Waits less |

## 3. Scope

**In:** refund eligibility, disruption rebooking options, policy explanation with citation.
**Out:** payment execution, customer-facing chat, non-English, anything requiring a contract exception.

## 4. Agent classification

Ran the [four-quadrant classifier](../../modules/00-agentic-foundations/activities/H1-01_Four-Quadrant_Classifier.xlsx).
Result: **high autonomy need, low determinism** — the agent quadrant. Control flow depends on data
discovered at runtime.

Ran the [six-failure-pattern diagnostic](../../modules/00-agentic-foundations/activities/H1-04_Six-Failure-Pattern_Diagnostic.xlsx).
Two patterns scored high and are addressed in section 7.

## 5. Success metrics

| Metric | Target | Blocker threshold | Measured by |
| --- | --- | --- | --- |
| Autonomous resolution rate | 60% | below 35% | Golden set + production sampling |
| Policy-contradicting answers | 0 | any | Golden set, safety subset |
| Citation present on policy answers | 100% | below 100% | Contract test |
| Cost per resolved enquiry | < $0.04 | above $0.08 | Token accounting |
| p95 latency | < 6 s | above 12 s | Observability |

Blocker thresholds are wired into
[`quality_gate.py`](../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py). Changing one is a
reviewed commit, never an edit made to get a build through.

## 6. Cost model

Estimated with the
[token-cost calculator](../../modules/00-agentic-foundations/activities/H2-03_Token-Cost_Calculator.xlsx).
Four drivers, per the [HLD](../architecture/README.md#5-cost-model):

| Driver | Assumption | Control |
| --- | --- | --- |
| Tokens per turn | System prompt + tool schemas + retrieved policy | Cap retrieved passages; keep instructions short |
| Turns per enquiry | 3–5 model calls typical | Delegation, not swarm |
| Retrieval volume | top-k after rerank, capped | Context packing budget |
| Runtime and storage | Session memory, 30-day retention | Explicit TTL |

## 7. Risks

| Risk | Likelihood | Mitigation | Owner |
| --- | --- | --- | --- |
| Answers from parametric knowledge, not policy | High | Mandatory citation; contract test fails without one | Engineering |
| Stale policy after a document change | Medium | Ingestion freshness check in the gate | Engineering |
| Silent quality drop after model failover | Medium | Log the answering model on every response | Engineering |
| Scope creep to payment execution | Medium | Explicitly out of scope; requires a new Gate 1 | Product |

## 8. What would make us stop

- Autonomous resolution below 35% on the golden set after two tuning rounds
- Any policy-contradicting answer that citation checking does not catch
- Cost per resolved enquiry above $0.08 with no path down

## 9. Open questions

1. Does the fare-rules system expose a stable API, or are we scraping? — **blocks** the technical design
2. Who owns the policy corpus and its update cadence? — **blocks** the freshness check
3. What is the human-handoff SLA when the agent abstains?

---

**Gate 2 outcome:** proceed to [agent spec](02-agent-spec.md). **Condition:** questions 1 and 2 answered first.
