from harness import check, expect, expect_eq
from _fixtures import REGISTRY, scripted, always, alternating, TOOL_A, TOOL_B, DONE

START = [{"role": "user", "content": [{"text": "q"}]}]


@check("two tools alternating forever is caught before the cap",
       teaches="A/B/A/B is the most common real oscillation and never repeats consecutively per tool.")
def t_alternating(m):
    r = m.run_loop(START, alternating(TOOL_A, TOOL_B), REGISTRY, max_steps=12)
    expect(r["outcome"] in ("stuck", "exhausted"), "an alternating model must not answer")
    expect(r["steps"] <= 12, "never exceed the cap")


@check("max_steps=0 makes no model calls at all")
def t_zero(m):
    called = {"n": 0}

    def counting(_msgs):
        called["n"] += 1
        return DONE

    r = m.run_loop(START, counting, REGISTRY, max_steps=0)
    expect_eq(called["n"], 0, "a zero budget means zero calls")
    expect(r["outcome"] != "answered", "you cannot answer without calling the model")


@check("an immediate answer costs one step")
def t_one_step(m):
    r = m.run_loop(START, always(DONE), REGISTRY, max_steps=6)
    expect_eq(r["outcome"], "answered")
    expect_eq(r["steps"], 1)


@check("history is returned and well formed")
def t_history(m):
    r = m.run_loop(START, scripted(TOOL_A, DONE), REGISTRY, max_steps=6)
    roles = [x["role"] for x in r["messages"]]
    expect_eq(roles, ["user", "assistant", "user", "assistant"],
              "the loop keeps the alternating history from AGL-02")


@check("the caller's starting history is not mutated")
def t_no_mutation(m):
    start = [{"role": "user", "content": [{"text": "q"}]}]
    m.run_loop(start, scripted(TOOL_A, DONE), REGISTRY, max_steps=6)
    expect_eq(len(start), 1, "run_loop must not extend the list it was given")
