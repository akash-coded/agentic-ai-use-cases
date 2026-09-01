from harness import check, expect, expect_eq, expect_not_in


@check("the failure message does not leak a stack trace")
def t_no_trace(m):
    def boom(**_):
        raise ValueError("inner detail")

    r = m.dispatch({"toolUseId": "t", "name": "boom", "input": {}}, {"boom": boom})["toolResult"]
    text = " ".join(str(b.get("text", "")) for b in r["content"])
    expect_not_in("Traceback", text, "send the model a sentence, not a Python traceback")


@check("a missing 'input' key is treated as no arguments",
       teaches="Models omit `input` for zero-argument tools. Crashing on it is a self-inflicted bug.")
def t_missing_input(m):
    r = m.dispatch({"toolUseId": "t", "name": "ping"}, {"ping": lambda: "pong"})["toolResult"]
    expect_eq(r["status"], "success", "a tool with no arguments must still dispatch")
    expect_eq(r["content"][0]["json"], "pong")


@check("an empty registry still produces a usable error")
def t_empty_registry(m):
    r = m.dispatch({"toolUseId": "t", "name": "anything", "input": {}}, {})["toolResult"]
    expect_eq(r["status"], "error")
    text = " ".join(str(b.get("text", "")) for b in r["content"])
    expect(len(text.strip()) > 0, "say something useful even when nothing is registered")


@check("the result shape is exactly what Converse expects",
       teaches="A shape the API rejects fails at the next turn, far from the cause.")
def t_shape(m):
    r = m.dispatch({"toolUseId": "t", "name": "f", "input": {}}, {"f": lambda: 1})
    expect_eq(list(r.keys()), ["toolResult"], "the block is wrapped in a single 'toolResult' key")
    tr = r["toolResult"]
    for k in ("toolUseId", "content", "status"):
        expect(k in tr, f"toolResult is missing {k!r}")
    expect(isinstance(tr["content"], list) and tr["content"], "content must be a non-empty list")
    expect(tr["status"] in ("success", "error"), "status is 'success' or 'error'")


@check("a tool returning None is still a success",
       teaches="None is a legitimate return. Treating it as failure hides working tools.")
def t_none(m):
    r = m.dispatch({"toolUseId": "t", "name": "f", "input": {}}, {"f": lambda: None})["toolResult"]
    expect_eq(r["status"], "success", "returning None is not an error")
