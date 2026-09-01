# Portability Matrix

An honest answer to "how much of this is locked to AWS?"

Most of what you learn here is portable. The lock-in is real but narrow, and it is concentrated in the
platform layer — which is also where the managed services earn their cost.

| Capability | Portability | What moves | What you would rebuild |
| --- | --- | --- | --- |
| Prompting, tokens, context budgeting | 🟢 **Total** | All of it | Nothing |
| Agent loop mechanics | 🟢 **Total** | All of it | Nothing |
| Tool schema design | 🟢 **Total** | The schemas themselves | Nothing |
| Multi-agent patterns | 🟢 **Total** | The topology and the reasoning | Framework glue |
| RAG pipeline design | 🟢 **Total** | Chunking, fusion, reranking, evaluation logic | Index and embedding calls |
| Evaluation and gating | 🟢 **Total** | Golden sets, metrics, gate thresholds | Log queries |
| Strands SDK | 🟡 **High** | Open source; runs against non-Bedrock providers | Model provider config |
| LangChain / LangGraph | 🟡 **High** | Provider-agnostic by design | Swap `langchain-aws` for another provider |
| LiteLLM routing | 🟢 **Total** | That is the entire point of it | Nothing |
| Bedrock Converse API | 🟠 **Medium** | The concepts; the message shape is close to common formats | The API calls |
| Bedrock Knowledge Bases | 🟠 **Medium** | Chunking and retrieval strategy | Ingestion and retrieval plumbing |
| Bedrock Guardrails | 🟠 **Medium** | The policy design | Enforcement mechanism |
| Bedrock Agents / Agent Builder | 🔴 **Low** | The design thinking | The whole agent definition |
| AgentCore Runtime / Memory / Identity / Gateway | 🔴 **Low** | Architecture and operational patterns | The platform |

## How to read this

**Green** is the majority of the curriculum, and it is deliberately front-loaded. Modules 00, 01, 05, 07,
09, 10 and 13 are almost entirely portable — that is why you write the agent loop by hand before touching a
framework, and build RAG by hand before touching a managed index.

**Red** is the platform layer. If you deploy on AgentCore you are committing to AWS for the runtime — the
same way choosing Lambda commits you. The *architecture* still transfers: an agent needs a runtime, an
identity, a memory store and a gateway wherever it runs.

## If you are evaluating lock-in seriously

- Keep tool implementations in plain Python behind an interface. Frameworks call them; they do not own them.
- Keep prompts and tool schemas in version-controlled files, not embedded in framework objects.
- Keep your golden set and evaluation harness framework-free. [Module 13](../../modules/13-agentic-qa-and-evaluation/) is written this way.
- Use [LiteLLM](../../modules/10-rag-opensearch-litellm/) if provider optionality is a hard requirement.

---

**Back to:** [Portable concepts](genai-core-concepts.md) &nbsp;·&nbsp; [AWS service map](aws-service-map.md)
