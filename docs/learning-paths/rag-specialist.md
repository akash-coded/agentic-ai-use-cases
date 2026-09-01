# 🔬 RAG Specialist

**For:** retrieval quality is your actual job. **Time:** ~35 hours. **Finish line:** a hybrid retrieval
pipeline with reranking you have *measured*, behind a gate that blocks regressions.

Most RAG advice is folklore. This path is built around measurement: you will not keep a component you
cannot show helped.

## 1 · Foundation — 5 h

- [Module 02](../../modules/02-bedrock-essentials/) — Converse API and knowledge bases. You need to know
  what the managed option gives you before you decide to beat it.
- [`knowledge_base_query.py`](../../modules/02-bedrock-essentials/src/knowledge_base_query.py)

## 2 · Build it by hand — 4 h

- [`rag_by_hand.py`](../../modules/10-rag-opensearch-litellm/src/rag_by_hand.py) — no library, no magic
- [RAG fundamentals deck](../../modules/10-rag-opensearch-litellm/slides/02_RAG_slides.md)
- [Lab 01 · foundations](../../modules/10-rag-opensearch-litellm/labs/rag-labs/01_foundations.ipynb)

## 3 · The pipeline, stage by stage — 14 h

| Lab | What it settles |
| --- | --- |
| [02 · multihop benchmark](../../modules/10-rag-opensearch-litellm/labs/rag-labs/02_multihop_benchmark.ipynb) | Where single-hop retrieval structurally fails |
| [03 · index design](../../modules/10-rag-opensearch-litellm/labs/rag-labs/03_index_design.ipynb) | Chunking as a structural decision, not a size |
| [04 · retrieval and reranking](../../modules/10-rag-opensearch-litellm/labs/rag-labs/04_retrieval_reranking.ipynb) | Hybrid + RRF, and whether reranking earned its latency |
| [05 · context generation](../../modules/10-rag-opensearch-litellm/labs/rag-labs/05_context_generation.ipynb) | Packing under a token budget |
| [06 · evaluation gate](../../modules/10-rag-opensearch-litellm/labs/rag-labs/06_evaluation_gate.ipynb) | The bar that blocks a bad index |
| [07 · tokens and cost](../../modules/10-rag-opensearch-litellm/labs/rag-labs/07_tokens_cost.ipynb) | What retrieval depth actually costs |
| [08 · agentic RAG](../../modules/10-rag-opensearch-litellm/labs/rag-labs/08_agentic_fde_lab.ipynb) | When the retriever should be an agent |

The [`ragkit`](../../modules/10-rag-opensearch-litellm/labs/rag-labs/ragkit/) library underneath these labs
is reusable — lift it into your own work.

## 4 · At scale on AWS — 6 h

- [OpenSearch decks](../../modules/10-rag-opensearch-litellm/slides/AWS_OpenSearch_Deck_1.pptx)
- [OpenSearch lab](../../modules/10-rag-opensearch-litellm/labs/opensearch/opensearch_lab.py)
- [LiteLLM](../../modules/10-rag-opensearch-litellm/notebooks/01_LiteLLM_notebook.ipynb) — provider routing
  and failover for embedding and generation

## 5 · Prove it — 6 h

- [Module 13](../../modules/13-agentic-qa-and-evaluation/) — golden sets, the harness, and
  [`quality_gate.py`](../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py)
- Exercises [EX3](../../modules/10-rag-opensearch-litellm/exercises/EX3_RAG_interim1.md),
  [EX5](../../modules/10-rag-opensearch-litellm/exercises/EX5_RAG_final.md),
  [EX6](../../modules/10-rag-opensearch-litellm/exercises/EX6_consolidated_takehome.md)

## Finish line

A pipeline where you can state, with numbers: your chunking strategy and why, your fusion weights, whether
reranking helped and by how much, your cost per query, and the threshold at which you would block a release.
