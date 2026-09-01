"""Evaluation. Every metric is written out so its blind spot is visible.

Retrieval layer:  evidence_recall_at_k, full_chain_recall, ndcg
Context layer:    coverage (every gold span present in the packed context)
Answer layer:     correctness, faithfulness (span support), abstention
Diagnosis:        the three handoff checks, the attribution 2x2, the four-question fault tree
Release:          run-to-run variance, frozen slice, gate
Judge:            Cohen's kappa for judge-versus-human agreement
"""
import math
import re
from dataclasses import dataclass, field
import numpy as np
import pandas as pd
from .chunking import gold_chunk_sets
from .context import pack, count_tokens
from .generate import citations_in


# ---------------------------------------------------------------- retrieval layer
def evidence_recall_at_k(gold_sets: list, ranked_ids: list, k: int) -> float:
    """Fraction of gold spans with at least one carrying chunk in the top k."""
    if not gold_sets:
        return float("nan")
    top = set(ranked_ids[:k])
    return sum(1 for s in gold_sets if s & top) / len(gold_sets)


def full_chain_recall(gold_sets: list, ranked_ids: list, k: int) -> float:
    """1.0 only if every gold span is present in the top k. The multi-hop metric."""
    if not gold_sets:
        return float("nan")
    top = set(ranked_ids[:k])
    return 1.0 if all(s & top for s in gold_sets) else 0.0


def ndcg(gold_sets: list, ranked_ids: list, k: int) -> float:
    """Rank-sensitive: a gold chunk at rank 1 is worth more than the same chunk at rank 8."""
    if not gold_sets:
        return float("nan")
    gold = set().union(*gold_sets)
    dcg = sum(1.0 / math.log2(i + 2) for i, cid in enumerate(ranked_ids[:k]) if cid in gold)
    ideal = sum(1.0 / math.log2(i + 2) for i in range(min(len(gold_sets), k)))
    return dcg / ideal if ideal else 0.0


# ---------------------------------------------------------------- context and answer layer
def coverage(gold_sets: list, packed_ids: list) -> float:
    if not gold_sets:
        return float("nan")
    p = set(packed_ids)
    return sum(1 for s in gold_sets if s & p) / len(gold_sets)


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def correctness(question, answer_text: str) -> float:
    """Null questions: 1.0 for an abstention. Others: token-overlap containment of the gold answer."""
    if question.answer is None:
        return 1.0 if "INSUFFICIENT EVIDENCE" in answer_text else 0.0
    if "INSUFFICIENT EVIDENCE" in answer_text:
        return 0.0
    gold = set(_norm(question.answer)) - {"dollars", "million", "billion", "against", "the", "in", "and"}
    got = set(_norm(answer_text))
    return 1.0 if gold and gold <= got else 0.0


def faithfulness(question, answer_text: str, texts: dict) -> float:
    """Span support: does a cited chunk carry each fact the answer relies on?

    Abstentions are faithful by definition. An answer with no citations is unsupported.
    """
    if "INSUFFICIENT EVIDENCE" in answer_text:
        return 1.0
    cites = citations_in(answer_text)
    if not cites or not question.gold:
        return 0.0
    cited_text = " ".join(" ".join(texts[c].split()) for c in cites if c in texts)
    return sum(1 for _, span in question.gold if " ".join(span.split()) in cited_text) / len(question.gold)


# ---------------------------------------------------------------- diagnosis
def handoffs(question, gold_sets, ranked_ids, packed_ids, answer_text, texts, k_pool=50) -> pd.DataFrame:
    """The three handoffs scored separately."""
    rows = [
        ("1. query to retrieval", "gold evidence in the candidate pool", full_chain_recall(gold_sets, ranked_ids, k_pool)),
        ("2. retrieval to context", "gold evidence survived packing", coverage(gold_sets, packed_ids)),
        ("3. context to answer", "answer correct and supported", min(correctness(question, answer_text), faithfulness(question, answer_text, texts))),
    ]
    df = pd.DataFrame(rows, columns=["handoff", "what it checks", "score"])
    df["verdict"] = np.where(df["score"] >= 1.0, "pass", "FAIL")
    return df


def attribution_cell(evidence_present: bool, answer_correct: bool) -> str:
    if evidence_present and answer_correct:
        return "healthy"
    if evidence_present and not answer_correct:
        return "generation failure"
    if not evidence_present and answer_correct:
        return "correct by chance"
    return "retrieval failure"


def fault_tree(gold_sets, pool_ids, packed_ids, answer_text, question, texts) -> pd.DataFrame:
    """The four-question fault-isolation tree, executed. Stops at the first owning stage."""
    steps = []
    q1 = bool(coverage(gold_sets, packed_ids) >= 1.0)
    steps.append(("Q1 Is every gold span in the packed context?", "yes" if q1 else "no"))
    if not q1:
        q2 = bool(full_chain_recall(gold_sets, pool_ids, len(pool_ids)) >= 1.0)
        steps.append(("Q2 Was every gold chunk in the candidate pool?", "yes" if q2 else "no"))
        owner = "ranking or packing fault: reranker, fusion, k, dedup, truncation" if q2 else "first-stage recall fault: chunking, embedding, hybrid weights, ANN parameters, filters"
        return pd.DataFrame(steps + [("Owning stage", owner)], columns=["question", "answer"])
    q3 = faithfulness(question, answer_text, texts) >= 1.0 and not ("INSUFFICIENT EVIDENCE" in answer_text)
    steps.append(("Q3 Is the answer grounded, cited, and not an abstention?", "yes" if q3 else "no"))
    if not q3:
        return pd.DataFrame(steps + [("Owning stage", "generation fault: grounding instruction, abstention policy, citation contract, model")], columns=["question", "answer"])
    q4 = correctness(question, answer_text) >= 1.0
    steps.append(("Q4 Is the answer entailed by the evidence and matching gold?", "yes" if q4 else "no"))
    owner = "pipeline is correct; suspect the label, the question, or the rubric" if q4 else "generation fault: the model read the right evidence and still concluded wrongly"
    return pd.DataFrame(steps + [("Owning stage", owner)], columns=["question", "answer"])


# ---------------------------------------------------------------- benchmark runner
@dataclass
class RunConfig:
    name: str
    mode: str = "hybrid"          # lexical | dense | hybrid
    n_pool: int = 50
    k: int = 5
    evidence_cap: int = 6000
    order: str = "rank"
    reranker: object = None       # callable(question_text, ranked) -> ranked
    decompose: object = None      # callable(question, retriever) -> ranked (agentic path)
    dedup_jaccard: float = None
    filters: dict = field(default_factory=dict)


def run_benchmark(cfg: RunConfig, retriever, generator, questions, chunks, store=None, seed: int = 0) -> pd.DataFrame:
    """One row per question with every layered metric, the attribution cell, tokens and simulated latency."""
    texts = {c.chunk_id: c.text for c in chunks}
    rows = []
    generator.rng = np.random.default_rng(seed)
    for q in questions:
        gold_sets = gold_chunk_sets(q, chunks)
        boundary_loss = any(len(s) == 0 for s in gold_sets)
        if cfg.decompose is not None:
            pool = cfg.decompose(q, retriever)
        else:
            pool = retriever.search(q.text, k=cfg.n_pool, mode=cfg.mode, **cfg.filters)
        if cfg.reranker is not None:
            pool = cfg.reranker(q.text, pool)
        pool_ids = [c for c, _ in pool]
        packed = pack(pool, texts, cfg.evidence_cap, k=cfg.k, order=cfg.order, dedup_jaccard=cfg.dedup_jaccard)
        ans = generator.answer(q, packed.chunk_ids, texts)
        ev_present = bool(coverage(gold_sets, packed.chunk_ids) >= 1.0) if q.gold else False
        corr = correctness(q, ans.text)
        rows.append({
            "qid": q.qid, "type": q.qtype, "frozen": q.frozen, "boundary_loss": boundary_loss,
            "recall@k": evidence_recall_at_k(gold_sets, pool_ids, cfg.k),
            "full_chain@k": full_chain_recall(gold_sets, pool_ids, cfg.k),
            "recall@pool": full_chain_recall(gold_sets, pool_ids, cfg.n_pool),
            "ndcg@k": ndcg(gold_sets, pool_ids, cfg.k),
            "coverage": coverage(gold_sets, packed.chunk_ids),
            "correct": corr, "faithful": faithfulness(q, ans.text, texts),
            "abstained": ans.abstained,
            "cell": attribution_cell(ev_present, corr >= 1.0) if q.gold else ("healthy" if corr >= 1.0 else "fabrication on null"),
            "evidence_tokens": packed.tokens, "k_packed": len(packed.chunk_ids),
            "answer": ans.text[:80],
        })
        if store is not None:
            store.save_trace(f"{cfg.name}:{q.qid}", q.text, {"config": cfg.name, "pool": pool_ids[:cfg.n_pool], "packed": packed.chunk_ids,
                                                             "dropped": packed.dropped, "answer": ans.text, "citations": ans.citations})
    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame, name: str = None) -> pd.Series:
    """Means over answerable questions for retrieval metrics, all questions for answer metrics."""
    ans = df[df["type"] != "null"]
    s = pd.Series({
        "recall@k": ans["recall@k"].mean(), "full_chain@k": ans["full_chain@k"].mean(), "recall@pool": ans["recall@pool"].mean(),
        "ndcg@k": ans["ndcg@k"].mean(), "coverage": ans["coverage"].mean(),
        "correct": df["correct"].mean(), "faithful": df["faithful"].mean(),
        "null_abstained": df[df["type"] == "null"]["abstained"].mean() if (df["type"] == "null").any() else float("nan"),
        "evidence_tokens": df["evidence_tokens"].mean(),
    })
    if name:
        s.name = name
    return s.round(3)


def variance(cfg, retriever, generator, questions, chunks, seeds=(0, 1, 2, 3, 4), metric: str = "correct") -> dict:
    """Re-run the same config under different generator seeds and report the noise band."""
    vals = [summarize(run_benchmark(cfg, retriever, generator, questions, chunks, seed=s))[metric] for s in seeds]
    return {"mean": float(np.mean(vals)), "std": float(np.std(vals)), "band": float(2 * np.std(vals)), "runs": vals}


def gate(before: pd.Series, after: pd.Series, tolerance: float = 0.02, cost_warn: float = 0.15) -> pd.DataFrame:
    """Compare two summaries. Hard block on a quality drop beyond tolerance; warn on cost."""
    rows = []
    for m in ["full_chain@k", "recall@k", "correct", "faithful", "null_abstained"]:
        d = float(after[m] - before[m])
        verdict = "BLOCK" if d < -tolerance else "ok"
        rows.append((m, round(float(before[m]), 3), round(float(after[m]), 3), round(d, 3), verdict))
    dt = (after["evidence_tokens"] - before["evidence_tokens"]) / max(1.0, before["evidence_tokens"])
    rows.append(("evidence_tokens", round(float(before["evidence_tokens"]), 1), round(float(after["evidence_tokens"]), 1), f"{dt:+.0%}", "WARN" if dt > cost_warn else "ok"))
    return pd.DataFrame(rows, columns=["metric", "before", "after", "delta", "verdict"])


def cohen_kappa(a: list, b: list) -> float:
    """Agreement beyond chance between two binary label lists."""
    a, b = np.asarray(a), np.asarray(b)
    po = float((a == b).mean())
    pe = float(a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean()))
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


# Test inputs and expected outcomes
# evidence_recall_at_k([{"x"},{"y"}], ["x","z","y"], 2)  -> 0.5
# full_chain_recall([{"x"},{"y"}], ["x","z","y"], 3)      -> 1.0
# ndcg([{"x"}], ["x"], 1)                                 -> 1.0
# attribution_cell(False, True)                           -> "correct by chance"
# cohen_kappa([1,1,0,0],[1,1,0,0])                        -> 1.0 ; cohen_kappa([1,1,1,1],[1,1,1,0]) -> 0.0
