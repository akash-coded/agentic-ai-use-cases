# Playbook · Scoping an agentic engagement

For consultants, solution architects and internal teams taking on agent work for someone else. The
failure mode is agreeing to an outcome you cannot evidence.

---

## The discovery call — five questions, in this order

**1. "What should your people be able to do in 90 days that they cannot do today?"**

Not "what do you want to build". The answer becomes your scope fence. If the answer is a technology
("we want agents"), you are talking to the wrong person or too early.

**2. "Walk me through the last ten times someone did this manually."**

Real cases, not the described process. The gap between the described process and the actual one is where
every agent project meets reality.

**3. "What happens today when someone doesn't know the answer?"**

This reveals whether the organisation *has* an escalation path. If humans have nowhere to escalate, the
agent will have nowhere either, and [abstention](../frameworks/abstention-budget.md) will be impossible to
design.

**4. "Who owns the knowledge this depends on, and how often does it change?"**

Unowned corpus = stale index = [confident-wrong](../runbooks/incident-stale-knowledge.md). If nobody owns
it, that ownership is a deliverable, not an assumption.

**5. "What would make you switch this off?"**

If they cannot answer, they have not thought about failure, and they will treat the first bad answer as a
betrayal rather than an expected event.

## The scoping matrix

Score the engagement before you price it.

| Factor | 🟢 Good | 🟡 Manageable | 🔴 Walk away or reprice |
| --- | --- | --- | --- |
| Outcome | Specific, measurable | Vague but narrowing | "Transform the business" |
| Data access | Available, documented | Available, undocumented | Blocked or unclear |
| Corpus ownership | Named owner, cadence | Owner findable | Nobody owns it |
| Escalation path | Exists today | Can be created | None, and none wanted |
| Success metric | Agreed and measurable | Definable | "We'll know it when we see it" |
| Sponsor | Owns the outcome | Owns a budget | Owns neither |
| Process stability | Stable | Minor changes coming | Being redesigned |

Two or more red cells is not an engagement, it is a discovery project. Sell that instead — it is honest and
it is often more valuable.

## Phasing that survives contact

| Phase | Duration | Deliverable | Gate |
| --- | --- | --- | --- |
| **0 · Discovery** | 1–2 wks | [Idea brief](../../docs/prd/00-idea-brief.md) + classification | Should this be an agent? |
| **1 · Specification** | 1–2 wks | [Agent spec](../../docs/prd/02-agent-spec.md), cost model, golden set v1 | Is it specified well enough to build? |
| **2 · Build** | 3–6 wks | Working agent, evaluated | Does it meet the bar? |
| **3 · Validate** | 1–2 wks | Shadow traffic, gate, runbooks | Safe to release? |
| **4 · Release** | 1 wk | Deployed, monitored, handed over | Can they run it without us? |

**Phase 1 is the one clients want to skip.** It is the one that determines whether phase 2 succeeds. The
golden set built in phase 1 is what makes phase 3 possible at all.

## The contract language that saves you

| Clause | Why |
| --- | --- |
| Success defined as **a metric on an agreed golden set**, not as user satisfaction | Otherwise "it feels wrong" is a breach |
| Golden set is a **joint deliverable**, signed off before build | It is the specification |
| Corpus quality and ownership is the **client's** responsibility | You cannot fix an unowned corpus |
| Model and platform changes are **change requests** | Providers move; that is not your risk to absorb |
| Abstention is a **success state**, defined with a target rate | Otherwise every "I don't know" is logged as a failure |

That last clause prevents the most common late-stage dispute in agent work.

## Pricing the invisible

| Under-priced | Why it bites |
| --- | --- |
| Golden-set construction | Days of work with the client's domain experts, and it is unavoidable |
| Corpus preparation | Frequently larger than the agent build |
| Evaluation harness | Reusable, but not free the first time |
| The organisational change | Routing work to the agent is a change-management project |
| Handover | If they cannot run it, you have not finished |

## The one-page proposal

| | |
| --- | --- |
| **Outcome in 90 days** | *(their words, from question 1)* |
| **In scope** | |
| **Explicitly out of scope** | |
| **How we will know it works** | Metric, on a golden set of N cases, built jointly in phase 1 |
| **What we need from you** | Data access, corpus owner, domain expert time, escalation path |
| **What would make us recommend stopping** | *(kill criteria, stated up front)* |

The last row wins more work than it loses. It is the clearest signal that you have done this before.

**Related:** [Build, buy or wait](build-buy-or-wait.md) · [Value Trace](../frameworks/value-trace.md) ·
[Module 15](../../modules/15-agentic-product-lifecycle/)
