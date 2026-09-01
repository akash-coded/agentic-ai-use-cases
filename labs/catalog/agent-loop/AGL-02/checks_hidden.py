from harness import check, expect, expect_eq
from _fixtures import REGISTRY, assistant_tool_turn, assistant_text_turn, roles, tool_results

START = [{"role": "user", "content": [{"text": "q"}]}]


@check("a failing tool still produces a result block")
def t_failing_tool(m):
    reg = {"boom": lambda: (_ for _ in ()).throw(RuntimeError("down"))}
    msgs, _ = m.advance(START, assistant_tool_turn(("t", "boom", {})), reg)
    trs = tool_results(msgs[-1])
    expect_eq(len(trs), 1, "a failure is still a result — the model needs a reply")
    expect_eq(trs[0]["status"], "error")


@check("mixed text and toolUse content keeps the whole assistant message",
       teaches="Models narrate before calling a tool. Dropping the text loses the reasoning trail.")
def t_mixed_content(m):
    resp = {"output": {"message": {"role": "assistant", "content": [
        {"text": "Let me check that booking."},
        {"toolUse": {"toolUseId": "t", "name": "get_booking", "input": {"booking_ref": "X"}}}]}},
        "stopReason": "tool_use"}
    msgs, _ = m.advance(START, resp, REGISTRY)
    expect_eq(msgs[1], resp["output"]["message"], "append the message whole, text included")


@check("roles alternate across several turns")
def t_multi_turn(m):
    msgs = list(START)
    msgs, _ = m.advance(msgs, assistant_tool_turn(("a", "get_booking", {"booking_ref": "X"})), REGISTRY)
    msgs, _ = m.advance(msgs, assistant_tool_turn(("b", "get_booking", {"booking_ref": "Y"})), REGISTRY)
    msgs, done = m.advance(msgs, assistant_text_turn("done"), REGISTRY)
    expect_eq(done, True)
    expect_eq(roles(msgs), ["user", "assistant", "user", "assistant", "user", "assistant"],
              "every tool round trip adds exactly one assistant and one user turn")


@check("an empty registry still yields a well-formed turn")
def t_empty_registry(m):
    msgs, done = m.advance(START, assistant_tool_turn(("t", "whatever", {})), {})
    expect_eq(done, False)
    expect_eq(roles(msgs)[-1], "user", "an unknown tool is still a user-role result")


@check("a tool_use response with no toolUse blocks does not create an empty user turn",
       teaches="An empty user message is a wasted turn and, on some providers, a validation error.")
def t_no_blocks(m):
    resp = {"output": {"message": {"role": "assistant", "content": [{"text": "hmm"}]}},
            "stopReason": "tool_use"}
    msgs, _ = m.advance(START, resp, REGISTRY)
    expect(roles(msgs) == ["user", "assistant"],
           f"expected no trailing empty user turn, got {roles(msgs)}")
