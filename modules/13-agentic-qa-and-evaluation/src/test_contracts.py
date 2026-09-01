"""
test_contracts.py   (Topic 1, Layer 1 of the test pyramid)
==========================================================
The bottom, widest layer: TOOL-CONTRACT TESTS.

What this layer is:
    Plain pytest over the tool functions. No model. No AWS. Fully deterministic.
    These run on EVERY commit because they are instant and free.

What a "contract" means here:
    Each tool promises a SHAPE (which keys it returns) and a RANGE (which values
    are allowed). The agent is built on top of that promise. If a tool quietly
    starts returning a different shape or an unknown status, the agent will
    behave strangely and you will waste hours debugging the model when the model
    was never the problem. These tests catch that class of bug before the agent
    ever runs.

How to run:
    pip install pytest
    pytest test_contracts.py -v

You can run this right now with no cloud access. That is the whole point of
keeping tool logic in plain functions (see travelmind_agent.py).
"""

import pytest

# Import the PLAIN tool functions directly. No agent, no model is constructed,
# so this import does not touch AWS.
from travelmind_agent import (
    lookup_booking,
    get_disruption_reason,
    get_rebooking_options,
    VALID_STATUSES,
)


# ---------------------------------------------------------------------------
# lookup_booking
# ---------------------------------------------------------------------------

def test_lookup_returns_the_required_shape():
    """The found-booking contract: these four keys must always be present.
    `<=` on sets reads as 'is a subset of', so this asserts the required keys
    are a subset of what the tool returned (extra keys are allowed, missing
    keys fail)."""
    out = lookup_booking("JX48Q2")
    assert {"pnr", "status", "flight", "date"} <= set(out)
    assert out["pnr"] == "JX48Q2"


def test_lookup_normalises_lowercase_and_spaces():
    """Customers type 'jx 48 q2'. The tool must normalise to the canonical key,
    otherwise a valid booking looks like a miss. This guards the normalisation
    logic that lives in one place in travelmind_agent.py."""
    messy = lookup_booking("  jx 48 q2 ")
    assert messy["status"] == "CANCELLED"          # same record as "JX48Q2"
    assert messy["pnr"] == "JX48Q2"


@pytest.mark.parametrize("pnr", ["JX48Q2", "AB12CD", "DL99XY", "ZZZZZZ"])
def test_status_is_always_a_known_value(pnr):
    """Range contract: the status is never a surprise string. A typo in the
    backend ('CANCELED' vs 'CANCELLED') would be caught here. Parametrize runs
    this once per PNR, including the not-found one."""
    assert lookup_booking(pnr)["status"] in VALID_STATUSES


def test_unknown_pnr_is_an_explicit_miss_not_a_guess():
    """The most important contract for trust: an unknown PNR returns NOT_FOUND.
    It must NOT fabricate a flight. If this ever returns a flight number, the
    agent could confidently tell a customer about a booking that does not exist."""
    out = lookup_booking("ZZZZZZ")
    assert out["status"] == "NOT_FOUND"
    assert "flight" not in out                     # nothing invented


# ---------------------------------------------------------------------------
# get_disruption_reason
# ---------------------------------------------------------------------------

def test_disruption_reason_is_present_for_a_cancelled_booking():
    """A disrupted booking must come with a reason code and a customer-facing
    detail sentence, so the agent has something real to explain."""
    out = get_disruption_reason("JX48Q2")
    assert out["reason"] == "weather"
    assert out["detail"]                           # non-empty string


def test_no_reason_is_manufactured_for_a_confirmed_booking():
    """The inverse contract: a confirmed booking has reason None. The tool must
    not invent a disruption for a healthy booking."""
    out = get_disruption_reason("AB12CD")
    assert out["reason"] is None
    assert out["detail"] == ""


# ---------------------------------------------------------------------------
# get_rebooking_options
# ---------------------------------------------------------------------------

def test_rebooking_returns_a_list_with_the_agreed_fields():
    """Shape contract for the list elements: every option has a flight and a
    departure time. The agent formats these for the customer, so a missing key
    would break the reply."""
    opts = get_rebooking_options("JX48Q2")
    assert isinstance(opts, list) and len(opts) >= 1
    for option in opts:
        assert {"flight", "dep"} <= set(option)


def test_rebooking_is_an_empty_list_when_there_are_none():
    """An empty list is a valid, honest answer ('no options'). The tool must
    return [] rather than None, so the agent can iterate without a guard."""
    assert get_rebooking_options("AB12CD") == []


def test_callers_cannot_mutate_the_backing_data():
    """A subtle one. get_rebooking_options returns a COPY. If it returned the
    internal list, one caller appending to it would corrupt the data for the
    next caller. This test proves the isolation."""
    first = get_rebooking_options("JX48Q2")
    first.append({"flight": "XX-999", "dep": "00:00"})   # mutate the returned list
    second = get_rebooking_options("JX48Q2")
    assert all(o["flight"] != "XX-999" for o in second)  # the backend is untouched
