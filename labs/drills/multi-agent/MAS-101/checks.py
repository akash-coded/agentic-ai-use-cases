from harness import check, expect
def a(m): 
    v = getattr(m, "answer", None); expect(isinstance(v, (int, float)) and v is not None, f"answer must be a number, got {v!r}"); return float(v)

@check("answer is a number")
def t_num(m): a(m)

@check("the orchestrator's own reasoning turns are included",
       teaches="Three delegations means the orchestrator reasons three times. Omitting it gives 3.65 — a topology that looks half its real cost.")
def t_orch(m): expect(abs(a(m) - 3.65) > 0.05, "3.65 is the total without the orchestrator's reasoning turns")

@check("the merge call is included",
       teaches="The merge carries base context PLUS every specialist's result. Omitting it gives 5.20. It is the single most expensive call and the one diagrams hide.")
def t_merge(m): expect(abs(a(m) - 5.20) > 0.05, "5.20 is the total without the merge call")

@check("H× is 6.65", teaches="2000 + 6000 + 2400 + 2900 = 13 300 tokens; ÷ 2000 = 6.65×.")
def t_exact(m): expect(abs(a(m) - 6.65) < 0.02, f"expected 6.65, got {a(m)}")
