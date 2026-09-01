"""ragkit: the in-memory retrieval, RAG and evaluation toolkit used by the FDE Academy notebooks.

Offline by default. Everything runs on numpy, pandas, matplotlib, scikit-learn and sqlite3.
"""
__version__ = "0.1.0"
from . import palette
from .store import Store, Doc, Chunk, content_hash
from .corpus import DOCS, QUESTIONS, ANCHOR, PLANS, Question, load, check_spans
from .chunking import CHUNKERS, chunk_corpus, fixed_words, sentence_window, structural, whole_doc, sentences, resolve_gold, gold_chunk_sets
from .lexical import BM25Index, tokenize, grep
from .dense import Embedder, LSAEmbedder, FlatIndex, IVFIndex, cosine
from .fusion import rrf, weighted, dedup, Retriever
from .context import count_tokens, TOKENIZER, Budget, Packed, pack, order_ends_first, skeleton, SYSTEM_CONTRACT
from .generate import MockGenerator, Answer, citations_in
from .evals import (evidence_recall_at_k, full_chain_recall, ndcg, coverage, correctness, faithfulness, handoffs,
                    attribution_cell, fault_tree, RunConfig, run_benchmark, summarize, variance, gate, cohen_kappa)
from .providers import configure, config, get_embedder, get_llm, get_kb, BedrockKB, BedrockLLM, BedrockEmbedder, BedrockReranker
from .rerank import MaxSimReranker, LLMReranker, make_reranker
from .latency import ILLUSTRATIVE_P95, Timer
from .cost import Rates, PROVIDER_MULTIPLIERS, Request, Bill, CacheSimulator, breakeven_reads, cumulative_cost_curve, query_cost
from .agent import AgentConfig, Trace, entities, carry_bridge, select_tool, sufficiency_check, run_agent, trace_metrics, decompose_pool
from .viz import table, verdict_style, bars, lines, decision, show_trace


def bootstrap(chunker: str = "structural", version: str = "v1", n_components: int = 48):
    """One call that builds the whole offline system: store, chunks, embedder, retriever, generator, questions."""
    store = Store()
    questions = load(store)
    chunks = chunk_corpus(store.docs(), chunker, version)
    store.add_chunks(chunks, version, chunker=chunker, embedder="lsa")
    store.set_live(version)
    embedder = get_embedder([c.text for c in chunks]) if config()["provider"] != "mock" else LSAEmbedder(n_components).fit([c.text for c in chunks])
    retriever = Retriever(store, chunks, embedder, name=f"{chunker}:{version}")
    generator = get_llm()
    return store, chunks, embedder, retriever, generator, questions
