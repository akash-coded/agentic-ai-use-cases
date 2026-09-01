# The Abstention Budget

> **One line:** an agent that never says "I don't know" is not confident, it is broken — and you should
> know its correct abstention rate before you launch.

Nobody sets a target for how often an agent should decline. So nobody notices when it declines never
(dangerous) or always (useless). This framework makes abstention a designed quantity.

---

## The four quadrants

|  | **Agent answered** | **Agent abstained** |
| --- | --- | --- |
| **Answerable** | ✅ Correct answer — the goal | ⚠️ **Timid**: unnecessary handoff, erodes trust in the agent |
| **Not answerable** | 🔴 **Confident-wrong**: the failure that ends projects | ✅ **Correct abstention** — also the goal |

Two of these are success. Note that they are *different* successes, and most evaluation only measures one.

## Setting the budget

Your correct abstention rate is a property of **your input distribution**, not of your model.

```
target_abstention ≈ ambiguous_inputs + out_of_scope_inputs + unretrievable_inputs
```

Sample 100 real inputs — real ones, from logs, not ones you invented — and classify:

| Class | Count | Correct behaviour |
| --- | --- | --- |
| Clearly answerable from available data | | Answer |
| Ambiguous — two defensible readings | | Abstain, state the ambiguity |
| Out of scope | | Refuse, route |
| Answerable in principle, data unavailable | | Abstain, say what is missing |
| **Target abstention rate** | | sum of rows 2–4 |

If your sample says 22% and your agent abstains on 3%, it is answering 19% of inputs it should not be.
That gap is where confident-wrong lives.

## The asymmetry that decides your threshold

Confident-wrong and timid are not equally bad, and the ratio is domain-specific:

| Domain | Cost of confident-wrong | Cost of timid | Bias toward |
| --- | --- | --- | --- |
| Refunds, policy, compliance | Very high | Low | **Abstention** |
| Internal search, drafting | Low | Moderate | Answering |
| Medical, legal, financial advice | Catastrophic | Low | **Heavy abstention** |
| Creative generation | Near zero | High | Answering |

Write your ratio down. It is the single most important number in your evaluation plan, and it is a
business decision, not an engineering one.

## Making abstention real

An abstention that reads like a failure will be prompt-engineered away by the next person who touches the
system. Make it a first-class output:

```
{ "decision": "abstain",
  "reason": "policy_ambiguous",
  "detail": "Fare rules permit two readings for involuntary changes on partially-flown tickets.",
  "route_to": "ops_lead",
  "what_would_resolve_it": "A ruling on clause 7.3(b) for partially-flown itineraries." }
```

The last field is what turns an abstention from a dead end into a work item.

## Measuring it

Your golden set needs an **abstention slice** where the correct answer is "I don't know". If it does not
have one, your evaluation cannot distinguish a careful agent from a lucky one.

- Target: ≥ 15% of golden-set cases should be correct-abstention cases
- Metric: abstention precision (of abstentions, how many were correct) and abstention recall (of cases
  needing abstention, how many were caught)
- Gate: abstention recall below threshold blocks release, same as any other metric

## The warning sign

> An agent whose abstention rate **drops** after a prompt change has usually not become smarter. It has
> become bolder. Check confident-wrong before celebrating.

## Where this shows up

- [Module 13](../../modules/13-agentic-qa-and-evaluation/) — golden sets and the gate
- [Sample evaluation plan](../../docs/prd/04-evaluation-plan.md) — 20 of 130 cases are abstention cases
- [Agent spec](../../docs/prd/02-agent-spec.md) — abstention as a designed behaviour

**Related:** [Grounding Triangle](grounding-triangle.md) · [Evidence Ladder](evidence-ladder.md) ·
[Silent Degradation Watchlist](silent-degradation-watchlist.md)
