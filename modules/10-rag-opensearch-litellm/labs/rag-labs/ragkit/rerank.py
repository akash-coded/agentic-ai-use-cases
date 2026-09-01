"""Rerankers. Each one is a callable (query, ranked) -> ranked, so RunConfig.reranker can take any of them.

MaxSimReranker      Late interaction (the ColBERT idea): every query token keeps its own vector,
                    and the score is the sum over query tokens of the best match among passage tokens.
                    Real, established, and runnable offline because the LSA embedder yields term vectors.
LLMReranker         Asks a language model to score each passage for the query. Real when a provider is
                    configured; falls back to MaxSimReranker offline.
"""
import re
import numpy as np
from .lexical import tokenize


class MaxSimReranker:
    name = "maxsim"

    def __init__(self, embedder, min_query_tokens: int = 1):
        self.emb = embedder
        self.tv = embedder.term_vectors()

    def _tokens(self, text: str):
        toks = [t for t in self.emb.vec.build_analyzer()(text) if t in self.tv]
        return toks, (np.stack([self.tv[t] for t in toks]) if toks else np.zeros((0, len(next(iter(self.tv.values()))))))

    def matrix(self, query: str, passage: str):
        """Token-by-token cosine matrix (query rows, passage columns) and the token lists."""
        qt, Q = self._tokens(query)
        pt, P = self._tokens(passage)
        if len(qt) == 0 or len(pt) == 0:
            return qt, pt, np.zeros((len(qt), len(pt)))
        return qt, pt, Q @ P.T

    def score(self, query: str, passage: str) -> float:
        qt, pt, M = self.matrix(query, passage)
        if M.size == 0:
            return 0.0
        return float(M.max(axis=1).sum() / len(qt))

    def __call__(self, query: str, ranked: list, texts: dict = None, top: int = None) -> list:
        texts = texts or self.texts
        pool = ranked[:top] if top else ranked
        rescored = [(cid, self.score(query, texts[cid])) for cid, _ in pool]
        return sorted(rescored, key=lambda x: -x[1]) + ranked[len(pool):]

    def bind(self, texts: dict):
        self.texts = texts
        return self


class LLMReranker:
    name = "llm"
    PROMPT = ("Rate how well the passage answers or supports the question. Reply with a single integer from 0 (irrelevant) "
              "to 10 (directly answers it).\n\nQuestion: {q}\n\nPassage: {p}\n\nScore:")

    def __init__(self, llm, fallback=None):
        self.llm = llm
        self.fallback = fallback

    def score(self, query: str, passage: str) -> float:
        if self.llm is None or getattr(self.llm, "name", "") == "mock":
            return self.fallback.score(query, passage) if self.fallback else 0.0
        out = self.llm.generate(self.PROMPT.format(q=query, p=passage), max_tokens=4)
        m = re.search(r"\d+", out)
        return float(m.group()) if m else 0.0

    def __call__(self, query: str, ranked: list, texts: dict = None, top: int = None) -> list:
        texts = texts or self.texts
        pool = ranked[:top] if top else ranked
        rescored = [(cid, self.score(query, texts[cid])) for cid, _ in pool]
        return sorted(rescored, key=lambda x: -x[1]) + ranked[len(pool):]

    def bind(self, texts: dict):
        self.texts = texts
        if self.fallback is not None:
            self.fallback.bind(texts)
        return self


def make_reranker(kind: str, retriever, texts: dict, top: int = 50):
    """A callable(query, ranked) -> ranked for RunConfig.reranker."""
    if kind == "maxsim":
        rr = MaxSimReranker(retriever.embedder).bind(texts)
    elif kind == "llm":
        from .providers import get_llm
        rr = LLMReranker(get_llm(), fallback=MaxSimReranker(retriever.embedder)).bind(texts)
    elif kind == "bedrock":
        from .providers import BedrockReranker
        rr = BedrockReranker().bind(texts)
    else:
        raise ValueError(kind)
    return lambda query, ranked: rr(query, ranked, top=top)


# Test inputs and expected outcomes
# rr = MaxSimReranker(retriever.embedder).bind(texts)
# rr.score("Nord Aerospace chief executive", texts[a1_chunk]) > rr.score("Nord Aerospace chief executive", texts[k1_chunk])  -> True
# qt, pt, M = rr.matrix("Nord Aerospace", "Nord Aerospace names Elena Ruiz"); M.shape == (len(qt), len(pt))          -> True
# make_reranker("maxsim", retriever, texts)("Nord Aerospace", retriever.hybrid("Nord Aerospace", 10))[0][0].split(":")[0] in ("a1","g1","g2")  -> True
