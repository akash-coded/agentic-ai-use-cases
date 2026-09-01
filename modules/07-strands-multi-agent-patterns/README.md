# 🕸️ Module 07 · Multi-Agent Patterns with Strands

> Swarm, graph, delegation, critique — and when each one is wrong.

**Estimated time:** 6–7 hours &nbsp;·&nbsp; **Prerequisites:** Module 06.

Multi-agent is not automatically better. This module teaches the patterns as a menu with costs attached: what each buys you, what it costs in tokens and latency, and the failure mode each invites.

---

## What you will be able to do

- Implement swarm, graph, delegation and critique patterns in Strands
- Choose a pattern from requirements rather than fashion
- Predict the token and latency cost of a topology before running it
- Debug a multi-agent system where the failure is in the handoff, not the agent

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Swarm | Strands multi-agent primitives |
| Graph orchestration | Bedrock model routing |
| Delegation |  |
| Critique/reflection loops |  |
| Deterministic vs autonomous orchestration |  |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/Advanced_Strands_Multi_Agent_Patterns_SLIDES.md`](slides/Advanced_Strands_Multi_Agent_Patterns_SLIDES.md) | Advanced multi-agent patterns |
| 2 | 💻 | [`notebooks/NB1_Foundations_Workflow_Patterns.ipynb`](notebooks/NB1_Foundations_Workflow_Patterns.ipynb) | NB1 — workflow patterns |
| 3 | ✏️ | [`exercises/Exercise_1_Foundations.md`](exercises/Exercise_1_Foundations.md) | Exercise 1 — foundations |
| 4 | ✏️ | [`exercises/Exercise_2_Dials_and_Cost.md`](exercises/Exercise_2_Dials_and_Cost.md) | Exercise 2 — dials and cost |
| 5 | 💻 | [`notebooks/NB2_Agentic_Patterns.ipynb`](notebooks/NB2_Agentic_Patterns.ipynb) | NB2 — agentic patterns |
| 6 | ✏️ | [`exercises/Exercise_3_Delegation_and_Critique.md`](exercises/Exercise_3_Delegation_and_Critique.md) | Exercise 3 — delegation and critique |
| 7 | 💻 | [`notebooks/NB3_Autonomous_Deterministic_Orchestration.ipynb`](notebooks/NB3_Autonomous_Deterministic_Orchestration.ipynb) | NB3 — autonomous vs deterministic |
| 8 | ✏️ | [`exercises/Exercise_4_Swarm_and_Graph.md`](exercises/Exercise_4_Swarm_and_Graph.md) | Exercise 4 — swarm and graph |
| 9 | 💻 | [`notebooks/PierPoint_Release_Desk_Graph_vs_Swarm.ipynb`](notebooks/PierPoint_Release_Desk_Graph_vs_Swarm.ipynb) | PierPoint: graph vs swarm, head to head |
| 10 | ✏️ | [`exercises/Exercise_5_Capstone_Composition.md`](exercises/Exercise_5_Capstone_Composition.md) | Exercise 5 — capstone composition |
| 11 | ✏️ | [`exercises/Coding_Exercise_3_Advanced.ipynb`](exercises/Coding_Exercise_3_Advanced.ipynb) | Advanced coding exercise |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 07 — Multi-Agent Patterns with Strands | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Solutions

Worked solutions live in [`solutions/`](solutions/). Attempt every exercise closed-book first — the solutions are written to be read *after* you have a wrong answer to compare against.

## Common mistakes

- Adding agents to fix a prompt problem. More agents multiply the prompt problem.
- Swarms with no termination condition. They will happily run until your budget ends.
- Ignoring that every handoff re-sends context. Topology is a cost decision.

## Folder map

```
exercises        9 file(s)
notebooks        8 file(s)
slides           1 file(s)
solutions        9 file(s)
src              1 file(s)
```

## Field guide for this module

Reference material for the ideas in this module — open these while you work, not before.

**Frameworks**

- [Handoff Multiplier](../../cheatsheets/frameworks/handoff-multiplier.md) — H× — what a topology costs versus one agent
- [Cost Cliff Map](../../cheatsheets/frameworks/cost-cliff-map.md) — Unbounded swarms are cliff 3
- [Three Clocks](../../cheatsheets/frameworks/three-clocks.md) — Turns multiply two of the three clocks

**Quick reference**

- [Strands](../../cheatsheets/quick-reference/strands.md) — Graph, swarm, delegation in code

**Recipes and procedures**

- [Choose a topology](../../cheatsheets/how-to/architects/choose-a-topology.md) — Choose one and justify it in an hour

---

⬅️ [Module 06 · Strands Foundations: Tools, Memory and MCP](../06-strands-foundations/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 08 · LangChain and LangGraph](../08-langchain-and-langgraph/) ➡️
