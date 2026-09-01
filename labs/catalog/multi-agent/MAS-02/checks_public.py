from harness import check, expect, expect_eq
from _fixtures import spec, SINGLE, DELEGATION_2, DELEGATION_4, CRITIQUE_1, SWARM_UNBOUNDED


@check("a single agent is the baseline: H× is exactly 1.0")
def t_single(m):
    r = m.estimate_topology(SINGLE)
    expect_eq(r["h_multiple"], 1.0)
    expect_eq(r["total_tokens"], 2000)
    expect_eq(r["warnings"], [])


@check("delegation costs more than one agent")
def t_delegation(m):
    r = m.estimate_topology(DELEGATION_2)
    expect(r["h_multiple"] > 1.0, f"two specialists cannot cost 1x; got {r['h_multiple']}")


@check("the breakdown names orchestrator, handoffs and merge",
       "A total nobody can decompose is a number nobody can argue with.")
def t_breakdown(m):
    b = m.estimate_topology(DELEGATION_2)["breakdown"]
    for k in ("orchestrator", "handoffs", "merge"):
        expect(k in b, f"breakdown is missing {k!r}")
    expect_eq(sum(b.values()), m.estimate_topology(DELEGATION_2)["total_tokens"],
              "the components must sum to the total")


@check("the merge call grows with specialist count",
       "It carries every specialist's output.",
       teaches="The merge is the most expensive single call in a delegation, and it is invisible on the diagram.")
def t_merge_grows(m):
    two = m.estimate_topology(DELEGATION_2)["breakdown"]["merge"]
    four = m.estimate_topology(DELEGATION_4)["breakdown"]["merge"]
    expect(four > two, f"merge should grow with specialists: {two} -> {four}")


@check("a high H× produces a warning",
       "Above 4x, a reviewer will ask — so the estimator should ask first.")
def t_high_h(m):
    # five specialists on these numbers is unambiguously above 4x
    big = spec("delegation", specialists=5, orch_turns=5)
    r = m.estimate_topology(big)
    expect(r["h_multiple"] > 4,
           f"five specialists with five orchestrator turns should exceed 4x, got {r['h_multiple']}")
    expect(r["warnings"], "an H× above 4 must be flagged, not just reported")


@check("an unbounded swarm is warned about",
       "A swarm with no round cap does not terminate.",
       teaches="Cost cliff 3: unbounded topologies are the fastest way to spend a budget.")
def t_unbounded(m):
    r = m.estimate_topology(SWARM_UNBOUNDED)
    expect(r["warnings"], "rounds<=0 on a swarm must warn")
    expect(any("bound" in w.lower() or "cap" in w.lower() for w in r["warnings"]),
           f"the warning should name the missing bound: {r['warnings']}")
