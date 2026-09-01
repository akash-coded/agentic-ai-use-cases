# 📋 Product Manager

**For:** you decide what gets built, negotiate its scope, and answer for it at a gate. **Time:** ~25 hours.
**Finish line:** a PRD, a guardrail bar engineering agreed to, and a gate review you can chair.

You will run a small number of notebooks. Not to write code — to have felt the constraints you are about to
make decisions about. A PM who has never watched a token count climb will underestimate cost forever.

## 1 · What is actually an agent — 6 h

Full [Module 00](../../modules/00-agentic-foundations/), including the workbooks:

- [Four-quadrant classifier](../../modules/00-agentic-foundations/activities/H1-01_Four-Quadrant_Classifier.xlsx) — run it on your own backlog
- [Six-failure-pattern diagnostic](../../modules/00-agentic-foundations/activities/H1-04_Six-Failure-Pattern_Diagnostic.xlsx)
- [PRD builder](../../modules/00-agentic-foundations/activities/H2-01_PRD-Builder.xlsx)
- [Token-cost calculator](../../modules/00-agentic-foundations/activities/H2-03_Token-Cost_Calculator.xlsx)

## 2 · Enough LLM to argue well — 4 h

- [Module 01 deck](../../modules/01-llm-and-aws-bridge/slides/Day1.5_LLM_AWS_Bridge.pptx)
- [LLM Intuition Bank](../../modules/01-llm-and-aws-bridge/exercises/LLM_Intuition_Bank.md) — closed-book. This is the highest-value four hours on this path.
- [Portable concepts](../concepts/genai-core-concepts.md)

## 3 · Feel the constraints — 4 h

Run these two notebooks even if you never run another:

- [`converse_api_masterclass.ipynb`](../../modules/02-bedrock-essentials/notebooks/converse_api_masterclass.ipynb) — watch the token count on every call
- [`Day6_Demo_1_NoStrands.ipynb`](../../modules/05-agent-loop-no-framework-to-strands/notebooks/Day6_Demo_1_NoStrands.ipynb) — see how many model calls one "simple" request costs

Then read the [verbosity tax exercise](../../modules/03-bedrock-agents/exercises/verbosity_tax_exercise.md).
It will change how you write acceptance criteria.

## 4 · The lifecycle and its gates — 8 h

Full [Module 15](../../modules/15-agentic-product-lifecycle/):

- [The artefact set](../../modules/15-agentic-product-lifecycle/slides/The_Agentic_Artefact_Set.pptx)
- [Exercise 1 · artefacts owed](../../modules/15-agentic-product-lifecycle/exercises/Exercise_1_Artefacts_Owed.md)
- [Exercise 4 · the guardrail bar](../../modules/15-agentic-product-lifecycle/exercises/Exercise_4_Guardrail_Bar.md)
- [Exercise A · the gate review](../../modules/15-agentic-product-lifecycle/exercises/Exercise_A_The_Gate_Review.md)
- [Exercise B · the cost-cut ultimatum](../../modules/15-agentic-product-lifecycle/exercises/Exercise_B_The_Cost_Cut_Ultimatum.md)

## 5 · What "done" means — 3 h

- [Module 13 deck](../../modules/13-agentic-qa-and-evaluation/slides/Agentic_QA_Training.pptx) — what
  evaluation can and cannot promise you
- [`quality_gate.py`](../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py) — read it. It is short,
  and it is the file that decides whether your feature ships.

## Finish line

For one real use case: a completed PRD, a cost-per-interaction estimate, a guardrail bar with engineering's
cost estimate attached, and a written go/no-go with its condition. Templates in
[`docs/prd/`](../prd/).
