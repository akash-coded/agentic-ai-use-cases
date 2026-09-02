from harness import check, expect, expect_eq
def a(m):
    v = getattr(m, "answer", None); expect(isinstance(v, list), f"answer must be a list, got {v!r}"); return [str(x) for x in v]
@check("starts at submitted", teaches="Acceptance is a state, not an implicit step.")
def t_start(m): expect_eq(a(m)[0], "submitted")
@check("passes through input-required when B needs the fare class",
       teaches="This is the state naïve clients mistake for a hang. B is waiting for YOU.")
def t_input(m): expect("input-required" in a(m), "B asked for more information")
@check("returns to working after A supplies the input", teaches="input-required is a pause, not a terminal state.")
def t_resume(m):
    v = a(m); i = v.index("input-required") if "input-required" in v else -1
    expect(i >= 0 and i + 1 < len(v) and v[i + 1] == "working", "after input is supplied, B works again")
@check("ends at completed")
def t_end(m): expect_eq(a(m)[-1], "completed")
@check("exact")
def t_exact(m): expect_eq(a(m), ["submitted", "working", "input-required", "working", "completed"])
