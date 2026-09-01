# ⚙️ Module 11 · Amazon Bedrock AgentCore

> Runtime, memory, identity, gateway, observability — agents as deployed services.

**Estimated time:** 8–10 hours &nbsp;·&nbsp; **Prerequisites:** Modules 05–06. Module 08 for the LangGraph deployment.

Everything so far ran in a notebook. AgentCore is how an agent becomes a service with an identity, a memory store, a gateway, traces and a bill. This module deploys agents three ways — Strands, LangGraph, and no framework at all — so you can see the runtime is framework-agnostic.

---

## What you will be able to do

- Deploy an agent to AgentCore Runtime and invoke it as a service
- Wire AgentCore Memory and reason about retention
- Configure identity and tool access with least privilege
- Route traffic through the gateway and read the traces
- Estimate runtime cost and capacity before you commit

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Agent as a service | Bedrock AgentCore Runtime |
| Session and identity | AgentCore Memory |
| Observability | AgentCore Identity |
| Harness engineering | AgentCore Gateway |
|  | AgentCore Observability |
|  | CloudWatch |
|  | IAM |
|  | CDK |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/AgentCore_Part1_Foundations.pptx`](slides/AgentCore_Part1_Foundations.pptx) | AgentCore foundations |
| 2 | 💻 | [`notebooks/00_setup_and_sanity.ipynb`](notebooks/00_setup_and_sanity.ipynb) | Setup and sanity check |
| 3 | 📖 | [`walkthroughs/01_agentcore_foundations.md`](walkthroughs/01_agentcore_foundations.md) | Foundations walkthrough |
| 4 | 💻 | [`notebooks/01_build_an_agent_three_ways.ipynb`](notebooks/01_build_an_agent_three_ways.ipynb) | One agent, three ways |
| 5 | 💻 | [`notebooks/02_agentcore_runtime.ipynb`](notebooks/02_agentcore_runtime.ipynb) | Runtime |
| 6 | 💻 | [`walkthroughs/AgentCore_01_Strands_Minimum_Deploy.ipynb`](walkthroughs/AgentCore_01_Strands_Minimum_Deploy.ipynb) | Minimum deploy — Strands |
| 7 | 💻 | [`walkthroughs/AgentCore_02_NoFramework_Minimum_Deploy.ipynb`](walkthroughs/AgentCore_02_NoFramework_Minimum_Deploy.ipynb) | Minimum deploy — no framework |
| 8 | 💻 | [`walkthroughs/AgentCore_03_LangGraph_Minimum_Deploy.ipynb`](walkthroughs/AgentCore_03_LangGraph_Minimum_Deploy.ipynb) | Minimum deploy — LangGraph |
| 9 | 💻 | [`notebooks/03_memory.ipynb`](notebooks/03_memory.ipynb) | Memory |
| 10 | 💻 | [`notebooks/04_tools_and_identity.ipynb`](notebooks/04_tools_and_identity.ipynb) | Tools and identity |
| 11 | ✏️ | [`exercises/exercise_A_parcelpilot.md`](exercises/exercise_A_parcelpilot.md) | Exercise A — ParcelPilot |
| 12 | 📖 | [`slides/AgentCore_Part2_Advanced.pptx`](slides/AgentCore_Part2_Advanced.pptx) | AgentCore advanced |
| 13 | 💻 | [`notebooks/05_multi_agent_orchestration.ipynb`](notebooks/05_multi_agent_orchestration.ipynb) | Multi-agent orchestration |
| 14 | 📖 | [`walkthroughs/03_harness_engineering.md`](walkthroughs/03_harness_engineering.md) | Harness engineering |
| 15 | ✏️ | [`exercises/exercise_B_voltdesk.md`](exercises/exercise_B_voltdesk.md) | Exercise B — VoltDesk |
| 16 | 💻 | [`notebooks/07_production_patterns.ipynb`](notebooks/07_production_patterns.ipynb) | Production patterns |
| 17 | 📊 | [`activities/AgentCore_Cost_and_Capacity_Workbench.xlsx`](activities/AgentCore_Cost_and_Capacity_Workbench.xlsx) | Cost and capacity workbench |
| 18 | ✏️ | [`exercises/exercise_END_renewq.md`](exercises/exercise_END_renewq.md) | Final exercise — RenewQ |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 11 — Amazon Bedrock AgentCore | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Project artefact

`src/MyFirstRuntimeAgent` is a complete CDK-managed AgentCore project — app code, infrastructure, and configuration.

## Solutions

This module has no separate solution set; the notebooks carry the worked answers inline.

## Common mistakes

- Deploying without a memory retention decision. Storage grows, and so does the bill.
- Over-broad IAM on the runtime role. Scope tools to what the agent actually needs.
- Skipping observability until something breaks in production.

## Folder map

```
activities       3 file(s)
exercises        4 file(s)
notebooks       12 file(s)
slides           2 file(s)
src             31 file(s)
walkthroughs    14 file(s)
```

---

⬅️ [Module 10 · RAG, OpenSearch and LiteLLM](../10-rag-opensearch-litellm/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 12 · A2A and A2UI: Agent Interoperability](../12-a2a-and-a2ui-interop/) ➡️
