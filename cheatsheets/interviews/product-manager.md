# Interview Guide · AI/Agentic Product Manager

Hiring a PM for agent products is hiring for judgement about uncertainty. These questions probe whether
someone can specify a system whose behaviour is probabilistic.

---

## The five questions

### 1. "How do you write acceptance criteria for something non-deterministic?"

**Weak:** "The agent should give accurate answers."
**Strong:** criteria expressed as **rates on a defined set**, not absolutes. "≥85% pass on a 130-case
golden set; 100% on the safety slice; every policy claim carries a citation." Knows the golden set is the
specification.

**Follow-up:** *"What's in the set besides happy paths?"* Looking for abstention and adversarial slices.

### 2. "What should the agent do when it doesn't know?"

**Weak:** "Give its best guess" or "say it doesn't know" without further thought.
**Strong:** abstention is a **designed rate** derived from the input distribution, not an accident. Knows
confident-wrong and timid are different failures with different costs, and that the ratio is a business
decision.

See [Abstention Budget](../frameworks/abstention-budget.md).

### 3. "Engineering says adding this feature is 'just a prompt change'. Respond."

**Weak:** "Great, let's do it."
**Strong:** a prompt change is a behaviour change — new capability, new failure mode, new evaluation
slice, permanent token cost on every turn. Asks: which outcome does it serve, what would prove it works,
what does it cost per task, does it need a new tool or permission.

This question separates PMs who will control agentic scope from those who will amplify it. See
[Scope Fence](../frameworks/scope-fence.md).

### 4. "The agent is 92% accurate. Is that good?"

**Weak:** "Yes" or "depends on the use case" and stops there.
**Strong:** *"Accurate on what set? Built how? What are the 8%?"* Eight percent spread evenly is very
different from 8% concentrated in a high-stakes category. Also asks what the human baseline is — people are
not 100% either.

### 5. "How would you justify this to a CFO?"

**Weak:** efficiency and customer experience, in adjectives.
**Strong:** walks the [Value Trace](../frameworks/value-trace.md) — model metric → system behaviour →
process change → operational effect → financial effect — with an honest denominator. Knows the ②→③ link is
where value usually leaks: a working agent nobody routes work to is worth nothing.

## Scenario exercise

> *"Your agent resolves 58% of enquiries autonomously against a 60% target. Launch is in two weeks. The
> sponsor wants to know if you're on track. What do you say?"*

**Listen for:**
- Asks what the 42% consists of before answering — abstentions? failures? out of scope?
- Distinguishes "abstained correctly" from "got it wrong" — the same number, opposite meanings
- Checks the safety slice, which is pass/fail regardless of the headline number
- Does not propose changing the target
- Has a view on whether 58% delivers the business case (break-even rate)

**Excellent answer:** "58% with a clean safety slice and correct abstentions is a launch. 58% including
confident-wrong answers is not, at any percentage."

## Depth probes

| Area | Question |
| --- | --- |
| Prioritisation | "Two teams want agents. How do you choose?" |
| Risk | "What is the worst realistic outcome, and what limits it?" |
| Measurement | "What do you instrument on day one?" |
| Stakeholders | "Legal asks whether the agent can be wrong. Answer them." |
| Cost | "Cost per interaction is 3× the estimate. What are the options?" |
| Sunsetting | "What would make you switch it off?" |

## Red flags

- Talks about model capability rather than system behaviour
- No concept of abstention
- Treats accuracy as a single number with no denominator
- "The AI will figure it out"
- Cannot say what is explicitly out of scope
- Would move the target to hit the date

## Green flags

- Asks what happens when it is wrong, before asking what it can do
- Distinguishes an evaluation set from a test set from production traffic
- Talks about the process change, not only the software
- Has an opinion on the confident-wrong versus timid trade-off for the domain
- Has killed something, and can explain how they announced it

---

## If you are the candidate

Prepare a story where you **narrowed** scope and the product got better. Bring one artefact — a real
acceptance criterion you wrote for a probabilistic system.

**Study:** [Scope Fence](../frameworks/scope-fence.md) · [Value Trace](../frameworks/value-trace.md) ·
[Abstention Budget](../frameworks/abstention-budget.md) ·
[Evidence Ladder](../frameworks/evidence-ladder.md) · the [sample PRDs](../../docs/prd/)

**Work through:** [Module 15](../../modules/15-agentic-product-lifecycle/) and the
[PM learning path](../../docs/learning-paths/product-manager.md)
