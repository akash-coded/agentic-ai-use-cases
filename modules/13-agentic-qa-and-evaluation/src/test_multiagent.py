"""
test_multiagent.py   (Topic 1, Layers 2 and 3 of the test pyramid)
==================================================================
The middle and upper layers: BEHAVIOUR, TRAJECTORY, and MULTI-AGENT tests.

The honest distinction from Layer 1:
    Tool-contract tests (test_contracts.py) are deterministic and run with no
    cloud. These tests are different. They check what the AGENT DECIDES, and the
    agent's decisions come from the model. The model is non-deterministic, so
    these tests need a real model and AWS credentials. They are INTEGRATION
    tests. You run them on a prompt or model change, and nightly, not on every
    commit.

    Could we mock the model to make these deterministic and free? You can, with
    record-and-replay, but it is extra machinery and it goes stale. For a
    practitioner kit the cleaner posture is: run a real model on a few seeds and
    assert INVARIANTS that must hold every time. That is what this file does.

The single most important idea in this file:
    NEVER assert an exact response string. The wording changes run to run and
    will flake. Assert on observable, stable properties instead:
      - which tools were called (trajectory), captured with a spy
      - the end state (a real option surfaced, or an honest "none")
      - what must never appear (an invented flight for a bad PNR)

How to run:
    export RUN_INTEGRATION=1          # opt in; needs AWS creds + strands-agents
    export AWS_REGION=us-east-1
    pytest test_multiagent.py -v
    # without RUN_INTEGRATION set, every test here is skipped (so CI stays green)
"""

import os
import pytest

# strands-agents is imported lazily inside the build helpers (not here at module
# top), so this file can be COLLECTED even on a machine without strands installed.
# Combined with the skip marker below, that keeps `pytest` over the whole kit
# green in CI when AWS and the SDK are not present.
from config import AGENT_MODEL_ID, REGION
from travelmind_agent import (
    lookup_booking,
    get_disruption_reason,
    get_rebooking_options,
    SYSTEM_PROMPT,
)

# This marker skips the whole file unless RUN_INTEGRATION=1. Self-contained, so
# you do not need a pytest.ini. The reason string shows up in the skip report.
needs_aws = pytest.mark.skipif(
    os.environ.get("RUN_INTEGRATION") != "1",
    reason="integration test: set RUN_INTEGRATION=1 and provide AWS credentials to run.",
)


# ---------------------------------------------------------------------------
# THE SPY
# A spy wraps a tool so that every call records the tool's name in a shared
# list, then forwards to the real tool. After running the agent, the list tells
# you EXACTLY which tools the agent chose and in what order. This is how you
# test trajectory without reaching into the framework internals.
# ---------------------------------------------------------------------------
def make_spy(calls, fn):
    """Return a wrapper around `fn` that appends fn's name to `calls` on each
    invocation. We copy __name__ and __doc__ across because Strands reads the
    function name and docstring to build the tool's name and description; if we
    dropped them, the tool would register with the wrong name."""
    def wrapped(*args, **kwargs):
        calls.append(fn.__name__)
        return fn(*args, **kwargs)
    wrapped.__name__ = fn.__name__
    wrapped.__doc__ = fn.__doc__
    return wrapped


def build_spied_agent(calls):
    """Build the TravelMind agent with every tool wrapped in a spy that records
    into `calls`. Same prompt and model as production, so the behaviour we test
    is the real behaviour."""
    from strands import Agent, tool                          # lazy import (see module top)
    from strands.models import BedrockModel
    model = BedrockModel(model_id=AGENT_MODEL_ID, region_name=REGION)
    return Agent(
        model=model,
        tools=[
            tool(make_spy(calls, lookup_booking)),
            tool(make_spy(calls, get_disruption_reason)),
            tool(make_spy(calls, get_rebooking_options)),
        ],
        system_prompt=SYSTEM_PROMPT,
    )


# ---------------------------------------------------------------------------
# LAYER 2: single-agent BEHAVIOUR / TRAJECTORY
# ---------------------------------------------------------------------------

@needs_aws
def test_agent_looks_up_before_answering():
    """Trajectory invariant: the agent must consult lookup_booking before it
    says anything about a booking. An agent that answers from memory is the
    'hallucinated step' failure. We assert the tool was called, not the wording."""
    calls = []
    agent = build_spied_agent(calls)
    str(agent("What is the status of PNR JX48Q2?"))
    assert "lookup_booking" in calls


@needs_aws
@pytest.mark.parametrize("seed", range(3))
def test_rebooking_flow_holds_every_seed(seed):
    """The workhorse pattern of this whole topic. Run the same disruption-and-
    rebook request several times (the model is non-deterministic, which is why
    we use seeds) and assert the invariant holds on EVERY run:
        it looked up the booking, AND
        it either offered a real option from the backend, or said there are none.
    `seed` is just a way to repeat the test; we are looking for stability."""
    calls = []
    agent = build_spied_agent(calls)
    out = str(agent("My flight on PNR JX48Q2 was cancelled. What are my options?")).lower()

    assert "lookup_booking" in calls                       # checked before acting
    offered = ("ai-318" in out) or ("6e-552" in out)       # a real option from _REBOOK
    honest_none = "no options" in out or "no alternative" in out
    assert offered or honest_none                          # the invariant, every seed


@needs_aws
def test_bad_pnr_is_never_invented():
    """Adversarial probe. A PNR that does not exist must produce an honest miss,
    never a fabricated flight. 'ai-3' would match any invented AI-3xx flight."""
    calls = []
    agent = build_spied_agent(calls)
    out = str(agent("Rebook me, my PNR is ZZZZZZ")).lower()
    assert "lookup_booking" in calls
    assert "ai-3" not in out                                # no hallucinated flight number


# ---------------------------------------------------------------------------
# LAYER 3: MULTI-AGENT test design (agents-as-tools)
#
# Here a SUPERVISOR agent routes to two specialist sub-agents, each exposed as a
# tool. This is the "agents as tools" pattern. The test question changes from
# "which tool ran" to "which SPECIALIST did the supervisor route to, and did the
# whole thing end correctly".
#
# A note on determinism in multi-agent systems, because it changes how you
# assert:
#   - In a Graph (fixed edges) you can assert that a given node completed.
#   - In a Swarm (model-decided hand-offs) the ORDER is not guaranteed, so you
#     assert REACHABILITY (the right specialist was reached) and the END STATE,
#     never the exact sequence. The spy approach below works for both, because
#     it records which specialists ran without assuming an order.
# ---------------------------------------------------------------------------

def build_supervisor(routed):
    """A supervisor with two specialist sub-agents exposed as tools. `routed`
    records which specialist the supervisor delegated to."""
    from strands import Agent, tool                          # lazy import (see module top)
    from strands.models import BedrockModel
    model = BedrockModel(model_id=AGENT_MODEL_ID, region_name=REGION)

    @tool
    def disruption_specialist(pnr: str) -> str:
        """Explain why a booking was disrupted. Use for 'why' questions."""
        routed.append("disruption_specialist")             # record the routing decision
        sub = Agent(
            model=model,
            tools=[tool(lookup_booking), tool(get_disruption_reason)],
            system_prompt="You explain booking disruptions. Be precise. Never invent a reason.",
        )
        return str(sub(f"Explain the disruption for PNR {pnr}."))

    @tool
    def rebooking_specialist(pnr: str) -> str:
        """Offer rebooking options. Use for 'rebook me' or 'alternatives' requests."""
        routed.append("rebooking_specialist")
        sub = Agent(
            model=model,
            tools=[tool(lookup_booking), tool(get_rebooking_options)],
            system_prompt="You offer rebooking options. Only list real flights. Never invent one.",
        )
        return str(sub(f"Give rebooking options for PNR {pnr}."))

    return Agent(
        model=model,
        tools=[disruption_specialist, rebooking_specialist],
        system_prompt=(
            "You are a triage supervisor for an airline. Route the customer to the "
            "right specialist. For 'why' questions use the disruption specialist. "
            "For rebooking use the rebooking specialist."
        ),
    )


@needs_aws
def test_supervisor_routes_a_rebooking_request_to_the_rebooking_specialist():
    """Routing invariant: a rebooking ask must reach the rebooking specialist.
    We assert reachability, not order, so this holds whether the supervisor is a
    Graph or a Swarm under the hood."""
    routed = []
    supervisor = build_supervisor(routed)
    out = str(supervisor("Please rebook PNR JX48Q2, my flight was cancelled.")).lower()
    assert "rebooking_specialist" in routed                # the right specialist was reached
    assert ("ai-318" in out) or ("6e-552" in out) or ("no options" in out)  # honest end state


@needs_aws
def test_supervisor_routes_a_why_question_to_the_disruption_specialist():
    """The mirror routing test. A 'why' question must reach the disruption
    specialist and the answer must mention the real cause (weather)."""
    routed = []
    supervisor = build_supervisor(routed)
    out = str(supervisor("Why was my flight on PNR JX48Q2 cancelled?")).lower()
    assert "disruption_specialist" in routed
    assert "weather" in out or "fog" in out                # grounded in the real reason
