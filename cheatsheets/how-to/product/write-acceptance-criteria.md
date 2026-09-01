# How to · Write acceptance criteria for a non-deterministic system

**Time:** 2 hours with a domain expert. **You need:** 30 real inputs.

Ordinary acceptance criteria are pass/fail on a single case. Agent criteria are **rates on a defined set**.
Get this wrong and you will spend the project arguing about whether "it feels right".

---

## 1. The shape

```
❌  "The agent gives accurate answers about refund policy."
❌  "The agent should handle most enquiries correctly."

✅  "On the 130-case refund golden set:
     - ≥85% resolved with the correct decision
     - 100% of policy claims carry a citation to a passage that supports them
     - 100% of the 20 safety cases handled correctly (no policy contradiction)
     - ≥90% of the 20 ambiguous cases result in abstention, not a guess
     - Cost per resolved enquiry ≤ $0.08"
```

Five numbers, one named set. Every one is arguable, which is exactly what makes them useful.

## 2. The set is the specification

You cannot write the criteria without the set. Build it from **real inputs**:

| Slice | Share | Correct behaviour |
| --- | --- | --- |
| Clearly answerable | ~50% | Answer, with citation |
| Ambiguous | ~15% | **Abstain**, stating the ambiguity |
| Out of scope | ~10% | Refuse, route to a human |
| Data unavailable | ~10% | Say what is missing |
| Adversarial | ~10% | Resist, including injection via retrieved documents |
| Currently failing | ≥15% | Whatever correct is — these are why the set is honest |

> A set built only from cases the agent already passes measures nothing. Insist on the last row.

## 3. Separate the numbers that are averages from the ones that are not

| Criterion | Type | Why |
| --- | --- | --- |
| Resolution rate | Average, ≥85% | Some failures are acceptable |
| Citation presence | **Absolute, 100%** | An uncited policy claim is a defect, not a miss |
| Safety slice | **Absolute, 100%** | Not 99%. A policy contradiction is not a rounding error |
| Cost per task | Average, ≤ $X | Individual variation is fine |

Mixing these is the most common error. If safety is averaged into a headline number, a safety failure can
be hidden by good performance elsewhere.

## 4. Include abstention as a success criterion

An agent that never declines is not confident; it is dangerous. Write the target explicitly:

```
Abstention rate: 20–30% of enquiries.
  Below 20% → investigate confident-wrong before celebrating.
  Above 30% → investigate retrieval quality.
```

Derive the number from your own input distribution — see
[Abstention Budget](../../frameworks/abstention-budget.md).

## 5. Define what a failure looks like

For each criterion, one sentence on what happens when it is missed:

| Criterion missed | Consequence |
| --- | --- |
| Resolution < 85% | Launch delayed; not a safety issue |
| Citation < 100% | **Blocks release** |
| Safety < 100% | **Blocks release, and triggers a review of the whole slice** |
| Cost > $0.08 | Launch with a cost-reduction plan and a review date |

Not every miss is equal. Say which are blockers, in advance, in writing.

## 6. Write the kill criteria at the same time

```
We stop this project if, after two tuning rounds:
  - resolution stays below 35%, or
  - cost per resolved enquiry stays above $0.15, or
  - any policy-contradicting answer survives citation checking
```

Written at the start this is confidence. Written at the end it is a negotiation.

## The template

```markdown
## Acceptance criteria

Measured on: [set name], [N] cases, frozen [date], built from [source].

| # | Criterion | Type | Bar | Blocks release? |
|---|-----------|------|-----|-----------------|
| 1 | Resolution rate           | avg | ≥85% | No |
| 2 | Citation presence         | abs | 100% | Yes |
| 3 | Safety slice              | abs | 100% | Yes |
| 4 | Abstention rate           | band| 20–30% | No |
| 5 | Cost per resolved enquiry | avg | ≤$0.08 | No |
| 6 | p95 latency               | avg | ≤12s | No |

Kill criteria: [...]
```

**Related:** [Evidence Ladder](../../frameworks/evidence-ladder.md) ·
[Abstention Budget](../../frameworks/abstention-budget.md) ·
[Sample evaluation plan](../../../docs/prd/04-evaluation-plan.md)
