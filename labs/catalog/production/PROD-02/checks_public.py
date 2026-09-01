from harness import check, expect, expect_eq
from _fixtures import (classify_error, working, failing, Throttled, BadRequest,
                       PRIMARY, FALLBACK, THROTTLED, BROKEN)


@check("the primary answering is not degraded")
def t_primary(m):
    r = m.invoke_with_failover("q", [PRIMARY, FALLBACK], classify_error)
    expect_eq(r["model_id"], "claude-primary")
    expect_eq(r["degraded"], False)
    expect_eq(r["failed"], False)


@check("a retryable failure falls through to the next model")
def t_failover(m):
    r = m.invoke_with_failover("q", [THROTTLED, FALLBACK], classify_error)
    expect_eq(r["failed"], False)
    expect_eq(r["model_id"], "claude-fallback", "the fallback answered")


@check("a fallback answer is marked degraded",
       "The one field that makes silent failover visible.",
       teaches="Without this, quality drops with no signal and no way to attribute it later.")
def t_degraded(m):
    r = m.invoke_with_failover("q", [THROTTLED, FALLBACK], classify_error)
    expect_eq(r["degraded"], True, "anything other than the primary answering is degraded")


@check("a fatal error stops the chain immediately",
       "A malformed request will be malformed on the fallback too.",
       teaches="Retrying a fatal error doubles latency and cost to produce the same failure.")
def t_fatal_stops(m):
    r = m.invoke_with_failover("q", [BROKEN, FALLBACK], classify_error)
    expect_eq(r["failed"], True, "a fatal primary error must not fall through")
    expect_eq(len(r["attempts"]), 1, "the fallback should never have been called")


@check("every attempt is recorded in order")
def t_attempts(m):
    r = m.invoke_with_failover("q", [THROTTLED, FALLBACK], classify_error)
    expect_eq([a["model_id"] for a in r["attempts"]], ["claude-primary", "claude-fallback"])
    expect_eq([a["outcome"] for a in r["attempts"]], ["retryable", "ok"])


@check("a chain where everything fails returns, it does not raise",
       "A failed chain is a value the caller can log and escalate.")
def t_all_fail(m):
    chain = [failing("a", Throttled("x")), failing("b", Throttled("y"))]
    r = m.invoke_with_failover("q", chain, classify_error)
    expect_eq(r["failed"], True)
    expect_eq(r["response"], None)
    expect_eq(len(r["attempts"]), 2, "both failures are on the record")
