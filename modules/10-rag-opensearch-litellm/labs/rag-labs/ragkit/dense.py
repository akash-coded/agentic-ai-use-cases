"""Dense retrieval: an embedder, an exact index, and an approximate index.

The offline embedder is latent semantic analysis, TF-IDF followed by truncated SVD,
fitted on the corpus itself. It is an established dense retriever from the 1990s and
it is used here as a stand-in: it encodes once, it is searched by cosine, and it also
yields a vector per term so late interaction can be shown. It is not a modern neural
embedder; a real one replaces it through the same `Embedder` interface.
"""
import numpy as np


class Embedder:
    """Interface. Subclasses implement embed(texts) -> unit-length float32 array."""
    name = "abstract"

    def embed(self, texts: list) -> np.ndarray:
        raise NotImplementedError

    def embed_one(self, text: str) -> np.ndarray:
        return self.embed([text])[0]


def _unit(m: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(m, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return (m / n).astype(np.float32)


class LSAEmbedder(Embedder):
    name = "lsa"

    def __init__(self, n_components: int = 48, random_state: int = 0):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.decomposition import TruncatedSVD
        self.vec = TfidfVectorizer(lowercase=True, sublinear_tf=True, stop_words="english", token_pattern=r"[a-z0-9][a-z0-9\-']+")
        self.svd = TruncatedSVD(n_components=n_components, random_state=random_state)
        self.fitted = False

    def fit(self, texts: list):
        X = self.vec.fit_transform(texts)
        k = min(self.svd.n_components, X.shape[1] - 1, X.shape[0] - 1)
        self.svd.set_params(n_components=k)
        self.svd.fit(X)
        self.fitted = True
        return self

    def embed(self, texts: list) -> np.ndarray:
        assert self.fitted, "call fit(corpus_texts) first"
        return _unit(self.svd.transform(self.vec.transform(texts)))

    def term_vectors(self) -> dict:
        """One unit vector per vocabulary term: the columns of the SVD, scaled by singular values."""
        V = self.svd.components_.T * self.svd.singular_values_
        V = _unit(V)
        return {t: V[i] for t, i in self.vec.vocabulary_.items()}

    def token_vectors(self, text: str) -> tuple:
        """Per-token vectors for a text, for late interaction. Unknown tokens are skipped."""
        tv = self.term_vectors()
        toks = [t for t in self.vec.build_analyzer()(text) if t in tv]
        return toks, np.stack([tv[t] for t in toks]) if toks else np.zeros((0, self.svd.n_components), np.float32)


class FlatIndex:
    """Exact nearest neighbour by cosine. Recall is 1.0 by construction."""
    name = "flat"

    def __init__(self, ids: list, vectors: np.ndarray):
        self.ids = list(ids)
        self.V = _unit(np.asarray(vectors, dtype=np.float32))

    def search(self, q: np.ndarray, k: int = 10) -> list:
        sims = self.V @ _unit(q.reshape(1, -1))[0]
        top = np.argsort(-sims)[:k]
        return [(self.ids[i], float(sims[i])) for i in top]

    def cosine(self, a_id: str, b_id: str) -> float:
        i, j = self.ids.index(a_id), self.ids.index(b_id)
        return float(self.V[i] @ self.V[j])


class IVFIndex:
    """Inverted-file approximate index: cluster vectors, search only the nearest nprobe clusters.

    On a corpus this small a flat scan is the right production choice. The point here is
    the knob: nprobe trades latency for recall, and recall against flat search is measurable.
    """
    name = "ivf"

    def __init__(self, ids: list, vectors: np.ndarray, nlist: int = 8, random_state: int = 0):
        from sklearn.cluster import KMeans
        self.ids = list(ids)
        self.V = _unit(np.asarray(vectors, dtype=np.float32))
        nlist = min(nlist, len(self.ids))
        self.km = KMeans(n_clusters=nlist, n_init=4, random_state=random_state).fit(self.V)
        self.centroids = _unit(self.km.cluster_centers_)
        self.lists = {c: np.where(self.km.labels_ == c)[0] for c in range(nlist)}
        self.nlist = nlist

    def search(self, q: np.ndarray, k: int = 10, nprobe: int = 1) -> list:
        qv = _unit(q.reshape(1, -1))[0]
        order = np.argsort(-(self.centroids @ qv))[:nprobe]
        cand = np.concatenate([self.lists[c] for c in order])
        sims = self.V[cand] @ qv
        top = cand[np.argsort(-sims)[:k]]
        return [(self.ids[i], float(self.V[i] @ qv)) for i in top]

    def scanned(self, q: np.ndarray, nprobe: int = 1) -> int:
        qv = _unit(q.reshape(1, -1))[0]
        order = np.argsort(-(self.centroids @ qv))[:nprobe]
        return int(sum(len(self.lists[c]) for c in order))


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(_unit(a.reshape(1, -1))[0] @ _unit(b.reshape(1, -1))[0])


# Test inputs and expected outcomes
# from ragkit.corpus import DOCS; from ragkit.chunking import chunk_corpus
# ch = chunk_corpus(DOCS, "structural"); emb = LSAEmbedder().fit([c.text for c in ch])
# V = emb.embed([c.text for c in ch]); np.allclose(np.linalg.norm(V, axis=1), 1.0)  -> True
# FlatIndex([c.chunk_id for c in ch], V).search(emb.embed_one("Nord Aerospace chief executive"), 3)  -> a1 or g2 chunk first
# IVFIndex(ids, V, nlist=6).search(q, 5, nprobe=6) == FlatIndex(ids, V).search(q, 5)   -> same ids when every list is probed
