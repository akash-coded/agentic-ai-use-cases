"""
travelmind_agent.py
===================
The SYSTEM UNDER TEST (SUT). This is the agent every other file in the kit
tests, evaluates, observes, and gates. Read this file first.

TravelMind is a booking-exception assistant for an airline. A customer asks
about a disrupted booking; the agent looks up the PNR, explains the disruption,
and offers rebooking options.

Two design choices in this file exist specifically to make QA possible.
They are worth understanding before you read the tests.

  1. TOOL LOGIC LIVES IN PLAIN FUNCTIONS.
     The three tools are ordinary Python functions. The agent wraps them with
     `tool(...)` at wiring time (see build_agent). Because the logic is plain,
     test_contracts.py can call it directly with no model and no AWS. If we had
     decorated the functions in place, they would be agent-callable but awkward
     to unit test. Separating "what the tool does" from "registering it as a
     tool" is the move that makes the bottom of the test pyramid cheap.

  2. THE AGENT IS BUILT LAZILY.
     Importing this file must NOT require AWS credentials, because the contract
     tests import the tool functions from here and run in CI with no cloud
     access. So the Bedrock-backed agent is created only when get_agent() is
     called, not at import time.

In production the tools would call the real airline API. Here they read a small
in-memory dictionary. That is deliberate: the thing we are testing is the
AGENT'S REASONING (did it look up before answering, did it avoid inventing a
flight), not the airline backend. A fixed backend also makes tests repeatable.
"""

# ---------------------------------------------------------------------------
# In-memory backend. Stands in for the airline API. Fixed, so tests are stable.
# Different PNRs deliberately have different statuses so the tests can exercise
# every branch: a cancellation, a confirmed booking, a delay, and a miss.
# ---------------------------------------------------------------------------
_BOOKINGS = {
    "JX48Q2": {"status": "CANCELLED", "flight": "AI-302", "date": "2026-06-12", "reason": "weather"},
    "AB12CD": {"status": "CONFIRMED", "flight": "6E-220", "date": "2026-06-20", "reason": None},
    "DL99XY": {"status": "DELAYED",   "flight": "AI-415", "date": "2026-06-14", "reason": "crew"},
}

# Human-readable detail for each disruption reason code.
_REASON_DETAIL = {
    "weather": "Heavy fog at the origin airport.",
    "crew":    "Crew duty-time limit reached.",
}

# Alternative flights offered for a disrupted PNR. A confirmed booking has none.
_REBOOK = {
    "JX48Q2": [{"flight": "AI-318", "dep": "18:40"}, {"flight": "6E-552", "dep": "21:15"}],
    "DL99XY": [{"flight": "AI-417", "dep": "20:05"}],
}

# The set of statuses the backend can ever return. The contract test asserts the
# agent's tools never produce anything outside this set. Surprise values are bugs.
VALID_STATUSES = {"CONFIRMED", "CANCELLED", "DELAYED", "NOT_FOUND"}


def _normalise_pnr(pnr: str) -> str:
    """Customers type PNRs in lower case and with stray spaces. Normalise once,
    here, so every tool sees a clean key. Centralising this avoids three slightly
    different cleanups drifting apart in three tools."""
    return pnr.strip().upper().replace(" ", "")


# ---------------------------------------------------------------------------
# TOOL 1: lookup_booking
# Plain function. Tested directly in test_contracts.py.
# ---------------------------------------------------------------------------
def lookup_booking(pnr: str) -> dict:
    """Look up a booking by its PNR code.

    Args:
        pnr: the 6-character booking reference, e.g. "JX48Q2".

    Returns:
        A dict with keys pnr, status, and (when found) flight and date.
        An unknown PNR returns status "NOT_FOUND" rather than raising or, worse,
        inventing a booking. That explicit miss is itself part of the contract:
        the agent must be able to say "I could not find that PNR".
    """
    key = _normalise_pnr(pnr)
    if key not in _BOOKINGS:
        return {"pnr": key, "status": "NOT_FOUND"}          # explicit miss, never a guess
    b = _BOOKINGS[key]
    return {"pnr": key, "status": b["status"], "flight": b["flight"], "date": b["date"]}


# ---------------------------------------------------------------------------
# TOOL 2: get_disruption_reason
# ---------------------------------------------------------------------------
def get_disruption_reason(pnr: str) -> dict:
    """Explain why a booking was delayed or cancelled.

    Returns a dict with pnr, reason (a short code or None), and detail (a
    customer-facing sentence, or empty when there is no disruption). A confirmed
    booking has reason None; the agent should not manufacture a reason for it.
    """
    key = _normalise_pnr(pnr)
    record = _BOOKINGS.get(key)
    if not record or not record.get("reason"):
        return {"pnr": key, "reason": None, "detail": ""}    # no disruption to explain
    reason = record["reason"]
    return {"pnr": key, "reason": reason, "detail": _REASON_DETAIL.get(reason, "")}


# ---------------------------------------------------------------------------
# TOOL 3: get_rebooking_options
# ---------------------------------------------------------------------------
def get_rebooking_options(pnr: str) -> list:
    """Return alternative flights for a disrupted booking.

    Always returns a list. An empty list means "no options found", which is a
    valid, honest answer. The agent must surface a real option from this list or
    say there are none; it must never invent a flight number.
    """
    key = _normalise_pnr(pnr)
    return list(_REBOOK.get(key, []))                        # copy, so callers cannot mutate ours


# ---------------------------------------------------------------------------
# THE AGENT
# Built lazily. Needs AWS credentials and the strands-agents package.
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are TravelMind, a booking-exception assistant for an airline. "
    "Always look up the PNR before answering. "
    "If the booking is disrupted, explain why and offer rebooking options. "
    "If the PNR is not found, say so plainly. "
    "Never invent a PNR, a flight number, or a policy."
)

# Module-level handle, populated by get_agent() on first use.
_agent = None


def build_agent(model_id=None, region=None):
    """Construct a fresh TravelMind agent. Import the heavy SDK inside the
    function so that importing this module (for the contract tests) does not
    require strands-agents or AWS credentials to be present."""
    from strands import Agent, tool                          # imported lazily on purpose
    from strands.models import BedrockModel
    from config import AGENT_MODEL_ID, REGION

    model = BedrockModel(
        model_id=model_id or AGENT_MODEL_ID,
        region_name=region or REGION,
    )
    return Agent(
        model=model,
        # tool(fn) wraps a plain function as an agent-callable tool. This is the
        # "decorate at wiring time" pattern that kept the functions unit-testable.
        tools=[tool(lookup_booking), tool(get_disruption_reason), tool(get_rebooking_options)],
        system_prompt=SYSTEM_PROMPT,
    )


def get_agent():
    """Return a shared agent instance, building it once on first call.
    Use this from the eval and observability files."""
    global _agent
    if _agent is None:
        _agent = build_agent()
    return _agent


def set_system_prompt(prompt: str):
    """Swap the system prompt and force a rebuild on next get_agent().
    Used by the prompt-regression demo in eval_harness.ipynb to compare two
    prompt versions on the same golden set."""
    global SYSTEM_PROMPT, _agent
    SYSTEM_PROMPT = prompt
    _agent = None                                            # invalidate, so the new prompt takes effect


if __name__ == "__main__":
    # A tiny smoke test of the TOOLS only (no model, no AWS), so you can run
    # `python travelmind_agent.py` and confirm the backend behaves.
    print("lookup CANCELLED :", lookup_booking("jx48q2"))   # lower case on purpose: normalisation
    print("lookup NOT_FOUND :", lookup_booking("ZZZZZZ"))
    print("reason weather   :", get_disruption_reason("JX48Q2"))
    print("reason none      :", get_disruption_reason("AB12CD"))
    print("rebook options   :", get_rebooking_options("JX48Q2"))
    print("rebook none      :", get_rebooking_options("AB12CD"))
