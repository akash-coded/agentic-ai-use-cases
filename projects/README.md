# Projects

Build-something-real work, at three scales. The [modules](../modules/) teach; these are where you put it
together and end up with an artefact you can show someone.

---

## Standalone project

### 🪨 [Bedrock Mini-Project](bedrock-mini-project/)

**~4 hours core, +4 in stretch tiers.** A self-contained build with scripts, knowledge-base documents and a
cost analysis. Pick one of three templates — internal knowledge assistant, customer support bot, or
research assistant — and take it as far as you want.

> Its [`README.md`](bedrock-mini-project/README.md) is a **scaffold with TODOs for you to fill in**, not
> documentation to read. Filling it in *is* part of the exercise: problem statement, tier reached,
> template chosen, and a [reflection](bedrock-mini-project/reflection.md).

**Pairs with:** [Module 02](../modules/02-bedrock-essentials/)

---

## Reference implementations inside modules

Complete, working systems you can read, run and lift into your own work.

| Project | What it is | Lift it for |
| --- | --- | --- |
| 🔍 **[`ragkit`](../modules/10-rag-opensearch-litellm/labs/rag-labs/ragkit/)** | A full retrieval library — chunking, dense and lexical retrieval, RRF fusion, reranking, context packing, evaluation, cost accounting | Any RAG pipeline you build |
| ⚙️ **[`MyFirstRuntimeAgent`](../modules/11-bedrock-agentcore/src/MyFirstRuntimeAgent/)** | A complete CDK-managed AgentCore project — app code, infrastructure, MCP client, model loading | Your first AgentCore deployment |
| 🔬 **[QA pipeline](../modules/13-agentic-qa-and-evaluation/src/)** | Golden set, contract tests, multi-agent tests, and a quality gate that exits non-zero | Any agent you need to gate |
| 🚀 **[Production pipeline](../modules/14-end-to-end-production/src/)** | Agent, runtime wrapper, model failover, release script, version manifest, readiness checklist, IAM policy | Taking an agent to production |

The QA and production sets are the two most reusable. Between them they are most of what separates a
notebook from a service.

---

## Capstone exercises

Larger builds that close a module or a track. Each ships with a worked solution.

| Capstone | Domain | Closes | Solution |
| --- | --- | --- | --- |
| 🚂 **[RailReserve](../modules/14-end-to-end-production/exercises/Capstone_RailReserve.md)** | Rail booking | The whole curriculum | [✓](../modules/14-end-to-end-production/solutions/Solution_Capstone_RailReserve.md) |
| 🧳 **[TravelMind Desk](../modules/05-agent-loop-no-framework-to-strands/exercises/Day6_Capstone_TravelMind_Desk.ipynb)** | Travel ops | Agent loop → Strands | [✓](../modules/05-agent-loop-no-framework-to-strands/solutions/Day6_Capstone_TravelMind_Desk_SOLUTION.ipynb) |
| 🕸️ **[Capstone Composition](../modules/07-strands-multi-agent-patterns/exercises/Exercise_5_Capstone_Composition.md)** | Multi-agent | Topology selection | [✓](../modules/07-strands-multi-agent-patterns/solutions/Exercise_5_Capstone_Composition_SOLUTION.md) |
| 🌐 **[Aurora Grid](../modules/12-a2a-and-a2ui-interop/exercises/A2A_Exercise_Aurora_Grid.md)** | Energy grid | A2A interop | [✓](../modules/12-a2a-and-a2ui-interop/solutions/Aurora_Grid_A2A_Solution.ipynb) |
| 📚 **[Consolidated RAG take-home](../modules/10-rag-opensearch-litellm/exercises/EX6_consolidated_takehome.md)** | Retrieval | The RAG track | [✓](../modules/10-rag-opensearch-litellm/solutions/SOL_EX6_consolidated_takehome.md) |
| 🛠️ **[Build your own agent](../modules/06-strands-foundations/exercises/take-home-build-your-own-agent.md)** | Your choice | Strands foundations | — |

**RailReserve is the one to aim for.** New domain, nothing pre-built for you, taken all the way through
build → evaluate → deploy → gate → rollback.

---

## If you want something to show

The most persuasive artefact is not a working agent. It is a working agent **with its numbers**:

| Have | Because |
| --- | --- |
| Cost per resolved task, measured | Everyone asks, almost nobody knows |
| A golden set with cases it fails | Proves the evaluation is honest |
| An abstention rate you designed | Shows you thought about being wrong |
| A rehearsed rollback, timed | Separates a demo from a service |
| One page of decisions and what you rejected | The [PRD templates](../docs/prd/) give you the shape |

Built something? **[Share it in Show and tell](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/show-and-tell)** —
what it does, which modules it came from, and what was harder than expected.

---

[🏠 Repository](../) · [📚 Curriculum](../modules/) · [🧭 Field guide](../cheatsheets/) ·
[📋 Sample PRDs](../docs/prd/)
