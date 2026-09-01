"""AGL-03 · Break phase — models that behave badly on purpose."""
from harness import check, expect, expect_eq
from _fixtures import REGISTRY, always, scripted, tool_turn, text_turn, TOOL_A, DONE

START = [{"role": "user", "content": [{"text": "q"}]}]


@check("a tool_use turn requesting nothing does not spin",
       "stopReason says tool_use, content has no toolUse blocks.",
       teaches="No tools requested means no progress possible; spending the budget confirming that is waste.")
def t_empty_tool_turn(m):
    empty = {"output": {"message": {"role": "assistant", "content": [{"text": "thinking"}]}},
             "stopReason": "tool_use"}
    r = m.run_loop(START, always(empty), REGISTRY, max_steps=8)
    expect(r["outcome"] != "answered", "an empty tool turn is not an answer")
    expect(r["steps"] <= 8, "must still respect the cap")


@check("a model that raises does not leave the loop half-open",
       "Upstream errors happen mid-run.",
       teaches="An exception escaping run_loop loses the history you had already paid for.")
def t_model_raises(m):
    state = {"n": 0}

    def flaky(_msgs):
        state["n"] += 1
        if state["n"] == 2:
            raise ConnectionError("provider dropped the connection")
        return TOOL_A

    try:
        r = m.run_loop(START, flaky, REGISTRY, max_steps=6)
    except ConnectionError:
        raise AssertionError(
            "the provider error escaped run_loop — catch it and return an outcome, "
            "so the caller keeps the history and the step count") from None
    expect(r["outcome"] != "answered", "a dropped connection is not an answer")


@check("every outcome carries the required keys",
       "The caller branches on this contract.",
       teaches="A missing key turns a handled failure into an AttributeError one layer up.")
def t_contract(m):
    for model, cap in [(always(DONE), 4), (always(TOOL_A), 4), (scripted(TOOL_A, TOOL_A, TOOL_A), 2)]:
        r = m.run_loop(START, model, REGISTRY, max_steps=cap)
        for k in ("outcome", "answer", "steps", "messages", "reason"):
            expect(k in r, f"outcome dict is missing {k!r}")
        expect(r["outcome"] in ("answered", "exhausted", "stuck", "failed"),
               f"unexpected outcome {r['outcome']!r}")
        expect(isinstance(r["steps"], int) and r["steps"] <= cap,
               f"steps ({r['steps']}) must be an int within the cap ({cap})")


@check("the same tool with DIFFERENT arguments is progress, not oscillation",
       "Retrying with a corrected argument is exactly what you want the model to do.",
       teaches="Signature on name alone punishes the self-correction you asked for in AGL-01.")
def t_not_false_positive(m):
    a1 = tool_turn({"toolUse": {"toolUseId": "1", "name": "get_booking", "input": {"booking_ref": "WRONG"}}})
    a2 = tool_turn({"toolUse": {"toolUseId": "2", "name": "get_booking", "input": {"booking_ref": "XY7Q2M"}}})
    r = m.run_loop(START, scripted(a1, a2, DONE), REGISTRY, max_steps=6)
    expect_eq(r["outcome"], "answered",
              "different arguments mean the model is correcting itself — let it")
