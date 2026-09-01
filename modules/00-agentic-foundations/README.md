# 🧭 Module 00 · Agentic Foundations

> Decide what deserves to be an agent before you build one.

**Estimated time:** 4–5 hours &nbsp;·&nbsp; **Prerequisites:** None. Start here even if you have never called an LLM API.

The most expensive mistake in agentic AI is building an agent for a job a `for` loop could do. This module gives you the vocabulary and the decision tools to tell the difference, and the artefacts to defend that decision to a stakeholder.

---

## What you will be able to do

- Classify any candidate use case as script, workflow, or agent — and justify it
- Name the six recurring failure patterns of agentic systems and spot them in a design
- Write an invariance test that proves a behaviour is stable across paraphrases
- Produce a one-page agent PRD that a reviewer can actually challenge
- Estimate token cost per interaction before a single line of code is written

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Agent vs workflow vs script | None yet — this module is deliberately cloud-free |
| Autonomy dials |  |
| Failure taxonomy |  |
| Invariance testing |  |
| Token economics |  |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/Day1_Half1.pptx`](slides/Day1_Half1.pptx) | Framing: what an agent is, and the four-quadrant classifier |
| 2 | 📊 | [`activities/H1-01_Four-Quadrant_Classifier.xlsx`](activities/H1-01_Four-Quadrant_Classifier.xlsx) | Classify your own use cases in the workbook |
| 3 | 📊 | [`activities/H1-02_Is-It-An-Agent_Vote.xlsx`](activities/H1-02_Is-It-An-Agent_Vote.xlsx) | Team vote — argue the borderline cases |
| 4 | 📊 | [`activities/H1-04_Six-Failure-Pattern_Diagnostic.xlsx`](activities/H1-04_Six-Failure-Pattern_Diagnostic.xlsx) | Diagnose the six failure patterns |
| 5 | ✏️ | [`exercises/Exercise_Mid-Session.pdf`](exercises/Exercise_Mid-Session.pdf) | Mid-session checkpoint |
| 6 | 📖 | [`slides/Day1_Half2.pptx`](slides/Day1_Half2.pptx) | From idea to PRD: scoping, guardrails, readiness |
| 7 | 📊 | [`activities/H2-01_PRD-Builder.xlsx`](activities/H2-01_PRD-Builder.xlsx) | Draft your agent PRD |
| 8 | 📊 | [`activities/H2-03_Token-Cost_Calculator.xlsx`](activities/H2-03_Token-Cost_Calculator.xlsx) | Cost your design before you build it |
| 9 | ✏️ | [`exercises/Day1_Half2_Applied_Exercise.md`](exercises/Day1_Half2_Applied_Exercise.md) | Applied exercise — full design pass |
| 10 | ✏️ | [`exercises/Architecture_Exercise.md`](exercises/Architecture_Exercise.md) | Architecture exercise |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 00 — Agentic Foundations | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Solutions

Worked solutions live in [`solutions/`](solutions/). Attempt every exercise closed-book first — the solutions are written to be read *after* you have a wrong answer to compare against.

## Common mistakes

- Calling something an agent because it uses an LLM. Autonomy is the test, not the model.
- Writing outcomes as 'understand X'. If you cannot test it, it is not an outcome.
- Deferring cost estimation until after the build. By then the architecture is fixed.

## Folder map

```
activities       9 file(s)
exercises        6 file(s)
slides           2 file(s)
solutions        2 file(s)
```

## Field guide for this module

Reference material for the ideas in this module — open these while you work, not before.

**Frameworks**

- [Autonomy Ladder](../../cheatsheets/frameworks/autonomy-ladder.md) — Build the lowest rung that passes your acceptance test
- [Scope Fence](../../cheatsheets/frameworks/scope-fence.md) — Four posts that stop "just add it to the prompt" creep
- [Evidence Ladder](../../cheatsheets/frameworks/evidence-ladder.md) — Six rungs of proof, and the claim each licenses
- [Value Trace](../../cheatsheets/frameworks/value-trace.md) — Five links from model metric to money

**Recipes and procedures**

- [Agent design review](../../cheatsheets/playbooks/agent-design-review.md) — Running the review this module prepares you for

---

🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 01 · LLM Intuition and the AWS Bridge](../01-llm-and-aws-bridge/) ➡️
