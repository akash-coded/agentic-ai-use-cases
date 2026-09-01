"""AGL-02 · Break phase — three turns, one failure, one back-reference."""
from harness import check, expect, expect_eq
from _fixtures import assistant_tool_turn, assistant_text_turn, roles, tool_results


@check("history survives a three-turn conversation with a mid-run failure",
       "Turn 2 fails; turn 3 must still be well formed.",
       teaches="Malformed history rarely fails where it was malformed — it fails a turn or two later.")
def t_three_turns(m):
    reg = {
        "get_booking": lambda booking_ref: {"ref": booking_ref},
        "flaky": lambda: (_ for _ in ()).throw(TimeoutError("upstream")),
    }
    msgs = [{"role": "user", "content": [{"text": "check two things"}]}]
    msgs, _ = m.advance(msgs, assistant_tool_turn(("a", "get_booking", {"booking_ref": "X"}),
                                                  ("b", "flaky", {})), reg)
    msgs, _ = m.advance(msgs, assistant_tool_turn(("c", "get_booking", {"booking_ref": "Y"})), reg)
    msgs, done = m.advance(msgs, assistant_text_turn("here is the summary"), reg)

    expect_eq(done, True)
    expect_eq(roles(msgs), ["user", "assistant", "user", "assistant", "user", "assistant"],
              "roles must still alternate after a failed tool")
    first = tool_results(msgs[2])
    expect_eq(len(first), 2, "both parallel results survived")
    expect_eq(sorted(r["status"] for r in first), ["error", "success"],
              "one succeeded and one failed — both are recorded")


@check("every toolUse in history has exactly one matching toolResult",
       "The invariant the API enforces, and the one you can check yourself.",
       teaches="An unanswered toolUse is the shape of the bug in AGL-01's silent-skip option.")
def t_pairing(m):
    reg = {"f": lambda: 1, "g": lambda: (_ for _ in ()).throw(ValueError("no"))}
    msgs = [{"role": "user", "content": [{"text": "go"}]}]
    msgs, _ = m.advance(msgs, assistant_tool_turn(("1", "f", {}), ("2", "g", {}), ("3", "missing", {})), reg)

    requested, answered = [], []
    for msg in msgs:
        for b in msg.get("content", []):
            if "toolUse" in b:
                requested.append(b["toolUse"]["toolUseId"])
            if "toolResult" in b:
                answered.append(b["toolResult"]["toolUseId"])
    expect_eq(sorted(requested), sorted(answered),
              "every request needs a reply — including the unknown tool")


@check("does not alias the assistant message into history",
       "Appending the same object you were handed lets a caller mutate your history.",
       teaches="Aliasing bugs surface as history that changes under you between turns.")
def t_no_alias(m):
    reg = {"f": lambda: 1}
    resp = assistant_tool_turn(("1", "f", {}))
    msgs, _ = m.advance([{"role": "user", "content": []}], resp, reg)
    # mutating our copy of the response must not rewrite what is in history
    resp["output"]["message"]["content"].append({"text": "injected later"})
    stored = msgs[1]
    injected = any(b.get("text") == "injected later" for b in stored.get("content", []))
    expect(not injected,
           "history changed when the response object was mutated afterwards — copy the message in")
