# Playbook · Running an agent design review

**Length:** 60 minutes. **Output:** a decision, with conditions written down and owned.

A design review that ends in "looks good" wasted an hour. This one ends in a scored artefact and a
named condition.

---

## Before the meeting (the organiser's job)

Send these 48 hours ahead. **If they do not arrive, postpone.** A review with no artefact is a status
update wearing a costume.

- [ ] The [agent spec](../../docs/prd/02-agent-spec.md) — goal, non-goals, tools, guardrails, escalation
- [ ] The [technical design](../../docs/prd/03-technical-design.md) — topology, decisions, rejected options
- [ ] A completed [Agent Readiness Scorecard](../frameworks/agent-readiness-scorecard.md), scored by the team
- [ ] Cost per task, **measured or explicitly modelled**

Ask one reviewer who did not build it to score the scorecard independently. **The disagreements are the
agenda.**

## The agenda

| Time | Section | Question on the table |
| --- | --- | --- |
| 0–5 | Frame | What outcome does this serve? |
| 5–15 | **Fit** | Should this be an agent, and at which rung? |
| 15–25 | **Containment** | What can it break, and what stops it? |
| 25–35 | **Evidence** | How do we know it works? |
| 35–45 | **Cost** | What does it cost, and where does it cliff? |
| 45–55 | **Reversibility** | How do we undo it? |
| 55–60 | Decision | Go / no-go / conditional, with the condition |

## The questions that do the work

**Fit** *(→ [Autonomy Ladder](../frameworks/autonomy-ladder.md))*
- Which rung does the acceptance test require? Which did you build?
- What share of traffic follows a known path? Could that be routed to a workflow?
- *Red flag:* "we built an agent because the project is about agents"

**Containment** *(→ [Blast Radius Grid](../frameworks/blast-radius-grid.md))*
- Which tools write? Which are irreversible? Which are wide?
- Is any guard implemented **only in the prompt**?
- *Red flag:* one IAM role for all tools

**Evidence** *(→ [Evidence Ladder](../frameworks/evidence-ladder.md))*
- What rung is your evidence on?
- Was the golden set frozen **before** tuning? Does it contain cases you currently fail?
- What is the target abstention rate, and how was it derived?
- *Red flag:* golden set built by labelling the agent's own output

**Cost** *(→ [Token Tax Ledger](../frameworks/token-tax-ledger.md), [Handoff Multiplier](../frameworks/handoff-multiplier.md))*
- Cost per task, measured. What is the H× of this topology?
- Which of the eight [cliffs](../frameworks/cost-cliff-map.md) can happen here, and what guards each?
- *Red flag:* cost described as "negligible" with no number

**Reversibility** *(→ [Reversibility Test](../frameworks/reversibility-test.md))*
- Do code, **prompt**, model and config all roll back together?
- When was rollback last rehearsed? How long did it take?
- *Red flag:* prompts not versioned

## The three questions that surface the most

1. **"What does it do when it doesn't know?"** — reveals whether abstention was designed or accidental
2. **"Show me a case it currently fails."** — if there isn't one, the golden set is a mirror
3. **"If the only guard is a sentence in the prompt, what happens when someone edits that sentence?"**

## The decision

| Outcome | Means |
| --- | --- |
| **Go** | No dimension below 2. Proceed |
| **Conditional go** | Proceed with a **named condition, an owner and a date** |
| **No-go** | A dimension at 0 or 1 that must be fixed first |
| **Not an agent** | Legitimate and valuable. Say it plainly |

Record it where the artefacts live, not in meeting notes nobody reopens.

```
Decision: conditional go
Condition: golden set must include ≥15 abstention cases drawn from real logs
Owner: —          Due: —          Verified by: —
```

## Facilitation notes

- **Score before the meeting.** The conversation should be about gaps, not about scoring.
- **The builder presents; the independent scorer challenges.** Not the other way around.
- **Write the condition in the room**, in the words the owner accepts. Conditions recalled later are
  conditions renegotiated later.
- **"I don't know" is an acceptable answer** and should be recorded as an open question, not punished.
  Punishing it teaches people to guess in reviews, which is the exact failure mode you are reviewing for.

**Related:** [Agent Readiness Scorecard](../frameworks/agent-readiness-scorecard.md) ·
[Module 15](../../modules/15-agentic-product-lifecycle/)
