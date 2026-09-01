"""MEM-01 · Break phase — budgets that cannot be met."""
from harness import check, expect, expect_eq
from _fixtures import msg, history, make_summariser


@check("a single message larger than the whole budget does not loop forever",
       "One turn, 5000 tokens, 500 budget.",
       teaches="Popping until it fits never terminates when the last message alone exceeds the budget.")
def t_oversized_single(m):
    r = m.trim_history([msg("user", "enormous", 5000)], 500, make_summariser(80))
    expect(r["messages"], "the last message survives even when it does not fit")
    expect(r["tokens"] > 500, "report the real total — do not pretend it fits")


@check("a summary bigger than what it replaced still terminates",
       "Summarisers can return more than they were given.",
       teaches="Assuming summarisation always shrinks turns an optimisation into an infinite loop.")
def t_fat_summary(m):
    r = m.trim_history(history(10, 100), 400, make_summariser(tokens=9000), keep_recent=2)
    expect(r["tokens"] <= 400 or len(r["messages"]) == 1,
           "either it fits, or only the newest message is left")


@check("keep_recent larger than the history is safe")
def t_keep_too_big(m):
    s = make_summariser()
    r = m.trim_history(history(3, 100), 100, s, keep_recent=10)
    expect(r["messages"], "still returns something")
    expect_eq(s.calls["n"], 0, "nothing is older than the protected block")


@check("keep_recent of zero still protects the newest message",
       "The one invariant that holds regardless of configuration.",
       teaches="A config value should not be able to delete the message you are answering.")
def t_keep_zero(m):
    h = history(10, 100)
    r = m.trim_history(h, 150, make_summariser(80), keep_recent=0)
    expect(r["messages"], "never return an empty history")
    expect_eq(r["messages"][-1]["content"], h[-1]["content"],
              "the newest turn survives even at keep_recent=0")
