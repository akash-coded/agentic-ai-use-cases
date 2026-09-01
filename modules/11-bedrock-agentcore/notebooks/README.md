# AgentCore, hands-on — from scratch to a deployed multi-agent system

An eight-notebook series that takes you from "what is AgentCore" to a deployed, observable, **production-hardened** multi-agent travel agent. Built for people who already know Bedrock Agents, the console Agent Builder, and the Strands SDK, and now want **Amazon Bedrock AgentCore**.

Anchor use case throughout: **TravelMind**, a flight-disruption / rebooking assistant.

---

## Read this first (the honest framing)

- **Region is `us-east-1`. Models are Claude Haiku 4.5 and Sonnet 4.5.** No ambiguity, no placeholders to guess. Model IDs carry the required `us.` cross-region inference prefix.
- **Every API in these notebooks was verified against the installed packages** (introspected live, June 2026) — not recalled from memory. Versions are pinned in `requirements.txt`.
- **Cells that call AWS are correct-by-construction.** They need *your* credentials and *your* model access to actually run. Each notebook opens with a sanity/preflight check, the same way the official samples expect you to export credentials first.
- **There are two deploy tools, and that matters in 2026.** The Python **starter toolkit** (`Runtime().configure/launch/invoke`) runs inside a notebook, so we teach with it. The **`@aws/agentcore` CLI** is now the AWS-recommended project workflow — we show its exact equivalents. The toolkit is labelled *legacy* but is fully functional today. We don't pretend there's one canonical path.

---

## Prerequisites

- An AWS account with **Bedrock model access enabled for Claude 4.x in `us-east-1`**.
- IAM permissions: `AmazonBedrockFullAccess` + `BedrockAgentCoreFullAccess` on your principal (tighten later).
- **Python 3.10+**. For the CLI sections, **Node.js 20+**.
- Comfort with Strands `Agent` / `@tool` (notebook 01 recaps it, but lightly).

---

## Setup

**VS Code / local**

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name agentcore --display-name "Python (agentcore)"
playwright install chromium           # only for the Browser section (notebook 04)
# set credentials: aws configure   (or export AWS_* env vars)
```

Then open the notebooks and select the **Python (agentcore)** kernel.

**Google Colab**

```python
!pip install -r requirements.txt
# credentials via Colab secrets (userdata) or env vars — shown in notebook 00
```

---

## The series

| # | Notebook | What you learn | Key APIs |
|---|---|---|---|
| 00 | `00_setup_and_sanity` | The 3-layer mental model (Converse → Agents → AgentCore); install; creds; a working preflight that scans model lifecycle | `bedrock-runtime` Converse, `bedrock` ListFoundationModels |
| 01 | `01_build_an_agent_three_ways` | The *same* agent built without a framework (raw Converse tool loop), via Bedrock Agents / RETURN_CONTROL, and via Strands | `Converse` tool loop, `InvokeInlineAgent`, Strands `Agent` |
| 02 | `02_agentcore_runtime` | Put an agent in production: the HTTP contract, `app.py`, local test, deploy, sessions, raw invoke, CLI equivalents | `BedrockAgentCoreApp`, `Runtime`, `invoke_agent_runtime` |
| 03 | `03_memory` | Short-term vs long-term memory, the four strategies, a memory **hook** for Strands, branches for data handoff | `MemoryClient`, `create_event`, `retrieve_memories`, Strands hooks |
| 04 | `04_tools_and_identity` | Code Interpreter (exact math), Browser (live web), Gateway (your APIs as MCP tools), Identity (inbound + outbound auth) | `AgentCoreCodeInterpreter`, `AgentCoreBrowser`, `create_gateway`, `@requires_api_key` |
| 05 | `05_multi_agent_orchestration` | Every coordination pattern: agents-as-tools, sequential graph, conditional+parallel graph, Swarm, A2A | `GraphBuilder`, `Swarm`, `A2AServer`, `MCPClient` |
| 06 | `06_travelmind_capstone` | Assemble it all — memory + tools + multi-agent core, deployed on Runtime, observable | everything above |
| 07 | `07_production_patterns` | Harden it for real traffic: orchestrator pool (LRU+TTL, thread-safe), retries/backoff, bounded context, S3 sessions, observability, validation, guardrails, readiness/warmup, cost-aware routing | pool + `boto_client_config` retries, `SlidingWindowConversationManager`, `S3SessionManager`, `@app.ping`, `cache_prompt` |

Run them in order. Each builds on the last; 03–05 feed the capstone (06), and 07 hardens it.

---

## How these were built (so you can trust the code)

- Package signatures were **introspected from the installed libraries**, not written from memory.
- Every notebook passes an **AST syntax validation** of all code cells.
- Every framework construct (agents, hooks, graphs, swarm, A2A server, the runtime app, the full capstone) was **constructed offline** to confirm it builds on `strands-agents 1.42.0` / `bedrock-agentcore 1.14.0`.
- Sources used for grounding: the `awslabs/agentcore-samples` repository structure and the public dev.to TravelMind walkthrough. The architecture is faithful to those; the data is mock.

---

## Honest caveats (don't get surprised)

- **Gateway target schema is left as a fill-in.** Creating a gateway + target is shown with verified top-level calls, but the deep `targetConfiguration.mcp` shape (your Lambda ARN or OpenAPI document) is marked `"...": "your backend here"` rather than fabricated. The **connection** code (MCPClient → gateway) is concrete and runnable.
- **Long-term memory extraction is asynchronous.** Right after writing events, `retrieve_memories` may return nothing for a moment. Short-term reads are immediate.
- **The capstone rebuilds the orchestrator per invocation** to scope memory to the right traveler. That's correct, not optimal — specialists are already cached at module level; tune pooling for real load.
- **The mock tools are mocks.** The capstone is one orchestrator + three specialists with fake backends. Swap in Gateway-fronted real APIs, put secrets in Identity, and add a JWT authorizer before you call anything production.

---

## Where to go next

- Replace mock tools with **Gateway**-fronted real services; move secrets into **Identity**.
- Put a **JWT/OAuth authorizer** in front of the runtime.
- Adopt the **`@aws/agentcore` CLI** for a real project + CI/CD.
- Turn on **evaluators / online-eval** and watch **CloudWatch GenAI Observability**.
- For concurrent session persistence, use **`S3SessionManager`** rather than file-based sessions.
