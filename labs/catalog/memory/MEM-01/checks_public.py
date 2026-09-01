from harness import check, expect, expect_eq
from _fixtures import msg, history, make_summariser


@check("under budget, history is returned untouched")
def t_under(m):
    s = make_summariser()
    h = history(4, 100)
    r = m.trim_history(h, 1000, s)
    expect_eq(r["messages"], h)
    expect_eq(r["evicted"], 0)
    expect_eq(r["summarised"], False)


@check("no model call is spent when under budget",
       "Summarising on a schedule pays for a call every turn.",
       teaches="Threshold, not schedule — otherwise memory costs a model call per turn forever.")
def t_no_call(m):
    s = make_summariser()
    m.trim_history(history(4, 100), 1000, s)
    expect_eq(s.calls["n"], 0, "summarise must not be called under budget")


@check("over budget, older turns are summarised into one message")
def t_summarise(m):
    s = make_summariser(tokens=80)
    r = m.trim_history(history(10, 100), 500, s, keep_recent=4)
    expect_eq(r["summarised"], True)
    expect_eq(s.calls["n"], 1, "exactly one summarisation call")
    expect(r["messages"][0].get("is_summary"), "the summary goes at the front")


@check("the result fits the budget")
def t_fits(m):
    r = m.trim_history(history(20, 100), 500, make_summariser(80), keep_recent=4)
    expect(r["tokens"] <= 500, f"returned {r['tokens']} tokens against a 500 budget")


@check("the most recent message is never dropped",
       "It is the one you are answering.",
       teaches="Dropping the newest turn is the one eviction that guarantees a wrong answer.")
def t_keep_newest(m):
    h = history(20, 100)
    newest = h[-1]
    r = m.trim_history(h, 250, make_summariser(80), keep_recent=4)
    expect(r["messages"][-1] is newest or r["messages"][-1] == newest,
           "the final message must survive any eviction")


@check("evicted counts what was removed")
def t_evicted(m):
    r = m.trim_history(history(10, 100), 500, make_summariser(80), keep_recent=4)
    expect(r["evicted"] >= 6, f"six older turns were summarised away, evicted={r['evicted']}")
