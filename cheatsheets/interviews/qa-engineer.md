# Interview Guide · QA / Test Engineer (Agentic AI)

Testing non-deterministic systems is a genuinely different discipline. These questions find people who
understand *how* it differs, rather than people who apply deterministic habits harder.

---

## The five questions

### 1. "How do you test a system that gives different answers to the same input?"

**Weak:** "Set temperature to 0 and assert equality."
**Strong:** you test **properties and rates**, not exact outputs. Contract tests for shape, invariance
tests across paraphrases, rate-based assertions on a golden set. Temperature 0 reduces variance but does
not make the system deterministic, and testing at 0 while shipping at 0.7 tests a different system.

### 2. "What's in your golden set besides cases that should work?"

**Weak:** "Edge cases."
**Strong:** names slices — abstention (correct answer is "I don't know"), adversarial (including injection
via *retrieved content*), out-of-scope (correct answer is refusal), failure honesty (tool returns nothing).
Knows a set built only from passing cases measures nothing.

**Follow-up:** *"How many of your cases fail today?"* Correct answer is "a meaningful share, deliberately".

### 3. "The build passes but you don't trust it. What do you check?"

**Strong:** checks whether the *gate* is real — does it exit non-zero or only warn? Were thresholds edited
recently, and in the same commit as the fix? Is the safety slice pass/fail or averaged into a headline
number? Has the golden set had a case added recently?

A gate that warns is not a gate. A candidate who checks the gate before the code understands this domain.

### 4. "How do you test that an agent handles tool failure?"

**Weak:** "Mock the tool to throw an exception."
**Strong:** yes, and then checks what the agent **says**. The dangerous failure is not a crash — it is the
agent narrating a plausible answer around a missing tool result. Tests specifically that empty results
produce abstention rather than invention.

Bonus: knows that returning `[]` reads to a model as "nothing applies", which is the opposite of "I could
not check".

### 5. "How do you catch a regression that nobody reported?"

**Strong:** silent degradation. Names canaries — which model answered, abstention rate, cost per task,
index freshness, citation-entailment sampling. Knows error rate catches only the failure you would have
noticed anyway.

See [Silent Degradation Watchlist](../frameworks/silent-degradation-watchlist.md).

## Practical exercise

> *"Here is an agent and its golden set of 40 cases. It passes 100%. Convince me it's not ready."*

**Look for:**
- Asks how the set was built — if from the agent's own output, it is a mirror
- Notices there are no abstention or adversarial cases
- Asks whether the gate fails or warns
- Tests a paraphrase of a passing case and watches it break
- Tests a tool failure
- Asks what the safety threshold is and whether it is averaged

**Excellent:** writes three failing cases in the first ten minutes.

## Depth probes

| Area | Question |
| --- | --- |
| Flakiness | "A case passes 8 times in 10. Bug or variance?" |
| Multi-agent | "Sub-answers correct, final answer wrong. Where is the bug?" |
| Grounding | "How do you test that a citation actually supports the claim?" |
| Injection | "How do you test prompt injection through retrieved documents?" |
| CI | "How long should the gate take, and what runs on every commit?" |
| Judges | "You use an LLM as a judge. How do you validate the judge?" |

That last one is a strong senior signal — an unvalidated judge is a measurement instrument nobody
calibrated.

## Red flags

- Wants exact-match assertions
- Treats variance as flakiness to be eliminated rather than characterised
- No concept of correct abstention
- Would raise a threshold to make a build pass
- Tests only the happy path plus obvious edge cases

## Green flags

- Asks how the golden set was constructed before looking at results
- Distinguishes "wrong" from "correctly declined" instinctively
- Thinks about the gate as a product with its own failure modes
- Wants to test tool failure, not just tool success
- Has an opinion on judge validation

---

## If you are the candidate

Your differentiator is that you can build the **gate** — the thing that turns evaluation into a decision.
Be able to describe one you built: the metrics, the thresholds, and a time it correctly blocked a release.

**Study:** [Evidence Ladder](../frameworks/evidence-ladder.md) ·
[Abstention Budget](../frameworks/abstention-budget.md) ·
[Grounding Triangle](../frameworks/grounding-triangle.md) ·
[Failure Signature Catalog](../frameworks/failure-signature-catalog.md)

**Work through:** [Module 13](../../modules/13-agentic-qa-and-evaluation/) — especially
[`quality_gate.py`](../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py)
