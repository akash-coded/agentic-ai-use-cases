from harness import check, expect, expect_eq
from _fixtures import NIGHTLY_RECONCILE, TICKET_SUMMARY, REFUND_DESK, ONBOARD_PACK, PAYMENT_AGENT


@check("known steps, no language, is a script")
def t_script(m):
    r = m.classify(NIGHTLY_RECONCILE)
    expect_eq(r["verdict"], "script")
    expect_eq(r["rung"], "R0")


@check("known steps with language is a workflow, not an agent",
       "A model inside fixed steps is still a workflow.",
       teaches="Using an LLM does not make something an agent. Choosing the steps does.")
def t_workflow(m):
    r = m.classify(TICKET_SUMMARY)
    expect_eq(r["verdict"], "workflow")
    expect_eq(r["rung"], "R2")


@check("branching on tool output is what makes an agent")
def t_agent(m):
    r = m.classify(REFUND_DESK)
    expect_eq(r["verdict"], "agent")
    expect_eq(r["rung"], "R3")


@check("a varying sequence without tool branching is still a workflow",
       "Apparent complexity is not autonomy.",
       teaches="This is the case most often mis-sold as an agent: complicated, but nothing decides at runtime.")
def t_complex_but_not_agent(m):
    expect_eq(m.classify(ONBOARD_PACK)["verdict"], "workflow")


@check("a dominant hot path is routed away from the agent",
       "The largest cost reduction available to most agents.")
def t_hot_path(m):
    expect_eq(m.classify(REFUND_DESK)["route_hot_path"], True, "72% is well above the 60% bar")
    expect_eq(m.classify(PAYMENT_AGENT)["route_hot_path"], False, "30% does not justify a second path")


@check("irreversible actions always produce a warning",
       "Whatever the rung.",
       teaches="An agent that can move money needs a human commit step, enforced in permissions.")
def t_irreversible(m):
    r = m.classify(PAYMENT_AGENT)
    expect(r["warnings"], "irreversible actions must be flagged")
    expect(any("human" in w.lower() or "commit" in w.lower() for w in r["warnings"]),
           f"the warning should name the mitigation: {r['warnings']}")


@check("reasons are never empty")
def t_reasons(m):
    for uc in (NIGHTLY_RECONCILE, TICKET_SUMMARY, REFUND_DESK, ONBOARD_PACK):
        r = m.classify(uc)
        expect(r["reasons"] and all(len(x) > 20 for x in r["reasons"]),
               f"{uc['name']}: verdict needs an explainable reason, got {r['reasons']}")
