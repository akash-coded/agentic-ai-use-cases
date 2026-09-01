from harness import check, expect, expect_eq
from _fixtures import msg, history, make_summariser


@check("summarise is called at most once")
def t_once(m):
    s = make_summariser(80)
    m.trim_history(history(40, 100), 300, s, keep_recent=4)
    expect(s.calls["n"] <= 1, f"summarise called {s.calls['n']} times")


@check("an empty history is handled")
def t_empty(m):
    r = m.trim_history([], 100, make_summariser())
    expect_eq(r["messages"], [])
    expect_eq(r["tokens"], 0)


@check("history shorter than keep_recent is not summarised")
def t_short(m):
    s = make_summariser()
    r = m.trim_history(history(2, 100), 150, s, keep_recent=4)
    expect_eq(s.calls["n"], 0, "there is nothing older than the protected block to summarise")


@check("tokens equals the sum of what is returned")
def t_tokens(m):
    r = m.trim_history(history(20, 100), 400, make_summariser(80), keep_recent=4)
    expect_eq(r["tokens"], sum(x.get("tokens", 0) for x in r["messages"]))


@check("the caller's list is not mutated")
def t_no_mutation(m):
    h = history(20, 100)
    m.trim_history(h, 300, make_summariser(80), keep_recent=4)
    expect_eq(len(h), 20, "trim_history must not mutate the history it was given")
