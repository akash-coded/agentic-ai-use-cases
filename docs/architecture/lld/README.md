# Low-Level Design Index

Each module zoomed in: the mechanism, its components, the contracts between them, and the ways it breaks. Start from the [high-level design](../README.md) if you want the whole system first.

| Module | What the LLD covers |
| --- | --- |
| **[00 · Agentic Foundations](00-agentic-foundations.md)** | The decision procedure that runs *before* any code: is this an agent, and what would make it good? |
| **[01 · LLM Intuition and the AWS Bridge](01-llm-and-aws-bridge.md)** | The mapping from model behaviour to Bedrock configuration choices. |
| **[02 · Amazon Bedrock Essentials](02-bedrock-essentials.md)** | The Converse API request/response cycle, including the tool-use round trip that most people get wrong. |
| **[03 · Amazon Bedrock Agents](03-bedrock-agents.md)** | What the managed agent loop does on your behalf, and how to see inside it. |
| **[04 · Agent Builder, Knowledge Bases and Guardrails](04-agent-builder-and-knowledge-bases.md)** | How a knowledge base is wired to an agent, and where grounding actually happens. |
| **[05 · The Agent Loop: No Framework to Strands](05-agent-loop-no-framework-to-strands.md)** | The loop itself — first written out, then replaced by a framework, with the difference made explicit. |
| **[06 · Strands Foundations: Tools, Memory and MCP](06-strands-foundations.md)** | Tools, memory and MCP as three separable concerns inside a Strands agent. |
| **[07 · Multi-Agent Patterns with Strands](07-strands-multi-agent-patterns.md)** | Four topologies, their cost profile, and the selection rule between them. |
| **[08 · LangChain and LangGraph](08-langchain-and-langgraph.md)** | Composition in LangChain, state in LangGraph, and an evidence-based comparison with Strands. |
| **[09 · LLM Memory Mechanics](09-llm-memory.md)** | Three memory strategies, what each drops, and the cost of each. |
| **[10 · RAG, OpenSearch and LiteLLM](10-rag-opensearch-litellm.md)** | The full retrieval pipeline, stage by stage, with a measurable gate at the end. |
| **[11 · Amazon Bedrock AgentCore](11-bedrock-agentcore.md)** | The five AgentCore primitives and how a deployed agent uses each. |
| **[12 · A2A and A2UI: Agent Interoperability](12-a2a-and-a2ui-interop.md)** | Capability discovery between agents, and agent-driven interface. |
| **[13 · Agentic QA and Evaluation](13-agentic-qa-and-evaluation.md)** | The test pyramid for non-deterministic systems, ending in a gate that blocks a deploy. |
| **[14 · End-to-End Production Pipeline](14-end-to-end-production.md)** | Build, validate, deploy, route, fail over, gate — the whole release path. |
| **[15 · Agentic Product Lifecycle](15-agentic-product-lifecycle.md)** | The artefact set owed at each gate, and the decisions each gate forces. |

---

[🏛️ Back to HLD](../README.md) · [📚 All modules](../../../modules/)
