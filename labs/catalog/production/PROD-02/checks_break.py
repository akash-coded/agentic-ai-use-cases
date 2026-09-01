"""PROD-02 · Break phase — bad afternoons."""
from harness import check, expect, expect_eq
from _fixtures import classify_error, working, failing, Throttled


@check("an empty model list fails cleanly",
       "Config errors produce empty chains.",
       teaches="An IndexError here looks like a code bug and is actually a config bug.")
def t_empty_chain(m):
    r = m.invoke_with_failover("q", [], classify_error)
    expect_eq(r["failed"], True)
    expect_eq(r["attempts"], [])


@check("an unclassifiable error is treated as fatal",
       "classify_error can itself raise.",
       teaches="Defaulting to retryable on an unknown error walks the whole chain for nothing.")
def t_classifier_raises(m):
    def bad_classifier(exc):
        raise KeyError("no rule for this")

    r = m.invoke_with_failover("q", [failing("a", RuntimeError("?")), working("b")], bad_classifier)
    expect_eq(r["failed"], True, "if you cannot classify it, do not retry it")
    expect_eq(len(r["attempts"]), 1, "the chain stops at the unclassifiable error")


@check("a model raising BaseException is caught",
       "Libraries call sys.exit().",
       teaches="`except Exception` misses SystemExit, and the whole request dies with the library.")
def t_base_exception(m):
    r = m.invoke_with_failover("q", [failing("a", SystemExit("library quit")), working("b")],
                               lambda e: "retryable")
    expect(r["failed"] is False or r["attempts"], "a BaseException must not escape the failover wrapper")


@check("the answering model is always identifiable",
       "Across every successful path.",
       teaches="This is the field the silent-degradation watchlist depends on; it must never be absent.")
def t_always_identifiable(m):
    chains = [[working("a")],
              [failing("a", Throttled("x")), working("b")],
              [failing("a", Throttled("x")), failing("b", Throttled("y")), working("c")]]
    for chain in chains:
        r = m.invoke_with_failover("q", chain, classify_error)
        expect_eq(r["failed"], False)
        expect(r["model_id"], "a successful response must always name its model")
        expect(isinstance(r["degraded"], bool), "degraded must be a real boolean, not None")
