# 🌉 Module 01 · LLM Intuition and the AWS Bridge

> Build a working mental model of LLMs, then map it onto AWS.

**Estimated time:** 3–4 hours &nbsp;·&nbsp; **Prerequisites:** Module 00.

Zero math. This module builds the intuition you need to make model choices you can defend — context windows, tokenisation, mixture-of-experts, temperature — and then connects each concept to the AWS surface where you will actually use it.

---

## What you will be able to do

- Explain next-token prediction, context windows and tokenisation without hand-waving
- Read a model card and predict how the model will behave on your workload
- Choose between model families on latency, cost and capability — not vibes
- Map every LLM concept onto its Amazon Bedrock equivalent

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Next-token prediction | Amazon Bedrock model catalogue |
| Tokenisation | Model IDs and regional prefixes |
| Context window | Cross-region inference profiles |
| Mixture-of-Experts |  |
| Temperature and sampling |  |
| Model families |  |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/Day1.5_LLM_AWS_Bridge.pptx`](slides/Day1.5_LLM_AWS_Bridge.pptx) | The bridge deck — LLM concepts mapped to AWS |
| 2 | ✏️ | [`exercises/LLM_Intuition_Bank.md`](exercises/LLM_Intuition_Bank.md) | Self-test bank: MCQs, diagrams, error-fixing. Closed-book first. |
| 3 | 📊 | [`activities/Day15_Companion_Workbook.xlsx`](activities/Day15_Companion_Workbook.xlsx) | Companion workbook |
| 4 | ✏️ | [`exercises/Day1.5_Ad-Hoc_Exercise_PickTheModel.pdf`](exercises/Day1.5_Ad-Hoc_Exercise_PickTheModel.pdf) | Pick the model — defend the choice |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 01 — LLM Intuition and the AWS Bridge | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Solutions

This module has no separate solution set; the notebooks carry the worked answers inline.

## Common mistakes

- Assuming a bigger context window is always better. It costs tokens and dilutes attention.
- Forgetting the `us.` / `eu.` inference-profile prefix on Bedrock model IDs — the single most common first error.

## Folder map

```
activities       1 file(s)
exercises        2 file(s)
slides           1 file(s)
```

---

⬅️ [Module 00 · Agentic Foundations](../00-agentic-foundations/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 02 · Amazon Bedrock Essentials](../02-bedrock-essentials/) ➡️
