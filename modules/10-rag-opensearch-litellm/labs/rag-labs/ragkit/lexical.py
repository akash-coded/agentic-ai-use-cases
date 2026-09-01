"""Lexical retrieval: an inverted index scored by BM25, and grep.

BM25 is implemented in the open so every term's contribution can be printed.
The formula is the established Okapi BM25 (Robertson and colleagues), with k1 for
term-frequency saturation and b for document-length normalisation.
"""
import math
import re
from collections import Counter, defaultdict

_TOKEN = re.compile(r"[a-z0-9][a-z0-9\-']*")
STOP = set("the a an and or of to in on at for by with from as is was were be been are it its this that these those "
           "which who whom what when where how did do does has have had will would said says say than then there their "
           "into after before over under about across between among per against not no".split())


def tokenize(text: str, keep_stop: bool = False) -> list:
    toks = _TOKEN.findall(text.lower())
    return toks if keep_stop else [t for t in toks if t not in STOP]


class BM25Index:
    """An inverted index with BM25 scoring. Built over chunks."""

    def __init__(self, chunks: list, k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.ids = [c.chunk_id for c in chunks]
        self.texts = {c.chunk_id: c.text for c in chunks}
        self.tf = {}
        self.postings = defaultdict(dict)     # term -> {chunk_id: tf}
        self.dl = {}
        for c in chunks:
            toks = tokenize(c.text)
            counts = Counter(toks)
            self.tf[c.chunk_id] = counts
            self.dl[c.chunk_id] = len(toks)
            for t, n in counts.items():
                self.postings[t][c.chunk_id] = n
        self.N = len(chunks)
        self.avgdl = sum(self.dl.values()) / max(1, self.N)

    def idf(self, term: str) -> float:
        n = len(self.postings.get(term, {}))
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def term_score(self, term: str, chunk_id: str) -> float:
        tf = self.postings.get(term, {}).get(chunk_id, 0)
        if tf == 0:
            return 0.0
        dl = self.dl[chunk_id]
        denom = tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
        return self.idf(term) * tf * (self.k1 + 1) / denom

    def score(self, query: str, chunk_id: str) -> float:
        return sum(self.term_score(t, chunk_id) for t in set(tokenize(query)))

    def search(self, query: str, k: int = 10) -> list:
        """Return [(chunk_id, score)] for the top k, scanning only postings that match."""
        acc = defaultdict(float)
        for t in set(tokenize(query)):
            for cid in self.postings.get(t, {}):
                acc[cid] += self.term_score(t, cid)
        ranked = sorted(acc.items(), key=lambda x: -x[1])
        return ranked[:k]

    def explain(self, query: str, chunk_id: str):
        """A DataFrame of per-term contributions for one chunk."""
        import pandas as pd
        rows = []
        for t in sorted(set(tokenize(query))):
            tf = self.postings.get(t, {}).get(chunk_id, 0)
            rows.append({"term": t, "tf_in_chunk": tf, "docs_with_term": len(self.postings.get(t, {})),
                         "idf": round(self.idf(t), 3), "contribution": round(self.term_score(t, chunk_id), 3)})
        df = pd.DataFrame(rows).sort_values("contribution", ascending=False)
        return df

    def saturation(self, tf_values, dl_ratio: float = 1.0):
        """Term-frequency saturation curve for a fixed idf of 1. Used for the plot."""
        return [tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * dl_ratio)) for tf in tf_values]


def grep(chunks: list, pattern: str, flags=re.IGNORECASE) -> list:
    """Literal pattern search over chunk text, the way ripgrep works over files."""
    rx = re.compile(pattern, flags)
    out = []
    for c in chunks:
        for line_no, line in enumerate(c.text.split(". "), start=1):
            if rx.search(line):
                out.append({"chunk_id": c.chunk_id, "doc_id": c.doc_id, "line": line_no, "match": line.strip()})
    return out


# Test inputs and expected outcomes
# from ragkit.corpus import DOCS; from ragkit.chunking import chunk_corpus
# idx = BM25Index(chunk_corpus(DOCS, "structural"))
# idx.search("Nord Aerospace", 3)[0][0].startswith(("a1", "g1", "g2"))  -> True
# idx.explain("Nord Aerospace", idx.search("Nord Aerospace", 1)[0][0])   -> two rows, "nord" has the higher idf
# grep(chunk_corpus(DOCS, "structural"), r"ERR-4471")                   -> one hit in doc h5
