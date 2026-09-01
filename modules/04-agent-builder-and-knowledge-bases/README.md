# 🏗️ Module 04 · Agent Builder, Knowledge Bases and Guardrails

> The low-code surface, and how to wire knowledge and safety into it.

**Estimated time:** 4–5 hours &nbsp;·&nbsp; **Prerequisites:** Module 03.

Agent Builder is the fastest path from idea to working agent. This module shows what it gives you for free, where its ceiling is, and how knowledge bases and guardrails attach to a real agent.

---

## What you will be able to do

- Build an agent in Agent Builder and understand what it generates
- Attach a knowledge base and verify grounding actually happened
- Configure guardrails and test them against adversarial input
- Know when to graduate from Agent Builder to code

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Low-code agent composition | Bedrock Agent Builder |
| Retrieval grounding | Bedrock Knowledge Bases |
| Safety policy design | Bedrock Guardrails |
|  | Lambda action groups |
|  | S3 data sources |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/agent_builder_deck.md`](slides/agent_builder_deck.md) | Agent Builder deck |
| 2 | 💻 | [`notebooks/agent_builder_notebook.ipynb`](notebooks/agent_builder_notebook.ipynb) | Agent Builder walkthrough |
| 3 | 📖 | [`slides/kb_guardrails_deck.md`](slides/kb_guardrails_deck.md) | Knowledge bases and guardrails |
| 4 | 💻 | [`notebooks/kb_guardrails_agentbuilder_notebook.ipynb`](notebooks/kb_guardrails_agentbuilder_notebook.ipynb) | KB + guardrails in Agent Builder |
| 5 | 💻 | [`notebooks/kb_guardrails_travelmind_notebook.ipynb`](notebooks/kb_guardrails_travelmind_notebook.ipynb) | TravelMind with KB and guardrails |
| 6 | 🔖 | [`guides/TravelMind_ActionGroups_Lambda_RoC_Runbook.md`](guides/TravelMind_ActionGroups_Lambda_RoC_Runbook.md) | Action groups + Lambda runbook |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 04 — Agent Builder, Knowledge Bases and Guardrails | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Solutions

This module has **no separate exercises or solutions**. It is a guided build: the three notebooks are
the practice, and each is worked end to end with the decisions explained as they are made.

For graded practice on the same material, use
[Module 03's exercises](../03-bedrock-agents/exercises/) (agent behaviour and action groups) and
[Module 10's RAG exercises](../10-rag-opensearch-litellm/exercises/) (retrieval quality), both of
which have worked solutions.

## Common mistakes

- Assuming a knowledge base is grounded because it returned text. Check the citations.
- Guardrails configured but never adversarially tested.

## Folder map

```
guides           1 file(s)
notebooks        3 file(s)
slides           3 file(s)
```

## Field guide for this module

Reference material for the ideas in this module — open these while you work, not before.

**Frameworks**

- [Grounding Triangle](../../cheatsheets/frameworks/grounding-triangle.md) — Is it retrieved, cited, or actually verified?
- [Blast Radius Grid](../../cheatsheets/frameworks/blast-radius-grid.md) — Score every tool before you wire it

**Quick reference**

- [RAG pipeline](../../cheatsheets/quick-reference/rag-pipeline.md) — Every stage, and the failure each causes
- [IAM for agents](../../cheatsheets/quick-reference/iam-for-agents.md) — KB service roles and the three-role split

**Recipes and procedures**

- [Runbook · stale knowledge base](../../cheatsheets/runbooks/incident-stale-knowledge.md) — The silent failure of a KB nobody re-syncs

---

⬅️ [Module 03 · Amazon Bedrock Agents](../03-bedrock-agents/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 05 · The Agent Loop: No Framework to Strands](../05-agent-loop-no-framework-to-strands/) ➡️
