# 🧵 Module 06 · Strands Foundations: Tools, Memory and MCP

> Agents with hands, memory, and a standard way to reach the outside world.

**Estimated time:** 5–6 hours &nbsp;·&nbsp; **Prerequisites:** Module 05.

Strands is AWS's open-source agent framework. This module covers the three things that turn a chat wrapper into an agent: tools it can call, memory it can keep, and MCP servers it can connect to.

---

## What you will be able to do

- Build a Strands agent with custom tools and a clear tool catalogue
- Add conversational and persistent memory, and know the difference
- Connect an agent to an MCP server and call its tools
- Design a tool schema that the model calls correctly the first time

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Tool design | Strands Agents SDK |
| Short vs long-term memory | Bedrock model providers |
| Model Context Protocol | AgentCore Memory |
| Agent composition |  |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/Strands_Deck1_Foundation.pptx`](slides/Strands_Deck1_Foundation.pptx) | Strands foundations |
| 2 | 💻 | [`notebooks/01_strands_foundations.ipynb`](notebooks/01_strands_foundations.ipynb) | Foundations notebook |
| 3 | ✏️ | [`exercises/build-1-give-the-agent-a-job.md`](exercises/build-1-give-the-agent-a-job.md) | Build 1 — give the agent a job |
| 4 | 💻 | [`notebooks/02_strands_tools_memory_mcp.ipynb`](notebooks/02_strands_tools_memory_mcp.ipynb) | Tools, memory and MCP |
| 5 | 📊 | [`activities/Tool_Catalog.xlsx`](activities/Tool_Catalog.xlsx) | Design your tool catalogue |
| 6 | ✏️ | [`exercises/build-2-the-toolsmith.md`](exercises/build-2-the-toolsmith.md) | Build 2 — the toolsmith |
| 7 | 📖 | [`slides/Strands_Deck2_Advanced.pptx`](slides/Strands_Deck2_Advanced.pptx) | Strands, advanced |
| 8 | 💻 | [`notebooks/03_strands_multiagent_capstone.ipynb`](notebooks/03_strands_multiagent_capstone.ipynb) | Multi-agent capstone |
| 9 | 💻 | [`notebooks/04_strands_multiagent_deepdive.ipynb`](notebooks/04_strands_multiagent_deepdive.ipynb) | Multi-agent deep dive |
| 10 | ✏️ | [`exercises/build-3-open-sandbox.md`](exercises/build-3-open-sandbox.md) | Build 3 — open sandbox |
| 11 | ✏️ | [`exercises/take-home-build-your-own-agent.md`](exercises/take-home-build-your-own-agent.md) | Take-home — build your own agent |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 06 — Strands Foundations: Tools, Memory and MCP | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Solutions

This module has no separate solution set; the notebooks carry the worked answers inline.

## Common mistakes

- Tool descriptions written for humans, not models. The model only has the schema.
- Confusing conversation history with memory. History is a buffer; memory is a decision about what to keep.

## Folder map

```
activities       5 file(s)
assets           1 file(s)
exercises        4 file(s)
notebooks        5 file(s)
slides           2 file(s)
src              2 file(s)
```

---

⬅️ [Module 05 · The Agent Loop: No Framework to Strands](../05-agent-loop-no-framework-to-strands/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 07 · Multi-Agent Patterns with Strands](../07-strands-multi-agent-patterns/) ➡️
