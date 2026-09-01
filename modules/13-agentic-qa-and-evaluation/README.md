# 🔬 Module 13 · Agentic QA and Evaluation

> How you prove an agent works — and block the ones that do not.

**Estimated time:** 5–6 hours &nbsp;·&nbsp; **Prerequisites:** Module 06 or 08. Module 11 recommended.

Non-deterministic systems need a different testing discipline. This module gives you golden sets, contract tests, multi-agent tests, a quality gate with real thresholds, and a CI step that actually blocks a bad deploy.

---

## What you will be able to do

- Build a golden set that represents real usage, not happy paths
- Write contract tests for tool schemas and agent outputs
- Test multi-agent handoffs where the bug lives between agents
- Run a quality gate that exits non-zero and blocks promotion
- Debug a failing agent from CloudWatch traces

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Golden sets | CloudWatch Logs Insights |
| Contract testing | AgentCore Observability |
| LLM-as-judge | Bedrock model invocation logging |
| Quality gates |  |
| Non-deterministic testing |  |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/Agentic_QA_Training.pptx`](slides/Agentic_QA_Training.pptx) | Agentic QA |
| 2 | 📖 | [`src/golden_set.jsonl`](src/golden_set.jsonl) | The golden set — study its shape |
| 3 | 💻 | [`notebooks/eval_harness.ipynb`](notebooks/eval_harness.ipynb) | Evaluation harness |
| 4 | 📖 | [`src/test_contracts.py`](src/test_contracts.py) | Contract tests |
| 5 | 📖 | [`src/test_multiagent.py`](src/test_multiagent.py) | Multi-agent tests |
| 6 | 📖 | [`src/quality_gate.py`](src/quality_gate.py) | The quality gate — the file with teeth |
| 7 | 💻 | [`notebooks/debug_walkthrough.ipynb`](notebooks/debug_walkthrough.ipynb) | Debugging walkthrough |
| 8 | 🔖 | [`src/cloudwatch_filters.md`](src/cloudwatch_filters.md) | CloudWatch filter patterns |
| 9 | ✏️ | [`exercises/QA_Exercise_TravelMind.md`](exercises/QA_Exercise_TravelMind.md) | QA exercise — TravelMind |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 13 — Agentic QA and Evaluation | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Solutions

This module has no separate solution set; the notebooks carry the worked answers inline.

## Common mistakes

- A gate that warns instead of failing. Teams learn to ignore it within a week.
- Golden sets built only from cases you already pass.

## Folder map

```
exercises        1 file(s)
notebooks        2 file(s)
slides           1 file(s)
src             11 file(s)
```

## Field guide for this module

Reference material for the ideas in this module — open these while you work, not before.

**Frameworks**

- [Evidence Ladder](../../cheatsheets/frameworks/evidence-ladder.md) — Never claim above your rung
- [Abstention Budget](../../cheatsheets/frameworks/abstention-budget.md) — The vital sign, and how to target it
- [Failure Signature Catalog](../../cheatsheets/frameworks/failure-signature-catalog.md) — Debug from evidence, not the prompt
- [Silent Degradation Watchlist](../../cheatsheets/frameworks/silent-degradation-watchlist.md) — 12 failures that never raise an error

**Quick reference**

- [Observability](../../cheatsheets/quick-reference/observability.md) — Ten log fields and Logs Insights queries

**Recipes and procedures**

- [Build a quality gate](../../cheatsheets/how-to/engineers/build-a-quality-gate.md) — A gate that exits non-zero
- [Validate an LLM judge](../../cheatsheets/how-to/qa-and-test/validate-an-llm-judge.md) — Calibrate before you trust

---

⬅️ [Module 12 · A2A and A2UI: Agent Interoperability](../12-a2a-and-a2ui-interop/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 14 · End-to-End Production Pipeline](../14-end-to-end-production/) ➡️
