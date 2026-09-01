# How to · Review someone else's agent architecture

**Time:** 90 minutes including preparation. **Output:** a scored artefact and a named condition.

---

## Before: ask for four things

If they do not arrive, postpone. A review with no artefact is a status update.

1. The [agent spec](../../../docs/prd/02-agent-spec.md) — goal, non-goals, tools, guardrails, escalation
2. The topology, with its H×
3. Cost per task, measured or explicitly modelled
4. A completed [Agent Readiness Scorecard](../../frameworks/agent-readiness-scorecard.md)

Score the scorecard independently yourself. **The disagreements are the agenda.**

## The review order — containment first

Not architecture first. Containment first. It is the only part that is urgent.

| Order | Dimension | The question |
| --- | --- | --- |
| 1 | **Containment** | What can it break, and what actually stops it? |
| 2 | **Fit** | Should this be an agent, at this rung? |
| 3 | **Evidence** | How do we know it works? |
| 4 | **Cost** | What does it cost, and where does it cliff? |
| 5 | **Reversibility** | How do we undo it? |

## The seven questions that find the most

1. **"Which tools write, and which are irreversible?"**
   Then: is any guard implemented only in the prompt? A prompt is not a guard.

2. **"Show me a case it currently fails."**
   If there isn't one, the golden set is a mirror.

3. **"What does it do when it doesn't know?"**
   Reveals whether abstention was designed or is accidental.

4. **"What's the H× of this topology, measured?"**
   And: what does the extra agent know that the first one didn't?

5. **"What share of traffic follows a known path?"**
   If it is high and everything goes through the agent, that is the cheapest available win.

6. **"When was rollback last rehearsed, and does it cover the prompt?"**
   Prompts are the usual gap.

7. **"Which of the eight cost cliffs can happen here, and what guards each?"**
   Uncapped loops and unbounded swarms are the two that recur.

## The patterns you will keep finding

| Pattern | Frequency | Fix |
| --- | --- | --- |
| One IAM role for all tools | Very common | Scope per tool |
| Golden set built from agent output | Very common | Rebuild from real inputs |
| Prompts unversioned | Very common | Into the manifest |
| No iteration cap in code | Common | Add one that raises |
| Multi-agent where one would do | Common | Measure H×, collapse |
| No abstention design | Common | Derive a target rate |
| Guard implemented in the prompt | Common | Move to IAM |

## Give the feedback well

**Lead with containment**, because it is the only thing that is genuinely urgent, and it is not a criticism
of their design taste.

**Separate the three kinds of finding:**

| Kind | Say |
| --- | --- |
| Blocker | "This blocks release: [specific]. Here is what would clear it." |
| Risk | "This will hurt you when [scenario]. Worth doing before scale." |
| Preference | "I'd do this differently, but yours works. Ignore me." |

Labelling preferences as preferences is what makes people act on your blockers.

## The output

```
Decision: conditional go
Condition: tool IAM scoped per tool; refund tool removed and replaced with
           assess_eligibility + human commit
Owner: —     Due: —     Verified by: —
```

Written in the room, in the owner's words. Conditions recalled later are renegotiated later.

**Related:** [Agent design review playbook](../../playbooks/agent-design-review.md) ·
[Agent Readiness Scorecard](../../frameworks/agent-readiness-scorecard.md) ·
[Blast Radius Grid](../../frameworks/blast-radius-grid.md)
