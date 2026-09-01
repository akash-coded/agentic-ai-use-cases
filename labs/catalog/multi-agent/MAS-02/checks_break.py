"""MAS-02 · Break phase — topologies that look reasonable and are not."""
from harness import check, expect, expect_eq
from _fixtures import spec


@check("handoff context larger than the base makes H× explode",
       "Passing the full context to every specialist.",
       teaches="This is what 'just give each agent everything' costs, and it scales with specialist count.")
def t_fat_handoff(m):
    lean = m.estimate_topology(spec("delegation", specialists=3, base=2000, handoff=400, orch_turns=3))
    fat = m.estimate_topology(spec("delegation", specialists=3, base=2000, handoff=2400, orch_turns=3))
    expect(fat["h_multiple"] > lean["h_multiple"] * 1.4,
           f"full-context handoffs should cost far more: {lean['h_multiple']} -> {fat['h_multiple']}")
    expect(fat["warnings"], "an H× this high must be flagged")


@check("a six-specialist delegation is flagged",
       "More specialists means more handoffs AND a bigger merge.",
       teaches="Specialist count hits the total twice; the second hit is the one people miss.")
def t_many_specialists(m):
    r = m.estimate_topology(spec("delegation", specialists=6, orch_turns=6))
    expect(r["h_multiple"] > 4, f"six specialists should exceed 4x; got {r['h_multiple']}")
    expect(r["warnings"], "and should warn")


@check("an unbounded critique loop warns",
       "Critique until convergence has no upper bound.",
       teaches="'Iterate until the critic accepts' is unbounded unless you cap the rounds.")
def t_unbounded_critique(m):
    r = m.estimate_topology(spec("critique", specialists=1, orch_turns=1, rounds=0))
    expect(r["warnings"], "an uncapped critique loop must warn")


@check("estimate_topology never raises on a partial spec",
       "Design-review inputs are always incomplete.",
       teaches="An estimator that needs every field cannot be used in the meeting where it matters.")
def t_partial(m):
    for s in ({}, {"shape": "delegation"}, {"shape": "swarm", "specialists": None, "rounds": None}):
        try:
            r = m.estimate_topology(s)
        except Exception as e:  # noqa: BLE001
            raise AssertionError(f"raised {type(e).__name__} on {s!r}") from None
        expect("h_multiple" in r and "breakdown" in r, "still a usable estimate")
