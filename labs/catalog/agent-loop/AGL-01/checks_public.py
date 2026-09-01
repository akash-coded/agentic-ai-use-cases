from harness import check, expect, expect_eq, expect_in


def _registry():
    return {
        "get_booking": lambda booking_ref: {"ref": booking_ref, "status": "CANCELLED"},
        "get_fare_rules": lambda fare_class: {"class": fare_class, "refundable": True},
    }


@check("carries the toolUseId through unchanged",
       "The id is how the model matches your reply to its request.")
def t_id(m):
    r = m.dispatch({"toolUseId": "tu_42", "name": "get_booking",
                    "input": {"booking_ref": "XY7Q2M"}}, _registry())
    expect_eq(r["toolResult"]["toolUseId"], "tu_42", "toolUseId must be echoed exactly")


@check("calls the tool and returns its value as a success result",
       "status success, and the return value under content[0]['json'].")
def t_success(m):
    r = m.dispatch({"toolUseId": "tu_1", "name": "get_booking",
                    "input": {"booking_ref": "XY7Q2M"}}, _registry())["toolResult"]
    expect_eq(r["status"], "success", "a working tool call is a success")
    expect_eq(r["content"][0]["json"], {"ref": "XY7Q2M", "status": "CANCELLED"},
              "the tool's return value belongs in content[0]['json']")


@check("passes input as keyword arguments",
       "The model sends a dict of named arguments, not positional ones.")
def t_kwargs(m):
    seen = {}

    def probe(**kw):
        seen.update(kw)
        return "ok"

    m.dispatch({"toolUseId": "tu_2", "name": "probe", "input": {"a": 1, "b": "two"}},
               {"probe": probe})
    expect_eq(seen, {"a": 1, "b": "two"}, "arguments must arrive as **kwargs")


@check("an unknown tool becomes an error result, not an exception",
       "The loop must survive the model inventing a tool.",
       teaches="Raising here turns a recoverable turn into an outage.")
def t_unknown(m):
    r = m.dispatch({"toolUseId": "tu_3", "name": "get_refund_status", "input": {}},
                   _registry())["toolResult"]
    expect_eq(r["status"], "error", "an unknown tool is an error result")


@check("the unknown-tool message names the tools that do exist",
       "This is what lets the model correct itself on the next turn.",
       teaches="Without the list, the model guesses again — usually the same wrong name.")
def t_unknown_names(m):
    r = m.dispatch({"toolUseId": "tu_4", "name": "nope", "input": {}}, _registry())["toolResult"]
    text = " ".join(str(b.get("text", "")) for b in r["content"])
    expect_in("get_booking", text, "the available tools must be named in the message")
    expect_in("get_fare_rules", text, "list every registered tool, not just one")


@check("a tool that raises becomes an error result",
       "One failing tool must not kill the loop.",
       teaches="An escaping exception ends the run; an error result lets the agent abstain honestly.")
def t_raises(m):
    def boom(**_):
        raise TimeoutError("upstream took too long")

    r = m.dispatch({"toolUseId": "tu_5", "name": "boom", "input": {}}, {"boom": boom})["toolResult"]
    expect_eq(r["status"], "error", "a raising tool is an error result, not a crash")
    text = " ".join(str(b.get("text", "")) for b in r["content"])
    expect(len(text.strip()) > 0, "the error result needs a message the model can read")
