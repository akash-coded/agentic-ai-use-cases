from harness import check, expect, expect_eq
from _fixtures import classify_error, working, failing, Throttled, PRIMARY, FALLBACK


@check("a three-model chain falls through twice")
def t_three(m):
    chain = [failing("a", Throttled("x")), failing("b", Throttled("y")), working("c")]
    r = m.invoke_with_failover("q", chain, classify_error)
    expect_eq(r["model_id"], "c")
    expect_eq(r["degraded"], True)
    expect_eq(len(r["attempts"]), 3)


@check("the successful attempt is recorded too",
       teaches="A log of only failures cannot tell you which model produced the answer.")
def t_success_recorded(m):
    r = m.invoke_with_failover("q", [PRIMARY], classify_error)
    expect_eq(r["attempts"][-1]["outcome"], "ok")
    expect_eq(r["attempts"][-1]["error"], None)


@check("failed chains report degraded=False, not True",
       teaches="Nothing answered, so nothing degraded — conflating them corrupts the metric.")
def t_failed_not_degraded(m):
    r = m.invoke_with_failover("q", [failing("a", Throttled("x"))], classify_error)
    expect_eq(r["failed"], True)
    expect_eq(r["degraded"], False)


@check("the response is passed through untouched")
def t_passthrough(m):
    payload = {"answer": "text", "usage": {"inputTokens": 10}}
    r = m.invoke_with_failover("q", [{"id": "m", "call": lambda _: payload}], classify_error)
    expect_eq(r["response"], payload)


@check("attempt records carry an error string on failure")
def t_error_text(m):
    r = m.invoke_with_failover("q", [failing("a", Throttled("rate limit")), FALLBACK], classify_error)
    expect(r["attempts"][0]["error"], "a failed attempt needs the error recorded")
