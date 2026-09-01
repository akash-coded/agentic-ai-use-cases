from harness import check, expect, expect_eq
from _fixtures import spec, SINGLE, DELEGATION_2, CRITIQUE_1


@check("critique is forced to one specialist")
def t_critique(m):
    a = m.estimate_topology(CRITIQUE_1)
    b = m.estimate_topology(spec("critique", specialists=5, orch_turns=1, rounds=1))
    expect_eq(a["total_tokens"], b["total_tokens"],
              "critique is producer + critic; extra specialists do not apply")


@check("rounds multiply the handoff cost")
def t_rounds(m):
    one = m.estimate_topology(spec("swarm", specialists=3, orch_turns=1, rounds=1))
    three = m.estimate_topology(spec("swarm", specialists=3, orch_turns=1, rounds=3))
    expect(three["breakdown"]["handoffs"] > one["breakdown"]["handoffs"],
           "three rounds cost more handoff tokens than one")


@check("h_multiple is rounded to two decimal places")
def t_rounding(m):
    h = m.estimate_topology(DELEGATION_2)["h_multiple"]
    expect_eq(round(h, 2), h, f"{h} is not rounded to 2dp")


@check("a zero base context does not divide by zero")
def t_zero_base(m):
    r = m.estimate_topology(spec("delegation", specialists=2, base=0))
    expect(isinstance(r["h_multiple"], float), "return a float, do not raise")


@check("single never warns, whatever else is set")
def t_single_clean(m):
    r = m.estimate_topology(spec("single", specialists=9, rounds=0, base=100))
    expect_eq(r["warnings"], [], "a single agent has no topology to warn about")
