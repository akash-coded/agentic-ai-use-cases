# Interview Guide · Business Analyst (AI/Agentic)

BAs on agent projects do something specific and hard: turn a fuzzy process into a specification precise
enough to evaluate. These questions probe that.

---

## The five questions

### 1. "How do you document a process that an agent will take over?"

**Weak:** a flowchart of the described process.
**Strong:** documents the **actual** process from real cases, including the exceptions. Knows the described
process and the real one differ, and that the difference is where the agent will fail.

**Follow-up:** *"How do you find the exceptions?"* Looking for: sample real cases, ask what happened when
it was not straightforward, look at escalation logs.

### 2. "What makes a good requirement for an agent, versus for normal software?"

**Weak:** "The same — clear and testable."
**Strong:** normal requirements are pass/fail; agent requirements are **rates on a defined set**. And the
set becomes an artefact you must build: real inputs, expected outputs, including cases where the correct
answer is "I don't know".

The BA who understands that the golden set *is* the requirements document is the one you want.

### 3. "Stakeholders disagree about what the right answer is. What do you do?"

**Weak:** escalate.
**Strong:** this is the job. Disagreement between experts means the case is genuinely ambiguous — which
means the correct agent behaviour is **abstention**, not a guess. Documents it as an ambiguity case, not a
requirement dispute.

This is the strongest signal available in a BA interview for agent work.

### 4. "How do you measure whether it worked?"

**Weak:** user satisfaction surveys.
**Strong:** traces from model metric to operational effect — [Value Trace](../frameworks/value-trace.md).
Knows the honest denominator: if 40% of enquiries are in scope and 58% resolve, the agent touches 23% of
volume, not 58%.

### 5. "What data would you need before this project starts?"

**Strong answers include:**
- A sample of real inputs, not curated examples
- Volume, by category
- What currently happens on the exceptions
- Who owns the knowledge the agent will depend on, and how often it changes
- The current escalation path

The corpus-ownership question is the one most candidates miss, and it is the one that determines whether
the system goes stale.

## Practical exercise

> *"Here are 20 real support tickets. Produce the input to an agent specification."*

**Look for:**
- Classifies into: clearly answerable / ambiguous / out of scope / data unavailable
- Notices tickets where two experts would disagree, and flags them as abstention cases
- Identifies what information each ticket needs and where it lives — the tool list, emerging
- Spots patterns that should be a workflow rather than an agent
- Asks about volume before assuming the distribution is representative

**Excellent:** produces a draft abstention rate from the classification, unprompted.

## Depth probes

| Area | Question |
| --- | --- |
| Elicitation | "SMEs say 'it depends'. How do you get to a rule?" |
| Edge cases | "How do you find the cases nobody mentions?" |
| Handover | "How do you hand a golden set to engineering?" |
| Change | "Policy changes monthly. What does that mean for the design?" |
| Adoption | "Agent works; nobody uses it. Diagnose." |

## Red flags

- Documents only the happy path
- Treats "the agent should be accurate" as a requirement
- No curiosity about what happens when it fails
- Assumes the described process is the real one
- Cannot distinguish ambiguous from unanswerable

## Green flags

- Asks for real cases immediately
- Treats expert disagreement as design input rather than a blocker
- Thinks about corpus ownership unprompted
- Distinguishes "the agent got it wrong" from "the agent correctly declined"
- Interested in what happens to the people whose work changes

---

## If you are the candidate

Your differentiator is that you can produce the **golden set** — the artefact that turns a vague ambition
into something evaluable. Say so, and describe how you would build one.

**Study:** [Value Trace](../frameworks/value-trace.md) · [Abstention Budget](../frameworks/abstention-budget.md) ·
[Autonomy Ladder](../frameworks/autonomy-ladder.md) ·
[Demo-to-Production Gap](../frameworks/demo-to-production-gap.md)

**Work through:** [Module 00](../../modules/00-agentic-foundations/) and
[Module 15](../../modules/15-agentic-product-lifecycle/)
