"""Fusion of ranked lists, deduplication, and the Retriever that wraps every mode.

Reciprocal rank fusion (Cormack, Clarke and Buettcher, 2009) is established: each list
contributes 1 / (k + rank), so an item ranked well by several lists rises to the top
without any score calibration between them.
"""
import numpy as np
from .lexical import BM25Index, tokenize
from .dense import FlatIndex


def rrf(lists: list, k: int = 60) -> list:
    """lists: list of ranked [(id, score)] lists. Returns [(id, fused_score)] descending."""
    acc = {}
    for ranked in lists:
        for rank, (cid, _) in enumerate(ranked, start=1):
            acc[cid] = acc.get(cid, 0.0) + 1.0 / (k + rank)
    return sorted(acc.items(), key=lambda x: -x[1])


def weighted(lists: list, weights: list) -> list:
    """Z-score each list, then take a weighted sum. Needs score calibration, unlike RRF."""
    acc = {}
    for ranked, w in zip(lists, weights):
        if not ranked:
            continue
        s = np.array([x[1] for x in ranked], dtype=float)
        z = (s - s.mean()) / (s.std() + 1e-9)
        for (cid, _), zs in zip(ranked, z):
            acc[cid] = acc.get(cid, 0.0) + w * float(zs)
    return sorted(acc.items(), key=lambda x: -x[1])


def dedup(ranked: list, texts: dict, jaccard: float = 0.8) -> list:
    """Drop near-duplicate chunks, keeping the higher-ranked one."""
    kept, kept_tok = [], []
    for cid, s in ranked:
        toks = set(tokenize(texts[cid]))
        if any(len(toks & kt) / max(1, len(toks | kt)) >= jaccard for kt in kept_tok):
            continue
        kept.append((cid, s))
        kept_tok.append(toks)
    return kept


class Retriever:
    """All three retrieval modes over one chunk set, with metadata and ACL filtering.

    Filters are applied as a pre-filter (the candidate set is scoped before ranking) or,
    for the demonstration of why it is wrong, as a post-filter after global top-k.
    """

    def __init__(self, store, chunks: list, embedder, name: str = "retriever"):
        self.store = store
        self.chunks = {c.chunk_id: c for c in chunks}
        self.docs = {d.doc_id: d for d in store.docs()}
        self.embedder = embedder
        self.bm25 = BM25Index(chunks)
        ids = [c.chunk_id for c in chunks]
        self.flat = FlatIndex(ids, embedder.embed([c.text for c in chunks]))
        self.name = name

    # ---- filters ----
    def _allowed(self, cid: str, user_groups=None, date_from: str = None, date_to: str = None, tenant: str = None) -> bool:
        d = self.docs[self.chunks[cid].doc_id]
        if user_groups is not None and not (set(d.acl) & set(user_groups)) and "everyone" not in d.acl:
            return False
        if tenant is not None and d.tenant != tenant:
            return False
        if date_from and d.date < date_from:
            return False
        if date_to and d.date > date_to:
            return False
        return True

    def _filtered(self, ranked: list, k: int, **f) -> list:
        return [(cid, s) for cid, s in ranked if self._allowed(cid, **f)][:k]

    # ---- modes ----
    def lexical(self, query: str, k: int = 10, **f) -> list:
        return self._filtered(self.bm25.search(query, k=len(self.chunks)), k, **f)

    def dense(self, query: str, k: int = 10, **f) -> list:
        return self._filtered(self.flat.search(self.embedder.embed_one(query), k=len(self.chunks)), k, **f)

    def hybrid(self, query: str, k: int = 10, rrf_k: int = 60, n_each: int = 50, **f) -> list:
        lex = self.lexical(query, k=n_each, **f)
        den = self.dense(query, k=n_each, **f)
        return rrf([lex, den], k=rrf_k)[:k]

    def post_filtered(self, query: str, k: int = 10, mode: str = "hybrid", **f) -> list:
        """The wrong way: global top-k first, then drop what the user may not see."""
        fn = {"lexical": self.lexical, "dense": self.dense, "hybrid": self.hybrid}[mode]
        top = fn(query, k=k)                      # no filters here
        return [(cid, s) for cid, s in top if self._allowed(cid, **f)]

    def search(self, query: str, k: int = 10, mode: str = "hybrid", **f) -> list:
        return {"lexical": self.lexical, "dense": self.dense, "hybrid": self.hybrid}[mode](query, k=k, **f)

    def text(self, cid: str) -> str:
        return self.chunks[cid].text

    def show(self, ranked: list, n_chars: int = 90):
        """A DataFrame view of a ranked list."""
        import pandas as pd
        rows = []
        for rank, (cid, s) in enumerate(ranked, start=1):
            c = self.chunks[cid]
            d = self.docs[c.doc_id]
            rows.append({"rank": rank, "chunk_id": cid, "doc": c.doc_id, "date": d.date, "score": round(s, 4),
                         "text": c.text[:n_chars] + ("..." if len(c.text) > n_chars else "")})
        return pd.DataFrame(rows)


# Test inputs and expected outcomes
# rrf([[("a",1),("b",0.5)],[("b",9),("c",8)]])[0][0]   -> "b" (ranked by both lists)
# dedup([("x",1),("y",0.9)], {"x":"same text here","y":"same text here"})  -> keeps only "x"
# Retriever(store, chunks, emb).lexical("Nord Aerospace", 3)[0][0].split(":")[0] in ("a1","g1","g2")  -> True
