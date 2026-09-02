# RET-102 · A rank fusion that ranks the wrong way

`retrieval` · **medium** · `fix` · ~12 min · no AWS account

Hybrid retrieval runs a lexical search and a dense search, then fuses the two rankings. Reciprocal rank fusion merges by **rank**, so you never have to reconcile two incompatible score scales. This implementation is subtly wrong, and the results look plausible enough to ship.

```python
def rrf(rankings, k=60):
    """rankings: a list of ranked lists of doc ids, best first. Returns fused doc ids, best first."""
    scores = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + rank
    return sorted(scores, key=scores.get, reverse=True)
```

## Find it

Run it in your head on `[["a","b","c"], ["b","a","d"]]`. Which document comes out on top — and should it?

The formula each retriever contributes for a document at rank *r* is `1 / (k + r)`. Fix the accumulation so a document ranked well by both retrievers rises, and one ranked well by only one is beaten by it.

````markdown
/drill RET-102

```python
def rrf(rankings, k=60):
    ...
```
````

## What this proves

That you understand *why* RRF uses a reciprocal — small ranks must produce large contributions — and that "the output is a sensible-looking list" is not evidence a ranker is correct.
