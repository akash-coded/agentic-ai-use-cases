# 🦜 Module 08 · LangChain and LangGraph

> The other ecosystem — and an honest side-by-side with Strands.

**Estimated time:** 7–8 hours &nbsp;·&nbsp; **Prerequisites:** Module 05. Module 06 recommended.

LangChain is the framework you will meet in most existing codebases. This module builds it up from first principles — why it exists, what it actually does — then puts it directly against Strands so you can choose with evidence rather than allegiance.

---

## What you will be able to do

- Explain what LangChain abstracts and why chains exist at all
- Build chains, tools, memory and structured output in LangChain
- Model a stateful workflow as a LangGraph graph
- Compare LangChain and Strands on the same task and justify a choice

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Chains and composition | langchain-aws |
| Runnables | Bedrock as a LangChain provider |
| Structured output | LangGraph on Bedrock |
| Graph state machines |  |
| Middleware |  |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/LangChain-from-Zero.pptx`](slides/LangChain-from-Zero.pptx) | LangChain from zero |
| 2 | 💻 | [`notebooks/01_why_langchain_context_and_history.ipynb`](notebooks/01_why_langchain_context_and_history.ipynb) | Why LangChain — context and history |
| 3 | 💻 | [`notebooks/02_essentials_how_langchain_works.ipynb`](notebooks/02_essentials_how_langchain_works.ipynb) | How LangChain actually works |
| 4 | ✏️ | [`exercises/exercise_1_foundations.md`](exercises/exercise_1_foundations.md) | Exercise 1 — foundations |
| 5 | 💻 | [`notebooks/03_basic_langchain.ipynb`](notebooks/03_basic_langchain.ipynb) | Basic LangChain |
| 6 | ✏️ | [`exercises/exercise_2_tools.md`](exercises/exercise_2_tools.md) | Exercise 2 — tools |
| 7 | 💻 | [`notebooks/04_intermediate_langchain.ipynb`](notebooks/04_intermediate_langchain.ipynb) | Intermediate |
| 8 | ✏️ | [`exercises/exercise_3_memory_and_structured_output.md`](exercises/exercise_3_memory_and_structured_output.md) | Exercise 3 — memory and structured output |
| 9 | 💻 | [`notebooks/05_advanced_langchain.ipynb`](notebooks/05_advanced_langchain.ipynb) | Advanced |
| 10 | ✏️ | [`exercises/exercise_4_middleware_and_graphs.md`](exercises/exercise_4_middleware_and_graphs.md) | Exercise 4 — middleware and graphs |
| 11 | 💻 | [`notebooks/PierPoint_LangGraph_Chains_to_Swarms.ipynb`](notebooks/PierPoint_LangGraph_Chains_to_Swarms.ipynb) | LangGraph: chains to swarms |
| 12 | 💻 | [`notebooks/06_langchain_vs_strands_side_by_side.ipynb`](notebooks/06_langchain_vs_strands_side_by_side.ipynb) | LangChain vs Strands, side by side |
| 13 | ✏️ | [`exercises/exercise_5_multiagent_capstone.md`](exercises/exercise_5_multiagent_capstone.md) | Exercise 5 — multi-agent capstone |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 08 — LangChain and LangGraph | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Solutions

Worked solutions live in [`solutions/`](solutions/). Attempt every exercise closed-book first — the solutions are written to be read *after* you have a wrong answer to compare against.

## Common mistakes

- Cargo-culting chains. If a function would do, use a function.
- LangGraph state that grows without bound — checkpointing is not free.

## Folder map

```
exercises       12 file(s)
notebooks       10 file(s)
slides           3 file(s)
solutions       12 file(s)
```

---

⬅️ [Module 07 · Multi-Agent Patterns with Strands](../07-strands-multi-agent-patterns/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 09 · LLM Memory Mechanics](../09-llm-memory/) ➡️
