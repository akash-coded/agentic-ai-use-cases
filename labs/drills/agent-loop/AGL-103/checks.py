from harness import check, expect, expect_eq
def msg(*calls): return {"role": "assistant", "content": [{"toolUse": {"toolUseId": str(i), "name": n, "input": a}} for i, (n, a) in enumerate(calls)]}
@check("the same call twice is oscillation")
def t_same(m):
    s1 = m.call_signature(msg(("get_booking", {"ref": "X"}))); s2 = m.call_signature(msg(("get_booking", {"ref": "X"})))
    expect_eq(m.is_oscillating(s1, s2), True)
@check("the same tool with DIFFERENT arguments is progress, not oscillation",
       teaches="Fingerprinting on name alone punishes the self-correction your dispatcher asked for.")
def t_diff_args(m):
    s1 = m.call_signature(msg(("get_booking", {"ref": "WRONG"}))); s2 = m.call_signature(msg(("get_booking", {"ref": "XY7Q2M"})))
    expect_eq(m.is_oscillating(s1, s2), False)
@check("order of parallel calls does not matter",
       teaches="Models emit parallel calls in arbitrary order; a fingerprint that depends on it will miss real repeats.")
def t_order(m):
    s1 = m.call_signature(msg(("a", {}), ("b", {"k": 1}))); s2 = m.call_signature(msg(("b", {"k": 1}), ("a", {})))
    expect_eq(s1, s2, "same set of calls must give the same signature")
@check("a message with no tool calls is never oscillation",
       teaches="Two text-only turns in a row are the model thinking, not looping — treat () as 'no signal'.")
def t_empty(m):
    e = m.call_signature({"role": "assistant", "content": [{"text": "hmm"}]})
    expect_eq(e, ()); expect_eq(m.is_oscillating(e, e), False)
@check("signatures are hashable",
       teaches="You will keep these in a set or as dict keys to detect longer cycles later.")
def t_hash(m): hash(m.call_signature(msg(("a", {"k": [1, 2]}) if False else ("a", {"k": 1}))))
