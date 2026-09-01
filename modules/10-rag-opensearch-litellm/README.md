# 📚 Module 10 · RAG, OpenSearch and LiteLLM

> Retrieval done properly — chunking, hybrid search, reranking, and an evaluation gate.

**Estimated time:** 8–10 hours &nbsp;·&nbsp; **Prerequisites:** Module 02. Module 06 or 08 for the agentic RAG labs.

The largest module, and the one with the most production value. Naive RAG is easy and usually bad. This module walks the whole pipeline — corpus, chunking, lexical and dense retrieval, fusion, reranking, context packing, evaluation — with a reusable `ragkit` library you can lift into your own work.

---

## What you will be able to do

- Build RAG by hand before using any managed service
- Choose a chunking strategy from document structure rather than habit
- Combine lexical and dense retrieval with reciprocal rank fusion
- Add reranking and measure whether it actually helped
- Gate a RAG release on evaluation metrics, not impressions
- Route across model providers with LiteLLM and fail over cleanly

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Chunking | Amazon OpenSearch Serverless |
| Embeddings | Bedrock Knowledge Bases |
| Lexical vs dense retrieval | Bedrock embeddings |
| Hybrid search and RRF | Bedrock Runtime |
| Reranking |  |
| Context packing |  |
| RAG evaluation |  |
| Model routing |  |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/02_RAG_slides.md`](slides/02_RAG_slides.md) | RAG fundamentals |
| 2 | 📖 | [`src/rag_by_hand.py`](src/rag_by_hand.py) | RAG by hand — no library, no magic |
| 3 | 💻 | [`labs/rag-labs/01_foundations.ipynb`](labs/rag-labs/01_foundations.ipynb) | Lab 1 — foundations |
| 4 | 💻 | [`labs/rag-labs/03_index_design.ipynb`](labs/rag-labs/03_index_design.ipynb) | Lab 3 — index and chunking design |
| 5 | 💻 | [`labs/rag-labs/04_retrieval_reranking.ipynb`](labs/rag-labs/04_retrieval_reranking.ipynb) | Lab 4 — retrieval and reranking |
| 6 | ✏️ | [`exercises/EX3_RAG_interim1.md`](exercises/EX3_RAG_interim1.md) | RAG interim exercise 1 |
| 7 | 💻 | [`labs/rag-labs/05_context_generation.ipynb`](labs/rag-labs/05_context_generation.ipynb) | Lab 5 — context packing and generation |
| 8 | 💻 | [`labs/rag-labs/06_evaluation_gate.ipynb`](labs/rag-labs/06_evaluation_gate.ipynb) | Lab 6 — the evaluation gate |
| 9 | ✏️ | [`exercises/EX5_RAG_final.md`](exercises/EX5_RAG_final.md) | RAG final exercise |
| 10 | 💻 | [`labs/rag-labs/07_tokens_cost.ipynb`](labs/rag-labs/07_tokens_cost.ipynb) | Lab 7 — tokens and cost |
| 11 | 💻 | [`labs/rag-labs/08_agentic_fde_lab.ipynb`](labs/rag-labs/08_agentic_fde_lab.ipynb) | Lab 8 — agentic RAG |
| 12 | 📖 | [`slides/AWS_OpenSearch_Deck_1.pptx`](slides/AWS_OpenSearch_Deck_1.pptx) | OpenSearch, part 1 |
| 13 | 💻 | [`labs/opensearch/opensearch_lab.py`](labs/opensearch/opensearch_lab.py) | OpenSearch lab |
| 14 | 📖 | [`slides/01_LiteLLM_slides.md`](slides/01_LiteLLM_slides.md) | LiteLLM — provider routing |
| 15 | 💻 | [`notebooks/01_LiteLLM_notebook.ipynb`](notebooks/01_LiteLLM_notebook.ipynb) | LiteLLM notebook |
| 16 | ✏️ | [`exercises/EX6_consolidated_takehome.md`](exercises/EX6_consolidated_takehome.md) | Consolidated take-home |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 10 — RAG, OpenSearch and LiteLLM | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Project artefact

`labs/rag-labs/ragkit` is a complete, reusable retrieval library — chunking, fusion, reranking, evaluation, cost. Lift it into your own projects.

## Solutions

Worked solutions live in [`solutions/`](solutions/). Attempt every exercise closed-book first — the solutions are written to be read *after* you have a wrong answer to compare against.

## Common mistakes

- Chunking by character count because it was the default. Structure beats size.
- Reranking added without measurement — it costs latency and may not help your corpus.
- Evaluating RAG on vibes. Build the golden set first.

## Folder map

```
exercises        6 file(s)
guides           2 file(s)
labs            88 file(s)
notebooks        6 file(s)
slides           6 file(s)
solutions        6 file(s)
src              1 file(s)
```

## Field guide for this module

Reference material for the ideas in this module — open these while you work, not before.

**Frameworks**

- [Grounding Triangle](../../cheatsheets/frameworks/grounding-triangle.md) — The three sides most systems confuse
- [Context Budget Ledger](../../cheatsheets/frameworks/context-budget-ledger.md) — Pack to a token budget, not a top-k
- [Evidence Ladder](../../cheatsheets/frameworks/evidence-ladder.md) — Why the golden set must be frozen first

**Quick reference**

- [RAG pipeline](../../cheatsheets/quick-reference/rag-pipeline.md) — Stage by stage, with the failure decoder
- [Model selection](../../cheatsheets/quick-reference/model-selection.md) — Routing and provider portability

**Recipes and procedures**

- [Runbook · stale knowledge base](../../cheatsheets/runbooks/incident-stale-knowledge.md) — Index freshness as a gate check

---

⬅️ [Module 09 · LLM Memory Mechanics](../09-llm-memory/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 11 · Amazon Bedrock AgentCore](../11-bedrock-agentcore/) ➡️
