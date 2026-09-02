from harness import check, expect, expect_eq
def hist(n, t=100): return [{"role": "user" if i % 2 == 0 else "assistant", "content": [{"text": f"turn {i}"}], "tokens": t} for i in range(n)]
def summ(tokens=80):
    calls = {"n": 0}
    def f(msgs):
        calls["n"] += 1; return {"role": "user", "content": [{"text": f"summary of {len(msgs)}"}], "tokens": tokens}
    f.calls = calls; return f

@check("bug 1 — under budget, no model call is spent",
       teaches="Summarising on a schedule pays for a call every turn, forever. Summarise at a threshold.")
def t_no_call(m):
    s = summ(); r = m.trim_history(hist(4), 1000, s)
    expect_eq(s.calls["n"], 0, "summarise must not run under budget"); expect_eq(len(r), 4)

@check("over budget, summarise runs exactly once")
def t_once(m):
    s = summ(); m.trim_history(hist(20), 500, s); expect_eq(s.calls["n"], 1)

@check("bug 2 — the newest message survives eviction",
       teaches="pop() removes the END of the list — the message you are about to answer. Evict from the front.")
def t_newest(m):
    h = hist(20); r = m.trim_history(h, 250, summ(80))
    expect(r and r[-1]["content"] == h[-1]["content"], "the last message must be the user's latest turn")

@check("the result fits the budget")
def t_fits(m):
    r = m.trim_history(hist(20), 500, summ(80)); expect(sum(x["tokens"] for x in r) <= 500, "over budget after trimming")

@check("under budget the history is returned unchanged")
def t_unchanged(m):
    h = hist(3); expect_eq(m.trim_history(h, 1000, summ()), h)
