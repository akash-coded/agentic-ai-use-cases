# 🪨 Module 02 · Amazon Bedrock Essentials

> Your first real calls: Converse API, tokens, tool use, knowledge bases, guardrails.

**Estimated time:** 6–8 hours &nbsp;·&nbsp; **Prerequisites:** Modules 00–01, and an AWS account with Bedrock model access enabled.

This is where AWS enters properly. One API — `Converse` — carries you from a hello-world call all the way to tool use and retrieval. Learn it well here and every later module gets easier.

---

## What you will be able to do

- Invoke any Bedrock model through the Converse API and read the token accounting
- Hold a correct multi-turn conversation, including the assistant tool-use turn
- Define a tool schema the model actually calls correctly
- Query a Bedrock Knowledge Base and ground an answer in retrieved context
- Apply a Guardrail and observe what it blocks

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Prompting | Amazon Bedrock Converse API |
| Multi-turn state | InvokeModel |
| Tool/function calling | Bedrock Knowledge Bases |
| Retrieval grounding | Bedrock Guardrails |
| Safety filtering | IAM for Bedrock |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/Bedrock_Chapters_1_to_4.pptx`](slides/Bedrock_Chapters_1_to_4.pptx) | Chapters 1–4: access, models, first calls, tokens |
| 2 | 💻 | [`notebooks/00_Bedrock_Onboarding.ipynb`](notebooks/00_Bedrock_Onboarding.ipynb) | Onboarding notebook — verify your access works |
| 3 | ✏️ | [`exercises/Exercise_1_First_Calls_and_the_Converse_API.pdf`](exercises/Exercise_1_First_Calls_and_the_Converse_API.pdf) | Exercise 1 · first calls |
| 4 | 💻 | [`notebooks/converse_api_masterclass.ipynb`](notebooks/converse_api_masterclass.ipynb) | Converse API masterclass |
| 5 | ✏️ | [`exercises/Exercise_2_Tokens_and_Multi-Turn_Conversations.pdf`](exercises/Exercise_2_Tokens_and_Multi-Turn_Conversations.pdf) | Exercise 2 · tokens and multi-turn |
| 6 | 📖 | [`slides/Bedrock_Chapters_5_to_8.pptx`](slides/Bedrock_Chapters_5_to_8.pptx) | Chapters 5–8: tool use, RAG, guardrails, agents |
| 7 | 💻 | [`notebooks/travelmind_refund_agent.ipynb`](notebooks/travelmind_refund_agent.ipynb) | TravelMind refund agent — tool use in anger |
| 8 | ✏️ | [`exercises/Exercise_3_Tool_Use_and_Knowledge_Bases.pdf`](exercises/Exercise_3_Tool_Use_and_Knowledge_Bases.pdf) | Exercise 3 · tool use and KBs |
| 9 | ✏️ | [`exercises/Exercise_4_Guardrails_Strands_and_End-to-End_Agent_Design.pdf`](exercises/Exercise_4_Guardrails_Strands_and_End-to-End_Agent_Design.pdf) | Exercise 4 · guardrails and end-to-end design |
| 10 | 💻 | [`notebooks/Day5_Bedrock_Build.ipynb`](notebooks/Day5_Bedrock_Build.ipynb) | Build session — put it together |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 02 — Amazon Bedrock Essentials | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Project artefact

[`projects/bedrock-mini-project`](../../projects/bedrock-mini-project) — a self-contained build with scripts, KB documents and a cost analysis.

## Solutions

Worked solutions live in [`solutions/`](solutions/). Attempt every exercise closed-book first — the solutions are written to be read *after* you have a wrong answer to compare against.

## Common mistakes

- Using `bedrock` when you need `bedrock-runtime`. Different clients, different operations.
- Dropping the assistant's tool-use message from history. The next turn then makes no sense to the model.
- Assuming model access is on by default. It is per-model, per-region, and must be requested.

## Folder map

```
activities       6 file(s)
assets           2 file(s)
exercises        6 file(s)
notebooks        5 file(s)
slides          10 file(s)
solutions        5 file(s)
src              1 file(s)
```

## Field guide for this module

Reference material for the ideas in this module — open these while you work, not before.

**Frameworks**

- [Token Tax Ledger](../../cheatsheets/frameworks/token-tax-ledger.md) — Four of six taxes are charged on every turn
- [Grounding Triangle](../../cheatsheets/frameworks/grounding-triangle.md) — Retrieved ≠ cited ≠ verified
- [Tool Surface Audit](../../cheatsheets/frameworks/tool-surface-audit.md) — Six axes per tool — the schema is what the model sees

**Quick reference**

- [Bedrock Converse API](../../cheatsheets/quick-reference/bedrock-converse.md) — Clients, message shape, and the tool-use round trip
- [Prompting for agents](../../cheatsheets/quick-reference/prompt-engineering-for-agents.md) — The three prompts in an agent

**Recipes and procedures**

- [Add a tool properly](../../cheatsheets/how-to/engineers/add-a-tool-properly.md) — 30-minute recipe for a tool the model calls correctly

---

⬅️ [Module 01 · LLM Intuition and the AWS Bridge](../01-llm-and-aws-bridge/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 03 · Amazon Bedrock Agents](../03-bedrock-agents/) ➡️
