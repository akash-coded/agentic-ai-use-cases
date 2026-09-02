from harness import check, expect, expect_eq
def converges_after(n):
    def step(task, state):
        c = state.get("c", 0) + 1; return {"c": c}, c >= n, 100
    return step
def never(step_tokens=100):
    """A swarm that never converges — with a tripwire, because the UNFIXED code
    loops forever and a test must still terminate. 500 rounds is far beyond any
    sane cap; reaching it means nothing stopped the loop."""
    calls = {"n": 0}
    def step(task, state):
        calls["n"] += 1
        if calls["n"] > 500:
            raise RuntimeError("500 rounds and nothing stopped the swarm — there is no bound")
        return state, False, step_tokens
    return step
@check("a converging swarm still completes")
def t_ok(m):
    r = m.run_swarm(converges_after(3), "t"); expect_eq(r["outcome"], "completed"); expect_eq(r["rounds"], 3)
@check("bug — a swarm that never converges now terminates",
       teaches="Without a bound this loop runs until your budget alarm fires — or does not.")
def t_terminates(m):
    r = m.run_swarm(never(), "t", max_rounds=5); expect_eq(r["outcome"], "stopped"); expect(r["rounds"] <= 5, f"ran {r['rounds']} rounds against a cap of 5")
@check("the round cap binds at exactly max_rounds")
def t_rounds(m): expect_eq(m.run_swarm(never(), "t", max_rounds=4)["rounds"], 4)
@check("the token budget binds before the round cap when it is hit first",
       teaches="Six cheap rounds and six expensive ones are not the same cap. Bound tokens too.")
def t_tokens(m):
    r = m.run_swarm(never(step_tokens=30_000), "t", max_rounds=100, max_tokens=50_000)
    expect_eq(r["outcome"], "stopped"); expect(r["rounds"] <= 2, f"should stop on tokens within 2 rounds, took {r['rounds']}")
    expect("token" in r["reason"].lower(), "reason should name the token budget")
@check("a stop is an outcome with a reason, not a fake completion",
       teaches="Reporting 'completed' when the cap bound is the best-effort lie from AGL-03, wearing a different hat.")
def t_reason(m):
    r = m.run_swarm(never(), "t", max_rounds=2); expect(r["outcome"] != "completed" and len(r.get("reason", "")) > 10, f"a bound stop needs a real reason; got outcome={r['outcome']!r} reason={r.get('reason')!r}")
