"""AGL-01 · Break phase.

Four situations that do not appear in tutorials. Each one has ended a real run.
"""
from harness import check, expect, expect_eq


@check("survives a tool that raises BaseException",
       "KeyboardInterrupt and SystemExit do not inherit from Exception.",
       teaches="`except Exception` misses these. A library that calls sys.exit() takes your agent with it.")
def t_base_exception(m):
    def rude(**_):
        raise SystemExit("a library called sys.exit()")

    r = m.dispatch({"toolUseId": "t", "name": "rude", "input": {}}, {"rude": rude})["toolResult"]
    expect_eq(r["status"], "error", "the loop must survive even a BaseException")


@check("survives a registry entry that is not callable",
       "Config errors put strings and None where functions should be.",
       teaches="`registry.get(name)` returning a non-callable passes a None check and fails at call time.")
def t_not_callable(m):
    r = m.dispatch({"toolUseId": "t", "name": "broken", "input": {}},
                   {"broken": "this is a string, not a function"})["toolResult"]
    expect_eq(r["status"], "error", "a non-callable entry is an error, not a crash")


@check("survives arguments the tool does not accept",
       "Models hallucinate parameter names.",
       teaches="A TypeError from **kwargs is the single most common dispatch crash in production.")
def t_bad_kwargs(m):
    r = m.dispatch({"toolUseId": "t", "name": "f", "input": {"wrong_name": 1}},
                   {"f": lambda booking_ref: booking_ref})["toolResult"]
    expect_eq(r["status"], "error", "an unexpected keyword must become an error result")
    text = " ".join(str(b.get("text", "")) for b in r["content"])
    expect(text.strip(), "tell the model what went wrong so it can retry with the right argument")


@check("never returns None",
       "Every dispatch must produce a block the loop can append.",
       teaches="A None return means the model asked a question and got no reply. It will answer anyway.")
def t_never_none(m):
    cases = [
        ({"toolUseId": "a", "name": "missing", "input": {}}, {}),
        ({"toolUseId": "b", "name": "f", "input": {}}, {"f": lambda: (_ for _ in ()).throw(RuntimeError("x"))}),
        ({"toolUseId": "c", "name": "f"}, {"f": lambda: 1}),
    ]
    for tu, reg in cases:
        out = m.dispatch(tu, reg)
        expect(out is not None, f"dispatch returned None for {tu['name']!r}")
        expect("toolResult" in out, "every path must return a toolResult block")
