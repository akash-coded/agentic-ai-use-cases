# 🔌 Module 12 · A2A and A2UI: Agent Interoperability

> Agents talking to agents, and agents talking to users.

**Estimated time:** 4–5 hours &nbsp;·&nbsp; **Prerequisites:** Module 06 and Module 11.

Two protocols solve two different problems. A2A lets agents from different vendors discover and call each other. A2UI gives an agent a way to render real interface, not just text. Both are early, both matter.

---

## What you will be able to do

- Read and publish an A2A agent card
- Make two independently-built agents complete a task together
- Decide when interop beats a direct tool call
- Render an agent-driven interface with A2UI

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Agent-to-agent protocols | A2A on AgentCore |
| Capability discovery | Strands A2A server |
| Agent-driven UI | AgentCore Gateway |
| Interop trade-offs |  |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/A2A_Protocol_Strands_AgentCore.pptx`](slides/A2A_Protocol_Strands_AgentCore.pptx) | The A2A protocol |
| 2 | ✏️ | [`exercises/exercise_1_read_the_card.md`](exercises/exercise_1_read_the_card.md) | Exercise 1 — read the card |
| 3 | 💻 | [`notebooks/01_A2A_with_Strands.ipynb`](notebooks/01_A2A_with_Strands.ipynb) | A2A with Strands |
| 4 | ✏️ | [`exercises/exercise_2_two_agent_handshake.md`](exercises/exercise_2_two_agent_handshake.md) | Exercise 2 — two-agent handshake |
| 5 | 💻 | [`notebooks/02_A2A_on_AgentCore.ipynb`](notebooks/02_A2A_on_AgentCore.ipynb) | A2A on AgentCore |
| 6 | ✏️ | [`exercises/exercise_3_right_tool_right_job.md`](exercises/exercise_3_right_tool_right_job.md) | Exercise 3 — right tool, right job |
| 7 | 📖 | [`slides/A2UI_The_UI_Layer_for_AI_Agents.pptx`](slides/A2UI_The_UI_Layer_for_AI_Agents.pptx) | A2UI — the UI layer |
| 8 | 💻 | [`notebooks/Notebook_1_A2UI_through_Strands.ipynb`](notebooks/Notebook_1_A2UI_through_Strands.ipynb) | A2UI through Strands |
| 9 | 💻 | [`notebooks/Notebook_2_A2UI_with_AgentCore.ipynb`](notebooks/Notebook_2_A2UI_with_AgentCore.ipynb) | A2UI with AgentCore |
| 10 | ✏️ | [`exercises/A2A_Exercise_Aurora_Grid.md`](exercises/A2A_Exercise_Aurora_Grid.md) | Aurora Grid — the full A2A exercise |
| 11 | ✏️ | [`exercises/mini_project_agent_mesh.md`](exercises/mini_project_agent_mesh.md) | Mini project — agent mesh |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 12 — A2A and A2UI: Agent Interoperability | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Solutions

Worked solutions live in [`solutions/`](solutions/). Attempt every exercise closed-book first — the solutions are written to be read *after* you have a wrong answer to compare against.

## Common mistakes

- Reaching for A2A when a function call would do. Protocols add latency and failure modes.
- Agent cards that overstate capability. Other agents will believe them.

## Folder map

```
exercises        5 file(s)
notebooks        8 file(s)
slides           2 file(s)
solutions        2 file(s)
src              3 file(s)
```

## Field guide for this module

Reference material for the ideas in this module — open these while you work, not before.

**Frameworks**

- [Handoff Multiplier](../../cheatsheets/frameworks/handoff-multiplier.md) — Each protocol hop is a full agent run
- [Tool Surface Audit](../../cheatsheets/frameworks/tool-surface-audit.md) — Trust an agent card like any other tool

**Quick reference**

- [MCP and A2A](../../cheatsheets/quick-reference/mcp-and-a2a.md) — When neither is the answer

---

⬅️ [Module 11 · Amazon Bedrock AgentCore](../11-bedrock-agentcore/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 13 · Agentic QA and Evaluation](../13-agentic-qa-and-evaluation/) ➡️
