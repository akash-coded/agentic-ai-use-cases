"""
travelmind_agent.py
===================
The TravelMind booking-exception agent. This is the thing we deploy, version,
and route in the rest of the kit. Nothing here is new from your build days; it
is collected in one file so every notebook and script can import it.

Design choices that matter downstream:
  - The three TOOLS are plain Python functions with no AWS dependency. That
    means you can test them, and test the agent's logic, with zero credentials.
  - build_agent() is the only thing that imports Strands and touches Bedrock.
    The import is lazy (inside the function), so importing this module never
    forces an AWS call or even requires strands to be installed.
  - A tiny in-memory backend stands in for a real reservation system, so the
    whole kit runs offline.

Model default: Haiku 4.5 (fast and cheap). Swap to Sonnet for harder tasks by
changing one string (see MODEL_ID below).
"""

# ----------------------------------------------------------------------------
# Config you might change. Kept at the top so it is easy to find.
# ----------------------------------------------------------------------------
MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"   # agent model
REGION = "us-east-1"

# The us. prefix is the cross-region inference profile. On-demand Claude models
# MUST be called through it. Dropping the prefix is the classic 404 (see the
# deploy runbook). Keep it.

SYSTEM_PROMPT = (
    "You are TravelMind, an airline booking-exception assistant. "
    "Always look up the PNR before answering. "
    "When a booking is disrupted, explain why and offer rebooking options. "
    "Never invent a PNR, a flight number, or a policy."
)

# ----------------------------------------------------------------------------
# In-memory backend (stands in for a reservation system).
# Three PNRs cover the cases the tools need to handle.
# ----------------------------------------------------------------------------
_BOOKINGS = {
    # pnr     : (status,      flight,   disruption_reason)
    "JX48Q2": ("CANCELLED", "AI-302", "weather"),
    "AB12CD": ("CONFIRMED", "6E-220", None),
    "DL99XY": ("DELAYED",   "AI-415", "crew"),
}

_REBOOKING = {
    # only disrupted bookings have alternatives offered
    "JX48Q2": [{"flight": "AI-318", "dep": "18:40"},
               {"flight": "6E-552", "dep": "21:15"}],
    "DL99XY": [{"flight": "AI-415", "dep": "20:05"}],
}


def _norm(pnr):
    """Normalise user input: strip spaces, upper-case. 'jx 48 q2' -> 'JX48Q2'."""
    return (pnr or "").strip().upper().replace(" ", "")


# ----------------------------------------------------------------------------
# THE TOOLS. Plain functions. Each returns a small, fixed-shape dict/list so it
# is easy to test and so the model gets predictable structure back.
# ----------------------------------------------------------------------------
def lookup_booking(pnr: str) -> dict:
    """Look up a booking by PNR. Returns status and flight, or NOT_FOUND.

    Shape: {"pnr", "status", "flight"} where status is one of
    CONFIRMED | CANCELLED | DELAYED | NOT_FOUND. A bad PNR never invents a flight.
    """
    k = _norm(pnr)
    if k not in _BOOKINGS:
        return {"pnr": k, "status": "NOT_FOUND"}
    status, flight, _ = _BOOKINGS[k]
    return {"pnr": k, "status": status, "flight": flight}


def get_disruption_reason(pnr: str) -> dict:
    """Why is this booking disrupted? Returns reason=None for a healthy booking."""
    k = _norm(pnr)
    if k not in _BOOKINGS:
        return {"pnr": k, "reason": None, "detail": "PNR not found"}
    _, _, reason = _BOOKINGS[k]
    return {"pnr": k, "reason": reason, "detail": ("disruption: " + reason) if reason else "no disruption"}


def get_rebooking_options(pnr: str) -> list:
    """Alternative flights for a disrupted booking. Empty list means none."""
    return list(_REBOOKING.get(_norm(pnr), []))


# ----------------------------------------------------------------------------
# THE AGENT. Built lazily so importing this module is free (no AWS, no strands).
# ----------------------------------------------------------------------------
def build_agent():
    """Construct the Strands agent. Imports Strands here, not at module load.

    The tools are wrapped with tool() at wiring time. Keeping the raw functions
    undecorated above is deliberate: you can unit-test them directly, and you
    decide here which functions become tools.
    """
    from strands import Agent, tool                  # lazy import
    from strands.models import BedrockModel

    model = BedrockModel(
        model_id=MODEL_ID,
        region_name=REGION,
        temperature=0.2,        # low: this is an operational assistant, not a poet
        max_tokens=1024,
    )
    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            tool(lookup_booking),
            tool(get_disruption_reason),
            tool(get_rebooking_options),
        ],
    )


# Lazy singleton so callers can do `from travelmind_agent import get_agent`.
_AGENT = None


def get_agent():
    """Return a single shared agent instance, building it on first use."""
    global _AGENT
    if _AGENT is None:
        _AGENT = build_agent()
    return _AGENT


# ----------------------------------------------------------------------------
# Offline stand-in for the agent. Lets every notebook run end to end with no
# credentials. It is NOT the model; it is a deterministic script over the same
# tools, so the shape of the answer is realistic.
# ----------------------------------------------------------------------------
def _find_pnr(text: str) -> str:
    """Pull a PNR out of free text. PNRs here are 6-char alphanumeric.

    Prefer a 6-char run containing a digit (JX48Q2, AB12CD, DL99XY). Otherwise
    accept a 6-char ALL-CAPS run (e.g. a bad PNR like ZZZZZZ), which avoids
    matching ordinary words like 'status' or 'rebook'.
    """
    import re
    cands = re.findall(r"[A-Za-z0-9]{6}", text or "")
    for tok in cands:
        if any(c.isdigit() for c in tok):
            return tok.upper()
    for tok in cands:
        if tok.isupper() and tok.isalpha():
            return tok.upper()
    return ""


def mock_agent(text: str) -> str:
    """A deterministic fake agent: find a PNR in the text, run the tools, reply.

    Use this anywhere LIVE is False. Swap to get_agent() when you have AWS creds.
    """
    pnr = _find_pnr(text)
    if not pnr:
        return "Please share your PNR (six characters) so I can look it up."
    bk = lookup_booking(pnr)
    if bk["status"] == "NOT_FOUND":
        return f"I could not find PNR {pnr}. Please double-check it."
    if bk["status"] == "CONFIRMED":
        return f"PNR {pnr} is confirmed on flight {bk['flight']}. Nothing to action."
    reason = get_disruption_reason(pnr)["reason"]
    opts = get_rebooking_options(pnr)
    if opts:
        opt_txt = ", ".join(f"{o['flight']} at {o['dep']}" for o in opts)
        return (f"PNR {pnr} is {bk['status'].lower()} due to {reason}. "
                f"Rebooking options: {opt_txt}.")
    return f"PNR {pnr} is {bk['status'].lower()} due to {reason}. No alternatives are available right now."


if __name__ == "__main__":
    # Quick offline self-check. Runs with no AWS.
    for q in ["Status of PNR JX48Q2?", "Rebook JX48Q2", "Is AB12CD ok?", "Check ZZZZZZ"]:
        print(q, "->", mock_agent(q))
