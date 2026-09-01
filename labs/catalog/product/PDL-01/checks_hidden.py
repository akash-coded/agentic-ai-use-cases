from harness import check, expect, expect_eq
from _fixtures import case, REFUND_DESK


@check("hot path exactly at the bar routes")
def t_boundary(m):
    expect_eq(m.classify(case("x", False, True, True, hot=0.6))["route_hot_path"], True)


@check("a workflow never routes a hot path",
       teaches="Routing around a workflow is meaningless — it has no expensive path to avoid.")
def t_workflow_no_route(m):
    expect_eq(m.classify(case("x", True, True, False, hot=0.9))["route_hot_path"], False)


@check("missing fields default to the least autonomous reading",
       teaches="An unanswered question should not silently promote a use case up the ladder.")
def t_defaults(m):
    r = m.classify({"name": "unspecified"})
    expect(r["verdict"] in ("script", "workflow"), f"got {r['verdict']!r} from an empty description")


@check("every verdict maps to a plausible rung")
def t_rungs(m):
    valid = {"script": {"R0"}, "workflow": {"R1", "R2"}, "agent": {"R3", "R4"}}
    for uc in (case("a", True, False, False), case("b", True, True, False),
               case("c", False, True, True)):
        r = m.classify(uc)
        expect(r["rung"] in valid[r["verdict"]],
               f"{r['verdict']} should not be {r['rung']}")


@check("an agent verdict always carries a permissions warning")
def t_agent_warning(m):
    r = m.classify(REFUND_DESK)
    expect(r["warnings"], "an agent verdict should say something about tool permissions")
