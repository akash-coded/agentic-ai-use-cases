from harness import check, expect, expect_eq
from _fixtures import CORPUS


@check("matching is case-insensitive")
def t_case(m):
    expect_eq(m.search_policy("CARRIER Refundable", CORPUS)["status"], "ok")


@check("all query terms must be present, not any")
def t_all_terms(m):
    r = m.search_policy("carrier zeppelin", CORPUS)
    expect_eq(r["status"], "no_matches", "'carrier' matches but 'zeppelin' does not — so nothing matches")


@check("an empty corpus is no_matches, not unavailable",
       teaches="An empty corpus WAS searched. The distinction has to survive the edge case.")
def t_empty_corpus(m):
    r = m.search_policy("refund", [])
    expect_eq(r["status"], "no_matches")
    expect_eq(r["searched_count"], 0)


@check("no path returns None, [], or a bare {}")
def t_never_bare(m):
    for args in [("refund", CORPUS), ("nope", CORPUS), ("refund", CORPUS, "down"), ("", CORPUS)]:
        r = m.search_policy(*args)
        expect(isinstance(r, dict) and r, f"{args} returned {r!r}")
        expect("status" in r, "status is mandatory on every path")


@check("the ok result does not carry advice",
       teaches="Advice on success trains the model to ignore it; keep the signal where it means something.")
def t_ok_clean(m):
    r = m.search_policy("carrier refundable", CORPUS)
    expect("advice" not in r, "a successful search needs no advice")
