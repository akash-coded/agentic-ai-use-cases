# Playbook · Killing an agent project

Most guidance is about starting. Stopping well is rarer, harder, and more valuable — and doing it badly
poisons the next three attempts.

---

## The kill criteria — write them at the start

Agree these in the [idea brief](../../docs/prd/00-idea-brief.md), before anyone is invested:

| Criterion | Threshold |
| --- | --- |
| Autonomous resolution after two tuning rounds | Below X% |
| Cost per resolved task with no path down | Above $Y |
| Safety failures that citation checking does not catch | Any |
| Time to first production value | Beyond N months |
| The process it serves | Being redesigned |

Kill criteria written at the start are an act of confidence, not pessimism. Written at the end, they are a
negotiation.

## The four honest reasons to stop

| Reason | Sounds like | Actually means |
| --- | --- | --- |
| **Wrong shape** | "It should have been a workflow" | You built at the wrong [rung](../frameworks/autonomy-ladder.md). Salvage the tools |
| **No trace to value** | "It works but nobody uses it" | The [②→③ link](../frameworks/value-trace.md) broke — a process problem |
| **Economics do not close** | "Cost per task will not come down" | Legitimate. Say the number |
| **The problem moved** | "The process is changing anyway" | Stopping is obviously correct |

Notice none of these is "the technology is not ready". That framing is almost always a cover for one of the
four above, and it teaches the organisation the wrong lesson.

## What to salvage — always more than people expect

An agent project that stops still produced:

| Asset | Reusable as |
| --- | --- |
| **Tool implementations** | Plain API integrations. Frequently the most valuable output |
| **Golden set** | A specification of correct behaviour, agent or not |
| **The corpus work** | Cleaned, chunked, structured knowledge — useful to search, to humans, to anything |
| **The evaluation harness** | Reusable for the next attempt |
| **The process map** | You now understand the workflow better than anyone |
| **The decision record** | Why this did not work is worth writing down |

> Teams routinely delete the golden set when a project stops. It is the single most reusable artefact,
> because it encodes what "correct" means in your domain independently of how you implement it.

## How to announce it

**Do:**
- Lead with the criterion that was met — "cost per task plateaued at $0.21 against a $0.08 bar"
- Name what is being kept and who owns it
- Say what would have to change for this to be worth revisiting
- Thank people specifically, for specific work

**Do not:**
- Call it a "pause" if it is a stop. Everyone knows, and the ambiguity blocks the team from moving on
- Blame the technology, the vendor, or the team
- Bury it. A quiet death makes the next proposal harder to fund

## The template

```
We are stopping [project].

Why: [criterion] was [value] against a bar of [threshold], after [what was tried].

What we are keeping:
  - [tool integrations] → owned by [team]
  - [golden set] → in [location], useful for [purpose]
  - [corpus work] → now powering [thing]

What would change this: [specific, e.g. "if per-token costs fall ~60%, the economics close"]

What we learned: [one or two sentences that will change the next attempt]
```

## The post-mortem question

> **At which gate could we have known this?**

Almost always earlier than you stopped. The answer usually points at an artefact that was skipped — a cost
model at Gate 2, an honest golden set at Gate 3 — and that is the process fix.

## The thing to protect

A project that stops cleanly, salvages its assets and states its learning **makes the next one easier to
fund**. A project that limps on for two quarters and dies quietly makes the next one impossible.

Stopping well is a capability worth building deliberately.

**Related:** [Value Trace](../frameworks/value-trace.md) ·
[Post-launch review](../../docs/prd/06-post-launch-review.md) ·
[Module 15](../../modules/15-agentic-product-lifecycle/)
