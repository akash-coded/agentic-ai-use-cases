"""PDL-01 · Break phase — candidates as stakeholders actually describe them."""
from harness import check, expect, expect_eq
from _fixtures import case


@check("'AI-powered intelligent document processing' is a script",
       "Sounds maximally agentic. Fixed pipeline, no language, no branching.",
       teaches="Buzzword density is uncorrelated with the rung a use case needs.")
def t_buzzwords(m):
    uc = case("AI-powered intelligent document processing pipeline", True, False, False, hot=0.95)
    expect_eq(m.classify(uc)["verdict"], "script",
              "the description is exciting; the control flow is a fixed pipeline")


@check("'just answer questions about our docs' can be an agent",
       "Sounds trivial. Which tool to call depends on what the last one returned.",
       teaches="Modest descriptions hide runtime branching more often than grand ones reveal it.")
def t_modest(m):
    uc = case("Just answer questions about our docs", False, True, True, hot=0.4)
    expect_eq(m.classify(uc)["verdict"], "agent")


@check("a 95% hot path on an agent is flagged for routing",
       "At that share, the agent is the exception path.",
       teaches="Nearly all traffic on one path means you built an agent to handle the 5%.")
def t_extreme_hot_path(m):
    uc = case("Refund desk, nearly all standard", False, True, True, hot=0.95)
    r = m.classify(uc)
    expect_eq(r["verdict"], "agent")
    expect_eq(r["route_hot_path"], True)
    expect(any("%" in x or "path" in x.lower() for x in r["reasons"]),
           "the reasons should mention the hot path, not just the flag")


@check("classify never raises on a partial description",
       "Discovery data is always incomplete.",
       teaches="A classifier that needs every field cannot be used in the conversation where it matters.")
def t_partial(m):
    for uc in ({}, {"name": "x"}, {"steps_known_upfront": None, "hot_path_share": None}):
        try:
            r = m.classify(uc)
        except Exception as e:  # noqa: BLE001
            raise AssertionError(f"raised {type(e).__name__} on {uc!r}") from None
        expect(r["verdict"] in ("script", "workflow", "agent"), "still a usable verdict")
