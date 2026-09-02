from harness import check, expect, expect_eq, expect_in

REG = {"get_booking": lambda booking_ref: {"ref": booking_ref}}

@check("the working paths still work")
def t_ok(m):
    r = m.dispatch({"toolUseId": "t", "name": "get_booking", "input": {"booking_ref": "X"}}, REG)["toolResult"]
    expect_eq(r["status"], "success"); expect_eq(r["content"][0]["json"], {"ref": "X"})

@check("bug 1 — an unknown tool no longer returns None",
       teaches="A None here means the model asked a question and got no reply. It answers anyway, from nothing.")
def t_unknown(m):
    r = m.dispatch({"toolUseId": "t", "name": "get_refund", "input": {}}, REG)
    expect(r is not None and "toolResult" in r, "an unknown tool must produce a toolResult block")
    expect_eq(r["toolResult"]["status"], "error")

@check("…and the message names the tools that exist",
       teaches="Without the list the model guesses again — usually the same wrong name.")
def t_names(m):
    r = m.dispatch({"toolUseId": "t", "name": "nope", "input": {}}, REG)["toolResult"]
    expect_in("get_booking", " ".join(b.get("text", "") for b in r["content"]))

@check("bug 2 — SystemExit from a tool no longer kills the loop",
       teaches="`except Exception` misses SystemExit and KeyboardInterrupt. A library calling sys.exit() takes the agent with it.")
def t_base(m):
    def rude(**_): raise SystemExit("a library quit")
    r = m.dispatch({"toolUseId": "t", "name": "rude", "input": {}}, {"rude": rude})
    expect(r is not None and r["toolResult"]["status"] == "error", "the loop must survive a BaseException")

@check("a hallucinated argument name becomes an error result, not a crash",
       teaches="TypeError from **args is the most common dispatch crash in production.")
def t_kwargs(m):
    r = m.dispatch({"toolUseId": "t", "name": "get_booking", "input": {"wrong": 1}}, REG)
    expect(r is not None and r["toolResult"]["status"] == "error", "unexpected keyword → error result")
