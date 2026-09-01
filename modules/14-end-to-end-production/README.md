# 🚀 Module 14 · End-to-End Production Pipeline

> The capstone: build, validate, deploy, fail over, and gate a release.

**Estimated time:** 8–10 hours &nbsp;·&nbsp; **Prerequisites:** Modules 11 and 13.

Everything converges here. You take TravelMind from source to a gated release — containerised, deployed, routed through a gateway, with model failover, a version manifest and a release pipeline that can say no.

---

## What you will be able to do

- Package an agent for deployment with a reproducible build
- Route requests through a gateway with model failover
- Run a release pipeline with a readiness checklist and version manifest
- Diagnose and recover from a gate failure
- Present the whole architecture to a stakeholder

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Release gating | AgentCore Runtime |
| Failover strategy | AgentCore Gateway |
| Versioning agents | IAM policies |
| Production readiness | CloudWatch |
|  | Container builds |
|  | Bedrock cross-region |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/EndToEnd_Production.pptx`](slides/EndToEnd_Production.pptx) | End-to-end production |
| 2 | 📖 | [`assets/reference_architecture.png`](assets/reference_architecture.png) | The reference architecture |
| 3 | 💻 | [`notebooks/TravelMind_Build_with_Decisions.ipynb`](notebooks/TravelMind_Build_with_Decisions.ipynb) | Build, with the decisions made explicit |
| 4 | 📖 | [`src/travelmind_agent.py`](src/travelmind_agent.py) | The agent source |
| 5 | 📖 | [`src/model_failover.py`](src/model_failover.py) | Model failover |
| 6 | 💻 | [`notebooks/gateway_routing.ipynb`](notebooks/gateway_routing.ipynb) | Gateway routing |
| 7 | 💻 | [`notebooks/TravelMind_Validate_with_Decisions.ipynb`](notebooks/TravelMind_Validate_with_Decisions.ipynb) | Validate |
| 8 | 💻 | [`notebooks/deploy_e2e.ipynb`](notebooks/deploy_e2e.ipynb) | Deploy end to end |
| 9 | 📊 | [`src/readiness_checklist.md`](src/readiness_checklist.md) | Readiness checklist |
| 10 | 📖 | [`src/release_pipeline.md`](src/release_pipeline.md) | Release pipeline |
| 11 | ✏️ | [`exercises/Exercise_6_Production_and_Gate_Failures.md`](exercises/Exercise_6_Production_and_Gate_Failures.md) | Production and gate failures |
| 12 | ✏️ | [`exercises/Capstone_RailReserve.md`](exercises/Capstone_RailReserve.md) | Capstone — RailReserve |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 14 — End-to-End Production Pipeline | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Solutions

Worked solutions live in [`solutions/`](solutions/). Attempt every exercise closed-book first — the solutions are written to be read *after* you have a wrong answer to compare against.

## Common mistakes

- A deploy with no rollback path. Version the manifest, not just the image.
- Failover that silently degrades quality. Log which model actually answered.

## Folder map

```
assets           1 file(s)
exercises        9 file(s)
notebooks        4 file(s)
slides           3 file(s)
solutions        8 file(s)
src             12 file(s)
tools            1 file(s)
```

---

⬅️ [Module 13 · Agentic QA and Evaluation](../13-agentic-qa-and-evaluation/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 15 · Agentic Product Lifecycle](../15-agentic-product-lifecycle/) ➡️
