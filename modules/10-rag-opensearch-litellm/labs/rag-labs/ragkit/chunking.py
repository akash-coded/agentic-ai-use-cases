"""Chunking strategies. Every chunker returns Chunk objects with stable ids.

A stable id is doc_id + ordinal + content hash, so an unchanged chunk keeps its id
across index rebuilds and a changed one gets a new id. That is what makes
incremental re-indexing possible.
"""
import re
from .store import Chunk, Doc, content_hash

_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")


def sentences(text: str) -> list:
    return [s.strip() for s in _SENT.split(text.replace("\n\n", " ")) if s.strip()]


def _mk(doc: Doc, ordinal: int, text: str, heading: str = "", version: str = "v1") -> Chunk:
    cid = f"{doc.doc_id}:{ordinal}:{content_hash(text)[:8]}"
    return Chunk(cid, doc.doc_id, ordinal, text, heading or doc.title, version)


def fixed_words(doc: Doc, size: int = 40, overlap: int = 0, version: str = "v1") -> list:
    """Cut the body into windows of `size` words, sliding by size minus overlap."""
    words = doc.body.replace("\n\n", " ").split()
    step = max(1, size - overlap)
    out, i, ordinal = [], 0, 0
    while i < len(words):
        out.append(_mk(doc, ordinal, " ".join(words[i:i + size]), version=version))
        ordinal += 1
        if i + size >= len(words):
            break
        i += step
    return out


def sentence_window(doc: Doc, n: int = 2, overlap: int = 0, version: str = "v1") -> list:
    """Windows of `n` sentences, sliding by n minus overlap sentences."""
    sents = sentences(doc.body)
    step = max(1, n - overlap)
    out, i, ordinal = [], 0, 0
    while i < len(sents):
        out.append(_mk(doc, ordinal, " ".join(sents[i:i + n]), version=version))
        ordinal += 1
        if i + n >= len(sents):
            break
        i += step
    return out


def structural(doc: Doc, carry_title: bool = True, version: str = "v1") -> list:
    """One chunk per paragraph, with the document title carried as the heading path."""
    paras = [p.strip() for p in doc.body.split("\n\n") if p.strip()]
    out = []
    for i, p in enumerate(paras):
        text = f"{doc.title}. {p}" if carry_title else p
        out.append(_mk(doc, i, text, heading=doc.title, version=version))
    return out


def whole_doc(doc: Doc, version: str = "v1") -> list:
    return [_mk(doc, 0, doc.body.replace("\n\n", " "), version=version)]


CHUNKERS = {
    "whole_doc": lambda d, v="v1": whole_doc(d, version=v),
    "fixed_25": lambda d, v="v1": fixed_words(d, 25, 0, version=v),
    "fixed_25_ov8": lambda d, v="v1": fixed_words(d, 25, 8, version=v),
    "fixed_40": lambda d, v="v1": fixed_words(d, 40, 0, version=v),
    "fixed_40_ov12": lambda d, v="v1": fixed_words(d, 40, 12, version=v),
    "sent_2": lambda d, v="v1": sentence_window(d, 2, 0, version=v),
    "sent_2_ov1": lambda d, v="v1": sentence_window(d, 2, 1, version=v),
    "structural": lambda d, v="v1": structural(d, version=v),
}


def chunk_corpus(docs: list, chunker: str = "structural", version: str = "v1") -> list:
    fn = CHUNKERS[chunker]
    out = []
    for d in docs:
        out.extend(fn(d, version))
    return out


def resolve_gold(question, chunks: list) -> dict:
    """Map each gold span to the chunk ids whose text contains it whole.

    A span with no containing chunk is boundary loss: the fact exists in the corpus
    but no single retrievable unit carries it.
    """
    by_doc = {}
    for c in chunks:
        by_doc.setdefault(c.doc_id, []).append(c)
    out = {}
    for doc_id, span in question.gold:
        norm_span = " ".join(span.split())
        hits = [c.chunk_id for c in by_doc.get(doc_id, []) if norm_span in " ".join(c.text.split())]
        out[(doc_id, span)] = hits
    return out


def gold_chunk_sets(question, chunks: list) -> list:
    """One set of acceptable chunk ids per gold span. Empty set means boundary loss."""
    return [set(v) for v in resolve_gold(question, chunks).values()]


# Test inputs and expected outcomes
# from ragkit.corpus import DOCS, ANCHOR
# len(fixed_words(DOCS[0], 40, 0))     -> 3 chunks for a 100-word body
# structural(DOCS[0])[0].heading        -> "Nord Aerospace names Elena Ruiz chief executive"
# gold_chunk_sets(ANCHOR, chunk_corpus(DOCS, "structural"))  -> two non-empty sets
# gold_chunk_sets(ANCHOR, chunk_corpus(DOCS, "fixed_25"))    -> at least one empty set (boundary loss)
