# Architecture: High-Level Design

Two systems are described here. The first is **the curriculum itself** — how 16 modules compose into a
capability. The second is **TravelMind**, the reference application you build across them.

Zoom into any module's internals via the [LLD index](lld/).

---

## 1. The curriculum as a system

```mermaid
flowchart TB
    subgraph T1["Track 1 · Think — no cloud required"]
        M00["00 Agentic Foundations"]
        M01["01 LLM and AWS Bridge"]
    end
    subgraph T2["Track 2 · Invoke — managed AWS"]
        M02["02 Bedrock Essentials"]
        M03["03 Bedrock Agents"]
        M04["04 Agent Builder and KBs"]
    end
    subgraph T3["Track 3 · Build — frameworks"]
        M05["05 No Framework to Strands"]
        M06["06 Strands Foundations"]
        M07["07 Multi-Agent Patterns"]
        M08["08 LangChain and LangGraph"]
        M09["09 LLM Memory"]
    end
    subgraph T4["Track 4 · Ground — retrieval"]
        M10["10 RAG, OpenSearch, LiteLLM"]
    end
    subgraph T5["Track 5 · Ship — platform"]
        M11["11 AgentCore"]
        M12["12 A2A and A2UI"]
        M13["13 QA and Evaluation"]
        M14["14 End-to-End Production"]
    end
    M15["15 Agentic Product Lifecycle<br/><i>parallel track</i>"]

    M00 --> M01 --> M02 --> M03 --> M04
    M02 --> M05 --> M06 --> M07
    M05 --> M08 --> M09
    M02 --> M10
    M06 & M08 --> M11 --> M12
    M11 --> M13 --> M14
    M10 --> M14
    M00 -.-> M15
    M15 -.-> M14
```

**Design rule behind the ordering:** every abstraction is preceded by the thing it abstracts. You write the
agent loop before meeting Strands (05 → 06). You build RAG by hand before touching a managed knowledge base
(10). You test before you deploy (13 → 14). Nothing is magic because you built the previous layer.

## 2. Learning-flow model

```mermaid
flowchart LR
    R["📖 Read<br/>deck or guide"] --> D["💻 Run<br/>notebook"]
    D --> P["✏️ Practise<br/>exercise"]
    P --> S{"Stuck?"}
    S -->|yes| SOL["📗 Compare with<br/>solution"]
    S -->|no| W["📊 Workbook<br/>decide and record"]
    SOL --> W
    W --> N["Next module"]
```

Every module follows this shape. The workbook step matters: it is where a design decision gets written
down and costed, which is what makes it defensible later.

## 3. TravelMind — the reference application

TravelMind is a travel-operations agent. It appears first in Module 02 as a single Bedrock call and is
still there in Module 14 as a gated, deployed, multi-agent service. Same domain, growing architecture.

```mermaid
flowchart TB
    U["User / calling system"] --> GW["AgentCore Gateway"]
    GW --> RT["AgentCore Runtime<br/><i>TravelMind orchestrator</i>"]

    RT --> MEM["AgentCore Memory<br/>session + long-term"]
    RT --> ID["AgentCore Identity<br/>scoped credentials"]

    RT --> SUB1["Flight agent"]
    RT --> SUB2["Refund agent"]
    RT --> SUB3["Disruption agent"]

    SUB1 & SUB2 & SUB3 --> BR["Bedrock Converse<br/>+ Guardrails"]
    SUB2 --> KB["Knowledge Base<br/>policy documents"]
    KB --> OSS["OpenSearch Serverless"]
    SUB1 --> LMB["Lambda action groups<br/>booking systems"]

    RT --> OBS["AgentCore Observability"]
    OBS --> CW["CloudWatch"]
    CW --> GATE["Quality gate<br/>blocks promotion"]

    style GATE fill:#8b2e2e,color:#fff
    style BR fill:#1f5f8b,color:#fff
    style RT fill:#1f5f8b,color:#fff
```

### Where each module contributes

| Layer | Built in | Notebook to read first |
| --- | --- | --- |
| Model invocation, guardrails | [02](../../modules/02-bedrock-essentials/) | `converse_api_masterclass.ipynb` |
| Managed agent + action groups | [03](../../modules/03-bedrock-agents/) | `03_action_groups.ipynb` |
| Knowledge base grounding | [04](../../modules/04-agent-builder-and-knowledge-bases/) | `kb_guardrails_travelmind_notebook.ipynb` |
| Orchestrator and sub-agents | [06](../../modules/06-strands-foundations/), [07](../../modules/07-strands-multi-agent-patterns/) | `03_strands_multiagent_capstone.ipynb` |
| Retrieval quality | [10](../../modules/10-rag-opensearch-litellm/) | `labs/rag-labs/04_retrieval_reranking.ipynb` |
| Runtime, memory, identity, gateway | [11](../../modules/11-bedrock-agentcore/) | `02_agentcore_runtime.ipynb` |
| Evaluation and the gate | [13](../../modules/13-agentic-qa-and-evaluation/) | `src/quality_gate.py` |
| Release, failover, rollback | [14](../../modules/14-end-to-end-production/) | `deploy_e2e.ipynb` |

A rendered reference architecture image also ships with Module 14:
[`reference_architecture.png`](../../modules/14-end-to-end-production/assets/reference_architecture.png).

## 4. Request lifecycle

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant G as Gateway
    participant O as Orchestrator
    participant M as Memory
    participant S as Sub-agent
    participant B as Bedrock
    participant K as Knowledge Base

    U->>G: request
    G->>O: authenticated invoke
    O->>M: load session context
    M-->>O: prior turns + facts
    O->>B: plan (Converse + tool schemas)
    B-->>O: tool call decision
    O->>S: delegate sub-task
    S->>K: retrieve grounding
    K-->>S: passages + citations
    S->>B: answer from context
    B-->>S: draft
    S-->>O: result
    O->>B: compose final (guardrails applied)
    B-->>O: response
    O->>M: persist what matters
    O-->>G: response + trace id
    G-->>U: answer
```

Note steps 4 and 12: memory is a read *and* a write decision, and both cost money. Note step 13: the trace
id is what makes [Module 13](../../modules/13-agentic-qa-and-evaluation/) possible at all.

## 5. Cost model

Cost lands in four places. Each has a module that teaches you to control it:

| Driver | Controlled by | Where |
| --- | --- | --- |
| Tokens per turn | Prompt and verbosity discipline | [00](../../modules/00-agentic-foundations/), [03](../../modules/03-bedrock-agents/) |
| Turns per task | Topology choice — every handoff re-sends context | [07](../../modules/07-strands-multi-agent-patterns/) |
| Retrieval volume | Chunk size, top-k, reranking depth | [10](../../modules/10-rag-opensearch-litellm/) |
| Runtime and storage | Retention policy, capacity planning | [11](../../modules/11-bedrock-agentcore/) |

Workbooks: [Token cost calculator](../../modules/00-agentic-foundations/activities/H2-03_Token-Cost_Calculator.xlsx) ·
[Bedrock cost estimator](../../modules/06-strands-foundations/activities/Bedrock_Cost_Estimator.xlsx) ·
[AgentCore cost and capacity](../../modules/11-bedrock-agentcore/activities/AgentCore_Cost_and_Capacity_Workbench.xlsx)

---

**Zoom in:** [Low-level design per module](lld/) &nbsp;·&nbsp;
**Zoom out:** [Learning paths](../learning-paths/) &nbsp;·&nbsp; [Concepts](../concepts/)
