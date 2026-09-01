# How to · Turn a business process into an agent specification

**Time:** 2–3 days. **Output:** a spec engineering can build from and QA can test against.

---

## 1. Document the real process, not the documented one

Take ten real cases and trace each end to end. Ask for each:

- What information did the person need, and where did they get it?
- What decision did they make, and on what basis?
- What did they do when they were not sure?
- How long did it take, and where did the time go?

> The gap between the described process and the real one is where every agent project meets reality. The
> described process has no exceptions. The real one is mostly exceptions.

## 2. Separate decision from lookup

| Activity | Usually |
| --- | --- |
| Finding information across systems | **Where the time goes** — good agent territory |
| Applying a documented rule | Deterministic — a workflow, maybe not an agent |
| Judgement between defensible readings | Human, or agent abstention |
| Exception handling | Human |

If the time is dominated by lookup and the decision is mostly rule-application, you may have a workflow
rather than an agent. That is a good finding, not a disappointing one — see
[Autonomy Ladder](../../frameworks/autonomy-ladder.md).

## 3. Derive the tool list from the lookups

Each place the person went for information becomes a candidate tool:

| Person did | Tool | Reads or writes? |
| --- | --- | --- |
| Opened the booking system | `get_booking` | Read |
| Checked fare rules | `get_fare_rules` | Read |
| Looked up disruption status | `get_disruption` | Read |
| Issued the refund | — | **Write — keep this human** |

Note the last row. Recommending is green; committing is not. See
[Blast Radius Grid](../../frameworks/blast-radius-grid.md).

## 4. Write the behaviour contract

| The agent must | The agent must never |
| --- | --- |
| Cite the policy supporting any claim | Answer a policy question without a citation |
| Abstain when policy is ambiguous | Guess at an ambiguous case |
| State when data could not be retrieved | Proceed on assumed data |

This table is the most useful single artefact you will produce. It is testable line by line.

## 5. Define escalation

| Trigger | Route to | SLA |
| --- | --- | --- |
| Policy ambiguous | Ops lead | |
| Booking not retrievable | Support queue | |
| Out of scope | | |
| User asks for a human | Immediately | |

If the organisation has no escalation path today, creating one is a **deliverable**, not an assumption.

## 6. Name the corpus owner

| | |
| --- | --- |
| Knowledge the agent depends on | |
| Who owns it | |
| How often it changes | |
| How the agent learns it changed | |

The last row is what prevents [stale-knowledge incidents](../../runbooks/incident-stale-knowledge.md).
Unowned corpus = confident-wrong, eventually and silently.

## 7. Quantify the baseline

You cannot show improvement without it:

| Metric | Today |
| --- | --- |
| Volume per day | |
| Handling time (median / p90) | |
| First-contact resolution | |
| Escalation rate | |
| Error rate today (humans are not 100% either) | |

That last row matters in review. "The agent is 87% accurate" lands very differently next to a human
baseline of 91% than next to one of 78%.

## 8. Assemble

Feed everything into the [agent spec template](../../../docs/prd/02-agent-spec.md):
identity, goal, non-goals, tools, memory, guardrails, escalation, acceptance criteria.

## The checklist

- [ ] Ten real cases traced end to end
- [ ] Decision separated from lookup
- [ ] Tool list derived, with read/write marked
- [ ] Behaviour contract written as must / must never
- [ ] Escalation path defined, and it exists
- [ ] Corpus owner named with a change cadence
- [ ] Baseline quantified, including the human error rate
- [ ] Golden set started — [here](build-a-golden-set.md)

**Related:** [Value Trace](../../frameworks/value-trace.md) ·
[Agent spec](../../../docs/prd/02-agent-spec.md) · [Module 15](../../../modules/15-agentic-product-lifecycle/)
