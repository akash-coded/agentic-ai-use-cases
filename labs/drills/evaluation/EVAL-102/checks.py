from harness import check, expect, expect_eq
def a(m):
    v = getattr(m, "answer", None); expect(isinstance(v, list), f"answer must be a list, got {v!r}"); return {str(x).upper() for x in v}
@check("B — 59 of 60 passing at freeze is a mirror, not a measurement",
       teaches="A set built from cases the agent already passes measures the agent against itself. 96% is the arithmetic guaranteeing it.")
def t_b(m): expect("B" in a(m), "the set has almost no failing cases at freeze")
@check("C — 'unclear' cases were removed; that slice is the abstention slice",
       teaches="Cases where experts disagree are not noise to delete. They are the cases whose correct answer is 'I don't know'.")
def t_c(m): expect("C" in a(m), "there are no abstention cases")
@check("E — frozen after tuning means it measures the tuning",
       teaches="Freeze first, tune second. The other order produces a set that reflects current behaviour — which is the definition of a mirror.")
def t_e(m): expect("E" in a(m), "the set was finalised after the last tuning round")
@check("A is satisfied — real tickets, not invented cases",
       teaches="Sampling from real tickets is exactly right. Do not mark it as a violation.")
def t_a(m): expect("A" not in a(m), "A is satisfied")
@check("D is satisfied — adversarial cases include retrieved-content injection",
       teaches="Eight adversarial cases with two via retrieved documents meets the bar.")
def t_d(m): expect("D" not in a(m), "D is satisfied")
@check("exact")
def t_exact(m): expect_eq(a(m), {"B", "C", "E"})
