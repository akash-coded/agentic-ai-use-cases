from harness import check, expect, expect_eq
@check("a document ranked well by BOTH retrievers wins",
       teaches="That is the point of fusion: agreement between retrievers is the strongest signal you have.")
def t_agree(m):
    out = m.rrf([["a", "b", "c"], ["b", "a", "d"]])
    expect(out[0] in ("a", "b") and out[1] in ("a", "b"), f"a and b appear in both lists and must lead: {out}")
@check("a document ranked first by one retriever beats one ranked last by one",
       teaches="Summing raw ranks inverts this: rank 1 contributes LESS than rank 3, and the sort puts the worst first.")
def t_direction(m):
    out = m.rrf([["x", "y", "z"]]); expect_eq(out, ["x", "y", "z"], "a single ranking must fuse to itself, in order")
@check("a doc seen by two retrievers at rank 2 beats a doc seen once at rank 1",
       teaches="1/62 + 1/62 > 1/61. Two moderate votes outrank one strong one — by design.")
def t_two_votes(m):
    out = m.rrf([["solo", "both"], ["other", "both"]]); expect_eq(out[0], "both")
@check("k is used — with a huge k, ranks barely matter and ties resolve by count",
       teaches="k damps the advantage of top ranks; it is why RRF needs no score tuning.")
def t_k(m):
    out = m.rrf([["a", "b"], ["b", "c"]], k=10_000); expect_eq(out[0], "b", "b appears twice; with a large k that dominates")
@check("empty input returns an empty list")
def t_empty(m): expect_eq(m.rrf([]), [])
