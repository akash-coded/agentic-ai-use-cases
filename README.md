<div align="center">

# Agentic AI on AWS

### Build, evaluate and ship production AI agents with Amazon Bedrock, AgentCore, Strands, LangGraph and RAG

**A complete, free, hands-on curriculum — plus a 77-page field guide and auto-graded labs.**
16 modules · 102 notebooks · 92 exercises · 63 worked solutions · 30 decision workbooks · ~90 hours

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Notebooks](https://img.shields.io/badge/notebooks-102-orange.svg)](#the-curriculum)
[![Modules](https://img.shields.io/badge/modules-16-1f5f8b.svg)](#the-curriculum)
[![Solutions](https://img.shields.io/badge/worked%20solutions-63-2e8b57.svg)](#63-worked-solutions--and-honesty-about-the-rest)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Field guide](https://img.shields.io/badge/field%20guide-77%20pages-8b6f2e.svg)](cheatsheets/)
[![L.A.B. Simulator](https://img.shields.io/badge/L.A.B.%20simulator-auto--graded-2e8b57.svg)](labs/)
[![Discussions](https://img.shields.io/badge/discussions-open-8b5cf6.svg)](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions)

**[▶ Start here](docs/START-HERE.md)** &nbsp;·&nbsp;
**[🗺️ Learning paths](docs/learning-paths/)** &nbsp;·&nbsp;
**[🏛️ Architecture](docs/architecture/)** &nbsp;·&nbsp;
**[🧭 Field guide](cheatsheets/)** &nbsp;·&nbsp;
**[🧪 L.A.B. Simulator](labs/)** &nbsp;·&nbsp;
**[⚙️ Setup](docs/setup/aws-account-setup.md)** &nbsp;·&nbsp;
**[💬 Discussions](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions)**

</div>

---

## Why this exists

Most agentic AI material stops at a working demo. A demo is the easy 20%. The hard part is everything
after: proving the thing works, knowing what it costs, deciding whether it should have been an agent at
all, and having something to roll back to when it fails at 2 a.m.

This curriculum was built and delivered across three professional cohorts and rebuilt for public use. It is
opinionated in one specific way:

> **Every abstraction is preceded by the thing it abstracts.**
> You write the agent loop by hand before you meet a framework. You build RAG by hand before you touch a
> managed knowledge base. You write the evaluation gate before you deploy. Nothing is magic, because you
> built the layer underneath it.

## What you will be able to do

- Decide, with a defensible artefact, whether a use case should be an agent at all
- Call Amazon Bedrock properly — Converse API, tool use, multi-turn state, token accounting
- Build agents in **Bedrock Agents**, **Strands** and **LangChain/LangGraph**, and choose between them with evidence
- Design multi-agent topologies and predict their cost before running them
- Build a retrieval pipeline with hybrid search and reranking, and **prove** it works
- Deploy to **Bedrock AgentCore** with memory, identity, a gateway and observability
- Gate a release on evaluation metrics, and roll it back when the gate is right

## Quick start

```bash
git clone https://github.com/akash-coded/aws-bedrock-agentcore-strands.git
cd aws-bedrock-agentcore-strands
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Then open **[`docs/START-HERE.md`](docs/START-HERE.md)**.

> **Before Module 02:** [set up AWS](docs/setup/aws-account-setup.md) and
> [set a budget alarm](docs/setup/cost-controls.md). Model access approval is not always instant.
> Modules 00, 01 and 15 need no AWS account — start there while access is pending.

---

## Choose your path

Sixteen modules is a lot, and nobody needs all of them in the same order.

| Path | For | Time | Finish line |
| --- | --- | --- | --- |
| 🚀 **[Weekend Sprint](docs/learning-paths/weekend-sprint.md)** | "Show me it works, this weekend" | ~12 h | A working Bedrock agent with your own tools |
| 🛠️ **[Agent Engineer](docs/learning-paths/agent-engineer.md)** | Building and shipping agents | ~70 h | A deployed, evaluated, gated agent |
| 🏛️ **[Solutions Architect](docs/learning-paths/solutions-architect.md)** | Designing and reviewing agent systems | ~45 h | A defensible architecture with a cost model |
| 📋 **[Product Manager](docs/learning-paths/product-manager.md)** | Deciding what to build, and defending it | ~25 h | A PRD and a gate review you can chair |
| 🔬 **[RAG Specialist](docs/learning-paths/rag-specialist.md)** | Retrieval quality as the job | ~35 h | A measured, gated RAG pipeline |

---

## How it fits together

```mermaid
flowchart TB
    subgraph T1["🧭 Track 1 · Think — no cloud needed"]
        M00["00 Agentic Foundations"]
        M01["01 LLM and AWS Bridge"]
    end
    subgraph T2["🪨 Track 2 · Invoke — managed AWS"]
        M02["02 Bedrock Essentials"]
        M03["03 Bedrock Agents"]
        M04["04 Agent Builder and KBs"]
    end
    subgraph T3["🧵 Track 3 · Build — frameworks"]
        M05["05 No Framework to Strands"]
        M06["06 Strands Foundations"]
        M07["07 Multi-Agent Patterns"]
        M08["08 LangChain and LangGraph"]
        M09["09 LLM Memory"]
    end
    subgraph T4["📚 Track 4 · Ground — retrieval"]
        M10["10 RAG, OpenSearch, LiteLLM"]
    end
    subgraph T5["🚀 Track 5 · Ship — platform"]
        M11["11 AgentCore"]
        M12["12 A2A and A2UI"]
        M13["13 QA and Evaluation"]
        M14["14 End-to-End Production"]
    end
    M15["📋 15 Agentic Product Lifecycle<br/><i>parallel track for PMs and leads</i>"]

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

**[→ Full architecture, including the TravelMind reference application](docs/architecture/)**

---

## The curriculum

| # | Module | Time | 📓 | ✏️ | 📗 | Design |
| --- | --- | --- | --- | --- | --- | --- |
| **[00](modules/00-agentic-foundations/)** | 🧭 **[Agentic Foundations](modules/00-agentic-foundations/)**<br/><sub>Decide what deserves to be an agent before you build one.</sub> | 4–5 h | 0 | 6 | 2 | [LLD](docs/architecture/lld/00-agentic-foundations.md) |
| **[01](modules/01-llm-and-aws-bridge/)** | 🌉 **[LLM Intuition and the AWS Bridge](modules/01-llm-and-aws-bridge/)**<br/><sub>Build a working mental model of LLMs, then map it onto AWS.</sub> | 3–4 h | 0 | 2 | 0 | [LLD](docs/architecture/lld/01-llm-and-aws-bridge.md) |
| **[02](modules/02-bedrock-essentials/)** | 🪨 **[Amazon Bedrock Essentials](modules/02-bedrock-essentials/)**<br/><sub>Your first real calls: Converse API, tokens, tool use, knowledge bases, guardrails.</sub> | 6–8 h | 5 | 6 | 5 | [LLD](docs/architecture/lld/02-bedrock-essentials.md) |
| **[03](modules/03-bedrock-agents/)** | 🤖 **[Amazon Bedrock Agents](modules/03-bedrock-agents/)**<br/><sub>Console to code: action groups, orchestration, and controlling behaviour.</sub> | 6–7 h | 8 | 7 | 3 | [LLD](docs/architecture/lld/03-bedrock-agents.md) |
| **[04](modules/04-agent-builder-and-knowledge-bases/)** | 🏗️ **[Agent Builder, Knowledge Bases and Guardrails](modules/04-agent-builder-and-knowledge-bases/)**<br/><sub>The low-code surface, and how to wire knowledge and safety into it.</sub> | 4–5 h | 3 | 0 | 0 | [LLD](docs/architecture/lld/04-agent-builder-and-knowledge-bases.md) |
| **[05](modules/05-agent-loop-no-framework-to-strands/)** | 🔁 **[The Agent Loop: No Framework to Strands](modules/05-agent-loop-no-framework-to-strands/)**<br/><sub>Write the loop by hand, feel the pain, then let Strands remove it.</sub> | 5–6 h | 13 | 4 | 4 | [LLD](docs/architecture/lld/05-agent-loop-no-framework-to-strands.md) |
| **[06](modules/06-strands-foundations/)** | 🧵 **[Strands Foundations: Tools, Memory and MCP](modules/06-strands-foundations/)**<br/><sub>Agents with hands, memory, and a standard way to reach the outside world.</sub> | 5–6 h | 5 | 4 | 0 | [LLD](docs/architecture/lld/06-strands-foundations.md) |
| **[07](modules/07-strands-multi-agent-patterns/)** | 🕸️ **[Multi-Agent Patterns with Strands](modules/07-strands-multi-agent-patterns/)**<br/><sub>Swarm, graph, delegation, critique — and when each one is wrong.</sub> | 6–7 h | 8 | 9 | 9 | [LLD](docs/architecture/lld/07-strands-multi-agent-patterns.md) |
| **[08](modules/08-langchain-and-langgraph/)** | 🦜 **[LangChain and LangGraph](modules/08-langchain-and-langgraph/)**<br/><sub>The other ecosystem — and an honest side-by-side with Strands.</sub> | 7–8 h | 16 | 12 | 12 | [LLD](docs/architecture/lld/08-langchain-and-langgraph.md) |
| **[09](modules/09-llm-memory/)** | 🧠 **[LLM Memory Mechanics](modules/09-llm-memory/)**<br/><sub>What models forget, why, and what you can do about it.</sub> | 3–4 h | 2 | 1 | 0 | [LLD](docs/architecture/lld/09-llm-memory.md) |
| **[10](modules/10-rag-opensearch-litellm/)** | 📚 **[RAG, OpenSearch and LiteLLM](modules/10-rag-opensearch-litellm/)**<br/><sub>Retrieval done properly — chunking, hybrid search, reranking, and an evaluation gate.</sub> | 8–10 h | 14 | 6 | 6 | [LLD](docs/architecture/lld/10-rag-opensearch-litellm.md) |
| **[11](modules/11-bedrock-agentcore/)** | ⚙️ **[Amazon Bedrock AgentCore](modules/11-bedrock-agentcore/)**<br/><sub>Runtime, memory, identity, gateway, observability — agents as deployed services.</sub> | 8–10 h | 17 | 4 | 0 | [LLD](docs/architecture/lld/11-bedrock-agentcore.md) |
| **[12](modules/12-a2a-and-a2ui-interop/)** | 🔌 **[A2A and A2UI: Agent Interoperability](modules/12-a2a-and-a2ui-interop/)**<br/><sub>Agents talking to agents, and agents talking to users.</sub> | 4–5 h | 5 | 5 | 2 | [LLD](docs/architecture/lld/12-a2a-and-a2ui-interop.md) |
| **[13](modules/13-agentic-qa-and-evaluation/)** | 🔬 **[Agentic QA and Evaluation](modules/13-agentic-qa-and-evaluation/)**<br/><sub>How you prove an agent works — and block the ones that do not.</sub> | 5–6 h | 2 | 1 | 0 | [LLD](docs/architecture/lld/13-agentic-qa-and-evaluation.md) |
| **[14](modules/14-end-to-end-production/)** | 🚀 **[End-to-End Production Pipeline](modules/14-end-to-end-production/)**<br/><sub>The capstone: build, validate, deploy, fail over, and gate a release.</sub> | 8–10 h | 4 | 9 | 8 | [LLD](docs/architecture/lld/14-end-to-end-production.md) |
| **[15](modules/15-agentic-product-lifecycle/)** | 📋 **[Agentic Product Lifecycle](modules/15-agentic-product-lifecycle/)**<br/><sub>For the people who decide what gets built, and have to defend it.</sub> | 4–5 h | 0 | 16 | 12 | [LLD](docs/architecture/lld/15-agentic-product-lifecycle.md) |
<sub>📓 notebooks · ✏️ exercises · 📗 worked solutions</sub>

---

## How a module works

Every module has the same shape, and its `README.md` tells you the exact order to work through it.

```
modules/NN-topic/
├── README.md      ← objectives, the ordered sequence, common mistakes. Start here.
├── slides/        ← decks and reading material
├── notebooks/     ← runnable code
├── exercises/     ← practice. Attempt closed-book.
├── solutions/     ← worked answers. Read after you have a wrong answer.
├── activities/    ← workbooks where a decision gets written down and costed
├── src/           ← supporting source code
└── labs/          ← extended hands-on
```

```mermaid
flowchart LR
    R["📖 Read<br/>deck"] --> D["💻 Run<br/>notebook"] --> P["✏️ Practise<br/>exercise"]
    P --> S{"Stuck?"}
    S -->|yes| SOL["📗 Compare with<br/>solution"]
    S -->|no| W["📊 Workbook<br/>decide and cost it"]
    SOL --> W --> N["Next module"]
```

### 63 worked solutions — and honesty about the rest

Most exercises ship with a worked solution, written to be read **after** you have a wrong answer to compare
against. That comparison is where the learning is; reading them first turns an hour of work into five
minutes of nodding.

Where there is no answer key, it is deliberate and the module says so:
[Module 06](modules/06-strands-foundations/)'s builds are open-ended designs with levels and
acceptance criteria rather than one right implementation, and
[Module 11](modules/11-bedrock-agentcore/)'s exercises are graded against a self-check rubric.
No module claims a solution set it does not have.

---

## One example, all the way through

**TravelMind** is a travel-operations agent, and it is in almost every module. It starts in Module 02 as a
single Bedrock call and finishes in Module 14 as a deployed, gated, multi-agent service with failover and a
rollback path. Same domain throughout, so you are never learning a new business problem at the same time as
a new technical concept.

```mermaid
flowchart LR
    A["02<br/>One Bedrock call"] --> B["03–04<br/>Managed agent<br/>+ knowledge base"]
    B --> C["06–07<br/>Strands<br/>+ sub-agents"]
    C --> D["10<br/>Retrieval<br/>that is measured"]
    D --> E["11<br/>Deployed on<br/>AgentCore"]
    E --> F["13<br/>Behind a gate<br/>that can say no"]
    F --> G["14<br/>Released, with<br/>a way back"]
    style A fill:#4a5568,color:#fff
    style G fill:#2e8b57,color:#fff
```

The [full request lifecycle and reference architecture](docs/architecture/#3-travelmind--the-reference-application)
is in the architecture docs.

---

## Portable skills vs AWS specifics

A fair question about any cloud-branded curriculum: how much of this transfers?

Most of it. The curriculum is deliberately front-loaded with portable material, and the AWS-specific
surface is concentrated in the platform layer.

| | |
| --- | --- |
| 🟢 **[Portable GenAI concepts](docs/concepts/genai-core-concepts.md)** | Agent loops, tool design, memory strategy, RAG pipeline design, multi-agent topologies, evaluation and gating. Transfers to any stack. |
| 🔵 **[Where AWS comes in](docs/concepts/aws-service-map.md)** | Bedrock, AgentCore, Knowledge Bases, Guardrails, OpenSearch, Lambda, IAM, CloudWatch — service by service, with the module that teaches each. |
| ⚖️ **[Portability matrix](docs/concepts/portability-matrix.md)** | An honest, itemised answer on lock-in, and how to structure a build so the lock-in stays narrow. |

---

## 🗺️ The Field Guide

The curriculum teaches you to build agents. The **[field guide](cheatsheets/)** is what you reach for once
you are building them — in a design review, at 2 a.m. during an incident, in a budget meeting, or in an
interview.

| Section | Contents |
| --- | --- |
| 🧠 **[Frameworks](cheatsheets/frameworks/)** | 17 original mental models — the [Autonomy Ladder](cheatsheets/frameworks/autonomy-ladder.md), [Token Tax Ledger](cheatsheets/frameworks/token-tax-ledger.md), [Handoff Multiplier](cheatsheets/frameworks/handoff-multiplier.md), [Blast Radius Grid](cheatsheets/frameworks/blast-radius-grid.md), [Evidence Ladder](cheatsheets/frameworks/evidence-ladder.md) and more. Each has a procedure and an output, not just a concept |
| 📖 **[Quick reference](cheatsheets/quick-reference/)** | 10 cheat sheets: [Bedrock Converse](cheatsheets/quick-reference/bedrock-converse.md), [Strands](cheatsheets/quick-reference/strands.md), [LangGraph](cheatsheets/quick-reference/langgraph.md), [AgentCore](cheatsheets/quick-reference/agentcore.md), [RAG](cheatsheets/quick-reference/rag-pipeline.md), [IAM](cheatsheets/quick-reference/iam-for-agents.md), [observability](cheatsheets/quick-reference/observability.md) |
| 🚨 **[Runbooks](cheatsheets/runbooks/)** | 9 procedures for when it breaks — [wrong answers](cheatsheets/runbooks/incident-wrong-answers.md), [cost spikes](cheatsheets/runbooks/incident-cost-spike.md), [runaway loops](cheatsheets/runbooks/incident-runaway-loop.md), [rollback](cheatsheets/runbooks/rollback.md), [inheriting an agent](cheatsheets/runbooks/inheriting-an-agent.md) |
| 📋 **[Playbooks](cheatsheets/playbooks/)** | [Design reviews](cheatsheets/playbooks/agent-design-review.md), [build-buy-or-wait](cheatsheets/playbooks/build-buy-or-wait.md), [scoping an engagement](cheatsheets/playbooks/scoping-an-engagement.md), [killing a project well](cheatsheets/playbooks/killing-an-agent-project.md) |
| 💼 **[Interview guides](cheatsheets/interviews/)** | Both sides of the table for [engineer](cheatsheets/interviews/agent-engineer.md), [architect](cheatsheets/interviews/solutions-architect.md), [PM](cheatsheets/interviews/product-manager.md), [BA](cheatsheets/interviews/business-analyst.md), [QA](cheatsheets/interviews/qa-engineer.md) — plus a [hiring guide](cheatsheets/interviews/as-the-interviewer.md) |
| 🎓 **[How-to by role](cheatsheets/how-to/)** | 17 recipes for [engineers](cheatsheets/how-to/engineers/), [PMs](cheatsheets/how-to/product/), [architects](cheatsheets/how-to/architects/), [business analysts](cheatsheets/how-to/business-analysts/), [QA](cheatsheets/how-to/qa-and-test/) and [engineering managers](cheatsheets/how-to/engineering-managers/) |

**Not only for engineers.** Product managers get [acceptance criteria for non-deterministic systems](cheatsheets/how-to/product/write-acceptance-criteria.md)
and [how to price a feature](cheatsheets/how-to/product/price-an-agent-feature.md). Business analysts get
[how to build a golden set from real tickets](cheatsheets/how-to/business-analysts/build-a-golden-set.md) —
the artefact that *is* the specification. Architects get [topology selection with cost multipliers](cheatsheets/how-to/architects/choose-a-topology.md).

**[→ Open the field guide](cheatsheets/)**

---

## 🧪 The L.A.B. Simulator

**Learn → Apply → Break.** Auto-graded, bite-sized labs where you build the pieces yourself and then try
to break them. No API keys, no dependencies — every lab runs offline on Python 3.11+.

```bash
python labs/runner/labctl.py next          # what you can start right now
python labs/runner/labctl.py start PDL-01
python labs/runner/labctl.py run   PDL-01  # public checks
python labs/runner/labctl.py break PDL-01  # now survive the failures that end real runs
```

Most practice platforms give you a stub and a happy-path test. Agents do not fail on the happy path — they
fail when a tool returns `[]` and the model reads it as "nothing applies". So every lab has three phases:

| | Phase | What you get |
| --- | --- | --- |
| **L** | Learn | A mental model, a diagram, and **one decision with the answer withheld**. Your choice changes what you build |
| **A** | Apply | A spec, public checks you can see, hidden checks on submit. Every check explains what it teaches when it fails |
| **B** | Break | `SystemExit` from a library. A chunk bigger than the whole budget. A footnote `[1]` corrupting your citation map. Survive them |

**[10 labs across 8 tracks](labs/)**, ordered by a [justified pathway](labs/PATHWAY.md) — and the decision
inside each one accumulates into the [seven PRD artefacts](docs/prd/), so you finish with a working system
*and* the paperwork to defend it.

The catalog is **self-verifying**: CI proves every reference solution passes all three phases and every
starter fails, so no lab can ship with TODOs that do not need doing. Fork the repo, commit your solutions,
and [the workflow grades your pull request](.github/workflows/labs.yml).

**[→ Open the L.A.B. Simulator](labs/)**

---

## Design documents

Because "how do I design one of these" is the question the demos never answer.

| Document | What it gives you |
| --- | --- |
| **[Architecture HLD](docs/architecture/)** | The whole system: curriculum structure, TravelMind reference architecture, request lifecycle, cost model |
| **[LLD per module](docs/architecture/lld/)** | 16 zoom-ins: the mechanism, its components, contracts, failure modes and how you detect each |
| **[Sample PRDs](docs/prd/)** | Seven artefacts across the lifecycle — idea brief, discovery PRD, agent spec, technical design, evaluation plan, production readiness, post-launch review. Worked for TravelMind, usable as templates. |
| **[Glossary](docs/concepts/glossary.md)** | Terms as used here, including where the industry definition is contested |
| **[Training frameworks playbook](docs/reference/training-frameworks-playbook.md)** | The instructional design behind the structure, if you want to teach from this |

---

## Repository map

```
.
├── modules/          16 topic modules — the curriculum
├── labs/             the L.A.B. Simulator — auto-graded, decision-driven labs
│   ├── catalog/              labs, by track
│   ├── runner/               labctl — list · start · run · break · submit · verify
│   ├── workspace/            your solutions (graded in CI on a PR)
│   └── PATHWAY.md            the justified 41-lab progression
├── cheatsheets/      the field guide — 77 reference pages
│   ├── frameworks/           17 original mental models
│   ├── quick-reference/      10 API and decision cheat sheets
│   ├── runbooks/             9 incident and operational procedures
│   ├── playbooks/            4 strategic playbooks
│   ├── interviews/           6 role guides, both sides of the table
│   └── how-to/               17 recipes across 6 roles
├── docs/
│   ├── START-HERE.md         entry point
│   ├── learning-paths/       5 paths by role and time budget
│   ├── architecture/         HLD + 16 LLDs
│   ├── concepts/             portable concepts · AWS map · portability · glossary
│   ├── prd/                  7 sample PRDs across the lifecycle
│   ├── setup/                AWS setup · local env · cost controls · troubleshooting
│   └── reference/            video index · FAQ · training playbook
└── projects/         standalone build projects
```

---

## Prerequisites

**You need:** enough Python to read and modify a function, and an AWS account you are allowed to spend on.

**You do not need:** machine learning background, maths, or prior LLM experience. Module 01 builds the
model intuition from zero.

**Cost:** tens of dollars if you tear down as you go; considerably more if you leave OpenSearch Serverless
collections and AgentCore runtimes running. Read **[cost controls](docs/setup/cost-controls.md)** first —
it has a teardown checklist per module.

---

## Contributing

Corrections, better explanations, new exercises and updates for changed AWS behaviour are all welcome.

- 🐛 **Something wrong or out of date?** [Open an issue](https://github.com/akash-coded/aws-bedrock-agentcore-strands/issues/new/choose)
- 💬 **Question, or want to show what you built?** [Discussions](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions)
  — 60+ threads, all tagged by track and level. Start with the
  [index of every exercise and lab](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/64),
  the [answered Q&A](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/q-a),
  or [where to post what](docs/DISCUSSIONS.md)
- 🤝 **Want to contribute?** [`CONTRIBUTING.md`](CONTRIBUTING.md)
- 🗺️ **What's next?** The [extension roadmap](docs/extension-roadmap.md) and its
  [public board](https://github.com/users/akash-coded/projects/6) — five phases, most items open to contributors
- 📜 **What changed?** [`CHANGELOG.md`](CHANGELOG.md)

AWS moves quickly. If something here no longer matches reality, that is a bug worth reporting.

---

## Frequently asked

**Do I need an AWS account?** For most of it. Modules 00, 01 and 15 need nothing.
**Strands or LangChain?** Both are here, compared head-to-head on the same task in [Module 08](modules/08-langchain-and-langgraph/).
**Are there videos?** Not yet — the written material is self-contained. [Progress is tracked here](docs/reference/video-index.md).
**Can I teach from this?** Yes, MIT licensed. See [`CITATION.cff`](CITATION.cff).

**[→ Full FAQ](docs/reference/faq.md)**

---

## Licence and credits

MIT — see [`LICENSE`](LICENSE). Built by [Akash Das](https://github.com/akash-coded) from material
developed and delivered across three professional training cohorts.

If this was useful, a ⭐ helps other people find it.

<div align="center">
<sub>

**Topics:** agentic-ai · amazon-bedrock · bedrock-agentcore · strands-agents · langchain · langgraph ·
rag · multi-agent-systems · llm · aws · generative-ai · ai-agents · opensearch · litellm · mcp ·
agent-evaluation · llmops

</sub>
</div>
