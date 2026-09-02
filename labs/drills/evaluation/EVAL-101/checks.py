from harness import check, expect, expect_eq
TH = {"min_pass_rate": 0.85, "min_safety_rate": 1.0, "max_uncited_claims": 0, "max_cost_usd": 0.08}
def rep(pr=0.9, s=1.0, u=0, c=0.03): return {"evals": {"pass_rate": pr, "safety_pass_rate": s, "uncited_claims": u}, "obs": {"cost_usd": c}}

@check("blank 1 — pass rate is an average", teaches="0.85 is an explicit statement that ~1 in 7 may be wrong. That is an average by definition.")
def t_b1(m): expect_eq(dict((b[0], b[4]) for b in m.BARS)["min_pass_rate"], "average")

@check("blank 2 — safety is absolute", teaches="A policy-contradicting answer reaching a user is not a rounding error, whatever the other 129 cases did.")
def t_b2(m): expect_eq(dict((b[0], b[4]) for b in m.BARS)["min_safety_rate"], "absolute")

@check("blank 3 — uncited claims are absolute", teaches="'Only one uncited claim' is still an ungrounded answer reaching a user.")
def t_b3(m): expect_eq(dict((b[0], b[4]) for b in m.BARS)["max_uncited_claims"], "absolute")

@check("blank 4 — a safety breach sorts before an average breach",
       teaches="CI logs are read top-down under pressure. A safety failure at position four is a safety failure nobody read.")
def t_b4(m):
    r = m.evaluate_gate(rep(pr=0.5, s=0.99, c=0.5), TH)
    expect_eq(r["decision"], "block"); expect(r["breaches"], "expected breaches")
    expect_eq(r["breaches"][0]["metric"], "min_safety_rate", f"first breach should be safety, got {r['breaches'][0]['metric']}")

@check("excellent on average, one safety failure — still blocked")
def t_hidden_failure(m):
    expect_eq(m.evaluate_gate(rep(pr=0.99, s=0.995, u=0, c=0.01), TH)["decision"], "block")
