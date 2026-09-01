# 🧠 Module 09 · LLM Memory Mechanics

> What models forget, why, and what you can do about it.

**Estimated time:** 3–4 hours &nbsp;·&nbsp; **Prerequisites:** Module 08 (or Module 06).

Models are stateless. Every 'memory' feature is engineering you or your framework did. This short, sharp module makes that machinery explicit so you stop being surprised by it.

---

## What you will be able to do

- Explain why an LLM has no memory and what each memory strategy actually does
- Implement buffer, summary and vector-backed memory and compare them
- Choose a memory strategy from cost and recall requirements

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Statelessness | AgentCore Memory |
| Buffer memory | Bedrock Knowledge Bases as long-term recall |
| Summary memory |  |
| Vector memory |  |
| Context budgeting |  |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/Mechanics_of_LLM_Memory.pptx`](slides/Mechanics_of_LLM_Memory.pptx) | Mechanics of LLM memory |
| 2 | 📖 | [`slides/langchain_memory_session_deck_v2.md`](slides/langchain_memory_session_deck_v2.md) | Memory session deck |
| 3 | 💻 | [`notebooks/01_demonstration_llm_memory.ipynb`](notebooks/01_demonstration_llm_memory.ipynb) | Memory demonstration |
| 4 | ✏️ | [`exercises/02_activities_llm_memory.ipynb`](exercises/02_activities_llm_memory.ipynb) | Memory activities |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 09 — LLM Memory Mechanics | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Solutions

There is no separate `solutions/` folder because the answers are inline: the
[activities notebook](exercises/02_activities_llm_memory.ipynb) carries `# SOLUTION` cells and collapsed
`<details>` reveals next to each task. Write your own answer into the `my_answer_` variables before you
expand anything.

## Common mistakes

- Summary memory that silently drops the one fact the user cares about.

## Folder map

```
exercises        1 file(s)
notebooks        1 file(s)
slides           3 file(s)
```

## Field guide for this module

Reference material for the ideas in this module — open these while you work, not before.

**Frameworks**

- [Context Budget Ledger](../../cheatsheets/frameworks/context-budget-ledger.md) — The overflow protocol
- [Silent Degradation Watchlist](../../cheatsheets/frameworks/silent-degradation-watchlist.md) — Summary memory drops the decisive fact

**Quick reference**

- [AgentCore](../../cheatsheets/quick-reference/agentcore.md) — Managed memory and retention

**Recipes and procedures**

- [Memory that does not grow forever](../../cheatsheets/how-to/engineers/memory-that-doesnt-grow-forever.md) — Caps, TTLs, and the test everyone skips

---

⬅️ [Module 08 · LangChain and LangGraph](../08-langchain-and-langgraph/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 10 · RAG, OpenSearch and LiteLLM](../10-rag-opensearch-litellm/) ➡️
