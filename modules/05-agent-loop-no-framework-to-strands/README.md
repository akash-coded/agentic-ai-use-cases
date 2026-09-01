# 🔁 Module 05 · The Agent Loop: No Framework to Strands

> Write the loop by hand, feel the pain, then let Strands remove it.

**Estimated time:** 5–6 hours &nbsp;·&nbsp; **Prerequisites:** Module 02. Module 03 helps but is not required.

The best way to understand a framework is to build what it replaces. You will write a working agent loop in plain Python, hit every sharp edge, and only then meet Strands — at which point every abstraction it offers will be obvious rather than magical.

---

## What you will be able to do

- Write a complete agent loop with no framework at all
- Explain exactly what a framework abstracts away, and what it costs you
- Build the same agent in Strands in a fraction of the code
- Choose deliberately between hand-rolled and framework code

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Agent loop mechanics | Bedrock Converse API |
| Tool dispatch | Strands on Bedrock |
| State management | AgentCore preview |
| Framework trade-offs |  |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/Day6_Deck1_Agent_Loop.pptx`](slides/Day6_Deck1_Agent_Loop.pptx) | The agent loop, from first principles |
| 2 | 💻 | [`notebooks/Day6_Demo_0_Foundations.ipynb`](notebooks/Day6_Demo_0_Foundations.ipynb) | Foundations |
| 3 | 💻 | [`notebooks/Day6_Demo_1_NoStrands.ipynb`](notebooks/Day6_Demo_1_NoStrands.ipynb) | The hand-built loop — no framework |
| 4 | ✏️ | [`exercises/Day6_Exercise.ipynb`](exercises/Day6_Exercise.ipynb) | Exercise: extend the hand-built loop |
| 5 | 📖 | [`slides/Day6_Deck2_Strands_AgentCore.pptx`](slides/Day6_Deck2_Strands_AgentCore.pptx) | Strands and AgentCore |
| 6 | 💻 | [`notebooks/Day6_Demo_2_Strands.ipynb`](notebooks/Day6_Demo_2_Strands.ipynb) | The same agent in Strands |
| 7 | 💻 | [`notebooks/Day6_Demo_2b_Strands_Advanced.ipynb`](notebooks/Day6_Demo_2b_Strands_Advanced.ipynb) | Strands, further |
| 8 | ✏️ | [`exercises/Day6_Exercise_2b.ipynb`](exercises/Day6_Exercise_2b.ipynb) | Exercise 2b |
| 9 | 💻 | [`notebooks/Day6_Demo_3_AgentCore.ipynb`](notebooks/Day6_Demo_3_AgentCore.ipynb) | First look at AgentCore |
| 10 | ✏️ | [`exercises/Day6_Capstone_TravelMind_Desk.ipynb`](exercises/Day6_Capstone_TravelMind_Desk.ipynb) | Capstone: TravelMind desk |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 05 — The Agent Loop: No Framework to Strands | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Solutions

Worked solutions live in [`solutions/`](solutions/). Attempt every exercise closed-book first — the solutions are written to be read *after* you have a wrong answer to compare against.

## Common mistakes

- Reaching for a framework before you can write the loop. You will not be able to debug it.
- Assuming Strands hides Bedrock. It does not — model IDs and access still apply.

## Folder map

```
activities       1 file(s)
exercises        4 file(s)
guides           1 file(s)
notebooks        6 file(s)
slides           2 file(s)
solutions        4 file(s)
```

---

⬅️ [Module 04 · Agent Builder, Knowledge Bases and Guardrails](../04-agent-builder-and-knowledge-bases/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 06 · Strands Foundations: Tools, Memory and MCP](../06-strands-foundations/) ➡️
