from harness import check, expect, expect_eq
from _fixtures import REGISTRY, assistant_tool_turn, assistant_text_turn, roles, tool_results

START = [{"role": "user", "content": [{"text": "Is XY7Q2M refundable?"}]}]


@check("end_turn appends the answer and reports done",
       "When the model is finished, the loop stops.")
def t_end(m):
    msgs, done = m.advance(START, assistant_text_turn("Yes — cancelled by the carrier."), REGISTRY)
    expect_eq(done, True, "end_turn means done")
    expect_eq(roles(msgs), ["user", "assistant"], "the assistant's answer is appended")


@check("the assistant's tool request is appended verbatim",
       "Skip this and the model asks for the same tool again — it has no record of asking.",
       teaches="This single omission is the most common agent-loop bug there is.")
def t_assistant_appended(m):
    resp = assistant_tool_turn(("tu_1", "get_booking", {"booking_ref": "XY7Q2M"}))
    msgs, done = m.advance(START, resp, REGISTRY)
    expect_eq(done, False, "a tool_use turn is not done")
    expect_eq(msgs[1], resp["output"]["message"],
              "the assistant message must be appended exactly as the model sent it")


@check("the tool result is a user turn",
       "Roles describe which side the content came from. Results are input to the model.")
def t_user_role(m):
    resp = assistant_tool_turn(("tu_1", "get_booking", {"booking_ref": "XY7Q2M"}))
    msgs, _ = m.advance(START, resp, REGISTRY)
    expect_eq(roles(msgs), ["user", "assistant", "user"], "history must alternate user/assistant/user")


@check("the result carries the matching toolUseId")
def t_id_match(m):
    resp = assistant_tool_turn(("tu_7", "get_booking", {"booking_ref": "XY7Q2M"}))
    msgs, _ = m.advance(START, resp, REGISTRY)
    trs = tool_results(msgs[-1])
    expect_eq(len(trs), 1, "one request, one result")
    expect_eq(trs[0]["toolUseId"], "tu_7", "the id ties reply to request")


@check("parallel tool calls become ONE user message",
       "Several results, one turn — otherwise two user messages break role alternation.",
       teaches="One message per result is rejected by the API, and the error points at the wrong place.")
def t_parallel(m):
    resp = assistant_tool_turn(("a", "get_booking", {"booking_ref": "X"}),
                               ("b", "get_disruption", {"flight_no": "BA1", "date": "2026-07-01"}))
    msgs, _ = m.advance(START, resp, REGISTRY)
    expect_eq(roles(msgs), ["user", "assistant", "user"], "still exactly one user turn")
    trs = tool_results(msgs[-1])
    expect_eq(len(trs), 2, "both results in the same message")
    expect_eq([t["toolUseId"] for t in trs], ["a", "b"], "results stay in request order")


@check("the caller's history is not mutated",
       "Two loops sharing a list is a bug you will not enjoy finding.")
def t_no_mutation(m):
    original = [{"role": "user", "content": [{"text": "hi"}]}]
    before = len(original)
    m.advance(original, assistant_text_turn("hello"), REGISTRY)
    expect_eq(len(original), before, "advance() must return a new list, not extend the old one")
